import pandas as pd
import databrickstest
import glob
from tempfile import TemporaryDirectory
from pandas.testing import assert_frame_equal


def test_etl():
    with databrickstest.session() as dbrickstest:
        with TemporaryDirectory() as tmp_dir:
            out_dir = f"{tmp_dir}/out"

            # Provide input and output location as widgets to notebook
            switch = {
                "training": "tests/unit/data_preparation_data/",
                "prepped_data": out_dir,
            }
            dbrickstest.dbutils.widgets.get.side_effect = lambda x: switch.get(
                x, "")

            # Run notebook
            dbrickstest.run_notebook("code/prepare", "data_preparation")

            # Notebook produces a directory with a single CSV file
            csv_files = glob.glob(f"{out_dir}/*.csv")
            assert len(csv_files) == 1
            resultDF = pd.read_csv(csv_files[0])

        # Compare produced Parquet file and expected CSV file
        expectedDF = pd.read_csv("tests/unit/data_preparation_expected.csv")
        assert_frame_equal(expectedDF, resultDF, check_dtype=False)

# Databricks notebook source
# This notebook processes the files in the input dataset
# and computes a cleaned rectangular feature dataset.
from azureml.core import Run
import pyspark.sql.functions as F

# COMMAND ----------

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databrickstest
    databrickstest.inject_variables()

# COMMAND ----------

# Widgets for interactive development. Values are automatically passed when run in Azure ML.
# In interactive development, use Databricks CLI to provision the proper secrets.
dbutils.widgets.text("secretscope", "training")
dbutils.widgets.text(
    "training", "wasbs://trainingdata@stmlopssampledev.blob.core.windows.net/"
)
dbutils.widgets.text(
    "training_blob_config",
    "fs.azure.account.key.stmlopssampledev.blob.core.windows.net",
)
dbutils.widgets.text(
    "training_blob_secretname", "account_key"
)
dbutils.widgets.text(
    "prepped_data", "wasbs://preppeddata@stmlopssampledev.blob.core.windows.net/"
)
dbutils.widgets.text(
    "prepped_data_blob_config",
    "fs.azure.account.key.stmlopssampledev.blob.core.windows.net"
)
dbutils.widgets.text(
    "prepped_data_blob_secretname", "account_key"
)

# COMMAND ----------

# Connect to Azure ML
dbutils.library.installPyPI(
    "azureml-sdk",
    version="1.0.79",
    extras="databricks")
# In an Azure ML run, settings get imported from passed `--AZUREML_*` parameters
run = Run.get_context()

# COMMAND ----------

# Set up storage credentials

spark.conf.set(
    dbutils.widgets.get("training_blob_config"),
    dbutils.secrets.get(
        scope=dbutils.widgets.get("secretscope"),
        key=dbutils.widgets.get("training_blob_secretname")
    ),
)

spark.conf.set(
    dbutils.widgets.get("prepped_data_blob_config"),
    dbutils.secrets.get(
        scope=dbutils.widgets.get("secretscope"),
        key=dbutils.widgets.get("prepped_data_blob_secretname")
    ),
)

# COMMAND ----------

in_dir = dbutils.widgets.get('training')

# COMMAND ----------

# Read data file with healthcare provider information
info = (
    spark.read.format("csv")
    .options(header="true", mode="FAILFAST")
    .load(f"{in_dir}/Inpatient_Rehabilitation_Facility_-_General_Information.csv.gz")
    .withColumnRenamed("CMS Certification Number (CCN)", "CCN")
    .cache())
# Display data for one provider
display(info.filter(info.CCN == "363038"))

# COMMAND ----------

# Read data file with number of patients by condition for healthcare providers
conditions = (
    spark.read.format("csv")
    .options(header="true", mode="FAILFAST")
    .load(f"{in_dir}/Inpatient_Rehabilitation_Facility_-_Conditions.csv.gz")
    .withColumnRenamed("CMS Certification Number (CCN)", "CCN")
    .cache())
# Display data for one provider
display(conditions.filter(conditions.CCN == "363038"))

# COMMAND ----------

# Read data file with scores for healthcare providers
provider = (
    spark.read.format("csv")
    .options(header="true", mode="FAILFAST")
    .load(f"{in_dir}/Inpatient_Rehabilitation_Facility_-_Provider_Data.csv.gz")
    .withColumnRenamed("CMS Certification Number (CCN)", "CCN")
    .cache())
# Display data for one provider
display(provider.filter(provider.CCN == "363038"))

# COMMAND ----------

# Pivot scores to rectangular format
metric_score = (provider
                .groupBy("CCN")
                .pivot("Measure Code")
                .agg(F.expr("first(double(Score))"))
                .withColumnRenamed("I_020_01_MSPB_SCORE_NATL", "Medicare Spending Per Beneficiary")
                )
display(metric_score.filter(metric_score.CCN == "363038"))

# COMMAND ----------

# Pivot number of patients by condition to rectangular format
condition_counts = conditions.groupBy("CCN").pivot(
    "Condition").agg(F.expr("coalesce(first(int(Count)), 0)"))
display(condition_counts.filter(
    condition_counts.CCN == "363038"))

# COMMAND ----------

# Join all three datasets
joined_df = (info
             .select("CCN", "State", "Ownership Type")
             .join(metric_score, ["CCN"])
             .join(condition_counts, ["CCN"])
             )
display(joined_df.filter(joined_df.CCN == "363038"))

# COMMAND ----------

run.log("DatasetSize", joined_df.count())

# COMMAND ----------

# Write out Parquet data
(joined_df
    .repartition(1)
    .write
    .option("header", "true")
    .csv(dbutils.widgets.get('prepped_data'))
 )

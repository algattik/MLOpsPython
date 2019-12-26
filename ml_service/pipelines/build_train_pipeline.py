from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep, DatabricksStep
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.core import Workspace
from azureml.core.runconfig import RunConfiguration, CondaDependencies
from azureml.core.datastore import Datastore
from azureml.data.data_reference import DataReference
from azure.common.credentials import get_azure_cli_credentials
from azure.mgmt.storage import StorageManagementClient
import os
import sys
import requests

sys.path.append(os.path.abspath("./ml_service/util"))  # NOQA: E402
from attach_compute import get_compute, get_databricks_compute
from env_variables import Env
from databricks_client import DatabricksClient


def main():
    """
    Builds the Azure ML pipeline for data engineering and model training.
    """

    e = Env()

    # Get Azure machine learning workspace
    aml_workspace = Workspace.get(
        name=e.workspace_name,
        subscription_id=e.subscription_id,
        resource_group=e.resource_group
    )
    print(aml_workspace)

    # Create a datastore for the training data container
    credentials, subscription = get_azure_cli_credentials()
    storage_client = StorageManagementClient(credentials, subscription)
    storage_keys = storage_client.storage_accounts.list_keys(
        e.resource_group, e.training_account_name
    )
    storage_key = storage_keys.keys[0].value
    blob_datastore = Datastore.register_azure_blob_container(
        workspace=aml_workspace,
        datastore_name=e.training_datastore_name,
        container_name=e.training_container_name,
        account_name=e.training_account_name,
        account_key=storage_key,
    )

    # Attach Databricks as Azure ML training compute
    dbricks_compute = get_databricks_compute(
        aml_workspace, e.databricks_compute_name)
    if dbricks_compute is not None:
        print("dbricks_compute:")
        print(dbricks_compute)

    # Create Databricks instance pool
    notebook_folder = f"/Shared/build{e.build_id}"
    dbricks_client = DatabricksClient(
        dbricks_compute.location, e.databricks_access_token)

    pool_name = "azureml_training"
    instance_pool_id = dbricks_client.get_instance_pool(pool_name)
    if not instance_pool_id:
        dbricks_client.call(
            'instance-pools/create',
            requests.post,
            json={
                "instance_pool_name": pool_name,
                "node_type_id": e.databricks_vm_size,
                "idle_instance_autotermination_minutes": 10,
                "preloaded_spark_versions": [e.databricks_runtime_version],
            }
        )
    instance_pool_id = dbricks_client.get_instance_pool(pool_name)

    # Create data preparation pipeline step

    training_data_input = DataReference(
        datastore=blob_datastore,
        path_on_datastore="/",
        data_reference_name="training"
    )

    workspace_datastore = Datastore(aml_workspace, "workspaceblobstore")
    feature_eng_output = PipelineData("prepped_data",
                                      datastore=workspace_datastore)

    notebook_path = dbricks_client.upload_notebook(
        notebook_folder,
        "code/prepare", "data_preparation")

    dataprep_step = DatabricksStep(
        name="Prepare data",
        inputs=[training_data_input],
        outputs=[feature_eng_output],
        spark_version=e.databricks_runtime_version,
        instance_pool_id=instance_pool_id,
        num_workers=e.databricks_nodes,
        notebook_path=notebook_path,
        compute_target=dbricks_compute,
        allow_reuse=True,
    )

    # Create model training step

    # Get Azure machine learning cluster
    aml_compute = get_compute(
        aml_workspace,
        e.compute_name,
        e.vm_size)
    if aml_compute is not None:
        print("aml_compute:")
        print(aml_compute)

    run_config = RunConfiguration(conda_dependencies=CondaDependencies.create(
        conda_packages=['numpy', 'pandas',
                        'scikit-learn', 'tensorflow', 'keras'],
        pip_packages=['azure', 'azureml-core',
                      'azure-storage',
                      'azure-storage-blob'])
    )
    run_config.environment.docker.enabled = True

    model_name_param = PipelineParameter(
        name="model_name", default_value=e.model_name)
    build_id_param = PipelineParameter(
        name="build_id", default_value=e.build_id)
    hyperparameter_alpha_param = PipelineParameter(
        name="hyperparameter_alpha", default_value=0.5)

    train_step = PythonScriptStep(
        name="Train Model",
        inputs=[feature_eng_output],
        script_name=e.train_script_path,
        compute_target=aml_compute,
        source_directory=e.sources_directory_train,
        arguments=[
            "--build_id", build_id_param,
            "--model_name", model_name_param,
            "--alpha", hyperparameter_alpha_param,
        ],
        runconfig=run_config,
        allow_reuse=False,
    )
    print("Step Train created")

    evaluate_step = PythonScriptStep(
        name="Evaluate Model ",
        script_name=e.evaluate_script_path,
        compute_target=aml_compute,
        source_directory=e.sources_directory_train,
        arguments=[
            "--build_id", build_id_param,
            "--model_name", model_name_param,
        ],
        runconfig=run_config,
        allow_reuse=False,
    )
    print("Step Evaluate created")

    register_step = PythonScriptStep(
        name="Register Model ",
        script_name=e.register_script_path,
        compute_target=aml_compute,
        source_directory=e.sources_directory_train,
        arguments=[
            "--build_id", build_id_param,
            "--model_name", model_name_param,
        ],
        runconfig=run_config,
        allow_reuse=False,
    )
    print("Step Register created")

    train_step.run_after(dataprep_step)
    evaluate_step.run_after(train_step)
    register_step.run_after(evaluate_step)
    steps = [dataprep_step, train_step, evaluate_step, register_step]

    train_pipeline = Pipeline(workspace=aml_workspace, steps=steps)
    train_pipeline._set_experiment_name
    train_pipeline.validate()
    published_pipeline = train_pipeline.publish(
        name=e.pipeline_name,
        description="Model training/retraining pipeline",
        version=e.build_id
    )
    print(f'Published pipeline: {published_pipeline.name}')
    print(f'for build {published_pipeline.version}')


if __name__ == '__main__':
    main()

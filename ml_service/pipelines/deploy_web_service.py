import argparse
import os
from azureml.core import Workspace
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig, Model
from ml_service.util.env_variables import Env
from ml_service.util.manage_environment import get_environment


def main():
    parser = argparse.ArgumentParser("smoke_test_scoring_service.py")

    parser.add_argument(
        "--type",
        type=str,
        choices=["AKS", "ACI"],
        required=True,
        help="type of service"
    )
    parser.add_argument(
        "--service",
        type=str,
        required=True,
        help="Name of the service to deploy"
    )
    args = parser.parse_args()

    e = Env()
    # Get Azure machine learning workspace
    aml_workspace = Workspace.get(
        name=e.workspace_name,
        subscription_id=e.subscription_id,
        resource_group=e.resource_group
    )
    print("get_workspace:")
    print(aml_workspace)

    # Create a reusable scoring environment
    environment = get_environment(
       aml_workspace, "diabetes_scoring",
       "diabetes_regression/scoring_dependencies.yml")

    inference_config = InferenceConfig(
        entry_script='score.py',
        source_directory=os.path.join(e.sources_directory_train, "scoring"),
        environment=environment,
    )
    if args.type == "AKS":
        aci_config = AciWebservice.deploy_configuration(
            description=f'Scoring model version {e.model_version}',
            tags={"BuildId": e.build_id},
            cpu_cores=1,
            memory_gb=4,
        )
    else:
        aci_config = AciWebservice.deploy_configuration(
            description=f'Scoring model version {e.model_version}',
            tags={"BuildId": e.build_id},
            cpu_cores=1,
            memory_gb=4,
        )
    model = Model(aml_workspace, name=e.model_name, version=e.model_version)
    service = Model.deploy(
        workspace=aml_workspace,
        name=args.service,
        models=[model],
        inference_config=inference_config,
        deployment_config=aci_config,
        overwrite=True,
    )
    service.wait_for_deployment(show_output=True)


if __name__ == '__main__':
    main()

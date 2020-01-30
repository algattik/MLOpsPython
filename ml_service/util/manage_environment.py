from azureml.core import Workspace, Environment
import hashlib


def get_environment(
    workspace: Workspace,
    base_name: str,
    environment_file: str,
):

    with open(environment_file, 'rb') as file:
        checksum = hashlib.sha1(file.read()).hexdigest()

    environment_name = base_name + "_" + checksum
    try:
        return Environment.get(
        workspace=workspace, name=environment_name)
    except Exception as e:
        return create_environment(workspace, environment_name, environment_file)


def create_environment(
    workspace: Workspace,
    environment_name: str,
    environment_file: str,
):

    try:
        aml_env = Environment.from_conda_specification(name=environment_name,
                                                       file_path=environment_file)
        aml_env.register(workspace)
        return aml_env
    except Exception as e:
        print(e)
        print('An error occurred while creating an environment.')
        raise

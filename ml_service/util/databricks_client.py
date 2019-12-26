import os
import sys
import requests
import base64
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import DatabricksStep
from azureml.core.datastore import Datastore
from azureml.data.data_reference import DataReference
from azure.common.credentials import get_azure_cli_credentials
from azure.mgmt.storage import StorageManagementClient
from requests.exceptions import HTTPError

sys.path.append(os.path.abspath("./ml_service/util"))  # NOQA: E402
from attach_compute import get_compute
from env_variables import Env


class DatabricksClient():
    def __init__(self, location, token):
        self.endpoint = f"https://{location}.azuredatabricks.net/api/2.0/"
        self.auth = {'Authorization': f"Bearer {token}"}
    
    
    def call(self, url, method, **kwargs):
        """
        Run a REST query against the Databricks API.
        Raises an exception on any non-success response.
        """
        response = method(f"{self.endpoint}{url}", headers=self.auth, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError:
            print(response.text)
            raise
        return response
    
    
    def upload_notebook(self, notebook_folder,
                        notebook_dir, notebook_name):
        """
        Uploads a notebook to databricks.
        """
    
        # Read notebook file into a Base-64 encoded string
        notebook_path = f"{notebook_folder}/{notebook_name}"
        with open(f"{notebook_dir}/{notebook_name}.py", "r") as file:
            file_content = file.read()
        content_b64 = base64.b64encode(file_content.encode('utf-8'))
    
        # Create the notebook directory in the Databricks workspace.
        # Will not fail if the directory already exists
        self.call(
            'workspace/mkdirs',
            requests.post,
            json={
                "path": notebook_folder,
            }
        )
    
        # Import notebook into workspace
        self.call(
            'workspace/import',
            requests.post,
            json={
                "content": content_b64.decode('ascii'),
                "path": notebook_path,
                "language": "PYTHON",
                "format": "SOURCE"
            }
        )
    
        return notebook_path
    
    
    def get_instance_pool(self, pool_name):
        """
        Get the instance pool ID corresponding to an instance pool name.
        Returns None if instance pool with that name was not found.
        """
        # Query API for list of instance pools
        response = self.call(
            'instance-pools/list',
            requests.get,
        )
        # API quirk: 'instance_pools' element is not returned if
        # there are no instance pools.
        if 'instance_pools' in response.json():
            for pool in response.json()['instance_pools']:
                if pool["instance_pool_name"] == pool_name:
                    return pool["instance_pool_id"]
        return None

import os
from dotenv import load_dotenv


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)  # noqa E501
        return class_._instances[class_]


class Env(Singleton):

    def __init__(self):
        load_dotenv()
        self._workspace_name = os.environ.get("WORKSPACE_NAME")
        self._resource_group = os.environ.get("RESOURCE_GROUP")
        self._subscription_id = os.environ.get("SUBSCRIPTION_ID")
        self._vm_size = os.environ.get("AML_COMPUTE_CLUSTER_CPU_SKU")
        self._compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME")
        self._vm_priority = os.environ.get("AML_CLUSTER_PRIORITY", 'lowpriority')  # noqa E501
        self._min_nodes = int(os.environ.get("AML_CLUSTER_MIN_NODES", 0))
        self._max_nodes = int(os.environ.get("AML_CLUSTER_MAX_NODES", 4))
        self._build_id = os.environ.get("BUILD_BUILDID")
        self._pipeline_name = os.environ.get("TRAINING_PIPELINE_NAME")
        self._sources_directory_train = os.environ.get("SOURCES_DIR_TRAIN")
        self._train_script_path = os.environ.get("TRAIN_SCRIPT_PATH")
        self._evaluate_script_path = os.environ.get("EVALUATE_SCRIPT_PATH")
        self._register_script_path = os.environ.get("REGISTER_SCRIPT_PATH")
        self._model_name = os.environ.get("MODEL_NAME")
        self._experiment_name = os.environ.get("EXPERIMENT_NAME")
        self._model_version = os.environ.get('MODEL_VERSION')
        self._image_name = os.environ.get('IMAGE_NAME')
        self._model_path = os.environ.get('MODEL_PATH')
        self._db_cluster_id = os.environ.get("DB_CLUSTER_ID")
        self._score_script = os.environ.get("SCORE_SCRIPT")
        self._training_datastore_name = os.environ.get(
            "TRAINING_DATASTORE_NAME", "trainingdatads")
        self._training_account_name = os.environ.get("TRAINING_ACCOUNT_NAME")
        self._training_container_name = os.environ.get(
            "TRAINING_CONTAINER_NAME", "trainingdata")
        self._databricks_compute_name = os.environ.get(
            "DATABRICKS_COMPUTE_NAME", "databricks")
        self._databricks_workspace_name = os.environ.get(
            "DATABRICKS_WORKSPACE_NAME")
        self._databricks_access_token = os.environ.get(
            "DATABRICKS_ACCESS_TOKEN")
        self._databricks_runtime_version = os.environ.get(
            "DATABRICKS_RUNTIME_VERSION", "6.2.x-scala2.11")
        self._databricks_vm_size = os.environ.get(
            "DATABRICKS_VM_SIZE", "Standard_D3_v2")
        self._databricks_nodes = int(os.environ.get("DATABRICKS_NODES", 1))

    @property
    def workspace_name(self):
        return self._workspace_name

    @property
    def resource_group(self):
        return self._resource_group

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def vm_size(self):
        return self._vm_size

    @property
    def compute_name(self):
        return self._compute_name

    @property
    def db_cluster_id(self):
        return self._db_cluster_id

    @property
    def build_id(self):
        return self._build_id

    @property
    def pipeline_name(self):
        return self._pipeline_name

    @property
    def sources_directory_train(self):
        return self._sources_directory_train

    @property
    def train_script_path(self):
        return self._train_script_path

    @property
    def evaluate_script_path(self):
        return self._evaluate_script_path

    @property
    def register_script_path(self):
        return self._register_script_path

    @property
    def model_name(self):
        return self._model_name

    @property
    def experiment_name(self):
        return self._experiment_name

    @property
    def vm_priority(self):
        return self._vm_priority

    @property
    def min_nodes(self):
        return self._min_nodes

    @property
    def max_nodes(self):
        return self._max_nodes

    @property
    def model_version(self):
        return self._model_version

    @property
    def image_name(self):
        return self._image_name

    @property
    def model_path(self):
        return self._model_path

    @property
    def score_script(self):
        return self._score_script

    @property
    def training_datastore_name(self):
        return self._training_datastore_name

    @property
    def training_account_name(self):
        return self._training_account_name

    @property
    def training_container_name(self):
        return self._training_container_name

    @property
    def databricks_compute_name(self):
        return self._databricks_compute_name

    @property
    def databricks_workspace_name(self):
        return self._databricks_workspace_name

    @property
    def databricks_access_token(self):
        return self._databricks_access_token

    @property
    def databricks_runtime_version(self):
        return self._databricks_runtime_version

    @property
    def databricks_vm_size(self):
        return self._databricks_vm_size

    @property
    def databricks_nodes(self):
        return self._databricks_nodes

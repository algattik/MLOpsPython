from azureml.core import Workspace
from azureml.core.compute import AmlCompute, DatabricksCompute
from azureml.core.compute import ComputeTarget
from azureml.exceptions import ComputeTargetException
from env_variables import Env


def get_compute(
    workspace: Workspace,
    compute_name: str,
    vm_size: str
):
    try:
        if compute_name in workspace.compute_targets:
            compute_target = workspace.compute_targets[compute_name]
            if compute_target and type(compute_target) is AmlCompute:
                print('Found existing compute target ' + compute_name
                      + ' so using it.')
        else:
            e = Env()
            compute_config = AmlCompute.provisioning_configuration(
                vm_size=vm_size,
                vm_priority=e.vm_priority,
                min_nodes=e.min_nodes,
                max_nodes=e.max_nodes,
                idle_seconds_before_scaledown="300"
                #    #Uncomment the below lines for VNet support
                #    vnet_resourcegroup_name=vnet_resourcegroup_name,
                #    vnet_name=vnet_name,
                #    subnet_name=subnet_name
            )
            compute_target = ComputeTarget.create(workspace, compute_name,
                                                  compute_config)
            compute_target.wait_for_completion(
                show_output=True,
                min_node_count=None,
                timeout_in_minutes=10)
        return compute_target
    except ComputeTargetException as e:
        print(e)
        print('An error occurred trying to provision compute.')
        exit(1)


def get_databricks_compute(
    workspace: Workspace,
    compute_name: str
):
    try:
        if compute_name in workspace.compute_targets:
            compute_target = workspace.compute_targets[compute_name]
            if compute_target and type(compute_target) is DatabricksCompute:
                print('Found existing compute target %s' % compute_name)
        else:
            e = Env()

            compute_config = DatabricksCompute.attach_configuration(
                resource_group=e.resource_group,
                workspace_name=e.databricks_workspace_name,
                access_token=e.databricks_access_token)

            compute_target = ComputeTarget.attach(
                workspace, compute_name, compute_config)

            compute_target.wait_for_completion(
                show_output=True)

        return compute_target
    except ComputeTargetException as e:
        print(e)
        print('An error occurred trying to provision compute.')
        exit(1)

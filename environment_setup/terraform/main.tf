# Deploy a Resource Group with an Azure ML Workspace and supporting resources.
#
# For suggested naming conventions, refer to:
#   https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/naming-and-tagging

# Resource Group

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.appname}-${var.environment}-main"
  location = var.location
}

module "azureml" {
  source = "./azureml"
  appname = var.appname
  environment = var.environment
  location = var.location
  tenant_id = data.azurerm_client_config.current.tenant_id
  resource_group_name = azurerm_resource_group.main.name
  devops_mlpipeline_sp_object_id = var.devops_mlpipeline_sp_object_id
}

module "acr-build" {
  source = "./acr-build"
  source_dir = "./azureml-buildcontainer"
  registry = module.azureml.container_registry.name
  image = "modelbuild:latest"
}

module "training-data" {
  source = "./training-data"
  appname = var.appname
  environment = var.environment
  resource_group_name = azurerm_resource_group.main.name
  location = var.location
  devops_mlpipeline_sp_object_id = var.devops_mlpipeline_sp_object_id
}

module "databricks" {
  source = "./databricks"
  appname = var.appname
  environment = var.environment
  resource_group_name = azurerm_resource_group.main.name
  location = var.location
}

module "vnet" {
  source = "./vnet"
  appname = var.appname
  environment = var.environment
  resource_group_name = azurerm_resource_group.main.name
  location = var.location
}

module "aks" {
  source = "./aks"
  appname = var.appname
  environment = var.environment
  location = var.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id = data.azurerm_client_config.current.tenant_id
  subnet_id = module.vnet.aks_subnet_id
  aks_sp_client_id = var.aks_sp_client_id
  aks_sp_client_secret = var.aks_sp_client_secret
}

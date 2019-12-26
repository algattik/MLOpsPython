resource "azurerm_storage_account" "training_data" {
  name                     = "st${var.appname}${var.environment}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_kind             = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "training_data" {
  name                  = "trainingdata"
  storage_account_name  = azurerm_storage_account.training_data.name
}

resource "azurerm_role_assignment" "training_data_mlpipeline" {
  scope                = azurerm_storage_account.training_data.id
  role_definition_name = "Reader and Data Access"
  principal_id         = var.devops_mlpipeline_sp_object_id
}


resource "azurerm_storage_blob" "example" {
  name                   = each.value
  for_each               = fileset("training-data/data/", "*")
  storage_account_name   = azurerm_storage_account.training_data.name
  storage_container_name = azurerm_storage_container.training_data.name
  type                   = "Block"
  source                 = "training-data/data/${each.value}"
}

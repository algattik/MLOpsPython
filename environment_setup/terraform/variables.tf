variable "appname" {
  type = string
  description = "Application name. Use only lowercase letters and numbers"
  default = "mlopssample"
}

variable "environment" {
  type    = string
  description = "Environment name, e.g. 'dev' or 'stage'"
  default = "dev"
}

variable "location" {
  type    = string
  description = "Azure region where to create resources."
  default = "East US"
}

# Service principal Object IDs.

variable "devops_mlpipeline_sp_object_id" {
  type    = string
  description = "Service principal object ID for the Azure DevOps ML Model CI/CD pipeline service connection. Should be the object ID of the service principal, not the object ID of the application nor the application ID. To retrieve, navigate in the AAD portal from an App registration to 'Managed application in local directory'."
}

variable "aks_sp_client_id" {
  type = string
  description = "Service principal client ID for the Azure Kubernetes Service cluster identity."
}

variable "aks_sp_client_secret" {
  type = string
  description = "Service principal client secret for the Azure Kubernetes Service cluster identity."
}

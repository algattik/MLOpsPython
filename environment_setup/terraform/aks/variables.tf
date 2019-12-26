variable "appname" {
  type = string
}

variable "environment" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type    = string
}

variable "tenant_id" {
  type    = string
}

variable "subnet_id" {
  type    = string
}

variable "aks_sp_client_id" {
  type = string
}

variable "aks_sp_client_secret" {
  type = string
}

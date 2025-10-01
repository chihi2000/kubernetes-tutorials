variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "tutorial"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "carsharing"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry (must be globally unique)"
  type        = string
  # No default - must be provided in terraform.tfvars
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "rg-carsharing-tutorial"
}

variable "aks_cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "aks-carsharing-tutorial"
}
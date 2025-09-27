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
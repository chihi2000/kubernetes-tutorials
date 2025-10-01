terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  # subscription id is an env variable 
  features {
  }
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-carsharing-tutorial"
  location = "East US"

  tags = {
    Environment = "Tutorial"
    Project     = "Carsharing"
    AutoDelete  = "true"
  }
}

# Azure Container Registry
resource "azurerm_container_registry" "main" {
  name                = "ghadaregistry2000"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    Environment = "Tutorial"
    Project     = "Carsharing"
    AutoDelete  = "true"
  }
}

# Azure Kubernetes Service
resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-carsharing-tutorial"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks-carsharing"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Tutorial"
    Project     = "Carsharing"
    AutoDelete  = "true"
  }
}

# Role assignment for AKS to pull from ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  role_definition_name = "AcrPull"
  scope                = azurerm_container_registry.main.id
}

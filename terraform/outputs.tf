output "acr_login_server" {
  description = "The login server URL for the Azure Container Registry"
  value       = azurerm_container_registry.main.login_server
}

output "acr_name" {
  description = "The name of the Azure Container Registry"
  value       = azurerm_container_registry.main.name
}

output "acr_admin_username" {
  description = "The admin username for the Azure Container Registry"
  value       = azurerm_container_registry.main.admin_username
}

output "acr_admin_password" {
  description = "The admin password for the Azure Container Registry"
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
}

output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "aks_cluster_name" {
  description = "The name of the AKS cluster"
  value       = azurerm_kubernetes_cluster.main.name
}

output "aks_fqdn" {
  description = "The FQDN of the AKS cluster"
  value       = azurerm_kubernetes_cluster.main.fqdn
}

output "aks_kube_config" {
  description = "Raw kubeconfig for the AKS cluster"
  value       = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive   = true
}
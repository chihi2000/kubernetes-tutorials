# Azure Container Registry - Terraform

This Terraform configuration creates an Azure Container Registry for the carsharing tutorial project.

## Prerequisites

- Azure CLI installed and logged in: `az login`
- Terraform installed

## Usage

### Deploy ACR
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Get ACR credentials
```bash
terraform output acr_login_server
terraform output acr_admin_username
terraform output -raw acr_admin_password
```

### Build and push Docker image
```bash
# Get ACR login server
ACR_LOGIN_SERVER=$(terraform output -raw acr_login_server)

# Build and tag image
docker build -t $ACR_LOGIN_SERVER/fastapi-carsharing:v1 ../pythonbuilding

# Login to ACR
az acr login --name $(terraform output -raw acr_name)

# Push image
docker push $ACR_LOGIN_SERVER/fastapi-carsharing:v1
```

### Clean up (IMPORTANT - saves money!)
```bash
terraform destroy
```

## Resources Created.

- Resource Group: `rg-carsharing-tutorial`
- Azure Container Registry: `acrcarsharing{random-suffix}`

All resources are tagged with `AutoDelete: true` for easy identification.

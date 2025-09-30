# Car Sharing Application - Kubernetes & Azure Learning Project

A comprehensive hands-on project demonstrating containerization, Kubernetes orchestration, and Azure cloud deployment of a full-stack car sharing application.

## Project Overview

This project implements a **FastAPI-based car sharing service** with a **MySQL database**, deployed on **Azure Kubernetes Service (AKS)**. It demonstrates real-world containerization and cloud-native deployment patterns.

### Application Architecture

The application follows a microservices architecture deployed on Kubernetes with the following components:

**Frontend Layer**: Users access the application through a web browser, connecting to the external LoadBalancer service that provides a public IP address for internet access.

**Load Balancing**: Azure Load Balancer distributes incoming HTTP requests across multiple FastAPI application instances, ensuring high availability and load distribution.

**Application Layer**: Two FastAPI pod replicas handle web requests, API calls, and business logic. Each pod runs the Python-based car sharing application with authentication, car management, and trip tracking functionality.

**Data Layer**: A single MySQL pod provides persistent data storage for users, cars, and trips. The database uses hostPath persistent storage to ensure data survives pod restarts and failures.

**Network Communication**: Internal cluster networking enables secure communication between FastAPI pods and the MySQL database through Kubernetes services, while external traffic flows through the LoadBalancer to reach the application pods.

### Key Features

- **Multi-user Authentication**: User signup/login with JWT tokens
- **Car Management**: CRUD operations for car inventory
- **Trip Tracking**: Record and manage car trips
- **Search Functionality**: Filter cars by size, doors, fuel type
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Persistent Storage**: Data survives pod restarts and crashes

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI (Python) | REST API server |
| **Database** | MySQL 8.0 | Data persistence |
| **Container** | Docker | Application packaging |
| **Orchestration** | Kubernetes | Container management |
| **Cloud Platform** | Azure AKS | Managed Kubernetes |
| **Infrastructure** | Terraform | Infrastructure as Code |
| **Registry** | Azure Container Registry | Container image storage |

## Project Structure

```
├── pythonbuilding/          # FastAPI application source
│   ├── carsharing.py       # Main FastAPI app
│   ├── db.py               # Database connection
│   └── models.py           # SQLModel data models
├── terraform/              # Infrastructure as Code
│   ├── main.tf             # AKS cluster & ACR setup
│   └── outputs.tf          # Resource outputs
├── Dockerfile              # Multi-stage container build
├── carsharing-app-dep.yaml # FastAPI Kubernetes deployment
├── mysql-dep.yaml          # MySQL deployment with persistence
└── secrets.yaml            # Database credentials (gitignored)
```

## Quick Start

### Prerequisites
- Azure subscription with AKS access
- Docker Desktop
- kubectl configured for AKS
- Terraform (for infrastructure)

### 1. Deploy Infrastructure
```bash
cd terraform
terraform init
terraform apply
```

### 2. Build & Push Container
```bash
# Login to Azure Container Registry
az acr login --name ghadaregistry2000

# Build for AMD64 (AKS compatibility)
docker build --platform linux/amd64 -t ghadaregistry2000.azurecr.io/fastapi-carsharing:v3 .
docker push ghadaregistry2000.azurecr.io/fastapi-carsharing:v3
```

### 3. Deploy to Kubernetes
```bash
# Deploy MySQL with persistent storage
kubectl apply -f mysql-dep.yaml

# Deploy FastAPI application
kubectl apply -f carsharing-app-dep.yaml

# Get external IP
kubectl get svc fastapi-carsharing-svc
```

### 4. Access Application
- **Web UI**: `http://<EXTERNAL-IP>/`
- **API Docs**: `http://<EXTERNAL-IP>/docs`
- **Health Check**: `http://<EXTERNAL-IP>/api/cars/allcars`

## Key Learning Concepts Demonstrated

### Container Architecture
- **Multi-platform builds**: ARM64 (local) vs AMD64 (cloud)
- **Image optimization**: Layer caching and build strategies
- **Security**: Non-root containers and secret management

### Kubernetes Patterns
- **Deployments**: Rolling updates and replica management
- **Services**: Load balancing and service discovery
- **Persistent Storage**: Data survival across pod restarts
- **ConfigMaps & Secrets**: Environment-based configuration

### Cloud Integration
- **Azure AKS**: Managed Kubernetes with auto-scaling
- **Azure Container Registry**: Private image storage with RBAC
- **Load Balancer**: External traffic routing
- **Infrastructure as Code**: Terraform for reproducible deployments

### Production Readiness
- **High Availability**: Multiple FastAPI replicas
- **Data Persistence**: MySQL survives pod failures
- **Monitoring**: Structured logging and health checks
- **Security**: RBAC, secrets, and network policies

## Learning Outcomes

This project provides hands-on experience with:

1. **Containerization**: Docker best practices and multi-stage builds
2. **Kubernetes**: Pod orchestration, services, and persistent volumes
3. **Cloud Native**: Azure services integration and managed infrastructure
4. **DevOps**: Infrastructure as Code and container registry workflows
5. **Database Management**: Persistent storage and data migration strategies
6. **Application Architecture**: Microservices patterns and API design

## Common Issues & Solutions

### Architecture Mismatch
**Problem**: `exec format error` on AKS
**Solution**: Build with `--platform linux/amd64` and `--no-cache`

### Data Loss
**Problem**: Database data disappears on pod restart
**Solution**: Use `hostPath` or `PersistentVolumeClaim` instead of `emptyDir`

### Image Pull Errors
**Problem**: AKS cannot pull from ACR
**Solution**: Verify RBAC role assignment: `AcrPull` permission for AKS identity

## Application Metrics

- **FastAPI Replicas**: 2 (High Availability)
- **MySQL Storage**: Persistent hostPath (`/mnt/mysql-data`)
- **External Access**: LoadBalancer with public IP
- **Database**: Full CRUD operations with relationships

## Next Steps

- [ ] Implement SSL/TLS certificates
- [ ] Add Prometheus monitoring
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling policies
- [ ] Add comprehensive logging with ELK stack

---

Author: cloud enthusiast that hates css
Purpose: Hands-on Kubernetes and cloud-native development education

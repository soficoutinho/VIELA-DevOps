
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = "5ec8d996-4116-49f6-9411-f785507b788d"
}

# Grupo de recursos existente
data "azurerm_resource_group" "viela" {
  name = "rg-viela-devops"
}

# Workspace de monitoramento existente
data "azurerm_log_analytics_workspace" "viela" {
  name                = "law-viela-devops"
  resource_group_name = data.azurerm_resource_group.viela.name
}

# Saidas do Terraform
output "resource_group_name" {
  value = data.azurerm_resource_group.viela.name
}

output "resource_group_location" {
  value = data.azurerm_resource_group.viela.location
}

# Ambiente Azure Container Apps
resource "azurerm_container_app_environment" "viela" {
  name                = "cae-viela-devops"
  location            = "canadacentral"
  resource_group_name = data.azurerm_resource_group.viela.name

  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.viela.id

  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
  }

  tags = {
    projeto    = "VIELA"
    ambiente   = "dev"
    finalidade = "fiap-global-solution"
  }
}

# Aplicacao VIELA API
resource "azurerm_container_app" "viela" {
  name                         = "ca-viela-api"
  container_app_environment_id = azurerm_container_app_environment.viela.id
  resource_group_name          = data.azurerm_resource_group.viela.name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"

  template {
    min_replicas = 0
    max_replicas = 1

    http_scale_rule {
      name                = "http-scaler"
      concurrent_requests = 10
    }

    container {
      name   = "viela-api"
      image  = "ghcr.io/soficoutinho/viela-devops:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      liveness_probe {
        transport = "HTTP"
        port      = 8000
        path      = "/health"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "http"

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  tags = {
    projeto    = "VIELA"
    ambiente   = "dev"
    finalidade = "fiap-global-solution"
  }
}


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

data "azurerm_resource_group" "viela" {
  name = "rg-viela-devops"
}

output "resource_group_name" {
  value = data.azurerm_resource_group.viela.name
}

output "resource_group_location" {
  value = data.azurerm_resource_group.viela.location
}

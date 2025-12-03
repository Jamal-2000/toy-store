terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1️⃣ Cloud SQL Instance
resource "google_sql_database_instance" "toy_store_instance_terra" {
  name             = "toy-store-terra"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"  # Cheapest tier
  }
}

# 2️⃣ Database inside the instance
resource "google_sql_database" "toy_store_terra_db" {
  name     = "toy_store"
  instance = google_sql_database_instance.toy_store_instance_terra.name
}

# 3️⃣ Database user
resource "google_sql_user" "toy_terra_user" {
  name     = "toy_user"
  instance = google_sql_database_instance.toy_store_instance_terra.name
  password = var.db_password
}

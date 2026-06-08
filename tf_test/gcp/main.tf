provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Base Network
resource "google_compute_network" "vpc_network" {
  name                    = "archgen-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "archgen-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.gcp_region
  network       = google_compute_network.vpc_network.id
}


# Cloud Storage for Static Hosting
resource "google_storage_bucket" "frontend_frontend1" {
  name          = "archgen-frontend-frontend1"
  location      = "US"
  force_destroy = true
  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}
resource "google_storage_bucket_iam_binding" "public_read_frontend1" {
  bucket = google_storage_bucket.frontend_frontend1.name
  role   = "roles/storage.objectViewer"
  members = [
    "allUsers",
  ]
}


# Cloud Run Compute
resource "google_cloud_run_service" "default_backend1" {
  name     = "cloudrun-backend1"
  location = var.gcp_region

  template {
    spec {
      containers {
        image = "gcr.io/cloudrun/hello"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}


# Cloud SQL PostgreSQL
resource "google_sql_database_instance" "default_db1" {
  name             = "cloudsql-db1"
  database_version = "POSTGRES_14"
  region           = var.gcp_region

  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = false
}


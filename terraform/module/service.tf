
/* ---------------------------------- Service Image --------------------------------- */

# Note: Generally it is NOT best practise to build images in Terraform. We are still
# doing it here for simplicity. In industry, you should think twice before doing this.
resource "null_resource" "docker_build" {

  provisioner "local-exec" {
    working_dir = path.module
    command     = "IMG=${var.region}-docker.pkg.dev/${var.project}/parma-registry/parma-mining-producthunt:${var.env}-$(git rev-parse --short HEAD) && docker build -t $IMG ./../../ && docker push $IMG && echo $IMG > .image.name"
  }

  triggers = {
    always_run = timestamp()
  }
}

# get output from docker_build
data "local_file" "image_name" {
  filename   = "${path.module}/.image.name"
  depends_on = [null_resource.docker_build]
}


/* ------------------------------------ Cloud Run ----------------------------------- */

resource "google_cloud_run_service" "parma_mining_producthunt_cloud_run" {
  name     = "parma-mining-producthunt-${var.env}"
  location = var.region

  template {
    spec {
      containers {
        image = data.local_file.image_name.content

        resources {
          limits = {
            # 0.5 vCPU, 256 MB RAM for ${var.env} == staging, else 1 vCPU, 512 MB RAM
            cpu    = var.env == "staging" ? "1" : "1"
            memory = var.env == "staging" ? "256Mi" : "512Mi"
          }
        }

        ports {
          container_port = 8080
        }
        env {
          name  = "ANALYTICS_BASE_URL"
          value = var.ANALYTICS_BASE_URL
        }
        env {
          name  = "PARMA_SHARED_SECRET_KEY"
          value = var.PARMA_SHARED_SECRET_KEY
        }
        env {
          name  = "DEPLOYMENT_ENV"
          value = var.env
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }

  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

/* --------------------------------------- IAM -------------------------------------- */

// Define a policy that allows any user to invoke the Cloud Run service.
data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

// Apply the policy to the Cloud Run service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.parma_mining_producthunt_cloud_run.location
  project  = google_cloud_run_service.parma_mining_producthunt_cloud_run.project
  service  = google_cloud_run_service.parma_mining_producthunt_cloud_run.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

provider "helm" {
  kubernetes {
    config_path = pathexpand(var.cluster_config_path)
  }
}

resource "helm_release" "helm_nginx" {
  name       = "nginx"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "nginx"
  version    = "13.1.6"

  values = [
    "${file("helm-values.yaml")}"
  ]
}

provider "kubernetes" {
  config_context_cluster = "arn:aws:eks:us-east-1:836566418525:cluster/turo"
  config_path            = "~/.kube/config"
}

provider "kubernetes" {
  config_context_cluster = "arn:aws:eks:us-east-1:836566418525:cluster/testing-fargate"
  config_path            = "~/.kube/config"
}

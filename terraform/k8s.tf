provider "kubernetes" {
  config_context_cluster = "arn:aws:eks:us-east-1:663118211814:cluster/tf-eks-test"
  config_path            = "~/.kube/config"
}

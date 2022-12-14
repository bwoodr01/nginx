# variables.tf

# variable "kind_cluster_name" {
#   type        = string
#   description = "The name of the cluster."
#   default     = "kind-terraform-learn"
# }

variable "cluster_config_path" {
  type        = string
  description = "The location where this cluster's kubeconfig will be saved to."
  default     = "~/.kube/config"
}

variable "namespace" {
  description = "The namespace it will be created if needed)."
  type        = string
  default     = "nginx"
}

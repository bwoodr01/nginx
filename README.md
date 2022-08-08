# Install dependencies

Python packages

```
pip install -r requirements.txt
```

Docker Desktop

```
<https://docs.docker.com/desktop/install/mac-install/>
```

Git CLI

```
brew install git
```

Terraform

```
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
brew update
brew upgrade hashicorp/tap/terraform
```

Helm

```
brew install helm
```

Helm

```
brew install eksctl
```

# Enhancement 1

Setting up IAM Permissions

```
eksctl --profile ben utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster turo \
    --approve
```

```
aws --profile ben iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://k8s/iam-policy.json
```

```
eksctl --profile ben create iamserviceaccount \
--cluster=turo \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--attach-policy-arn=arn:aws:iam::836566418525:policy/AWSLoadBalancerControllerIAMPolicy \
--override-existing-serviceaccounts \
--region us-east-1 \
--approve
```

Add the EKS chart repo to helm

```
helm repo add eks https://aws.github.io/eks-charts
```

Install chart

```
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=fargate-testing --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
```

Apply terraform changes with ALB controller helm-values.yaml changes

```
terraform init
terraform plan
terraform apply
```

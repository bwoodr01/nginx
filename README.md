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

# Build new image

```
./build.sh
```

Output will include tag

# Update Terraform with new tag

```
python update.py terraform -t <tag>
```

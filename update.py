# Standard Library
import sys
import yaml
import os
import logging

# Third-party
import click
from github import Github

# Custom modules
from utils import subprocess_exec_cmd

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

docker_repo = "bwoodr01/nginx"
github_repo = "bwoodr01/nginx"
terraform_helm_values = "terraform/helm-values.yaml"


@click.group()
def update():
    pass


@update.command()
@click.option(
    "-t",
    "--tag",
    help="Docker image tag to update terraform code",
    required=True,
)
@click.option(
    "-ght",
    "--token",
    help="Github Access Token",
    required=False,
)
def terraform_pr_tag(tag: str, token: str):
    """
    Takes docker tag and make PR for helm-values changes

    \b
    Examples:
        python update.py terraform-pr-tag -t 419b521
    """

    if not token:
        if not os.getenv("GITHUB_TOKEN"):
            logger.error("Must provide token! Use --token arg or set GITHUB_TOKEN env")
            sys.exit(1)
        else:
            token = os.getenv("GITHUB_TOKEN")

    # docker needs to be installed on local machine
    docker_pull_cmd = f"docker pull {docker_repo}:{tag}"
    process = subprocess_exec_cmd(docker_pull_cmd)

    if process.returncode != 0:
        logger.error(f"Failed to validate docker image: {docker_repo}:{tag}")
        logger.error(process.stdout)
        sys.exit(process.returncode)
    else:
        logger.info(f"Validated docker image: {docker_repo}:{tag}")

    with open(terraform_helm_values, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        data["image"]["tag"] = tag

    with open(terraform_helm_values, "w") as f:
        yaml.dump(data, f)
        logger.info(f"Added {tag} to {terraform_helm_values}")

    # git need to be installed on local machine

    # checkout branch
    git_checkout_cmd = f"git checkout -b terraform-update-tag-{tag}"
    process = subprocess_exec_cmd(git_checkout_cmd)
    logger.info(f"Checked out branch terraform-update-tag-{tag}")

    # add changes
    git_add_cmd = f"git add {terraform_helm_values}"
    process = subprocess_exec_cmd(git_add_cmd)
    logger.info(f"Added {terraform_helm_values}")

    # set upstream
    git_commit_cmd = f"git commit -m 'Setting terraform value to use new tag {tag}'"
    process = subprocess_exec_cmd(git_commit_cmd)
    logger.info("Wrote commit message")

    # git set upstream
    git_push_cmd = f"git push -u origin terraform-update-tag-{tag}"
    process = subprocess_exec_cmd(git_push_cmd)
    logger.info("Pushed branch")

    # create PR
    github = Github(token)

    repo = github.get_repo(github_repo)
    body = f"Updating terraform helm values tag to: {tag}"
    head = f"terraform-update-tag-{tag}"
    pr = repo.create_pull(
        title="New docker tag",
        body=body,
        head=head,
        base="main",
    )
    logger.info(f"PR opened at https://github.com/{github_repo}/pulls")
    logger.info(pr)

    pass


@update.command()
def terraform_resources():
    """
    Deploys terraform

    \b
    Examples:
        python update.py terraform-resources
    """

    working_dir = os.getcwd() + "/terraform"

    init_cmd = "terraform init"
    logger.info(f"Running {init_cmd}")
    subprocess_exec_cmd(init_cmd, working_dir, timeout=120)

    apply_cmd = "terraform apply --auto-approve"
    logger.info(f"Running {apply_cmd}")
    subprocess_exec_cmd(apply_cmd, working_dir, timeout=600)

    logger.info("Successfulyl deployed terraform!")


@update.command()
def terraform_nuke():
    """
    Runs terraform destroy and removes all local state files

    \b
    Examples:
        python update.py terraform-nuke
    """

    working_dir = os.getcwd() + "/terraform"

    destroy_cmd = "terraform destroy"
    logger.info(f"Running {destroy_cmd}")
    subprocess_exec_cmd(destroy_cmd, working_dir, timeout=600)

    cleanup_cmd = "rm -rf .terraform/ && rm .terraform* && rm terraform.tfstate*"
    logger.info(f"Running {cleanup_cmd}")
    subprocess_exec_cmd(cleanup_cmd, working_dir, timeout=30)

    logger.info("Successfulyl deleted terraform!")


if __name__ == "__main__":
    update()

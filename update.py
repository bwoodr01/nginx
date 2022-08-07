from typing_extensions import Required
import click
import logging
import subprocess
import shlex
import sys
import yaml
import os


# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

docker_repo = "bwoodr01/nginx"
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
def terraform(tag: str, token: str):

    if not token:
        if not os.getenv("GITHUB_TOKEN"):
            logger.error("Must provide token! Use --token arg or set GITHUB_TOKEN env")
            sys.exit(1)
        else:
            token = os.getenv("GITHUB_TOKEN")

    # docker needs to be installed on local machine
    docker_pull_cmd = f"docker pull {docker_repo}:{tag}"
    process = subprocess.run(
        shlex.split(docker_pull_cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf8",
        check=False,
        timeout=10,
    )
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

    # git checkout branch
    git_checkout_cmd = f"git checkout --branch terraform-update-tag-{tag}"
    process = subprocess.run(
        shlex.split(git_checkout_cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf8",
        check=False,
        timeout=10,
    )

    print(process)

    # # git add change
    # git_add_cmd = f"git add {terraform_helm_values}"
    # process = subprocess.run(
    #     shlex.split(git_add_cmd),
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,
    #     encoding="utf8",
    #     check=False,
    #     timeout=10,
    # )

    # # git set upstream
    # git_push_cmd = f"git push -u origin terraform-update-tag-{tag}"
    # process = subprocess.run(
    #     shlex.split(git_push_cmd),
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,
    #     encoding="utf8",
    #     check=False,
    #     timeout=10,
    # )

    # git create PR

    pass


if __name__ == "__main__":
    update()

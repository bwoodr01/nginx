#! /bin/bash

DOCKER_REPO='bwoodr01/nginx'

# get current commit
TAG=$(git rev-parse --short HEAD)
echo "TAG set: ${TAG}"

# build
echo "Building image..."
docker build . -t ${DOCKER_REPO}:${TAG}

# push
echo "Pushing image..."
docker push ${DOCKER_REPO}:${TAG}

# output
echo "-------------------------------------------"
echo "Pushed image: ${DOCKER_REPO}:${TAG}"
echo "-------------------------------------------"

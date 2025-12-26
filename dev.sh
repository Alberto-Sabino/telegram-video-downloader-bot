#!/usr/bin/env bash
# dev.sh — build the Docker image then start a temporary interactive container
# Usage:
#   ./dev.sh            # build image and drop you into a bash shell inside container
#   ./dev.sh pytest     # run pytest inside a temp container (non-interactive)

set -euo pipefail

IMAGE_NAME=python-dev:local
WORKDIR_IN_CONTAINER=/app
HOST_PROJECT_DIR=$(pwd)

# Build the image using the Dockerfile in the current directory
# Enable BuildKit to take advantage of the pip cache mount in the Dockerfile
DOCKER_BUILDKIT=1 docker build -t "$IMAGE_NAME" .

# If a .env file exists in the project root, forward it into the container
ENV_FILE_ARG=""
if [ -f ".env" ]; then
  ENV_FILE_ARG="--env-file .env"
  echo "Found .env — environment variables in .env will be forwarded to the container"
fi

# If no extra args are provided, start an interactive shell mounted to the project
if [ $# -eq 0 ]; then
  docker run --rm -it \
    $ENV_FILE_ARG \
    -v "$HOST_PROJECT_DIR":$WORKDIR_IN_CONTAINER \
    -w $WORKDIR_IN_CONTAINER \
    -p 8000:8000 \
    "$IMAGE_NAME" bash
else
  # Run an arbitrary command non-interactively in the container
  docker run --rm -it \
    $ENV_FILE_ARG \
    -v "$HOST_PROJECT_DIR":$WORKDIR_IN_CONTAINER \
    -w $WORKDIR_IN_CONTAINER \
    "$IMAGE_NAME" "$@"
fi

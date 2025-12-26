#!/usr/bin/env bash
set -euo pipefail

# Simple remote helper that pulls an image and runs it as a container named `bot_app`.
# Usage: docker-deploy.sh <image> [container_name] [port]

IMAGE=${1:-}
NAME=${2:-bot_app}
PORT=${3:-8000}

if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image> [container_name] [port]" >&2
  exit 2
fi

echo "Deploying image: $IMAGE"

docker pull "$IMAGE"

if docker ps -a --format '{{.Names}}' | grep -q "^${NAME}$"; then
  echo "Stopping and removing existing container: $NAME"
  docker rm -f "$NAME" || true
fi

echo "Running container $NAME (port $PORT -> 8000)"
docker run -d --name "$NAME" --restart unless-stopped -p ${PORT}:8000 "$IMAGE"

echo "Deployment complete."
#!/usr/bin/env bash
set -euo pipefail

# Simple remote helper that pulls an image and runs it as a container named `bot_app`.
# Usage: docker-deploy.sh <image> [container_name] [port]

IMAGE=${1:-}
NAME=${2:-bot_app}
PORT=${3:-8000}

if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image> [container_name] [port]" >&2
  exit 2
fi

echo "Deploying image: $IMAGE"

docker pull "$IMAGE"

if docker ps -a --format '{{.Names}}' | grep -q "^${NAME}$"; then
  echo "Stopping and removing existing container: $NAME"
  docker rm -f "$NAME" || true
fi

echo "Running container $NAME (port $PORT -> 8000)"
docker run -d --name "$NAME" --restart unless-stopped -p ${PORT}:8000 "$IMAGE"

echo "Deployment complete."
#!/usr/bin/env bash
set -euo pipefail

# Simple remote helper that pulls an image and runs it as a container named `bot_app`.
# Usage: docker-deploy.sh <image> [container_name] [port]

IMAGE=${1:-}
NAME=${2:-bot_app}
PORT=${3:-8000}

if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image> [container_name] [port]" >&2
  exit 2
fi

echo "Deploying image: $IMAGE"

docker pull "$IMAGE"

if docker ps -a --format '{{.Names}}' | grep -q "^${NAME}$"; then
  echo "Stopping and removing existing container: $NAME"
  docker rm -f "$NAME" || true
fi

echo "Running container $NAME (port $PORT -> 8000)"
docker run -d --name "$NAME" --restart unless-stopped -p ${PORT}:8000 "$IMAGE"

echo "Deployment complete."

# Use BuildKit features for faster rebuilds when available
# To benefit from pip caching during build set DOCKER_BUILDKIT=1 when running docker build

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps layer first. When requirements.txt doesn't change, Docker will reuse this layer
# --mount=type=cache reuses pip caches between builds (requires BuildKit)
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt

# Copy project source after deps install to keep rebuilds fast
COPY . .

CMD ["bash"]


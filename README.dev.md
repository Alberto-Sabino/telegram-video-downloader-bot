# Development with Docker (temporary container)

This project includes a minimal `Dockerfile` that installs the Python runtime and the packages listed in `requirements.txt`.

Use the provided `dev.sh` helper to build the image and run a temporary container for development.

Quick commands

- Build image and open a shell inside a temporary container:

```bash
./dev.sh
```

- Run tests inside a temporary container (non-interactive):

```bash
./dev.sh pytest -q
```

- Run a one-off Python command inside the container:

```bash
./dev.sh python -m pip list
```

Notes and tips

- The helper mounts your project directory into `/app` inside the container. Any file changes you make on the host are immediately visible inside the container.
- The Dockerfile already runs `pip install -r requirements.txt` during the image build. If you add new dependencies, re-run `./dev.sh` to rebuild.
- Port `8000` is exposed (docker run publishes it to the host) — adjust or add ports if your app needs others.
- The container image is ephemeral: `--rm` removes the container after exit. Use `docker run` without `--rm` if you want to keep containers around.

Troubleshooting

- If Docker Desktop/Engine isn't running on your machine, start it first.
- On Windows with WSL, make sure Docker integration with WSL is enabled or use the Docker engine available to WSL.

If you want, I can also:

- Add a `docker-compose.dev.yml` with a bind-mounted service and a `Makefile` with short commands.
- Modify `Dockerfile` to include development tools (git, build-essential) or a non-root user.
- Add a GitHub Actions workflow to run tests inside this image automatically.

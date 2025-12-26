# CI/CD and deploy guide

This project ships a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

- runs unit tests on push to `main`,
- builds a Docker image and publishes it to GitHub Container Registry (GHCR),
- optionally deploys the image to one of several targets (Fly.io, SSH host, Render, Railway) if the matching secrets are provided,
- creates pull requests to sync `main` into other open branches and can optionally auto-merge them.

Required repository secrets (set in Settings → Secrets → Actions):

- `AUTO_MERGE` (optional): set to `true` to attempt auto-merging the sync PRs when possible.
- `FLY_API_TOKEN` and `FLY_APP_NAME` (optional): enable Fly.io deploy.
- `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY` (optional): enable SSH deploy. `SSH_PRIVATE_KEY` should be the private key in PEM format.
- `RENDER_API_KEY` and `RENDER_SERVICE_ID` (optional): enable Render deploy (uses a simple API call template).
- `RAILWAY_TOKEN` and `RAILWAY_PROJECT_ID` (optional): enable Railway deploy (placeholder/template).

Notes on options

- GHCR: the workflow pushes images to `ghcr.io/<owner>/<repo>:latest` and `...:<sha>`.
- Fly.io: if you choose Fly, create an app and provide `FLY_API_TOKEN` and `FLY_APP_NAME`.
- SSH: the workflow will copy `deploy/docker-deploy.sh` to `/tmp` on the host and run it to pull and run the container.
- Render & Railway: the workflow contains lightweight templates that attempt to trigger a deploy via the providers' APIs. You may need to adapt the payloads depending on your service configuration; treat those steps as a starting point.

Security and safety

- Auto-merge is optional; enabling `AUTO_MERGE=true` may cause branches to be updated automatically. Use with caution if branch protections or code review policies are required.
- The SSH deploy step requires a server with Docker installed and the supplied SSH key authorized for the `SSH_USER` account.

If you want, I can help:
- adapt the Render/Railway API calls to your project settings;
- add an auto-merge policy that waits for required checks to pass before merging;
- add paging/more robust handling for very large repos (the workflow already pages branches using Octokit pagination).
# CI/CD and deploy guide

This project ships a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

- runs unit tests on push to `main`,
- builds a Docker image and publishes it to GitHub Container Registry (GHCR),
- optionally deploys the image to one of several targets (Fly.io, SSH host, Render, Railway) if the matching secrets are provided,
- creates pull requests to sync `main` into other open branches and can optionally auto-merge them.

Required repository secrets (set in Settings → Secrets → Actions):

- `AUTO_MERGE` (optional): set to `true` to attempt auto-merging the sync PRs when possible.
- `FLY_API_TOKEN` and `FLY_APP_NAME` (optional): enable Fly.io deploy.
- `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY` (optional): enable SSH deploy. `SSH_PRIVATE_KEY` should be the private key in PEM format.
- `RENDER_API_KEY` and `RENDER_SERVICE_ID` (optional): enable Render deploy (uses a simple API call template).
- `RAILWAY_TOKEN` and `RAILWAY_PROJECT_ID` (optional): enable Railway deploy (placeholder/template).

Notes on options

- GHCR: the workflow pushes images to `ghcr.io/<owner>/<repo>:latest` and `...:<sha>`.
- Fly.io: if you choose Fly, create an app and provide `FLY_API_TOKEN` and `FLY_APP_NAME`.
- SSH: the workflow will copy `deploy/docker-deploy.sh` to `/tmp` on the host and run it to pull and run the container.
- Render & Railway: the workflow contains lightweight templates that attempt to trigger a deploy via the providers' APIs. You may need to adapt the payloads depending on your service configuration; treat those steps as a starting point.

Security and safety

- Auto-merge is optional; enabling `AUTO_MERGE=true` may cause branches to be updated automatically. Use with caution if branch protections or code review policies are required.
- The SSH deploy step requires a server with Docker installed and the supplied SSH key authorized for the `SSH_USER` account.

If you want, I can help:
- adapt the Render/Railway API calls to your project settings;
- add an auto-merge policy that waits for required checks to pass before merging;
- add paging/more robust handling for very large repos (the workflow already pages branches using Octokit pagination).
# CI/CD and deploy guide

This project ships a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

- runs unit tests on push to `main`,
- builds a Docker image and publishes it to GitHub Container Registry (GHCR),
- optionally deploys the image to one of several targets (Fly.io, SSH host, Render, Railway) if the matching secrets are provided,
- creates pull requests to sync `main` into other open branches and can optionally auto-merge them.

Required repository secrets (set in Settings → Secrets → Actions):

- `AUTO_MERGE` (optional): set to `true` to attempt auto-merging the sync PRs when possible.
- `FLY_API_TOKEN` and `FLY_APP_NAME` (optional): enable Fly.io deploy.
- `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY` (optional): enable SSH deploy. `SSH_PRIVATE_KEY` should be the private key in PEM format.
- `RENDER_API_KEY` and `RENDER_SERVICE_ID` (optional): enable Render deploy (uses a simple API call template).
- `RAILWAY_TOKEN` and `RAILWAY_PROJECT_ID` (optional): enable Railway deploy (placeholder/template).

Notes on options

- GHCR: the workflow pushes images to `ghcr.io/<owner>/<repo>:latest` and `...:<sha>`.
- Fly.io: if you choose Fly, create an app and provide `FLY_API_TOKEN` and `FLY_APP_NAME`.
- SSH: the workflow will copy `deploy/docker-deploy.sh` to `/tmp` on the host and run it to pull and run the container.
- Render & Railway: the workflow contains lightweight templates that attempt to trigger a deploy via the providers' APIs. You may need to adapt the payloads depending on your service configuration; treat those steps as a starting point.

Security and safety

- Auto-merge is optional; enabling `AUTO_MERGE=true` may cause branches to be updated automatically. Use with caution if branch protections or code review policies are required.
- The SSH deploy step requires a server with Docker installed and the supplied SSH key authorized for the `SSH_USER` account.

If you want, I can help:
- adapt the Render/Railway API calls to your project settings;
- add an auto-merge policy that waits for required checks to pass before merging;
- add paging/more robust handling for very large repos (the workflow already pages branches using Octokit pagination).

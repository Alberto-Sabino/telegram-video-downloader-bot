## Repo overview

This is a small Telegram bot project split into a lightweight domain layer (`botlib`) and a tiny compatibility shim (`bot.py`). Key responsibilities:

- `botlib/` — core package with business logic and small adapters:
  - `services.py` — domain/service layer: `handle_update(update, adapter)` implements behavior (URL detection, download, zipping, fallback upload).
  - `telegram_adapter.py` — minimal Telegram API adapter (polling, send_message, send_document). Handler contract: handler(update: dict, adapter).
  - `http_client.py` — normalized `get`/`post` helpers that return a response dict (no exceptions raised).
  - `downloader.py` — wrapper around `yt_dlp` (`download_video(url, out_dir)`); returns filepath or None.
  - `logger.py` — `get_logger(name)` centralizes logging setup.

- `bot.py` — a backward-compat shim re-exporting `get`/`post` for older imports.
- `bot_app.py` — exposes FastAPI `app` for webhook mode and contains polling/webhook startup helpers. It expects env vars `MODE`, `TELEGRAM_TOKEN`, and `WEBHOOK_URL` for webhook mode.

## Important patterns & conventions (for an AI to follow)

- Adapter pattern: business logic in `services.py` never calls HTTP directly — it receives an `adapter` object and calls `adapter.send_message(...)` or `adapter.send_document(...)`. When making changes, preserve this boundary.
- Normalized HTTP responses: `botlib.http_client.get/post` return dicts with keys `ok`, `status`, `headers`, `body`, and optional `error`. Tests and adapters expect this structure — do not raise exceptions from these helpers.
- Handler signature: functions that process updates accept `(update: dict, adapter)`; unit tests patch functions imported into modules (see tests that patch `botlib.telegram_adapter.get` and `botlib.telegram_adapter.post`). When writing tests, patch the names imported by the module under test (patch where they are used, not where they are defined).
- External deps: `requests` and `yt-dlp` are runtime dependencies. `downloader.py` returns `None` if `yt_dlp` is unavailable — callers check for None.

## Env vars and runtime modes

- TELEGRAM_TOKEN — bot token (required for polling or adapter construction).
- MODE — `polling` (default) or `webhook`. `bot_app.py` exposes `app` for ASGI servers in webhook mode.
- WEBHOOK_URL — required when MODE=webhook; `bot_app.set_webhook` will call Telegram's setWebhook.
- TELEGRAM_MAX_UPLOAD_BYTES — cutoff (bytes) used to decide whether to send via Telegram or fallback to `transfer.sh`.

## Developer workflows

- Run tests locally: pytest (the repo includes simple pytest-based unit tests that mock network interactions).
- Docker/dev container: use `./dev.sh` to build and run a temporary dev container; tests can be run inside the container (`./dev.sh pytest -q`).
- Run webhook ASGI: expose `bot_app.app` to an ASGI server (e.g. `uvicorn bot_app:app --host 0.0.0.0 --port 8000`) and set `WEBHOOK_URL` to a reachable HTTPS URL including `/webhook/{TELEGRAM_TOKEN}`.
- Run polling locally: set `TELEGRAM_TOKEN` and run `python bot_app.py` (defaults to polling mode unless `MODE=webhook`).

## Testing notes & examples

- Tests mock the `requests` calls inside `botlib.http_client` and patch names imported into modules. Example: tests patch `botlib.telegram_adapter.get` (not `botlib.http_client.get`) because the adapter imports those names.
- Example: to simulate an incoming update in tests, create `update = {"update_id": 1, "message": {"chat": {"id": 123}, "text": "hi"}}` and call `botlib.handle_update(update, adapter_mock)`.

## Quick pointers for changes

- If you add network behavior, prefer using `botlib.http_client` and keep its normalized response contract.
- If you change the adapter surface, update tests that construct or patch `TelegramAdapter` (they assume `send_message` returns a dict with `ok`).
- Keep `services.py` free of HTTP specifics — it should only orchestrate downloads and call adapter methods so it remains testable.

If anything here is unclear or you'd like more examples (test snippets, typical refactors), tell me what to expand and I will iterate.
## Repo overview

This is a small Telegram bot project split into a lightweight domain layer (`botlib`) and a tiny compatibility shim (`bot.py`). Key responsibilities:

- `botlib/` — core package with business logic and small adapters:
  - `services.py` — domain/service layer: `handle_update(update, adapter)` implements behavior (URL detection, download, zipping, fallback upload).
  - `telegram_adapter.py` — minimal Telegram API adapter (polling, send_message, send_document). Handler contract: handler(update: dict, adapter).
  - `http_client.py` — normalized `get`/`post` helpers that return a response dict (no exceptions raised).
  - `downloader.py` — wrapper around `yt_dlp` (`download_video(url, out_dir)`); returns filepath or None.
  - `logger.py` — `get_logger(name)` centralizes logging setup.

- `bot.py` — a backward-compat shim re-exporting `get`/`post` for older imports.
- `bot_app.py` — exposes FastAPI `app` for webhook mode and contains polling/webhook startup helpers. It expects env vars `MODE`, `TELEGRAM_TOKEN`, and `WEBHOOK_URL` for webhook mode.

## Important patterns & conventions (for an AI to follow)

- Adapter pattern: business logic in `services.py` never calls HTTP directly — it receives an `adapter` object and calls `adapter.send_message(...)` or `adapter.send_document(...)`. When making changes, preserve this boundary.
- Normalized HTTP responses: `botlib.http_client.get/post` return dicts with keys `ok`, `status`, `headers`, `body`, and optional `error`. Tests and adapters expect this structure — do not raise exceptions from these helpers.
- Handler signature: functions that process updates accept `(update: dict, adapter)`; unit tests patch functions imported into modules (see tests that patch `botlib.telegram_adapter.get` and `botlib.telegram_adapter.post`). When writing tests, patch the names imported by the module under test (patch where they are used, not where they are defined).
- External deps: `requests` and `yt-dlp` are runtime dependencies. `downloader.py` returns `None` if `yt_dlp` is unavailable — callers check for None.

## Env vars and runtime modes

- TELEGRAM_TOKEN — bot token (required for polling or adapter construction).
- MODE — `polling` (default) or `webhook`. `bot_app.py` exposes `app` for ASGI servers in webhook mode.
- WEBHOOK_URL — required when MODE=webhook; `bot_app.set_webhook` will call Telegram's setWebhook.
- TELEGRAM_MAX_UPLOAD_BYTES — cutoff (bytes) used to decide whether to send via Telegram or fallback to `transfer.sh`.

## Developer workflows

- Run tests locally: pytest (the repo includes simple pytest-based unit tests that mock network interactions).
- Docker/dev container: use `./dev.sh` to build and run a temporary dev container; tests can be run inside the container (`./dev.sh pytest -q`).
- Run webhook ASGI: expose `bot_app.app` to an ASGI server (e.g. `uvicorn bot_app:app --host 0.0.0.0 --port 8000`) and set `WEBHOOK_URL` to a reachable HTTPS URL including `/webhook/{TELEGRAM_TOKEN}`.
- Run polling locally: set `TELEGRAM_TOKEN` and run `python bot_app.py` (defaults to polling mode unless `MODE=webhook`).

## Testing notes & examples

- Tests mock the `requests` calls inside `botlib.http_client` and patch names imported into modules. Example: tests patch `botlib.telegram_adapter.get` (not `botlib.http_client.get`) because the adapter imports those names.
- Example: to simulate an incoming update in tests, create `update = {"update_id": 1, "message": {"chat": {"id": 123}, "text": "hi"}}` and call `botlib.handle_update(update, adapter_mock)`.

## Quick pointers for changes

- If you add network behavior, prefer using `botlib.http_client` and keep its normalized response contract.
- If you change the adapter surface, update tests that construct or patch `TelegramAdapter` (they assume `send_message` returns a dict with `ok`).
- Keep `services.py` free of HTTP specifics — it should only orchestrate downloads and call adapter methods so it remains testable.

If anything here is unclear or you'd like more examples (test snippets, typical refactors), tell me what to expand and I will iterate.

"""Entrypoint for running the bot in polling or webhook mode.

Supports two modes controlled by the `MODE` env var: `polling` (default) and
`webhook`. For webhook mode you must set `WEBHOOK_URL` to a public HTTPS URL
where Telegram can POST updates. The FastAPI `app` is exposed so you can run
it with Uvicorn.
"""

import os
import logging
from typing import Any, Dict

from fastapi import FastAPI, Request, Response

from botlib.telegram_adapter import TelegramAdapter
from botlib.services import handle_update
from botlib.logger import get_logger


logger = get_logger(__name__)

app = FastAPI()


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.post("/webhook/{token}")
async def webhook(token: str, request: Request) -> Response:
    body = await request.json()
    # Basic auth: ensure token matches
    bot_token = os.getenv("TELEGRAM_TOKEN")
    if not bot_token or token != bot_token:
        logger.warning("Webhook token mismatch or missing")
        return Response(status_code=403)

    # Telegram sends the update as JSON body
    try:
        handle_update(body, TelegramAdapter(token=bot_token))
    except Exception:
        logger.exception("Error handling webhook update")
    return Response(status_code=200)


def set_webhook(token: str, webhook_url: str) -> bool:
    import requests

    url = f"https://api.telegram.org/bot{token}/setWebhook"
    data = {"url": webhook_url}
    try:
        resp = requests.post(url, data=data, timeout=10)
        resp.raise_for_status()
        return True
    except Exception:
        logger.exception("Failed to set webhook")
        return False


def run_polling():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN is required for polling mode")
    adapter = TelegramAdapter(token=token)
    adapter.run_polling(handle_update)


def main():
    mode = os.getenv("MODE", "polling").lower()
    if mode == "webhook":
        webhook_host = os.getenv("WEBHOOK_URL")
        token = os.getenv("TELEGRAM_TOKEN")
        if not webhook_host or not token:
            raise RuntimeError("WEBHOOK_URL and TELEGRAM_TOKEN are required for webhook mode")
        target = f"{webhook_host.rstrip('/')}/webhook/{token}"
        ok = set_webhook(token, target)
        if not ok:
            raise RuntimeError("Failed to set webhook")
        # Run Uvicorn externally; this module exposes `app` for ASGI servers.
        logger.info("Webhook configured; start ASGI server to receive updates")
    else:
        logger.info("Starting polling mode")
        run_polling()


if __name__ == "__main__":
    main()

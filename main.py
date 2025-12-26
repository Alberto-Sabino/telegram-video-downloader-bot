"""Production-friendly launcher for the bot.

This module provides two common production entry patterns:

- Polling mode: start long-running polling loop (default). Requires
  `TELEGRAM_TOKEN` env var.
- Webhook mode: configure Telegram webhook (calls `set_webhook`) and
  expose the FastAPI `app` using an ASGI server (recommended `uvicorn`).

The project already contains `bot_app.py` which exposes `app` and
`run_polling()` helpers; this script uses those helpers and documents
the recommended `uvicorn` command used by `Dockerfile.prod`.
"""

import os
import sys
import logging

from bot_app import set_webhook, run_polling
from botlib.logger import get_logger

logger = get_logger(__name__)


def main():
	mode = os.getenv("MODE", "polling").lower()
	token = os.getenv("TELEGRAM_TOKEN")

	if mode == "webhook":
		webhook_url = os.getenv("WEBHOOK_URL")
		if not token or not webhook_url:
			logger.error("WEBHOOK mode requires TELEGRAM_TOKEN and WEBHOOK_URL environment variables")
			sys.exit(2)

		target = f"{webhook_url.rstrip('/')}/webhook/{token}"
		logger.info("Setting webhook to %s", target)
		ok = set_webhook(token, target)
		if not ok:
			logger.error("Failed to set webhook")
			sys.exit(1)

		logger.info("Webhook configured. Start an ASGI server that exposes `bot_app:app`.")
		logger.info("Recommended (same as Dockerfile.prod): uvicorn bot_app:app --host 0.0.0.0 --port 8000")
		return

	# default: polling
	if not token:
		logger.error("TELEGRAM_TOKEN is required for polling mode")
		sys.exit(2)

	logger.info("Starting polling mode")
	try:
		run_polling()
	except KeyboardInterrupt:
		logger.info("Polling stopped by user")


if __name__ == "__main__":
	main()

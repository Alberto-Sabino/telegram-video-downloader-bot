"""A minimal Telegram Bot API adapter using polling.

This adapter is deliberately small and depends only on the project's
`http_client` so it's easy to test and swap implementations.
"""

import os
import time
from typing import Any, Dict, Iterable, List, Optional

from . import get, post
from .logger import get_logger


logger = get_logger(__name__)


class TelegramAdapter:
    """Simple polling adapter for Telegram Bot API.

    Usage:
      adapter = TelegramAdapter(token)
      updates = adapter.get_updates()
      adapter.send_message(chat_id, "hi")
    """

    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("Telegram token must be provided via constructor or TELEGRAM_TOKEN env")
        self.base_url = base_url or f"https://api.telegram.org/bot{self.token}"

    def _url(self, method: str) -> str:
        return f"{self.base_url}/{method}"

    def get_updates(self, offset: Optional[int] = None, timeout: int = 10) -> List[Dict[str, Any]]:
        params = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset
        url = self._url("getUpdates")
        result = get(url, params=params)
        if not result.get("ok"):
            logger.warning("getUpdates failed: %s", result.get("error"))
            return []
        return result.get("body", {}).get("result", [])

    def send_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        url = self._url("sendMessage")
        payload = {"chat_id": chat_id, "text": text}
        return post(url, payload)

    def send_document(self, chat_id: int, file_path: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """Send a file to the given chat using sendDocument (multipart upload).

        Returns a normalized response dict similar to `post`/`get`.
        """
        # Use requests directly to send multipart/form-data
        try:
            import requests
        except Exception:
            return {"ok": False, "status": None, "headers": {}, "body": None, "error": "requests not available"}

        url = self._url("sendDocument")
        files = {"document": (filename or os.path.basename(file_path), open(file_path, "rb"))}
        data = {"chat_id": str(chat_id)}
        try:
            resp = requests.post(url, data=data, files=files)
            resp.raise_for_status()
        except Exception as exc:
            logger.exception("Failed to upload document")
            return {"ok": False, "status": None, "headers": {}, "body": None, "error": str(exc)}

        try:
            body = resp.json()
        except Exception:
            body = resp.text

        return {"ok": resp.ok, "status": resp.status_code, "headers": dict(resp.headers), "body": body}

    def run_polling(self, handler, poll_interval: float = 1.0):
        """Continuously poll for updates and dispatch to `handler(update, self)`.

        Handler is a callable that receives (update: dict, adapter: TelegramAdapter).
        """
        offset = None
        try:
            while True:
                updates = self.get_updates(offset=offset)
                for upd in updates:
                    offset = max(offset or 0, upd.get("update_id", 0) + 1)
                    try:
                        handler(upd, self)
                    except Exception:
                        logger.exception("Error in update handler")
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            logger.info("Polling stopped by user")


__all__ = ["TelegramAdapter"]

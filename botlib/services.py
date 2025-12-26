"""Domain/service layer for update handling.

Keep business logic separated from adapters. Handlers receive plain
update dicts (as returned by Telegram getUpdates) and use the adapter to
perform side effects.
"""

from typing import Dict, Any

import os
import re
import shutil
import tempfile
import zipfile

from .logger import get_logger
from .downloader import download_video


logger = get_logger(__name__)


URL_RE = re.compile(r"https?://\S+")


def handle_update(update: Dict[str, Any], adapter) -> None:
    """Handle a single update. If text contains a URL, download video and send a zip.

    Otherwise, echo the text back.
    """
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        logger.debug("Ignoring non-message update: %s", update)
        return

    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    text = msg.get("text")
    if chat_id is None:
        logger.debug("Message missing chat_id: %s", msg)
        return

    if text:
        # Look for first URL in text
        m = URL_RE.search(text)
        if m:
            url = m.group(0)
            logger.info("Detected URL in message: %s", url)
            temp_dir = tempfile.mkdtemp(prefix="bot_dl_")
            try:
                downloaded = download_video(url, temp_dir)
                if not downloaded:
                    adapter.send_message(chat_id, "Sorry, I couldn't download that video.")
                    return

                # create a zip archive containing the downloaded file
                zip_path = os.path.join(temp_dir, "video.zip")
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.basename(downloaded)
                    zf.write(downloaded, arcname=arcname)

                # If file is too large for Telegram, optionally upload to transfer.sh and send link
                max_bytes = int(os.getenv("TELEGRAM_MAX_UPLOAD_BYTES", str(50 * 1024 * 1024)))
                size = os.path.getsize(zip_path)
                if size > max_bytes:
                    # try to upload to transfer.sh as a fallback
                    try:
                        import requests

                        with open(zip_path, "rb") as fh:
                            files = {"file": ("video.zip", fh)}
                            r = requests.post("https://transfer.sh/", files=files, timeout=60)
                        if r.status_code == 200:
                            link = r.text.strip()
                            adapter.send_message(chat_id, f"File too large to send via Telegram. Download it here: {link}")
                        else:
                            adapter.send_message(chat_id, "File too large to send, and fallback upload failed.")
                    except Exception:
                        adapter.send_message(chat_id, "File too large and fallback upload failed.")
                else:
                    result = adapter.send_document(chat_id, zip_path, filename="video.zip")
                    if not result.get("ok"):
                        adapter.send_message(chat_id, "Failed to upload the video.")
                return
            finally:
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass

    # Fallback echo behavior
    text = text or ""
    reply = f"Echo: {text}"
    result = adapter.send_message(chat_id, reply)
    if not result.get("ok"):
        logger.warning("Failed to send reply: %s", result.get("error"))


__all__ = ["handle_update"]

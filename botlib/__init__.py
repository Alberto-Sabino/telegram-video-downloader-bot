"""Lightweight bot library package.

Expose stable helpers used by the rest of the project. Designed so tests and
existing imports continue to work while the internal layout follows a
cleaner package structure.
"""

from .http_client import get, post
from .logger import get_logger

# optional components
from .telegram_adapter import TelegramAdapter  # type: ignore
from .services import handle_update  # type: ignore

__all__ = ["get", "post", "get_logger", "TelegramAdapter", "handle_update"]

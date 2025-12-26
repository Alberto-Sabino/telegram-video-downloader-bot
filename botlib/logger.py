"""Simple logger wrapper for consistent logging across the bot.

This keeps logging configuration in one place so we can later route logs to
files, external sinks, or adjust formatting without touching business code.
"""

import logging
from typing import Optional


def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger instance.

    This function is idempotent and safe to call from multiple modules.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


__all__ = ["get_logger"]

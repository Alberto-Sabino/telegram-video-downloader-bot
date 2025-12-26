"""HTTP helpers for the bot.

This module provides `get` and `post` functions that return a normalized
response dict instead of raising. It intentionally keeps a small surface
area and minimal dependencies so it's easy to test and reuse in adapters.
"""

from typing import Any, Dict, Optional

try:
    import requests
    from requests import Response
except Exception:  # pragma: no cover - fallback if requests isn't installed
    requests = None  # type: ignore

DEFAULT_TIMEOUT = 10.0


def _format_response(response: Response) -> Dict[str, Any]:
    try:
        body = response.json()
    except Exception:
        body = response.text

    return {
        "ok": response.ok,
        "status": response.status_code,
        "headers": dict(response.headers),
        "body": body,
    }


def post(url: str,
         message: Any,
         headers: Optional[Dict[str, str]] = None,
         timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    if requests is None:
        return {"ok": False, "status": None, "headers": {}, "body": None,
                "error": "`requests` library not available"}

    try:
        resp = requests.post(url, json=message, headers=headers, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "status": None, "headers": {}, "body": None,
                "error": str(exc)}

    result = _format_response(resp)
    if not resp.ok:
        result.setdefault("error", None)
    return result


def get(url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    if requests is None:
        return {"ok": False, "status": None, "headers": {}, "body": None,
                "error": "`requests` library not available"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "status": None, "headers": {}, "body": None,
                "error": str(exc)}

    result = _format_response(resp)
    if not resp.ok:
        result.setdefault("error", None)
    return result


__all__ = ["get", "post"]

"""Backward-compatibility shim.

This module re-exports the cleaned-up implementations from the `botlib`
package so older imports continue to work while we migrate internals.
"""

from botlib.http_client import get, post

__all__ = ["get", "post"]

"""Download videos from many sites using yt-dlp.

This module provides a small wrapper around `yt_dlp` to download a single
video into `out_dir` and return the downloaded filepath.
"""

import os
from typing import Optional

try:
    from yt_dlp import YoutubeDL
except Exception:  # pragma: no cover - runtime dependency
    YoutubeDL = None  # type: ignore


def download_video(url: str, out_dir: str) -> Optional[str]:
    """Download `url` into `out_dir` and return the path of the downloaded file.

    Returns None on error (caller should handle and report back to user).
    """
    if YoutubeDL is None:
        return None

    os.makedirs(out_dir, exist_ok=True)
    # output template: choose title.ext
    outtmpl = os.path.join(out_dir, "%(title)s.%(ext)s")
    ydl_opts = {
        "outtmpl": outtmpl,
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
        # quiet=False so that callers can enable logging; keep default verbosity low
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # info may be a dict for single video; determine filename
            filename = ydl.prepare_filename(info)
            if os.path.exists(filename):
                return filename
            # sometimes prepare_filename uses ext not matching; try to find a file in out_dir
            for f in os.listdir(out_dir):
                path = os.path.join(out_dir, f)
                if os.path.isfile(path):
                    return path
    except Exception:
        return None

    return None

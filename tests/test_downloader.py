import os

import pytest

from botlib import downloader


def test_download_no_yt_dlp(monkeypatch, tmp_path):
    monkeypatch.setattr(downloader, "YoutubeDL", None)
    out = downloader.download_video("http://x", str(tmp_path))
    assert out is None


def test_download_success(monkeypatch, tmp_path):
    # Fake YoutubeDL implementation
    class FakeYDL:
        def __init__(self, opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download=True):
            return {"id": "abc"}

        def prepare_filename(self, info):
            return str(tmp_path / "title.mp4")

    monkeypatch.setattr(downloader, "YoutubeDL", FakeYDL)
    # create the expected file
    p = tmp_path / "title.mp4"
    p.write_bytes(b"ok")

    out = downloader.download_video("http://x", str(tmp_path))
    assert out is not None
    assert out.endswith("title.mp4")


def test_prepare_filename_missing_uses_first_file(monkeypatch, tmp_path):
    # Fake YoutubeDL where prepare_filename returns a non-existent file
    class FakeYDL:
        def __init__(self, opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download=True):
            return {"id": "abc"}

        def prepare_filename(self, info):
            return str(tmp_path / "not_there.mp4")

    monkeypatch.setattr(downloader, "YoutubeDL", FakeYDL)
    # create a real file in out_dir so fallback can pick it
    real = tmp_path / "found.mp4"
    real.write_bytes(b"ok")

    out = downloader.download_video("http://x", str(tmp_path))
    assert out is not None
    assert out.endswith("found.mp4")

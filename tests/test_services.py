import os
import sys
import tempfile
import zipfile

import pytest

from botlib import services


class DummyAdapter:
    def __init__(self):
        self.calls = []

    def send_message(self, chat_id, text):
        self.calls.append(("send_message", chat_id, text))
        return {"ok": True}

    def send_document(self, chat_id, file_path, filename=None):
        self.calls.append(("send_document", chat_id, file_path, filename))
        return {"ok": True}


def test_echo_message(monkeypatch):
    adapter = DummyAdapter()
    update = {"update_id": 1, "message": {"chat": {"id": 42}, "text": "hello"}}
    services.handle_update(update, adapter)

    assert adapter.calls
    typ, cid, text = adapter.calls[0]
    assert typ == "send_message"
    assert cid == 42
    assert text == "Echo: hello"


def test_non_message_update_is_ignored(monkeypatch):
    adapter = DummyAdapter()
    update = {"update_id": 1, "edited_channel_post": {"some": "value"}}
    services.handle_update(update, adapter)
    assert adapter.calls == []


def test_handle_url_triggers_download_and_send(monkeypatch, tmp_path):
    # Create a fake downloaded file and patch download_video to return it
    dl_dir = tmp_path
    downloaded = dl_dir / "video.mp4"
    downloaded.write_bytes(b"fake video")

    def fake_download(url, out_dir):
        return str(downloaded)

    monkeypatch.setattr(services, "download_video", fake_download)

    adapter = DummyAdapter()
    update = {"update_id": 2, "message": {"chat": {"id": 99}, "text": "check this https://example.com"}}
    services.handle_update(update, adapter)

    # ensure document was sent
    assert any(c[0] == "send_document" for c in adapter.calls)


def test_large_file_triggers_transfer_sh_fallback(monkeypatch, tmp_path):
    # Create a fake downloaded file
    dl_dir = tmp_path
    downloaded = dl_dir / "bigfile.mp4"
    downloaded.write_bytes(b"x" * 1024)

    def fake_download(url, out_dir):
        return str(downloaded)

    monkeypatch.setattr(services, "download_video", fake_download)

    # Force TELEGRAM_MAX_UPLOAD_BYTES very small so zip will be larger
    monkeypatch.setenv("TELEGRAM_MAX_UPLOAD_BYTES", "1")

    # Provide a fake requests.post used by the fallback upload
    class FakeResp:
        status_code = 200

        def __init__(self, text):
            self.text = text

    def fake_post(url, files=None, timeout=None):
        return FakeResp("https://transfer.sh/fake-link")

    sys_modules = sys.modules
    # ensure requests is available for import in services
    import types

    fake_requests = types.SimpleNamespace(post=fake_post)
    monkeypatch.setitem(sys_modules, "requests", fake_requests)

    adapter = DummyAdapter()
    update = {"update_id": 3, "message": {"chat": {"id": 100}, "text": "http://foo"}}
    services.handle_update(update, adapter)

    # fallback should send a message containing transfer.sh link
    assert any(c[0] == "send_message" and ("transfer.sh" in c[2] or "https://transfer.sh" in c[2]) for c in adapter.calls)


def test_download_failure_sends_error_message(monkeypatch):
    # simulate download_video returning None
    monkeypatch.setattr(services, "download_video", lambda url, out_dir: None)
    adapter = DummyAdapter()
    update = {"update_id": 10, "message": {"chat": {"id": 7}, "text": "http://nope"}}
    services.handle_update(update, adapter)

    # should send a sorry message
    assert any(c[0] == "send_message" and "couldn't download" in c[2] for c in adapter.calls)


def test_fallback_upload_failure_sends_message(monkeypatch, tmp_path):
    # create a fake downloaded file
    downloaded = tmp_path / "video.mp4"
    downloaded.write_bytes(b"x" * 1024)

    monkeypatch.setattr(services, "download_video", lambda url, out_dir: str(downloaded))
    monkeypatch.setenv("TELEGRAM_MAX_UPLOAD_BYTES", "1")

    class FakeResp:
        status_code = 500
        def __init__(self, text=""):
            self.text = text

    def fake_post(url, files=None, timeout=None):
        return FakeResp("")

    import sys, types
    fake_requests = types.SimpleNamespace(post=fake_post)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    adapter = DummyAdapter()
    update = {"update_id": 11, "message": {"chat": {"id": 8}, "text": "http://big"}}
    services.handle_update(update, adapter)

    # fallback upload failed -> send_message called with failure note
    assert any(c[0] == "send_message" and ("fallback upload failed" in c[2] or "too large" in c[2]) for c in adapter.calls)

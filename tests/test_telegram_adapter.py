import sys
import types

import pytest

from botlib.telegram_adapter import TelegramAdapter


def test_init_without_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
    with pytest.raises(ValueError):
        TelegramAdapter(token=None)


def test_send_message_uses_post(monkeypatch):
    def fake_post(url, message, headers=None, timeout=None):
        return {"ok": True, "status": 200, "headers": {}, "body": {}}

    monkeypatch.setattr("botlib.telegram_adapter.post", fake_post)
    adapter = TelegramAdapter(token="tok", base_url="http://api")
    res = adapter.send_message(1, "hi")
    assert res["ok"] is True


def test_send_document_uses_requests(monkeypatch, tmp_path):
    fn = tmp_path / "f.txt"
    fn.write_text("x")

    class FakeResp:
        ok = True
        status_code = 200
        headers = {}

        def json(self):
            return {"ok": True}
        
        def raise_for_status(self):
            return None

    def fake_requests_post(url, data=None, files=None):
        return FakeResp()

    fake_requests = types.SimpleNamespace(post=fake_requests_post)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    adapter = TelegramAdapter(token="tok", base_url="http://api")
    res = adapter.send_document(1, str(fn))
    assert res["ok"] is True


def test_get_updates_handles_error(monkeypatch):
    # make get return a non-ok result
    monkeypatch.setattr("botlib.telegram_adapter.get", lambda url, params=None, headers=None, timeout=None: {"ok": False, "error": "boom"})
    adapter = TelegramAdapter(token="tok", base_url="http://api")
    updates = adapter.get_updates()
    assert updates == []


def test_run_polling_stops_on_keyboardinterrupt(monkeypatch):
    # Make get_updates raise KeyboardInterrupt to exit the loop
    def fake_get_updates(self, offset=None, timeout=10):
        raise KeyboardInterrupt()

    monkeypatch.setattr(TelegramAdapter, "get_updates", fake_get_updates)

    adapter = TelegramAdapter(token="tok", base_url="http://api")

    # handler should not be called; run_polling should catch KeyboardInterrupt
    called = {"h": False}

    def handler(update, adp):
        called["h"] = True

    adapter.run_polling(handler, poll_interval=0)
    assert called["h"] is False

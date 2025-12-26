import types

from botlib import http_client


def test_requests_not_available(monkeypatch):
    monkeypatch.setattr(http_client, "requests", None)
    r = http_client.get("http://x")
    assert r["ok"] is False
    assert "error" in r
    r2 = http_client.post("http://x", {"k": "v"})
    assert r2["ok"] is False


def test_get_request_exception(monkeypatch):
    class FakeRequests:
        class exceptions:
            RequestException = Exception

        def get(self, url, params=None, headers=None, timeout=None):
            raise Exception("boom")

    monkeypatch.setattr(http_client, "requests", FakeRequests())
    res = http_client.get("http://x")
    assert res["ok"] is False
    assert "error" in res


def test_format_response_non_json(monkeypatch):
    # create a fake Response-like object where json() raises
    class FakeResp:
        ok = True
        status_code = 200
        headers = {"h": "v"}
        text = "plain text"

        def json(self):
            raise ValueError("no json")

    out = http_client._format_response(FakeResp())
    assert out["body"] == "plain text"

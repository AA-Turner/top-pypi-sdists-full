import hashlib
import hmac
import json

import pytest
import requests

import omnidoc.client as client_module
from omnidoc import JobFailedError, OmniDocClient, OmniDocError, parse_webhook, verify_webhook


class FakeResponse:
    def __init__(self, status_code=200, body=None, headers=None, content=b""):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}
        self.content = content
        self.reason = "OK" if status_code < 400 else "Error"

    def json(self):
        if self._body is None:
            raise ValueError("no json body")
        return self._body

    def iter_content(self, chunk_size=1):
        yield self.content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0)


class PutOk:
    status_code = 200

    def raise_for_status(self):
        return None


@pytest.fixture
def sleeps(monkeypatch):
    recorded = []
    monkeypatch.setattr(client_module.time, "sleep", lambda seconds: recorded.append(seconds))
    return recorded


def make_client(responses, **kwargs):
    session = FakeSession(responses)
    return OmniDocClient("sk_test", session=session, **kwargs), session


def test_api_key_is_read_from_environment(monkeypatch):
    monkeypatch.setenv("OMNIDOC_API_KEY", "sk_env")
    client = OmniDocClient(session=FakeSession([]))
    assert client._api_key == "sk_env"


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("OMNIDOC_API_KEY", raising=False)
    with pytest.raises(ValueError):
        OmniDocClient(session=FakeSession([]))


def test_request_sends_key_header_to_api_base():
    client, session = make_client([FakeResponse(200, {"balance": 10})])
    assert client.credit_balance() == {"balance": 10}
    method, url, kwargs = session.calls[0]
    assert method == "GET"
    assert url == "https://omnidoc.top/api/v1/billing/credits/balance"
    assert kwargs["headers"]["X-API-Key"] == "sk_test"


def test_retries_429_using_retry_after(sleeps):
    client, session = make_client(
        [
            FakeResponse(429, {"code": "RATE_LIMITED", "message": "slow down"}, {"Retry-After": "7"}),
            FakeResponse(200, {"ok": 1}),
        ]
    )
    assert client.usage_summary() == {"ok": 1}
    assert sleeps == [7.0]
    assert len(session.calls) == 2


def test_quota_exceeded_is_not_retried(sleeps):
    client, session = make_client(
        [FakeResponse(429, {"code": "AUTH_API_KEY_QUOTA_EXCEEDED", "message": "quota used up"})]
    )
    with pytest.raises(OmniDocError) as info:
        client.usage_summary()
    assert info.value.code == "AUTH_API_KEY_QUOTA_EXCEEDED"
    assert sleeps == []
    assert len(session.calls) == 1


def test_gives_up_after_max_retries(sleeps):
    client, session = make_client(
        [FakeResponse(503, {"message": "busy"}) for _ in range(3)], max_retries=2
    )
    with pytest.raises(OmniDocError) as info:
        client.usage_summary()
    assert info.value.status_code == 503
    assert len(session.calls) == 3


def test_error_carries_request_id():
    client, _ = make_client(
        [FakeResponse(401, {"code": "UNAUTHORIZED", "message": "bad key"}, {"X-Request-Id": "req-1"})]
    )
    with pytest.raises(OmniDocError) as info:
        client.usage_summary()
    assert info.value.status_code == 401
    assert info.value.request_id == "req-1"


def test_422_field_list_becomes_readable_message():
    client, _ = make_client(
        [FakeResponse(422, {"detail": [{"loc": ["body", "target_lang"], "msg": "Field required"}]})]
    )
    with pytest.raises(OmniDocError) as info:
        client.post_json("jobs", json={})
    assert info.value.message == "参数校验失败"


def test_create_job_sends_idempotency_key_and_only_set_options():
    client, session = make_client([FakeResponse(201, {"id": "job1", "status": "pending"})])
    job = client.create_job(
        "doc1", "en", output_mode="bilingual", engine="xr-397b", idempotency_key="key-1"
    )
    assert job["id"] == "job1"
    method, url, kwargs = session.calls[0]
    assert method == "POST" and url.endswith("/jobs")
    assert kwargs["headers"]["Idempotency-Key"] == "key-1"
    assert kwargs["json"] == {
        "document_id": "doc1",
        "target_lang": "en",
        "output_mode": "bilingual",
        "engine": "xr-397b",
    }


def test_create_job_retry_reuses_idempotency_key(sleeps):
    client, session = make_client(
        [FakeResponse(503, {"message": "busy"}), FakeResponse(201, {"id": "job2"})]
    )
    client.create_job("doc1", "en", idempotency_key="same-key")
    keys = [call[2]["headers"]["Idempotency-Key"] for call in session.calls]
    assert keys == ["same-key", "same-key"]


def test_upload_runs_presign_put_finalize(monkeypatch, tmp_path):
    source = tmp_path / "report.docx"
    source.write_bytes(b"hello")
    put_calls = []

    def fake_put(url, headers=None, data=None, timeout=None):
        put_calls.append((url, headers, data.read()))
        return PutOk()

    monkeypatch.setattr(client_module.requests, "put", fake_put)
    client, session = make_client(
        [
            FakeResponse(
                200,
                {
                    "upload_url": "https://upload.example/x",
                    "upload_headers": {"Content-Type": "application/octet-stream"},
                    "finalize_token": "tok",
                },
            ),
            FakeResponse(200, {"document": {"id": "doc9"}}),
        ]
    )
    assert client.upload(source) == "doc9"

    url, headers, body = put_calls[0]
    assert url == "https://upload.example/x"
    assert headers["Content-Length"] == "5"
    assert body == b"hello"
    # 直传地址不能带 API Key
    assert "X-API-Key" not in headers
    assert session.calls[0][1].endswith("/upload/presign")
    assert session.calls[1][1].endswith("/upload/finalize")
    assert session.calls[1][2]["json"] == {"finalize_token": "tok"}


def test_translate_file_downloads_with_server_filename(monkeypatch, tmp_path):
    source = tmp_path / "in.docx"
    source.write_bytes(b"x")
    monkeypatch.setattr(client_module.requests, "put", lambda *a, **k: PutOk())
    client, _ = make_client(
        [
            FakeResponse(200, {"upload_url": "https://u", "upload_headers": {}, "finalize_token": "t"}),
            FakeResponse(200, {"document": {"id": "d1"}}),
            FakeResponse(201, {"id": "j1", "status": "pending"}),
            FakeResponse(200, {"id": "j1", "status": "completed"}),
            FakeResponse(200, [{"id": "a1", "format": "docx"}]),
            FakeResponse(
                200,
                content=b"DATA",
                headers={"Content-Disposition": "attachment; filename*=UTF-8''%E6%96%87%E6%A1%A3.docx"},
            ),
        ]
    )
    files = client.translate_file(source, "en", output_dir=tmp_path / "out", poll_interval=0)
    assert [f.name for f in files] == ["文档.docx"]
    assert files[0].read_bytes() == b"DATA"


def test_download_strips_directory_parts_from_server_filename(tmp_path):
    client, _ = make_client(
        [FakeResponse(200, content=b"Z", headers={"Content-Disposition": 'attachment; filename="../../evil.txt"'})]
    )
    saved = client.download_artifact("a1", tmp_path, fallback_name="a1.txt")
    assert saved.parent == tmp_path
    assert saved.name == "evil.txt"


def test_translate_file_raises_when_job_failed(monkeypatch, tmp_path):
    source = tmp_path / "in.pdf"
    source.write_bytes(b"x")
    monkeypatch.setattr(client_module.requests, "put", lambda *a, **k: PutOk())
    client, _ = make_client(
        [
            FakeResponse(200, {"upload_url": "https://u", "upload_headers": {}, "finalize_token": "t"}),
            FakeResponse(200, {"document": {"id": "d2"}}),
            FakeResponse(201, {"id": "j2", "status": "pending"}),
            FakeResponse(
                200,
                {"id": "j2", "status": "failed", "quota_exceeded": True, "error_msg": "余额不足"},
            ),
        ]
    )
    with pytest.raises(JobFailedError) as info:
        client.translate_file(source, "en", output_dir=tmp_path, poll_interval=0)
    assert info.value.quota_exceeded is True


def _sign(payload: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def test_verify_webhook_accepts_matching_signature():
    body = b'{"event":"job.completed","timestamp":1000,"data":{}}'
    assert verify_webhook(body, _sign(body, "s3cret"), "s3cret")


def test_verify_webhook_rejects_tampered_body():
    body = b'{"x":1}'
    assert not verify_webhook(b'{"x":2}', _sign(body, "s3cret"), "s3cret")


def test_parse_webhook_returns_event_within_tolerance():
    body = json.dumps(
        {"event": "job.completed", "timestamp": 1000, "data": {"job_id": "j", "status": "completed"}}
    ).encode()
    event = parse_webhook(body, _sign(body, "k"), "k", now=1500)
    assert event["data"]["job_id"] == "j"


def test_parse_webhook_rejects_stale_event():
    body = json.dumps({"event": "job.completed", "timestamp": 1000, "data": {}}).encode()
    with pytest.raises(ValueError, match="stale"):
        parse_webhook(body, _sign(body, "k"), "k", now=1000 + 13 * 3600)

import os

import pytest

from testmu_selenium import downloads_path
from testmu_selenium._downloads import download_uploaded_files


class _Response:
    def __init__(self, body=b"", payload=None, status=200):
        self._body = body
        self._payload = payload
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload

    def iter_content(self, _size):
        yield self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass


class _Calls(list):
    resolve_status = 200


@pytest.fixture
def fake_requests(monkeypatch):
    calls = _Calls()

    def _get(url, params=None, headers=None, **_kw):
        calls.append((url, params, headers))
        if url.endswith("/api/v1/files/resolve"):
            return _Response(payload={"media_url": "cdn.example/media/CUR-resume.pdf", "media_id": "CUR",
                                      "file_name": "resolved.txt"}, status=calls.resolve_status)
        return _Response(body=b"bytes")

    import testmu_selenium._downloads as downloads
    monkeypatch.setattr(downloads.requests, "get", _get)
    return calls


def test_downloads_path_honors_env(monkeypatch, tmp_path):
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))
    assert downloads_path("a.txt") == os.path.join(str(tmp_path), "a.txt")
    monkeypatch.delenv("TESTMU_DOWNLOAD_PATH")
    assert downloads_path("a.txt") == os.path.join(os.path.expanduser("~"), "Downloads", "a.txt")


def test_file_entry_resolves_through_test_manager_by_alias(fake_requests, monkeypatch, tmp_path):
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("ATMS_URL", "https://tms.example")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))

    download_uploaded_files([
        {"alias": "resume", "name": "resume.pdf", "media_url": "cdn.example/media/OLD-resume.pdf"},
        {"alias": "notes"},
    ])

    assert fake_requests[0][0] == "https://tms.example/api/v1/files/resolve"
    assert fake_requests[0][1] == {"alias": "resume"}
    assert fake_requests[0][2]["Authorization"].startswith("Basic ")
    assert fake_requests[1][0] == "https://cdn.example/media/CUR-resume.pdf"
    assert fake_requests[1][2]["Authorization"].startswith("Basic ")
    assert (tmp_path / "resume.pdf").read_bytes() == b"bytes"
    assert (tmp_path / "resolved.txt").read_bytes() == b"bytes"


def test_local_alias_is_not_resolved(fake_requests, monkeypatch, tmp_path):
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("ATMS_URL", "https://tms.example")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))

    download_uploaded_files([{"alias": "local.resume", "name": "resume.pdf", "media_url": "cdn.example/media/OLD-resume.pdf"}])

    assert [c[0] for c in fake_requests] == ["https://cdn.example/media/OLD-resume.pdf"]


def test_failed_resolve_falls_back_to_the_stored_media_url(fake_requests, monkeypatch, tmp_path):
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))
    fake_requests.resolve_status = 403

    download_uploaded_files([{"alias": "resume", "name": "resume.pdf", "media_url": "cdn.example/media/OLD-resume.pdf"}])

    assert fake_requests[1][0] == "https://cdn.example/media/OLD-resume.pdf"
    assert (tmp_path / "resume.pdf").read_bytes() == b"bytes"


def test_file_is_always_fetched_fresh(fake_requests, monkeypatch, tmp_path):
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))
    (tmp_path / "resume.pdf").write_bytes(b"stale")

    download_uploaded_files([{"alias": "resume", "name": "resume.pdf"}])

    assert (tmp_path / "resume.pdf").read_bytes() == b"bytes"
    assert len(fake_requests) == 2


def test_media_url_entry_downloads_directly(fake_requests, monkeypatch, tmp_path):
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))

    download_uploaded_files([{"media_url": "cdn.example/a.txt", "name": "a.txt"}])

    assert fake_requests[0][0] == "https://cdn.example/a.txt"
    assert fake_requests[0][2]["Authorization"].startswith("Basic ")
    assert (tmp_path / "a.txt").exists()


def test_without_credentials_nothing_happens(fake_requests, monkeypatch, tmp_path):
    monkeypatch.delenv("LT_USERNAME", raising=False)
    monkeypatch.delenv("LT_ACCESS_KEY", raising=False)
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))

    download_uploaded_files([{"alias": "resume", "name": "resume.pdf"}])

    assert fake_requests == []
    assert not (tmp_path / "resume.pdf").exists()


@pytest.fixture
def clean_vars():
    from testmu_selenium import _vars
    from testmu_selenium._step_variables import pop_step_variables
    _vars.clear_state()
    pop_step_variables()
    yield _vars
    _vars.clear_state()
    pop_step_variables()


def test_aliased_download_registers_file_variable(fake_requests, clean_vars, monkeypatch, tmp_path):
    from testmu_selenium import var
    from testmu_selenium._step_variables import pop_step_variables
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path))

    download_uploaded_files([
        {"name": "resume.pdf", "alias": "cv"},
        {"name": "My Photo (1).PNG", "alias": "local.photo", "media_url": "cdn.example/photo.png"},
        {"media_url": "cdn.example/a.txt", "name": "a.txt"},
    ])

    store = clean_vars._variable_store
    assert store == {
        "file.cv": str(tmp_path / "resume.pdf"),
        "file.local.photo": str(tmp_path / "My Photo (1).PNG"),
    }
    assert pop_step_variables() == {}
    assert var("{{file.cv}}") == str(tmp_path / "resume.pdf")


def test_failed_download_does_not_register(fake_requests, clean_vars, monkeypatch, tmp_path):
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("TESTMU_DOWNLOAD_PATH", str(tmp_path / "missing" / "x"))
    import testmu_selenium._downloads as downloads

    def _boom(*_a, **_kw):
        raise RuntimeError("down")
    monkeypatch.setattr(downloads.requests, "get", _boom)

    download_uploaded_files([{"name": "resume.pdf", "alias": "cv"}])

    assert clean_vars._variable_store == {}

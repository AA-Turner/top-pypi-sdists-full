import pytest
from mistralai.client import httpclient

from mistralai.workflows import _mistral_http
from mistralai.workflows._mistral_http import MISTRAL_HTTP


def test_backend_matches_the_module_the_mistralai_client_is_built_on() -> None:
    # The generated httpclient is read here only to catch drift: the backend itself is selected
    # from the mistralai version, not from this implementation alias.
    assert MISTRAL_HTTP is httpclient.httpx


@pytest.mark.parametrize(
    ("mistralai_version", "expected"),
    [("2.10.1", "httpx"), ("3.0.0", "httpx2"), ("3.4.0rc1", "httpx2")],
)
def test_backend_is_selected_from_the_mistralai_major(
    monkeypatch: pytest.MonkeyPatch, mistralai_version: str, expected: str
) -> None:
    imported: list[str] = []
    monkeypatch.setattr(_mistral_http, "version", lambda _: mistralai_version)
    monkeypatch.setattr(_mistral_http, "import_module", imported.append)

    _mistral_http._select_backend()

    assert imported == [expected]


def test_unsupported_mistralai_major_fails_at_import(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_mistral_http, "version", lambda _: "4.0.0")

    with pytest.raises(ImportError, match="does not support mistralai 4.0.0"):
        _mistral_http._select_backend()

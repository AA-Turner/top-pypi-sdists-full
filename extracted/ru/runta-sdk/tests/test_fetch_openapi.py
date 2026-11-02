from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import urllib.request
from unittest.mock import Mock

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fetch-runta-openapi.py"
spec = importlib.util.spec_from_file_location("fetch_runta_openapi", SCRIPT)
fetch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)


def test_fetches_current_public_contract_from_authenticated_contents_api(monkeypatch):
    request = Mock(return_value=b"openapi: 3.1.0\n")
    monkeypatch.setattr(fetch, "request_bytes", request)
    assert (
        fetch.fetch_contract(
            repo="runta-dev/runta",
            branch="integration",
            path="openapi/public.yaml",
            token="test-token",
        )
        == b"openapi: 3.1.0\n"
    )
    request.assert_called_once_with(
        "https://api.github.com/repos/runta-dev/runta/contents/openapi/public.yaml?ref=integration",
        token="test-token",
        accept="application/vnd.github.raw+json",
    )


def test_contents_url_encodes_custom_branch_and_path(monkeypatch):
    request = Mock(return_value=b"contract")
    monkeypatch.setattr(fetch, "request_bytes", request)
    fetch.fetch_contract(
        repo="org/repo",
        branch="feature/contracts",
        path="spec/public api.yaml",
        token=None,
    )
    assert request.call_args.args[0].endswith(
        "/spec/public%20api.yaml?ref=feature%2Fcontracts"
    )


def arguments(tmp_path, *, strict):
    return SimpleNamespace(
        repo="org/repo",
        branch="dev",
        path="openapi/public.yaml",
        raw_url=None,
        output=tmp_path / "contract.yaml",
        no_fallback=strict,
    )


def test_strict_fetch_failure_does_not_accept_existing_or_fallback_contract(
    tmp_path, monkeypatch
):
    args = arguments(tmp_path, strict=True)
    args.output.write_bytes(b"stale contract")
    monkeypatch.setattr(fetch, "parse_args", lambda: args)
    monkeypatch.setattr(
        fetch,
        "fetch_contract",
        Mock(side_effect=fetch.FetchError("source unavailable")),
    )
    fallback = Mock()
    monkeypatch.setattr(fetch, "request_bytes", fallback)
    assert fetch.main() == 1
    assert args.output.read_bytes() == b"stale contract"
    fallback.assert_not_called()


def test_successful_strict_fetch_replaces_committed_copy(tmp_path, monkeypatch):
    args = arguments(tmp_path, strict=True)
    monkeypatch.setattr(fetch, "parse_args", lambda: args)
    monkeypatch.setattr(fetch, "fetch_contract", Mock(return_value=b"source contract"))
    assert fetch.main() == 0
    assert args.output.read_bytes() == b"source contract"


def test_optional_raw_fallback_uses_configured_source_path(tmp_path, monkeypatch):
    args = arguments(tmp_path, strict=False)
    monkeypatch.setattr(fetch, "parse_args", lambda: args)
    monkeypatch.setattr(
        fetch, "fetch_contract", Mock(side_effect=fetch.FetchError("offline"))
    )
    fallback = Mock(return_value=b"raw contract")
    monkeypatch.setattr(fetch, "request_bytes", fallback)
    assert fetch.main() == 0
    fallback.assert_called_once_with(
        "https://raw.githubusercontent.com/org/repo/dev/openapi/public.yaml", token=None
    )
    assert args.output.read_bytes() == b"raw contract"


@pytest.mark.parametrize("cross_host", [False, True])
def test_redirect_only_forwards_auth_to_same_host(cross_host):
    request = urllib.request.Request("https://api.github.com/source")
    request.add_header("Authorization", "Bearer test-token")
    target = (
        "https://blob.example.test/file"
        if cross_host
        else "https://api.github.com/next"
    )
    redirected = fetch._NoAuthCrossHostRedirect().redirect_request(
        request, None, 302, "", {}, target
    )
    assert redirected.get_header("Authorization") == (
        None if cross_host else "Bearer test-token"
    )

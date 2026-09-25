"""The stdio child environment must not inherit the AI client's full environment."""

import os

import pytest

from runlayer_cli.main import _build_stdio_env


@pytest.fixture
def parent_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-secret")
    monkeypatch.setenv("GITHUB_TOKEN", "gh-token")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.corp:3128")
    monkeypatch.setenv("no_proxy", "localhost")
    monkeypatch.setenv("SSL_CERT_FILE", "/etc/ssl/corp.pem")
    monkeypatch.setenv("NODE_EXTRA_CA_CERTS", "/etc/ssl/corp-node.pem")
    monkeypatch.setenv("LANG", "en_US.UTF-8")
    monkeypatch.setenv("PATH", "/usr/bin")
    for key in (
        "REQUESTS_CA_BUNDLE",
        "CURL_CA_BUNDLE",
        "SSL_CERT_DIR",
        "TMPDIR",
        "LC_ALL",
        "HTTP_PROXY",
        "NO_PROXY",
    ):
        monkeypatch.delenv(key, raising=False)
    for key in ("http_proxy", "https_proxy"):
        monkeypatch.delenv(key, raising=False)


@pytest.mark.usefixtures("parent_env")
def test_parent_secrets_not_inherited() -> None:
    env = _build_stdio_env({})

    assert "AWS_SECRET_ACCESS_KEY" not in env
    assert "GITHUB_TOKEN" not in env
    # mcp's stdio_client layers PATH/HOME/... underneath; we don't copy them.
    assert "PATH" not in env


@pytest.mark.usefixtures("parent_env")
def test_proxy_tls_locale_vars_inherited_when_set() -> None:
    env = _build_stdio_env({})

    assert env["HTTPS_PROXY"] == "http://proxy.corp:3128"
    assert env["no_proxy"] == "localhost"
    assert env["SSL_CERT_FILE"] == "/etc/ssl/corp.pem"
    # Node ignores SSL_CERT_FILE; npx servers behind TLS inspection need this.
    assert env["NODE_EXTRA_CA_CERTS"] == "/etc/ssl/corp-node.pem"
    assert env["LANG"] == "en_US.UTF-8"
    assert "REQUESTS_CA_BUNDLE" not in env


@pytest.mark.usefixtures("parent_env")
def test_configured_env_wins_over_inherited() -> None:
    env = _build_stdio_env(
        {"env": {"HTTPS_PROXY": "http://other:8080", "API_TOKEN": "configured"}}
    )

    assert env["HTTPS_PROXY"] == "http://other:8080"
    assert env["API_TOKEN"] == "configured"


@pytest.mark.usefixtures("parent_env")
def test_non_string_config_entries_ignored() -> None:
    env = _build_stdio_env({"env": {"PORT": 8080, 1: "x", "OK": "yes"}})

    assert env == {
        "HTTPS_PROXY": "http://proxy.corp:3128",
        "no_proxy": "localhost",
        "SSL_CERT_FILE": "/etc/ssl/corp.pem",
        "NODE_EXTRA_CA_CERTS": "/etc/ssl/corp-node.pem",
        "LANG": "en_US.UTF-8",
        "OK": "yes",
    }


def test_windows_folds_env_key_case(monkeypatch: pytest.MonkeyPatch) -> None:
    """On Windows ``os.environ`` answers both casings, so without folding the
    child would get ``HTTPS_PROXY`` (parent) beside ``https_proxy`` (configured)
    and the spawn picks one arbitrarily."""
    monkeypatch.setattr(os, "name", "nt")
    monkeypatch.setenv("HTTPS_PROXY", "http://parent:3128")
    monkeypatch.setenv("https_proxy", "http://parent:3128")

    env = _build_stdio_env({"env": {"https_proxy": "http://cfg:8080"}})

    proxy_keys = [key for key in env if key.upper() == "HTTPS_PROXY"]
    assert proxy_keys == ["HTTPS_PROXY"]
    assert env["HTTPS_PROXY"] == "http://cfg:8080"


def test_empty_parent_and_config_returns_dict(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY", "SSL_CERT_FILE", "LANG"):
        monkeypatch.delenv(key, raising=False)
        monkeypatch.delenv(key.lower(), raising=False)
    for key in (
        "LC_ALL",
        "TMPDIR",
        "REQUESTS_CA_BUNDLE",
        "CURL_CA_BUNDLE",
        "SSL_CERT_DIR",
        "NODE_EXTRA_CA_CERTS",
    ):
        monkeypatch.delenv(key, raising=False)

    # A dict (not None) keeps StdioServerParameters.env set, so mcp still merges
    # its platform base set underneath rather than substituting it wholesale.
    assert _build_stdio_env({"env": None}) == {}

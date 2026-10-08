"""Tests for the webapp server entrypoint."""

import os

from airbyte_ops_webapp import serve as serve_module


def test_configure_backend_env_defaults_to_stateless(monkeypatch) -> None:
    monkeypatch.delenv(serve_module.STATELESS_HTTP_ENV_VAR, raising=False)

    serve_module._configure_backend_env()

    assert os.environ[serve_module.STATELESS_HTTP_ENV_VAR] == "true"


def test_configure_backend_env_preserves_explicit_false(monkeypatch) -> None:
    monkeypatch.setenv(serve_module.STATELESS_HTTP_ENV_VAR, "false")

    serve_module._configure_backend_env()

    assert os.environ[serve_module.STATELESS_HTTP_ENV_VAR] == "false"

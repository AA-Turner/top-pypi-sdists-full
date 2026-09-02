"""Tests for brokered secret injection during sandbox creation."""

import asyncio
import inspect

import pytest

from novita_sandbox import AsyncSandbox, Sandbox
from novita_sandbox.core.exceptions import InvalidArgumentException
from novita_sandbox.core.sandbox_async.sandbox_api import SandboxApi as AsyncSandboxApi
from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi as SyncSandboxApi


def test_create_accepts_secrets_for_brokered_secret_injection():
    assert "secret_envs" in inspect.signature(Sandbox.create).parameters
    assert "secret_envs" in inspect.signature(AsyncSandbox.create).parameters


def test_create_sandbox_request_includes_secrets(monkeypatch):
    captured = {}

    class StopAfterCapture(Exception):
        pass

    def fake_sync_detailed(*, body, client):
        captured["body"] = body.to_dict()
        raise StopAfterCapture()

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: object(),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.post_sandboxes.sync_detailed",
        fake_sync_detailed,
    )

    with pytest.raises(StopAfterCapture):
        SyncSandboxApi._create_sandbox(
            template="agent-template",
            timeout=60,
            auto_pause=False,
            allow_internet_access=True,
            metadata={},
            env_vars={},
            secure=True,
            secret_envs={"OPENAI_API_KEY": "openai-prod"},
            api_key="nvta_test",
            api_url="http://localhost:3000",
        )

    assert captured["body"]["secrets"] == {"OPENAI_API_KEY": "openai-prod"}


def test_create_sandbox_rejects_invalid_secret_env_name(monkeypatch):
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: object(),
    )

    with pytest.raises(InvalidArgumentException):
        SyncSandboxApi._create_sandbox(
            template="agent-template",
            timeout=60,
            auto_pause=False,
            allow_internet_access=True,
            metadata={},
            env_vars={},
            secure=True,
            secret_envs={"openai-prod": "openai-prod"},
            api_key="nvta_test",
            api_url="http://localhost:3000",
        )


def test_create_sandbox_rejects_non_mapping_secret_envs(monkeypatch):
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: object(),
    )

    with pytest.raises(InvalidArgumentException):
        SyncSandboxApi._create_sandbox(
            template="agent-template",
            timeout=60,
            auto_pause=False,
            allow_internet_access=True,
            metadata={},
            env_vars={},
            secure=True,
            secret_envs=[],
            api_key="nvta_test",
            api_url="http://localhost:3000",
        )


def test_create_sandbox_rejects_invalid_secret_name(monkeypatch):
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: object(),
    )

    with pytest.raises(InvalidArgumentException):
        SyncSandboxApi._create_sandbox(
            template="agent-template",
            timeout=60,
            auto_pause=False,
            allow_internet_access=True,
            metadata={},
            env_vars={},
            secure=True,
            secret_envs={"OPENAI_API_KEY": "openai/prod"},
            api_key="nvta_test",
            api_url="http://localhost:3000",
        )


def test_create_sandbox_rejects_env_and_secret_env_collision(monkeypatch):
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: object(),
    )

    with pytest.raises(InvalidArgumentException):
        SyncSandboxApi._create_sandbox(
            template="agent-template",
            timeout=60,
            auto_pause=False,
            allow_internet_access=True,
            metadata={},
            env_vars={"OPENAI_API_KEY": "plain-value"},
            secure=True,
            secret_envs={"OPENAI_API_KEY": "openai-prod"},
            api_key="nvta_test",
            api_url="http://localhost:3000",
        )


def test_async_create_sandbox_request_includes_validated_secrets(monkeypatch):
    captured = {}

    class StopAfterCapture(Exception):
        pass

    async def fake_asyncio_detailed(*, body, client):
        captured["body"] = body.to_dict()
        raise StopAfterCapture()

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        lambda config: object(),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.post_sandboxes.asyncio_detailed",
        fake_asyncio_detailed,
    )

    async def run():
        await AsyncSandboxApi._create_sandbox(
            template="agent-template",
            timeout=60,
            auto_pause=False,
            allow_internet_access=True,
            metadata={},
            env_vars={},
            secure=True,
            secret_envs={"OPENAI_API_KEY": "openai-prod"},
            api_key="nvta_test",
            api_url="http://localhost:3000",
        )

    with pytest.raises(StopAfterCapture):
        asyncio.run(run())

    assert captured["body"]["secrets"] == {"OPENAI_API_KEY": "openai-prod"}

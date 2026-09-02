import httpx
import pytest

from novita_sandbox.core import NotFoundException, TimeoutException
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.sandbox_sync.main import Sandbox
from novita_sandbox.core.sandbox_async.main import AsyncSandbox


def test_sandbox_is_running_propagates_connect_error():
    class EnvdApi:
        @staticmethod
        def get(*args, **kwargs):
            raise httpx.ConnectError("connection closed")

    sandbox = object.__new__(Sandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    with pytest.raises(httpx.ConnectError):
        sandbox.is_running()


def test_sandbox_is_running_rethrows_timeout_error():
    class EnvdApi:
        @staticmethod
        def get(*args, **kwargs):
            raise httpx.TimeoutException("timed out")

    sandbox = object.__new__(Sandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    with pytest.raises(TimeoutException):
        sandbox.is_running()


def test_sandbox_is_running_returns_true_on_200():
    class EnvdApi:
        @staticmethod
        def get(*args, **kwargs):
            return httpx.Response(200)

    sandbox = object.__new__(Sandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    assert sandbox.is_running() is True


def test_sandbox_is_running_returns_false_on_502():
    class EnvdApi:
        @staticmethod
        def get(*args, **kwargs):
            return httpx.Response(502)

    sandbox = object.__new__(Sandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    assert sandbox.is_running() is False


def test_sandbox_is_running_raises_on_other_status():
    class EnvdApi:
        @staticmethod
        def get(*args, **kwargs):
            return httpx.Response(404, json={"message": "not found"})

    sandbox = object.__new__(Sandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    with pytest.raises(NotFoundException):
        sandbox.is_running()


@pytest.mark.asyncio
async def test_async_sandbox_is_running_propagates_connect_error():
    class EnvdApi:
        @staticmethod
        async def get(*args, **kwargs):
            raise httpx.ConnectError("connection closed")

    sandbox = object.__new__(AsyncSandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    with pytest.raises(httpx.ConnectError):
        await sandbox.is_running()


@pytest.mark.asyncio
async def test_async_sandbox_is_running_rethrows_timeout_error():
    class EnvdApi:
        @staticmethod
        async def get(*args, **kwargs):
            raise httpx.TimeoutException("timed out")

    sandbox = object.__new__(AsyncSandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    with pytest.raises(TimeoutException):
        await sandbox.is_running()


@pytest.mark.asyncio
async def test_async_sandbox_is_running_returns_true_on_200():
    class EnvdApi:
        @staticmethod
        async def get(*args, **kwargs):
            return httpx.Response(200)

    sandbox = object.__new__(AsyncSandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    assert await sandbox.is_running() is True


@pytest.mark.asyncio
async def test_async_sandbox_is_running_returns_false_on_502():
    class EnvdApi:
        @staticmethod
        async def get(*args, **kwargs):
            return httpx.Response(502)

    sandbox = object.__new__(AsyncSandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    assert await sandbox.is_running() is False


@pytest.mark.asyncio
async def test_async_sandbox_is_running_raises_on_other_status():
    class EnvdApi:
        @staticmethod
        async def get(*args, **kwargs):
            return httpx.Response(404, json={"message": "not found"})

    sandbox = object.__new__(AsyncSandbox)
    sandbox._envd_api = EnvdApi()
    sandbox._SandboxBase__connection_config = ConnectionConfig()

    with pytest.raises(NotFoundException):
        await sandbox.is_running()

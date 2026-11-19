"""Client.get_zax_client against a fake zax_client module, which CI cannot install (TEMPORARY(zax-private))."""

import json
import sys
import time
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from arraylake import Client, config
from arraylake.compute.types import ServiceType
from arraylake.token import TokenHandler

from . import fake_jwt


class FakeZaxClient:
    def __init__(self, address: str, *, tls: bool = False, token: Any = None) -> None:
        self.address, self.tls, self.token = address, tls, token


def deployment(name: str | None, service_type: ServiceType = ServiceType.zax) -> SimpleNamespace:
    url = f"https://zax-{name or 'default'}.compute.earthmover.io/v1/services/{name or 'zax'}/my-org"
    return SimpleNamespace(url=url, config=SimpleNamespace(service_type=service_type, deployment_name=name))


@pytest.fixture
def connect(monkeypatch):
    """Call get_zax_client against fake zax deployments, with no network access."""
    module = ModuleType("zax_client")
    module.Client = FakeZaxClient  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "zax_client", module)

    def _connect(deployments=(deployment(None),), deployment_name=None, **client_kwargs):
        services = MagicMock()
        services.list_enabled.return_value = list(deployments)
        client = Client("https://foo.com", **client_kwargs)
        with patch.object(Client, "get_services", return_value=services):
            return client.get_zax_client("my-org", deployment_name)

    with config.set({"token": None}):
        yield _connect


def _set_cached_id_token(token_file, id_token):
    data = json.loads(token_file.read_text())
    data["id_token"] = id_token
    token_file.write_text(json.dumps(data))


def test_api_token_is_used_as_is(connect, test_token):
    zc = connect(token=test_token)
    assert (zc.address, zc.tls, zc.token) == ("zax-default.compute.earthmover.io:32010", True, test_token)


def test_cached_login_is_refreshed_per_call(connect, test_token_file, monkeypatch):
    tokens = iter([fake_jwt(time.time() + 7200)])
    refreshes = []

    async def refresh_quietly(self):
        refreshes.append(1)
        self.update({"id_token": next(tokens)})

    monkeypatch.setattr(TokenHandler, "refresh_quietly", refresh_quietly)
    _set_cached_id_token(test_token_file, fake_jwt(time.time() - 10))  # already expired
    zc = connect()

    assert zc.token() == json.loads(test_token_file.read_text())["id_token"]
    assert len(refreshes) == 1
    # A login renewed elsewhere (or a later refresh) is picked up by the same client.
    renewed = fake_jwt(time.time() + 9000)
    _set_cached_id_token(test_token_file, renewed)
    assert zc.token() == renewed


def test_requires_token_or_login(connect, test_token_file):
    test_token_file.unlink()
    with pytest.raises(ValueError, match="al auth login"):
        connect()


def test_selects_a_deployment_by_name(connect, test_token):
    zc = connect(deployments=[deployment("a"), deployment("b"), deployment("sql", ServiceType.sql)], deployment_name="b", token=test_token)
    assert zc.address == "zax-b.compute.earthmover.io:32010"


@pytest.mark.parametrize(
    ("deployments", "deployment_name", "message"),
    [
        ([deployment("a")], "b", "no zax service named 'b'"),
        ([deployment("sql", ServiceType.sql)], None, "has no zax service. Enable one"),
    ],
)
def test_a_missing_service_is_an_error(connect, test_token, deployments, deployment_name, message):
    with pytest.raises(ValueError, match=message):
        connect(deployments=deployments, deployment_name=deployment_name, token=test_token)


def test_missing_zax_client_names_the_package(monkeypatch, test_token):
    monkeypatch.setitem(sys.modules, "zax_client", None)
    with pytest.raises(ImportError, match="zax-client"):
        Client("https://foo.com", token=test_token).get_zax_client("my-org")

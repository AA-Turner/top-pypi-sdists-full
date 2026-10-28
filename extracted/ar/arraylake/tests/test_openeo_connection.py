import json
import logging
import time
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from arraylake import Client, config
from arraylake.compute.types import ServiceType
from arraylake.token import TokenHandler

from . import fake_jwt

openeo = pytest.importorskip("openeo")

SERVICE_URL = "https://compute.earthmover.io/my-org/openeo"


@pytest.fixture
def connect(monkeypatch):
    """Call get_openeo_connection against one fake openEO deployment, with no network access."""
    # Every request (version discovery, capabilities, ...) gets this capabilities document back.
    session = MagicMock()
    session.request.return_value.status_code = 200
    session.request.return_value.json.return_value = {"api_version": "1.2.0", "endpoints": []}
    real_connect = openeo.connect
    monkeypatch.setattr(openeo, "connect", lambda url: real_connect(url, session=session))

    deployment = SimpleNamespace(url=SERVICE_URL, config=SimpleNamespace(service_type=ServiceType.openeo, deployment_name=None))
    services = MagicMock()
    services.list_enabled.return_value = [deployment]

    def _connect(**client_kwargs):
        client = Client("https://foo.com", **client_kwargs)
        with patch.object(Client, "get_services", return_value=services):
            return client.get_openeo_connection("my-org")

    with config.set({"token": None}):
        yield _connect


def _set_cached_id_token(token_file, id_token):
    data = json.loads(token_file.read_text())
    data["id_token"] = id_token
    token_file.write_text(json.dumps(data))


def _sent_auth(connection, url):
    """The auth object openeo attaches to a request for ``url``."""
    connection.get(url)
    return connection.session.request.call_args.kwargs["auth"]


def _authorization(auth):
    prepared = MagicMock(headers={})
    return auth(prepared).headers["Authorization"]


def test_cached_login_is_refreshed_per_request(connect, test_token_file, monkeypatch):
    tokens = iter([fake_jwt(time.time() + 7200), fake_jwt(time.time() + 7200)])
    refreshes = []

    async def refresh_quietly(self):
        refreshes.append(1)
        self.update({"id_token": next(tokens)})

    monkeypatch.setattr(TokenHandler, "refresh_quietly", refresh_quietly)
    _set_cached_id_token(test_token_file, fake_jwt(time.time() - 10))  # already expired
    connection = connect()

    auth = _sent_auth(connection, "/jobs")
    first = _authorization(auth)
    assert len(refreshes) == 1
    assert first == f"Bearer {json.loads(test_token_file.read_text())['id_token']}"

    # A login renewed elsewhere (or a later refresh) is picked up by the same connection.
    renewed = fake_jwt(time.time() + 9000)
    _set_cached_id_token(test_token_file, renewed)
    assert _authorization(auth) == f"Bearer {renewed}"
    assert auth.bearer == renewed  # openeo's job manager reads `.bearer`


def test_api_token_is_used_as_is(connect, test_token):
    connection = connect(token=test_token)
    assert _authorization(_sent_auth(connection, "/jobs")) == f"Bearer {test_token}"


def test_requires_token_or_login(connect, test_token_file):
    test_token_file.unlink()
    with pytest.raises(ValueError, match="al auth login"):
        connect()


def test_result_asset_downloads_are_unauthenticated(connect, test_token):
    # Presigned asset URLs reject extra auth; openeo only sends the connection's auth to its own root URL.
    connection = connect(token=test_token)
    assert _sent_auth(connection, "https://bucket.s3.amazonaws.com/results/out.nc?X-Amz-Signature=abc") is None


def test_unknown_other_dimension_warning_is_silenced(connect, test_token, caplog):
    connect(token=test_token)
    connect(token=test_token)
    metadata_logger = logging.getLogger("openeo.metadata")
    assert len([f for f in metadata_logger.filters if type(f).__name__ == "_UnknownOtherDimensionFilter"]) == 1

    with caplog.at_level(logging.WARNING, logger="openeo.metadata"):
        metadata_logger.warning("Unknown dimension type %r", "other")
        metadata_logger.warning("Unknown dimension type %r", "weird")
    assert [r.getMessage() for r in caplog.records] == ["Unknown dimension type 'weird'"]

"""Anonymous reads of PUBLIC repos, against a mocked server: the compose API fakes a user on every request."""

import json
import pickle
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
import respx

from arraylake import AsyncClient, Client, config
from arraylake import client as client_module
from arraylake.exceptions import AuthException
from arraylake.types import OpenRepoResponse

URL = "https://example.test"
OPEN_URL = f"{URL}/repos/my-org/my-repo/open"
ANONYMOUS_PRINCIPAL_ID = "00000000-0000-4000-8000-0000a0a0a0a0"


def _bucket(platform: str) -> dict[str, Any]:
    bucket: dict[str, Any] = {
        "id": "8a8d2d3c-5f8b-4c3e-9a63-0c1f1f3d6e10",
        "nickname": "public-data",
        "name": "public-data",
        "prefix": "",
        "created": "2026-10-01T00:00:00Z",
        "updated": "2026-10-01T00:00:00Z",
        "created_by": None,
        "is_default": False,
        "health": None,
    }
    if platform == "r2":
        bucket |= {
            "platform": "s3-compatible",
            "extra_config": {"endpoint_url": "https://acct.r2.cloudflarestorage.com", "region_name": "auto"},
            "auth_config": {
                "method": "r2_customer_managed_role",
                "external_account_id": "redacted",
                "parent_access_key_id": "redacted",
                "parent_secret_access_key": "redacted",
                "duration_seconds": 3600,
            },
        }
    elif platform == "s3":
        bucket |= {
            "platform": "s3",
            "extra_config": {"region_name": "us-east-1"},
            "auth_config": {"method": "aws_customer_managed_role", "external_customer_id": "redacted", "external_role_name": "redacted"},
        }
    else:
        bucket |= {
            "platform": "gs",
            "extra_config": {},
            "auth_config": {"method": "gcp_customer_managed_role", "target_service_account": "redacted"},
        }
    return bucket


def _credentials(platform: str, key: str) -> dict[str, Any]:
    expiration = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
    if platform == "gs":
        return {"access_token": key, "principal": "redacted", "expiration": expiration}
    return {"aws_access_key_id": key, "aws_secret_access_key": "secret", "aws_session_token": "session", "expiration": expiration}


def _open_body(platform: str = "s3", key: str = "ANONKEY") -> dict[str, Any]:
    """The shape the server sends an anonymous caller: redacted, no VCCs, the shared anonymous identity."""
    return {
        "repo_bucket": _bucket(platform),
        "repo_prefix": "public/my-repo",
        "repo_credentials": _credentials(platform, key),
        "virtual_chunk_credentials": {},
        "author": {"name": "Anonymous", "email": "anonymous@earthmover.io"},
        "principal_id": ANONYMOUS_PRINCIPAL_ID,
        "status": {"mode": "online", "message": None, "initiated_by": {}},
    }


@pytest.fixture
def server(respx_mock: respx.MockRouter) -> respx.MockRouter:
    respx_mock.post(f"{URL}/user/diagnostics").respond(200, json={})
    return respx_mock


@pytest.fixture
def logged_out(test_token_file: Path) -> Path:
    test_token_file.unlink()
    return test_token_file


def _log_in(token_file: Path) -> None:
    token_file.write_text(
        json.dumps({"access_token": "a", "id_token": "id-456", "refresh_token": "r", "expires_in": 86400, "token_type": "Bearer"})
    )


@pytest.mark.parametrize("platform", ["s3", "r2", "gs"])
async def test_anonymous_open_sends_no_authorization(server: respx.MockRouter, logged_out: Path, platform: str) -> None:
    route = server.get(OPEN_URL).respond(200, json=_open_body(platform))
    client = AsyncClient(URL)

    assert client._is_anonymous()
    mstore_config, _, response = await client._open_repo_response("my-org/my-repo")

    assert mstore_config.anonymous

    assert "Authorization" not in route.calls.last.request.headers
    assert isinstance(response, OpenRepoResponse)
    assert response.virtual_chunk_credentials == {}
    assert str(response.author.email) == "anonymous@earthmover.io"


async def test_anonymous_repo_object_sends_no_authorization(server: respx.MockRouter, logged_out: Path) -> None:
    route = server.get(f"{URL}/repos/my-org/my-repo").respond(404, json={"detail": "Repo my-org/my-repo not found"})

    with pytest.raises(AuthException, match="not found or not public"):
        await AsyncClient(URL).get_repo_object("my-org/my-repo")
    assert "Authorization" not in route.calls.last.request.headers


@pytest.mark.parametrize("status_code", [401, 404])
async def test_anonymous_open_of_a_hidden_repo_says_not_public(server: respx.MockRouter, logged_out: Path, status_code: int) -> None:
    server.get(OPEN_URL).respond(status_code, json={"detail": "Repo my-org/my-repo not found"})

    with pytest.raises(AuthException) as exc_info:
        await AsyncClient(URL)._open_repo_response("my-org/my-repo")
    assert str(exc_info.value) == "Repo my-org/my-repo not found or not public. Run arraylake auth login to open private repos."


@pytest.mark.parametrize("anonymous", [True, False], ids=["anonymous", "no-login"])
async def test_other_calls_still_need_a_login(server: respx.MockRouter, logged_out: Path, anonymous: bool) -> None:
    client = AsyncClient(URL)
    mstore = client._metastore(client._metastore_config("my-org", anonymous=anonymous))

    with pytest.raises(AuthException, match="Not logged in"):
        await mstore.list_databases()
    assert not server.calls


def test_malformed_token_file_is_not_anonymous(test_token_file: Path) -> None:
    test_token_file.write_text("not json")
    assert not AsyncClient(URL)._is_anonymous()


@pytest.mark.parametrize("opened_anonymously", [True, False], ids=["anonymous", "logged-in"])
def test_refresh_keeps_the_open_time_auth_decision(server: respx.MockRouter, logged_out: Path, opened_anonymously: bool) -> None:
    """A worker with no token file must never refresh a logged-in repo anonymously."""
    route = server.get(OPEN_URL).respond(200, json=_open_body())
    client = AsyncClient(URL)
    refresh = client._maybe_get_credential_refresh_func_for_icechunk(
        OpenRepoResponse.model_validate(_open_body()).repo_bucket,
        client._metastore_config("my-org", anonymous=opened_anonymously),
        "my-repo",
    )
    assert refresh is not None

    if opened_anonymously:
        assert refresh().access_key_id == "ANONKEY"
        assert "Authorization" not in route.calls.last.request.headers
    else:
        with pytest.raises(AuthException, match="Not logged in"):
            refresh()
        assert not route.called


async def test_login_after_anonymous_open_does_not_reuse_anonymous_credentials(server: respx.MockRouter, logged_out: Path) -> None:
    route = server.get(OPEN_URL).mock(
        side_effect=[httpx.Response(200, json=_open_body(key="ANONKEY")), httpx.Response(200, json=_open_body(key="USERKEY"))]
    )
    client = AsyncClient(URL)
    await client._open_repo_and_cache(client._read_metastore_config("my-org"), "my-repo")

    _log_in(logged_out)
    with config.set({"token": None}):
        creds = await client._refresh_repo_bucket_credentials(client._read_metastore_config("my-org"), "my-repo", "s3")

    assert route.call_count == 2
    assert route.calls.last.request.headers["Authorization"] == "Bearer id-456"
    assert creds.aws_access_key_id == "USERKEY"  # type: ignore[union-attr]


def test_public_client_get_repo_opens_anonymously_and_its_refresh_survives_pickling(
    server: respx.MockRouter, logged_out: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Dask and Coiled ship the refresh closure to workers that have no token file."""
    expired = _open_body(key="OPENKEY")
    expired["repo_credentials"]["expiration"] = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
    route = server.get(OPEN_URL).mock(
        side_effect=[httpx.Response(200, json=expired), httpx.Response(200, json=_open_body(key="WORKERKEY"))]
    )
    storage_kwargs: dict[str, Any] = {}
    opened = SimpleNamespace(commit_metadata={})
    opened.set_default_commit_metadata = opened.commit_metadata.update

    def capture_storage(**kwargs: Any) -> object:
        storage_kwargs.update(kwargs)
        return object()

    async def open_async(storage: object, **kwargs: Any) -> SimpleNamespace:
        return opened

    monkeypatch.setattr(client_module, "_get_icechunk_storage_obj", capture_storage)
    monkeypatch.setattr(client_module.IcechunkRepository, "open_async", open_async)

    assert Client(URL).get_repo("my-org/my-repo") is opened
    assert opened.commit_metadata["author_email"] == "anonymous@earthmover.io"
    assert "Authorization" not in route.calls.last.request.headers

    refresh = pickle.loads(pickle.dumps(storage_kwargs["credential_refresh_func"]))
    assert refresh().access_key_id == "WORKERKEY"
    assert route.call_count == 2
    assert "Authorization" not in route.calls.last.request.headers

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import httpx
import pytest

from arraylake.metastore import http_metastore
from arraylake.metastore.http_metastore import HttpMetastore, HttpMetastoreConfig, UnsupportedCredentialProviderError
from arraylake.types import KNOWN_CREDENTIAL_PROVIDERS, BucketModifyRequest


class _Captured(Exception):
    """Raised by the stubbed transport once the request body has been recorded, so
    the test never has to synthesize a valid response payload."""


@pytest.fixture
def metastore_capturing_body(monkeypatch):
    sent: dict[str, str] = {}

    async def fake_request(self, method, path, **kwargs):
        sent["method"] = method
        sent["path"] = path
        sent["content"] = kwargs.get("content")
        raise _Captured

    monkeypatch.setattr(HttpMetastore, "_request", fake_request, raising=False)
    return HttpMetastore(HttpMetastoreConfig("http://localhost:8000", "my-org")), sent


async def _body_for_bucket_patch(metastore, sent, request):
    with pytest.raises(_Captured):
        await metastore.modify_bucket_config(uuid4(), request)
    return json.loads(sent["content"])


@pytest.mark.asyncio
async def test_bucket_patch_omits_untouched_fields(metastore_capturing_body):
    metastore, sent = metastore_capturing_body
    body = await _body_for_bucket_patch(metastore, sent, BucketModifyRequest(name="renamed"))

    assert body == {"name": "renamed"}
    assert sent["method"] == "PATCH"


@pytest.mark.asyncio
@pytest.mark.parametrize("field", ["platform", "name", "prefix", "extra_config", "auth_config", "em_managed"])
async def test_bucket_patch_never_sends_a_null_for_an_untouched_field(metastore_capturing_body, field):
    metastore, sent = metastore_capturing_body
    body = await _body_for_bucket_patch(metastore, sent, BucketModifyRequest())

    assert field not in body


@pytest.mark.asyncio
async def test_bucket_patch_keeps_an_omitted_shared_secret_off_the_wire(metastore_capturing_body):
    """AWSRoleAuthPatch tracks the omitted secret via model_fields_set; the outer
    dump must not undo that by expanding it to an explicit null."""
    metastore, sent = metastore_capturing_body
    request = BucketModifyRequest(
        auth_config={
            "method": "aws_customer_managed_role",
            "external_customer_id": "123456789012",
            "external_role_name": "a-new-role",
        },
    )
    body = await _body_for_bucket_patch(metastore, sent, request)

    assert "shared_secret" not in body["auth_config"]
    assert body["auth_config"]["external_role_name"] == "a-new-role"


@pytest.mark.asyncio
async def test_bucket_patch_still_sends_an_explicitly_set_value(metastore_capturing_body):
    metastore, sent = metastore_capturing_body
    body = await _body_for_bucket_patch(metastore, sent, BucketModifyRequest(prefix="", name="renamed"))

    assert body == {"name": "renamed", "prefix": ""}


@pytest.mark.asyncio
async def test_repo_patch_omits_untouched_fields(metastore_capturing_body):
    metastore, sent = metastore_capturing_body
    with pytest.raises(_Captured):
        await metastore.modify_database("my-repo", description="just the description")
    body = json.loads(sent["content"])

    assert body == {"description": "just the description"}
    assert "optimization_config" not in body


@pytest.mark.asyncio
async def test_repo_patch_still_sends_every_supplied_field(metastore_capturing_body):
    metastore, sent = metastore_capturing_body
    with pytest.raises(_Captured):
        await metastore.modify_database("my-repo", description="d", remove_metadata=["stale"])
    body = json.loads(sent["content"])

    assert body == {"description": "d", "remove_metadata": ["stale"]}


FUTURE_CREDENTIALS: dict[str, Any] = json.loads(
    (Path(__file__).parents[2] / "contracts" / "bucket-credentials" / "future-credentials.json").read_text()
)


@pytest.fixture
def metastore_answering(monkeypatch: pytest.MonkeyPatch) -> Callable[[Any], tuple[HttpMetastore, list[tuple[str, dict[str, Any]]]]]:
    def answer(payload: Any) -> tuple[HttpMetastore, list[tuple[str, dict[str, Any]]]]:
        sent: list[tuple[str, dict[str, Any]]] = []

        async def fake_request(self: HttpMetastore, method: str, path: str, **kwargs: Any) -> httpx.Response:
            sent.append((path, kwargs))
            return httpx.Response(200, json=payload, request=httpx.Request(method, "https://api.example.com/x"))

        monkeypatch.setattr(HttpMetastore, "_request", fake_request, raising=False)
        return HttpMetastore(HttpMetastoreConfig("https://api.example.com", "my-org")), sent

    return answer


def _open_payload(repo_credentials: Any, vccs: dict[str, Any]) -> dict[str, Any]:
    return {
        "repo_bucket": {
            "id": str(uuid4()),
            "platform": "s3",
            "nickname": "repo-bucket",
            "name": "repo-bucket",
            "is_default": False,
            "extra_config": {},
        },
        "repo_prefix": "p",
        "repo_credentials": repo_credentials,
        "virtual_chunk_credentials": {
            prefix: {"credentials": creds, "org": "my-org", "bucket_nickname": "vcc-bucket", "platform": "s3"}
            for prefix, creds in vccs.items()
        },
        "author": {"email": "a@example.com"},
        "principal_id": "p",
        "status": {"mode": "online", "initiated_by": {}},
    }


@pytest.mark.asyncio
async def test_open_repo_skips_a_container_with_an_unknown_provider(metastore_answering, monkeypatch):
    known, unknown = FUTURE_CREDENTIALS["new_s3_with_refresh_and_extra_fields"], FUTURE_CREDENTIALS["unknown_provider"]
    metastore, _ = metastore_answering(_open_payload(known, {"s3://known/": known, "future://unknown/": unknown}))
    logger = MagicMock()
    monkeypatch.setattr(http_metastore, "logger", logger)

    response = await metastore.open_repo("repo")

    assert list(response.virtual_chunk_credentials) == ["s3://known/"]
    assert "future://unknown/" in logger.warning.call_args.args[0]


@pytest.mark.asyncio
async def test_open_repo_asks_for_an_upgrade_when_the_repo_provider_is_unknown(metastore_answering):
    metastore, _ = metastore_answering(_open_payload(FUTURE_CREDENTIALS["unknown_provider"], {}))

    with pytest.raises(UnsupportedCredentialProviderError, match="Upgrade arraylake"):
        await metastore.open_repo("repo")


@pytest.mark.asyncio
@pytest.mark.parametrize("case", ["new_s3_with_refresh_and_extra_fields", "old_gcs_without_provider_or_refresh", "new_azure"])
async def test_bucket_credentials_parse_old_and_new_shapes(metastore_answering, case: str):
    metastore, sent = metastore_answering(FUTURE_CREDENTIALS[case])

    creds = await metastore.get_bucket_credentials_from_repo("repo", container="s3://known/")

    assert creds.provider in KNOWN_CREDENTIAL_PROVIDERS
    assert sent == [("/repos/my-org/repo/bucket-credentials", {"params": {"container": "s3://known/"}})]


@pytest.mark.asyncio
async def test_bucket_credentials_ask_for_an_upgrade_when_the_provider_is_unknown(metastore_answering):
    metastore, _ = metastore_answering(FUTURE_CREDENTIALS["unknown_provider"])

    with pytest.raises(UnsupportedCredentialProviderError, match="Upgrade arraylake"):
        await metastore.get_bucket_credentials_from_bucket(uuid4())


@pytest.mark.asyncio
async def test_refresh_url_is_followed_only_on_the_api_host(metastore_answering):
    metastore, sent = metastore_answering(FUTURE_CREDENTIALS["new_s3_with_refresh_and_extra_fields"])
    url = "https://api.example.com/repos/my-org/repo/bucket-credentials?container=s3%3A%2F%2Fknown%2F"

    await metastore.get_credentials_from_refresh_url(url)
    with pytest.raises(ValueError, match="refusing to send credentials"):
        await metastore.get_credentials_from_refresh_url("https://elsewhere.example.com/steal")

    assert sent == [(url, {})]

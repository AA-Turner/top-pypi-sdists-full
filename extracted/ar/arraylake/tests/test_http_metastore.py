import json
from uuid import uuid4

import pytest

from arraylake.metastore.http_metastore import HttpMetastore, HttpMetastoreConfig
from arraylake.types import BucketModifyRequest


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
    body = await _body_for_bucket_patch(metastore, sent, BucketModifyRequest(nickname="renamed"))

    assert body == {"nickname": "renamed"}
    assert sent["method"] == "PATCH"


@pytest.mark.asyncio
@pytest.mark.parametrize("field", ["platform", "name", "prefix", "extra_config", "auth_config", "em_managed"])
async def test_bucket_patch_never_sends_a_null_for_an_untouched_field(metastore_capturing_body, field):
    metastore, sent = metastore_capturing_body
    body = await _body_for_bucket_patch(metastore, sent, BucketModifyRequest(nickname="renamed"))

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
    body = await _body_for_bucket_patch(metastore, sent, BucketModifyRequest(prefix="", nickname="renamed"))

    assert body == {"nickname": "renamed", "prefix": ""}


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

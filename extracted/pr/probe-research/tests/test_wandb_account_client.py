"""Dedicated account mutation wire and credential non-persistence via the real SDK."""

import json

import httpx
import pytest

from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.errors import RosError
from probe.sdk.transport import Transport

ACCOUNT = "00000000-0000-4000-8000-000000000003"
SECRET = "synthetic-provider-secret"
OPERATIONS = [
    ("create_wandb_account", {"api_key": SECRET}, "POST", "/v1/integrations/wandb/accounts"),
    ("reconnect_wandb_account", {"connection_id": ACCOUNT, "api_key": SECRET}, "POST",
     f"/v1/integrations/wandb/accounts/{ACCOUNT}/reconnect"),
    ("disconnect_wandb_account", {"connection_id": ACCOUNT}, "DELETE",
     f"/v1/integrations/wandb/accounts/{ACCOUNT}"),
]


@pytest.mark.parametrize("method,arguments,verb,path", OPERATIONS)
@pytest.mark.parametrize("status", [200, 404, 503])
@pytest.mark.parametrize("redact", [False, True])
def test_account_mutations_use_dedicated_contract_and_never_queue_credentials(
    tmp_path, method, arguments, verb, path, status, redact,
):
    requests = []

    def respond(request):
        requests.append(request)
        assert request.method == verb and request.url.path == path
        assert "/mirror/" not in request.url.path  # no legacy destructive-delete fallback
        body = json.loads(request.content) if request.content else None
        assert body == ({"credentials": {"api_key": SECRET}} if verb == "POST" else None)
        if status != 200:
            return httpx.Response(status, json={"detail": "fixture refusal"})
        if verb == "DELETE":
            return httpx.Response(204)
        return httpx.Response(201 if method == "create_wandb_account" else 200,
                              json={"id": ACCOUNT, "source": "wandb", "workspace_id": None})

    settings = Settings(base_url="https://api.invalid", token="synthetic")
    spool = tmp_path / "outbox"
    with httpx.Client(base_url=settings.base_url, transport=httpx.MockTransport(respond)) as http:
        transport = Transport(settings, client=http, max_retries=0, attribution="backfill")
        with Client(settings=settings, transport=transport, async_writes=True, auto_drain=False,
                    drain_interval=9999, spool_dir=spool, redact=redact) as client:
            if status == 200:
                result = getattr(client, method)(**arguments)
                assert result is None if verb == "DELETE" else result["id"] == ACCOUNT
            else:
                with pytest.raises(RosError):
                    getattr(client, method)(**arguments)
            assert len(requests) == 1
            assert not client.journal.pending()
    for file in spool.rglob("*"):
        if file.is_file():
            assert SECRET.encode() not in file.read_bytes()


@pytest.mark.parametrize("verb,path,enrollment", [
    ("POST", "/v1/integrations/wandb/accounts", True),
    ("POST", f"/v1/integrations/wandb/accounts/{ACCOUNT}/reconnect", True),
    ("PATCH", "/v1/integrations/wandb/accounts", False),
    ("POST", "/v1/integrations/wandb/accounts/notes", False),
    ("POST", "/v1/integrations/wandb/accounts/not-an-id/reconnect", False),
    ("POST", f"/v1/integrations/wandb/accounts/{ACCOUNT}/reconnect/notes", False),
    ("POST", "/v1/projects/synthetic/notes", False),
])
def test_only_explicit_account_enrollment_preserves_api_key(verb, path, enrollment):
    """Authentication input has a narrow exception; adjacent captured data does not."""
    seen = []

    def respond(request):
        seen.append(json.loads(request.content))
        return httpx.Response(200, json={})

    settings = Settings(base_url="https://api.invalid", token="synthetic")
    original = {"credentials": {"api_key": SECRET},
                "notes": "password=synthetic-notes-secret", "meta": {"api_key": SECRET}}
    with httpx.Client(base_url=settings.base_url, transport=httpx.MockTransport(respond)) as http:
        transport = Transport(settings, client=http, max_retries=0, attribution="backfill")
        transport.request(verb, path, json_body=original)
    body = seen[0]
    assert body["credentials"] == ({"api_key": SECRET} if enrollment else "<redacted>")
    assert SECRET not in json.dumps(body["meta"])
    assert "synthetic-notes-secret" not in body["notes"]
    assert original["meta"]["api_key"] == SECRET  # never mutate caller-owned data


def test_enrollment_route_has_no_durable_journal_exception(tmp_path):
    from probe.sdk.journal import Journal

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/integrations/wandb/accounts",
                        {"credentials": {"api_key": SECRET}})
    assert journal.pending()
    for file in (tmp_path / "outbox").rglob("*"):
        if file.is_file():
            assert SECRET.encode() not in file.read_bytes()

"""Final install notification is scoped, bounded, synchronous, and fieldless."""

from contextlib import nullcontext

import httpx
import pytest

from probe.cli import desktop
from probe.sdk import errors
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.transport import Transport

SCOPE = {"userId": "signed-in-user", "customerId": "approved-team"}


@pytest.fixture
def client(monkeypatch):
    calls = []

    def handle(request):
        calls.append(request)
        if request.url.path == "/v1/me":
            return httpx.Response(200, json={"user_id": SCOPE["userId"], "customer_id": SCOPE["customerId"]})
        assert request.url.path == "/v1/desktop/onboarding/complete"
        assert request.content == b"" and request.method == "POST"
        return httpx.Response(200, json={"complete": True, "scope": SCOPE})

    settings = Settings(base_url="https://test.invalid", token="fixed-human-token")
    transport = Transport(settings, client=httpx.Client(base_url=settings.base_url, transport=httpx.MockTransport(handle)), max_retries=0)
    value = Client(settings=settings, transport=transport, fail_open=False, async_writes=False, auto_drain=False)
    monkeypatch.setattr(desktop, "_client", lambda: nullcontext(value))
    yield value, calls
    value.close()


def test_notification_verifies_scope_then_sends_no_identity_or_settings(client):
    value, calls = client
    result = desktop.dispatch({"op": "onboarding_complete", **SCOPE})
    assert result == {"complete": True, "scope": SCOPE}
    assert [request.url.path for request in calls] == ["/v1/me", "/v1/desktop/onboarding/complete"]
    assert all(request.headers["authorization"] == "Bearer fixed-human-token" for request in calls)
    assert all(0 < request.extensions["timeout"]["read"] <= 12 for request in calls)
    assert not value.fail_open and not value._ambient_credentials


@pytest.mark.parametrize("scope", [
    {**SCOPE, "userId": "different"}, {**SCOPE, "customerId": "other"},
])
def test_account_switch_never_sends_completion(client, scope):
    _, calls = client
    with pytest.raises(ValueError, match="account or destination changed"):
        desktop.dispatch({"op": "onboarding_complete", **scope})
    assert len(calls) == 1 and calls[0].method == "GET"


@pytest.mark.parametrize("scope", [{}, {"userId": ""}, {**SCOPE, "token": "no"}])
def test_missing_identity_or_unknown_fields_are_refused_before_network(client, scope):
    _, calls = client
    with pytest.raises(ValueError):
        desktop.dispatch({"op": "onboarding_complete", **scope})
    assert calls == []


def test_api_refusal_and_unknown_response_never_count_as_complete(client, monkeypatch):
    value, _ = client
    for body in (None, {}, {"complete": True, "scope": {**SCOPE, "userId": "other"}}):
        monkeypatch.setattr(value, "complete_desktop_onboarding", lambda: body)
        with pytest.raises(ValueError, match="did not acknowledge"):
            desktop.dispatch({"op": "onboarding_complete", **SCOPE})
    def unavailable():
        raise errors.TransportError("offline")
    monkeypatch.setattr(value, "complete_desktop_onboarding", unavailable)
    with pytest.raises(errors.TransportError):
        desktop.dispatch({"op": "onboarding_complete", **SCOPE})

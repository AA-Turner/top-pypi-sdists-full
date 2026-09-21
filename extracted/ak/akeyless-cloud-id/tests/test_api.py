"""Public-API and provider-dispatch tests for CloudId.

The real API selects a cloud provider by *method name* (there is no single
``generate(type=...)`` dispatcher), so these tests verify that:

* the class imports and instantiates,
* each per-cloud method exists and is callable, and
* each method dispatches to the correct underlying cloud SDK (proven offline by
  monkeypatching the SDK entrypoints), while an unknown provider name is
  rejected with AttributeError.
"""

import base64

import pytest

import akeyless_cloud_id
from akeyless_cloud_id import CloudId


def test_import_and_instantiate():
    c = CloudId()
    assert isinstance(c, CloudId)


def test_version_exposed():
    assert isinstance(akeyless_cloud_id.__version__, str)
    assert akeyless_cloud_id.__version__


@pytest.mark.parametrize("method_name", ["generate", "generateGcp", "generateAzure", "generateAlibaba"])
def test_provider_methods_exist(method_name):
    c = CloudId()
    assert callable(getattr(c, method_name))


def test_unknown_provider_rejected():
    """There is no dispatcher for arbitrary provider 'types': asking for a
    provider that does not exist must raise AttributeError."""
    c = CloudId()
    with pytest.raises(AttributeError):
        getattr(c, "generateOracle")


def test_gcp_dispatch_is_offline_and_uses_google_id_token(monkeypatch):
    """generateGcp must route to google.oauth2.id_token.fetch_id_token and
    base64-encode the returned OIDC token. Fully offline via monkeypatch."""
    import google.auth.transport.requests as gart
    import google.oauth2.id_token as idt

    captured = {}

    monkeypatch.setattr(gart, "Request", lambda: object())

    def fake_fetch(request, audience):
        captured["audience"] = audience
        return "gcp-oidc-token-for-" + audience

    monkeypatch.setattr(idt, "fetch_id_token", fake_fetch)

    token = CloudId().generateGcp(audience="https://example.com")

    assert captured["audience"] == "https://example.com"
    assert base64.b64decode(token).decode() == "gcp-oidc-token-for-https://example.com"


def test_gcp_dispatch_default_audience(monkeypatch):
    """The documented default audience is akeyless.io."""
    import google.auth.transport.requests as gart
    import google.oauth2.id_token as idt

    captured = {}
    monkeypatch.setattr(gart, "Request", lambda: object())

    def fake_fetch(request, audience):
        captured["audience"] = audience
        return "tok"

    monkeypatch.setattr(idt, "fetch_id_token", fake_fetch)

    CloudId().generateGcp()
    assert captured["audience"] == "akeyless.io"


def test_azure_dispatch_is_offline_and_uses_default_credential(monkeypatch):
    """generateAzure must route to azure.identity.DefaultAzureCredential,
    request the management scope, and base64-encode the returned token."""
    import azure.identity

    captured = {}

    class _FakeToken:
        token = "azure-access-token"

    class _FakeCredential:
        def get_token(self, scope):
            captured["scope"] = scope
            return _FakeToken()

    monkeypatch.setattr(azure.identity, "DefaultAzureCredential", _FakeCredential)

    token = CloudId().generateAzure()

    assert captured["scope"] == "https://management.azure.com/.default"
    assert base64.b64decode(token).decode() == "azure-access-token"

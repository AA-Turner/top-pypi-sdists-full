"""The scraper's own provider keys are read at CALL time through one door (``_ext.provider_secret``).

No ``secret_source`` injected (a standalone install, the separately deployed scraper service): the process
environment, exactly as before. Injected (the platform server): the source's answer is final — an empty answer
(a held key the host cannot read) is "not configured", never the environment copy — and a changed answer is used
on the very next call.
"""

from __future__ import annotations

import pytest

from matrx_scraper import _ext
from matrx_scraper.features.stock_image_search import resolve_unsplash_key
from matrx_scraper.performance import _resolve_oauth_client, _resolve_psi_api_key, _resolve_service_account_info
from matrx_scraper.search.brave_client import BraveSearchClient

KEYS = (
    "BRAVE_SEARCH_API_KEY_PRO_AI", "UNSPLASH_ACCESS_KEY", "GOOGLE_PSI_API_KEY", "GOOGLE_SEARCH_API_KEY",
    "AME_GOOGLE_SEARCH_API_KEY", "FIREBASE_SERVICE_ACCOUNT", "GOOGLE_SERVICE_ACCOUNT", "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET", "GSC_CLIENT_ID", "GSC_CLIENT_SECRET", "GOOGLE_OAUTH_CLIENT_SECRETS",
)
CLIENT_ID = "123.apps.googleusercontent.com"
SA = '{"type": "service_account", "client_email": "x@y"}'


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    for name in KEYS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delitem(_ext._registry, "secret_source", raising=False)


def test_unset_everywhere_is_not_configured():
    assert resolve_unsplash_key() is None
    assert _resolve_psi_api_key() is None
    assert _resolve_service_account_info() is None
    assert _resolve_oauth_client() == (None, None)
    with pytest.raises(ValueError, match="No Brave API key"):
        BraveSearchClient()
    assert BraveSearchClient(allow_missing_key=True)._api_key is None


def test_no_source_reads_the_environment(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY_PRO_AI", "env-brave")
    monkeypatch.setenv("UNSPLASH_ACCESS_KEY", "env-unsplash")
    monkeypatch.setenv("GOOGLE_SEARCH_API_KEY", "env-google")
    monkeypatch.setenv("FIREBASE_SERVICE_ACCOUNT", SA)
    monkeypatch.setenv("GOOGLE_CLIENT_ID", CLIENT_ID)
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "env-csec")
    assert BraveSearchClient()._api_key == "env-brave"
    assert resolve_unsplash_key() == "env-unsplash"
    assert _resolve_psi_api_key() == "env-google"
    assert _resolve_service_account_info() == {"type": "service_account", "client_email": "x@y"}
    assert _resolve_oauth_client() == (CLIENT_ID, "env-csec")


def test_injected_source_answers_at_call_time(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY_PRO_AI", "env-brave")
    held = {
        "BRAVE_SEARCH_API_KEY_PRO_AI": "vault-brave-1", "UNSPLASH_ACCESS_KEY": "vault-unsplash",
        "GOOGLE_PSI_API_KEY": "vault-psi", "FIREBASE_SERVICE_ACCOUNT": SA,
        "GOOGLE_CLIENT_ID": CLIENT_ID, "GOOGLE_CLIENT_SECRET": "vault-csec",
    }
    monkeypatch.setitem(_ext._registry, "secret_source", held.get)
    client = BraveSearchClient()
    assert client._api_key == "vault-brave-1"
    held["BRAVE_SEARCH_API_KEY_PRO_AI"] = "vault-brave-2"  # rotated: the same client uses it next call
    assert client._api_key == "vault-brave-2"
    assert BraveSearchClient(api_key="callers-own")._api_key == "callers-own"  # an explicit key is never replaced
    assert resolve_unsplash_key() == "vault-unsplash"
    assert resolve_unsplash_key("explicit") == "explicit"
    assert _resolve_psi_api_key() == "vault-psi"
    assert _resolve_service_account_info()["type"] == "service_account"
    assert _resolve_oauth_client() == (CLIENT_ID, "vault-csec")


def test_an_unreadable_held_key_is_not_configured(monkeypatch):
    # The host answers "" for a held key that does not decrypt; the env copy is never used.
    for name in ("BRAVE_SEARCH_API_KEY_PRO_AI", "UNSPLASH_ACCESS_KEY", "GOOGLE_PSI_API_KEY"):
        monkeypatch.setenv(name, "env-copy")
    monkeypatch.setitem(_ext._registry, "secret_source", lambda name: "")
    with pytest.raises(ValueError, match="No Brave API key"):
        BraveSearchClient()
    assert resolve_unsplash_key() is None
    assert _resolve_psi_api_key() is None


def test_bright_data_client_reads_its_key_per_request():
    from matrx_scraper.vendors.brightdata import BrightDataClient, BrightDataError

    assert BrightDataClient("given")._current_key() == "given"  # no source: the key it was built with
    held = {"key": "vault-1"}
    client = BrightDataClient("vault-1", key_source=lambda: held["key"])
    held["key"] = "vault-2"
    assert client._current_key() == "vault-2"
    held["key"] = ""  # removed / unreadable after boot: refused by name, nothing sent
    with pytest.raises(BrightDataError, match="not configured"):
        client._current_key()

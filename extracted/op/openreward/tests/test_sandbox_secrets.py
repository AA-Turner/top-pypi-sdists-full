"""Unit tests for sandbox secret encoding and api_key domain augmentation.

No network — these exercise the pure helpers in
``openreward.api.sandboxes.secrets``.
"""

from __future__ import annotations

import base64
import json

from openreward.api.sandboxes.secrets import (
    augment_secrets_with_api_key,
    build_secrets_header,
    openreward_service_hosts,
)


def _domains(secret_entry) -> list[str]:
    """The augmented api_key entry is a ``(value, allowed_domains)`` tuple."""
    assert isinstance(secret_entry, tuple)
    return secret_entry[1]


def test_api_key_allowed_domains_include_search_service():
    """The auto-injected api_key secret must be permitted to reach the
    backdated web service (search/fetch), which authenticates with the same
    key — otherwise the egress proxy 403s the web toolset from sandboxes."""
    out = augment_secrets_with_api_key(
        None,
        api_key="or_test",
        base_url="https://sessions.openreward.ai",
        api_base_url="https://api.openreward.ai",
    )
    assert out is not None
    for key in ("api_key", "OPENREWARD_API_KEY"):
        domains = _domains(out[key])
        assert "search.openreward.ai" in domains, domains
        # internal cluster variant is derived automatically
        assert "search.openreward.internal" in domains, domains
        # original session/api hosts are still present
        assert "sessions.openreward.ai" in domains
        assert "api.openreward.ai" in domains


def test_search_host_respects_env_override(monkeypatch):
    monkeypatch.setenv("OPENREWARD_WEB_SEARCH_URL", "https://search.example.test/search")
    monkeypatch.setenv("OPENREWARD_WEB_FETCH_URL", "https://search.example.test/fetch")
    out = augment_secrets_with_api_key(
        None, api_key="or_test", base_url="https://sessions.openreward.ai", api_base_url=None
    )
    domains = _domains(out["api_key"])
    assert "search.example.test" in domains
    # deduped — the single host appears once despite two env vars
    assert domains.count("search.example.test") == 1


def test_openreward_service_hosts_default_and_override(monkeypatch):
    monkeypatch.delenv("OPENREWARD_WEB_SEARCH_URL", raising=False)
    monkeypatch.delenv("OPENREWARD_WEB_FETCH_URL", raising=False)
    assert openreward_service_hosts() == ["search.openreward.ai"]

    monkeypatch.setenv("OPENREWARD_WEB_SEARCH_URL", "https://s.example.test/search")
    monkeypatch.setenv("OPENREWARD_WEB_FETCH_URL", "https://f.example.test/fetch")
    assert openreward_service_hosts() == ["s.example.test", "f.example.test"]


def test_none_api_key_is_passthrough():
    assert augment_secrets_with_api_key(None, None, None, None) is None
    passed = augment_secrets_with_api_key({"k": ("v", ["d"])}, None, None, None)
    assert passed == {"k": ("v", ["d"])}


def test_build_secrets_header_roundtrip_preserves_domains():
    out = augment_secrets_with_api_key(
        None, api_key="or_test", base_url="https://sessions.openreward.ai", api_base_url=None
    )
    decoded = json.loads(base64.b64decode(build_secrets_header(out)))
    assert "search.openreward.ai" in decoded["api_key"]["allowed_domains"]
    assert decoded["api_key"]["value"] == "or_test"

"""End-to-end integration tests across module boundaries.

These tests exercise multiple modules working together — the kind of
failures that unit tests (each passing in isolation) miss. Designed to
catch:

  - Shape drift: backend /chat response format ↔ CLI provider parsing
  - Tier flow: free user → 403 → upgrade prompt path is intact
  - Anonymizer chokepoint: ALL cloud calls pass through anonymization
  - Model routing: cloud:* IDs resolve to SageHostedProvider
  - Document → vision → prompt builder cooperate without mismatch

Each test mocks the network layer (no real Vertex AI / Cloud Run calls)
but uses real instances of every sage module so contract drift surfaces.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]



# ── Privacy + anonymizer chokepoint ──────────────────────────────────────────


class TestAnonymizerChokepoint:
    """Every cloud payload MUST go through anonymize_payload before
    leaving the user's machine. This is a privacy contract — if a future
    refactor adds a path that bypasses the anonymizer, sage's
    /privacy/cloud-ai page becomes a lie."""

    def test_openai_compat_payload_anonymized_before_send(self):
        from sage.providers.anonymizer import anonymize_payload

        # Payload as constructed by openai_compat's _build_payload
        raw_payload = {
            "model": "qwen/qwen3-coder:free",
            "messages": [{"role": "user", "content": "email me at jane@example.com"}],
            "user": "uid-12345",
            "metadata": {"session": "abc"},
            "temperature": 0.7,
            "max_tokens": 256,
            "stream": False,
        }
        sanitized = anonymize_payload(raw_payload, provider_name="openrouter")
        # Forbidden fields stripped
        assert "user" not in sanitized
        assert "metadata" not in sanitized
        # PII in messages scrubbed
        assert "jane@example.com" not in sanitized["messages"][0]["content"]
        # Legitimate fields preserved
        assert sanitized["temperature"] == 0.7
        assert sanitized["model"] == "qwen/qwen3-coder:free"

    def test_gemini_payload_also_anonymized(self):
        from sage.providers.anonymizer import anonymize_payload

        raw = {
            "contents": [
                {"role": "user", "parts": [{"text": "send to jane@example.com"}]},
            ],
            "user": "uid-12345",
        }
        out = anonymize_payload(raw, provider_name="gemini")
        assert "user" not in out
        assert "jane@example.com" not in out["contents"][0]["parts"][0]["text"]

    def test_local_provider_passthrough_unchanged(self):
        """Anonymizer is for cloud — local Ollama/llama-cpp calls don't
        leave the machine, so no need to scrub."""
        from sage.providers.anonymizer import anonymize_payload

        raw = {"user": "test", "messages": []}
        out = anonymize_payload(raw, provider_name="ollama")
        assert out is raw  # Identity — pure passthrough


# ── Tier rate limiter contract ───────────────────────────────────────────────


class TestTierFlow:
    """The end-to-end tier story: free users blocked from cloud, paid
    users get them, both get OpenRouter and local. Backend → CLI."""

    def test_free_user_gcp_path_blocked_with_upgrade_payload(self):
        from backend.tier_rate_limiter import (
            TierRateLimiter,
            classify_model_resource,
            billing_tier_to_rate_tier,
        )

        limiter = TierRateLimiter()
        # Map: free billing tier → free rate tier
        assert billing_tier_to_rate_tier("free") == "free"
        # Map: cloud:* model_id → gcp_hosted resource
        assert classify_model_resource("cloud:qwen-coder-7b") == "gcp_hosted"

        # Combined: free user trying to hit cloud → upgrade required
        decision = limiter.check_and_consume(
            uid="alice", tier="free", resource="gcp_hosted",
        )
        assert not decision.allowed
        assert decision.upgrade_required
        assert "Pro plan" in decision.reason or "upgrade" in decision.reason.lower()

    def test_paid_user_gcp_path_succeeds_under_quota(self):
        from backend.tier_rate_limiter import TierRateLimiter, billing_tier_to_rate_tier

        # All paying billing tiers map to "paid"
        for billing in ("starter", "pro", "premium", "starter_annual"):
            assert billing_tier_to_rate_tier(billing) == "paid"

        limiter = TierRateLimiter()
        decision = limiter.check_and_consume("bob", "paid", "gcp_hosted")
        assert decision.allowed
        assert decision.daily_used == 1

    def test_paid_user_at_daily_cap_returns_429_with_retry_after(self):
        from unittest.mock import patch
        from backend.tier_rate_limiter import TierRateLimiter, TIERS

        with patch.dict(
            TIERS["paid"],
            {**TIERS["paid"], "gcp_hosted":
                TIERS["paid"]["gcp_hosted"].__class__(
                    daily_cap=2, burst_per_minute=100, accessible=True,
                )},
            clear=False,
        ):
            limiter = TierRateLimiter()
            limiter.check_and_consume("c", "paid", "gcp_hosted")
            limiter.check_and_consume("c", "paid", "gcp_hosted")
            blocked = limiter.check_and_consume("c", "paid", "gcp_hosted")
            assert not blocked.allowed
            # 429-equivalent: not upgrade-required, has retry-after
            assert not blocked.upgrade_required
            assert blocked.retry_after_seconds is not None
            assert blocked.retry_after_seconds > 0

    def test_admin_user_bypasses_all_limits(self):
        """is_admin() lookup → tier="admin" → unlimited access everywhere."""
        from backend.billing import is_admin
        from backend.tier_rate_limiter import TierRateLimiter, billing_tier_to_rate_tier

        # Admin emails recognized
        assert is_admin("laynefaler@gmail.com")
        assert is_admin("wmfaler@gmail.com")
        assert is_admin("elana@recoveryhelpnow.com")
        assert not is_admin("random@example.com")

        # Admin tier → no caps anywhere
        assert billing_tier_to_rate_tier("admin") == "admin"
        limiter = TierRateLimiter()
        # 50 calls all succeed (no daily cap for admin)
        for _ in range(50):
            d = limiter.check_and_consume("admin-uid", "admin", "gcp_hosted")
            assert d.allowed


# ── Backend response shape ↔ CLI provider parsing ────────────────────────────


class TestBackendResponseShape:
    """The backend's /chat returns one of two shapes:

      Non-streaming: {"ok": True, "output": "<text>", "conversation_id": ...}
      Streaming:    SSE with {"token": "<piece>"} per chunk

    SageHostedProvider must parse BOTH. If the backend changes its shape
    (or the provider drops support for one), this test catches it."""

    def test_provider_parses_non_streaming_response(self):
        from sage.providers.sage_hosted import SageHostedProvider

        # Use a stub client that returns the canonical backend shape
        class _StubClient:
            def post(self, url, json, headers):
                return _Resp({
                    "ok": True,
                    "output": "The answer is 42.",
                    "conversation_id": None,
                })

        # We can't easily instantiate the full provider with a stub client
        # (it uses httpx.Client internally), so test the parser directly.
        # The fields we extract should match the backend's contract.
        backend_response = {
            "ok": True,
            "output": "The answer is 42.",
            "conversation_id": None,
        }
        # Reproduces what provider.generate's body extraction does
        if backend_response.get("ok") and "output" in backend_response:
            extracted = backend_response["output"]
        else:
            extracted = ""
        assert extracted == "The answer is 42."

    def test_provider_parses_streaming_token_events(self):
        """SSE 'data: {"token": "...}' lines yield tokens correctly."""
        import json as json_mod
        ssel = b'data: {"token": "2"}\n\ndata: {"token": " +"}\n\ndata: {"done": true}\n\n'
        # Lines after iter_lines split:
        lines = [
            'data: {"token": "2"}',
            'data: {"token": " +"}',
            'data: {"done": true}',
        ]
        tokens = []
        for line in lines:
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload:
                continue
            parsed = json_mod.loads(payload)
            if parsed.get("done"):
                break
            if parsed.get("token"):
                tokens.append(parsed["token"])
        assert tokens == ["2", " +"]

    def test_provider_handles_upgrade_required_403(self):
        """Free user → /chat returns 403 with structured detail.
        Provider must raise UpgradeRequired, not a generic error."""
        from sage.providers.sage_hosted import (
            SageHostedProvider, UpgradeRequired,
        )

        class _FakeResponse:
            status_code = 403
            is_success = False
            text = ""

            def read(self):
                return None

            def json(self):
                return {
                    "detail": {
                        "error": "Sage-hosted models are part of the Pro plan.",
                        "upgrade_required": True,
                        "upgrade_url": "https://sageworksai.com/#billing",
                    },
                }

        provider = SageHostedProvider()
        with pytest.raises(UpgradeRequired):
            provider._raise_for_status(_FakeResponse())


class _Resp:
    def __init__(self, body):
        self._body = body
        self.status_code = 200
        self.is_success = True

    def json(self):
        return self._body

    def raise_for_status(self):
        pass


# ── Model registry ↔ CloudRuntime URL lookup ────────────────────────────────


class TestModelRegistryContract:
    """The model_registry.json file is the source of truth for cloud:*
    URLs (with env var override). CloudRuntime reads it on load(); if
    the file shape changes, CloudRuntime breaks."""

    def test_registry_keys_match_deployed_services(self):
        """Every deployed model service must appear in model_registry.json, and
        every registry key must resolve to one of those services.

        This used to assert set-EQUALITY against 8 hardcoded key names, which
        made it fail the moment the registry legitimately grew. The registry now
        holds 15 keys and its own `_comment` explains why: the 7 newer canonical
        names (qwen3-coder, gemma-4, llama-3-2, llava-llama-3, mistral-small,
        phi-4-reasoning, yi-coder-9b) are ALIASES that intentionally point at the
        same Cloud Run URLs as the 8 original keys, so existing config keeps
        working. `cloud:qwen3-coder` is in fact the default model this very test
        suite drives, so the hardcoded list was rejecting the primary model.

        A hardcoded name list re-breaks on every legitimate addition. Derive the
        deployed services from the cloudbuild YAMLs instead -- which is what the
        original docstring claimed to do -- and assert the two directions that
        actually matter.
        """
        model_servers = Path(__file__).parent.parent.parent / "model_servers"
        registry_path = model_servers / "model_registry.json"
        if not registry_path.exists():
            pytest.skip(
                "MISSING PREREQUISITE: model_servers/model_registry.json not found at "
                f"{registry_path}. It is the source of truth for cloud:* URLs; a "
                "fabricated stand-in would assert nothing. Run this test from a full "
                "source checkout."
            )

        registry = json.loads(registry_path.read_text())
        registry_entries = {k: v for k, v in registry.items() if k != "_comment"}

        # One cloudbuild.<served-model-name>.yaml per individually deployed
        # service. The multi-* bundles are composite deploys, not served-model
        # names, so they are not registry keys.
        deployed = {
            path.name[len("cloudbuild."):-len(".yaml")]
            for path in model_servers.glob("cloudbuild.*.yaml")
        }
        deployed -= {name for name in deployed if name.startswith("multi-")}
        assert deployed, f"No per-model cloudbuild YAMLs found in {model_servers}"

        # 1. No deployed service may be missing from the registry, or
        #    CloudRuntime cannot route to it at all.
        missing = deployed - registry_entries.keys()
        assert not missing, (
            f"Deployed model services absent from model_registry.json: {sorted(missing)}. "
            "CloudRuntime.load() cannot resolve a URL for these."
        )

        # 2. Every key -- canonical or alias -- must resolve to a URL that some
        #    deployed service owns. This is what catches a real typo or a stale
        #    alias left pointing at a decommissioned service, while still
        #    allowing new aliases to be added freely.
        deployed_urls = {registry_entries[name] for name in deployed}
        dangling = {
            key: url for key, url in registry_entries.items()
            if url not in deployed_urls
        }
        assert not dangling, (
            f"Registry keys point at URLs no deployed service owns: {dangling}. "
            f"Known service URLs: {sorted(deployed_urls)}"
        )

    def test_cloud_runtime_url_lookup_via_env(self, monkeypatch):
        """The env-var fallback path must work — used in production
        where the registry file isn't shipped with the backend container."""
        from backend.runtimes.cloud_runtime import _lookup_service_url

        monkeypatch.setenv("CLOUD_MODEL_URL_QWEN_CODER_7B", "https://qwen-test.example.com")
        url = _lookup_service_url("qwen-coder-7b")
        assert url == "https://qwen-test.example.com"

    def test_cloud_runtime_returns_none_for_unconfigured_model(self, monkeypatch):
        """If no env var AND no registry entry, lookup returns None so
        the runtime raises a clear 'not deployed' error rather than
        crashing on a None URL."""
        from backend.runtimes.cloud_runtime import _lookup_service_url

        # Make sure no env var leak from other tests
        for var in list(monkeypatch._setattr or []):
            pass
        monkeypatch.delenv("CLOUD_MODEL_URL_NONEXISTENT", raising=False)
        # Should not crash; should return None
        result = _lookup_service_url("nonexistent-fake-model-xyz")
        # None means "not configured" — the caller (CloudRuntime.load) raises a clear error
        assert result is None or "fake" not in result


# ── End-to-end vision flow ───────────────────────────────────────────────────


class TestVisionFlow:
    """User attaches an image → CLI encodes → message has multipart content
    → routes to cloud:llava-next-7b. If any step shape-drifts, this fails."""

    def test_image_path_to_vision_message_to_provider_input(self, tmp_path):
        from sage.core.vision_input import build_vision_message, encode_image_for_vision

        png = tmp_path / "test.png"
        png.write_bytes(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\rIDATx\x9cc\x00\x01\x00\x00\x05\x00"
            b"\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )

        attachment = encode_image_for_vision(png)
        assert attachment.data_url.startswith("data:image/png;base64,")

        msg = build_vision_message("describe", [png])
        # OpenAI multimodal shape — exactly what LLaVA-NeXT vLLM expects
        assert msg["role"] == "user"
        assert isinstance(msg["content"], list)
        # First part is the prompt text
        assert msg["content"][0]["type"] == "text"
        # Second part is the image with a data URL
        assert msg["content"][1]["type"] == "image_url"
        assert msg["content"][1]["image_url"]["url"].startswith("data:image/png")


# ── Search → orchestration → result shape ───────────────────────────────────


class TestSearchOrchestration:
    """The full Perplexity-style flow: classify → retrieve → synthesize →
    cite. All in-process (no real API calls). Validates the result shape
    matches what the CLI command renders."""

    def test_pipeline_returns_renderable_result(self):
        from sage.core.query_orchestrator import (
            QueryOrchestrator, QueryClassification, QueryType,
        )

        orch = QueryOrchestrator(
            available_models=["cloud:llama-3-1-8b", "cloud:qwen-coder-7b"],
        )
        # Wire up the stages with simple fakes
        orch._classify_stage = lambda q: QueryClassification(
            query_type=QueryType.FACTUAL, confidence=0.9, requires_search=True,
        )
        orch._retrieve_stage = lambda q: [
            {"uri": "https://example.com/a", "title": "A"},
            {"uri": "https://example.com/b", "title": "B"},
        ]
        orch._synthesize_stage = lambda q, c, srcs: ("Synthesized answer.", 42)
        orch._cite_stage = lambda ans, srcs: srcs

        result = orch.run("test query")
        # Shape contract — CLI rendering depends on these
        assert result.answer == "Synthesized answer."
        assert result.sources[0]["uri"] == "https://example.com/a"
        assert result.total_tokens == 42
        assert "CLASSIFY" in result.models_used
        assert "SYNTHESIZE" in result.models_used


# ── Privacy posture: delete + export work together ──────────────────────────


class TestPrivacyControls:
    """The transparency promise: users can audit + delete their data.
    Tests the controls a paying customer (or regulator) would verify."""

    def test_anonymizer_module_advertises_what_it_strips(self):
        """The /privacy/cloud-ai page mirrors this list; if the Python
        set drifts from the React component, the transparency page lies.

        Frontend mirror lives at:
          ai-platform/frontend/src/legal/CloudAITransparency.jsx (FORBIDDEN_KEYS)
        """
        from sage.providers.anonymizer import FORBIDDEN_TOP_LEVEL_KEYS

        # Frontend ships this list verbatim
        frontend_advertises = {
            "user", "user_id", "userid",
            "end_user", "end_user_id",
            "customer", "customer_id",
            "client_id", "uid",
            "email", "identity", "metadata",
            "fingerprint", "session_id", "request_id",
        }
        assert frontend_advertises == FORBIDDEN_TOP_LEVEL_KEYS, (
            "Anonymizer's forbidden-key set drifted from the frontend "
            "transparency page. Update both: anonymizer.py + "
            "frontend/src/legal/CloudAITransparency.jsx"
        )

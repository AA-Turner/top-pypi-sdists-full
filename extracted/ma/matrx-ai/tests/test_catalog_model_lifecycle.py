"""Guards for the model lifecycle ruling (2026-09-09, DECISIONS.md):

- a DEPRECATED model resolves and runs normally — no substitution — and the
  server warns ONCE per model per process, naming the replacement;
- a RETIRED model is refused with an error naming the replacement;
- the replacement is `successor_id` when set, else same maker + same output
  modalities + is_primary (never a deprecated/retired candidate);
- TTS tier routing no longer treats "deprecated" as a reason to reroute.

Each of these was demonstrated FAILING before the fix: the views hid deprecated
rows, `resolve_tts_call_profile` rerouted on `model_is_deprecated`, and nothing
anywhere named a replacement.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog import lifecycle
from matrx_ai.catalog import resolve as resolve_mod
from matrx_ai.catalog.lifecycle import (
    ModelRetiredError,
    describe_replacement,
    gate_model_lifecycle,
    replacement_candidates,
    reset_deprecation_warnings,
)
from matrx_ai.catalog.manager import ai_catalog_manager
from matrx_ai.testing.profile_factory import make_profile

GOOGLE = "provider-google"
FLASH_37 = "model-gemini-3.7-flash"
FLASH_38 = "model-gemini-3.8-flash"
PRO = "model-gemini-pro"
IMAGE_PRIMARY = "model-gemini-image"
DEAD = "model-gemini-1.0"


def _states(**overrides: dict[str, Any]) -> dict[str, dict[str, Any]]:
    text = {"input": ["text"], "output": ["text"]}
    base = {
        FLASH_37: {
            "id": FLASH_37, "name": "gemini-3.7-flash", "common_name": "Gemini 3.7 Flash",
            "provider_id": GOOGLE, "is_deprecated": True, "is_primary": False,
            "retired_at": None, "successor_id": None, "capabilities": text,
        },
        FLASH_38: {
            "id": FLASH_38, "name": "gemini-3.8-flash", "common_name": "Gemini 3.8 Flash",
            "provider_id": GOOGLE, "is_deprecated": False, "is_primary": True,
            "retired_at": None, "successor_id": None, "capabilities": text,
        },
        PRO: {
            "id": PRO, "name": "gemini-pro", "common_name": "Gemini Pro",
            "provider_id": GOOGLE, "is_deprecated": False, "is_primary": True,
            "retired_at": None, "successor_id": None, "capabilities": text,
        },
        IMAGE_PRIMARY: {
            "id": IMAGE_PRIMARY, "name": "gemini-image", "common_name": "Gemini Image",
            "provider_id": GOOGLE, "is_deprecated": False, "is_primary": True,
            "retired_at": None, "successor_id": None,
            "capabilities": {"input": ["text"], "output": ["image"]},
        },
        DEAD: {
            "id": DEAD, "name": "gemini-1.0", "common_name": "Gemini 1.0",
            "provider_id": GOOGLE, "is_deprecated": True, "is_primary": False,
            "retired_at": "2026-09-01T00:00:00+00:00", "successor_id": FLASH_38,
            "capabilities": text,
        },
    }
    for key, patch in overrides.items():
        base[key] = {**base[key], **patch}
    return base


@pytest.fixture(autouse=True)
def _fresh_warnings():
    reset_deprecation_warnings()
    yield
    reset_deprecation_warnings()


def _capture_vcprint(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []

    def fake(*args: Any, **kwargs: Any) -> None:
        calls.append({"args": args, **kwargs})

    monkeypatch.setattr(lifecycle, "vcprint", fake)
    return calls


# ── the gate ─────────────────────────────────────────────────────────────────
def test_deprecated_model_passes_the_gate_and_warns_once_per_process(monkeypatch):
    calls = _capture_vcprint(monkeypatch)
    states = _states()
    gate_model_lifecycle(FLASH_37, states)  # must NOT raise — deprecated still runs
    gate_model_lifecycle(FLASH_37, states)
    gate_model_lifecycle(FLASH_37, states)
    assert len(calls) == 1, "a request storm on a deprecated model must not become a log storm"
    text = str(calls[0]["args"][0])
    assert "DEPRECATED" in text and "still runs" in text
    assert "Gemini 3.8 Flash" in text and "Gemini Pro" in text  # same-class fallback names ALL
    assert calls[0]["title"].endswith("AI MODEL DEPRECATED")


def test_live_model_is_silent(monkeypatch):
    calls = _capture_vcprint(monkeypatch)
    gate_model_lifecycle(FLASH_38, _states())
    assert calls == []


def test_retired_model_is_refused_naming_the_successor(monkeypatch):
    calls = _capture_vcprint(monkeypatch)
    with pytest.raises(ModelRetiredError) as exc:
        gate_model_lifecycle(DEAD, _states())
    assert "retired" in str(exc.value)
    assert "Gemini 3.8 Flash" in str(exc.value) and FLASH_38 in str(exc.value)
    assert calls and calls[0]["title"].endswith("AI MODEL RETIRED")
    # Refusal is loud EVERY time — it is an error, not a once-per-process warning.
    with pytest.raises(ModelRetiredError):
        gate_model_lifecycle(DEAD, _states())
    assert len(calls) == 2


# ── replacement naming ───────────────────────────────────────────────────────
def test_explicit_successor_beats_the_inferred_class():
    states = _states(**{FLASH_37: {"successor_id": PRO}})
    assert [c["id"] for c in replacement_candidates(FLASH_37, states)] == [PRO]
    assert "successor_id" in describe_replacement(FLASH_37, states)


def test_inferred_replacement_is_same_maker_same_outputs_primary_and_alive():
    states = _states(**{PRO: {"is_deprecated": True}})  # a deprecated primary never qualifies
    ids = {c["id"] for c in replacement_candidates(FLASH_37, states)}
    assert ids == {FLASH_38}
    assert IMAGE_PRIMARY not in ids  # different output modality = different class


def test_no_replacement_says_so_instead_of_inventing_one():
    states = _states(**{FLASH_38: {"is_primary": False}, PRO: {"is_primary": False}})
    assert replacement_candidates(FLASH_37, states) == []
    assert "successor_id" in describe_replacement(FLASH_37, states)


# ── resolve_call_profile runs a deprecated model, refuses a retired one ───────
def _seed_catalog(states: dict[str, dict[str, Any]]) -> None:
    ai_catalog_manager.load_from_rows(
        endpoints=[{"id": "ep-google", "vendor": "google", "internal_name": "google_direct",
                    "display_name": "Google", "is_active": True}],
        apis=[{"id": "api-google-chat", "name": "google_chat", "display_name": "Google Chat",
               "translator_key": "google_chat", "rules": {"params": {}, "constraints": []}}],
        offerings=[
            {"id": f"off-{mid}", "model_id": mid, "endpoint_id": "ep-google",
             "api_id": "api-google-chat", "provider_model_id": st["name"], "is_available": True,
             "override": {"params": {}, "constraints": []}}
            for mid, st in states.items()
        ],
        settings=[],
        providers={GOOGLE: "Google"},
        models=list(states.values()),
    )


def _stub_loader(states: dict[str, dict[str, Any]], monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    async def load_model(ref: str):
        st = states.get(ref)
        if st is None:
            return None
        return SimpleNamespace(
            id=st["id"], name=st["name"], provider_id=st["provider_id"],
            capabilities=st["capabilities"], pricing=None,
        )

    monkeypatch.setattr(ai_model_manager_instance, "load_model", load_model)


@pytest.mark.asyncio
async def test_resolve_call_profile_runs_a_deprecated_model_without_substitution(monkeypatch):
    calls = _capture_vcprint(monkeypatch)
    states = _states(**{FLASH_37: {"successor_id": FLASH_38}})
    _seed_catalog(states)
    _stub_loader(states, monkeypatch)
    profile = await resolve_mod.resolve_call_profile(FLASH_37)
    profile_again = await resolve_mod.resolve_call_profile(FLASH_37)
    assert profile.model_id == FLASH_37, "the caller asked for 3.7 — it gets 3.7"
    assert profile.model_name == "gemini-3.7-flash"
    assert profile.resolution_route == "preferred"
    assert profile.model_is_deprecated is True
    assert profile.model_retired_at is None
    assert profile.model_successor_id == FLASH_38
    assert profile_again.model_id == FLASH_37
    assert len(calls) == 1 and "Gemini 3.8 Flash" in str(calls[0]["args"][0])


@pytest.mark.asyncio
async def test_resolve_call_profile_refuses_a_retired_model(monkeypatch):
    _capture_vcprint(monkeypatch)
    states = _states()
    _seed_catalog(states)
    _stub_loader(states, monkeypatch)
    with pytest.raises(ModelRetiredError, match="Gemini 3.8 Flash"):
        await resolve_mod.resolve_call_profile(DEAD)


# ── TTS: deprecated is not a reroute reason ──────────────────────────────────
@pytest.mark.asyncio
async def test_tts_routing_keeps_a_deprecated_model_that_carries_the_tier(monkeypatch):
    pinned = make_profile(
        model_name="gemini-2.5-pro-preview-tts",
        wire_format="google_chat",
        vendor="google",
        capabilities={"input": ["text"], "output": ["audio"], "features": [],
                      "interaction": "turn", "multilingual": True},
    ).model_copy(update={
        "model_is_deprecated": True,
        "offering_metadata": {"tts": {"quality_tiers": ["high_quality"], "is_default": True}},
    })

    async def fake_resolve(model_ref: str, endpoint_hint=None, *, offering_id=None):
        return pinned

    monkeypatch.setattr(resolve_mod, "resolve_call_profile", fake_resolve)
    out = await resolve_mod.resolve_tts_call_profile("gemini-2.5-pro-preview-tts", "high_quality")
    assert out is pinned, "before the ruling this rerouted purely because the model was deprecated"
    assert out.resolution_route != "tier_reroute"

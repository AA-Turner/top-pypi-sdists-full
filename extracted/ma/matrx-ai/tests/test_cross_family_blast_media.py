"""Cross-MODALITY blast net — chat configs fired at every MEDIA family's
resolver and media configs fired at every CHAT family's resolver.

The sibling ``test_cross_family_blast.py`` proves chat families survive each
other's configs. This net proves the crown-jewel guarantee holds ACROSS the
chat/media boundary, through the REAL seams:

  * media seam: ``BaseMediaGeneration._outbound_params`` — every chat family's
    full golden config set fired at every media family. A canonical chat key
    not declared by the media family's compiled rules (``verbosity``,
    ``reasoning_effort``, ``thinking_budget``, ...) must be DROPPED by the
    shared declared-keys gate, never leaked into the provider body via
    PASSTHROUGH_RULE. The gate must also be a PURE foreign-key filter — output
    for the declared keys is byte-identical to the ungated resolver
    (``scripts/validate_media_parity.py`` stays 0-diff).
  * chat seam: ``resolve_outbound_params`` — a curated media config grid fired
    at every chat family. The chat gate already handles this; asserted anyway
    so a regression on either side screams here.

Media rules come from ``fixtures/media_family_rules/*.json`` (regenerate:
``uv run python scripts/dump_media_family_rules.py``); chat rules + source
configs come from the chat param golden. Both are offline — this runs on
every CI pass.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import CompiledControlsMap, flatten_dotted
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.base_media import BaseMediaGeneration
from matrx_ai.providers.outbound_params import resolve_outbound_params

from test_chat_param_golden import compiled_from_golden, load_golden
from test_cross_family_blast import _all_source_configs
from test_cross_family_blast import _variant_keys as _chat_variant_keys

MEDIA_FIXTURE_DIR = Path(__file__).parent / "fixtures" / "media_family_rules"

_MAX_FAILURES_SHOWN = 8

# Every canonical media-cluster key the canonicalizer can emit — the curated
# grid below must exercise all of them against the chat families.
_MEDIA_SOURCE_CONFIGS: list[dict[str, Any]] = [
    {"aspect_ratio": "16:9"},
    {"width": 1024, "height": 768},
    {"width": 2048, "height": 1152, "count": 4},
    {"duration_seconds": 8, "fps": 24, "generate_audio": True},
    {"steps": 30, "guidance_scale": 7.5, "negative_prompt": "blurry, low quality"},
    {
        "background": "transparent",
        "output_compression": 80,
        "moderation": "low",
        "input_fidelity": "high",
        "partial_images": 2,
    },
    {
        "style": "vivid",
        "disable_safety_checker": True,
        "enhance_prompt": True,
        "encode_quality": 85,
    },
    {"render_quality": "high", "resolution": "1k", "output_format": "png"},
    # Mixed: chat-legal knobs riding WITH media knobs — only the media keys
    # may be dropped by a chat family's gate.
    {"temperature": 0.7, "max_output_tokens": 1000, "aspect_ratio": "1:1", "seed": 42},
]


def _media_variant_keys() -> list[str]:
    keys = sorted(p.stem for p in MEDIA_FIXTURE_DIR.glob("*.json"))
    assert keys, (
        f"no media rule fixtures under {MEDIA_FIXTURE_DIR} — regenerate with "
        "`uv run python scripts/dump_media_family_rules.py`"
    )
    return keys


def _load_media(variant_key: str) -> dict[str, Any]:
    return json.loads((MEDIA_FIXTURE_DIR / f"{variant_key}.json").read_text())


def _compiled_media(payload: dict[str, Any]) -> CompiledControlsMap:
    rules = {key: ControlRule.model_validate(rule) for key, rule in payload["rules"].items()}
    return CompiledControlsMap(rules=rules, value_orders=payload["value_orders"])


def _declared_keys(compiled: CompiledControlsMap) -> set[str]:
    declared = set(compiled.rules)
    for rule in compiled.rules.values():
        declared.update(rule.processor_config.get("consumes", []))
    return declared


def test_media_fixture_covers_every_media_family() -> None:
    """The fixture set must never silently shrink — a deleted family fixture
    would take its whole cross-modality net with it."""
    families = {_load_media(k)["family"] for k in _media_variant_keys()}
    expected = {
        "google_image",
        "google_video",
        "openai_image",
        "openai_video",
        "replicate_image",
        "replicate_video",
        "together_image",
        "together_video",
        "xai_image",
        "xai_video",
    }
    missing = expected - families
    assert not missing, f"media rule fixtures missing for families: {sorted(missing)}"


@pytest.mark.parametrize("media_variant", _media_variant_keys())
def test_chat_configs_never_leak_into_media_bodies(media_variant: str) -> None:
    payload = _load_media(media_variant)
    compiled = _compiled_media(payload)
    declared = _declared_keys(compiled)
    assert compiled.rules, f"{media_variant}: empty rules — the gate would be a no-op"

    failures: list[str] = []
    for config in _all_source_configs():
        ns = SimpleNamespace(**config)
        canonical = canonical_settings_from_config(ns)
        foreign = {
            key for key in canonical if not key.startswith("_") and key not in declared
        }
        try:
            params = BaseMediaGeneration._outbound_params(compiled, ns)
        except Exception as exc:  # noqa: BLE001 — the assertion IS "never raises"
            failures.append(f"RAISED {type(exc).__name__}: {exc} for config={config}")
            continue
        flat = flatten_dotted(params) if any(isinstance(v, dict) for v in params.values()) else params
        leaked = foreign & set(flat)
        if leaked:
            failures.append(f"LEAK foreign key(s) {sorted(leaked)} for config={config}")
            continue
        # The gate is a PURE foreign-key filter: on the declared subset the
        # seam must be byte-identical to the raw resolver (media parity 0-diff).
        clean = {k: v for k, v in canonical.items() if k not in foreign}
        direct, _ = compiled.outbound(clean, context={})
        if params != direct:
            failures.append(
                f"GATE MUTATED DECLARED KEYS for config={config}\n"
                f"  seam  : {json.dumps(params, sort_keys=True, default=str)}\n"
                f"  direct: {json.dumps(direct, sort_keys=True, default=str)}"
            )
    if failures:
        pytest.fail(
            f"{media_variant}: {len(failures)} unsafe chat-config outcomes at the "
            f"media seam:\n" + "\n".join(failures[:_MAX_FAILURES_SHOWN])
        )


@pytest.mark.parametrize("chat_variant", _chat_variant_keys())
def test_media_configs_never_leak_into_chat_bodies(chat_variant: str) -> None:
    payload = load_golden(chat_variant)
    compiled = compiled_from_golden(payload)
    declared = _declared_keys(compiled)
    assert compiled.rules, f"{chat_variant}: empty rules — the gate would be a no-op"

    failures: list[str] = []
    for config in _MEDIA_SOURCE_CONFIGS:
        ns = SimpleNamespace(**config)
        canonical = canonical_settings_from_config(ns)
        canonical.pop("response_format", None)
        foreign = {
            key for key in canonical if not key.startswith("_") and key not in declared
        }
        try:
            params = resolve_outbound_params(ns, compiled)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"RAISED {type(exc).__name__}: {exc} for config={config}")
            continue
        flat = flatten_dotted(params) if any(isinstance(v, dict) for v in params.values()) else params
        leaked = foreign & set(flat)
        if leaked:
            failures.append(f"LEAK foreign key(s) {sorted(leaked)} for config={config}")
    if failures:
        pytest.fail(
            f"{chat_variant}: {len(failures)} unsafe media-config outcomes at the "
            f"chat seam:\n" + "\n".join(failures[:_MAX_FAILURES_SHOWN])
        )


@pytest.mark.parametrize("media_variant", _media_variant_keys())
def test_verbosity_regression_at_every_media_family(media_variant: str) -> None:
    """The exact red-team reproduction: verbosity (a gpt-5 text control) +
    temperature riding on a media config must never reach a media body;
    the declared media keys on the same config must keep working."""
    payload = _load_media(media_variant)
    compiled = _compiled_media(payload)
    ns = SimpleNamespace(
        model=payload["model"],
        verbosity="low",
        temperature=0.7,
        aspect_ratio="16:9",
    )
    params = BaseMediaGeneration._outbound_params(
        compiled, ns, context={"operation": "generate"}
    )
    flat = flatten_dotted(params) if any(isinstance(v, dict) for v in params.values()) else params
    assert "verbosity" not in flat, f"{media_variant}: verbosity leaked into the media body"
    if "verbosity" not in compiled.rules:
        # Foreign everywhere it isn't declared — and it must also never ride
        # through under a renamed provider key.
        assert all("verbosity" not in str(k) for k in flat)
    # FLUX-style families derive width/height from aspect_ratio — the gate must
    # not disturb the declared media keys (the live-check mirror).
    if payload["family"] == "together_image":
        assert "width" in flat and "height" in flat, (
            f"{media_variant}: aspect_ratio stopped producing dimensions — the "
            f"gate touched a declared key (params={flat})"
        )

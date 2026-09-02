"""Generated kind-surface bootstrap (Content IR Wave 1, C2) — parity + host drift.

The bootstrap (``kind_surfaces_generated.py``) is GENERATED from live
``content_ir.kind_surface`` by matrx-frontend's ``pnpm check:shapes:surfaces:refresh``,
which writes this repo's file and the TS twin from ONE run. These tests prove:

1. Cross-runtime parity — the TS twin embeds the byte-identical canonical
   payload (skipped LOUDLY when matrx-frontend is not checked out).
2. Registry↔host reconciliation — every registered surface token this host's
   hard-coded detector literals can fire maps to the SAME kind the registry
   declares (via ``BLOCK_KIND_MAP``). The literals stay until the Wave-2
   enforcement ratchet; this test is what keeps them honest meanwhile.
3. Known host gaps are RATCHETED — a surface the Python host cannot detect at
   all must be in the explicit known-gap set below. A new gap fails loudly;
   closing one requires shrinking the set (visible progress, never silence).
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from matrx_ai.processing.blocks.block_detector import (
    CODE_LANGUAGE_ALIASES,
    SPECIAL_CODE_LANGUAGES,
    detect_json_block_type,
    detect_xml_block_type,
)
from matrx_ai.processing.blocks.envelope import BLOCK_KIND_MAP
from matrx_ai.processing.blocks.kind_surfaces_generated import (
    KIND_SURFACE_BOOTSTRAP_JSON,
    KIND_SURFACE_ENTRIES,
    get_surface_for_fence,
    get_surface_for_json_root_key,
    get_surface_for_tag,
)

AIDREAM_ROOT = Path(__file__).resolve().parents[3]
FE_TWIN = (
    Path(os.environ.get("MATRX_FRONTEND_ROOT", AIDREAM_ROOT.parent / "matrx-frontend"))
    / "features/content-ir/registry/system-surfaces.generated.ts"
)

# Surfaces the PYTHON host currently cannot fire at all (no detector literal).
# Shrink-only: adding a row here is registry↔host drift and needs a ruling.
KNOWN_PYTHON_HOST_GAPS: set[tuple[str, str]] = set()


def test_bootstrap_is_well_formed() -> None:
    assert len(KIND_SURFACE_ENTRIES) > 0
    seen: set[tuple[str, str]] = set()
    for entry in KIND_SURFACE_ENTRIES:
        key = (entry["surface_type"], entry["token"])
        assert key not in seen, f"duplicate surface {key}"
        seen.add(key)
        assert entry["kind"]
        assert entry["parser_strategy"]
        assert entry["token"] == entry["token"].lower()


def test_lookup_helpers_serve_the_table() -> None:
    for entry in KIND_SURFACE_ENTRIES:
        by_type = {
            "xml_tag": get_surface_for_tag,
            "fence_lang": get_surface_for_fence,
            "json_root_key": get_surface_for_json_root_key,
        }.get(entry["surface_type"])
        if by_type is None:
            continue
        assert by_type(entry["token"]) == entry


def test_cross_runtime_parity_with_frontend_twin() -> None:
    if not FE_TWIN.exists():
        message = (
            f"matrx-frontend twin not found at {FE_TWIN} — cross-runtime "
            "kind-surface parity NOT verified (set MATRX_FRONTEND_ROOT)."
        )
        # Same rule as the splitter parity gate: the `kinds-parity` CI job
        # provisions the sibling checkout and sets MATRX_PARITY_REQUIRED=1,
        # where "could not run" is a broken gate rather than an excuse.
        if os.environ.get("MATRX_PARITY_REQUIRED") == "1":
            pytest.fail(
                f"PARITY UNVERIFIED: {message}\n\nMATRX_PARITY_REQUIRED=1 — this run "
                "was declared enforcing. Fix the sibling checkout in the job; never "
                "relax this flag."
            )
        pytest.skip(f"SKIPPED LOUDLY: {message}")
    text = FE_TWIN.read_text(encoding="utf-8")
    match = re.search(r"KIND_SURFACE_BOOTSTRAP_JSON = '([^']*)'", text)
    assert match, "TS twin lost its KIND_SURFACE_BOOTSTRAP_JSON marker"
    assert match.group(1) == KIND_SURFACE_BOOTSTRAP_JSON, (
        "TS and Python kind-surface bootstraps embed DIFFERENT payloads — "
        "regenerate BOTH from one `pnpm check:shapes:surfaces:refresh` run"
    )


def _python_host_block_type(surface_type: str, token: str) -> str | None:
    """The block type this host's hard-coded literals produce for a token."""
    if surface_type == "fence_lang":
        normalized = CODE_LANGUAGE_ALIASES.get(token, token)
        return normalized if normalized in SPECIAL_CODE_LANGUAGES else None
    if surface_type == "xml_tag":
        detected = detect_xml_block_type(f"<{token}>")
        return detected[0] if detected else None
    if surface_type == "json_root_key":
        return detect_json_block_type('{"%s": {}}' % token)
    return None  # tool_name etc. — no markdown host


def test_host_literals_agree_with_the_registry() -> None:
    """Every bootstrap surface is fireable by this host's literals (or is a
    ratcheted known gap), and the block type it fires converges to the SAME
    kind the registry declares."""
    problems: list[str] = []
    live_gaps: set[tuple[str, str]] = set()

    for entry in KIND_SURFACE_ENTRIES:
        surface_type = entry["surface_type"]
        token = entry["token"]
        if surface_type not in ("fence_lang", "xml_tag", "json_root_key"):
            continue
        block_type = _python_host_block_type(surface_type, token)
        if block_type is None:
            live_gaps.add((surface_type, token))
            continue
        mapped_kind = BLOCK_KIND_MAP.get(block_type)
        if mapped_kind is None:
            problems.append(
                f"({surface_type}, {token!r}) fires block type {block_type!r} which has "
                "no BLOCK_KIND_MAP entry — the host detects it but never converges it"
            )
        elif mapped_kind != entry["kind"]:
            problems.append(
                f"({surface_type}, {token!r}) → block {block_type!r} → BLOCK_KIND_MAP says "
                f"{mapped_kind!r} but kind_surface says {entry['kind']!r}"
            )

    unexpected_gaps = live_gaps - KNOWN_PYTHON_HOST_GAPS
    healed_gaps = KNOWN_PYTHON_HOST_GAPS - live_gaps
    if unexpected_gaps:
        problems.append(
            f"NEW Python host detection gap(s): {sorted(unexpected_gaps)} — a registered "
            "surface this host cannot fire; port the detector literal or get a ruling "
            "and add it to KNOWN_PYTHON_HOST_GAPS"
        )
    if healed_gaps:
        problems.append(
            f"KNOWN_PYTHON_HOST_GAPS is stale — now detectable: {sorted(healed_gaps)}; "
            "delete the healed entries (shrink-only ratchet)"
        )

    assert not problems, "\n".join(problems)

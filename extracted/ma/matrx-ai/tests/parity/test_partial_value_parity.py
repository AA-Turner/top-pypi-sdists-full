"""PARTIAL-VALUE parity — do both runtimes agree on what a user sees mid-stream?

The detection gate (``test_ts_parser_parity.py``) pins that Python and TypeScript
assign the same block TYPE. That was enough while structure only rendered when it
finished. Now that it renders WHILE it streams, there is a second question, and
nothing on either side alone can answer it: **two production paths each produce a
progressive value, and if they disagree the same answer renders differently
depending on which wire shape the server happened to use.**

  * Python   — the ``metadata.__ir_partial`` channel (``StreamBlockProcessor``),
               live whenever the server sends ``render_block`` events.
  * Frontend — ``StreamBlockAccumulator``, which parses raw ``chunk`` text itself
               and emits blocks carrying a STREAMING ``metadata.__ir`` envelope.

WHAT THIS GATE ASSERTS (and deliberately does not)
--------------------------------------------------
1. **Both runtimes saw the same JSON.** Python's final partial value, restricted
   to the SOURCE vocabulary, must equal the frontend's completed value. This is
   the assertion that would catch a closer bug corrupting data — a partial that
   is valid JSON but not the model's JSON.
2. **They agree on where structure exists at all.** A document with nothing
   structured produces zero on BOTH sides.
3. **The known asymmetry is ASSERTED, never merely tolerated** (§4 below).

It asserts NOTHING about kind NAMING. Resolving a kind's schema needs the live
registry, which this harness has no credentials for (the frontend logs a warm-load
failure and degrades to ``kindState: "raw"`` by design). A gate that asserted kind
naming here would be measuring its own environment, so that question stays open
and is recorded as such rather than silently assumed.

Run:  uv run pytest packages/matrx-ai/tests/parity
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import pytest

from .harness import BridgeUnavailable, frontend_root

# ---------------------------------------------------------------------------
# §4 — THE DECLARED ASYMMETRY
# ---------------------------------------------------------------------------
#
# The frontend's own chunk path renders NOTHING structured while a legacy-JSON
# kind streams: its `content_ir.kind_surface` rows for these families carry
# `"streaming": false` (see matrx-frontend
# `features/content-ir/registry/system-surfaces.generated.ts`), so every
# streaming emission carries an EMPTY value and `kindState: "pending_kind"`
# until the region closes.
#
# That is a frontend RULING, not drift — and it is the whole justification for
# the `__ir_partial` channel: for these kinds, server-side detection is the only
# thing that can render them progressively at all.
#
# It is asserted rather than ignored, exactly like the detection gate's
# EXPECTED_DIVERGENT_FIXTURES: the day the frontend flips those surfaces to
# streaming, TWO progressive renders exist for one region and someone must
# reconcile them deliberately. This test failing is that conversation starting.
FE_EMITS_NO_STREAMING_VALUE_FOR_LEGACY_JSON = (
    "matrx-frontend marks legacy-JSON kind surfaces streaming:false, so its own "
    "accumulator shows no structure until the region closes — which is why the "
    "server's __ir_partial channel exists for these kinds"
)

# ---------------------------------------------------------------------------
# §4b — THE SECOND REGIME: a SELF-DECLARING root region (added 2026-08-23)
# ---------------------------------------------------------------------------
#
# A kind-bound agent (`ai.agent.produce` -> `response_format_for_kind`) streams a
# BARE JSON document whose FIRST key is `__kind`. That is not a legacy-JSON kind
# and the asymmetry above does not describe it: BOTH runtimes see structure while
# it streams, because both can read the discriminator the model itself wrote.
#
# Two PRODUCERS is not two RENDERS, and the reconciliation is already made rather
# than owed: STREAMING_PARTIAL_KINDS.md §7b rule 4 — a lane whose server block
# scope is open is marked `block_shadowed` and STOPS feeding its own accumulator,
# precisely so one region is never rendered twice under two sets of block ids. So
# exactly one of the two is live on any given surface: the accumulator in chat,
# the server's channel on a workflow run page.
#
# What must therefore hold for these documents is the OPPOSITE of §4 — both sides
# produce structure — plus the value agreement asserted for every document. The
# day only one side does, the surface that lost it renders raw JSON.
BOTH_RUNTIMES_RENDER_A_SELF_DECLARING_ROOT = (
    "a __kind-first bare region is readable by BOTH runtimes; §7b rule 4's "
    "block_shadowed flag is what keeps two producers from becoming two renders"
)

# Pre-recognition is FIRST-KEY only (`block_detector.root_kind_declaration`): a
# `__kind` that arrives LATE is deliberately not announced, because announcing a
# kind after the reader has already watched the raw text is not pre-recognition.
# The frontend's own parser has no such rule — it resolves `__kind` at any depth
# and any position. That divergence is intentional and costs nothing: on a lane
# where the server announces, the frontend parser is shadowed and not running.
PY_DOES_NOT_ANNOUNCE_A_LATE_KIND_KEY = (
    "pre-recognition is first-key only; the frontend parser resolves __kind "
    "anywhere, and on a shadowed lane it is not the renderer anyway"
)


def _self_declaring_root(document: str) -> str | None:
    """The kind a document declares on its FIRST key, via the LIVE recognizer."""
    from matrx_ai.processing.blocks.block_detector import root_kind_declaration

    return root_kind_declaration(document)


def _declares_kind_anywhere(document: str) -> bool:
    return '"__kind"' in document

# Keys ``adapt_block_data`` ADDS on top of the model's own JSON, mapping the
# source vocabulary into the kind's. The frontend does not adapt (its own
# ruling), so they are excluded from the value comparison by name — never by a
# blanket "ignore extra keys", which would hide a real divergence.
PY_ADAPTER_ADDED_KEYS: dict[str, str] = {
    "__kind": "the discriminator the server stamps; the FE reads it from the surface map",
    "title": "quiz_set canonical title, adapted from quiz_title",
    "questions": "quiz_set canonical question list, adapted from multiple_choice",
}


def _bridge() -> Path:
    return (
        Path(__file__).resolve().parents[4]
        / "packages/matrx-ai/matrx_ai/processing/blocks/tests/ts_bridge/stream_partials.ts"
    )


def _run_frontend(documents: dict[str, str], chunk: int) -> dict[str, list[dict[str, Any]]]:
    root = frontend_root()
    if root is None:
        raise BridgeUnavailable(
            "matrx-frontend checkout not found — partial-value parity is "
            "UNVERIFIED, never 'passing'. Set MATRX_FRONTEND_ROOT."
        )
    script = _bridge()
    if not script.is_file():
        raise BridgeUnavailable(f"the partial-value bridge is missing at {script}")

    with tempfile.TemporaryDirectory() as tmp:
        job = Path(tmp) / "job.json"
        out = Path(tmp) / "out.json"
        job.write_text(json.dumps({"chunk": chunk, "documents": documents}))
        # Node resolves packages from the importing file's directory, not from
        # cwd. Stage the cross-repo bridge inside the frontend checkout so both
        # its node_modules packages and tsconfig aliases resolve in CI.
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ts", dir=root, delete=False
        ) as staged_file:
            staged_file.write(script.read_text())
            staged = Path(staged_file.name)
        try:
            proc = subprocess.run(
                [
                    "npx", "tsx", "--tsconfig", str(root / "tsconfig.json"),
                    str(staged), "--in", str(job), "--out", str(out),
                ],
                cwd=root, capture_output=True, text=True, timeout=300,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            raise BridgeUnavailable(f"could not execute the TS bridge: {exc}") from exc
        finally:
            staged.unlink(missing_ok=True)
        if not out.is_file():
            raise BridgeUnavailable(
                f"the TS bridge produced no output (exit {proc.returncode}).\n"
                f"stderr:\n{proc.stderr[-2000:]}"
            )
        return json.loads(out.read_text())


def _generator():
    import importlib.util
    import sys

    script = Path(__file__).resolve().parents[4] / "scripts/generate_partial_kind_fixture.py"
    spec = importlib.util.spec_from_file_location("_pk_fixture_parity", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_pk_fixture_parity"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def measured():
    """Both runtimes, same documents, same chunk size. Real execution, both sides."""
    generator = _generator()
    try:
        frontend = _run_frontend(generator.DOCS, generator.CHUNK)
    except BridgeUnavailable as exc:
        pytest.skip(f"PARTIAL-VALUE PARITY UNVERIFIED — {exc}")

    python_side = generator.build()["fixtures"]
    return generator, python_side, frontend


def _python_partial_values(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r["event"]["root"]["value"] for r in rows if r["event"]["state"] == "partial"]


def _source_vocabulary(value: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in value.items() if k not in PY_ADAPTER_ADDED_KEYS}


def _canonical(block_type: str, value: dict[str, Any]) -> dict[str, Any]:
    """The kind's OWN vocabulary — the part a component actually renders.

    🚨 Why this exists (2026-08-22). The comparison used to be
    "python's partial minus the adapter's additions == the frontend's value",
    which silently assumed Python's partial stays in the MODEL's key spelling.
    That held only while a strict parser refused the document: the moment
    ``parse_quiz`` was fixed to accept the shape models really write (no ids,
    answer-as-text), Python's preferred path kicked in — ``_partial_value``
    documents that it PREFERS the real parser precisely so the provisional
    value and the final value are the same object — and the leftover keys
    became the parser's normalised twins (``multipleChoice``,
    ``correctAnswer: 0``, ``id``).

    Nothing the reader sees changed: ``adapt_block_data`` reads both spellings
    and both answer forms, so the CANONICAL keys are identical either way.
    Comparing the leftovers was therefore measuring the passthrough, not the
    render — so the gate now compares what renders, on both sides, through the
    one deterministic projection. Still two independent parsers, still fails
    the moment either side loses or invents an element (proven by mutating the
    closer). Blocks with no adapter case are unchanged: the projection is
    identity and the source-vocabulary comparison stands.
    """
    from matrx_ai.processing.blocks.envelope import adapt_block_data

    adapted = adapt_block_data(block_type, value)
    # `__kind` is the SERVER's discriminator stamp, never something the model
    # wrote — the frontend reads it from its own surface map. Comparing it
    # would only ever assert that Python stamps what Python stamps.
    canonical = {
        k: v
        for k, v in adapted.items()
        if k in PY_ADAPTER_ADDED_KEYS and k != "__kind"
    }
    return canonical or {
        k: v for k, v in _source_vocabulary(adapted).items() if k != "__kind"
    }


def _block_type_for(rows: list[dict[str, Any]]) -> str:
    """The detector's block type for this document, from the kind it announced."""
    from matrx_ai.processing.blocks.envelope import BLOCK_KIND_MAP

    for row in rows:
        kind = row["event"].get("root", {}).get("kind") or row["event"].get("kind")
        for block_type, mapped in BLOCK_KIND_MAP.items():
            if mapped == kind:
                return block_type
    return ""


def test_both_runtimes_saw_the_same_json(measured):
    """The value assertion: a partial is incomplete, never a DIFFERENT document.

    Python closes truncated JSON to build its partials; the frontend parses the
    same text with its own tokenizer. At the end of the region their values must
    agree on everything the model actually wrote — compared in the kind's own
    vocabulary, which is what a component renders (see ``_canonical``).
    """
    _generator_module, python_side, frontend = measured

    compared = 0
    for name, rows in python_side.items():
        values = _python_partial_values(rows)
        if not values:
            continue
        completed = [e for e in frontend.get(name, []) if e["status"] == "complete"]
        if not completed:
            continue

        block_type = _block_type_for(rows)
        python_final = _canonical(block_type, values[-1])
        frontend_final = _canonical(block_type, completed[-1]["value"])
        assert python_final == frontend_final, (
            f"{name}: the two runtimes disagree about the JSON the model sent.\n"
            f"  python (source vocabulary): {json.dumps(python_final, sort_keys=True)[:400]}\n"
            f"  frontend:                   {json.dumps(frontend_final, sort_keys=True)[:400]}\n"
            "One of them is showing the user data the model did not write."
        )
        compared += 1

    assert compared, "no document produced a comparable value — the gate proved nothing"


def test_both_runtimes_agree_on_where_structure_exists(measured):
    """Neither side may invent structure the other never saw.

    Catches a producer that starts announcing kinds for prose — the failure mode
    that would put a skeleton on screen for a paragraph.
    """
    _generator_module, python_side, frontend = measured

    documents = _generator_module.DOCS

    for name, rows in python_side.items():
        python_has = bool(_python_partial_values(rows))
        frontend_has = any(e["value"] for e in frontend.get(name, []))
        document = documents.get(name, "")
        if (
            not python_has
            and _declares_kind_anywhere(document)
            and _self_declaring_root(document) is None
        ):
            # The LATE-`__kind` case: a NAMED divergence, not drift. Assert it
            # in both directions so it cannot quietly become something else.
            assert frontend_has, (
                f"{name}: neither runtime found structure in a document that "
                "declares a kind — the frontend parser stopped resolving a late "
                f"__kind. Recorded: {PY_DOES_NOT_ANNOUNCE_A_LATE_KIND_KEY}"
            )
            continue
        assert python_has == frontend_has, (
            f"{name}: python {'found' if python_has else 'found NO'} structure but "
            f"the frontend {'found' if frontend_has else 'found NO'} structure — "
            "the same document renders structurally on one path and not the other"
        )


def test_the_declared_asymmetry_is_still_true(measured):
    """An ASSERTED divergence, never a tolerated one.

    The frontend shows nothing structured while a legacy-JSON kind streams
    (surfaces are `streaming: false`); the server's partial channel does. If
    that ever stops being true, two progressive renders exist for one region and
    the reconciliation is a decision — so this fails loudly instead of quietly
    resolving itself.
    """
    _generator_module, python_side, frontend = measured

    documents = _generator_module.DOCS

    checked = 0
    self_declaring_checked = 0
    for name, rows in python_side.items():
        if not _python_partial_values(rows):
            continue
        streaming = [e for e in frontend.get(name, []) if e["status"] == "streaming"]
        if not streaming:
            continue
        populated = [e for e in streaming if e["value"]]

        if _self_declaring_root(documents.get(name, "")) is not None:
            # §4b: the OTHER regime. Here the frontend SHOULD render structure
            # while it streams — asserted positively, so this regime cannot
            # silently degrade into the legacy one and start showing raw JSON.
            self_declaring_checked += 1
            assert populated, (
                f"{name}: the frontend renders NOTHING structured while a "
                "__kind-first region streams, so a chat surface shows raw JSON "
                f"until it closes.\n\nRecorded: "
                f"{BOTH_RUNTIMES_RENDER_A_SELF_DECLARING_ROOT}"
            )
            continue

        checked += 1
        assert not populated, (
            f"{name}: the frontend NOW emits structured values while streaming "
            f"({len(populated)} of {len(streaming)} emissions) — the recorded "
            f"asymmetry has changed.\n\nRecorded reason: "
            f"{FE_EMITS_NO_STREAMING_VALUE_FOR_LEGACY_JSON}\n\n"
            "Two progressive renders now exist for one region. Decide which one "
            "the user sees and reconcile the wire contract: "
            "common-docs/systems/content-ir-system/STREAMING_PARTIAL_KINDS.md"
        )

    assert checked, (
        "no document exercised the asymmetry — this test would pass vacuously, "
        "which is exactly the failure it exists to prevent"
    )
    assert self_declaring_checked, (
        "no document exercised the SELF-DECLARING regime (§4b) — the bound-agent "
        "shape every ai.agent.produce step emits would be unmeasured"
    )


def test_only_the_server_renders_these_kinds_progressively(measured):
    """The channel's own justification, measured rather than asserted in prose.

    If this ever fails because Python stopped producing partials, progressive
    rendering for legacy-JSON kinds is GONE on every surface — and nothing else
    in either repo's suite would notice.
    """
    _generator_module, python_side, _frontend = measured

    progressive = {
        name: len(_python_partial_values(rows)) for name, rows in python_side.items()
    }
    assert progressive.get("clean_finish", 0) > 5, (
        "the server no longer streams a structured answer progressively "
        f"(clean_finish produced {progressive.get('clean_finish', 0)} partials) — "
        "the frontend's own path cannot do it for these kinds, so the user is "
        "back to staring at a loader"
    )

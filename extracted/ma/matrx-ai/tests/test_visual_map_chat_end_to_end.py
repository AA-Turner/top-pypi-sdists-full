"""Model output → stored checked value, for the six live chat subjects, through the REAL diagram engine.

2026-10-24 live (verify-final-A, server 4b26943bec72): 0 of 6 subjects drew in chat. Two breaks:
1. S1: the strict decoder forced ``"spec": {}`` (unified_client ``forced_empty_maps``); the loop then checked
   only the identity it fills and answered "/ must have required property 'meta'" — an empty spec must be
   named as empty, never "checked".
2. S4/S5: the model wrote ``diagram_type`` "state" / "data_flow" and lifecycle ``schema_version`` 1. Both
   are the engine's constants, frozen to the repairer; three repair answers set them and every one was
   refused, so the error could never clear.

Each subject is the exact value the loop received live (``fixtures/visual_map_chat_live_drafts.json``),
inside the live ``<artifact type="visual_map">`` wrapper. The engine is the real ``@ai-matrx/diagrams``
validate (node); the repairer answers an empty patch, so everything that clears is the server's own work.
"""

from __future__ import annotations

import asyncio
import contextvars
import json
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.orchestrator import visual_map_repair as vmr
from matrx_ai.orchestrator.visual_map_repair import (
    CallPointResult,
    content_inventory,
    find_visual_maps,
)

ROOT = Path(__file__).resolve().parents[3]
ENGINE = ROOT / "apps/shared/diagrams/src/index.mjs"
DRAFTS = json.loads((Path(__file__).parent / "fixtures/visual_map_chat_live_drafts.json").read_text())
S1_SPEC = json.loads((ROOT / "apps/shared/diagrams/test/fixtures/subjects/S1/archify/spec.json").read_text())
CURRENT_VERSION = {"lifecycle": 3, "workflow": 2}

pytestmark = pytest.mark.skipif(shutil.which("node") is None or not ENGINE.exists(),
                                reason="needs node and the diagram engine source")

_NODE = """
import * as m from %s;
let raw = ""; for await (const c of process.stdin) raw += c;
const {type, spec} = JSON.parse(raw);
const r = await m.validate(type, spec);
process.stdout.write(JSON.stringify(r.diagnostics ?? []));
"""


def engine_validate(type_: str, spec: dict[str, Any]) -> list[dict[str, Any]]:
    out = subprocess.run(["node", "--input-type=module", "-e", _NODE % json.dumps(ENGINE.as_uri())],
                         input=json.dumps({"type": type_, "spec": spec}), capture_output=True, text=True,
                         timeout=60, check=True)
    return json.loads(out.stdout)


class RealEngine:
    def __init__(self) -> None:
        self.validated: list[dict[str, Any]] = []
        self.delivered: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []

    async def read_knobs(self, *, organization_id, user_id):
        return {"repair_max_rounds": 4, "repair_stall_rounds": 1, "quality": "showcase", "repair_group_max": 6,
                "repair_model": ""}

    async def schema_version(self, type):  # noqa: A002
        return CURRENT_VERSION.get(type, 1)

    async def validate(self, type, spec, *, quality):  # noqa: A002
        self.validated.append(json.loads(json.dumps(spec)))
        diags = engine_validate(type, spec)
        return {"ok": not any(d.get("severity") == "error" for d in diags), "diagnostics": diags}

    async def deliver(self, type, spec, *, organization_id, subject_ref, round, quality):  # noqa: A002
        diags = engine_validate(type, spec)
        errors = [d for d in diags if d.get("severity") == "error"]
        self.delivered.append((json.loads(json.dumps(spec)), diags))
        return {"ok": not errors, "verified": not errors, "issues": len(errors), "diagnostics": diags,
                "inspection_id": f"insp-{len(self.delivered)}", "receipt": {"viewBox": [0, 0, 1124, 600]},
                "measured_diagnostics": []}

    async def persist_round(self, **_):
        return "row"

    async def repair(self, provision, *, organization_id):
        return CallPointResult(bound=False)

    async def review(self, provision, *, organization_id):
        return CallPointResult(bound=False)


def _subjects() -> dict[str, dict[str, Any]]:
    s1 = {"__kind": "visual_map", "type": "architecture", "spec": S1_SPEC, "verified": False, "issues": 0}
    return {"S1": s1, **{k: v for k, v in DRAFTS.items() if k.startswith("S")}}


def _gate(value: dict[str, Any], monkeypatch) -> tuple[Any, RealEngine, Any]:
    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters import SilentEmitter

    import matrx_ai._ext as ext

    part = SimpleNamespace(
        text=f'<artifact type="visual_map" id="a1" version="1" title="Visual Map 1">\n{json.dumps(value)}\n</artifact>',
        metadata={})
    monkeypatch.setattr(vmr, "_assistant_text_parts", lambda *_: [part])

    async def no_change(provision):
        return '{"changes": []}'

    monkeypatch.setattr(vmr, "authoring_model_repairer", lambda _req: no_change)
    engine = RealEngine()

    class Emitter:
        async def send_info(self, payload):
            pass

        async def send_warning(self, payload):
            pass

    def _in_ctx():
        set_app_context(AppContext(emitter=SilentEmitter(), user_id="u", organization_id="org", request_id="req"))
        ext._registry["visual_map_delivery"] = engine
        try:
            request = SimpleNamespace(config=SimpleNamespace(messages=[]), request_id="req")
            return asyncio.run(vmr.visual_map_gate(request, None, SimpleNamespace(emitter=Emitter())))
        finally:
            ext._registry.pop("visual_map_delivery", None)

    outcomes = contextvars.copy_context().run(_in_ctx)
    return part, engine, outcomes


@pytest.mark.parametrize("subject", ["S1", "S2", "S3", "S4", "S5", "S6"])
def test_the_stored_turn_holds_the_full_checked_spec(subject: str, monkeypatch) -> None:
    value = _subjects()[subject]
    draft = content_inventory(value["spec"])
    part, engine, outcomes = _gate(value, monkeypatch)

    assert outcomes and engine.validated, f"{subject}: nothing was checked"
    first = engine.validated[0]
    assert set(first) - {"schema_version", "diagram_type"}, f"{subject}: the engine got the identity only: {first}"
    assert content_inventory(first) == draft, f"{subject}: the engine did not get what the model drew"

    stored = find_visual_maps(part.text)
    assert part.text.startswith("<artifact") and len(stored) == 1, part.text[:200]
    checked = stored[0][2]
    delivered_spec, delivered_diags = engine.delivered[-1]
    assert checked["spec"] == delivered_spec, f"{subject}: the stored spec is not the spec that was checked"
    assert content_inventory(checked["spec"]) == draft, f"{subject}: the stored turn lost drawn content"
    assert checked["inspection_id"] and isinstance(checked["verified"], bool) and isinstance(checked["issues"], int)
    # The identity is the engine's constant; it never survives as an error.
    identity_errors = [d for d in delivered_diags if d.get("code") == "schema/const"
                       and str((d.get("subject") or {}).get("path")) in ("/schema_version", "/diagram_type")]
    assert not identity_errors, f"{subject}: identity still wrong after checking: {identity_errors}"
    assert checked["spec"]["diagram_type"] == value["type"]


def test_an_empty_spec_is_named_empty_not_checked(monkeypatch) -> None:
    """The live S1 payload: the strict decoder's ``"spec": {}``."""
    value = {"__kind": "visual_map", "type": "architecture", "spec": {}, "verified": False, "issues": 0}
    part, engine, outcomes = _gate(value, monkeypatch)
    assert engine.validated == [], f"an empty spec was 'checked' as if it were a diagram: {engine.validated}"
    assert outcomes[0].stop_reason == "empty"
    assert any("no diagram content" in n for n in outcomes[0].notes), outcomes[0].notes

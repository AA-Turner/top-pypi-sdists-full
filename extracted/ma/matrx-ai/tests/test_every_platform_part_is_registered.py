"""FORCING GUARD — every piece of text the platform adds is registered, labeled, and visible.

Defects 25 + 27 (2026-10-18): the mid-loop "SYSTEM NOTICE (not from the user)" turns, the
live-plan reminder and the Kind Directives guidance were code-only text absent from every
census, so no author could see that they exist. Each now has an entry in
``matrx_ai.config.platform_parts`` (shown in the Builder Model view), and:

1. every ``host_authored_user_turn(..., reason=...)`` in matrx_ai names a registered reason;
2. on a real wire request (Anthropic + a Chat-Completions provider), the labeled platform
   parts are EXACTLY the text the author did not write and the person did not type:
   removing them leaves only the authored system text and her message.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.platform_parts import (
    PLATFORM_PARTS,
    mid_loop_reason_registered,
    platform_parts_in_request,
    without_platform_parts,
)
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.testing.profile_factory import make_profile

PKG = Path(__file__).resolve().parents[1] / "matrx_ai"
AUTHORED = "You are the receiving desk. Marker AUTH-1."
TYPED = "TYPED-1 Please send the line."


def _reasons() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for path in PKG.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", None)) == "host_authored_user_turn"):
                continue
            for kw in node.keywords:
                if kw.arg != "reason":
                    continue
                where = f"{path.relative_to(PKG)}:{node.lineno}"
                if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    found.append((where, kw.value.value))
                elif isinstance(kw.value, ast.JoinedStr) and isinstance(kw.value.values[0], ast.Constant):
                    found.append((where, str(kw.value.values[0].value)))
                # reason=self.reason (config/host_turn.py) is the CALLER's host turn (a request field).
    return found


def test_every_mid_loop_host_turn_reason_is_registered() -> None:
    reasons = _reasons()
    assert len(reasons) >= 8, reasons
    missing = [(w, r) for w, r in reasons if not mid_loop_reason_registered(r)]
    assert not missing, f"host turns with no registered platform part: {missing}"


@pytest.mark.parametrize(
    ("module", "cls", "wire_format"),
    [
        ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
        ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
        ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ],
)
def test_labeled_platform_parts_are_exactly_the_unattributed_text(module: str, cls: str, wire_format: str) -> None:
    import importlib

    system = SystemInstruction(base_instruction=AUTHORED, include_date=True)
    system.inject_context_block("<org_catalog>\nAcme (active)\n</org_catalog>")
    config = UnifiedConfig(
        model="m",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text=TYPED)])]),
    )
    config.system_instruction = system
    config.messages.attach_turn_context("<live_date>It is now 09:00.</live_date>", slot="live_date")
    translator = getattr(importlib.import_module(module), cls)()
    request = translator.build_request(config, make_profile(model_name="m", wire_format=wire_format))
    if cls == "GoogleTranslator":
        request = {"contents": request["contents"], "system": str(request["config"].system_instruction)}

    parts = platform_parts_in_request(request)
    ids = sorted({p["id"] for p in parts})
    assert ids == ["current_date", "organization_catalog", "turn_context"], ids
    for p in parts:
        assert p["label"] == PLATFORM_PARTS[p["id"]].label and p["source"]

    from matrx_ai.config.platform_parts import _strings

    left = [
        without_platform_parts(text).strip()
        for where, text in _strings(request)
        if not where.startswith("tools") and where.split(".")[-1] in ("text", "content", "system")
    ]
    left = [t for t in left if t]
    assert sorted(left) == sorted([AUTHORED, TYPED]), left

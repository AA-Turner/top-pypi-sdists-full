from __future__ import annotations

from pathlib import Path


def test_raw_anthropic_sdk_is_confined_to_provider_adapter():
    package_root = Path(__file__).parents[1] / "matrx_ai"
    violations: list[str] = []
    for path in package_root.rglob("*.py"):
        relative = path.relative_to(package_root)
        if relative.parts[:2] == ("providers", "anthropic"):
            continue
        source = path.read_text(encoding="utf-8")
        if "AsyncAnthropic" in source or "anthropic.AsyncAnthropic" in source:
            violations.append(str(relative))

    assert violations == [], (
        "Raw Anthropic SDK callers bypass routing and cost capture; route them "
        f"through execute_ai_request instead: {violations}"
    )

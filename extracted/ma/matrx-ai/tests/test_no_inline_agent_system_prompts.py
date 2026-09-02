from __future__ import annotations

from pathlib import Path


def test_inline_agent_system_prompts_are_confined_to_infrastructure():
    package_root = Path(__file__).parents[1] / "matrx_ai"
    allowlist = {
        Path("agents/definition.py"),
        Path("agents/resolver.py"),
        Path("db/_cx_managers_impl.py"),
        Path("graph_nodes/_strict_json.py"),
        Path("graph_nodes/agent_loop_actions.py"),
        Path("graph_nodes/chat_action.py"),
        Path("graph_nodes/llm_action.py"),
        Path("orchestrator/requests.py"),
    }
    violations: list[str] = []
    for path in package_root.rglob("*.py"):
        relative = path.relative_to(package_root)
        if relative in allowlist:
            continue
        source = path.read_text(encoding="utf-8")
        if "UnifiedConfig.from_dict(" in source and "system_instruction" in source:
            violations.append(str(relative))

    assert violations == [], (
        "Inline agent system prompts are invisible to the admin UI, unversioned, "
        "and unmanageable by the slots system. "
        "create a builtin agent, declare a Mandate, and run it through the canonical "
        f"agent system instead: {violations}"
    )

"""An agent's system prompt is authored in the platform, never typed into code.

WHY THIS WAS REWRITTEN (2026-09-11). The old version certified GREEN the exact
files the mandate-guard audit was about, in two independent ways:

1. It HAND-ALLOWLISTED four ``graph_nodes/*`` files — and they did not belong
   there. They never author a prompt: they FORWARD one their caller or the
   workflow author supplied (``inputs.system_instruction``). The allowlist was
   papering over a detector that could not tell "writes a prompt" from
   "passes a prompt along", and in doing so it also silenced anything else
   those files might ever do.
2. Its detector was the literal token pair ``"UnifiedConfig.from_dict(" in
   source and "system_instruction" in source``. ``extract_action.py`` builds
   its system prompt as an f-string and ships it as a ``{"role": "system"}``
   message — no ``system_instruction`` token anywhere — so the one file in the
   package that really does author an agent prompt in code was invisible to a
   guard whose whole job was to find it.

The detector now reads the AST and asks the real question: does this file put
AUTHORED TEXT — a string literal or f-string — into the system channel of a
request it builds? Forwarding a value is fine and always was; typing the prompt
is the defect. That change is what let the four allowlist entries be deleted
rather than trusted.
"""

from __future__ import annotations

import ast
from pathlib import Path

#: Infrastructure that legitimately constructs a system channel: the agent
#: runtime itself, the request model, and the conversation manager. Each is a
#: place the platform's OWN authored prompt is assembled from the database, not
#: a place someone typed one.
ALLOWLIST = {
    Path("agents/definition.py"),
    Path("agents/resolver.py"),
    Path("db/_cx_managers_impl.py"),
    Path("orchestrator/requests.py"),
}

#: Known inline prompts still in the package. THIS LIST ONLY SHRINKS — each row
#: is a D20 conversion item: the prompt belongs on a builtin agent behind a
#: Mandate, so an admin can read it, version it and rebind it.
#: ``graph_nodes/extract_action.py`` — the extraction analyzer instruction,
#: invisible to this guard until 2026-09-11 because it carries no
#: ``system_instruction`` token. Its runtime call is now held by
#: ``workflow.step_intelligence``; the PROMPT still has to move.
PENDING_CONVERSION = {
    Path("graph_nodes/extract_action.py"),
}

_AUTHORED = (ast.Constant, ast.JoinedStr)


def _is_authored_text(node: ast.AST) -> bool:
    """A string literal or f-string — text a developer typed, not a value passed."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, str) and node.value.strip() != ""
    if isinstance(node, ast.JoinedStr):
        return True
    if isinstance(node, ast.BinOp):  # "a" + variable, and friends
        return _is_authored_text(node.left) or _is_authored_text(node.right)
    return False


def _authors_a_system_prompt(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        # system_instruction="You are ..." as a keyword or a dict entry
        if isinstance(node, ast.keyword) and node.arg == "system_instruction":
            if _is_authored_text(node.value):
                return True
        if isinstance(node, ast.Dict):
            pairs = {
                key.value: value
                for key, value in zip(node.keys, node.values, strict=False)
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            }
            if "system_instruction" in pairs and _is_authored_text(
                pairs["system_instruction"]
            ):
                return True
            role = pairs.get("role")
            if (
                isinstance(role, ast.Constant)
                and role.value == "system"
                and "content" in pairs
                and _is_authored_text(pairs["content"])
            ):
                return True
        # A name that IS the system prompt, assigned authored text:
        #   system_prompt = f"You are a strict data extraction analyzer..."
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            if value is None:
                continue
            for target in targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id in {"system_prompt", "system_text", "system_message"}
                    and _is_authored_text(value)
                ):
                    return True
    return False


def _offenders() -> list[str]:
    package_root = Path(__file__).parents[1] / "matrx_ai"
    found: list[str] = []
    for path in sorted(package_root.rglob("*.py")):
        relative = path.relative_to(package_root)
        if relative in ALLOWLIST or relative in PENDING_CONVERSION:
            continue
        source = path.read_text(encoding="utf-8")
        if "UnifiedConfig.from_dict(" not in source and "UnifiedConfig(" not in source:
            continue
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:  # a file we cannot read is never a silent pass
            found.append(f"{relative} (unparseable)")
            continue
        if _authors_a_system_prompt(tree):
            found.append(str(relative))
    return found


def test_inline_agent_system_prompts_are_confined_to_infrastructure():
    violations = _offenders()
    assert violations == [], (
        "Inline agent system prompts are invisible to the admin UI, unversioned, "
        "and unmanageable by the mandate system. Create a builtin agent, declare a "
        "Mandate, and run it through the canonical agent system instead: "
        f"{violations}"
    )


def test_the_detector_can_actually_fail():
    """A guard nobody has seen fail is not a guard.

    Both shapes must be caught: the keyword the old detector looked for, and the
    ``{"role": "system"}`` message it was blind to — which is how the package's
    one real inline prompt hid for months.
    """
    keyword_shape = ast.parse(
        'config = UnifiedConfig.from_dict({"system_instruction": "You are a judge."})'
    )
    message_shape = ast.parse(
        'msgs = [{"role": "system", "content": f"You are a strict analyzer. {x}"}]'
    )
    assigned_shape = ast.parse('system_prompt = "You are a strict analyzer."')
    forwarded = ast.parse(
        'config = UnifiedConfig.from_dict({"system_instruction": inputs.system})'
    )
    forwarded_message = ast.parse('msgs = [{"role": "system", "content": system_text}]')

    assert _authors_a_system_prompt(keyword_shape)
    assert _authors_a_system_prompt(message_shape)
    assert _authors_a_system_prompt(assigned_shape)
    assert not _authors_a_system_prompt(forwarded), "forwarding a value is not authoring"
    assert not _authors_a_system_prompt(forwarded_message)


def test_pending_conversion_only_shrinks():
    """Every pending row must still exist and still be an inline prompt.

    A conversion list that keeps naming a file which no longer offends turns
    into decoration; one that keeps naming a deleted file hides a real
    regression somewhere else.
    """
    package_root = Path(__file__).parents[1] / "matrx_ai"
    for relative in sorted(PENDING_CONVERSION):
        path = package_root / relative
        assert path.exists(), (
            f"{relative} is on the inline-prompt conversion list but no longer exists — "
            "delete the row."
        )
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert _authors_a_system_prompt(tree), (
            f"{relative} no longer authors a system prompt in code — delete its row "
            "from PENDING_CONVERSION so the ratchet tightens."
        )

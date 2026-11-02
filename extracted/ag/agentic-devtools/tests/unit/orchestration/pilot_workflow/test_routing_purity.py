"""Tests verifying routing functions are pure (no I/O, no side effects).

Uses AST inspection to assert that routing functions do not perform:
- File I/O (open, read, write, Path operations)
- Network I/O (requests, urllib, http)
- Time delays (time.sleep, asyncio.sleep)
- Print/logging side effects
- Subprocess calls
"""

import ast
import inspect

import pytest

from agentic_devtools.orchestration import pilot_workflow

ROUTING_FUNCTIONS = [
    "route_after_initiate",
    "route_after_setup",
    "route_after_retrieve",
    "route_after_plan",
    "route_after_checklist_creation",
    "route_after_implementation",
    "route_after_implementation_review",
    "route_after_verify",
    "route_after_commit",
    "route_after_pull_request",
]

# Forbidden function calls that indicate impurity
FORBIDDEN_CALLS = {
    "open",
    "print",
    "sleep",
    "subprocess",
    "run",
    "Popen",
    "requests",
    "urlopen",
}

# Forbidden module roots for module-qualified calls (e.g., subprocess.run)
FORBIDDEN_MODULES = {"subprocess", "requests", "urllib", "http"}

# Forbidden attribute accesses that indicate I/O
FORBIDDEN_ATTRS = {
    "sleep",
    "read",
    "write",
    "read_text",
    "write_text",
    "read_bytes",
    "write_bytes",
    "mkdir",
    "rmdir",
    "unlink",
    "open",
}


def _get_function_source(func_name: str) -> str:
    """Get the source code of a routing function."""
    func = getattr(pilot_workflow, func_name)
    return inspect.getsource(func)


def _find_impure_calls(source: str) -> list[str]:
    """Find forbidden function calls in source code AST."""
    tree = ast.parse(source)
    violations: list[str] = []

    def _attribute_chain_name(node: ast.AST) -> str | None:
        parts: list[str] = []
        current: ast.AST = node

        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if not isinstance(current, ast.Name):
            return None

        parts.append(current.id)
        return ".".join(reversed(parts))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Direct calls: open(...), print(...)
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                violations.append(f"Forbidden call: {node.func.id}()")

            # Attribute calls: time.sleep(...), path.read_text(...)
            if isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_ATTRS:
                violations.append(f"Forbidden attribute call: .{node.func.attr}()")

            # Module-based calls: subprocess.run(...), requests.get(...)
            qualified_name = _attribute_chain_name(node.func)
            if qualified_name:
                root_name = qualified_name.split(".", 1)[0]
                if root_name in FORBIDDEN_MODULES:
                    violations.append(f"Forbidden module call: {qualified_name}()")

    return violations


class TestRoutingPurity:
    """All routing functions must be pure — no I/O, no side effects."""

    @pytest.mark.parametrize("func_name", ROUTING_FUNCTIONS)
    def test_no_impure_calls(self, func_name: str) -> None:
        source = _get_function_source(func_name)
        violations = _find_impure_calls(source)
        assert violations == [], f"{func_name} has impure calls: {violations}"

    @pytest.mark.parametrize("func_name", ROUTING_FUNCTIONS)
    def test_only_takes_state_parameter(self, func_name: str) -> None:
        """Routing functions should only take a single 'state' parameter."""
        func = getattr(pilot_workflow, func_name)
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        assert params == ["state"], f"{func_name} should only take 'state', got: {params}"

    @pytest.mark.parametrize("func_name", ROUTING_FUNCTIONS)
    def test_returns_string(self, func_name: str) -> None:
        """Routing functions must return a string (node name)."""
        func = getattr(pilot_workflow, func_name)
        # Call with minimal state
        result = func({})
        assert isinstance(result, str)

    @pytest.mark.parametrize("func_name", ROUTING_FUNCTIONS)
    def test_deterministic(self, func_name: str) -> None:
        """Same input state should always produce same output."""
        func = getattr(pilot_workflow, func_name)
        state = {"issue_key": "TEST-1", "error": None}
        result1 = func(state)
        result2 = func(state)
        assert result1 == result2

import ast
import re
import subprocess
from datetime import date
from pathlib import Path

_ENDPOINT_OWNER_PATHS = frozenset(
    {
        "agentic_devtools/ai_providers/copilot.py",
        "agentic_devtools/ai_providers/agent_tasks_payload.py",
    }
)
# These are the three intentionally retained legacy consumers; each expires with the migration
# window rather than being silently exempted from the boundary.
_LEGACY_ALLOWLIST = {
    "agentic_devtools/cli/ci/agent_assignment.py": date(2026, 12, 31),
    ".github/scripts/speckit-trigger/agent-fallback.js": date(2026, 12, 31),
    ".github/workflows/speckit-agent-fallback-cleanup.yml": date(2026, 12, 31),
}
_AGENT_TASKS_MARKERS = frozenset({"agents/repos/", "copilot/coding-agent/tasks"})
_EXCLUDED_SOURCE_PARTS = frozenset({"generated", "node_modules", "tests", "vendor", "vendors"})
_SOURCE_EXTENSIONS = frozenset({".js", ".py", ".ps1", ".sh", ".ts", ".tsx", ".yml", ".yaml"})
_QUOTED_STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
_QUOTED_CONCAT_RE = re.compile(
    r'(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')(?:\s*\+\s*(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'))+'
)
_ASSIGNMENT_RE = re.compile(
    r"(?m)^\s*(?:const|let|var)?\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*"
    r"(?P<expr>(?:[A-Za-z_][A-Za-z0-9_]*|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)"
    r"(?:\s*\+\s*(?:[A-Za-z_][A-Za-z0-9_]*|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`))*)\s*;?\s*$"
)
_EXPR_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`")
_TEMPLATE_SLOT_RE = re.compile(r"\$\{([^}]*)\}")
_ARRAY_JOIN_ROUTE_RE = re.compile(
    r"\[[^\]]*['\"]agents['\"][^\]]*['\"]repos['\"][^\]]*['\"]tasks['\"][^\]]*\]\s*\.join\(\s*['\"]/['\"]\s*\)"
)
_ARRAY_ASSIGNMENT_RE = re.compile(
    r"(?m)^\s*(?:const|let|var)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*\[(?P<items>[^\]]*)\]\s*;?\s*$"
)
_ARRAY_JOIN_CALL_RE = re.compile(r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\.join\(\s*['\"]/['\"]\s*\)")
_UNRESOLVED_SENTINEL = "*"


def _constant_string_values(
    node: ast.AST,
    bindings: dict[str, ast.AST] | None = None,
    resolving: frozenset[str] = frozenset(),
) -> set[str]:
    bindings = bindings or {}
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, ast.Name):
        if node.id in bindings and node.id not in resolving:
            return _constant_string_values(node=bindings[node.id], bindings=bindings, resolving=resolving | {node.id})
        return {_UNRESOLVED_SENTINEL}
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _constant_string_values(node.left, bindings, resolving)
        right = _constant_string_values(node.right, bindings, resolving)
        return {a + b for a in left for b in right}
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "join"
        and len(node.args) == 1
        and not node.keywords
    ):
        separators = _constant_string_values(node.func.value, bindings, resolving)
        argument = node.args[0]
        if not separators or not isinstance(argument, (ast.List, ast.Tuple)):
            return set()
        join_parts: list[set[str]] = []
        for element in argument.elts:
            values = _constant_string_values(element, bindings, resolving)
            if not values:
                return set()
            join_parts.append(values)
        if not join_parts:
            return {""}
        joined_values: set[str] = set()
        for separator in separators:
            combinations = join_parts[0]
            for part in join_parts[1:]:
                combinations = {left + separator + right for left in combinations for right in part}
            joined_values.update(combinations)
        return joined_values
    if isinstance(node, ast.JoinedStr):
        parts: list[set[str]] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append({value.value})
                continue
            if isinstance(value, ast.FormattedValue):
                rendered = _constant_string_values(value.value, bindings, resolving)
                parts.append(rendered if rendered else {_UNRESOLVED_SENTINEL})
                continue
            return set()
        if not parts:
            return {""}
        combinations = parts[0]
        for part in parts[1:]:
            combinations = {left + right for left in combinations for right in part}
        return combinations
    return set()


def _concatenated_quoted_string_values(text: str) -> set[str]:
    values: set[str] = set()
    for expression in _QUOTED_CONCAT_RE.findall(text):
        pieces: list[str] = []
        for token in _QUOTED_STRING_RE.findall(expression):
            try:
                parsed = ast.literal_eval(token)
            except (SyntaxError, ValueError):
                pieces = []
                break
            if not isinstance(parsed, str):
                pieces = []
                break
            pieces.append(parsed)
        if len(pieces) > 1:
            values.add("".join(pieces))
    return values


def _bound_constant_string_values(text: str) -> set[str]:
    values: set[str] = set()
    pending: dict[str, list[str]] = {}
    resolved: dict[str, str] = {}

    for match in _ASSIGNMENT_RE.finditer(text):
        tokens = _EXPR_TOKEN_RE.findall(match.group("expr"))
        if tokens:
            pending[match.group("name")] = tokens

    while pending:
        progressed = False
        for name in tuple(pending):
            parts: list[str] = []
            for token in pending[name]:
                if token[0] in {"'", '"'}:
                    try:
                        parsed = ast.literal_eval(token)
                    except (SyntaxError, ValueError):
                        parts = []
                        break
                    if not isinstance(parsed, str):
                        parts = []
                        break
                    parts.append(parsed)
                    continue
                if token[0] == "`":
                    rendered = _render_template_literal(token, resolved)
                    if rendered is None:
                        parts = []
                        break
                    parts.append(rendered)
                    continue
                if token in resolved:
                    parts.append(resolved[token])
                    continue
                parts = []
                break
            if not parts:
                continue
            folded = "".join(parts)
            resolved[name] = folded
            if len(pending[name]) > 1 or pending[name][0].startswith("`"):
                values.add(folded)
            pending.pop(name)
            progressed = True
        if not progressed:
            # Fold remaining assignments using the sentinel for genuinely
            # external identifiers (those not declared anywhere in this text).
            # This preserves detectable route fragments even when runtime
            # values like `owner` or `repo` are never assigned locally.
            # Loop until no further progress to handle chains of pending
            # variables that resolve once earlier dependencies are folded.
            sentinel_progressed = True
            while pending and sentinel_progressed:
                sentinel_progressed = False
                for name in tuple(pending):
                    parts = []
                    for token in pending[name]:
                        if token[0] in {"'", '"'}:
                            try:
                                parsed = ast.literal_eval(token)
                            except (SyntaxError, ValueError):
                                parts = []
                                break
                            if not isinstance(parsed, str):
                                parts = []
                                break
                            parts.append(parsed)
                            continue
                        if token[0] == "`":
                            rendered = _render_template_literal(token, resolved)
                            parts.append(rendered if rendered is not None else _UNRESOLVED_SENTINEL)
                            continue
                        if token in resolved:
                            parts.append(resolved[token])
                            continue
                        # Pending (not yet resolved): skip this assignment for now.
                        if token in pending:
                            parts = []
                            break
                        # Genuinely external runtime identifier: substitute sentinel.
                        parts.append(_UNRESOLVED_SENTINEL)
                    if parts:
                        folded = "".join(parts)
                        resolved[name] = folded
                        if _UNRESOLVED_SENTINEL in folded or len(pending[name]) > 1 or pending[name][0].startswith("`"):
                            values.add(folded)
                        pending.pop(name)
                        sentinel_progressed = True
            break
    return values


def _render_template_literal(token: str, resolved: dict[str, str]) -> str | None:
    if len(token) < 2 or token[0] != "`" or token[-1] != "`":
        return None
    literal = token[1:-1]
    parts: list[str] = []
    cursor = 0
    for match in _TEMPLATE_SLOT_RE.finditer(literal):
        parts.append(literal[cursor : match.start()])
        reference = match.group(1).strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", reference):
            parts.append(resolved.get(reference, _UNRESOLVED_SENTINEL))
        else:
            parts.append(_UNRESOLVED_SENTINEL)
        cursor = match.end()
    tail = literal[cursor:]
    if "${" in tail:
        return None
    parts.append(tail)
    return "".join(parts)


def _contains_unresolved_agent_tasks_route(text: str) -> bool:
    if _ARRAY_JOIN_ROUTE_RE.search(text) is not None:
        return True

    route_arrays: set[str] = set()
    for assignment in _ARRAY_ASSIGNMENT_RE.finditer(text):
        pieces: list[str] = []
        for token in _QUOTED_STRING_RE.findall(assignment.group("items")):
            try:
                parsed = ast.literal_eval(token)
            except (SyntaxError, ValueError):
                continue
            if isinstance(parsed, str):
                pieces.append(parsed)
        try:
            agents_index = pieces.index("agents")
            repos_index = pieces.index("repos", agents_index + 1)
            pieces.index("tasks", repos_index + 1)
        except ValueError:
            continue
        else:
            route_arrays.add(assignment.group("name"))

    if not route_arrays:
        return False

    return any(call.group("name") in route_arrays for call in _ARRAY_JOIN_CALL_RE.finditer(text))


def test_only_copilot_provider_owns_agent_tasks_endpoint() -> None:
    root = Path(__file__).resolve().parents[2]
    offenders: list[str] = []
    source_patterns = [f"*{extension}" for extension in sorted(_SOURCE_EXTENSIONS)]
    tracked_sources = subprocess.run(
        ["git", "ls-files", "-z", "--", *source_patterns],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    for relative in sorted({raw_path.decode("utf-8") for raw_path in tracked_sources if raw_path}):
        relative_path = Path(relative)
        if relative_path.suffix not in _SOURCE_EXTENSIONS or _EXCLUDED_SOURCE_PARTS.intersection(relative_path.parts):
            continue
        if relative in _ENDPOINT_OWNER_PATHS or relative in _LEGACY_ALLOWLIST:
            continue
        path = root / relative
        text = path.read_text(encoding="utf-8")
        constant_strings = _concatenated_quoted_string_values(text)
        constant_strings.update(_bound_constant_string_values(text))
        if path.suffix == ".py":
            tree = ast.parse(text, filename=relative)
            bindings: dict[str, ast.AST] = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            bindings[target.id] = node.value
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
                    bindings[node.target.id] = node.value
            constant_strings.update(
                {value for node in ast.walk(tree) for value in _constant_string_values(node, bindings)}
            )
        haystack = text if not constant_strings else text + "\n" + "\n".join(constant_strings)
        if any(marker in haystack for marker in _AGENT_TASKS_MARKERS) or _contains_unresolved_agent_tasks_route(text):
            offenders.append(relative)

    assert not offenders, f"Direct Agent Tasks endpoint usage outside provider: {offenders}"


def test_legacy_allowlist_entries_are_unexpired() -> None:
    root = Path(__file__).resolve().parents[2]
    for relative, expiry in _LEGACY_ALLOWLIST.items():
        assert (root / relative).is_file(), f"Legacy allowlist entry does not exist: {relative}"
        assert expiry > date.today(), f"Legacy allowlist entry is expired: {relative}"


def test_legacy_allowlist_entry_exercises_legacy_marker() -> None:
    root = Path(__file__).resolve().parents[2]
    for relative in _LEGACY_ALLOWLIST:
        text = (root / relative).read_text(encoding="utf-8")
        assert any(marker in text for marker in _AGENT_TASKS_MARKERS), (
            f"Allowlist entry {relative!r} does not use any Agent Tasks endpoint marker; remove it"
        )


def test_constant_string_values_resolve_named_concatenations() -> None:
    tree = ast.parse('prefix = "agents/"\nresource = "repos/"\nurl = prefix + resource + "owner/repo/tasks"')
    bindings: dict[str, ast.AST] = {
        node.targets[0].id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
    }

    values = {value for node in ast.walk(tree) for value in _constant_string_values(node, bindings)}

    assert "agents/repos/owner/repo/tasks" in values


def test_constant_string_values_resolve_f_strings_with_named_constants() -> None:
    tree = ast.parse('prefix = "copilot/coding-agent/"\nroute = f"{prefix}tasks"')
    bindings: dict[str, ast.AST] = {
        node.targets[0].id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
    }

    values = {value for node in ast.walk(tree) for value in _constant_string_values(node, bindings)}

    assert "copilot/coding-agent/tasks" in values


def test_constant_string_values_preserves_constant_fragments_around_unresolved_slots() -> None:
    tree = ast.parse('prefix = "agents/"\nroute = f"{prefix}repos/{owner}/{repo}/tasks"')
    bindings: dict[str, ast.AST] = {
        node.targets[0].id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
    }

    values = {value for node in ast.walk(tree) for value in _constant_string_values(node, bindings)}

    assert any("agents/repos/" in v for v in values)


def test_constant_string_values_preserves_binop_fragments_around_unresolved_slots() -> None:
    tree = ast.parse('prefix = "agents"\nroute = "/" + prefix + "/repos/" + owner + "/" + repo + "/tasks"')
    bindings: dict[str, ast.AST] = {
        node.targets[0].id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
    }

    values = {value for node in ast.walk(tree) for value in _constant_string_values(node, bindings)}

    assert any("agents/repos/" in v for v in values)


def test_constant_string_values_supports_join_built_routes_with_runtime_segments() -> None:
    tree = ast.parse('route = "/" + "/".join(("agents", "repos", owner, repo, "tasks"))')

    values = {value for node in ast.walk(tree) for value in _constant_string_values(node, {})}

    assert any("agents/repos/" in v for v in values)


def test_contains_unresolved_agent_tasks_route_detects_js_array_join_route() -> None:
    text = "const route = ['agents', 'repos', owner, repo, 'tasks'].join('/');"

    assert _contains_unresolved_agent_tasks_route(text)


def test_contains_unresolved_agent_tasks_route_detects_named_js_array_join_route() -> None:
    text = "const parts = ['agents', 'repos', owner, repo, 'tasks'];\nconst route = parts.join('/');"

    assert _contains_unresolved_agent_tasks_route(text)


def test_contains_unresolved_agent_tasks_route_ignores_non_agent_routes() -> None:
    text = "const route = ['repos', owner, repo, 'issues'].join('/');"

    assert not _contains_unresolved_agent_tasks_route(text)


def test_concatenated_quoted_string_values_handles_split_js_literals() -> None:
    text = "const route = 'copilot/coding-agent/' + 'tasks';"

    assert _concatenated_quoted_string_values(text) == {"copilot/coding-agent/tasks"}


def test_bound_constant_string_values_resolves_named_js_constants() -> None:
    text = "const prefix = 'copilot/coding-agent/';\nconst route = prefix + 'tasks';"

    assert "copilot/coding-agent/tasks" in _bound_constant_string_values(text)


def test_bound_constant_string_values_resolves_js_template_literals() -> None:
    text = "const segment = 'agents';\nconst route = `/${segment}/repos/${owner}/${repo}/tasks`;"

    assert any("agents/repos/" in value for value in _bound_constant_string_values(text))


def test_bound_constant_string_values_detects_route_with_external_runtime_identifiers() -> None:
    # Route built from a mix of resolved locals and external runtime identifiers.
    # The resolver must substitute the sentinel for genuinely external names so
    # that the constant route fragments (e.g. 'agents/repos/') remain detectable.
    text = "const prefix = 'agents';\nconst route = '/' + prefix + '/repos/' + owner + '/' + repo + '/tasks';"

    result = _bound_constant_string_values(text)
    assert any("agents/repos/" in value for value in result)

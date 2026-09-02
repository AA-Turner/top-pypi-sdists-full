"""Every API URL this repo's own clients build must be served by a real route.

Nine client-built URLs matched no route and nothing compared them (#652). Three
were live: the MCP `sync_repository` tool POSTed to `…/repositories/{id}/sync`
(the route is `…/github-registrations/{id}/sync`), `analyze_temporal_patterns`
POSTed to `/ai/analyze-temporal` (the route is `/ai/analyze`), and
`innoday tickets refresh` POSTed to `…/tickets/refresh`, an endpoint deliberately
removed after Trello. All were half-finished renames, and every one of them
reached a user as a *successful* result or a bare non-zero exit.

Four things this guard does deliberately, each because the cheaper version of it
was tried during the audit and gave a wrong answer:

1. **The route table is resolved through `_IncludedRouter`.** A flat walk of
   `app.routes` yields 34 entries in this FastAPI version -- 6 real routes plus
   28 opaque wrappers -- so a guard built on that walk would compare against
   almost nothing and pass everything. `test_route_table_reconciles` pins the
   resolved figure against `scripts/check_endpoint_count.sh` so the walker
   cannot silently degrade.

2. **Matching is by compiled regex, not string equality.** The literal `refresh`
   in `…/tickets/refresh` is absorbed by `{ticket_id}`, so that URL is a **405**,
   not a 404. String normalisation misfiles it, and "no such path" and "wrong
   method on a real path" need different fixes.

3. **A literal that lands in a `{param}` slot is reported, not accepted.** It
   matches the regex, so a plain regex test calls it served; it is exactly the
   shape of a stale path segment.

4. **Unresolvable calls are named, not skipped.** The ~5 generic pass-through
   wrappers (`_API.get(path)`, `InnoDayAPIClient.get(endpoint)`) take the path as
   a parameter and cannot be resolved statically. They sit in `EXEMPT_CALLS`,
   which `test_exemptions_are_exactly_consumed` asserts is exactly consumed --
   the same pinning `tests/test_auth_tiers.py` applies to its public-route list.
   A pattern-based filter was rejected: a pattern lets the next stale URL opt out
   of the guard silently, which is the failure this whole test exists to stop.

What this does NOT cover: query parameters the route does not declare (FastAPI
drops unknown ones silently), request-body shape, and fields bound from the query
string while the client sends JSON. Those are separate classes; see #652.
"""

import ast
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from starlette.routing import Mount, compile_path

from src.api.app import app

REPO_ROOT = Path(__file__).resolve().parent.parent

# The four places this repo talks to its own API from. `src/integrations/` goes
# through `InnoDayAPIClient`, so it is covered by the same receiver rules as the
# CLI. Nothing else in `src/` calls InnoDay's own API: every other `httpx` use
# targets GitHub, Jira, Linear, Trello, Notion, Slack or Supabase, and those are
# skipped by host (see `_is_external`).
CLIENT_DIRS = ("src/mcp", "src/cli", "src/integrations", "scripts")

HTTP_VERBS = {"get", "post", "put", "patch", "delete", "head", "options"}

# Expressions that construct something with HTTP verb methods on it, and how the
# first argument of a verb call on it is interpreted:
#
#   "absolute" -- the argument is a whole URL or a server-absolute path
#                 (`httpx`, and the MCP server's `_API`, which appends the
#                 argument to `api_url` unchanged).
#   "innoday"  -- the argument is an *endpoint* that goes through
#                 `InnoDayAPIClient._build_api_url`, which adds `/api/v1` and,
#                 for tickets/repositories, the org scope.
#
# A verb call on one of these receivers must resolve to a route or be exempt --
# being unable to resolve it is a failure, not a skip.
CLIENT_FACTORIES = {
    "httpx.AsyncClient": "absolute",
    "httpx.Client": "absolute",
    "requests.Session": "absolute",
    "_API": "absolute",
    "InnoDayAPIClient": "innoday",
    "create_api_client": "innoday",
}

# Receivers whose kind is not visible from a construction in the same file, each
# with the reason. `test_pinned_lists_are_exactly_consumed` fails when one stops
# matching, so this cannot rot into a list of things that no longer exist -- and
# a receiver that is in neither this map nor a visible construction is *reported*,
# not skipped, so a new client cannot quietly escape the guard.
RECEIVER_KINDS: Dict[Tuple[str, str], str] = {
    # `InnoDayVersionStore.__init__(api_client, ...)` is documented as taking "a
    # constructed InnoDayAPIClient"; the parameter carries no annotation.
    ("src/integrations/innoday_version_store.py", "self._api"): "innoday",
}

# A placeholder for any `{...}` segment. Long enough not to collide with a real
# literal segment, and shaped like the UUIDs these paths actually carry.
_PARAM_FILL = "11111111-1111-1111-1111-111111111111"

# The generic pass-through wrappers. Each takes the path as a parameter, so there
# is no path here to check -- the checkable thing is each *caller* of these, and
# those are extracted separately. Keyed on (file, unparsed URL expression) rather
# than a line number so that moving code does not invalidate the list.
#
# `test_exemptions_are_exactly_consumed` fails if an entry stops matching, so a
# wrapper that is deleted or rewritten cannot leave a dead exemption behind.
EXEMPT_CALLS: Dict[Tuple[str, str], str] = {
    (
        "src/cli/client.py",
        "url",
    ): "InnoDayAPIClient's generic verbs pass an already-built URL to httpx; `url` comes from the caller's `endpoint`",
}


# ---------------------------------------------------------------------------
# The route table
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Route:
    path: str
    methods: Tuple[str, ...]
    regex: re.Pattern
    module: str
    name: str


def _resolve_routes() -> List[Route]:
    """Flatten the app's real route table.

    `app.routes` in this FastAPI version holds `_IncludedRouter` wrappers, whose
    own `.path` is absent and whose children live behind
    `.original_router.routes` with the prefix on `.include_context.prefix`.
    Recursing those two attributes is what turns 34 entries into 237.
    """
    out: List[Route] = []

    def walk(routes, prefix: str = "") -> None:
        for route in routes:
            if type(route).__name__ == "_IncludedRouter":
                context = getattr(route, "include_context", None)
                original = getattr(route, "original_router", None)
                walk(
                    getattr(original, "routes", []) or [],
                    prefix + (getattr(context, "prefix", "") or ""),
                )
                continue
            if isinstance(route, Mount):
                walk(getattr(route, "routes", []) or [], prefix + (route.path or ""))
                continue
            path = prefix + getattr(route, "path", "")
            endpoint = getattr(route, "endpoint", None)
            out.append(
                Route(
                    path=path,
                    methods=tuple(sorted(getattr(route, "methods", None) or ["GET"])),
                    regex=compile_path(path)[0],
                    module=getattr(endpoint, "__module__", "") or "",
                    name=getattr(endpoint, "__name__", "")
                    or getattr(route, "name", ""),
                )
            )

    walk(app.routes)
    return out


ROUTES = _resolve_routes()


# ---------------------------------------------------------------------------
# The client calls
# ---------------------------------------------------------------------------


@dataclass
class Call:
    file: str
    line: int
    verb: Optional[str]
    template: Optional[str]
    raw: str
    receiver: str
    kind: Optional[str]  # "absolute" | "innoday" | None when unresolved


def _unparse(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover -- defensive
        return "<unparseable>"


def _build_api_url(endpoint: str) -> str:
    """Mirror `InnoDayAPIClient._build_api_url`.

    Kept in step with that method deliberately rather than imported: the real one
    needs a live config object and returns an absolute URL. The org-scoped branch
    is modelled as taken, because every caller of a `tickets`/`repositories` path
    raises `APIError` when the org is unset.
    """
    endpoint = endpoint.lstrip("/")
    if endpoint.startswith("api/v1/"):
        endpoint = endpoint[len("api/v1/") :]
    if endpoint.startswith("tickets") or endpoint.startswith("repositories"):
        return f"/api/v1/organizations/{{organization_id}}/{endpoint}"
    return f"/api/v1/{endpoint}"


def test_the_modelled_url_builder_matches_the_real_one():
    """`_build_api_url` above is a copy, so pin it to the original.

    A guard that models its subject wrongly is worse than no guard: it reports
    confidently about paths the client never builds. Nothing tied the copy to
    `InnoDayAPIClient._build_api_url`, so adding a third org-scoped prefix there
    would have left this file silently mis-modelling every such URL while still
    passing.

    The real method needs a live config and returns an absolute URL, which is why
    it is modelled rather than imported -- so compare the *path* the two produce
    for the shapes that actually occur, including the org-scoped branch and the
    already-prefixed form.
    """
    from unittest.mock import patch

    from src.cli.client import InnoDayAPIClient

    probes = [
        "tickets",
        "tickets/refresh",
        "repositories",
        "organizations",
        "api/v1/organizations",
        "/tickets",
        "ai/analyze",
    ]

    with patch.object(InnoDayAPIClient, "__init__", lambda self: None):
        client = InnoDayAPIClient()
        # `api_base_url` is what `_build_api_url` joins against, not `base_url`.
        client.api_base_url = "http://x"
        client.organization_id = "{organization_id}"
        for endpoint in probes:
            real = InnoDayAPIClient._build_api_url(client, endpoint)
            real_path = real[len("http://x") :] if real.startswith("http://x") else real
            assert real_path == _build_api_url(endpoint), (
                f"the modelled builder and the real one disagree on {endpoint!r}: "
                f"real={real_path!r} modelled={_build_api_url(endpoint)!r}"
            )


class _Scope:
    """String values of local names, resolved by the nearest preceding binding."""

    def __init__(self) -> None:
        self.frames: List[Dict[str, List[Tuple[int, str]]]] = []

    def push(self) -> None:
        self.frames.append({})

    def pop(self) -> None:
        self.frames.pop()

    def add(self, name: str, line: int, value: str) -> None:
        self.frames[-1].setdefault(name, []).append((line, value))

    def lookup(self, name: str, line: int) -> Optional[str]:
        for frame in reversed(self.frames):
            best: Optional[Tuple[int, str]] = None
            for bound_line, value in frame.get(name, []):
                if bound_line <= line and (best is None or bound_line > best[0]):
                    best = (bound_line, value)
            if best:
                return best[1]
        return None


def _template(node: ast.AST, scope: _Scope, line: int) -> Optional[str]:
    """Render a URL expression into a path template, or None if not static.

    Interpolations become `{expr}` placeholders unless the interpolated value is
    itself a resolvable path fragment, which is how `url = self._build_api_url(…)`
    followed by `self.api_client.get(url)` resolves in one pass.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                inner = _template(value.value, scope, line)
                # Inline an interpolation that is itself part of the URL -- a path
                # fragment, or a query string assembled separately (`clear{query}`,
                # where `query` is `"?dry_run=true" if dry_run else ""`). Anything
                # else is a single path segment, so it becomes a placeholder.
                if inner is not None and (
                    "/" in inner or inner.startswith(("http", "?", "&"))
                ):
                    parts.append(inner)
                else:
                    parts.append("{" + _unparse(value.value) + "}")
            else:
                parts.append("{?}")
        return "".join(parts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _template(node.left, scope, line)
        right = _template(node.right, scope, line)
        return None if left is None or right is None else left + right
    if isinstance(node, ast.Name):
        return scope.lookup(node.id, line)
    if isinstance(node, ast.Attribute):
        return "{" + _unparse(node) + "}"
    if isinstance(node, ast.IfExp):
        return _template(node.body, scope, line) or _template(node.orelse, scope, line)
    if isinstance(node, ast.Call):
        func = _unparse(node.func)
        if func.endswith("_build_api_url") and node.args:
            inner = _template(node.args[0], scope, line)
            return None if inner is None else _build_api_url(inner)
        if func.endswith((".rstrip", ".lstrip", ".strip")) and isinstance(
            node.func, ast.Attribute
        ):
            return _template(node.func.value, scope, line)
    return None


def _import_aliases(tree: ast.AST) -> Dict[str, str]:
    """Local name -> imported name.

    `src/cli/commands/*.py` import the client as
    `from src.cli.client import InnoDayAPIClient as APIClient`, so matching the
    factory list against the source text alone recognises nothing in the files
    that make most of the CLI's requests.
    """
    aliases: Dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.asname:
                    aliases[alias.asname] = alias.name.rsplit(".", 1)[-1]
    return aliases


def _factory_kind(rendered: str, aliases: Dict[str, str]) -> Optional[str]:
    match = re.match(r"(?:await\s+)?([\w.]+)\s*\(", rendered)
    if not match:
        return None
    called = match.group(1)
    for candidate in (called, called.rsplit(".", 1)[-1]):
        candidate = aliases.get(candidate, candidate)
        if candidate in CLIENT_FACTORIES:
            return CLIENT_FACTORIES[candidate]
    return None


def _client_receivers(tree: ast.AST, relative: str) -> Dict[str, str]:
    """Receiver expression -> kind, for every HTTP client visible in a module.

    Three sources, in order of reliability: a construction bound by `with` or by
    assignment (including `self.x = httpx.AsyncClient(...)`), a parameter
    annotation, and the pinned `RECEIVER_KINDS` for the one client that is only
    documented in prose.
    """
    aliases = _import_aliases(tree)
    kinds: Dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if not isinstance(item.optional_vars, ast.Name):
                    continue
                kind = _factory_kind(_unparse(item.context_expr), aliases)
                if kind:
                    kinds[item.optional_vars.id] = kind
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, (ast.Name, ast.Attribute)):
                kind = _factory_kind(_unparse(node.value), aliases)
                if kind:
                    kinds[_unparse(target)] = kind
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in list(node.args.args) + list(node.args.kwonlyargs):
                annotation = _unparse(arg.annotation) if arg.annotation else ""
                resolved = aliases.get(annotation, annotation)
                if resolved in CLIENT_FACTORIES:
                    kinds[arg.arg] = CLIENT_FACTORIES[resolved]
    # `InnoDayAPIClient` holds its raw `httpx.AsyncClient` as `.api_client`, so
    # `<innoday client>.api_client.delete(...)` takes whole URLs, not endpoints.
    for receiver, kind in list(kinds.items()):
        if kind == "innoday":
            kinds[f"{receiver}.api_client"] = "absolute"
    for (file, receiver), kind in RECEIVER_KINDS.items():
        if file == relative:
            kinds.setdefault(receiver, kind)
    return kinds


_SCOPE_NODES = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Lambda,
)


def _own_nodes(body: List[ast.stmt]):
    """Every node under `body`, stopping at (but yielding) nested scopes.

    Scoping matters more than it looks: with one module-wide scope, the `url`
    that `InnoDayAPIClient.get_comments` binds is still visible inside the
    generic `put`/`patch`/`delete` defined below it, so those three were reported
    as 405s on the comments route -- three false findings, and the kind of noise
    that gets a guard switched off.
    """
    stack = list(body)
    while stack:
        node = stack.pop()
        yield node
        if isinstance(node, _SCOPE_NODES):
            continue
        stack.extend(ast.iter_child_nodes(node))


def _bind_names(body: List[ast.stmt], scope: _Scope) -> None:
    for sub in _own_nodes(body):
        if isinstance(sub, _SCOPE_NODES):
            continue
        if isinstance(sub, ast.Assign) and len(sub.targets) == 1:
            target = sub.targets[0]
            if isinstance(target, ast.Name):
                value = _template(sub.value, scope, sub.lineno)
                if value:
                    scope.add(target.id, sub.lineno, value)
        elif (
            isinstance(sub, ast.AnnAssign)
            and isinstance(sub.target, ast.Name)
            and sub.value is not None
        ):
            value = _template(sub.value, scope, sub.lineno)
            if value:
                scope.add(sub.target.id, sub.lineno, value)


def _looks_like_api_path(template: Optional[str]) -> bool:
    """True for a template that is plainly a URL or a server-absolute path.

    This is the second half of the extraction: it catches a verb call on a
    receiver the factory list does not recognise. Combined with the receiver
    rule, the only thing that escapes both is an unknown client whose URL is not
    statically knowable -- which nothing static could catch.
    """
    if not template:
        return False
    if template.startswith(("http://", "https://")):
        return True
    return re.sub(r"^\{[^}]*\}", "", template).startswith("/")


def _is_external(template: str) -> bool:
    """A URL naming a host that is not this API."""
    match = re.match(r"https?://([^/]+)", template)
    if not match:
        return False
    host = match.group(1)
    if host.startswith("{"):
        return False
    return not host.startswith(("localhost", "127.0.0.1"))


def _extract_calls() -> List[Call]:
    files: List[Path] = []
    for directory in CLIENT_DIRS:
        files.extend(
            p
            for p in sorted((REPO_ROOT / directory).rglob("*.py"))
            if "__pycache__" not in p.parts
        )

    calls: List[Call] = []
    for path in files:
        tree = ast.parse(path.read_text())
        relative = str(path.relative_to(REPO_ROOT))
        receivers = _client_receivers(tree, relative)

        scope = _Scope()

        def visit(body: List[ast.stmt]) -> None:
            scope.push()
            _bind_names(body, scope)
            nested: List[ast.AST] = []
            for node in _own_nodes(body):
                if isinstance(node, _SCOPE_NODES):
                    nested.append(node)
                    continue
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                if not isinstance(func, ast.Attribute) or func.attr not in HTTP_VERBS:
                    continue
                receiver = _unparse(func.value)
                url_node = node.args[0] if node.args else None
                for keyword in node.keywords:
                    if keyword.arg == "url":
                        url_node = keyword.value
                if url_node is None:
                    continue
                template = _template(url_node, scope, node.lineno)
                kind = receivers.get(receiver)
                if kind is None and not _looks_like_api_path(template):
                    continue
                calls.append(
                    Call(
                        file=relative,
                        line=node.lineno,
                        verb=func.attr.upper(),
                        template=template,
                        raw=_unparse(url_node),
                        receiver=receiver,
                        kind=kind,
                    )
                )
            for node in nested:
                inner = node.body
                visit(inner if isinstance(inner, list) else [ast.Expr(value=inner)])
            scope.pop()

        visit(tree.body)

    seen: Set[Tuple] = set()
    unique: List[Call] = []
    for call in calls:
        key = (call.file, call.line, call.verb, call.template, call.raw)
        if key in seen:
            continue
        seen.add(key)
        unique.append(call)
    return unique


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    call: Call
    path: str
    kind: str  # "no-route" | "wrong-method" | "literal-in-param" | "unresolvable"
    nearest: List[str] = field(default_factory=list)


def _client_path(template: str) -> str:
    """Strip host and query, collapse slashes -- leaving a comparable path.

    A bare endpoint (`repositories`) comes back unchanged and without a leading
    slash; that is the `InnoDayAPIClient` convention and `_build_api_url` handles
    it, so the caller decides what to do with the result.
    """
    path = template
    match = re.match(r"https?://[^/]*(/.*)?$", path)
    if match:
        path = match.group(1) or "/"
    else:
        # A leading `{base_url}` placeholder is the same thing spelled as an
        # interpolation: `f"{get_config().api_url}/api/v1/..."`.
        path = re.sub(r"^\{[^}]*\}", "", path)
    path = path.split("?")[0]
    path = re.sub(r"/+", "/", path)
    return path.rstrip("/") or "/"


def _concrete(path: str) -> str:
    return re.sub(r"\{[^}]*\}", _PARAM_FILL, path)


def _segments_absorb_literal(client_path: str, route_path: str) -> Optional[str]:
    """Return the client's literal segment that landed in a route `{param}`.

    `…/tickets/refresh` matches `…/tickets/{ticket_id}` on the regex, but the
    client meant a literal action, not an id. Reporting it is the difference
    between "served" and "405 on a route that will never do what you asked".
    """
    client_segments = client_path.strip("/").split("/")
    route_segments = route_path.strip("/").split("/")
    if len(client_segments) != len(route_segments):
        return None
    for client_segment, route_segment in zip(client_segments, route_segments):
        route_is_param = route_segment.startswith("{") and route_segment.endswith("}")
        client_is_param = client_segment.startswith("{") and client_segment.endswith(
            "}"
        )
        if route_is_param and not client_is_param:
            return client_segment
    return None


def _nearest(path: str, limit: int = 3) -> List[str]:
    """Route templates sharing the longest literal prefix with `path`."""
    wanted = path.strip("/").split("/")
    scored = []
    for route in ROUTES:
        segments = route.path.strip("/").split("/")
        shared = 0
        for a, b in zip(wanted, segments):
            if a == b or (b.startswith("{") and a.startswith("{")):
                shared += 1
            else:
                break
        scored.append((shared, f"{'/'.join(sorted(route.methods))} {route.path}"))
    scored.sort(key=lambda item: -item[0])
    return [label for score, label in scored[:limit] if score > 0]


def _check(call: Call) -> Optional[Finding]:
    if call.template is None:
        return Finding(call, "<unresolved>", "unresolvable")
    if _is_external(call.template):
        return None
    path = _client_path(call.template)
    if call.kind == "innoday":
        path = _build_api_url(path)
    elif call.kind is None:
        # Reached only via the URL-shape half of the extraction: something with
        # verb methods that no construction, annotation or RECEIVER_KINDS entry
        # identifies. Its path convention is unknown, so it cannot be checked --
        # and silently assuming one is how a wrong URL passes.
        return Finding(call, path, "unknown-client")
    if not path.startswith("/"):
        return Finding(call, path, "unresolvable")
    concrete = _concrete(path)

    method_only: List[Route] = []
    absorbed: List[Tuple[Route, str]] = []
    for route in ROUTES:
        if not route.regex.match(concrete):
            continue
        if call.verb not in route.methods:
            method_only.append(route)
            continue
        literal = _segments_absorb_literal(path, route.path)
        if literal is not None:
            absorbed.append((route, literal))
            continue
        return None  # served, and no literal fell into a parameter slot

    if method_only:
        return Finding(
            call,
            path,
            "wrong-method",
            [f"{'/'.join(sorted(r.methods))} {r.path}" for r in method_only],
        )
    if absorbed:
        return Finding(
            call,
            path,
            "literal-in-param",
            [
                f"{'/'.join(sorted(r.methods))} {r.path} (absorbs literal '{lit}')"
                for r, lit in absorbed
            ],
        )
    return Finding(call, path, "no-route", _nearest(path))


def _findings() -> Tuple[List[Finding], Set[Tuple[str, str]], Set[Tuple[str, str]]]:
    findings: List[Finding] = []
    exempt_used: Set[Tuple[str, str]] = set()
    receivers_used: Set[Tuple[str, str]] = set()
    for call in _extract_calls():
        if (call.file, call.receiver) in RECEIVER_KINDS:
            receivers_used.add((call.file, call.receiver))
        finding = _check(call)
        if finding is None:
            continue
        # An exemption may only silence a call whose URL could not be resolved --
        # never one that resolved to a path no route serves. Otherwise a single
        # entry covering a generic wrapper would also cover every sibling method
        # in the same file that happens to pass its URL through the same local
        # name, which is how `tickets/refresh` hid behind `url` in a first draft
        # of this guard.
        key = (call.file, call.raw)
        if finding.kind in ("unresolvable", "unknown-client") and key in EXEMPT_CALLS:
            exempt_used.add(key)
            continue
        findings.append(finding)
    return findings, exempt_used, receivers_used


def _report(findings: List[Finding]) -> str:
    explain = {
        "no-route": "404 -- no route serves this path",
        "wrong-method": "405 -- the path is served, but not with this method",
        "literal-in-param": "the literal segment is absorbed by a route parameter",
        "unresolvable": "could not be resolved statically -- make it static or add it to EXEMPT_CALLS with a reason",
        "unknown-client": "the receiver is not a recognised client -- add it to RECEIVER_KINDS with its path convention",
    }
    lines = []
    for finding in sorted(findings, key=lambda f: (f.call.file, f.call.line)):
        call = finding.call
        lines.append(
            f"  {call.file}:{call.line}  {call.verb} {finding.path}\n"
            f"      built from: {call.raw}\n"
            f"      problem:    {explain[finding.kind]}\n"
            f"      nearest:    {finding.nearest or ['(none)']}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_route_table_reconciles_with_the_endpoint_count_script():
    """Guard the guard: a degraded walker must fail here, not pass everything.

    `scripts/check_endpoint_count.sh` counts HTTP-verb decorators under
    `src/routers/`. That figure and this walk must agree exactly on the router
    routes, and every route the walk finds beyond them must be one of the
    accounted-for extras below.
    """
    script = subprocess.run(
        ["bash", "scripts/check_endpoint_count.sh"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert script.returncode == 0, script.stdout + script.stderr
    documented = int(re.search(r"OK: (\d+) endpoints", script.stdout).group(1))

    standard = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    router_decorators = {
        (method, route.path, route.module, route.name)
        for route in ROUTES
        if route.module.startswith("src.routers")
        for method in route.methods
        if method in standard
    }
    assert len(router_decorators) == documented, (
        f"walked {len(router_decorators)} router endpoints, "
        f"check_endpoint_count.sh counts {documented}"
    )

    # The remainder, named so a change to it is deliberate:
    #   * HEAD /api/v1/public/health -- a `@router.head` the script's verb regex
    #     excludes on purpose, and the whole of the 227-vs-228 gap.
    #   * five routes declared on the app rather than a router.
    #   * four FastAPI built-ins (/openapi.json, /docs, /docs/oauth2-redirect,
    #     /redoc).
    extras = sorted(
        f"{'/'.join(sorted(r.methods))} {r.path}"
        for r in ROUTES
        if not (r.module.startswith("src.routers") and set(r.methods) & standard)
    )
    assert extras == [
        "GET / (src.api.app)".replace(" (src.api.app)", ""),
        "GET /auth/callback",
        "GET /device",
        "GET /health",
        "GET /invite/accept",
        "GET/HEAD /docs",
        "GET/HEAD /docs/oauth2-redirect",
        "GET/HEAD /openapi.json",
        "GET/HEAD /redoc",
        "HEAD /api/v1/public/health",
    ], extras


def test_every_client_url_is_served_by_a_route():
    findings, _, _ = _findings()
    assert not findings, (
        f"{len(findings)} client-built URL(s) no route serves:\n"
        + _report(findings)
        + "\n\nFix the client, or -- for a generic wrapper whose path is a "
        "parameter -- add it to EXEMPT_CALLS in this file with a reason."
    )


def test_pinned_lists_are_exactly_consumed():
    """A stale exemption is a hole, so an unused entry fails.

    Same reasoning as `tests/test_auth_tiers.py::test_public_route_list_is_pinned`:
    an exemption list only stays honest if shrinking the thing it exempts breaks
    the build.
    """
    _, exempt_used, receivers_used = _findings()
    unused = sorted(
        [("EXEMPT_CALLS", k) for k in set(EXEMPT_CALLS) - exempt_used]
        + [("RECEIVER_KINDS", k) for k in set(RECEIVER_KINDS) - receivers_used]
    )
    assert not unused, (
        "Pinned entries matched no call -- the client moved, was renamed, or was "
        "deleted. Remove them:\n  " + "\n  ".join(map(str, unused))
    )


def test_a_literal_absorbed_by_a_path_parameter_is_not_reported_as_served():
    """The case that motivated regex matching, pinned so it cannot regress.

    `POST /api/v1/organizations/{org}/tickets/refresh` matches
    `…/tickets/{ticket_id}` -- so it is a 405, not a 404, and a string-equality
    guard calls it a missing path while a naive regex guard calls it served.
    Neither is right.
    """
    call = Call(
        file="<synthetic>",
        line=0,
        verb="POST",
        template="/api/v1/organizations/{organization_id}/tickets/refresh",
        raw="synthetic",
        receiver="synthetic",
        kind="absolute",
    )
    finding = _check(call)
    assert finding is not None, "a removed endpoint was reported as served"
    assert finding.kind in ("wrong-method", "literal-in-param"), finding.kind
    assert any("tickets/{ticket_id}" in n for n in finding.nearest), finding.nearest

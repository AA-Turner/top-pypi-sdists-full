"""Contract-parity guard: every backend operation is reachable from the client.

This is the test that should have existed. `make regen` regenerates
`_generated/models.py` from `schema/openapi.json`, so a new backend route silently
grows a *model* while the hand-written `sdk/client.py` + `cli/main.py` stay blind to
it. Nothing failed, so nobody noticed the client couldn't call it. This test closes
that loop: it diffs the schema against what the client actually calls.

How reachability is decided
---------------------------
We parse the client's real call sites with `ast` rather than regexing source, because
paths are built by f-string (`f"/v1/artifacts/{aid}/confirm"`) and module constant
(`_START_PATH`). Both are resolved to a path *template* — every interpolation becomes
`{}` — and the schema's paths are normalized the same way, so `/v1/runs/{run_ref}`
matches a call site written as `f"/v1/runs/{run_id}"`. Positional structure is what
matters; parameter *names* are the backend's business.

The two allowlists are deliberately different things
----------------------------------------------------
`NOT_CLIENT_SURFACE` is permanent: routes that are somebody else's job (browser, infra,
dashboard). `PENDING` is a debt ledger: routes we intend to reach but haven't. Keeping
them apart stops "not our job" from quietly absorbing "not done yet".

Both are self-cleaning. Three failure modes are enforced (see the tests below): an
unlisted unreachable route fails; an allowlisted route that becomes reachable fails
(delete the entry); an allowlist entry the schema no longer declares fails (the route
was renamed or dropped). So the lists cannot rot into fiction.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_SRC = _ROOT / "src" / "probe"
_SCHEMA = _ROOT / "schema" / "openapi.json"

# Attribute name -> HTTP method, for calls shaped `<receiver>.<verb>("/path", ...)`.
_VERB_ATTRS = {
    "get": "GET",
    "post": "POST",
    "patch": "PATCH",
    "delete": "DELETE",
    "put": "PUT",
    "get_page": "GET",
}
# Calls shaped `x.<name>("METHOD", "/path", ...)` — Transport.request, Client.write.
_METHOD_FIRST = {"request", "write"}
_HTTP_METHODS = {"GET", "POST", "PATCH", "DELETE", "PUT"}

# Both branches gate on the receiver, so a lookalike (`ROUTES.get("/v1/x")` on a plain
# dict, `audit_log.write("POST", "/v1/x")` on a logger) can't be mistaken for an HTTP
# call and mark a route reachable that nothing calls — which would hide the exact gap
# this file exists to find. Everything in this repo reaches the wire through a
# `*transport` attribute; the exceptions are bare httpx clients named `http`
# (sdk/device.py, before a Transport exists) and `client` (mcp/server.py).
_HTTP_RECEIVER_NAMES = {"http", "client"}


def _is_http_receiver(receiver: str) -> bool:
    """Receiver for a verb call (`x.get("/path")`): an HTTP client, not a dict."""
    return receiver.endswith("transport") or receiver in _HTTP_RECEIVER_NAMES


def _is_dispatch_receiver(receiver: str) -> bool:
    """Receiver for a method-first call (`x.write("POST", "/path")`).

    `write`/`request` are common method names (files, buffers, loggers), so the
    method+path shape alone is not enough — `audit_log.write("POST", "/x")` would
    otherwise register. Only the SDK's own dispatchers carry these: `Client.write`
    (receiver `self`), the composed clients (`self.client` / `self._client`), and
    `Transport.request` (`*transport`). A logger/buffer receiver is rejected.
    """
    return (
        receiver == "self"
        or receiver.endswith("client")  # self.client, self._client, a bare `client`
        or _is_http_receiver(receiver)
    )


_PARAM = re.compile(r"\{[^}]*\}")

Op = tuple[str, str]


def _normalize(path: str) -> str:
    """`/v1/runs/{run_ref}/bundle` -> `/v1/runs/{}/bundle`."""
    return _PARAM.sub("{}", path)


def _module_constants(tree: ast.Module) -> dict[str, str]:
    """Module-level `NAME = "string"` / `NAME: str = "string"` (e.g. device.py's
    _START_PATH)."""
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        if not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                out[target.id] = node.value.value
    return out


def _as_path(node: ast.expr, constants: dict[str, str]) -> str | None:
    """Resolve an argument to a path template, or None if it isn't a static path."""
    if isinstance(node, ast.Constant):
        return node.value if isinstance(node.value, str) else None
    if isinstance(node, ast.Name):
        return constants.get(node.id)
    if isinstance(node, ast.JoinedStr):  # f-string
        parts: list[str] = []
        for piece in node.values:
            if isinstance(piece, ast.Constant) and isinstance(piece.value, str):
                parts.append(piece.value)
            elif isinstance(piece, ast.FormattedValue):
                parts.append("{}")
            else:
                return None
        return "".join(parts)
    return None


def _arg_node(node: ast.Call, index: int, keyword: str) -> ast.expr | None:
    """The positional-or-keyword argument expression (`t.get(path=...)` counts)."""
    if len(node.args) > index:
        return node.args[index]
    for kw in node.keywords:
        if kw.arg == keyword:
            return kw.value
    return None


def _arg(node: ast.Call, index: int, keyword: str, constants: dict[str, str]) -> str | None:
    """That argument, resolved to a string."""
    found = _arg_node(node, index, keyword)
    return _as_path(found, constants) if found is not None else None


def _is_opaque_path(node: ast.expr | None) -> bool:
    """True when the path is BUILT by an expression we cannot read — `.format()`,
    `"/".join(...)`, `"/v1/" + x`, `"%s" % x`.

    A bare name or subscript is NOT opaque: that is a generic dispatcher forwarding a
    caller-supplied path (`Client.write`, the spool replay), whose real routes are
    recorded at its own call sites. Flagging those would be noise.
    """
    return isinstance(node, (ast.Call, ast.BinOp))


def _receiver(node: ast.Call) -> str:
    """The call's receiver as source text: `self.transport.get(...)` -> `self.transport`."""
    return ast.unparse(node.func.value) if isinstance(node.func, ast.Attribute) else ""


def _scan(
    src: Path | None = None, root: Path | None = None
) -> tuple[dict[Op, list[str]], list[str]]:
    """Walk the client for HTTP call sites.

    Returns `(operations -> call sites, opaque transport calls)`.

    Only args resolving to a literal starting with "/" are recorded, which is what
    keeps `dict.get("some_key")` and `put_url(absolute_r2_url)` out — neither looks
    like an API path.

    KNOWN LIMIT: only literals, f-strings, and module-level string constants resolve.
    A path built by `.format()`, `+`, `%`, or `"/".join(...)` is invisible here. That
    is why the second return value exists: a `*transport` call whose path is BUILT by
    such an expression is reported, so a new unreadable style fails loudly instead of
    silently marking a route unreachable — or, worse, letting a PENDING entry sit
    there forever after the route was actually wired.
    """
    src, root = src or _SRC, root or _ROOT
    found: dict[Op, list[str]] = {}
    opaque: list[str] = []

    for py in sorted(src.rglob("*.py")):
        tree = ast.parse(py.read_text(), filename=str(py))
        constants = _module_constants(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            where = f"{py.relative_to(root)}:{node.lineno}"
            attr, receiver = node.func.attr, _receiver(node)
            if attr in _METHOD_FIRST and _is_dispatch_receiver(receiver):
                # `write`/`request` need BOTH an HTTP-method arg0 AND a dispatcher
                # receiver: the method string alone would let `audit_log.write("POST",
                # "/x")` through, and the receiver alone would catch `file.write("POST")`
                # (no path). Together they pin it to a real SDK dispatch.
                path_node = _arg_node(node, 1, "path")
                method = _arg(node, 0, "method", constants)
                path = _arg(node, 1, "path", constants)
                if not method or method.upper() not in _HTTP_METHODS:
                    continue
            elif attr in _VERB_ATTRS and _is_http_receiver(receiver):
                path_node = _arg_node(node, 0, "path")
                method, path = _VERB_ATTRS[attr], _arg(node, 0, "path", constants)
            else:
                continue

            if path and path.startswith("/"):
                found.setdefault((method.upper(), _normalize(path)), []).append(where)
            elif _is_dispatch_receiver(receiver) and _is_opaque_path(path_node):
                opaque.append(f"{where}  ({receiver}.{attr}(...))")
    return found, opaque


def client_call_sites() -> dict[Op, list[str]]:
    """Every HTTP operation the client makes, mapped to its `file:line` call sites."""
    return _scan()[0]


def schema_operations() -> dict[Op, str]:
    """Every operation the backend declares, mapped to its operationId."""
    spec = json.loads(_SCHEMA.read_text())
    ops: dict[Op, str] = {}
    for path, item in spec["paths"].items():
        for verb, operation in item.items():
            if verb.upper() not in {"GET", "POST", "PATCH", "DELETE", "PUT"}:
                continue  # `parameters`, `servers`, ... are not operations
            ops[(verb.upper(), _normalize(path))] = operation.get("operationId", "?")
    return ops


# --------------------------------------------------------------------------
# Allowlist 1: PERMANENT. Not the SDK/CLI's job. Every entry states why.
# --------------------------------------------------------------------------
NOT_CLIENT_SURFACE: dict[Op, str] = {
    # RETIRING, not unwired. An experiment IS a project now, and the client
    # reads this document at `/v1/projects/{}/notes/versions/{}` -- the same
    # rows, from the address that survives the route cut. The experiment path
    # still exists on the server for old clients and becomes a 410 at the cut,
    # at which point this entry fails the self-cleaning check and gets deleted
    # along with the route. That is the intended lifecycle, not an oversight.
    (
        "GET",
        "/v1/experiments/{}/notes/versions/{}",
    ): "retiring with the experiment routes; the client reads it at the project address",
    ("POST", "/v1/sessions/{}/anchors"): "explicit dashboard session association; historical backfill keeps sessions standalone",
    ("GET", "/v1/sessions/{}/artifacts/tree"): "dashboard lazy browsing of session artifacts",
    ("GET", "/v1/sessions/{}/receipts"): "authenticated operator receipt inspection; the capture producer uses the device-scoped endpoint",
    ("GET", "/ingest/v1/sessions/{}/{}/receipts"): "paired-device protocol, reached by tap_core.session_journal.Wire through urllib rather than the SDK transport",
    # PRB-011: this route is now `include_in_schema=False`, so it is absent from a
    # freshly regenerated snapshot. The committed snapshot still carries it (it was
    # not regenerated to avoid dragging in unrelated schema drift), which keeps
    # parity green today. DELETE this line at the next `make regen` -- otherwise
    # `test_allowlisted_operations_still_exist_in_the_schema` will fail on a route
    # the regenerated schema no longer declares.
    ("POST", "/internal/github/installation_token"): "engine-to-control-plane credential broker; internal authentication only",
    ("POST", "/v1/search/entities"): "dashboard structured entity-search adapter; SDK search uses the general search endpoint",
    ("GET", "/v1/integrations/capabilities"): "dashboard connector-detail rollout switch",
    ("GET", "/v1/integrations/github/installations/{}/backfills"): "dashboard installation history-job controls",
    ("POST", "/v1/integrations/github/installations/{}/backfills"): "dashboard reviewed installation history-job creation",
    ("GET", "/v1/integrations/github/installations/{}/backfills/{}"): "dashboard installation history-job progress",
    ("POST", "/v1/integrations/github/installations/{}/backfills/{}/cancel"): "dashboard installation history-job cancellation",
    ("POST", "/v1/integrations/github/installations/{}/backfills/{}/retry"): "dashboard installation history-job retry",
    ("GET", "/v1/integrations/github/installations/{}/purge-preview"): "dashboard installation-removal review",
    ("GET", "/v1/integrations/github/installations/{}/scope-options"): "dashboard installation history scope picker",
    ("GET", "/v1/integrations/github/installations/{}/sync"): "dashboard installation live-sync controls",
    ("PATCH", "/v1/integrations/github/installations/{}/sync"): "dashboard installation live-sync controls",
    ("GET", "/v1/integrations/mirror/connections/{}/backfills"): "dashboard mirror connection history-job controls",
    ("POST", "/v1/integrations/mirror/connections/{}/backfills"): "dashboard reviewed mirror connection history-job creation",
    ("GET", "/v1/integrations/mirror/connections/{}/backfills/{}"): "dashboard mirror connection history-job progress",
    ("POST", "/v1/integrations/mirror/connections/{}/backfills/{}/cancel"): "dashboard mirror connection history-job cancellation",
    ("POST", "/v1/integrations/mirror/connections/{}/backfills/{}/retry"): "dashboard mirror connection history-job retry",
    ("GET", "/v1/experiments/{}/artifacts/tree"): "dashboard lazy folder browsing; CLI uses experiment artifact listing",
    ("GET", "/public/v1/projects/{}/artifacts/tree"): "anonymous dashboard lazy folder browsing",
    ("GET", "/public/v1/experiments/{}/artifacts/tree"): "anonymous dashboard lazy folder browsing",
    ("GET", "/public/v1/runs/{}/artifacts/tree"): "anonymous dashboard lazy folder browsing",
    # 2026-09-04: the browser-side OAuth consent page (a human clicks it);
    # surfaced by the dump-openapi that accompanied 0193.
    ("GET", "/oauth/consent"): "browser consent page, never called by the SDK",
    ("GET", "/healthz"): "infra liveness probe; not a client call",
    ("GET", "/livez"): "infra liveness probe; not a client call",
    # The device-retirement review. Deliberately dashboard-only: retiring is a
    # judgment about machines the SERVER cannot make -- a legacy capture row has
    # no stable identity, and two laptops can share a hostname -- so it needs a
    # human looking at the evidence and ticking boxes. A CLI verb would either
    # re-create that UI in a terminal or invite the "retire everything that looks
    # old" heuristic the whole flow exists to refuse.
    (
        "POST",
        "/v1/client-installations/retire",
    ): "dashboard-only; the remove control on a credential-less client row",
    # MCP OAuth: for third-party MCP clients doing browser-based auth against the
    # hosted MCP server. `probe` is the non-agent surface and authenticates with a PAT.
    (
        "GET",
        "/.well-known/oauth-authorization-server",
    ): "MCP OAuth discovery; browser/agent surface",
    ("GET", "/oauth/authorize"): "MCP OAuth; browser surface",
    ("POST", "/oauth/consent"): "MCP OAuth; browser surface",
    ("GET", "/oauth/jwks"): "MCP OAuth; key discovery for token verifiers",
    ("POST", "/oauth/register"): "MCP OAuth dynamic client registration; agent surface",
    ("POST", "/oauth/token"): "MCP OAuth; browser/agent surface",
    # The team note's whole-document save is DELIBERATELY not a client surface
    # (0125). Agents write it with append and edit, which are lossless: replacing
    # the whole document means holding it in context and re-emitting it to change
    # one line, dropping whatever the agent did not think to repeat. The dashboard
    # keeps this route because a person editing in a browser can see what they are
    # overwriting and gets a version-checked save. Wiring it into the SDK would
    # hand an agent exactly the primitive the design removes.
    ("PUT", "/v1/team-note"): (
        "dashboard-only whole-document save. It does NOT merge -- a person is "
        "looking at the document, so telling them it moved beats handing them a "
        "merged result they did not ask for. Agents use POST /v1/team-note/sync, "
        "which does merge and IS wired."
    ),
    # The dashboard assistant's two server-computed writes. Not client surface
    # because the client has a FILE: it syncs whole documents and never needs the
    # server to compute a change for it. These exist for the one caller that has
    # no filesystem and structurally cannot read the document to rewrite it (the
    # note's cap is exactly the assistant's tool-result budget), so the server
    # does its read-modify-write. Wiring them into the SDK would hand a client
    # that already has the whole document a second, weaker way to change it.
    ("POST", "/v1/team-note/apply/paragraph"): (
        "dashboard-assistant surface; SDK clients sync the whole file instead"
    ),
    ("POST", "/v1/team-note/apply/span"): (
        "dashboard-assistant surface; SDK clients sync the whole file instead"
    ),
    # Browser OIDC legs: redirects, not JSON.
    ("GET", "/auth/login"): "browser OIDC redirect leg",
    ("GET", "/auth/callback"): "browser OIDC redirect leg",
    (
        "POST",
        "/auth/logout",
    ): "clears the session cookie; the CLI revokes via DELETE /v1/tokens/current",
    # Session-only by construction. A PAT is bound to one team at the row level and
    # /v1/me deliberately reports one tenant, so these cannot answer a token caller.
    ("GET", "/auth/me"): "session-only; /v1/me is the machine-credential door and IS wired",
    ("POST", "/auth/onboarding"): "session-only; the dashboard saves website onboarding progress",
    ("POST", "/auth/switch-team"): (
        "session-only. A PAT is team-bound at the row level, so this 403s for the CLI. "
        "Teams are not a switchable axis; workspaces are (2026-07-15 decision)."
    ),
    ("POST", "/auth/teams"): "session-only team admin; dashboard surface",
    (
        "GET",
        "/auth/teams/members",
    ): "session-only (require_team_role -> require_session); dashboard surface",
    ("PATCH", "/auth/teams/members/{}"): "session-only team admin; dashboard surface",
    ("DELETE", "/auth/teams/members/{}"): "session-only team admin; dashboard surface",
    ("GET", "/auth/teams/invites"): "session-only team admin; dashboard surface",
    ("POST", "/auth/teams/invites"): "session-only team admin; dashboard surface",
    ("DELETE", "/auth/teams/invites/{}"): "session-only team admin; dashboard surface",
    ("POST", "/auth/teams/invites/{}/resend"): "session-only team admin; dashboard surface",
    # Same family as the rows above and the same dependency (`_OWNER` ->
    # require_team_role -> require_session), so a PAT gets a 403 here, not a
    # result. Surfaced 2026-08-06 by the `make dump-openapi` in the team-note
    # pass: it shipped on the backend while the checked-in schema sat stale.
    ("POST", "/auth/teams/transfer-ownership"): "session-only team admin; dashboard surface",
    # Deletes the signed-in IDENTITY, not team data, and is gated on
    # `require_session`. Structurally not a token surface: a PAT is bound to one
    # team at the row level and names no browser identity to delete.
    ("DELETE", "/auth/account"): "session-only account deletion; dashboard surface",
    ("GET", "/auth/invites/pending"): "session-only; dashboard surface",
    ("POST", "/auth/invites/{}/accept"): "session-only; dashboard surface",
    # The device-flow approval leg is the human's half of the handshake: the CLI
    # starts (/auth/device/code) and exchanges (/auth/device/token) — both wired —
    # while a signed-in human approves in the dashboard's /authorize page.
    (
        "GET",
        "/auth/device/requests/{}",
    ): "session-only; the dashboard /authorize page is the human surface",
    (
        "POST",
        "/auth/device/requests/{}",
    ): "session-only; the dashboard /authorize page approves/denies",
    (
        "POST",
        "/auth/device/install-code",
    ): "session-only; the dashboard issues the install code that the CLI redeems",
    # Deliberate security invariant, not an oversight: "a leaked token must not be
    # able to mint more tokens" (app/auth/token_router.py). It rejects PATs outright,
    # so `probe token create` drives the device flow instead — a human approves in
    # the browser and the same backend mints exactly one PAT.
    (
        "POST",
        "/v1/tokens",
    ): "session-only mint by design; `probe token create` uses the device flow",
    # Inbound webhook: GitHub POSTs here (HMAC-verified), the `probe` client never
    # calls it. Structurally not a client surface, like the liveness probes.
    ("POST", "/webhooks/github"): "inbound GitHub webhook; server receives, client never calls",
    # GitHub knowledge-connector management. DECISION (2026-07-16): never CLI surface.
    # The CLI interacts with our own data; installing a connector is a browser OAuth
    # flow, and connector admin lives in the dashboard alongside team admin.
    (
        "POST",
        "/v1/integrations/github/installations",
    ): "browser OAuth install flow; dashboard surface",
    ("DELETE", "/v1/integrations/github/installations/{}"): "connector admin; dashboard surface",
    ("GET", "/v1/integrations/ingestion"): "connector status for the dashboard's Integrations page",
    (
        "GET",
        "/v1/integrations/ingestion/{}/devices",
    ): "per-device connector stats for the dashboard",
    (
        "GET",
        "/v1/integrations/{}/backfill",
    ): "backfill progress for a dashboard spinner; carries no data the CLI lacks",
    # Integrations v2 mirror lane (#1321, 0187_mirrored_objects). Same family as
    # the connector-admin routes above: connecting a mirror is a browser flow
    # (credential + scope pickers), and the purge preview is the dashboard's
    # "are you sure" affordance. Surfaced by the 0193 `dump-openapi`; the lane
    # landed without re-snapshotting the schema.
    ("POST", "/v1/integrations/mirror/connections"): "connector admin; dashboard surface",
    ("DELETE", "/v1/integrations/mirror/connections/{}"): "connector admin; dashboard surface",
    ("PATCH", "/v1/integrations/mirror/connections/{}"): "connector admin; dashboard surface",
    (
        "GET",
        "/v1/integrations/mirror/connections/{}/purge-preview",
    ): "purge confirmation preview for the dashboard",
    (
        "POST",
        "/v1/integrations/mirror/connections/{}/reconnect",
    ): "browser reconnect flow; dashboard surface",
    ("GET", "/v1/client-status"): "authenticated update-banner decision for the dashboard",
    # Summary generation machinery. DECISION (2026-07-16, re-verified 2026-07-17 against
    # the v0.29.0.0 run-anchor/storage rewrite): these carry NO data. The generated
    # summary persists to the anchor entity's `metadata.summary`, already readable
    # through ProjectOut/ExperimentOut/RunOut, which ARE wired. The routes are async
    # (202 + enqueue) whose fresh/generating/stale states drive a dashboard spinner, and
    # a `probe summary` group would invent a noun outside project->experiment->run.
    (
        "POST",
        "/v1/runs/{}/summary/generate",
    ): "async generation machinery; the summary itself is on RunOut",
    ("GET", "/v1/runs/{}/summary/status"): "dashboard spinner state; carries no data",
    (
        "POST",
        "/v1/trials/{}/summary/generate",
    ): "async generation machinery; the summary itself is on TrialOut",
    ("GET", "/v1/trials/{}/summary/status"): "dashboard spinner state; carries no data",
    # Overview pages (0199): the page IS the project's/experiment's summary on a
    # tenant admitted to the lane, and the LANE writes it -- there is no agent
    # write door any more, so there is nothing here for the SDK to wire.
    # Reading one back is the dashboard's sandboxed frame, the regenerate
    # button is the same async machinery as summary/regenerate, and the status
    # route is its spinner. The short form every other surface needs
    # (`metadata.overview.blurb`) already rides on ProjectOut/ExperimentOut.
    ("GET", "/v1/projects/{}/overview"): "dashboard frame; the blurb is on ProjectOut",
    (
        "POST",
        "/v1/projects/{}/overview/regenerate",
    ): "async generation machinery; the button on the Overview tab",
    # Notes history is the dashboard document editor's recovery surface. The
    # agent's mutation contract stays deliberately smaller: append and edit are
    # concurrency-safe and now cover all six carriers, including Trial. Adding
    # eighteen history/restore verbs to the CLI would duplicate that editor
    # without improving the write path agents actually use.
    ("GET", "/v1/projects/{}/notes/versions"): "dashboard notes history surface",
    (
        "POST",
        "/v1/projects/{}/notes/versions/{}/restore",
    ): "dashboard notes history restore surface",
    ("GET", "/v1/experiments/{}/notes/versions"): "dashboard notes history surface",
    (
        "POST",
        "/v1/experiments/{}/notes/versions/{}/restore",
    ): "dashboard notes history restore surface",
    ("GET", "/v1/runs/{}/notes/versions"): "dashboard notes history surface",
    (
        "POST",
        "/v1/runs/{}/notes/versions/{}/restore",
    ): "dashboard notes history restore surface",
    ("GET", "/v1/groups/{}/notes/versions"): "dashboard notes history surface",
    (
        "POST",
        "/v1/groups/{}/notes/versions/{}/restore",
    ): "dashboard notes history restore surface",
    ("GET", "/v1/artifacts/{}/notes/versions"): "dashboard notes history surface",
    ("GET", "/v1/artifacts/{}/notes/versions/{}"): "dashboard notes history surface",
    (
        "POST",
        "/v1/artifacts/{}/notes/versions/{}/restore",
    ): "dashboard notes history restore surface",
    # Relays bounded, allowlisted blob bytes inline for the dashboard's file viewer.
    # The CLI's door to real bytes is GET /v1/artifacts/{}/download, which IS wired.
    ("GET", "/v1/artifacts/{}/preview"): "inline UI viewer relay; the CLI uses /download",
    # The README panels (0118/0150). These return markdown already rewritten for a
    # BROWSER — image sources point at artifact preview routes the dashboard
    # resolves against its own `/api` origin — so the value is meaningless
    # anywhere else. What the CLI and SDK genuinely need is `repo` on the entity
    # itself, and that IS reachable through its detail read.
    ("GET", "/v1/projects/{}/readme"): "dashboard render surface; the SDK reads project.repo",
    (
        "GET",
        "/v1/experiments/{}/readme",
    ): "dashboard render surface; the SDK reads experiment.repo",
    ("GET", "/v1/runs/{}/readme"): "dashboard render surface; the SDK reads run.repo",
    (
        "GET",
        "/public/v1/projects/{}/readme",
    ): "anonymous published-page render surface; no client identity to use it",
    (
        "GET",
        "/public/v1/experiments/{}/readme",
    ): "anonymous published-page render surface; no client identity to use it",
    (
        "GET",
        "/public/v1/runs/{}/readme",
    ): "anonymous published-page render surface; no client identity to use it",
    (
        "GET",
        "/v1/projects/{}/subtree",
    ): "dashboard project-directory expansion; the SDK exposes direct child listing",
    # The W&B connect/import flow, driven entirely by the dashboard
    # (dashboard/src/lib/api/wandb.ts). NOT the same mechanism as `probe import
    # wandb`, which mirrors history into an existing run by talking to W&B
    # directly and never touches these routes.
    #
    # Listed here in the 0118 branch because that branch regenerated
    # schema/openapi.json, which had not been refreshed since #612 added them —
    # the routes shipped, the snapshot did not, so the guard had nothing to
    # check. Pre-existing, surfaced rather than introduced.
    (
        "POST",
        "/v1/integrations/wandb/connect",
    ): "dashboard W&B connect flow; the CLI mirrors from W&B directly",
    (
        "GET",
        "/v1/integrations/wandb",
    ): "dashboard W&B connect flow; the CLI mirrors from W&B directly",
    (
        "GET",
        "/v1/integrations/wandb/projects",
    ): "dashboard W&B connect flow; the CLI mirrors from W&B directly",
    (
        "POST",
        "/v1/integrations/wandb/imports",
    ): "dashboard W&B import flow; the CLI mirrors from W&B directly",
    (
        "GET",
        "/v1/integrations/wandb/imports/{}",
    ): "dashboard W&B import progress polling",
    (
        "DELETE",
        "/v1/integrations/wandb/connection/{}",
    ): "dashboard W&B connect flow; the CLI mirrors from W&B directly",
    # Mirror connections (/v1/integrations/mirror/*, integrations-v2): a
    # dashboard-only connector-admin surface. NOT listed yet ON PURPOSE — the
    # committed openapi.json predates those routes and this file's
    # self-cleaning check rejects allowlist entries for operations the
    # snapshot does not declare. Whoever runs the next `make regen` adds the
    # seven NOT_CLIENT_SURFACE entries alongside the snapshot update.
    # Reached by the probe-research-tap PLUGIN (plugins/probe-research-tap/tap/), not by
    # the SDK/CLI under src/probe/ that this file scans. The tap builds its URLs by
    # concatenation, so they cannot resolve here — but it pins both paths in its own
    # tests (tests/test_base_url.py, tests/test_killswitch.py), so they stay guarded.
    (
        "POST",
        "/ingest/v1/sessions/claude-code",
    ): "tap plugin surface; path pinned by the tap's own tests",
    (
        "GET",
        "/ingest/v1/sessions/status",
    ): "tap plugin killswitch; path pinned by the tap's own tests",
    # 0231 -- THE EXPERIMENT SURFACE THE CLIENT HAS ALREADY LEFT.
    #
    # An experiment IS a project now, and every one of these has a
    # `/v1/projects/*` twin sharing its implementation --
    # `tests/unit/test_every_experiment_route_has_a_project_twin.py` in the
    # backend proves all 45 pairs exist, and the SDK calls the project address
    # for every one of them. PR 5b deletes these routes and answers them with a
    # 410 naming the replacement.
    #
    # NOT "PENDING": there is no work owed here. Wiring the client back up to a
    # route that is being retired is the opposite of what the merge is for, and
    # the entries leave this list when the routes themselves do.
    #
    # THE CLIENT MOVED FIRST, DELIBERATELY. A client that moves before the cut
    # keeps working across it; one that moves with it has a window where neither
    # address is certain.
    (
        "GET",
        "/v1/experiments",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "DELETE",
        "/v1/experiments/{}",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "PATCH",
        "/v1/experiments/{}",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/artifacts",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/artifacts",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/artifacts/uploads",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/code",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/edges",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/groups",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/groups",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/reproduce",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/runs",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/sub-notes",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "PATCH",
        "/v1/experiments/{}/sub-notes",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/sub-notes",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/versions",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/versions",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/versions/{}",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "GET",
        "/v1/experiments/{}/wandb-sources",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "POST",
        "/v1/experiments/{}/wandb-sources",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "DELETE",
        "/v1/experiments/{}/wandb-sources/{}",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    (
        "PATCH",
        "/v1/experiments/{}/wandb-sources/{}",
    ): "retired by 0231; the client calls the /v1/projects twin, and PR 5b deletes this",
    # Dashboard-owned, both of them, and both surfaced by the snapshot refresh
    # this branch ran rather than introduced by it.
    (
        "PUT",
        "/v1/projects/{}/metadata/{}",
    ): "dashboard-owned metadata allowlist (compare layouts); no CLI surface",
    (
        "POST",
        "/v1/projects/{}/summary/generate",
    ): "0231 alias of summary/regenerate, added so the experiment surface maps by one segment; the client calls neither",
}

# --------------------------------------------------------------------------
# Allowlist 2: TEMPORARY debt. Routes we intend to reach but have not yet.
# --------------------------------------------------------------------------
# EMPTY, and that is the point — every route the backend declares is now either
# reachable from the client or permanently and explicitly not our job.
#
# It held 15 entries until the workspace-context pass (2026-07-20): the 12 workspace
# and project-anchor routes were wired (`probe workspace`, `probe project`, and the
# anchor-generalized `probe artifact add`), and the 3 GitHub-connector routes were
# resolved to a permanent decision rather than left pending — they moved up into
# NOT_CLIENT_SURFACE with their reasoning.
#
# Keep this dict. An empty debt ledger is the healthy state, not a dead structure:
# the next backend fold that lands ahead of the client goes here, with a pointer to
# what will close it, instead of being quietly absorbed into "not our job".
PENDING: dict[Op, str] = {
    # The companion daemon's model gateway (research-os companion-server
    # branch). The daemon that calls it is built on its own branch; when it
    # lands, `test_allowlisted_operations_are_still_unreachable` fails here
    # and this entry is deleted with it.
    ("POST", "/v1/companion/complete"): "companion daemon lane; its client ships separately",
    # Surfaced 2026-09-21 by the `dump-openapi` that accompanied the
    # `summary_markdown` retirement (0220), second batch: main landed the
    # workspace/project access routes (#1769) while this branch was out. Newly
    # VISIBLE debt, nothing to do with the retirement; it belongs to the lane
    # that shipped it. The W&B account PATCH was in this batch too and came
    # straight back out: `test_allowlisted_operations_are_still_unreachable`
    # refuses an entry the client CAN reach, which is the half of this guard
    # that stops the allowlist becoming a place routes go to be forgotten.
    ("GET", "/v1/projects/{}/access"): "workspace permissions lane, #1769",
    ("PUT", "/v1/projects/{}/access"): "workspace permissions lane, #1769",
    ("GET", "/v1/workspaces/{}/access"): "workspace permissions lane, #1769",
    ("PUT", "/v1/workspaces/{}/access"): "workspace permissions lane, #1769",
    # Surfaced 2026-09-20 by the `dump-openapi` that accompanied the
    # `summary_markdown` retirement (0220). Same story as every batch below:
    # the Overview page routes (0217/0218) and the workspace-writers routes
    # shipped on the backend while the checked-in schema sat stale, so this
    # guard could not see them. Newly VISIBLE debt, nothing to do with the
    # retirement; they belong to the lanes that shipped them.
    ("PUT", "/v1/projects/{}/overview/page"): "overview page lane, backend 0218",
    ("GET", "/v1/projects/{}/overview/versions"): "overview page lane, backend 0217",
    ("GET", "/v1/projects/{}/overview/versions/{}"): "overview page lane, backend 0217",
    ("POST", "/v1/projects/{}/overview/versions/{}/restore"): "overview page lane, backend 0217",
    ("GET", "/v1/projects/{}/writers"): "workspace writers lane, backend 0214",
    ("PUT", "/v1/projects/{}/writers"): "workspace writers lane, backend 0214",
    ("PUT", "/v1/artifact-upload-bytes"): "artifact upload lane",
    # Surfaced 2026-09-09 by the `dump-openapi` that accompanied the session
    # digest cutover (0204). Same story as every batch below: the W&B
    # connection-delete route (#1506) shipped on the backend while the
    # checked-in schema sat stale, so this guard could not see it. Newly
    # VISIBLE debt, nothing to do with the cutover; it belongs to the mirror
    # lane that shipped it.
    ("DELETE", "/v1/integrations/wandb/accounts/{}/record"): "W&B mirror lane, #1506",
    # Surfaced 2026-09-04 by the `dump-openapi` that accompanied 0193. Same
    # story as every batch below: the workspace-digest route (0186) shipped on
    # the backend while the checked-in schema sat stale, so this guard could
    # not see it. Newly VISIBLE debt, nothing to do with code capture; it
    # belongs to the workspace-digest lane that shipped it.
    ("GET", "/v1/workspace-digest"): "workspace-digest lane, backend 0186",
    ("POST", "/v1/workspace-digest/refresh"): "workspace-digest lane, backend 0186",
    # Surfaced 2026-09-02 by the `dump-openapi` that accompanied run rewind
    # (0185). Same story as every batch below: the paper-artifacts routes
    # (0184) shipped on the backend while the checked-in schema sat stale, so
    # this guard could not see them. Newly VISIBLE debt, nothing to do with
    # rewind; they belong to the papers lane that shipped them.
    ("GET", "/v1/papers/{}/artifacts"): "papers lane, backend 0184",
    ("POST", "/v1/papers/{}/artifacts"): "papers lane, backend 0184",
    ("POST", "/v1/papers/{}/artifacts/uploads"): "papers lane, backend 0184",
    # Surfaced 2026-08-13 by the `dump-openapi` that accompanied the
    # short_id -> slug rename (0109). Same story as the 2026-07-21 batch below:
    # these shipped on the backend while the checked-in schema sat stale, so this
    # guard could not see them. NOT new debt and nothing to do with the rename --
    # newly VISIBLE debt, which is the guard working as designed.
    # Surfaced 2026-08-18 by a `dump-openapi` pass. Same story again: a backend
    # route shipped without regenerating the schema, so
    # this guard was blind to it and main passed on a stale file. Newly VISIBLE
    # debt, not new debt -- the route belongs beside the rebuild controls above,
    # which are dashboard-only for the same reason.
    # The five coordinate/telemetry read shapes (research-os#162 + #177:
    # metrics grouped/wide/export, the coordinate catalog, /v1/series/latest)
    # cleared this ledger in the coordinate read-surface pass (B7): they are
    # now literal call sites in sdk/client.py, surfaced through the CLI's
    # metrics/coordinates/series verbs and the read-only MCP tools.
    #
    # Surfaced 2026-07-21 by the first `make dump-openapi` in a while: these
    # routes shipped on the backend while the checked-in schema sat stale, so
    # this guard could not see them. They are not new debt, only newly VISIBLE
    # debt -- which is the guard working as designed.
    #
    # Device pairing (backend v0.17.0.0). The pairing flow lives in the
    # dashboard and the imsg/agent-tap plugin; whether `probe` should also drive
    # it from the CLI is an open product question, not a wiring oversight.
    # Surfaced 2026-08-31 by the `dump-openapi` that accompanied the
    # client-installation naming route. Same story as every batch above: both
    # shipped on the backend while the checked-in schema sat stale, so this
    # guard could not see them. NOT new debt and nothing to do with that route
    # -- newly VISIBLE debt, which is the guard working as designed.
    ("GET", "/v1/chart-settings"): "dashboard-only chart axis config; no CLI verb proposed",
    ("POST", "/agent-tap/pair"): "device pairing; dashboard + agent-tap plugin surface today",
    ("POST", "/agent-tap/revoke"): "device pairing; dashboard + agent-tap plugin surface today",
    ("POST", "/v1/pairing-tokens"): "device pairing; mint flow is dashboard-driven today",
    ("GET", "/v1/devices"): "paired-device list; dashboard surface today",
    ("DELETE", "/v1/devices/{}"): "unpair; dashboard surface today",
    # Surfaced 2026-08-24 by the `dump-openapi` that accompanied the Trial
    # notes-carrier removal. The note-publishing surface (#900 team note, #918
    # per-entity) shipped on the backend while the checked-in schema sat stale,
    # so this guard was blind to it and main passed on a stale file. Newly
    # VISIBLE debt, not new debt, and NOT this branch's to wire: publishing a
    # note is a dashboard share control today, the same shape as every other
    # `/public` grant already listed here.
    # The sub-note SDK/CLI half (PR3 of that train) landed and deleted the
    # eighteen "not this branch's to wire" entries the dump-openapi sweep had
    # added. What stays is the HISTORY surface: versions, one version, restore
    # — dashboard reads/writes today, with no SDK caller by design (the CLI
    # reads documents, not their history).
    # Surfaced 2026-08-31 by the `dump-openapi` that accompanied paper lineage
    # (0176). THIRD time this exact story appears in this file, which is itself
    # the finding: each of these shipped on the backend while the checked-in
    # schema sat stale, so this guard was blind to them and main passed on a
    # stale file. Newly VISIBLE debt, not new debt, and not this branch's to
    # wire -- the two routes paper lineage actually added (GET
    # /v1/projects/{}/paper-edges, DELETE /v1/edges/{}) are real SDK + CLI call
    # sites (`probe paper edges`, `probe edge remove`) and deliberately absent
    # from this list.
    #
    # Chart-settings and metric-view HISTORY are the same dashboard-only shape
    # as the sub-note history entries below: version lists, one version, and a
    # revert control, all driven from chart UI that has no CLI equivalent.
    ("GET", "/v1/chart-settings/versions"): "chart history; dashboard-only read today",
    (
        "GET",
        "/v1/chart-settings/versions/{}",
    ): "chart history; dashboard-only read today",
    ("POST", "/v1/chart-settings/revert"): "chart revert; dashboard-only write today",
    ("GET", "/v1/views/{}/versions"): "metric-view history; dashboard-only read today",
    (
        "GET",
        "/v1/views/{}/versions/{}",
    ): "metric-view history; dashboard-only read today",
    ("POST", "/v1/views/{}/revert"): "metric-view revert; dashboard-only write today",
    # Paper BODY fetch (0173). Reader-facing: the dashboard opens a paper and
    # streams its parsed text from a 24h cache. Nothing an agent scripting the
    # CLI wants -- it already has the paper's URL; the MCP's `find_papers`
    # reads literature through its paper index.
    ("GET", "/v1/papers/{}/content"): "paper reader; dashboard-only read today",
    # Same sweep, same story: the paper DIGEST routes (#1200) landed days before
    # this branch and their schema was never re-dumped either. Both are driven
    # from the paper detail page -- the dashboard reads the digest and offers a
    # regenerate control beside it -- and an agent scripting the CLI wants the
    # paper's own fields, not a generated summary of them.
    ("GET", "/v1/papers/{}/digest"): "paper digest; dashboard-only read today",
    (
        "POST",
        "/v1/papers/{}/digest/regenerate",
    ): "paper digest regenerate; dashboard-only control today",
    ("GET", "/v1/sub-notes/{}/versions"): "sub-note history; dashboard-only read today",
    (
        "GET",
        "/v1/sub-notes/{}/versions/{}",
    ): "sub-note history; dashboard-only read today",
    (
        "POST",
        "/v1/sub-notes/{}/versions/{}/restore",
    ): "sub-note restore; dashboard-only write today",
    ("GET", "/public/v1/notes/{}"): "anonymous published note; dashboard share surface",
    (
        "GET",
        "/public/v1/notes/{}/versions",
    ): "anonymous published note history; dashboard share surface",
    (
        "GET",
        "/public/v1/notes/{}/versions/{}",
    ): "anonymous published note version; dashboard share surface",
    ("PUT", "/v1/projects/{}/notes/public"): "note share control; dashboard surface today",
    ("GET", "/v1/projects/{}/notes/public"): "note share control; dashboard surface today",
    ("DELETE", "/v1/projects/{}/notes/public"): "note share control; dashboard surface today",
    ("PUT", "/v1/experiments/{}/notes/public"): "note share control; dashboard surface today",
    ("GET", "/v1/experiments/{}/notes/public"): "note share control; dashboard surface today",
    (
        "DELETE",
        "/v1/experiments/{}/notes/public",
    ): "note share control; dashboard surface today",
    ("PUT", "/v1/runs/{}/notes/public"): "note share control; dashboard surface today",
    ("GET", "/v1/runs/{}/notes/public"): "note share control; dashboard surface today",
    ("DELETE", "/v1/runs/{}/notes/public"): "note share control; dashboard surface today",
    ("PUT", "/v1/team-note/public"): "team-note share control; dashboard surface today",
    ("GET", "/v1/team-note/public"): "team-note share control; dashboard surface today",
    ("DELETE", "/v1/team-note/public"): "team-note share control; dashboard surface today",
    # Operator actions with no CLI story yet.
    ("POST", "/v1/integrations/ingestion/retry-dlq"): "operator action; no CLI verb designed yet",
    (
        "DELETE",
        "/v1/workspaces/{}/files/{}",
    ): "workspace file delete; `probe` has no file-rm verb yet",
    #
    # Surfaced 2026-08-03 by the `make dump-openapi` in the search/lineage pass:
    # this shipped on the backend while the checked-in schema sat stale. Newly
    # VISIBLE debt, not new debt, and unrelated to that pass -- wiring it there
    # would have been scope creep. Same shape as the two batches below.
    (
        "PUT",
        "/v1/experiments/{}/metadata/{}",
    ): "experiment metadata set; `probe` has no metadata verb yet",
    #
    # Surfaced 2026-08-02 by the `make regen` in the archive-removal pass: the
    # public share-links surface (research-os#226) and two sandbox-state reads
    # shipped on the backend while the checked-in schema sat stale. Newly
    # VISIBLE debt, not new debt -- the same shape as the 2026-07-21 batch
    # above, and the same guard doing its job. Nothing here is archive-related.
    (
        "GET",
        "/public/v1/experiments/{}",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/experiments/{}/artifacts",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "POST",
        "/public/v1/experiments/{}/artifacts/{}/download",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/experiments/{}/artifacts/{}/preview",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/experiments/{}/runs",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/info",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/papers/{}",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/projects/{}",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/projects/{}/artifacts",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "POST",
        "/public/v1/projects/{}/artifacts/{}/download",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/projects/{}/artifacts/{}/preview",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/projects/{}/experiments",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/projects/{}/runs",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/artifacts",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "POST",
        "/public/v1/runs/{}/artifacts/{}/download",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/artifacts/{}/preview",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/bundle",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/coordinates",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/lineage",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/metrics/export",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/metrics/grouped",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/metrics/wide",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/sandbox-state/diff",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/sandbox-state/file",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/spans",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "POST",
        "/public/v1/series/query",
    ): "public share read; unauthenticated browser surface, no client story yet",
    ("DELETE", "/v1/experiments/{}/public"): "share-links publish control; dashboard surface today",
    ("GET", "/v1/experiments/{}/public"): "share-links publish control; dashboard surface today",
    ("PUT", "/v1/experiments/{}/public"): "share-links publish control; dashboard surface today",
    ("DELETE", "/v1/projects/{}/public"): "share-links publish control; dashboard surface today",
    ("GET", "/v1/projects/{}/public"): "share-links publish control; dashboard surface today",
    ("PUT", "/v1/projects/{}/public"): "share-links publish control; dashboard surface today",
    ("DELETE", "/v1/papers/{}/public"): "share-links publish control; dashboard surface today",
    ("GET", "/v1/papers/{}/public"): "share-links publish control; dashboard surface today",
    ("PUT", "/v1/papers/{}/public"): "share-links publish control; dashboard surface today",
    ("GET", "/v1/public-access"): "share-links publish control; dashboard surface today",
    ("DELETE", "/v1/runs/{}/public"): "share-links publish control; dashboard surface today",
    ("GET", "/v1/runs/{}/public"): "share-links publish control; dashboard surface today",
    ("PUT", "/v1/runs/{}/public"): "share-links publish control; dashboard surface today",
    (
        "GET",
        "/v1/runs/{}/sandbox-state/diff",
    ): "sandbox-state read; `probe trial` reads these through the bundle today",
    (
        "GET",
        "/v1/runs/{}/sandbox-state/file",
    ): "sandbox-state read; `probe trial` reads these through the bundle today",
    #
    # Same batch, second pass: chart settings (research-os 0078) and the session
    # work/artifact-session reads (0084) landed on the backend after the earlier
    # snapshot too. Dashboard surfaces today; no `probe` verb designed yet.
    ("PUT", "/v1/chart-settings"): "chart presentation state; dashboard surface today",
    ("DELETE", "/v1/chart-settings"): "chart presentation state; dashboard surface today",
    ("GET", "/v1/artifacts/{}/sessions"): "artifact session roll-up; dashboard surface today",
    #
    # The six PRIVATE metric-view routes (research-os 0087-0089) were parked here
    # on 2026-08-03 as "dashboard surface today" and cleared the same day: the
    # dashboard turned out to be the WRONG authoring surface. An expression comes
    # from an agent session or a script, so `probe.expr` + `probe views` are the
    # door, and the dashboard only renders/renames/deletes. They are call sites in
    # sdk/client.py now.
    (
        "GET",
        "/public/v1/runs/{}/views",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/views/{}/data",
    ): "public share read; unauthenticated browser surface, no client story yet",
    (
        "GET",
        "/public/v1/runs/{}/trials/{}",
    ): "anonymous published Trial page; the authenticated SDK uses /v1/trials/{}",
    (
        "GET",
        "/public/v1/runs/{}/trials",
    ): "anonymous published Trial inventory; the SDK uses authenticated /v1/runs/{}/trials",
    # --- surfaced 2026-08-12 by the first schema refresh in a while ----------
    # These eleven are not new debt. They are debt this test could not SEE:
    # `schema/openapi.json` was ten paths behind the backend, so routes that
    # shipped without a regen were invisible to the reachability check. The
    # refresh that added a batch of dashboard-only routes pulled them all in at
    # once. Listed rather than silently re-hidden, because an unlisted gap is
    # indistinguishable from a route nobody wanted.
    ("POST", "/ingest/v1/sessions/codex"): "codex session ingest; the plugin posts this directly",
    ("POST", "/ingest/v1/sessions/pi"): "pi session ingest; the plugin posts this directly",
    ("GET", "/v1/artifacts/{}/content"): "artifact content by id; same anchor-first reason",
    ("GET", "/v1/service-tokens"): "service tokens; no CLI verb designed yet",
    ("POST", "/v1/service-tokens"): "service tokens; no CLI verb designed yet",
    ("DELETE", "/v1/service-tokens/{}"): "service tokens; no CLI verb designed yet",
}

# The REVERSE debt ledger: client call sites that land AHEAD of the backend,
# each pointing at the fold that will declare the route. Same discipline as
# PENDING, opposite direction: an entry the schema now declares fails (delete
# it — the debt is paid), and an entry with no call site fails (it is not debt,
# it is litter). Every entry must ship with an old-backend guard at its call
# site, because until the backend lands, EVERY deployment is an old backend.
# Empty, and that is the ledger working: the entries that lived here --
# `POST /v1/runs/{}/reopen` among them -- are declared by the backend now, so
# the debt is paid and the entries go. The old-backend guard in `reopen_run()`
# STAYS: a client talks to whatever backend it is pointed at, and plenty of
# those are older than this schema.
CLIENT_AHEAD: dict[Op, str] = {
    # Shape: ("METHOD", "/v1/path/{}"): "why the client is ahead + the guard".
    (
        "POST",
        "/v1/runs",
    ): "daemon v2 floating runs (S1, server PR in flight); `create_floating_run` turns "
    "an old backend's 405 into CapabilityUnavailable naming --project/--experiment",
    (
        "POST",
        "/v1/runs/{}/log-chunks",
    ): "live console log (plan item (h)); the server route merged in #2012, the generated "
    "schema has not been regenerated since. `logstream.prepare` creates no spool and sends "
    "nothing unless /v1/server/features declares run_log_stream",
    # Plan item (g): the multipart doors (server PR, 0273). `Run._maybe_multipart`
    # queues nothing and keeps 0.7's reference row unless /v1/server/features
    # declares artifact_multipart; a queued op that meets an older server (404)
    # dead-letters with the same reference row (`sdk/multipart.py`).
    ("POST", "/v1/runs/{}/artifacts/multipart"): "artifacts over 64 MiB (plan (g)), gated on "
    "artifact_multipart; 404 -> reference row",
    ("POST", "/v1/runs/{}/artifacts/multipart/{}/parts"): "plan (g) part URLs, same gate",
    ("GET", "/v1/runs/{}/artifacts/multipart/{}"): "plan (g) resume listing, same gate",
    ("POST", "/v1/runs/{}/artifacts/multipart/{}/complete"): "plan (g) complete, same gate",
    ("DELETE", "/v1/runs/{}/artifacts/multipart/{}"): "plan (g) abort, same gate",
    # Lineage plan 3, F2 (server 0285, gaps-server lane; the schema has not been
    # regenerated since). The write recorder journals its list only when
    # /v1/server/features declares run_outputs; these are the direct doors.
    ("POST", "/v1/runs/{}/outputs"): "a run's recorded writes (plan 3 F2); the recorder sends "
    "only when run_outputs is declared; an older backend answers 404",
    ("GET", "/v1/runs/{}/outputs"): "a run's recorded writes (plan 3 F2); an older backend "
    "answers 404 (NotFound)",
    # research-os 0291 (hide one session's own work); the schema has not been
    # regenerated since. Only the hosted MCP reads it, for a caller carrying
    # X-Probe-Hide-Session-Work; an older backend's 404 is caught and reported
    # as `session_work_exclusion_unsupported`, never read as "nothing created".
    ("GET", "/v1/sessions/{}/created"): "what a session created (0291); the MCP marks "
    "session_work_exclusion_unsupported on a 404",
}

_ALLOWED: dict[Op, str] = {**NOT_CLIENT_SURFACE, **PENDING}


def _fmt(ops) -> str:
    return "\n".join(
        f"  {method:6} {path}" for method, path in sorted(ops, key=lambda o: (o[1], o[0]))
    )


def test_no_allowlist_entry_is_in_both_lists():
    """A route is either not-our-job or not-done-yet. Never both."""
    overlap = set(NOT_CLIENT_SURFACE) & set(PENDING)
    assert not overlap, f"listed as both permanent and pending:\n{_fmt(overlap)}"


def test_every_backend_operation_is_reachable_from_the_client():
    """The parity check itself: no unlisted backend route may be unreachable."""
    ops = schema_operations()
    reachable = set(client_call_sites())
    unreachable = set(ops) - reachable - set(_ALLOWED)
    assert not unreachable, (
        f"{len(unreachable)} backend operation(s) are unreachable from the client.\n\n"
        f"{_fmt(unreachable)}\n\n"
        "Wire each one up (sdk/client.py + cli/main.py), or add it to NOT_CLIENT_SURFACE "
        "(with a reason) / PENDING (with a tracking pointer) in this file."
    )


def test_allowlisted_operations_are_still_unreachable():
    """Anti-rot: implementing a route means deleting its allowlist entry.

    Without this, PENDING silently becomes a list of things we already did, and
    NOT_CLIENT_SURFACE stops describing the boundary it claims to describe.
    """
    reachable = set(client_call_sites())
    stale = {op: why for op, why in _ALLOWED.items() if op in reachable}
    assert not stale, (
        "these operations are allowlisted but ARE reachable — delete their entries:\n"
        + "\n".join(f"  {m:6} {p}\n      listed as: {why}" for (m, p), why in sorted(stale.items()))
    )


def test_allowlisted_operations_still_exist_in_the_schema():
    """Anti-rot: an entry for a route the backend dropped is a lie. Delete it."""
    ops = schema_operations()
    ghosts = set(_ALLOWED) - set(ops)
    assert not ghosts, (
        "allowlisted operations that the backend no longer declares — delete these entries "
        f"(or run `make regen` if the schema is stale):\n{_fmt(ghosts)}"
    )


def test_client_only_calls_operations_the_backend_declares():
    """The reverse drift: a client call to a route that does not exist.

    Catches typos and rot — a path that quietly 404s forever is worse than a
    compile error, because fail-open callers swallow it.
    """
    ops = schema_operations()
    sites = client_call_sites()
    phantom = {op: where for op, where in sites.items() if op not in ops and op not in CLIENT_AHEAD}
    assert not phantom, (
        "the client calls operations the backend does not declare:\n"
        + "\n".join(
            f"  {m:6} {p}\n      called from: {', '.join(where)}"
            for (m, p), where in sorted(phantom.items())
        )
        + "\n\nRun `make regen` if the schema is stale; otherwise this call is "
        "dead code — or, for a deliberate SDK-ahead-of-backend fold, a "
        "CLIENT_AHEAD entry with its old-backend guard."
    )


def test_client_ahead_entries_are_live_debt():
    """A CLIENT_AHEAD entry is debt, and debt must be real and unpaid.

    Declared by the schema -> paid, delete the entry. Never called by the
    client -> not debt, litter. Either staleness hides real phantoms behind
    the ledger."""
    ops = schema_operations()
    sites = client_call_sites()
    paid = [op for op in CLIENT_AHEAD if op in ops]
    assert not paid, (
        "the backend now declares these CLIENT_AHEAD routes — the debt is "
        f"paid, delete the entries:\n{_fmt(paid)}"
    )
    litter = [op for op in CLIENT_AHEAD if op not in sites]
    assert not litter, (
        "no client call site reaches these CLIENT_AHEAD routes — they are "
        f"not debt, remove them:\n{_fmt(litter)}"
    )


# -- guards on the extractor itself -----------------------------------------
# The parity check is only as good as its path extraction. A silent regression here
# (e.g. f-strings stop resolving) would mark everything unreachable — or worse, mark
# the whole suite green by finding nothing to check.


def test_extractor_resolves_fstring_and_constant_paths():
    sites = client_call_sites()
    # f-string interpolation -> `{}` (sdk/run.py builds this from presign['artifact_id'])
    assert ("POST", "/v1/artifacts/{}/confirm") in sites
    # module-level constant (sdk/device.py's _START_PATH)
    assert ("POST", "/auth/device/code") in sites
    assert ("POST", "/auth/device/install-token") in sites
    # plain literal
    assert ("GET", "/v1/me") in sites


def test_no_transport_call_builds_its_path_opaquely():
    """No API call may be invisible to the parity check.

    A `*transport` call whose path is assembled by `.format()`/`+`/`%`/`join` is a
    hole: the route it hits looks unreachable (noisy but safe), or — worse — a PENDING
    entry it satisfies never clears. Use a literal or f-string, or teach `_as_path`.
    """
    _, opaque = _scan()
    assert not opaque, "transport calls with an unreadable path:\n  " + "\n  ".join(opaque)


def _scan_source(tmp_path, source: str):
    """Run the extractor over a synthetic module instead of the real client."""
    (tmp_path / "fake_module.py").write_text(source)
    return _scan(src=tmp_path, root=tmp_path)


def test_extractor_reads_constants_fstrings_and_keyword_paths(tmp_path):
    found, opaque = _scan_source(
        tmp_path,
        """
_CONST = "/auth/device/code"
_ANNOTATED: str = "/v1/annotated"

def calls(self, thing_id):
    self.transport.get("/v1/literal")
    self.transport.post(_CONST, {})
    self.transport.get(_ANNOTATED)
    self.transport.patch(f"/v1/things/{thing_id}/parts", {})
    self.transport.get(path="/v1/keyword")
    self.transport.request("DELETE", f"/v1/things/{thing_id}")
    self._client.write("POST", "/v1/written", {})
""",
    )
    assert not opaque
    assert set(found) == {
        ("GET", "/v1/literal"),
        ("POST", "/auth/device/code"),
        ("GET", "/v1/annotated"),
        ("PATCH", "/v1/things/{}/parts"),
        ("GET", "/v1/keyword"),
        ("DELETE", "/v1/things/{}"),
        ("POST", "/v1/written"),
    }


def test_extractor_ignores_lookalikes_that_are_not_api_calls(tmp_path):
    """A dict keyed by paths, and a presigned absolute URL, are not operations."""
    found, opaque = _scan_source(
        tmp_path,
        """
ROUTES = {"/v1/not-a-call": 1}

def calls(self, body, url, data):
    ROUTES.get("/v1/not-a-call")          # a plain dict, not a transport
    body.get("slug")                       # not a path at all
    self.transport.put_url(url, data)      # absolute R2 URL, no API path
    self.transport.get_url(url)
""",
    )
    assert found == {}
    assert not opaque  # put_url/get_url are not path-taking verbs


def test_extractor_reports_a_transport_path_it_cannot_read(tmp_path):
    """The guard that keeps the known limits honest: an unreadable path is loud."""
    found, opaque = _scan_source(
        tmp_path,
        """
def calls(self, thing_id):
    self.transport.get("/v1/things/{}/parts".format(thing_id))
    self.transport.post("/v1/" + thing_id, {})
""",
    )
    assert found == {}
    assert len(opaque) == 2
    assert all("self.transport" in u for u in opaque)


def test_extractor_does_not_flag_generic_dispatchers(tmp_path):
    """`Client.write` and the spool replay forward a caller-supplied path. Their real
    routes are recorded at their own call sites, so they must not be reported."""
    found, opaque = _scan_source(
        tmp_path,
        """
def write(self, method, path, body=None):
    return self.transport.request(method, path, json_body=body)

def flush(self, transport, entry):
    return transport.request(entry["method"], entry["path"])
""",
    )
    assert found == {}
    assert not opaque


def test_method_first_requires_a_dispatcher_receiver(tmp_path):
    """`write`/`request` are ubiquitous method names — a method-string + path on a
    NON-dispatcher receiver (a logger, a buffer) must NOT register as a reachable
    route. Otherwise an unrelated `.write("POST", "/v1/x")` could silently satisfy —
    and thereby retire — a PENDING entry, with no test going red.
    """
    found, _ = _scan_source(
        tmp_path,
        """
def calls(self, audit_log, buf):
    audit_log.write("POST", "/v1/runs/gc")   # a logger, not an HTTP client
    buf.write("GET", "/v1/tokens")            # a buffer
    self.write("POST", "/v1/real")            # Client.write — a real dispatch
    self._client.write("PATCH", "/v1/also-real")  # run helper — a real dispatch
""",
    )
    assert set(found) == {("POST", "/v1/real"), ("PATCH", "/v1/also-real")}
    assert ("POST", "/v1/runs/gc") not in found
    assert ("GET", "/v1/tokens") not in found


def test_verb_call_on_a_bare_http_client_is_seen(tmp_path):
    """`client.get("/v1/me")` (mcp/server.py's httpx client) must register, so a route
    wired only through such a receiver still clears its PENDING entry."""
    found, _ = _scan_source(
        tmp_path,
        """
def calls(client, some_dict):
    client.get("/v1/me")            # a real httpx client
    some_dict.get("not-a-path")     # a dict lookup, ignored (no leading /)
""",
    )
    assert ("GET", "/v1/me") in found


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("/v1/runs/{run_ref}/bundle", "/v1/runs/{}/bundle"),
        ("/v1/experiments/{experiment_id}/versions/{version}", "/v1/experiments/{}/versions/{}"),
        ("/v1/projects", "/v1/projects"),
    ],
)
def test_normalize_collapses_parameter_names(raw, expected):
    """Parameter naming is the backend's business; only position matters."""
    assert _normalize(raw) == expected

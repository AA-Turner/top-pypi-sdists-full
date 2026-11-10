"""Probe API data-source adapter used by the read-only MCP service."""

from __future__ import annotations
import time

from ...sdk import errors
from ...sdk.client.client import Client
from ...shared.reads.search_contract import Capability
from ...foundation.compose.compose import compose
from probe.mcp.source.catalog import CatalogReadsMixin
from probe.mcp.source.documents import DocumentReadsMixin
from probe.mcp.source.entities import EntityReadsMixin
from probe.mcp.source.lineage import LineageReadsMixin
from probe.mcp.source.projects import ProjectReadsMixin
from probe.mcp.source.runs import RunReadsMixin
from probe.mcp.source.search import SearchReadsMixin
from probe.mcp.source.sessions import SessionReadsMixin

# How long a cached `GET /v1/me` answer is reused. EVERY envelope carries the
# caller's identity (service._envelope), and every read tool returns an
# envelope, so without this a thirty-read agent session made thirty identical
# identity requests for one token. Short on purpose: identity is not immutable —
# a role can change — so this bounds the staleness to a minute rather than to
# the lifetime of an MCP process.
_IDENTITY_TTL_SECONDS = 60.0

# After a failed refresh, keep serving the last good identity for this long
# before trying again. Without it, an outage costs one `/v1/me` attempt per tool
# call for its whole duration. Mirrors `_FAILURE_BACKOFF_S` in
# `app/client_version/router.py`, which solves the same problem.
_IDENTITY_FAILURE_BACKOFF_SECONDS = 30.0


@compose
class ResearchOSSource(
    SearchReadsMixin,
    EntityReadsMixin,
    CatalogReadsMixin,
    LineageReadsMixin,
    RunReadsMixin,
    ProjectReadsMixin,
    DocumentReadsMixin,
    SessionReadsMixin,
):
    """Read authoritative structured data through Probe APIs.

    The source never connects directly to Postgres or R2. The API enforces
    tenancy and returns object-store resource pointers where appropriate.
    """

    def __init__(self, client: Client):
        self.client = client
        # Per-SOURCE, which is per-token: server._acquire_service memoizes one
        # source per token and evicts them by LRU, so this needs no key and no
        # separate cleanup, and one tenant's identity can never be served to
        # another. Lock-free: two threads racing both fetch and write the same
        # value, which costs one extra request and cannot produce a wrong one.
        self._identity: dict | None = None
        self._identity_at: float = float("-inf")
        self._identity_failed_at: float = float("-inf")

    def close(self) -> None:
        self.client.close()

    def capabilities(self) -> dict[str, bool]:
        # STATIC BY DESIGN, and that rests on one deployment fact: the MCP only
        # ever talks to the HOSTED backend. Self-host (docs/SELF_HOST.md) ships
        # the chart to customer clusters running their own version, but it
        # serves SDK/CLI machine clients — not this. So "does this backend have
        # POST /v1/search" has a constant answer here, and the probe that used
        # to ask it was spending a BILLED recall action per session to compute
        # that constant: the client omitted `include_semantic`, inherited the
        # server default of True (app/search/schemas.py), and entered
        # memory_action(MEMORY_ACTION_RECALL) on every MCP session start. It
        # also emitted a content-inclusive `search_performed` event carrying the
        # literal query "capability probe", which was ~17% of all such events.
        #
        # DO NOT turn these back into probes without re-testing that fact. If an
        # MCP is ever pointed at a self-hosted install these flags are wrong,
        # and the failure is a 404 at the call site rather than a graceful
        # degrade. See TODOS.md, "The MCP talks only to the hosted backend".
        # The residual protection is unchanged: search() and browse() raise
        # CapabilityUnavailable when a route really is absent, which is a
        # truthful failure rather than a preemptive denial.
        #
        # managed_artifact_upload was hardcoded False and STALE — the routes are in
        # schema/openapi.json and answer live (/v1/runs/{id}/artifacts/uploads +
        # /v1/artifacts/{id}/download). It was set in one stroke alongside a
        # /v1/search change, never as a deliberate call. Because research_context
        # derives `missing` from this map, that stale flag pinned EVERY context
        # envelope to state="partial" — the same "unconditionally missing" lie the
        # contract/versions/usage views told. (A `versioned_assets` flag sat here
        # for the same reason; it went with the asset registry itself.)
        return {
            Capability.STRUCTURED_EXPERIMENTS: True,
            Capability.STRUCTURED_BROWSE: True,
            Capability.UNIFIED_SEARCH: True,
            Capability.SEMANTIC_SEARCH: True,
            Capability.KB_DOCUMENTS: True,
            # Server-side project scoping (research-os #103). Declared in the
            # enum since it shipped and never once populated — `capabilities()`
            # simply omitted the key, so every reader saw it as absent. The
            # backend applies the scope and `service._echoes_project_scope`
            # degrades honestly if a response ever fails to confirm it.
            Capability.PROJECT_SCOPED_SEARCH: True,
            # The one honest False: sdk/capture/code/code.py captures git/env LOCALLY and
            # there is no backend snapshot route to read one back.
            Capability.PORTABLE_SNAPSHOTS: False,
            Capability.MANAGED_ARTIFACT_UPLOAD: True,
            # True for the SAME reason every other flag here is static: this
            # process only ever talks to the hosted backend, and that backend
            # carries FIRECRAWL_API_KEY. It is a claim about the deployment, not
            # about the next call -- an account out of credits still answers
            # True here and `web_search` in that response's `missing`.
            Capability.WEB_SEARCH: True,
        }

    def browse(
        self,
        *,
        scope: str | None = None,
        depth: int | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        workspace_id: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        runs_cursor: str | None = None,
        subprojects_cursor: str | None = None,
        continuation_handles: bool | None = None,
        exclude_origin_session: str | None = None,
    ) -> dict:
        """GET /v1/browse, raising CapabilityUnavailable on a backend without it.

        A pre-browse backend must NOT degrade to an empty tree: "nothing exists
        here" and "this server cannot tell you what exists" are opposite claims,
        and the first one would stop an agent looking further.
        """
        try:
            response = self.client.browse(
                scope=scope,
                depth=depth,
                status=status,
                tags=tags,
                workspace_id=workspace_id,
                limit=limit,
                cursor=cursor,
                runs_cursor=runs_cursor,
                subprojects_cursor=subprojects_cursor,
                continuation_handles=continuation_handles,
                exclude_origin_session=exclude_origin_session,
            )
        except errors.NotFoundError:
            # A scoped 404 means the SCOPE was not found on a backend that has
            # the route; only an unscoped 404 proves the route is missing.
            if scope is not None:
                raise
            raise self._browse_unavailable() from None
        return response

    def _browse_unavailable(self) -> errors.CapabilityUnavailable:
        return errors.CapabilityUnavailable(
            Capability.STRUCTURED_BROWSE,
            "this Probe backend predates GET /v1/browse",
        )

    def _capability_unavailable(self) -> errors.CapabilityUnavailable:
        # Nothing catches this any more, so it is the message a researcher reads.
        # "predates POST /v1/search" was the only possible cause when a probe
        # had confirmed the route; on the hosted backend, which is the only one
        # this talks to, that route exists, so a repeated unscoped 404 is far
        # likelier to be routing or an ingress fault. Name both.
        return errors.CapabilityUnavailable(
            Capability.UNIFIED_SEARCH,
            "POST /v1/search answered 404 twice: this backend either predates "
            "the endpoint or is not routing it",
        )

    def identity(self) -> dict:
        """``GET /v1/me``, cached for ``_IDENTITY_TTL_SECONDS``.

        Cached HERE rather than on ``Client.me`` on purpose: the SDK method is
        also what ``probe whoami`` calls, where a caller asking who they are
        after changing something deserves the live answer.

        A failed refresh SERVES THE LAST GOOD ANSWER rather than failing, and
        then BACKS OFF, both borrowed from `app/client_version/router.py`
        (`_FAILURE_BACKOFF_S`, "serves the last-good cache regardless of age").
        Identity is not the answer the caller asked for — it is a field on the
        envelope around it — so a `/v1/me` blip must not take down every read
        tool. Serving stale alone is not enough: without the backoff a 30-second
        outage still re-requests `/v1/me` on every tool call, which is the exact
        per-call traffic this cache exists to remove, arriving when the backend
        can least absorb it. Only a cold cache propagates the error, because
        then there is nothing truthful to serve.
        """
        now = time.monotonic()
        if self._identity is not None:
            if (now - self._identity_at) <= _IDENTITY_TTL_SECONDS:
                return self._identity
            if (now - self._identity_failed_at) < _IDENTITY_FAILURE_BACKOFF_SECONDS:
                # A refresh failed recently. Keep serving what we have rather
                # than retrying once per tool call for the length of the outage.
                return self._identity
        try:
            identity = self.client.me()
        except (errors.AuthError, errors.ScopeError):
            # NOT stale-served. A 401/403 is not a blip — it is the server
            # saying this token is no longer who the cached answer says it is,
            # which is exactly the change the TTL exists to notice. Serving the
            # old identity through a revoked or re-scoped token would report a
            # researcher and tenant that no longer apply.
            raise
        except errors.RosError:
            if self._identity is None:
                raise
            # Stale, and knowingly so. Stamp the FAILURE, never _identity_at:
            # treating a failure as a refresh would hide the outage for a full
            # TTL and then expire into another storm.
            self._identity_failed_at = time.monotonic()
            return self._identity
        self._identity = identity
        self._identity_at = time.monotonic()
        self._identity_failed_at = float("-inf")
        return identity

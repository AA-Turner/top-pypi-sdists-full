"""Probe Research API data-source adapter used by the read-only MCP service."""

from __future__ import annotations

import base64
import re
import time
import uuid
from typing import Any

from ..sdk import errors, nonfinite
from ..sdk.client import SOURCE_READ_CONTRACT, Anchor, Client
from .contract import Capability, EntityType, NoteCatalogKind
from .delivery_context import current_delivery, document_hint, pin_document, source_changed

#: A retired ref kind, kept ONLY so `get()` can tell a caller the surface is
#: gone instead of failing as a malformed id. The literal string is load-bearing
#: -- it is what a stale client sends -- so this is the one place the retired
#: name survives on purpose. Not an EntityType member: it names nothing that
#: exists, and putting it back in the enum would re-advertise it in every tool
#: schema. Delete it when stale clients stop asking.
_RETIRED_REF_KIND = "wiki"

_RETIRED_REF_DETAIL = (
    "that surface was removed. Its shared-prose role is now the TEAM NOTE: "
    'get_entity(ref="team-note") reads it, and editing the synced '
    "`probe-team-note.md` file IS the write -- both adding and correcting. "
    "Per-entity notes "
    'live on the entity itself: get_entity(ref="project:<id>", view="notes"). '
    "If your instructions still tell you to start there, they are "
    "out of date -- upgrade the plugin (`uv tool upgrade probe-research`) and "
    "re-run `probe wizard` to refresh them."
)
_INDEX_SLUG = "contents"

# The agents whose sessions the capture pipeline records, in the order a bare
# `session:<id>` ref tries them. Mirrors the backend's TranscriptAgent literal:
# `source` is part of the transcript document's identity, so an unqualified id
# has to be resolved by asking, not by guessing one and reading its 404 as
# "never captured".
def _transcript_agents() -> tuple[str, ...]:
    from probe.harness import get_registry

    return tuple(h.id for h in get_registry().captured())


_TRANSCRIPT_AGENTS = _transcript_agents()

# The session-id SHAPE, byte-for-byte the backend's `_SESSION_RE`
# (app/runs/agent_session.py): the id lands in a URL path segment
# (`/v1/sessions/{id}/...`), so a value carrying `/`, `?`, `#`, `..` or
# whitespace would silently re-steer the request -- `?` truncates the path and
# turns a real read into a bogus empty one, `..` walks out of `/sessions/` onto
# another GET route under the same read token. Validating the shape here, at the
# one point every session ref resolves through, closes that off with the SAME
# gate the write path already enforces, so a value that could never have been
# stored never reaches the wire.
_SESSION_ID_RE = re.compile(r"\A[A-Za-z0-9._:-]{8,200}\Z")

#: `kind_rank` per notes-catalog kind, exactly as the catalog's SQL arms number
#: them (app/notes_catalog/service.py): the tiebreak inside one `created_at`,
#: and the middle third of its cursor. The team note has none -- it is never in
#: a keyset page.
_NOTE_KIND_RANK: dict[str, int] = {
    NoteCatalogKind.PROJECT: 6,
    NoteCatalogKind.EXPERIMENT: 5,
    NoteCatalogKind.RUN: 4,
    NoteCatalogKind.SUB_NOTE: 3,
    NoteCatalogKind.GROUP: 2,
    NoteCatalogKind.ARTIFACT: 1,
}

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


class ResearchOSSource:
    """Read authoritative structured data through Probe Research APIs.

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
            # The one honest False: sdk/snapshot.py captures git/env LOCALLY and
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
            "this Probe Research backend predates GET /v1/browse",
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

    def search(
        self,
        query: str,
        *,
        corpus: list[str] | None = None,
        workspace_id: str | None = None,
        project_id: str | None = None,
        top_k: int | None = None,
        exact_limit: int | None = None,
        exact_cursor: str | None = None,
        semantic_cursor: str | None = None,
        exclude_agent_session: str | None = None,
        curated_only: bool | None = None,
        exclude_origin_session: str | None = None,
    ) -> dict:
        """POST /v1/search.

        404 policy (rolling deploys + oracle-safe SCOPE 404s). This used to need
        a capability probe to tell "the route is gone" from "the scope is gone",
        and that probe cost a billed recall action per session. It is not needed,
        because the MCP only ever talks to the hosted backend, where the route is
        always there:

        - RETRY ONCE on any 404. A stale pod mid-rolling-deploy 404s scoped and
          unscoped requests alike, and attributing that to the scope turns a
          deploy into "your project does not exist" — a wrong answer about the
          caller's own data. Project scope is the commoner of the two, so
          getting this wrong has a wide blast radius.
        - A SECOND 404 on a SCOPED request means that scope is absent (both
          workspace and project scopes are oracle-safe 404s): NotFound.
        - A SECOND 404 on an UNSCOPED request has no scope left to blame, so the
          route itself is missing: CapabilityUnavailable, which names the real
          problem instead of reporting "not found" for a search with nothing to
          find. Nothing catches it — there is deliberately no keyword fallback
          any more (see `service.search_knowledge`) — so it reaches the caller
          as a truthful failure.
        """
        retried = False
        while True:
            try:
                response = self.client.search(
                    query,
                    corpus=corpus,
                    workspace_id=workspace_id,
                    project_id=project_id,
                    curated_only=curated_only,
                    top_k=top_k,
                    exact_limit=exact_limit,
                    exact_cursor=exact_cursor,
                    semantic_cursor=semantic_cursor,
                    exclude_agent_session=exclude_agent_session,
                    exclude_origin_session=exclude_origin_session,
                )
            except errors.NotFoundError:
                if retried:
                    # Second 404: the deploy window is ruled out, so the 404 is
                    # about the REQUEST. A scope in hand means that scope is
                    # absent; no scope means the route is.
                    if workspace_id is not None or project_id is not None:
                        raise
                    raise self._capability_unavailable() from None
                retried = True
                continue
            return response

    def query_sql(
        self,
        *,
        sql: str | None = None,
        tables: list[str] | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """``POST /v1/sql``. No retry: a query is not idempotent in cost, and a
        refusal (422), timeout (408), overload (429) or plan refusal (402) is an
        answer the agent must read, not a blip to paper over."""
        return self.client.query_sql(sql=sql, tables=tables, max_rows=max_rows)

    # Literature uses the same backend and provider contract as the assistant.
    # Keep filtering and per-mode validation at that shared boundary.

    def find_papers(
        self,
        *,
        mode: str,
        query: str | None = None,
        paper_id: str | None = None,
        limit: int | None = None,
        authors: str | None = None,
        categories: str | None = None,
        published_from: str | None = None,
        published_to: str | None = None,
        expand: str | None = None,
    ) -> dict:
        """``POST /v1/web/papers``."""
        return self.client.find_papers(
            mode,
            query=query,
            paper_id=paper_id,
            limit=limit,
            authors=authors,
            categories=categories,
            published_from=published_from,
            published_to=published_to,
            expand=expand,
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

    def projects(self, *, limit: int = 50) -> list[dict]:
        return self.client.list_projects(limit=limit).items

    def experiments(self, *, project_id: str | None = None, limit: int = 100) -> list[dict]:
        return self.client.list_experiments(project_id=project_id, limit=limit).items

    def runs(
        self,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
        direct: bool = False,
        limit: int = 100,
    ) -> list[dict]:
        """``project_id`` lists ALL the project's runs — project-direct and
        experiment-attached (research-os 0054); ``direct=True`` narrows to
        experiment-less runs server-side."""
        return self.client.list_runs(
            experiment_id=experiment_id,
            project_id=project_id,
            direct=direct,
            limit=limit,
        ).items

    def unfiled_runs(
        self, *, limit: int = 10, exclude_origin_session: str | None = None
    ) -> list[dict]:
        """FLOATING runs, filed nowhere yet (daemon v2): the caller's own, every
        one for an admin. Raises CapabilityUnavailable on a backend that
        predates them (it ignores the filter and would list filed runs).

        ``exclude_origin_session`` leaves out, server-side and inside the page,
        the runs that session created (research-os 0291)."""
        params = (
            {"exclude_origin_session": exclude_origin_session}
            if exclude_origin_session is not None
            else {}
        )
        return self.client.list_runs(unfiled=True, limit=limit, **params).items

    def session_created(self, session_id: str) -> dict:
        """``GET /v1/sessions/{id}/created``: what that session CREATED (0291)."""
        return self.client.session_created(session_id)

    def artifact_ref(self, value: str) -> dict:
        """Resolve ``artifact:<value>`` where value is a NAME or an ID.

        The two axes answer DIFFERENT questions, and conflating them is what #135
        got wrong in the other direction:

        * a NAME asks "does an official X already exist" -- the reuse check. It is
          scoped to SHARED and stays that way (:meth:`artifact_by_name`).
        * an ID is an identity the caller ALREADY holds (``search_knowledge``
          returns artifact hits carrying an id and ``resource: null``). It is not a
          reuse question at all, so the shared scoping does not apply to it.

        #135 answered an id with a 422 saying ids are unresolvable because no
        ``GET /v1/artifacts/{id}`` route exists. The premise was wrong: no ENTITY
        route exists, but ``GET /v1/artifacts/{id}/versions`` takes a raw id and
        already backs the versions view, so an id is resolvable today.
        """
        try:
            uuid.UUID(value)
        except ValueError:
            return self.artifact_by_name(value)
        return self.artifact_by_id(value)

    def artifact_by_id(self, artifact_id: str) -> dict:
        """Resolve an artifact ID, without widening the reuse check's scope.

        DELIBERATE SCOPE DECISION -- an id resolves for EVERY artifact, but only a
        SHARED one resolves to a full card:

        * ``view=versions`` works for any artifact whatever its anchor, because
          ``GET /v1/artifacts/{id}/versions`` is an unscoped by-id route. A caller
          holding an id gets the version chain even for a run-anchored artifact.
        * a full CARD needs the artifact's ROW (name, metadata), and the only list
          that yields one is ``GET /v1/shared/files``. So a shared id gets the same
          card a name does; a non-shared id resolves to an id-only identity that
          says where the rest lives.

        This does NOT widen the reuse check. That check is ``artifact:<name>`` and
        is still SHARED-only: "is there an official X" must not be answered off a
        run-anchored copy. Resolving an id the caller already holds answers a
        different question and licences nothing.

        A not-found here is authoritative in a way the name path's never is: ids
        are global and unscoped, so "no artifact with this id" rules out every
        anchor at once, where "no artifact named X" only ever ruled out SHARED.
        """
        # Shared FIRST, for the card. Costs one unbounded list (same read the name
        # path already does) and is the only source of a full row.
        rows = self.client.list_anchored(Anchor.SHARED) or []
        for row in rows:
            if str(row.get("id")) == artifact_id:
                return row
        # Not shared. The artifact almost certainly still EXISTS -- run-, experiment-
        # and project-anchored artifacts never appear in the shared list -- so
        # answering not-found here would be the #135 inversion wearing new clothes:
        # get_entity's contract reads an error as "a new identity is licensed".
        # Prove existence off the unscoped by-id route instead of guessing.
        self.artifact_versions(artifact_id)  # 404s iff the id is genuinely unknown
        return {
            "id": artifact_id,
            "shared": False,
            # Carried so the card says why it is thin rather than looking truncated.
            "resolution_note": (
                f"artifact {artifact_id} exists but is not shared, so only its id "
                f"and version chain are readable here (there is no "
                f"GET /v1/artifacts/{{id}} entity route, and only "
                f"GET /v1/shared/files yields a full row). view=versions is "
                f"complete; for name and metadata read the owning container with "
                f"run:<id> / experiment:<id> view=artifacts, or promote it with "
                f"`probe shared share`. This is NOT absence and licences no new "
                f"identity."
            ),
        }

    def artifact_by_name(self, name: str) -> dict:
        """Resolve an artifact NAME to the artifact, at the shared (lab-wide) level.

        This is the reuse-before-you-create seam, and it is by NAME because the
        question is "does an official X already exist" -- you have the name, not an
        id. There is no ``GET /v1/artifacts/{id}`` read route at all, so name is not
        merely the convenient axis here, it is the only one.

        SHARED, not a container, on purpose: the retired asset registry enforced
        tenant-unique names, and a shared-level artifact is what that identity
        became (#143 folded every asset into an artifact keeping its id). Scoping
        this to a project would answer a narrower question than the one the caller
        asked and would licence a duplicate that already exists one level up.
        """
        # `prefix` is a FOLDER filter, NOT a name filter: `path` is a GENERATED
        # column holding the DIRNAME of `name` (research-os 0029), and the clause
        # is `path = $1 OR path LIKE '$1/%'`. Passing the whole name would match
        # nothing for a root-level file, whose path is '' -- and "nothing" here
        # reads as "no such artifact", i.e. licence to create the duplicate this
        # check exists to prevent. So narrow by the name's DIRECTORY and match the
        # name ourselves. A root-level name has no directory, and the whole shared
        # scope is then the honest search space.
        # An id never reaches here: `artifact_ref` routes UUID-shaped values to
        # `artifact_by_id`. #135 raised a 422 at this point instead, on the premise
        # that ids were unresolvable -- they are not, and refusing one sent agents
        # back to a name they may not have. The invariant that 422 protected still
        # holds, just earlier: an id is never answered as an absent NAME.
        folder = name.rsplit("/", 1)[0] if "/" in name else ""
        params = {"prefix": folder} if folder else {}
        # NO `limit`, deliberately. A cap would make an artifact past the cap read
        # as absent, and absent is defined downstream as licence to create a new
        # identity -- reintroducing the precise bug the retired asset registry
        # had (assets.resolve() read one default-limit page, so asset 51+ resolved
        # to no_match and callers were told to register a duplicate). An unbounded
        # read of one curated team folder is the cheaper failure. A server-side
        # name filter would fix both; /v1/shared/files has no such parameter yet.
        rows = self.client.list_anchored(Anchor.SHARED, **params) or []
        exact = [row for row in rows if row.get("name") == name]
        if not exact:
            # States what was SEARCHED, not what exists. This lookup covers live
            # COMPLETE artifacts at the SHARED level only -- a run/experiment/
            # project-anchored artifact of the same name is real and invisible
            # here, and so is an upload still pending. "Nothing exists" would
            # overstate all of that, and downstream this message is read as
            # licence to create a new identity, so the overstatement is the
            # expensive direction to be wrong in.
            raise errors.NotFoundError(
                f"no completed artifact named {name!r} at the SHARED level, which "
                f"is the only scope this check covers. That is the answer to "
                f"'does an OFFICIAL one exist' -- it does not rule out a copy "
                f"anchored to a run, experiment or project, or an upload still "
                f"pending. Check a container with run:<id> / experiment:<id> "
                f"view=artifacts; promote a workspace file with `probe shared share`."
            )
        if len(exact) > 1:
            # Loud, and deliberately NOT a not-found: an agent reads not-found as
            # "a new identity is licensed" and would create a THIRD copy of a name
            # that is already duplicated. Naming the ids is the only answer that
            # leads to a merge instead.
            ids = ", ".join(sorted(str(row.get("id")) for row in exact))
            raise errors.ValidationError(
                f"{len(exact)} shared artifacts are named {name!r} (ids: {ids}); "
                f"this name is already duplicated -- reconcile them rather than "
                f"pinning either blindly",
                status=422,
            )
        return exact[0]

    def get(self, ref: str) -> tuple[str, dict]:
        """Resolve ``kind:value`` (or a bare id) to ``(kind, entity)``.

        ``group`` is here rather than behind a research_list_groups tool: a sweep is
        an experiment-shaped noun, so it belongs on the same ref seam as the rest.
        ``artifact`` is reached by name OR id (see :meth:`artifact_ref`).
        """
        # A TOMBSTONE, not an absence. This ref was the orienting read every
        # agent was told to make first, and that instruction lives in prose on
        # machines a release cannot reach -- a plugin nobody upgraded, a
        # CLAUDE.md written months ago. Removing the member without this leaves
        # those callers a bare "unknown kind" or, worse, "a bare ref must be a
        # UUID": both true, both useless, and neither says the surface was
        # retired or where the prose went.
        if ref.split(":", 1)[0] == _RETIRED_REF_KIND:
            raise errors.ValidationError(_RETIRED_REF_DETAIL, status=410)
        # The TEAM NOTE (0125), the second singleton and checked here for the same
        # reason: `ref="team-note"` carries no colon, so the bare-ref branch below
        # would report it as a malformed UUID.
        if ref == EntityType.TEAM_NOTE.value or ref == f"{EntityType.TEAM_NOTE.value}:":
            context = current_delivery()
            hint = document_hint("team-note") if context and context.snapshot else None
            if hint and "version" in hint:
                try:
                    note = self.client.get_team_note_version(hint["version"])
                except errors.NotFoundError as exc:
                    raise source_changed("saved team-note version is unavailable") from exc
            else:
                note = self.client.get_team_note()
            return EntityType.TEAM_NOTE.value, {
                "body": note.get("body") or "",
                "version": note.get("version"),
                "updated_at": note.get("updated_at"),
                "updated_by": note.get("updated_by"),
                "remaining_chars": note.get("remaining_chars"),
            }
        kind, _, value = ref.partition(":")
        if not value:
            value = kind
            kind = ""
        if kind == EntityType.SESSION.value:
            return kind, self._session_entity(value)
        if kind == EntityType.SUB_NOTE.value:
            # Kept OUT of `getters` below on purpose: that table is also the
            # bare-UUID sweep, and a sub-note is only ever reached by an id a
            # notes row handed out under this prefix -- one more 404 on every
            # bare-ref miss would buy nothing.
            return kind, self._sub_note_entity(value)
        getters = {
            EntityType.RUN.value: self.client.get_run,
            EntityType.EXPERIMENT.value: self.client.get_experiment,
            EntityType.PROJECT.value: self.client.get_project,
            EntityType.GROUP.value: self.client.get_group,
            # 0135. Keyed by ROLLOUT SPAN id, which is why it is safe in the
            # bare-ref sweep below: it shares an id space with spans, not with
            # the four above, so no bare UUID can resolve to both a trial and
            # something else.
            EntityType.TRIAL.value: self.client.get_trial,
        }
        if kind == EntityType.ARTIFACT.value:
            return kind, self.artifact_ref(value)
        if kind in getters:
            return kind, getters[kind](value)
        if kind:
            # An unknown kind is REJECTED, never guessed at. `asset:<name>` used to
            # land here and fall into the loop below, where get_experiment() raised
            # a raw 422 uuid_parsing on a non-UUID value -- so the agent that
            # followed the retired instruction to the letter got a Postgres-shaped
            # parse error naming `experiment_id`, and nothing that said "assets are
            # gone". Any ref kind retired later would leak the same way.
            known = sorted(
                [
                    *getters,
                    EntityType.ARTIFACT.value,
                    EntityType.SESSION.value,
                    EntityType.SUB_NOTE.value,
                ]
            )
            raise errors.ValidationError(
                f"unknown ref kind {kind!r} in {ref!r}; supported kinds are {known} "
                f"(assets were folded into artifacts: use artifact:<name>; the team "
                f'note is the bare ref "team-note")',
                status=422,
            )
        # A bare ref is only ever an id, and every id route validates it as a UUID.
        # Checking the SHAPE here rather than catching the backend's 422 keeps a
        # REAL 422 -- schema drift, a backend invariant -- propagating instead of
        # being rewritten into "nothing matches this ref". Catching every
        # ValidationError would swallow those, which is the same class of mistake
        # as the leak this replaced, only quieter.
        try:
            uuid.UUID(value)
        except ValueError:
            raise errors.NotFoundError(
                f"no run, experiment, project, group, or trial matches {ref!r}: "
                f"a bare ref must be a UUID id (names are reached as artifact:<name>)"
            ) from None
        for candidate in getters:
            try:
                return candidate, getters[candidate](value)
            except errors.NotFoundError:
                continue
        raise errors.NotFoundError(
            f"no run, experiment, project, group, or trial matches {ref}"
        )

    def bundle(self, run_id: str) -> dict:
        """The run bundle, read under the coverage contract. A source-backed run
        (a W&B mirror) answers 422 without it -- which made every view built on
        the bundle (`handoff`, `sessions`) fail on exactly the imported runs. The
        MCP reads the catalog's coverage receipts rather than rendering them."""
        return self.client.run_bundle(run_id, source_read_contract=SOURCE_READ_CONTRACT)

    def lineage(self, run_id: str) -> dict:
        return self.client.run_lineage(run_id)

    def run_edges(self, run_id: str) -> list[dict]:
        """Lineage EDGES touching this run (artifact / asset-version provenance).

        A different relation from `lineage()`, which walks `parent_run_id` and
        answers "which run was this forked from". Both are needed to answer
        "where did this run's data come from", and only one of them was ever
        surfaced -- which is why the lineage view reported empty on runs that
        demonstrably consumed a dataset and produced artifacts."""
        return self.client.run_edges(run_id)

    def run_upstream(self, run_id: str, depth: int) -> dict:
        """What the run built on, `depth` hops back, across parents, runs it
        built on, and the writers of the files it read (server 0255)."""
        return self.client.run_upstream(run_id, depth=depth)

    def artifact_lineage(self, artifact_id: str) -> dict:
        return self.client.artifact_lineage(artifact_id)

    def project_lineage(self, project_id: str) -> dict:
        """A project's or experiment's own links, its origin, and its children
        with theirs (server 0278, lineage plan 2 L12/L18)."""
        return self.client.project_lineage(project_id)

    def experiment_edges(self, experiment_id: str, limit: int) -> list[dict]:
        """The graph AMONG an experiment's runs and files, stored edges first,
        at most ``limit``."""
        return self.client.experiment_edges(experiment_id, limit=limit)

    def server_records_reads(self) -> bool:
        """Whether the server has the read lineage routes (0255). An older or
        self-hosted server answers them 404, which a view would otherwise pass
        on as "not found" for an entity that exists. Unknown counts as yes: the
        real call then says what is wrong."""
        try:
            return bool(self.client.supports_feature("run_inputs"))
        except Exception:  # noqa: BLE001
            return True

    # -- reads the SDK already had, which the MCP simply never surfaced --------

    def run_spans(self, run_id: str, **filters: Any) -> list[dict]:
        """The trajectory itself. The run bundle carries span_type COUNTS only, so
        before this an agent could see that 500 rollouts happened and not one of
        what they did."""
        return self.client.run_spans(run_id, **filters)

    def run_trials(self, run_id: str, **kw: Any) -> Any:
        """One cursor-aware page of the run's AUTHORED trials (0135).

        Not the same read as filtering `run_spans(span_type="rollout")`. That
        returns the producer's spans; this returns the sidecar rows, which is
        where a researcher's title, description and note live -- and the sidecar
        exists even when its rollout falls outside a bounded run-wide span slice,
        which is exactly when the span read would have said the trial was not
        there."""
        return self.client.list_run_trials(run_id, **kw)

    def run_series(self, run_id: str) -> list[dict]:
        return self.client.run_series(run_id)

    def query_series(self, run_ids: list[str], **kw: Any) -> dict:
        """`POST /v1/series/query` -- the only points door a SOURCE-BACKED run
        has, because it is the only one that can carry the provider's coverage
        receipt. Used as the fallback when the raw-row route refuses."""
        return self.client.query_series(run_ids, **kw)

    def latest_scalars(self, run_ids: list[str], *, keys: list[str]) -> dict:
        """`POST /v1/series/latest`: each series' catalog summary -- its
        `point_count` above all -- read off the derived catalog, never a point
        scan. One call for every run of a series read."""
        return self.client.latest_scalars(run_ids, keys=keys)

    def run_metrics(self, run_id: str, **filters: Any) -> list[dict]:
        # A tool response is strict JSON (the budget serializer refuses NaN), so
        # a non-finite point goes back to `value: null` beside its marker.
        return [nonfinite.to_wire(p) for p in self.client.run_metrics(run_id, **filters)]

    def run_metrics_grouped(self, run_id: str, key: str, **kw: Any) -> dict:
        """Server-side reduce/group (0059/0062). The client follows `next_step`
        paging; the service bounds the total through `max_rows`."""
        return self.client.get_metrics_grouped(run_id, key, **kw)

    def run_coordinates(self, run_id: str) -> list[dict]:
        return self.client.list_run_coordinates(run_id)

    def export_points(self, run_id: str, **kw: Any):
        """The lossless raw-point generator; the service slices one bounded page
        off it and hands the keyset cursor back to the agent. Strict JSON, as
        :meth:`run_metrics`."""
        return (nonfinite.to_wire(p) for p in self.client.export_metric_points(run_id, **kw))

    def run_artifacts(self, run_id: str, **filters: Any) -> list[dict]:
        return self.client.list_run_artifacts(run_id, **filters)

    def experiment_artifacts(self, experiment_id: str) -> list[dict]:
        return self.client.list_experiment_artifacts(experiment_id)

    def project_artifacts(self, project_id: str) -> list[dict]:
        return self.client.list_project_artifacts(project_id)

    def project_papers(
        self, project_id: str, limit: int = 50
    ) -> tuple[list[dict], bool]:
        """One page of a project's papers (0152), newest first, and whether
        the backend has more past it.

        ONE page on purpose: the rows carry two Markdown documents each, so
        walking every cursor would blow a token budget on a read whose point is
        orientation. The tab is where a long review is browsed in full.

        The CURSOR comes back with the rows because dropping it would be a lie
        rather than an inefficiency: a review with 80 papers would hand back 50
        and report complete, and the agent would believe it had read the whole
        reading list."""
        page = self.client.list_papers(project_id, limit=limit)
        return page.items, bool(page.next_cursor)

    def project_code_commits(self, project_id: str, **filters: Any) -> dict:
        """One page of the proxied commit timeline (0134): {state, source,
        items, cursor}. state='stale' is real data with degraded freshness."""
        return self.client.list_project_commits(project_id, **filters)

    def project_commit(
        self, project_id: str, sha: str, source_id: str | None = None
    ) -> dict:
        return self.client.get_project_commit(project_id, sha, source_id)

    def experiment_code(self, experiment_id: str) -> dict:
        """The experiment's code window (phase 6): sources inherited from the
        project, each run's stored owner/repo@sha, per-repo commit windows.
        Stored rows only — the backend never asks GitHub on this read."""
        return self.client.get_experiment_code(experiment_id)

    def run_code(self, run_id: str) -> dict:
        """The run's resolved owner/repo@sha (0134). This one read MAY verify
        resolvability against GitHub server-side (cached, bounded)."""
        return self.client.get_run_code(run_id)

    def run_code_compare(self, run_id: str, to: str) -> dict:
        """What changed in code between two runs, from stored link rows only:
        {state, base, head, swapped, commits, ...} with base = the older run."""
        return self.client.compare_run_code(run_id, to)

    def artifact_versions(self, artifact_id: str) -> list[dict]:
        """The artifact's version chain, newest first — what the reuse check reads
        once :meth:`artifact_by_name` has turned a name into an identity."""
        return self.client.list_artifact_versions(artifact_id)

    def run_events(self, run_id: str) -> list[dict]:
        return self.client.events.for_run(run_id)

    def run_views(self, run_id: str) -> list[dict]:
        """``GET /v1/runs/{ref}/views``: the metric views saved on the run."""
        return self.client.list_views(run_id)

    def run_sandbox_diff(
        self,
        run_id: str,
        *,
        trial: str,
        path_prefix: str | None = None,
        cursor: str | None = None,
        limit: int,
    ) -> dict:
        """``GET /v1/runs/{ref}/sandbox-state/diff``: one keyset page of a
        trial's begin/end filesystem diff, plus whole-scan `counts`.

        Here and not on the SDK client: it is a read only this surface pages,
        and `probe trial` reaches the same bundle through its own files."""
        params: dict[str, Any] = {"trial": trial, "limit": limit}
        if path_prefix:
            params["path_prefix"] = path_prefix
        if cursor:
            params["cursor"] = cursor  # harness-literal-ok: the pagination cursor
        return self.client.transport.get(
            f"/v1/runs/{run_id}/sandbox-state/diff", params=params
        )

    def artifact_sessions(self, artifact_id: str, *, limit: int) -> dict:
        """``GET /v1/artifacts/{id}/sessions``: `{sessions, session_total}`, the
        captured sessions that registered or touched the file."""
        return self.client.transport.get(
            f"/v1/artifacts/{artifact_id}/sessions", params={"limit": limit}
        )

    def project_readme(self, project_id: str) -> dict:
        """``GET /v1/projects/{ref}/readme``: the attached repository's README
        as `{state, reason, repo, path, markdown, html_url, commit_sha}`.

        Its image links point at dashboard preview routes, so they do not
        resolve here; the TEXT is what an agent reads it for.

        NOT A PURE READ, and accepted as such (review of #2216): when the stored
        snapshot is missing or older than its max age, the route refreshes it --
        a GitHub fetch, the README's images uploaded to R2 as system-attributed
        artifacts, and the snapshot row rewritten -- exactly as a dashboard view
        of the README panel does. It is a cache refresh of content the project
        already shows, never a write an agent chose."""
        return self.client.transport.get(f"/v1/projects/{project_id}/readme")

    def _sub_note_entity(self, value: str) -> dict:
        """``GET /v1/sub-notes/{id}``: one titled sub-note WITH its body."""
        # The id lands in a URL path segment. The route types it a UUID, so a
        # value that is not one can never resolve -- refuse it here rather than
        # let a `/` or `..` re-steer the request.
        try:
            uuid.UUID(value)
        except ValueError:
            raise errors.ValidationError(
                f"{value!r} is not a sub-note id: a sub-note is reached as "
                f"sub_note:<uuid>, the id a notes view row or a notes-catalog "
                f"row carries",
                status=422,
            ) from None
        return dict(self.client.get_sub_note(value))

    # -- flat listings (browse modes other than `tree`) ------------------------

    def workspaces(self) -> list[dict]:
        """``GET /v1/workspaces``: every workspace, whole and in server order
        (creation is capped tenant-wide, so the route does not page)."""
        return self.client.list_workspaces()

    def run_list(
        self,
        *,
        project_id: str | None = None,
        experiment_id: str | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        active: bool = False,
        cursor: str | None = None,
        limit: int,
        exclude_origin_session: str | None = None,
    ) -> tuple[list[dict], str | None]:
        """``GET /v1/runs``: one page of the lab's runs, NEWEST FIRST, and the
        keyset cursor past it. ``active`` is the server's liveness filter
        (status running AND a heartbeat inside the window), not a status."""
        params: dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        if active:
            params["active"] = "true"
        if cursor:
            params["cursor"] = cursor  # harness-literal-ok: the pagination cursor
        if exclude_origin_session is not None:
            params["exclude_origin_session"] = exclude_origin_session
        page = self.client.list_runs(
            project_id=project_id, experiment_id=experiment_id, tags=tags, **params
        )
        return list(page.items), page.next_cursor

    @staticmethod
    def run_cursor_after(row: dict) -> str | None:
        """The `GET /v1/runs` cursor that resumes AFTER `row`: the list's own
        keyset, base64 of `<created_at>|<id>` (app/core/pagination.py), which
        the server reads as `(created_at, id) < (that row's)`.

        Built from the row rather than taken from the response because the MCP
        delivers a PREFIX of a page when its budget runs out, and has to resume
        after the last row it actually sent -- the server only names the cursor
        after the page's last row. Positional resumption (re-fetch, skip N) is
        what this replaced: a run that stopped being active, or was deleted,
        between two calls shifted every later row by one, so a row was skipped.

        None when the row lacks either half, so a caller can refuse to page
        rather than restart from the top."""
        created_at, row_id = row.get("created_at"), row.get("id")
        if not isinstance(created_at, str) or not created_at or not row_id:
            return None
        # `+00:00`, not `Z`: the server's `datetime.fromisoformat` reads both on
        # 3.11+, and only the offset form on anything older.
        if created_at.endswith("Z"):
            created_at = created_at[:-1] + "+00:00"
        return base64.urlsafe_b64encode(f"{created_at}|{row_id}".encode()).decode()

    @staticmethod
    def note_cursor_after(row: dict) -> str | None:
        """The `GET /v1/notes` cursor that resumes AFTER `row`: the catalog's
        own keyset, base64 of `<created_at>|<kind_rank>|<id>`
        (app/notes_catalog/service.py `encode_cursor`), read by the server as
        `(created_at, kind_rank, id) < (that row's)`.

        Built from the row for the reason `run_cursor_after` is: a mid-page cut
        must resume after the last row SENT. Finding that row again in a
        re-read page failed whenever newer notes had pushed it off the page.

        None for the team note (a first-page singleton with no keyset) and for
        a kind with no rank here -- the caller falls back to finding the row."""
        rank = _NOTE_KIND_RANK.get(row.get("kind"))
        created_at, row_id = row.get("created_at"), row.get("id")
        if rank is None or not isinstance(created_at, str) or not created_at or not row_id:
            return None
        if created_at.endswith("Z"):
            created_at = created_at[:-1] + "+00:00"
        return base64.urlsafe_b64encode(f"{created_at}|{rank}|{row_id}".encode()).decode()

    def notes_catalog(
        self, *, query: str | None = None, cursor: str | None = None, limit: int
    ) -> dict:
        """``GET /v1/notes``, the tenant-wide catalog: `{items, next_cursor}`.

        Always with a `limit` (a bare call answers the dashboard's lazy ROOT
        tree, see `Client.list_notes`) and with sub-notes included: they are
        openable here now (`sub_note:<id>`), so hiding them would hide the one
        row a search was most likely looking for."""
        return self.client.list_notes(
            query=query, cursor=cursor, limit=limit, include_sub_notes=True
        )

    def files(
        self, *, workspace_id: str | None = None, prefix: str | None = None, limit: int
    ) -> list[dict]:
        """The team's Shared folder (``GET /v1/shared/files``) or one workspace's
        files (``GET /v1/workspaces/{id}/files``), name-ordered. Neither route
        takes a cursor; ``prefix`` is a FOLDER filter, not a name match."""
        params: dict[str, Any] = {"limit": limit}
        if prefix:
            params["prefix"] = prefix
        if workspace_id is not None:
            return self.client.list_anchored(Anchor.WORKSPACE, workspace_id, **params) or []
        return self.client.list_anchored(Anchor.SHARED, **params) or []

    def experiment_groups(self, experiment_id: str) -> list[dict]:
        return self.client.list_groups(experiment_id)

    def experiment_versions(self, experiment_id: str) -> list[dict]:
        return self.client.list_experiment_versions(experiment_id)

    def execution_record(self, content_hash: str) -> dict:
        """The pinned environment behind ``run.env_ref`` — code, deps, hardware,
        settings, paths. This is what makes the reproduce view a reproduction."""
        return self.client.get_execution_record(content_hash)

    def reproduce(self, run_id: str) -> dict:
        """The server-assembled run reproduction record. Passthrough: the client is
        thin here on purpose — the backend is the one place that reads every piece
        together (research-os /reproduce)."""
        return self.client.run_reproduce(run_id)

    def experiment_reproduce(self, experiment_id: str, *, version: int | None = None) -> dict:
        """Per-run reproduction summaries across an experiment; ``version`` pins
        against a minted manifest. Passthrough to research-os /reproduce."""
        return self.client.experiment_reproduce(experiment_id, version=version)

    def experiment(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """One experiment through the experiment API (light experiments R4):
        identity, question, notes, run count, overview status. With the
        project it is filed under (a run row names it), one request; without,
        ``GET /v1/scopes/{id}`` finds it first."""
        if project_id:
            try:
                return self.client.get_experiment(experiment_id, project_id=project_id)
            except errors.NotFoundError:
                pass  # not filed there after all: ask where it is
        return self.client.get_experiment(experiment_id)

    def experiment_document(self, experiment_id: str) -> str | None:
        """The experiment's authored Markdown, as its Overview page holds it.

        Read at the experiment's PROJECT address, deliberately and for now: the
        experiment API serves the page (HTML) but not the authored block, which
        the server cuts out of the page for the project-address read. The server
        keeps that read working for this client until R6."""
        return self.client.get_experiment_document(experiment_id)

    # -- versioned note documents ---------------------------------------------

    def notes_document(self, kind: str, entity: dict) -> tuple[str | None, int | None]:
        """Pin an explicit notes read, using an already-known saved version.

        Detail schemas that omit ``notes_version`` use the original-prefix
        fallback. Do not list history to decorate ordinary cards or discover a
        version: the body already fetched is enough for honest consistency.
        A resumed known version is read directly under the same API auth/RLS.
        """
        body, version = entity.get("notes"), entity.get("notes_version")
        if current_delivery() is None:
            return body, version
        source = f"notes:{kind}:{entity['id']}"
        hint = document_hint(source)
        if hint and "version" in hint:
            version = hint["version"]
            entity_id = entity["id"]
            try:
                if kind == "project":
                    saved = self.client.transport.get(f"/v1/projects/{entity_id}/notes/versions/{version}")
                elif kind == "experiment":
                    # The PROJECT address. An experiment and its project twin share one
                    # uuid and the notes routes are mounted on both, so this is the
                    # same document read from the address that survives the route cut.
                    saved = self.client.transport.get(
                        f"/v1/projects/{entity_id}/notes/versions/{version}"
                    )
                elif kind == "run":
                    saved = self.client.transport.get(f"/v1/runs/{entity_id}/notes/versions/{version}")
                elif kind == "group":
                    saved = self.client.transport.get(f"/v1/groups/{entity_id}/notes/versions/{version}")
                else:
                    raise errors.ValidationError("Unsupported notes document kind", status=422)
            except errors.NotFoundError as exc:
                raise source_changed("saved notes version is unavailable") from exc
            body = saved.get("body")
            if saved.get("version") != version or not isinstance(body, str):
                raise source_changed("saved notes version is unavailable")
        pinned = pin_document(body or "", source, version=version)
        return (None if body is None and not pinned else pinned), version

    # -- captured coding-agent sessions ----------------------------------------

    def _session_entity(self, value: str) -> dict:
        """Resolve ``session:<id>`` or ``session:<agent>/<id>`` to its entity.

        The entity is the session's WORK read -- what it touched, grouped by
        entity type -- because that is a session's identity to a reader: "the
        session that produced run X" is how one is ever referred to. The
        transcript stays behind ``view="transcript"``; inlining megabytes of it
        on the card would make the cheap glance the most expensive read here.

        `/work` answers EMPTY for an unknown well-formed id (deliberately not an
        oracle for another product's ids), so an all-empty entity is "not
        observed here", not proof of absence -- the transcript view is the
        existence check, and its 404 is honest.
        """
        agent, sep, session_id = value.partition("/")
        if not sep:
            agent, session_id = "", value
        elif agent not in _TRANSCRIPT_AGENTS:
            raise errors.ValidationError(
                f"unknown session agent {agent!r}: a qualified session ref is "
                f"session:<agent>/<id> with agent one of {sorted(_TRANSCRIPT_AGENTS)}, "
                f"and a bare session:<id> resolves the agent itself",
                status=422,
            )
        if not session_id:
            raise errors.ValidationError(
                "a session ref needs an id: session:<id> or session:<agent>/<id> "
                "(ids ride on the `sessions` field of project/experiment/run reads)",
                status=422,
            )
        if not _SESSION_ID_RE.match(session_id):
            # The id becomes a URL path segment; a value the backend could never
            # have stored must be refused HERE rather than sent to re-steer the
            # request. Same shape the write path enforces (backend `_SESSION_RE`).
            raise errors.ValidationError(
                f"{session_id!r} is not a session id: ids are 8-200 chars of "
                f"letters, digits, and '.', '_', ':', '-' (a URL path segment, so "
                f"'/', '?', '#', and whitespace are rejected)",
                status=422,
            )
        try:
            entity = dict(self.client.session_work(session_id))
        except errors.NotFoundError as exc:
            # `/work` never 404s a well-formed id on a backend that HAS the route
            # -- an unobserved id answers EMPTY by design. So a 404 here is not
            # "no such session", it is "this backend predates the session routes",
            # and resolution gates ALL three views. Say that instead of letting a
            # raw 404 read as data loss (the browse/search pattern).
            raise errors.NotFoundError(
                f"this Probe Research backend predates the agent-session routes "
                f"(GET /v1/sessions/{{id}}/work): upgrade the server to read "
                f"session {session_id}. A current backend answers an unknown "
                f"session with an empty work read, never a 404."
            ) from exc
        entity["id"] = session_id
        if agent:
            # The caller's explicit agent outranks the observation: /work reports
            # `agent: null` for a session it never saw an entity link from, and
            # the transcript read needs the value to address the document.
            entity["agent"] = agent
        return entity

    def session_transcript(self, session_id: str, *, agent: str | None = None) -> dict:
        """The complete normalized transcript, resolving the agent if unnamed.

        ``source`` is part of the document's identity server-side, so a bare id
        is tried under each known agent rather than defaulting to one -- a
        default would read every codex session as "never captured". A probe per agent,
        bounded by the size of ``_TRANSCRIPT_AGENTS``, and only on refs that
        did not name the agent.
        """
        context = current_delivery()
        if context and context.snapshot:
            # Resolve once. Later pages must not fall through to another
            # recording agent when the original transcript is deleted.
            prefix = f"transcript:{session_id}:"
            if not context.snapshot["source"].startswith(prefix):
                raise source_changed("document identity changed")
            agent = context.snapshot["source"][len(prefix) :]
        if agent is not None and agent not in _TRANSCRIPT_AGENTS:
            # Caught here, not left to the backend's literal-validation 422:
            # that error names a Pydantic type, and the fix is a value.
            raise errors.ValidationError(
                f"unknown transcript source {agent!r}: one of {sorted(_TRANSCRIPT_AGENTS)}",
                status=422,
            )
        candidates = (agent,) if agent is not None else _TRANSCRIPT_AGENTS
        last: errors.NotFoundError | None = None
        for candidate in candidates:
            try:
                return self.client.session_transcript(session_id, source=candidate)
            except errors.NotFoundError as exc:
                last = exc
        # One message for both the named-agent and probed paths: the backend's
        # bare "transcript not found" reads as "no such session", and sending an
        # agent away from work that demonstrably happened is the expensive
        # misreading.
        tried = agent or f"any known agent ({', '.join(_TRANSCRIPT_AGENTS)})"
        raise errors.NotFoundError(
            f"no captured transcript for session {session_id} under {tried}. "
            f"A session listed on a project or run can still have no "
            f"transcript: capture may not have been enabled on the machine "
            f"that ran it."
        ) from last

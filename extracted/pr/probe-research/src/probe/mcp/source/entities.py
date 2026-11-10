"""resolve `kind:value` refs (or bare ids, artifact names) to one entity."""

from __future__ import annotations
import uuid

from ...sdk import errors
from ...sdk.artifact.anchors import Anchor
from ...shared.reads.search_contract import EntityType
from ..delivery.context import current_delivery, document_hint, source_changed
from probe.mcp.source.catalog import _CATALOG_DETAIL_ROUTES, dataset_ref_problem

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
    "out of date -- update Probe (`npx -y probe-research update --json`) to "
    "refresh them."
)
_INDEX_SLUG = "contents"


class EntityReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def projects(self, *, limit: int = 50) -> list[dict]:
        return self.client.list_projects(limit=limit).items

    def experiments(self, *, project_id: str | None = None, limit: int = 100) -> list[dict]:
        return self.client.list_experiments(project_id=project_id, limit=limit).items

    def artifact_ref(self, value: str) -> dict:
        """Resolve ``artifact:<value>`` where value is a NAME or an ID.

        The two axes answer DIFFERENT questions, and conflating them is what #135
        got wrong in the other direction:

        * a NAME asks "does an official X already exist" -- the reuse check. It is
          scoped to SHARED and stays that way (:meth:`artifact_by_name`).
        * an ID is an identity the caller ALREADY holds (``search``
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

        An id resolves for EVERY artifact to a full card: a shared id from
        ``GET /v1/shared/files`` (the same row its name resolves to), any other
        anchor from ``GET /v1/artifacts/{id}``, marked ``shared: False``.

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
        # Not shared. Run-, experiment- and project-anchored artifacts never appear
        # in the shared list, but `GET /v1/artifacts/{id}` reads any anchor by id
        # (RLS-scoped; 404 iff the id is unknown to this tenant). An error here must
        # stay a real NotFound: get_entity reads one as "a new identity is licensed".
        row = dict(self.client.get_artifact(artifact_id))
        row["shared"] = False
        return row

    def artifact_content(self, artifact_id: str) -> bytes:
        """The artifact's stored bytes (presigned GET). A client-owned reference has
        no managed bytes and raises the backend's 409."""
        return self.client.download_artifact(artifact_id)

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
        parameters = {"prefix": folder} if folder else {}
        # NO `limit`, deliberately. A cap would make an artifact past the cap read
        # as absent, and absent is defined downstream as licence to create a new
        # identity -- reintroducing the precise bug the retired asset registry
        # had (assets.resolve() read one default-limit page, so asset 51+ resolved
        # to no_match and callers were told to register a duplicate). An unbounded
        # read of one curated team folder is the cheaper failure. A server-side
        # name filter would fix both; /v1/shared/files has no such parameter yet.
        rows = self.client.list_anchored(Anchor.SHARED, **parameters) or []
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
            entity = {
                "body": note.get("body") or "",
                "version": note.get("version"),
                "updated_at": note.get("updated_at"),
                "updated_by": note.get("updated_by"),
            }
            # Fullness in TOKENS, the unit the cap refuses in (`remaining_chars`
            # measures the character backstop now). A count the server could not
            # give -- or a server older than token caps -- adds nothing, never a
            # number in the wrong unit.
            for key in ("tokens", "limit_tokens", "remaining_tokens"):
                value = note.get(key)
                if isinstance(value, int) and not isinstance(value, bool):
                    entity[key] = value
            return EntityType.TEAM_NOTE.value, entity
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
        if kind in _CATALOG_DETAIL_ROUTES:
            if kind == EntityType.DATASET.value:
                problem = dataset_ref_problem(value)
                if problem is not None:
                    raise errors.ValidationError(f"{ref!r} is refused: {problem}", status=422)
            return kind, self.catalog_entity(kind, f"{kind}:{value}")
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
                    *_CATALOG_DETAIL_ROUTES,
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

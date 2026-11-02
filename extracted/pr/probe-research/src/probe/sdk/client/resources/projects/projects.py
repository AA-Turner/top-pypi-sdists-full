"""ProjectsResource (client.projects, typed reads) and ProjectsMixin, Client's methods: create,
resolve, ensure and read projects, their sessions and contributors (twin: app/projects)."""

from __future__ import annotations
import builtins
from typing import Any

from .....generated.models import (
    ArtifactOut,
    BestPickOut,
    HeadlineMetricOut,
    LinkedSessionsOut,
    OverviewOut,
    ProjectDetailOut,
    ProjectOut,
    ProjectWorkspaceOut,
)
from ....delivery.transport.transport import Page
from ...resource import Resource

from .... import errors


def _session_page_params(order: str, after: str | None, limit: int) -> dict[str, Any]:
    """The query of a session-page read (`list_project_sessions`,
    `list_experiment_sessions`): `order` as given, `after` only when set."""
    params: dict[str, Any] = {"order": order, "limit": limit}
    if after is not None:
        params["after"] = after
    return params


def _same_name(row: dict, name: str) -> bool:
    return str(row.get("name", "")).lower() == name.lower()


def _exactly(rows: list[dict], slug: str, *, strict: bool = False) -> dict | None:
    """The row whose slug actually MATCHES, or None.

    Never `rows[0]`. FastAPI silently drops a query parameter it does not
    declare, so a backend without the `?slug=` filter (an older engine, a
    rolled-back data plane, a self-hosted install) answers an unfiltered first
    page — and taking `rows[0]` there attaches the caller to a real, arbitrary,
    WRONG entity instead of erroring. That failure is worse than the
    get-or-create it replaced: get-or-create at least made an isolated new
    identity, where this appends your metrics to someone else's experiment.

    The membership check in `run()` cannot catch it either, because it reads its
    comparand from the same broken listing and so agrees with the bug. Verifying
    the slug here is what makes an unfiltered response degrade to "not found".
    """
    for row in rows or ():
        if row.get("slug") == slug:
            return row
    if strict and len(rows or ()) > 1:
        # A miss from a listing nobody filtered is not an absence. Only callers
        # deciding id-vs-slug ask for strict; get-or-create still wants "absent".
        raise errors.UnfilteredListing(
            f"this backend did not apply ?slug={slug!r} (returned {len(rows)} rows)"
        )
    return None


class ProjectsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- projects -----------------------------------------------------------
    def create_project(
        self,
        slug: str,
        name: str | None = None,
        *,
        kind: str,
        part_of: list[str] | None = None,
        parent_project_id: str | None = None,
        workspace_id: str | None = None,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        authored_by: str | None = None,
    ) -> dict:
        """Create a project. Raises ``ConflictError`` if the slug is taken.

        ``kind`` is REQUIRED and declares what the project is for:
        ``training`` (weights move), ``evaluation`` (frozen weights — sweeps,
        evals), ``research`` (papers, design, theory) or ``general``. It
        structures the dashboard page; it never gates data. Machine paths with
        no intent-holder pass ``"general"``.

        Projects are flat. ``part_of`` (project ids) links the new project as a
        PART of each of them (0401): a phase of a bigger effort is its own
        project, linked to it, never filed under it. Nothing moves and nothing
        is inherited; with no ``workspace_id`` the server files it in the
        first target's workspace. ``parent_project_id`` is the older spelling,
        kept for existing callers: the server records it as a ``part_of`` link
        too.

        ``workspace_id`` (an id, or a workspace slug) names the workspace;
        omitted (and no ``part_of``/``parent_project_id``), this computer's
        workspace (:meth:`computer_workspace_id`). With neither, a team with
        several workspaces refuses, so your home workspace is pinned on this
        computer and the create sent again; with no home (or after `probe
        workspace use --clear`) it raises ``WorkspaceRequired``. A pin naming a
        deleted workspace is dropped and the create sent once more the same way.

        Creation is always explicit: there is no get-or-create. A caller that
        does not know whether the project exists asks :meth:`resolve_project`
        first and decides.

        ``document`` is authored Markdown that lives INSIDE the
        project's Overview page, as a block the page's AI writer may not
        rewrite. When the project is about a codebase, put a line containing only
        ``[README](https://github.com/owner/repo)`` in ``document``: the
        dashboard renders that repository's README there, refreshed on push, and
        for a private repo too when the team's GitHub App is installed on that
        account. The LINK TEXT is what makes it an embed, and ``project.repo`` is
        derived from it -- see :meth:`update_project`."""
        body: dict[str, Any] = {"slug": slug, "kind": kind}
        # OMITTED, not `name or slug`. The server nulls a name byte-identical to
        # the slug (`app/core/naming.py::chosen_name`), so sending it was already
        # a no-op -- but with `authored_by` on the wire it became a LIE: the slug
        # plus a human declaration claims a person chose the identifier as the
        # title. Say nothing instead.
        if name:
            body["name"] = name
        _put_authorship(body, authored_by)
        if part_of:
            body["part_of"] = list(part_of)
        if parent_project_id is not None:
            body["parent_project_id"] = parent_project_id
        is_computer_workspace = False
        if workspace_id is not None:
            # A slug is looked up only here, on the create itself: a caller
            # whose project already exists never pays for (or trips on) it.
            workspace_id = self.workspace_id_for(workspace_id)
        elif parent_project_id is None and not part_of:
            # This computer's workspace: what its setup picked (`probe workspace
            # use`), or PROBE_WORKSPACE. None leaves it to the server, which
            # files into a team's only workspace and refuses (422
            # `workspace_required`) when there are several. Not for a linked
            # create: the server files that beside its first target, and
            # sending this computer's workspace would override it.
            workspace_id = self.computer_workspace_id()
            is_computer_workspace = workspace_id is not None
        if workspace_id is not None:
            body["workspace_id"] = workspace_id
        if description is not None:
            body["description"] = description
        if document is not None:
            body["document"] = document
        if tags is not None:
            body["tags"] = tags
        if metadata is not None:
            body["metadata"] = metadata
        try:
            row = self.transport.post("/v1/projects", body)
        except errors.WorkspaceRequired:
            # No workspace on this computer: pin the person's home here, then send
            # it again (every time, unless they ran `probe workspace use --clear`).
            home = None if "workspace_id" in body else self._pin_home_workspace()
            if home is None:
                raise
            body["workspace_id"] = home
            row = self.transport.post("/v1/projects", body)
        except errors.ValidationError as exc:
            # This computer's pin names a deleted workspace (A6): drop it and send
            # once more as a fresh computer would, into the home when there is one.
            if not (
                is_computer_workspace
                and isinstance(exc.detail, str)
                and exc.detail.startswith(errors.WORKSPACE_NOT_FOUND)
                and self._drop_dead_pin(body["workspace_id"])
            ):
                raise
            home = self._pin_home_workspace()
            if home is None:
                del body["workspace_id"]  # the server files a lone workspace, else 422s
            else:
                body["workspace_id"] = home
            row = self.transport.post("/v1/projects", body)
        if tags is not None:
            self._verify_tags_written(tags, row, "POST /v1/projects")
        return row

    def resolve_project(self, slug: str, *, strict: bool = False) -> dict | None:
        """Look a project up by slug. ``None`` when it does not exist.

        `(customer_id, slug)` is UNIQUE, so ``?slug=`` returns 0 or 1 row and an
        empty result is an unambiguous "absent" rather than "not on this page".
        Nothing is hidden from this read: a deleted project is gone, and its slug
        is free again."""
        rows = self.transport.get("/v1/projects", params={"slug": slug})
        return _exactly(rows, slug, strict=strict)

    def ensure_project(
        self, slug: str, name: str | None = None, *, kind: str = "general", **kw
    ) -> dict:
        """Get-or-create a project by slug. SDK-only; see :meth:`run`.

        ``kind`` defaults to ``"general"`` HERE, unlike :meth:`create_project`:
        the ensure path is what implicit machinery (``run()``'s auto-create,
        folder backfills) calls, and a default that silently mislabeled real
        intent would be worse than the neutral label. A caller that knows what
        it is building passes the real kind.

        :meth:`create_project` stays the explicit one, where a taken slug is an
        error. This is for callers who do not care whether it existed, only that
        it does now — but a slug that LOOKS like a typo of an existing one is
        refused rather than created. See :meth:`_refuse_near_miss`."""
        found = self.resolve_project(slug)
        if found is not None:
            return found
        self._guard_creatable("project", slug)
        try:
            return self.create_project(slug, name, kind=kind, **kw)
        except errors.ConflictError as exc:
            # Lost a create race with a concurrent process. Get-or-create promises
            # the row exists afterwards, not that WE made it, so re-resolve rather
            # than surface a conflict the caller cannot act on. Re-raise if it is
            # still absent — then the 409 meant something else.
            #
            # NOT the swallow #87 removed. That one hid a TYPO behind a
            # successful-looking create; this resolves a race between two
            # processes asking for the same, correct, slug.
            found = self.resolve_project(slug)
            if found is None:
                limit = getattr(self.settings, "workspace_limit", None)
                if limit is not None:
                    # Not a race: the slug's holder is a project this computer's
                    # workspace limit hides (slugs are one tenant-wide namespace).
                    # A bare 409 reads as a bug; say what it is and the way out.
                    raise errors.ConflictError(
                        f"project {slug!r} exists outside this computer's workspace limit "
                        f"{limit.label}: Probe here only sees that workspace, so it can neither "
                        f"use nor recreate it. Pick another project slug, or `probe workspace limit "
                        f"--team` (or `PROBE_WORKSPACE_LIMIT=team` for one job) to see the whole team.",
                        detail=exc.detail if isinstance(exc, errors.ConflictError) else None,
                    ) from exc
                raise
            return found

    def get_project(self, project_id: str) -> dict:
        return self.transport.get(f"/v1/projects/{project_id}")

    def _project_named(self, project: object) -> "tuple[dict | None, str | None]":
        """`run(project=)`'s project (and an offline run's at its sync, `offline`):
        the row an id-shaped ref names (`_project_by_id_ref`, never created),
        else the slug to resolve, or create under ``question=``. ``slug:`` is
        taken off: what follows is a slug, whatever it looks like."""
        ref = str(project)
        if ref.startswith("slug:"):
            return None, ref[len("slug:"):]
        if _id_ref(ref):
            return self._project_by_id_ref(ref), None
        return None, ref

    def _project_by_id_ref(self, ref: str) -> dict:
        """The project an id-shaped ref (`_id_ref`) names, or raise: never
        created (#3623: a run given its project's id was refused as "no project
        with slug", and with ``question=`` could make one slugged by the id).
        ``id:<uuid>`` is only ever the id. A bare one is a slug too, as
        everywhere (`test_ref_resolution.py`: one project's id was another's
        slug, and the wrong one was deleted): it names whichever project it is
        the slug or the id of, and when it is both, of two projects, it is
        refused with the spelling for each."""
        bare = ref.removeprefix("id:")
        by_slug = None if ref.startswith("id:") else self.resolve_project(ref)
        row = None
        if _BARE_ID.fullmatch(bare):
            try:
                row = self.get_project(bare.lower())
            except errors.NotFoundError:
                row = None
        if row is not None and row.get("kind") == "experiment":
            # Every experiment id is served at /v1/projects/{id} too.
            if by_slug is not None:
                return by_slug
            raise errors.ValidationError(
                f"{bare!r} is experiment {row.get('slug')!r}, not a project: "
                f"pass experiment={row.get('slug')!r} instead."
            )
        if by_slug is not None and row is not None and by_slug.get("id") != row.get("id"):
            raise errors.ValidationError(
                f"{bare!r} names two projects: it is the id of {row.get('slug')!r} and the slug of "
                f"another. Pass project='id:{bare}' for the first, project='slug:{bare}' for the second."
            )
        found = by_slug or row
        if found is None:
            from ....settings.workspace_limit import annotate_not_found, maybe_hidden_hint

            raise annotate_not_found(
                errors.NotFoundError(
                    f"no project with id {bare!r}"
                    + ("" if ref.startswith("id:") else " (nor with it as its slug)")
                    + ". `probe project list` shows the projects; an id is never created as a project."
                ),
                maybe_hidden_hint(getattr(self.settings, "workspace_limit", None)),
            )
        return found

    def get_project_overview(self, project_id: str) -> dict:
        """Read the complete saved unified Overview; never queue generation."""
        return self.transport.get(f"/v1/projects/{project_id}/overview")

    def list_project_sessions(
        self,
        project_id: str,
        *,
        order: str = "oldest",
        after: str | None = None,
        limit: int = 50,
    ) -> dict:
        """``GET /v1/projects/{P}/sessions``: one page of the coding-agent
        sessions that worked on the project or on something in it --
        ``{sessions, session_total, next_after}``.

        ``order`` is ``oldest`` (by when each session first touched the
        project, the detail read's order) or ``newest`` (the most recently
        active first). Pages past the first pass the previous page's
        ``next_after`` back as ``after``; ``limit`` is at most 50. An
        experiment id here is a 404: use :meth:`list_experiment_sessions`."""
        return self.transport.get(
            f"/v1/projects/{project_id}/sessions",
            params=_session_page_params(order, after, limit),
        )

    def list_project_contributors(self, project_id: str) -> list[dict]:
        """Who worked on this project. Projects are flat, so every credit is
        the project's own: `direct` is always true and `via_project_id` null
        (kept for older readers)."""
        return self.transport.get(f"/v1/projects/{project_id}/contributors")

    def add_project_contributor(self, project_id: str, user_id: str) -> dict:
        """Credit someone who has not written anything yet (a reviewer).
        422 if they are not an active member of the team."""
        return self.transport.post(f"/v1/projects/{project_id}/contributors", {"user_id": user_id})

    def remove_project_contributor(self, project_id: str, user_id: str) -> None:
        """Drop someone's credit on this project; 404 if they have none here.
        Not a ban: contributing again re-adds them."""
        self.transport.delete(f"/v1/projects/{project_id}/contributors/{user_id}")


class ProjectsResource(Resource):
    """`client.projects`: typed project reads. `Page.items` are `ProjectOut`; one project is
    `ProjectDetailOut`."""

    __slots__ = ()

    def get(self, project_id: str) -> ProjectDetailOut:
        """One project as `GET /v1/projects/{project}` serves it (`Client.get_project`)."""
        return self._to_model(ProjectDetailOut, self._client.get_project(project_id))

    def list(
        self,
        *,
        workspace_id: str | None = None,
        tags: list[str] | None = None,
        part_of: str | None = None,
        parent_id: str | None = None,
        **params: Any,
    ) -> Page:
        """A page of projects, filtered as `Client.list_projects` filters them."""
        page = self._client.list_projects(
            workspace_id=workspace_id, tags=tags, part_of=part_of, parent_id=parent_id, **params,
        )
        return self._to_typed_page(ProjectOut, page)

    def get_overview(self, project_id: str) -> OverviewOut:
        """`Client.get_project_overview` as an `OverviewOut`."""
        return self._to_model(OverviewOut, self._client.get_project_overview(project_id))

    def list_sessions(
        self, project_id: str, *, order: str = "oldest", after: str | None = None, limit: int = 50,
    ) -> LinkedSessionsOut:
        """`Client.list_project_sessions` as a `LinkedSessionsOut`."""
        return self._to_model(
            LinkedSessionsOut,
            self._client.list_project_sessions(project_id, order=order, after=after, limit=limit),
        )

    def get_metric(self, project_id: str) -> HeadlineMetricOut:
        """`Client.get_project_metric` as a `HeadlineMetricOut`."""
        return self._to_model(HeadlineMetricOut, self._client.get_project_metric(project_id))

    def get_best(self, project_id: str, *, history: int | None = None) -> BestPickOut:
        """`Client.get_project_best` as a `BestPickOut`."""
        return self._to_model(
            BestPickOut,
            self._client.get_project_best(project_id, history=history),
        )

    def get_workspace(
        self, project_id: str, *, scope: str | None = None, runs_limit: int | None = None,
        runs_offset: int | None = None, files_limit: int | None = None,
        include_experiments: bool | None = None,
    ) -> ProjectWorkspaceOut:
        """`Client.get_project_workspace` as a `ProjectWorkspaceOut`."""
        return self._to_model(
            ProjectWorkspaceOut,
            self._client.get_project_workspace(
                project_id, scope=scope, runs_limit=runs_limit, runs_offset=runs_offset,
                files_limit=files_limit, include_experiments=include_experiments,
            ),
        )

    def list_artifacts(self, project_id: str) -> builtins.list[ArtifactOut]:
        """`Client.list_project_artifacts` as `ArtifactOut`s."""
        return self._to_models(ArtifactOut, self._client.list_project_artifacts(project_id))

from probe.sdk.client.authorship import _put_authorship  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.ids import _BARE_ID, _id_ref  # noqa: E402 -- pieces need each other; the front door loads this one first

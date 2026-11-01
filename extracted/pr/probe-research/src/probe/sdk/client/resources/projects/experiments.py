"""ExperimentsResource (client.experiments, typed reads) and ExperimentsMixin, Client's methods:
create, fork, resolve, ensure and read experiments and their documents (twin: app/experiments)."""

from __future__ import annotations
import builtins
from .....generated.models import (
    ArtifactOut,
    ExperimentGroupOut,
    ExperimentInheritedOut,
    ExperimentReproduce,
    HeadlineMetricOut,
    LineageEdgeOut,
    LinkedSessionsOut,
    OverviewOut,
    OverviewStatusOut,
    ProjectExperimentDetailOut,
    ProjectExperimentOut,
    RunGroupOut,
)
from ....delivery.transport.transport import Page
from ...resource import Resource
import shlex
from typing import Any
from .....models import ProjectKind as _ProjectKind

from .... import errors
from ....errors import CapabilityUnavailable
from probe.sdk.client.resources.projects.experiment_locator import _walks_once


#: AN EXPERIMENT'S ADDRESS ON THE WIRE.
#:
#: 0231 made an experiment a project row (a "leaf") and retired
#: `/v1/experiments/*` (410). The light-experiments split gave experiments their
#: own record again and, at R4, this client moved onto the experiment API:
#: `/v1/projects/{project}/experiments[/{experiment}]` (see the experiments
#: section of `Client`). Since X21 the experiment's children are addressed
#: there too (`/v1/projects/{P}/experiments/{E}/<child>`), and the read-only
#: `Reader` reads the experiment API as well.
#:
#: Paths are spelled out at every call site rather than built by a helper:
#: `tests/test_parity.py` READS the client's source to decide which backend
#: routes a client can reach, and refuses a transport call whose path it cannot
#: resolve.


#: An experiment's description was replaced by its question (0231); both the
#: project address and the experiment API refuse it, and this says why first.
_EXPERIMENT_DESCRIPTION_RETIRED = (
    "an experiment's description was replaced by its QUESTION (0231): a "
    "leaf project's `description` field holds the question it answers, so "
    "there is no separate slot left for this text. Pass question= for what "
    "the experiment is testing, or document= for prose about it -- which is "
    "where existing descriptions were moved."
)

#: What a server without experiment forks (its route answers a route-absent
#: 404) is told: the SDK and the server ship on separate trains.
_PREDATES_FORKS = (
    "this Probe server predates experiment forks (POST .../experiments/{E}/fork, GET "
    ".../inherited); upgrade the server, or use `experiment create` + `edge add` with "
    "derived_from"
)


def _refuse_read_only_experiment_fields(**fields: object) -> None:
    """Refuse the fields an experiment no longer takes, before anything is sent.

    Since the light experiments' R3 switch an experiment is its own record, and
    the tags and metadata its project row carried are kept read-only (the
    project address answers 422 naming them); the experiment API has no such
    fields at all. Refusing here says so in one line instead of a round trip."""
    given = sorted(name for name, value in fields.items() if value is not None)
    if given:
        raise ValueError(
            f"{', '.join(given)} cannot be set on an experiment: an experiment's "
            "tags and metadata are kept read-only since it moved to its own record "
            "(light experiments). Set its name, question, notes or document instead."
        )


def _from_experiment_api(row: object) -> object:
    """An experiment from the experiment API, in the vocabulary callers already read.

    The experiment API answers an experiment AS an experiment: `project_id` is
    the project it is filed under and `question` the question it answers. Code
    written against the project address also reads `parent_project_id`,
    `description` (which held the question) and `kind`, so those are added --
    never replacing a field the API sent.

    `summary` on the API's detail read is the OVERVIEW PAGE's status, while on
    the project address `summary` was the deprecated alias of `summary_metrics`
    (headline numbers). It is renamed `overview_status` so no reader takes a
    page's queue state for a result."""
    if not isinstance(row, dict):
        return row
    out = dict(row)
    if isinstance(out.get("summary"), dict) and "content" in out["summary"]:
        out["overview_status"] = out.pop("summary")
    out.setdefault("kind", _ProjectKind.experiment.value)
    if "project_id" in out:
        out.setdefault("parent_project_id", out["project_id"])
    if "question" in out:
        out.setdefault("description", out["question"])
    return out


def _to_served_experiment(row: object) -> object:
    """The flat row as the server sent it: undo `_from_experiment_api`'s `summary` rename."""
    if isinstance(row, dict) and "overview_status" in row and "summary" not in row:
        return {**row, "summary": row["overview_status"]}
    return row


class ExperimentsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def create_experiment(
        self,
        slug: str,
        name: str | None = None,
        *,
        question: str | None = None,
        project_id: str,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        authored_by: str | None = None,
    ) -> dict:
        """Create an experiment in a project. Raises ``ConflictError`` if the slug is taken.

        ``POST /v1/projects/{project_id}/experiments``. The question is REQUIRED
        and is not synthesised. This used to accept ``None`` and compose a marked
        ``[auto]`` placeholder from ambient context, which then became permanent:
        an existing experiment keeps its own question first-write-wins, so
        nothing ever replaced the placeholder unless a human noticed and ran
        ``probe experiment set``. Making creation explicit means naming what you
        are testing at the moment you create it.

        Slugs are one namespace with project slugs, tenant-wide. On a 409 the
        error's ``existing`` names the holder (``id``, ``parent_project_id``,
        ``kind``); it is this experiment only when ``kind`` is ``experiment``
        and ``parent_project_id`` is ``project_id``.

        ``document`` seeds authored Markdown that lives INSIDE the experiment's
        Overview page, as a block the page's AI writer may not rewrite (written
        by a PATCH right after the create, which takes no document). A README
        embed in that document also derives the experiment's repo, using the
        same syntax documented by :meth:`update_experiment`.

        ``tags`` and ``description`` are refused: an experiment's tags are kept
        read-only since it moved to its own record, and its question replaced
        its description."""
        if not question:
            raise errors.ValidationError(
                f"an experiment needs a question: what do you expect {slug} to show?"
            )
        if not project_id:
            raise errors.ValidationError(
                "an experiment needs an explicit project_id; create or resolve the project first"
            )
        if description is not None:
            raise ValueError(_EXPERIMENT_DESCRIPTION_RETIRED)
        _refuse_read_only_experiment_fields(tags=tags)
        body: dict[str, Any] = {"slug": slug, "question": question}
        # See create_project: omitted, never the slug. Same reason.
        if name:
            body["name"] = name
        _put_authorship(body, authored_by)
        row = _from_experiment_api(
            self.transport.post(f"/v1/projects/{project_id}/experiments", body)
        )
        if document is not None:
            try:
                row["document"] = self._write_experiment_document(
                    str(row["id"]), document, authored_by, project_id=str(row["project_id"])
                )
            except errors.RosError as exc:
                raise errors.DocumentNotWritten(
                    f"experiment {slug!r} was created ({row['id']}), but its document was "
                    f"not written: {exc}. Write it with `probe experiment set "
                    f"{shlex.quote(slug)} --summary <markdown or @file>` (SDK: "
                    f"update_experiment({str(row['id'])!r}, document=...)); creating it "
                    "again would only meet its own slug.",
                    experiment=row,
                    status=exc.status,
                ) from exc
        return row

    def fork_experiment(
        self,
        source: str,
        slug: str,
        *,
        question: str,
        name: str | None = None,
        project_id: str | None = None,
        authored_by: str | None = None,
    ) -> dict:
        """Fork an experiment: a new experiment of the same project that starts
        where ``source`` is (``POST /v1/projects/{P}/experiments/{E}/fork``).

        The server COPIES the source's notes (opening with a line naming it),
        sub-notes, page document, tags, chart settings and its own files (rows
        naming the same bytes; nothing is uploaded again), links the fork
        ``forked_from`` the source, and lets the fork READ the source's runs and
        their files live (:meth:`experiment_inherited`) until one of those files
        changes on the source side -- then the fork keeps its own copy of what it
        had. The answer is the new experiment plus ``fork`` (what was copied and
        the link's id). ``question`` is the fork's own: what it tries that the
        source did not. A taken slug raises ``ConflictError``, as a create does."""
        if not question or not question.strip():
            raise errors.ValidationError(
                f"a fork needs its own question: what does {slug} try that the source did not?"
            )
        body: dict[str, Any] = {"slug": slug, "question": question}
        if name:
            body["name"] = name
        _put_authorship(body, authored_by)
        try:
            return _from_experiment_api(
                self._on_experiment(
                    lambda p, e: self.transport.post(
                        f"/v1/projects/{p}/experiments/{e}/fork", body
                    ),
                    source,
                    project_id,
                )
            )
        except CapabilityUnavailable as exc:
            raise CapabilityUnavailable("experiment_fork", _PREDATES_FORKS) from exc

    def experiment_inherited(
        self,
        experiment_id: str,
        *,
        runs: bool = False,
        after: str | None = None,
        limit: int | None = None,
        project_id: str | None = None,
    ) -> dict:
        """What a fork reads live from its source: its sources (nearest first)
        and one page of their run files, or with ``runs`` their runs, as they
        were at the fork (``GET /v1/projects/{P}/experiments/{E}/inherited``).
        A file id here is the source run's file: :meth:`download_artifact`
        reads it as is. Page on with ``after`` = the answer's ``next_after``."""
        params: dict[str, Any] = {"kind": "runs" if runs else "files"}
        if after is not None:
            params["after"] = after
        if limit is not None:
            params["limit"] = limit
        try:
            return self._on_experiment(
                lambda p, e: self.transport.get(
                    f"/v1/projects/{p}/experiments/{e}/inherited", params=params
                ),
                experiment_id,
                project_id,
            )
        except CapabilityUnavailable as exc:
            raise CapabilityUnavailable("experiment_fork", _PREDATES_FORKS) from exc

    def _write_experiment_document(
        self,
        experiment_id: str,
        document: str,
        authored_by: str | None,
        *,
        project_id: str | None = None,
    ) -> str | None:
        """Write an experiment's Overview-page block and check it landed.

        ``PATCH /v1/projects/{P}/experiments/{E}`` with ``document``. The check
        reads the write's OWN answer, which echoes the document it wrote: a
        detail GET answers from the page, a lossy rendering of what was sent
        (see :meth:`update_project`)."""
        body: dict[str, Any] = {"document": document}
        _put_authorship(body, authored_by)
        written = self._on_experiment(
            lambda p, e: self.transport.patch(f"/v1/projects/{p}/experiments/{e}", body),
            experiment_id,
            project_id,
        )
        self._verify_entity_markdown_written(
            "experiment", document, written, "PATCH /v1/projects/{P}/experiments/{E}"
        )
        return written.get("document") if isinstance(written, dict) else None

    def resolve_experiment(
        self, slug: str, *, strict: bool = False, project_id: str | None = None
    ) -> dict | None:
        """Look an experiment up by slug. ``None`` when it does not exist.

        With ``project_id``, one request: ``GET /v1/projects/{P}/experiments/{slug}``
        (None when it is not filed there, or is in the trash). Without it,
        experiment slugs are unique per TENANT: ``GET /v1/scopes?slug=`` places
        it and its project's item route reads it (two requests). Against a
        server older than that route, the caller's projects are walked.

        A slug an experiment had before a rename (``legacy_slug``) resolves too,
        after every live slug, as it does on the server. ``strict`` is accepted
        for callers of the old signature; there is no unfiltered listing left
        for it to guard against."""
        del strict
        if project_id:
            try:
                row = self.transport.get(f"/v1/projects/{project_id}/experiments/{slug}")
            except errors.NotFoundError:
                return None
            except errors.RosError as exc:
                if exc.in_trash:
                    # In the trash: its slug was moved aside and is free again.
                    return None
                raise
            return self._find_experiment([_from_experiment_api(row)], slug)
        try:
            scope = self._experiment_scope(slug)
        except CapabilityUnavailable:
            return self._walk_for_slug(slug)
        if scope is None:
            return None
        try:
            return self.get_experiment(
                str(scope.get("experiment_id") or scope["id"]), project_id=str(scope["project_id"])
            )
        except errors.NotFoundError:
            return None  # gone between the two reads

    @_walks_once
    def ensure_experiment(
        self,
        slug: str,
        name: str | None = None,
        *,
        question: str,
        project_id: str,
        **kw,
    ) -> dict:
        """Get-or-create an experiment by slug in a project. SDK-only; see :meth:`run`.

        ``question`` is REQUIRED and keyword-only: reaching this method means
        creation is on the table, and an experiment is never created without one.
        It is NOT applied to an experiment that already exists — those are
        first-write-wins, so reopening never rewrites the question. Nothing is
        synthesised; the ``[auto]`` placeholder was permanent unless a human
        noticed it, which is why it is gone.

        A slug that resolves to nothing but looks like a typo of an existing one
        is REFUSED, not created — see :meth:`_refuse_near_miss`. A create that
        loses a race adopts the winner only when it is an experiment filed in
        this same project (the server's 409 names the holder); a slug held by a
        project, or by an experiment in another project, raises. Callers who want
        the strict three-outcome error for an absent slug use
        :meth:`resolve_or_raise` instead."""
        found = self.resolve_experiment(slug, project_id=project_id)
        if found is not None:
            return found
        self._guard_creatable("experiment", slug)
        try:
            return self.create_experiment(
                slug, name, question=question, project_id=project_id, **kw
            )
        except errors.ConflictError as exc:
            holder = exc.existing if isinstance(exc.existing, dict) else {}
            if holder.get("kind") != _ProjectKind.experiment.value:
                raise
            if str(holder.get("parent_project_id")) != str(project_id):
                raise errors.ValidationError(
                    f"experiment {slug!r} already exists in another project "
                    f"({holder.get('parent_project_id')}), not in {project_id}. Name "
                    "the project it belongs to, or choose another slug."
                ) from exc
            # Lost a create race to the same experiment; see ensure_project.
            return self.get_experiment(
                str(holder.get("id") or exc.existing_id), project_id=project_id
            )

    def get_experiment(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """One experiment: identity, question, notes, run count, overview status.

        ``GET /v1/projects/{P}/experiments/{E}``, the project from ``project_id``
        or ``GET /v1/scopes/{E}``. ``experiment_id`` may also be its slug. The
        row names the project it is filed under as ``project_id`` (and, for
        callers of the project address, as ``parent_project_id``)."""
        project, experiment = self._locate_experiment(experiment_id, project_id)
        return _from_experiment_api(
            self.transport.get(f"/v1/projects/{project}/experiments/{experiment}")
        )

    def get_experiment_document(
        self, experiment_id: str, *, project_id: str | None = None
    ) -> str | None:
        """The experiment's authored Markdown (``document=``), as its Overview page
        holds it; None when it has none.

        The experiment detail's ``document`` (``GET /v1/projects/{P}/experiments/
        {E}``). Not byte-identical to what was sent: the page renders it (see
        :meth:`update_project`)."""
        row = self.get_experiment(experiment_id, project_id=project_id)
        return row.get("document") if isinstance(row, dict) else None

    def get_experiment_leaf(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """The experiment with its authored ``document`` and the notes' headroom
        (``notes_limit_tokens``, ``notes_tokens``, ``notes_remaining_tokens``; the
        ``notes_*_chars`` pair beside them measures the character backstop).

        Kept for callers of 0.209.0, which read these from the experiment's
        PROJECT address (``GET /v1/projects/{E}``). The experiment detail carries
        all three now, so this is :meth:`get_experiment`; nothing here addresses
        an experiment as a project."""
        return self.get_experiment(experiment_id, project_id=project_id)

    def get_experiment_overview(
        self, experiment_id: str, *, project_id: str | None = None, status_only: bool = False
    ) -> dict:
        """The experiment's Overview page (``OverviewOut``, the same shape as a
        project's), or with ``status_only`` just its freshness and queue state.

        ``GET /v1/projects/{P}/experiments/{E}/overview[/status]``. Its
        ``anchor_type`` reads ``project`` before the server's R3 switch and
        ``experiment`` after; never branch on it."""
        project, experiment = self._locate_experiment(experiment_id, project_id)
        if status_only:
            return self.transport.get(
                f"/v1/projects/{project}/experiments/{experiment}/overview/status"
            )
        return self.transport.get(f"/v1/projects/{project}/experiments/{experiment}/overview")

    def list_experiment_sessions(
        self,
        experiment_id: str,
        *,
        project_id: str | None = None,
        order: str = "oldest",
        after: str | None = None,
        limit: int = 50,
    ) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/sessions``: one page of the
        coding-agent sessions that worked on the experiment or on something in
        it -- ``{sessions, session_total, next_after}``, the same page shape and
        parameters as :meth:`list_project_sessions`."""
        project, experiment = self._locate_experiment(experiment_id, project_id)
        return self.transport.get(
            f"/v1/projects/{project}/experiments/{experiment}/sessions",
            params=_session_page_params(order, after, limit),
        )


class ExperimentsResource(Resource):
    """`client.experiments`: typed experiment reads. `Page.items` are `ProjectExperimentOut`; one
    experiment is `ProjectExperimentDetailOut`."""

    __slots__ = ()

    def get(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> ProjectExperimentDetailOut:
        """`Client.get_experiment` as the server's `ProjectExperimentDetailOut`: its `summary` is
        the overview status the flat read renames `overview_status`."""
        row = self._client.get_experiment(experiment_id, project_id=project_id)
        return self._to_model(ProjectExperimentDetailOut, _to_served_experiment(row))

    def list(
        self, *, project_id: str | None = None, name: str | None = None, limit: int | None = None,
        cursor: str | None = None,
    ) -> Page:
        """`Client.list_experiments` with its items as `ProjectExperimentOut`; `next_cursor`
        unchanged. No `tags` or other filters: the flat method refuses every one of them."""
        return self._to_typed_page(
            ProjectExperimentOut,
            self._client.list_experiments(
                project_id=project_id, name=name, limit=limit, cursor=cursor,
            ),
        )

    def get_overview(self, experiment_id: str, *, project_id: str | None = None) -> OverviewOut:
        """`Client.get_experiment_overview` as an `OverviewOut`."""
        return self._to_model(
            OverviewOut,
            self._client.get_experiment_overview(experiment_id, project_id=project_id),
        )

    def get_overview_status(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> OverviewStatusOut:
        """`Client.get_experiment_overview(status_only=True)` as an `OverviewStatusOut`."""
        return self._to_model(
            OverviewStatusOut,
            self._client.get_experiment_overview(
                experiment_id, project_id=project_id, status_only=True,
            ),
        )

    def list_sessions(
        self, experiment_id: str, *, project_id: str | None = None, order: str = "oldest",
        after: str | None = None, limit: int = 50,
    ) -> LinkedSessionsOut:
        """`Client.list_experiment_sessions` as a `LinkedSessionsOut`."""
        return self._to_model(
            LinkedSessionsOut,
            self._client.list_experiment_sessions(
                experiment_id, project_id=project_id, order=order, after=after, limit=limit,
            ),
        )

    def get_inherited_files(
        self, experiment_id: str, *, after: str | None = None, limit: int | None = None,
        project_id: str | None = None,
    ) -> ExperimentInheritedOut:
        """`Client.experiment_inherited` (its source's run files) as an `ExperimentInheritedOut`."""
        return self._to_model(
            ExperimentInheritedOut,
            self._client.experiment_inherited(
                experiment_id, after=after, limit=limit, project_id=project_id,
            ),
        )

    def get_inherited_runs(
        self, experiment_id: str, *, after: str | None = None, limit: int | None = None,
        project_id: str | None = None,
    ) -> ExperimentInheritedOut:
        """`Client.experiment_inherited(runs=True)` (its source's runs) as an
        `ExperimentInheritedOut`."""
        return self._to_model(
            ExperimentInheritedOut,
            self._client.experiment_inherited(
                experiment_id, after=after, limit=limit, project_id=project_id, runs=True,
            ),
        )

    def list_groups(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> builtins.list[ExperimentGroupOut]:
        """`Client.list_groups` as `ExperimentGroupOut`s."""
        return self._to_models(
            ExperimentGroupOut,
            self._client.list_groups(experiment_id, project_id=project_id),
        )

    def get_group(self, group_id: str) -> RunGroupOut:
        """`Client.get_group` as a `RunGroupOut`."""
        return self._to_model(RunGroupOut, self._client.get_group(group_id))

    def list_edges(
        self, experiment_id: str, *, limit: int | None = None, project_id: str | None = None,
    ) -> builtins.list[LineageEdgeOut]:
        """`Client.experiment_edges` as `LineageEdgeOut`s."""
        return self._to_models(
            LineageEdgeOut,
            self._client.experiment_edges(experiment_id, limit=limit, project_id=project_id),
        )

    def get_metric(self, experiment_id: str, *, project_id: str | None = None) -> HeadlineMetricOut:
        """`Client.get_experiment_metric` as a `HeadlineMetricOut`."""
        return self._to_model(
            HeadlineMetricOut,
            self._client.get_experiment_metric(experiment_id, project_id=project_id),
        )

    def get_reproduction(
        self, experiment_id: str, *, version: int | None = None, project_id: str | None = None,
    ) -> ExperimentReproduce:
        """`Client.experiment_reproduce` as an `ExperimentReproduce`."""
        return self._to_model(
            ExperimentReproduce,
            self._client.experiment_reproduce(
                experiment_id, version=version, project_id=project_id,
            ),
        )

    def list_artifacts(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> builtins.list[ArtifactOut]:
        """`Client.list_experiment_artifacts` as `ArtifactOut`s."""
        return self._to_models(
            ArtifactOut,
            self._client.list_experiment_artifacts(experiment_id, project_id=project_id),
        )

from probe.sdk.client.authorship import _put_authorship  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.projects.projects import _session_page_params  # noqa: E402 -- pieces need each other; the front door loads this one first

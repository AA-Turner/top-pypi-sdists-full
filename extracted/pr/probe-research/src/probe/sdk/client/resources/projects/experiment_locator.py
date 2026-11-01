"""ExperimentLocatorMixin, Client's methods: find which project an experiment lives in -- scopes,
the home cache, one shared tenant-wide walk (twins: app/projects, app/experiments)."""

from __future__ import annotations

import contextvars
import functools
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from collections.abc import Callable, Iterable
from typing import Any
from .....models import ScopeKind as _ScopeKind

from .... import errors
from ....errors import CapabilityUnavailable
from ....delivery.ops.ops import UNPLACED_PROJECT

#: The experiment API's page sizes (`app/experiments/store.py`,
#: `read_router.py`): at most 500 per page, 100 when unasked.
_EXPERIMENT_PAGE_MAX = 500

#: A child route this server does not have: it predates X21.
_PREDATES_CHILD_ROUTES = (
    "this Probe server predates the experiment API's child routes (research-os #2282, "
    "light experiments X21 -- and X21b for an experiment's W&B sources), which this client "
    "uses for an experiment's runs, groups, files, notes, lineage and W&B sources; upgrade "
    "the server, or keep the previous probe release until it is"
)


def _moved_away(exc: errors.RosError) -> bool:
    """A 404 or 410 at an experiment's remembered or supplied project: it may
    have moved, so it is worth placing again. Not a route-absent 404."""
    return bool(exc.in_trash) or (
        isinstance(exc, errors.NotFoundError) and not _route_absent(exc)
    )


def _experiment_pages(transport: Any, project_id: str, *, missing_ok: bool = True) -> list[dict]:
    """One project's experiments through the experiment API, every page
    (offset paged, newest first, :data:`_EXPERIMENT_PAGE_MAX` a page). With
    ``missing_ok`` a project that went away (404) or into the trash (410)
    since it was listed is [] -- a walk skips it; without, the error rises."""
    rows: list[dict] = []
    offset = 0
    while True:
        try:
            page = transport.get(
                f"/v1/projects/{project_id}/experiments",
                params={"limit": _EXPERIMENT_PAGE_MAX, "offset": offset},
            )
        except errors.NotFoundError:
            if missing_ok:
                return rows
            raise
        except errors.RosError as exc:
            if missing_ok and exc.in_trash:
                return rows
            raise
        rows.extend(_from_experiment_api(item) for item in page.get("items") or [])
        next_offset = page.get("next_offset")
        if next_offset is None:
            return rows
        offset = next_offset


def _offset_cursor(cursor: str | None) -> int:
    """The experiment list's page token: an offset, as this client hands it out."""
    if cursor in (None, ""):
        return 0
    try:
        offset = int(str(cursor))
    except ValueError:
        raise ValueError(
            f"cursor {cursor!r} is not an experiment-list cursor (an older client's "
            "keyset cursor does not carry over); start from the first page"
        ) from None
    if offset < 0:
        raise ValueError("cursor cannot be negative")
    return offset


#: How many projects' experiment lists one walk fetches at once.
_WALK_CONCURRENCY = 8

#: A walk of every project's experiments, kept for ONE top-level call
#: (`run()`, `ensure_experiment`, `resolve_or_raise`): the near-miss guard can
#: be asked twice in one call (before a parent project is committed, then again
#: in the create), and the second ask must not walk the tenant again. Keyed by
#: client, per context (so per thread), and only ever holding a COMPLETE walk.
_WALK_MEMO: contextvars.ContextVar[dict[int, list[dict]] | None] = contextvars.ContextVar(
    "probe_experiment_walk_memo", default=None
)


@contextmanager
def _one_walk():
    """Share one experiment walk across everything inside this block."""
    if _WALK_MEMO.get() is not None:
        yield
        return
    token = _WALK_MEMO.set({})
    try:
        yield
    finally:
        _WALK_MEMO.reset(token)


def _walks_once(method):
    """Run a top-level method inside :func:`_one_walk`."""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        with _one_walk():
            return method(*args, **kwargs)

    return wrapper


class ExperimentLocatorMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- experiments --------------------------------------------------------
    #
    # THE EXPERIMENT API (light experiments R4). An experiment is read and
    # written as an experiment, under the project it is filed in:
    #
    #   GET    /v1/projects/{P}/experiments            list (offset paged, with a total)
    #   POST   /v1/projects/{P}/experiments            create
    #   GET    /v1/projects/{P}/experiments/{E}        one (uuid, slug or legacy slug)
    #   PATCH  /v1/projects/{P}/experiments/{E}        edit; `project_id` moves it
    #   DELETE /v1/projects/{P}/experiments/{E}        move to the trash
    #   GET    /v1/scopes/{id}                         where an id is filed
    #   GET    /v1/projects/{P}/workspace?scope=...    T16: one scope in one read
    #   /v1/projects/{P}/experiments/{E}/<child>       its runs, groups, edges,
    #       lineage, versions, reproduce, code, artifacts[/uploads], sub-notes,
    #       notes/versions (server X21)
    #
    # Nothing here addresses an experiment as a project (`/v1/projects/{E}`):
    # from the server's R4 refusal on, an older client that does is answered
    # 410 `client_too_old`, and R6 removes that address. The experiment's
    # `document` (a block of its Overview page) is the detail's `document` and
    # the PATCH's; a child route needs the project the experiment is filed in,
    # which `_on_experiment` finds once per client (`GET /v1/scopes/{E}`) when
    # the caller does not pass it. Its W&B sources are children too (server
    # X21b), and a run moves into it by `experiment_id` on the run PATCH.
    #
    # The writes take uuids only (the server refuses a slug in either slot:
    # a slug can be minted again once its holder is in the trash), so a slug is
    # resolved to its id first.

    def get_scope(self, scope_id: str) -> dict:
        """What a project, experiment or run id is, and where it is filed:
        ``{id, kind: project|experiment|run, project_id, experiment_id, run_id}``.

        ``GET /v1/scopes/{id}``. 404 for an id the caller cannot see, 410 with the
        trash notice for one in the trash. ``project_id`` is null only for an
        unfiled run."""
        return self.transport.get(f"/v1/scopes/{scope_id}")

    def get_scope_by_slug(self, slug: str) -> dict:
        """The project or experiment ``slug`` names, tenant-wide, in the same
        shape as :meth:`get_scope`: a live experiment slug, else a project's,
        else the slug an experiment had before a rename.

        ``GET /v1/scopes?slug=``. 404 when nothing the caller can see holds it,
        410 with the trash notice when the holder is in the trash. Raises
        ``CapabilityUnavailable`` against a server that predates the route."""
        try:
            return self.transport.get("/v1/scopes", params={"slug": slug})
        except errors.NotFoundError as exc:
            if _route_absent(exc):
                raise CapabilityUnavailable(
                    "scope_by_slug", "this Probe server has no GET /v1/scopes?slug= yet"
                ) from None
            raise

    def _experiment_scope(self, slug: str) -> dict | None:
        """The scope of the EXPERIMENT ``slug`` names, or None (nothing holds it,
        the holder is in the trash, or a project holds it). Raises
        ``CapabilityUnavailable`` against an older server."""
        try:
            scope = self.get_scope_by_slug(slug)
        except errors.NotFoundError:
            return None
        except errors.RosError as exc:
            if exc.in_trash:
                return None
            raise
        if scope.get("kind") != _ScopeKind.experiment.value or not scope.get("project_id"):
            return None
        return scope

    def get_project_workspace(
        self,
        project_id: str,
        *,
        scope: str | None = None,
        runs_limit: int | None = None,
        runs_offset: int | None = None,
        files_limit: int | None = None,
        include_experiments: bool | None = None,
    ) -> dict:
        """One scope of a project in one read (the T16 workspace read model).

        Not :meth:`get_workspace`, which reads a WORKSPACE (the place projects
        are filed); this reads a project's page for one of its scopes.

        ``scope`` is ``project:<id>`` (the default), ``experiment:<id>`` or
        ``run:<id>``, and must be inside the project. Answers ``{project_id,
        scope, writable, experiments, runs: {ids, total, limit, offset,
        next_offset, series_cap}, question, summary, files}``: the project's
        experiments with run counts (null with ``include_experiments=False``),
        the run ids in scope newest first (at most ``series_cap`` per page, the
        most one series query takes), the experiment's question, the scope's
        overview status and the root of its Files tree."""
        params = {
            key: value
            for key, value in {
                "scope": scope,
                "runs_limit": runs_limit,
                "runs_offset": runs_offset,
                "files_limit": files_limit,
                "include_experiments": (
                    None if include_experiments is None else str(include_experiments).lower()
                ),
            }.items()
            if value is not None
        }
        return self.transport.get(f"/v1/projects/{project_id}/workspace", params=params or None)

    def _locate_experiment(self, ref: str, project_id: str | None) -> tuple[str, str]:
        """``(project id, experiment ref)`` for an experiment the caller named.

        With the project known, the ref goes to the server as given (the item
        route takes a uuid, slug or legacy slug). Without it, ONE request places
        it: ``GET /v1/scopes/{id}`` for a uuid, ``GET /v1/scopes?slug=`` for a
        slug. Only a server older than that route makes a slug cost a walk of
        the caller's projects (:meth:`_tenant_experiments`)."""
        ref = str(ref)
        if project_id:
            return str(project_id), ref
        if _is_uuid(ref):
            scope = self.get_scope(ref)
            if scope.get("kind") != _ScopeKind.experiment.value or not scope.get("project_id"):
                raise errors.NotFoundError(
                    f"no experiment with id {ref!r}: that id is a {scope.get('kind') or 'something else'}"
                )
            return self._remember_home(str(scope["project_id"]), ref)
        try:
            scope = self._experiment_scope(ref)
        except CapabilityUnavailable:
            row = self._walk_for_slug(ref)
            if row is None:
                raise errors.NotFoundError(f"no experiment {ref!r}") from None
            return self._remember_home(str(row["project_id"]), str(row["id"]))
        if scope is None:
            raise errors.NotFoundError(f"no experiment {ref!r}")
        return self._remember_home(
            str(scope["project_id"]), str(scope.get("experiment_id") or scope["id"])
        )

    def _remember_home(self, project: str, experiment: str) -> tuple[str, str]:
        """Remember where the server just said an experiment is filed, so its
        child routes cost no second lookup; ``(project, experiment)``."""
        if _is_uuid(project) and _is_uuid(experiment):
            self._experiment_homes[experiment] = project
        return project, experiment

    def _experiment_ids(self, ref: str, project_id: str | None) -> tuple[str, str]:
        """``(project uuid, experiment uuid)``: what the experiment API's writes take."""
        project, experiment = self._locate_experiment(ref, project_id)
        if not _is_uuid(experiment) or not _is_uuid(project):
            row = self.get_experiment(experiment, project_id=project)
            project, experiment = str(row["project_id"]), str(row["id"])
        return project, experiment

    def _experiment_home(
        self, ref: str, project_id: str | None = None
    ) -> tuple[str, str, bool]:
        """``(project uuid, experiment uuid, from_cache)`` to address one of an
        experiment's CHILD routes (``/v1/projects/{P}/experiments/{E}/...``).

        An experiment's children (runs, groups, files, notes history, sub-notes,
        versions, lineage) are addressed under the project it is filed in, so a
        caller holding only the experiment's id costs one ``GET /v1/scopes/{E}``
        -- once per client: the answer is remembered by experiment id. A move
        makes it stale, which :meth:`_on_experiment` repairs on the 404."""
        homes = self._experiment_homes
        ref = str(ref)
        if project_id and _is_uuid(ref) and _is_uuid(str(project_id)):
            homes[ref] = str(project_id)
            return str(project_id), ref, False
        if not project_id and ref in homes:
            return homes[ref], ref, True
        project, experiment = self._experiment_ids(ref, project_id)
        homes[experiment] = project
        return project, experiment, False

    def _on_experiment(
        self,
        call: Callable[[str, str], Any],
        experiment_id: str,
        project_id: str | None = None,
        *,
        journaled: bool = False,
    ) -> Any:
        """``call(project, experiment)`` on an experiment's child route.

        ``call`` spells its path as a literal f-string (``f"/v1/projects/{p}/
        experiments/{e}/groups"``): the parity guard reads call sites statically,
        and a path built from a shared prefix would be invisible to it.

        A 404 or 410 at a project this did not just get from ``/v1/scopes`` --
        remembered, or supplied by the caller -- means the experiment may have
        moved since: its place is asked again and, if that names another
        project, the call is made once more (a 404 or 410 creates nothing, so a
        create is safe to resend). A route-absent 404 is a server older than
        X21, said so (``CapabilityUnavailable``).

        ``journaled=True``: the caller's write is about to be QUEUED rather than
        sent (:meth:`_journals`). It is queued under the experiment alone
        (``/v1/projects/~/experiments/{E}/...``) and placed when it drains, so
        queueing needs no network and survives a move. Only for an experiment
        uuid: a slug has to be placed now to be named at all."""
        if journaled and _is_uuid(str(experiment_id)):
            return call(UNPLACED_PROJECT, str(experiment_id))
        supplied = bool(project_id)
        try:
            project, experiment, cached = self._experiment_home(experiment_id, project_id)
        except errors.RosError as exc:
            # A slug looked up under a supplied project that does not hold it.
            if not (supplied and _moved_away(exc)):
                raise
            project, experiment, cached = self._experiment_home(experiment_id, None)
            supplied = False
        try:
            return call(project, experiment)
        except errors.RosError as exc:
            if _route_absent(exc):
                raise CapabilityUnavailable(
                    "experiment_child_routes", _PREDATES_CHILD_ROUTES
                ) from exc
            if not ((cached or supplied) and _moved_away(exc)):
                raise
            self._experiment_homes.pop(experiment, None)
            try:
                fresh, experiment, _ = self._experiment_home(experiment, None)
            except errors.RosError:
                raise exc from None
            if fresh == project:
                raise
            return call(fresh, experiment)

    def _journals(self, *, strict: bool | None, sync: bool = False) -> bool:
        """Whether :meth:`write` would QUEUE a durable write with these flags
        rather than send it. The one place that decision is spelled, so a
        caller that addresses the write differently when queued
        (:meth:`_on_experiment` ``journaled=``) cannot drift from it."""
        strict = (not self.fail_open) if strict is None else strict
        return self._delivery.sink.queues(strict=strict, sync=sync)

    def _tenant_experiments(self, *, stop_at: str | None = None) -> list[dict]:
        """Every experiment the caller can see, project by project.

        The experiment API lists experiments PER PROJECT, so this reads the
        project list (it never holds an experiment) and each project's
        experiments, :data:`_WALK_CONCURRENCY` projects at a time. Paid only
        where a whole list is the question -- the near-miss guard, a
        project-less ``list_experiments`` -- or against a server older than
        ``GET /v1/scopes?slug=``. ``stop_at`` ends the walk at the first batch
        holding that live slug. A project trashed or hidden mid-walk is skipped.
        Inside :func:`_one_walk` a complete walk is fetched once."""
        memo = _WALK_MEMO.get()
        if memo is not None and id(self) in memo:
            return memo[id(self)]
        projects = [str(row["id"]) for row in self._all_slugs("project")]
        rows: list[dict] = []
        complete = True
        if projects:
            with ThreadPoolExecutor(max_workers=min(_WALK_CONCURRENCY, len(projects))) as pool:
                for start in range(0, len(projects), _WALK_CONCURRENCY):
                    batch = projects[start : start + _WALK_CONCURRENCY]
                    # Each task in a COPY of this context: the hosted MCP binds the
                    # caller's client headers in a context variable, and a bare
                    # worker thread would report the server's own version instead.
                    futures = [
                        pool.submit(contextvars.copy_context().run, self._experiments_of, pid)
                        for pid in batch
                    ]
                    for future in futures:
                        rows.extend(future.result())
                    if stop_at is not None and any(r.get("slug") == stop_at for r in rows):
                        complete = start + _WALK_CONCURRENCY >= len(projects)
                        break
        if complete and memo is not None:
            memo[id(self)] = rows
        return rows

    def _experiments_of(self, project_id: str) -> list[dict]:
        """One project's experiments, every page; [] for a project that went
        away (404) or into the trash (410) since the project list was read."""
        return _experiment_pages(self.transport, project_id)

    def _walk_for_slug(self, slug: str) -> dict | None:
        """The experiment ``slug`` names, found by walking (an older server only)."""
        return self._find_experiment(self._tenant_experiments(stop_at=slug), slug)

    @staticmethod
    def _find_experiment(rows: Iterable[dict], slug: str) -> dict | None:
        """The experiment ``slug`` names: its slug, else the slug it had before a
        rename (``legacy_slug``) -- second, as the server's resolvers rank them,
        so a live slug outranks somebody's remembered name for another row."""
        rows = list(rows)
        for row in rows:
            if row.get("slug") == slug:
                return row
        for row in rows:
            if row.get("legacy_slug") == slug:
                return row
        return None
from probe.sdk.client.ids import _is_uuid  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.projects.experiments import _from_experiment_api  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.server_features import _route_absent  # noqa: E402 -- pieces need each other; the front door loads this one first

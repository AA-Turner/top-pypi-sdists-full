"""SummariesResource (client.summaries, typed reads) and SummariesMixin, Client's methods: a
project's or experiment's summary, versions and visuals (twins: app/summaries, app/overviews)."""

from __future__ import annotations
from .....generated.models import (
    SummaryOut,
    SummaryVersionOut,
    SummaryVersionsOut,
    VisualsOptionsOut,
)
from ...resource import Resource
from typing import Any

from .... import errors
from ....errors import CapabilityUnavailable


#: What a server without the summary and visuals routes (a route-absent 404)
#: is told: the CLI ships on its own train.
_PREDATES_SUMMARIES = (
    "this Probe server predates recorder summaries (GET/PUT .../summary, .../visuals); "
    "upgrade the server, or keep the previous probe release until it is"
)


class SummariesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- summaries (recorder-written, project and experiment) -----------------
    #
    # ONE method per read for BOTH anchors, keyed by which of `project` /
    # `experiment` is given, as the CLI's `probe summary` is (`--project P` |
    # `--experiment E [--project P]`). The experiment's project is located the
    # way every experiment read locates it (`_locate_experiment`).

    def _summary_anchor(
        self, project: str | None, experiment: str | None
    ) -> tuple[str, str | None]:
        """``(project id, experiment ref | None)`` for a summary read."""
        if experiment is not None:
            return self._locate_experiment(experiment, project)
        if project is None:
            raise ValueError("name the anchor: project=<ref> or experiment=<ref>")
        return str(project), None

    def get_summary(
        self,
        *,
        project: str | None = None,
        experiment: str | None = None,
        format: str | None = None,
    ) -> dict:
        """``GET …/summary``: the project's or experiment's summary as Markdown
        (``markdown`` is ``""`` with no page), with ``version``, ``edited_at``,
        ``edited_by``, ``via``, ``session_title``, ``you``, ``today`` and the
        tenant's ``mode`` (``lane`` | ``recorder``). ``format="html"`` asks for
        the full page instead: ``format``, ``html`` (a person's blocks between
        ``<!-- kept: hN -->`` markers), ``series`` (its chart declarations) and
        ``chartable`` (what they may name). A server older than full pages
        ignores the parameter: no ``format`` key comes back, and the answer is
        Markdown."""
        p, e = self._summary_anchor(project, experiment)
        params = {"format": format} if format else None
        if e is None:
            return self.transport.get(f"/v1/projects/{p}/summary", params=params)
        return self.transport.get(f"/v1/projects/{p}/experiments/{e}/summary", params=params)

    def list_summary_versions(
        self,
        *,
        project: str | None = None,
        experiment: str | None = None,
        before: int | None = None,
        limit: int = 20,
    ) -> dict:
        """``GET …/summary/versions``: ``{versions, next_before}``, newest first,
        each ``{version, created_at, created_by, source, via, mode,
        session_title, size_chars}``. ``before`` resumes past a version number
        (a page's ``next_before``); ``limit`` is at most 50."""
        params: dict[str, Any] = {"limit": limit}
        if before is not None:
            params["before"] = before
        p, e = self._summary_anchor(project, experiment)
        if e is None:
            return self.transport.get(f"/v1/projects/{p}/summary/versions", params=params)
        return self.transport.get(
            f"/v1/projects/{p}/experiments/{e}/summary/versions", params=params
        )

    def get_summary_version(
        self, version: int, *, project: str | None = None, experiment: str | None = None
    ) -> dict:
        """``GET …/summary/versions/{v}``: one version's ``markdown`` with its
        ``created_at``, ``created_by``, ``source``, ``via`` and ``mode``."""
        p, e = self._summary_anchor(project, experiment)
        v = int(version)
        if e is None:
            return self.transport.get(f"/v1/projects/{p}/summary/versions/{v}")
        return self.transport.get(f"/v1/projects/{p}/experiments/{e}/summary/versions/{v}")

    # -- summaries and Metrics-center visuals (writer-owns-summary) -------------
    # A project's or an experiment's summary is its Overview page as Markdown,
    # kept by whoever records the session (the daemon's writer, an inline agent,
    # the main agent with Probe on). Every method takes `project=`, and
    # `experiment=` (an id or slug) for an experiment's page; the reads are
    # `get_summary`, `list_summary_versions` and `get_summary_version` above:
    #
    #   GET  .../summary[?format=html]     SummaryOut {markdown | html+series+chartable, version, you, today, mode, ...}
    #   PUT  .../summary                   {markdown | html (+series), expected_version, session_id, directed}
    #   GET  .../summary/versions          {versions, next_before}
    #   GET  .../summary/versions/{v}      one version's Markdown
    #   GET  .../visuals/options           the closed set `visuals set` picks from
    #   PUT  .../visuals                   {visuals, expected_version, directed}
    #
    # where `...` is `/v1/projects/{P}` or `/v1/projects/{P}/experiments/{E}`.
    # The PUTs are NOT retried on a 503: `summary_writer_off` answers the same
    # until the team's switch moves, and a retry only delays saying so.

    def _summary_route(self, call_project, call_experiment, project_id, experiment_id):
        """Call the project route, or the experiment's (placed through
        `_on_experiment`). A server without these routes answers FastAPI's own
        404, said as `CapabilityUnavailable("summaries")`."""
        try:
            if experiment_id is not None:
                return self._on_experiment(call_experiment, str(experiment_id), project_id)
            if not project_id:
                raise ValueError("name the anchor: project=<ref> or experiment=<ref>")
            return call_project(str(project_id))
        except CapabilityUnavailable as exc:
            raise CapabilityUnavailable("summaries", _PREDATES_SUMMARIES) from exc
        except errors.NotFoundError as exc:
            if _route_absent(exc):
                raise CapabilityUnavailable("summaries", _PREDATES_SUMMARIES) from exc
            raise

    def put_summary(
        self,
        markdown: str | None = None,
        *,
        expected_version: int,
        project: str | None = None,
        experiment: str | None = None,
        session_id: str | None = None,
        directed: bool = False,
        html: str | None = None,
        series: list | None = None,
        whole_page: bool = False,
    ) -> dict:
        """Replace the summary from ``markdown``, or from ``html`` -- the full
        page as ``get_summary(format="html")`` gave it, its chart declarations
        in ``series`` or in the draft's ``data-probe-series`` block -- never
        both: ``{version, markdown}`` (``markdown``, or ``html`` and
        ``series``, is what a fresh GET in that format now returns). Raises
        ``ConflictError`` on a 409 whose ``detail.code`` says why:
        ``version_moved`` (``detail`` carries the head's ``version`` and
        ``markdown``, or ``html`` and ``series``, to merge onto),
        ``erased_since_checkout`` (check out again: no merge) or
        ``session_erased``; ``ValidationError`` on a 422 (``detail.code`` and
        ``detail.message`` state the limit); ``ServerError`` 503
        ``summary_writer_off`` while the team's pages are the overview lane's."""
        if (markdown is None) == (html is None):
            raise ValueError("put_summary takes exactly one of markdown= and html=")
        body: dict[str, Any] = {
            "expected_version": int(expected_version),
            "session_id": session_id,
            "directed": bool(directed),
        }
        if html is not None:
            body["html"] = html
            if series is not None:
                body["series"] = series
            if whole_page:
                # The writer's checkout pushed whole: the only push the server
                # judges `no_chart` (an older server ignores the field).
                body["whole_page"] = True
        else:
            body = {"markdown": markdown, **body}
        return self._summary_route(
            lambda p: self.transport.request(
                "PUT", f"/v1/projects/{p}/summary", json_body=body, idempotent=False
            ).json(),
            lambda p, e: self.transport.request(
                "PUT", f"/v1/projects/{p}/experiments/{e}/summary", json_body=body, idempotent=False
            ).json(),
            project,
            experiment,
        )

    def get_visuals_options(
        self, *, project: str | None = None, experiment: str | None = None
    ) -> dict:
        """What the Metrics center's tables and charts may name, in the names
        the server's checker accepts: ``scope``, ``eligible`` / ``reason``,
        ``version`` (the page's: send it back as ``expected_version``),
        ``current`` (the stored list), ``kinds``, ``runs`` (newest first) /
        ``runs_truncated`` / ``statuses``, ``metrics`` (``key``, ``kind``,
        ``dimensions``, ``per_sample``) / ``metrics_open``, ``summary_paths``
        / ``config_paths`` / ``paths_truncated`` and ``caps`` (None when not
        eligible)."""
        return self._summary_route(
            lambda p: self.transport.get(f"/v1/projects/{p}/visuals/options"),
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/visuals/options"),
            project,
            experiment,
        )

    def put_visuals(
        self,
        visuals: list,
        *,
        expected_version: int,
        project: str | None = None,
        experiment: str | None = None,
        directed: bool = False,
    ) -> dict:
        """Replace the Metrics center's tables and charts: ``{version, visuals:
        [{id, kind}]}``. ``ConflictError`` (409 ``version_moved``, ``detail``
        carries the ``current`` list: no merge, choose again),
        ``ValidationError`` (422 ``visuals_refused``: the checker's message),
        ``ServerError`` 503 ``summary_writer_off``."""
        body = {"visuals": list(visuals), "expected_version": int(expected_version),
                "directed": bool(directed)}
        return self._summary_route(
            lambda p: self.transport.request(
                "PUT", f"/v1/projects/{p}/visuals", json_body=body, idempotent=False
            ).json(),
            lambda p, e: self.transport.request(
                "PUT", f"/v1/projects/{p}/experiments/{e}/visuals", json_body=body, idempotent=False
            ).json(),
            project,
            experiment,
        )


class SummariesResource(Resource):
    """`client.summaries`: typed reads of a project's or experiment's summary document."""

    __slots__ = ()

    def get(
        self, *, project: str | None = None, experiment: str | None = None,
        format: str | None = None,
    ) -> SummaryOut:
        """`Client.get_summary` as a `SummaryOut`."""
        return self._to_model(
            SummaryOut,
            self._client.get_summary(project=project, experiment=experiment, format=format),
        )

    def list_versions(
        self, *, project: str | None = None, experiment: str | None = None,
        before: int | None = None, limit: int = 20,
    ) -> SummaryVersionsOut:
        """`Client.list_summary_versions` as a `SummaryVersionsOut`."""
        return self._to_model(
            SummaryVersionsOut,
            self._client.list_summary_versions(
                project=project, experiment=experiment, before=before, limit=limit,
            ),
        )

    def get_version(
        self, version: int, *, project: str | None = None, experiment: str | None = None,
    ) -> SummaryVersionOut:
        """`Client.get_summary_version` as a `SummaryVersionOut`."""
        return self._to_model(
            SummaryVersionOut,
            self._client.get_summary_version(version, project=project, experiment=experiment),
        )

    def get_visuals_options(
        self, *, project: str | None = None, experiment: str | None = None,
    ) -> VisualsOptionsOut:
        """`Client.get_visuals_options` as a `VisualsOptionsOut`."""
        return self._to_model(
            VisualsOptionsOut,
            self._client.get_visuals_options(project=project, experiment=experiment),
        )

from probe.sdk.client.server_features import _route_absent  # noqa: E402 -- pieces need each other; the front door loads this one first

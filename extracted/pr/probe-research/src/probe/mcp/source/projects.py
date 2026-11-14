"""project, experiment and workspace reads: files, branches and best picks, papers, code, README, groups, versions."""

from __future__ import annotations

import logging
from typing import Any

from ...sdk import errors
from ...sdk.artifact.anchors import Anchor
from probe.mcp.source.people import PeopleFilters, read_owner_headers, read_query_note_header


class ProjectReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def experiment_artifacts(self, experiment_id: str) -> list[dict]:
        return self.client.list_experiment_artifacts(experiment_id)

    def experiment_inherited(
        self,
        experiment_id: str,
        *,
        runs: bool,
        after: str | None,
        limit: int,
        project_id: str | None = None,
    ) -> dict:
        """One page of what a fork reads live from its source
        (``GET /v1/projects/{P}/experiments/{E}/inherited``): its sources and
        their run files, or with ``runs`` the runs."""
        return self.client.experiment_inherited(
            experiment_id, runs=runs, after=after, limit=limit, project_id=project_id
        )

    def project_branches(self, project_id: str) -> dict:
        """``GET /v1/projects/{P}/branches``: the project tree's lines of work."""
        return self.client.project_branches(project_id)

    def experiment_branch(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/branch``: its line of work and
        the ones it split from."""
        return self.client.experiment_branch(experiment_id, project_id=project_id)

    def workspace_branches(self, workspace_id: str) -> dict:
        """``GET /v1/workspaces/{W}/branches``: the workspace's lines of work."""
        return self.client.workspace_branches(workspace_id)

    def project_best(self, project_id: str, *, history: int) -> dict:
        """``GET /v1/projects/{P}/best?history=N``: the pick and its events,
        newest first (#3624)."""
        return self.client.get_project_best(project_id, history=history)

    def workspace_best(self, workspace_id: str, *, history: int) -> dict:
        """``GET /v1/workspaces/{W}/best?history=N``: as :meth:`project_best`."""
        return self.client.get_workspace_best(workspace_id, history=history)

    def project_artifacts(self, project_id: str) -> list[dict]:
        return self.client.list_project_artifacts(project_id)

    def fetch_panes(self, project_id: str) -> dict:
        """``GET /v1/projects/{P}/panes``: ``{panes, preview}``, the project's or experiment's panes first to
        last (each with its HTML) and a project's canvas preview (None for an experiment)."""
        return self.client.read_pane_list(project_id)

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

    def artifact_versions(self, artifact_id: str) -> list[dict]:
        """The artifact's version chain, newest first — what the reuse check reads
        once :meth:`artifact_by_name` has turned a name into an identity."""
        return self.client.list_artifact_versions(artifact_id)

    def intent(self, kind: str, entity_id: str) -> dict | None:
        """``GET /v1/intent/{kind}/{id}``: the researcher's ask behind a run,
        experiment or project, quoted from the session that created it, or None.

        Best effort, never a reason a card fails: a 404 (no ask known), an
        older server without the route, or any transport error reads as no
        intent. NOT A PURE READ, as `project_readme` is not: a miss is resolved
        on the server from the session's trajectory and cached."""
        try:
            found = self.client.transport.get(f"/v1/intent/{kind}/{entity_id}")
        except errors.NotFoundError:
            return None
        except Exception as exc:  # noqa: BLE001 -- a card never fails on this field
            logging.getLogger("probe.mcp.source").debug("intent read failed: %s", type(exc).__name__)
            return None
        return found if isinstance(found, dict) else None

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

    # -- flat listings (browse modes other than `projects`) ------------------------

    def workspaces(self) -> list[dict]:
        """``GET /v1/workspaces``: every workspace, whole and in server order
        (creation is capped tenant-wide, so the route does not page)."""
        return self.client.list_workspaces()

    def files(
        self,
        *,
        workspace_id: str | None = None,
        prefix: str | None = None,
        limit: int,
        filters: PeopleFilters = PeopleFilters(),
        query: str | None = None,
    ) -> Any:
        """The team's Shared folder (``GET /v1/shared/files``) or one workspace's
        files (``GET /v1/workspaces/{id}/files``), name-ordered (`order="recent"`: newest first;
        `query`: the loose name match, best first). Neither route takes a cursor; ``prefix`` is a
        FOLDER filter. A list of rows, or with `filters` or `query` the route's
        `{items, owner_matched?, unowned_count?, query_note?}`."""
        parameters: dict[str, Any] = {"limit": limit, **filters.to_query()}
        if prefix:
            parameters["prefix"] = prefix
        if query:
            parameters["query"] = query
        if filters.is_set or query:
            # The body stays a bare list; who `owner` matched rides the response headers.
            path = f"/v1/workspaces/{workspace_id}/files" if workspace_id is not None else "/v1/shared/files"
            response = self.client.transport.request("GET", path, params=parameters, idempotent=True)
            return {
                "items": response.json() or [],
                **read_owner_headers(response.headers),
                **read_query_note_header(response.headers),
            }
        if workspace_id is not None:
            return self.client.list_anchored(Anchor.WORKSPACE, workspace_id, **parameters) or []
        return self.client.list_anchored(Anchor.SHARED, **parameters) or []

    def experiment_groups(self, experiment_id: str) -> list[dict]:
        return self.client.list_groups(experiment_id)

    def experiment_versions(self, experiment_id: str) -> list[dict]:
        return self.client.list_experiment_versions(experiment_id)

    def experiment_reproduce(self, experiment_id: str, *, version: int | None = None) -> dict:
        """Per-run reproduction summaries across an experiment; ``version`` pins
        against a minted manifest. Passthrough to research-os /reproduce."""
        return self.client.experiment_reproduce(experiment_id, version=version)

"""HeadlinesMixin, Client's methods: headline metric and best-run picks for a project, experiment
or workspace (twins: app/projects, app/projects/workspaces)."""

from __future__ import annotations
from typing import Any


class HeadlinesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- the declared headline metric and the best pick ------------------------
    #
    # Declarations with a history of who said so, never computed. Who wrote one
    # comes from the credential: every token -- this client's included -- is an
    # AGENT, a dashboard login a PERSON. An agent over a person's metric is 409
    # `METRIC_IS_A_PERSONS`, over a person's current pick 409 `PICK_IS_A_PERSONS`
    # (`ConflictError.detail` names who picked what and when). There is no
    # override: the person changes theirs from the dashboard.

    def get_project_metric(self, project_id: str) -> dict:
        """The headline metric a project resolves to (its own, else the nearest
        ancestor's): ``{anchor, metric | null, cleared_here}``."""
        return self.transport.get(f"/v1/projects/{project_id}/metric")

    def set_project_metric(
        self, project_id: str, key: str, *, goal: str, reduce: str | None = None
    ) -> dict:
        """Declare the metric that ranks a project's work: ``key`` as runs log it
        (``test/acc``), ``goal`` ``max`` or ``min`` (never inferred), ``reduce``
        ``final`` (the server's default: a run's final value) or ``best`` (its
        series' extreme along ``goal``). Its experiments inherit
        it. ``project_id`` is the project's uuid (writes take uuids)."""
        body: dict[str, Any] = {"key": key, "goal": goal}
        if reduce is not None:
            body["reduce"] = reduce
        return self.transport.put(f"/v1/projects/{project_id}/metric", body)

    def clear_project_metric(self, project_id: str) -> dict:
        """Clear a project's own metric, so it inherits its parent's again."""
        return self.transport.delete(f"/v1/projects/{project_id}/metric")

    def get_experiment_metric(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """The headline metric an experiment resolves to: its own override, else
        its project's, else the nearest ancestor's."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/metric"),
            experiment_id,
            project_id,
        )

    def set_experiment_metric(
        self,
        experiment_id: str,
        key: str,
        *,
        goal: str,
        reduce: str | None = None,
        project_id: str | None = None,
    ) -> dict:
        """Override one experiment's headline metric (the arguments of
        :meth:`set_project_metric`)."""
        body: dict[str, Any] = {"key": key, "goal": goal}
        if reduce is not None:
            body["reduce"] = reduce
        return self._on_experiment(
            lambda p, e: self.transport.put(f"/v1/projects/{p}/experiments/{e}/metric", body),
            experiment_id,
            project_id,
        )

    def clear_experiment_metric(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """Clear an experiment's override, so it inherits its project's again."""
        return self._on_experiment(
            lambda p, e: self.transport.delete(f"/v1/projects/{p}/experiments/{e}/metric"),
            experiment_id,
            project_id,
        )

    def get_project_best(self, project_id: str, *, history: int | None = None) -> dict:
        """A project's current best pick and its events, newest first:
        ``{scope, pick | null, history}`` (``history`` events read, at most 50)."""
        params = {"history": history} if history is not None else None
        return self.transport.get(f"/v1/projects/{project_id}/best", params=params)

    def pick_project_best(
        self, project_id: str, experiment_id: str, *, reason: str | None = None
    ) -> dict:
        """Pick an experiment of the project's tree as its best. ``reason`` (one
        or two sentences) is required from an agent, so from every token. Both
        ids are uuids."""
        body: dict[str, Any] = {"experiment_id": str(experiment_id)}
        if reason is not None:
            body["reason"] = reason
        return self.transport.post(f"/v1/projects/{project_id}/best", body)

    def clear_project_best(self, project_id: str, *, reason: str | None = None) -> dict:
        """Clear a project's pick. History is never replayed: after a clear the
        project has no pick until the next one."""
        params = {"reason": reason} if reason else None
        return self.transport.request(
            "DELETE", f"/v1/projects/{project_id}/best", params=params, idempotent=True
        ).json()

    def get_workspace_best(self, workspace_id: str, *, history: int | None = None) -> dict:
        """A workspace's current best pick and its events (as :meth:`get_project_best`)."""
        params = {"history": history} if history is not None else None
        return self.transport.get(f"/v1/workspaces/{workspace_id}/best", params=params)

    def pick_workspace_best(
        self, workspace_id: str, experiment_id: str, *, reason: str | None = None
    ) -> dict:
        """Pick an experiment of the workspace's projects as its best (the rules
        of :meth:`pick_project_best`)."""
        body: dict[str, Any] = {"experiment_id": str(experiment_id)}
        if reason is not None:
            body["reason"] = reason
        return self.transport.post(f"/v1/workspaces/{workspace_id}/best", body)

    def clear_workspace_best(self, workspace_id: str, *, reason: str | None = None) -> dict:
        """Clear a workspace's pick."""
        params = {"reason": reason} if reason else None
        return self.transport.request(
            "DELETE", f"/v1/workspaces/{workspace_id}/best", params=params, idempotent=True
        ).json()

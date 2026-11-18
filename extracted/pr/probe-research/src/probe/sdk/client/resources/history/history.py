"""VersionsResource (client.versions, typed reads) and VersionsMixin, Client's methods: the saved versions of a
notes document (a project's, an experiment's, a run's, a sub-note's) and of an Overview page (twins:
app/projects/notes, app/projects/experiments/versions, app/generation/overviews)."""

from __future__ import annotations

from typing import Any

from .....generated.models import NoteVersionsOut, OverviewVersionOut, OverviewVersionsOut
from ...resource import Resource


def _build_page_query(before: int | None, limit: int | None) -> dict[str, Any] | None:
    """`before` (a version number) and `limit`, without the unset one."""
    return {key: value for key, value in {"before": before, "limit": limit}.items() if value is not None} or None


class VersionsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- notes history -------------------------------------------------------
    def list_project_note_versions(self, project_id: str, *, before: int | None = None, limit: int | None = None) -> dict:
        """``GET /v1/projects/{id}/notes/versions``: a project's notes versions, newest first."""
        return self.transport.get(f"/v1/projects/{project_id}/notes/versions", params=_build_page_query(before, limit))

    def get_project_note_version(self, project_id: str, version: int) -> dict:
        """``GET /v1/projects/{id}/notes/versions/{n}``: one saved version of a project's notes."""
        return self.transport.get(f"/v1/projects/{project_id}/notes/versions/{version}")

    def list_experiment_note_versions(
        self, experiment_id: str, *, project_id: str | None = None, before: int | None = None, limit: int | None = None
    ) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/notes/versions``: an experiment's notes versions, newest first."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/notes/versions",
                                            params=_build_page_query(before, limit)),
            experiment_id,
            project_id,
        )

    def get_experiment_note_version(self, experiment_id: str, version: int, *, project_id: str | None = None) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/notes/versions/{n}``: one saved version of an experiment's notes."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/notes/versions/{version}"),
            experiment_id,
            project_id,
        )

    def list_run_note_versions(self, run_id: str, *, before: int | None = None, limit: int | None = None) -> dict:
        """``GET /v1/runs/{id}/notes/versions``: a run's notes versions, newest first."""
        return self.transport.get(f"/v1/runs/{run_id}/notes/versions", params=_build_page_query(before, limit))

    def get_run_note_version(self, run_id: str, version: int) -> dict:
        """``GET /v1/runs/{id}/notes/versions/{n}``: one saved version of a run's notes."""
        return self.transport.get(f"/v1/runs/{run_id}/notes/versions/{version}")

    def list_sub_note_versions(self, sub_note_id: str, *, before: int | None = None, limit: int | None = None) -> dict:
        """``GET /v1/sub-notes/{id}/versions``: a sub-note's versions, newest first."""
        return self.transport.get(f"/v1/sub-notes/{sub_note_id}/versions", params=_build_page_query(before, limit))

    def get_sub_note_version(self, sub_note_id: str, version: int) -> dict:
        """``GET /v1/sub-notes/{id}/versions/{n}``: one saved version of a sub-note."""
        return self.transport.get(f"/v1/sub-notes/{sub_note_id}/versions/{version}")

    # -- Overview page history -----------------------------------------------
    def list_project_overview_versions(
        self, project_id: str, *, before: int | None = None, limit: int | None = None
    ) -> dict:
        """``GET /v1/projects/{id}/overview/versions``: a project's Overview page versions, newest first."""
        return self.transport.get(f"/v1/projects/{project_id}/overview/versions", params=_build_page_query(before, limit))

    def get_project_overview_version(self, project_id: str, version: int) -> dict:
        """``GET /v1/projects/{id}/overview/versions/{n}``: one saved version of a project's Overview page."""
        return self.transport.get(f"/v1/projects/{project_id}/overview/versions/{version}")

    def list_experiment_overview_versions(
        self, experiment_id: str, *, project_id: str | None = None, before: int | None = None, limit: int | None = None
    ) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/overview/versions``: an experiment's Overview page versions."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/overview/versions",
                                            params=_build_page_query(before, limit)),
            experiment_id,
            project_id,
        )

    def get_experiment_overview_version(
        self, experiment_id: str, version: int, *, project_id: str | None = None
    ) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/overview/versions/{n}``: one saved experiment Overview page."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/overview/versions/{version}"),
            experiment_id,
            project_id,
        )


class VersionsResource(Resource):
    """`client.versions`: typed history reads. One saved notes version is a plain dict (the server names no model)."""

    __slots__ = ()

    def list_project_notes(self, project_id: str, *, before: int | None = None, limit: int | None = None) -> NoteVersionsOut:
        """`Client.list_project_note_versions` as a `NoteVersionsOut`."""
        return self._to_model(NoteVersionsOut, self._client.list_project_note_versions(project_id, before=before, limit=limit))

    def list_experiment_notes(
        self, experiment_id: str, *, project_id: str | None = None, before: int | None = None, limit: int | None = None
    ) -> NoteVersionsOut:
        """`Client.list_experiment_note_versions` as a `NoteVersionsOut`."""
        return self._to_model(NoteVersionsOut, self._client.list_experiment_note_versions(
            experiment_id, project_id=project_id, before=before, limit=limit))

    def list_run_notes(self, run_id: str, *, before: int | None = None, limit: int | None = None) -> NoteVersionsOut:
        """`Client.list_run_note_versions` as a `NoteVersionsOut`."""
        return self._to_model(NoteVersionsOut, self._client.list_run_note_versions(run_id, before=before, limit=limit))

    def list_sub_note(self, sub_note_id: str, *, before: int | None = None, limit: int | None = None) -> NoteVersionsOut:
        """`Client.list_sub_note_versions` as a `NoteVersionsOut`."""
        return self._to_model(NoteVersionsOut, self._client.list_sub_note_versions(sub_note_id, before=before, limit=limit))

    def list_project_overview(
        self, project_id: str, *, before: int | None = None, limit: int | None = None
    ) -> OverviewVersionsOut:
        """`Client.list_project_overview_versions` as an `OverviewVersionsOut`."""
        return self._to_model(OverviewVersionsOut, self._client.list_project_overview_versions(
            project_id, before=before, limit=limit))

    def get_project_overview(self, project_id: str, version: int) -> OverviewVersionOut:
        """`Client.get_project_overview_version` as an `OverviewVersionOut`."""
        return self._to_model(OverviewVersionOut, self._client.get_project_overview_version(project_id, version))

    def list_experiment_overview(
        self, experiment_id: str, *, project_id: str | None = None, before: int | None = None, limit: int | None = None
    ) -> OverviewVersionsOut:
        """`Client.list_experiment_overview_versions` as an `OverviewVersionsOut`."""
        return self._to_model(OverviewVersionsOut, self._client.list_experiment_overview_versions(
            experiment_id, project_id=project_id, before=before, limit=limit))

    def get_experiment_overview(
        self, experiment_id: str, version: int, *, project_id: str | None = None
    ) -> OverviewVersionOut:
        """`Client.get_experiment_overview_version` as an `OverviewVersionOut`."""
        return self._to_model(OverviewVersionOut, self._client.get_experiment_overview_version(
            experiment_id, version, project_id=project_id))

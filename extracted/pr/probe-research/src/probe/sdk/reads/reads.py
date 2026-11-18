"""`probe.Reader`: DEPRECATED. A thin wrapper over `probe.Client`, kept one minor release for code written
against it (api-access D8, TODO-1). `probe.Client(service_token=...)` reads everything a team API key can.

    import probe

    client = probe.Client()                       # PROBE_SERVICE_TOKEN (+ PROBE_BASE_URL)
    points = client.run_metrics(run_id, key="reward", labels={"sample": 5})
    blob = client.fetch_artifact(artifact_id)

Each Reader method calls the matching Client method (the table in `service-token-sdk.md`) and the first call
warns once (`DeprecationWarning`).
"""

from __future__ import annotations

import threading
import warnings
from typing import Any

from .. import errors
from ..client.client import Client
from ..client import Reference
from ..delivery.transport.transport import Transport
from ..settings.settings import resolve

__all__ = ["Reader", "Reference"]

_warned = threading.Event()


def _warn_deprecated() -> None:
    """One DeprecationWarning per process, at the first Reader call."""
    if _warned.is_set():
        return
    _warned.set()
    warnings.warn(
        "probe.Reader is deprecated and goes in a future release: use probe.Client() (it reads with "
        "PROBE_SERVICE_TOKEN too); every Reader method has a Client method of the same job",
        DeprecationWarning,
        stacklevel=3,
    )


class Reader:
    """Deprecated read client for a team API key: every method calls the matching `probe.Client` method.

    Construct with :meth:`from_env` (or pass a prepared :class:`Transport`). Use as a context manager to close
    the underlying HTTP client."""

    def __init__(self, transport: Transport):
        self._client = Client(settings=transport.settings, transport=transport, async_writes=False, auto_drain=False)

    @classmethod
    def from_env(cls, *, base_url: str | None = None, service_token: str | None = None) -> Reader:
        """A Reader from ``PROBE_SERVICE_TOKEN`` + ``PROBE_BASE_URL`` (or the arguments). Never falls back to
        ``PROBE_TOKEN``: it reads with the team key alone."""
        settings = resolve(base_url=base_url, service_token=service_token)
        if not settings.service_token:
            raise errors.AuthError("no service token configured (set PROBE_SERVICE_TOKEN or pass service_token=)")
        settings.token = None
        settings.credential_conflict = None
        settings.should_use_service_token = True
        return cls(Transport(settings))

    @property
    def client(self) -> Client:
        """The `probe.Client` this Reader calls: move code to it."""
        return self._client

    def close(self) -> None:
        self._client.transport.close()

    def __enter__(self) -> Reader:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- enumeration --------------------------------------------------------
    def projects(self, *, workspace_id=None, slug=None, tags=None) -> list[dict]:
        _warn_deprecated()
        return list(self._client.iter_projects(workspace_id=workspace_id, slug=slug, tags=tags))

    def project(self, project_id: str) -> dict:
        _warn_deprecated()
        return self._client.get_project(project_id)

    def experiments(self, *, project_id=None, slug=None, tags=None) -> list[dict]:
        """One project's experiments, or every project's; ``slug`` names at most one. ``tags`` is refused
        (an experiment's tags are read-only since it moved to its own record)."""
        _warn_deprecated()
        if tags:
            raise ValueError(
                "experiments have no tags to filter by any more: they are kept "
                "read-only since an experiment moved to its own record"
            )
        if slug is not None:
            try:
                return [self._client.get_experiment(slug, project_id=project_id)]
            except errors.NotFoundError:
                return []
        return list(self._client.iter_experiments(project_id=project_id))

    def experiment(self, experiment_id: str) -> dict:
        _warn_deprecated()
        return self._client.get_experiment(experiment_id)

    def runs(self, *, experiment_id=None, project_id=None, status=None, tags=None) -> list[dict]:
        _warn_deprecated()
        return list(self._client.iter_runs(experiment_id=experiment_id, project_id=project_id, status=status, tags=tags))

    def run(self, ref: str) -> dict:
        _warn_deprecated()
        return self._client.get_run(ref)

    def browse(self, *, scope=None, depth=1, status=None, tags=None) -> dict:
        _warn_deprecated()
        return self._client.browse(scope=scope, depth=depth, status=status, tags=tags)

    def groups(self, experiment_id: str) -> list[dict]:
        _warn_deprecated()
        return self._client.list_groups(experiment_id)

    def group(self, group_id: str) -> dict:
        _warn_deprecated()
        return self._client.get_group(group_id)

    # -- metrics ------------------------------------------------------------
    def metrics(self, run: str, *, key=None, kind=None, dimensions=None, labels=None, span_id=None,
                step_from=None, step_to=None, limit=None) -> list[dict]:
        _warn_deprecated()
        return self._client.run_metrics(run, key=key, kind=kind, dimensions=dimensions, labels=labels,
                                        span_id=span_id, step_from=step_from, step_to=step_to, limit=limit)

    def metrics_grouped(self, run: str, key: str, *, by=None, where=None, agg=None, kind=None, step_bucket=None,
                        step_from=None, step_to=None) -> dict:
        _warn_deprecated()
        if isinstance(by, str):
            by = [part for part in by.split(",") if part]
        return self._client.get_metrics_grouped(run, key, by=by, where=where, agg=agg, kind=kind,
                                                step_bucket=step_bucket, step_from=step_from, step_to=step_to)

    def metrics_wide(self, run: str, *, key=None, kind=None, step_from=None, step_to=None) -> dict:
        _warn_deprecated()
        keys = [key] if isinstance(key, str) else key
        return self._client.get_metrics_wide(run, key=keys, kind=kind, step_from=step_from, step_to=step_to)

    def series(self, run: str) -> list[dict]:
        _warn_deprecated()
        return self._client.run_series(run)

    def series_query(self, run_ids: list[str], **body: Any) -> dict:
        _warn_deprecated()
        return self._client.query_series(run_ids, **body)

    def coordinates(self, run: str) -> list[dict]:
        _warn_deprecated()
        return self._client.list_run_coordinates(run)

    # -- run detail ---------------------------------------------------------
    def bundle(self, run: str) -> dict:
        _warn_deprecated()
        return self._client.run_bundle(run)

    def lineage(self, run: str) -> dict:
        _warn_deprecated()
        return self._client.run_lineage(run)

    # -- artifacts ----------------------------------------------------------
    def artifacts(self, run: str, *, kind=None, prefix=None) -> list[dict]:
        _warn_deprecated()
        return self._client.list_run_artifacts(run, kind=kind, prefix=prefix)

    def download_url(self, artifact_id: str) -> str | Reference:
        _warn_deprecated()
        return self._client.get_artifact_download_target(artifact_id)

    def download_artifact(self, artifact_id: str, *, dest: str | None = None, mode: str = "auto") -> bytes | dict | Reference:
        _warn_deprecated()
        return self._client.fetch_artifact(artifact_id, dest=dest, mode=mode)

    def preview(self, artifact_id: str) -> bytes:
        _warn_deprecated()
        return self._client.get_artifact_preview(artifact_id)

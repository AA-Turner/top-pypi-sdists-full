"""Which deployment a DAG file belongs to — production, or one branch of it.

CI writes a `_databaas_target.json` into every deployed bundle. This module
resolves that file **from the DAG file using it**, not from its own location,
which is what lets one shared copy serve every bundle correctly.

That matters because `DataBaasS3DagBundle` registers every bundle directory on
one process-wide `sys.path` and the dag-processor parses all bundles in one
process. Two bundles each shipping their own `databaas_target.py` compete for a
single global module name: a dev bundle's copy could win the import for a *prod*
DAG file, registering it as `dev_<slug>_<name>`. The real prod dag id was then
never produced, Airflow marked it stale, and it vanished from the DAG list while
its running DagRuns stayed visible.

Shipping here — in site-packages, via a pinned wheel — is safer than the
previous `/opt/databaas` placement rather than riskier, because
`_register_sys_path_recursive` *appends* bundle directories. site-packages
precedes every appended entry, so no bundle can shadow this module. Do not
change that append back to `insert(0)`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_CONFIG_NAME = "_databaas_target.json"
# DAG files normally sit in the bundle root next to the config. A few levels
# covers repos that nest them; the walk stops well short of escaping into
# another bundle, since the parent dirs hold no config.
_MAX_PARENTS = 10

_cache: dict[Path, DeploymentTarget] = {}


class DeploymentTarget:
    """One deployment's identity, as CI recorded it.

    Attributes:
        mode: ``"production"`` or a development mode.
        dev_key: The branch key for a development deployment.
        bundle: The bundle name.
        paused: Whether DAGs from this deployment should start paused.
        source_repo: Repository the bundle was deployed from.
        source_ref: Git ref it was deployed from.
        source_commit: Commit SHA.
        source_run_url: URL of the CI run that deployed it.
        deployed_at: Deployment timestamp.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Build from the parsed ``_databaas_target.json``."""
        self.mode = data["mode"]
        self.dev_key = data.get("dev_key", "")
        self.bundle = data["bundle"]
        self.paused = self.mode != "production"
        self.source_repo = data.get("repo", "")
        self.source_ref = data.get("ref", "")
        self.source_commit = data.get("commit", "")
        self.source_run_url = data.get("run_url", "")
        self.deployed_at = data.get("deployed_at", "")

    @property
    def is_production(self) -> bool:
        """Whether this is the production deployment."""
        return self.mode == "production"

    def dag_id(self, name: str) -> str:
        """``name`` in production, ``dev_<dev_key>_<name>`` otherwise."""
        return name if self.is_production else f"dev_{self.dev_key}_{name}"

    def tags(self, *tags: str) -> list[str]:
        """``tags`` plus ``dev:<dev_key>`` on a development deployment."""
        result = list(tags)
        if not self.is_production:
            result.append(f"dev:{self.dev_key}")
        return result

    def doc_suffix(self) -> str:
        """Markdown "Deployed from" footer for ``doc_md``; empty if unknown."""
        if not self.source_repo:
            return ""
        short_sha = self.source_commit[:8]
        return (
            f"\n\n---\n**Deployed from:** `{self.source_repo}@{self.source_ref}` "
            f"(`{short_sha}`) · [CI run]({self.source_run_url}) · {self.deployed_at}"
        )


def _find_config(start: Path) -> Path:
    for candidate in (start, *list(start.parents)[:_MAX_PARENTS]):
        path = candidate / _CONFIG_NAME
        if path.is_file():
            return path
    raise RuntimeError(
        f"{_CONFIG_NAME} not found in {start} or its parents. CI writes it into "
        "every deployed bundle; a DAG file outside a deployed bundle cannot "
        "resolve its deployment target."
    )


def target_for(caller_file: str | None) -> DeploymentTarget:
    """Resolve the deployment target for a DAG file.

    Call as `target_for(__file__)` from the DAG itself. Library code must pass
    the DAG's path through explicitly — resolving it from a library module's
    own location is the bug this signature exists to make impossible.

    Args:
        caller_file: The DAG file's ``__file__``.

    Raises:
        RuntimeError: If ``caller_file`` is empty or no
            ``_databaas_target.json`` is found in its directory or parents.

    Example:
        >>> from databaas_utils.airflow import target_for
        >>> t = target_for(__file__)
        >>> with DAG(t.dag_id("daily_summary"), tags=t.tags("weather")): ...
    """
    if not caller_file:
        raise RuntimeError(
            "databaas_utils could not determine the calling DAG file: the caller "
            "has no __file__. Use target_for(__file__) explicitly."
        )
    directory = Path(caller_file).resolve().parent
    cached = _cache.get(directory)
    if cached is None:
        cached = DeploymentTarget(json.loads(_find_config(directory).read_text()))
        _cache[directory] = cached
    return cached


class _CallerScopedTarget:
    """Resolves per calling DAG file so one shared module serves every bundle.

    Resolution happens on *attribute access*, not on import, so the caller's
    frame is the DAG file itself. That keeps `from databaas_target import target`
    working unchanged in DAGs that already use it.
    """

    def __getattr__(self, name: str) -> Any:
        # Never resolve for dunder probes (hasattr, copy, pickle): those must
        # raise AttributeError, not a config-missing error.
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(target_for(sys._getframe(1).f_globals.get("__file__")), name)


target = _CallerScopedTarget()

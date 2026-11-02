"""Naming a thing per deployment, so a branch run cannot write production data.

CI prefixes dev dag_ids so two deployments coexist in one Airflow. That is not
enough on its own: without scoping the *data* too, a branch run writes the
production tables and moves the production cursor.

This module is deliberately Airflow-free and knows nothing about
`databaas_target`. The dependency runs the other way — `databaas_utils.airflow.
scoping` resolves the slug from the calling DAG file and passes it in. That
inversion is what lets this code live in site-packages at all: the prior art
called `databaas_target` from library code, and its caller-frame lookup then
resolved against the library's own directory rather than the DAG's.
"""

from __future__ import annotations

import logging
import os
import re
from collections.abc import Mapping
from typing import Final

log = logging.getLogger(__name__)

SLUG_ENV_VAR: Final = "DATABAAS_DEPLOY_SLUG"

_UNSAFE = re.compile(r"[^a-z0-9]+")
_default_slug: dict[str, str | None] = {"value": None}


class _Unset:
    """Distinguishes "not supplied" from an explicit None (meaning production)."""


UNSET: Final = _Unset()


def normalise(key: str) -> str:
    """Lower-case `key` and squash anything unsafe to single underscores.

    >>> normalise("Feature/Add-Login")
    'feature_add_login'
    """
    return _UNSAFE.sub("_", (key or "").lower()).strip("_")


def set_default_slug(value: str | None) -> None:
    """Set the process-wide slug.

    For containers and notebooks, where there is one deployment per process by
    construction. **Not** for Airflow: the dag-processor parses production and
    dev bundles in one process, so a process-wide slug would leak a branch's
    suffix into production table names — the data-layer twin of the dag-id
    incident that `databaas_target` exists to prevent.

    Args:
        value: The slug, or ``None`` to mean production.
    """
    _default_slug["value"] = normalise(value) or None if value else None


def _current_slug(
    *, override: str | _Unset | None = UNSET, env: Mapping[str, str] | None = None
) -> str | None:
    """The slug for this deployment, or None for production.

    Resolution order: explicit override, then `set_default_slug`, then
    ``DATABAAS_DEPLOY_SLUG`` in the environment.

    Exported as ``slug``.
    """
    if not isinstance(override, _Unset):
        return normalise(override) or None if override else None
    if _default_slug["value"] is not None:
        return _default_slug["value"]
    source = env if env is not None else os.environ
    return normalise(source.get(SLUG_ENV_VAR, "")) or None


slug = _current_slug


def scoped(name: str, *, slug: str | _Unset | None = UNSET) -> str:
    """`name` in production, `name_dev_<slug>` on a branch deployment.

    Suffixed rather than prefixed so the production name stays the sort-order
    prefix of its branches, and so a bare `name` is always the real one.

    In a DAG use ``databaas_utils.airflow.scoped``, which finds the slug from
    the deployment for you.

    Args:
        name: The production name, e.g. a table or namespace.
        slug: Override the slug; ``None`` forces the production name.

    Example:
        >>> set_default_slug("add-login")
        >>> scoped("daily_summary")
        'daily_summary_dev_add_login'
    """
    branch = _current_slug(override=slug)
    return name if branch is None else f"{name}_dev_{branch}"

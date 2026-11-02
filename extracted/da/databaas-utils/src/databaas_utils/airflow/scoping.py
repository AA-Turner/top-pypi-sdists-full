"""Deployment-scoped names, resolved from the calling DAG file.

The rule this module encodes: **the caller-frame trick is only sound in a
function called directly from the DAG file.** `sys._getframe(1)` inside
`scoped()` gives the DAG; inside a helper that `scoped()` calls, it gives the
helper. Every public function here therefore takes a `caller_file=` override so
a wrapper can pass `__file__` through instead of silently resolving itself.

The prior art violated this: `lakehouse_core.deploy.slug()` read
`databaas_target.target.mode`, so the lookup resolved against `deploy.py`'s own
directory. It worked only because `deploy.py` shipped inside the bundle, where
the parent walk still found the bundle's config. From site-packages the same
call raises at DAG parse time, in production.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from databaas_utils.scoping import normalise
from databaas_utils.scoping import scoped as _core_scoped

log = logging.getLogger(__name__)

# This package's own directory. A caller frame resolving to somewhere inside it
# means library code reached these functions without passing the DAG's path.
_PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def _caller_file(explicit: str | None, depth: int) -> str | None:
    if explicit:
        return explicit
    resolved = sys._getframe(depth).f_globals.get("__file__")
    if resolved and _is_inside_package(resolved):
        raise RuntimeError(
            f"{Path(resolved).name} called a deployment-scoping helper without "
            "passing caller_file. sys._getframe resolves to the calling module, "
            "so library code must forward the DAG's path explicitly:\n"
            "    scoped(name, caller_file=__file__)\n"
            "Resolving from inside the installed package would find no bundle "
            "config and silently return PRODUCTION names for a dev deployment."
        )
    return resolved


def _is_inside_package(path: str) -> bool:
    try:
        return _PACKAGE_ROOT in Path(path).resolve().parents
    except OSError:  # pragma: no cover - unresolvable paths are not ours
        return False


def current_slug(*, caller_file: str | None = None) -> str | None:
    """The branch slug for the calling DAG file; None in production.

    MUST be called directly from the DAG file, or given `caller_file=__file__`.

    Args:
        caller_file: The DAG file's ``__file__``, if calling from a helper.
    """
    from databaas_utils.airflow.target import target_for

    resolved = _caller_file(caller_file, 2)
    try:
        deployment = target_for(resolved)
    except RuntimeError:
        # No config: a local checkout, not a deployed bundle. Reads as "not a
        # deployment", which is production-shaped — the same as the prior art.
        return None

    if deployment.is_production:
        return None
    key = normalise(deployment.dev_key)
    if not key:
        log.warning("non-production deployment with no dev_key — not scoping data")
        return None
    return key


def scoped(name: str, *, caller_file: str | None = None) -> str:
    """`name` in production, `name_dev_<slug>` on a branch deployment.

    MUST be called directly from the DAG file, or given `caller_file=__file__`.

    Args:
        name: The production name, e.g. a table or namespace.
        caller_file: The DAG file's ``__file__``, if calling from a helper.

    Example:
        >>> table = scoped("daily_summary")  # in a DAG file
        'daily_summary_dev_add_login'
    """
    resolved = _caller_file(caller_file, 2)
    return _core_scoped(name, slug=current_slug(caller_file=resolved))

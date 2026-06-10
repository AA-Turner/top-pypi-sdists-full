import contextlib
import typing as t

from taktile_auth.recursion import RecursionMode
from taktile_auth.settings import settings


@contextlib.contextmanager
def override_recursion_settings(
    *,
    mode: t.Optional[RecursionMode] = None,
    warn_weight: t.Optional[int] = None,
    abort_weight: t.Optional[int] = None,
    ttl_seconds: t.Optional[int] = None,
) -> t.Iterator[None]:
    """Temporarily override ``taktile_auth.settings.RECURSION_*`` values.
    Used by tests that need non-default thresholds."""
    overrides: t.Dict[str, t.Any] = {}
    if mode is not None:
        overrides["RECURSION_MODE"] = mode
    if warn_weight is not None:
        overrides["RECURSION_WARN_WEIGHT"] = warn_weight
    if abort_weight is not None:
        overrides["RECURSION_ABORT_WEIGHT"] = abort_weight
    if ttl_seconds is not None:
        overrides["RECURSION_TTL_SECONDS"] = ttl_seconds

    previous = {key: settings._settings[key] for key in overrides}
    settings._settings.update(overrides)
    try:
        yield
    finally:
        settings._settings.update(previous)

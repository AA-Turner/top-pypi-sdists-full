"""Gated ``/proc/sys/vm/drop_caches`` escape hatch.

The codebase's normal teardown paths should release GPU-driver pages on their
own. This helper exists so an operations runbook can opt in to the kernel-level
fallback (``echo 3 > /proc/sys/vm/drop_caches``) without us shipping it as a
default behaviour. It is intentionally restrictive:

* Refuses unless the env var is set (default ``MATRICE_ALLOW_DROP_CACHES``).
* Refuses unless the process is root (effective uid == 0).
* Logs every invocation at WARNING.

Not called from any normal code path. Production services should never invoke
this implicitly.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_DROP_CACHES_PATH = "/proc/sys/vm/drop_caches"
DEFAULT_ENV_GATE = "MATRICE_ALLOW_DROP_CACHES"


def drop_caches(
    level: int = 3,
    *,
    require_env: Optional[str] = DEFAULT_ENV_GATE,
) -> bool:
    """Write ``level`` to ``/proc/sys/vm/drop_caches`` if gates allow.

    Returns ``True`` if the write succeeded, ``False`` otherwise. Never raises.

    level:
        1 = pagecache, 2 = dentries+inodes, 3 = both (default).
    require_env:
        Name of the env var that must be set to a truthy value. Pass ``None``
        to skip the env gate (only do this from tests or explicit ops tools).
    """
    if level not in (1, 2, 3):
        logger.warning("drop_caches: refusing invalid level %r", level)
        return False
    if require_env is not None:
        value = os.environ.get(require_env, "")
        if value.lower() in ("", "0", "false", "no", "off"):
            logger.warning(
                "drop_caches: refusing — env %s not set to a truthy value",
                require_env,
            )
            return False
    if os.geteuid() != 0:
        logger.warning("drop_caches: refusing — process is not root")
        return False
    try:
        # sync first so dirty pages get written before the kernel drops cache.
        os.sync()
        with open(_DROP_CACHES_PATH, "w", encoding="ascii") as f:
            f.write(f"{level}\n")
    except OSError:
        logger.warning("drop_caches: write failed", exc_info=True)
        return False
    logger.warning("drop_caches: wrote level=%d to %s", level, _DROP_CACHES_PATH)
    return True

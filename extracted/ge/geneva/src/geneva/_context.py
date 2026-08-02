# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import logging
from contextvars import ContextVar
from typing import TYPE_CHECKING, ClassVar, Literal

_LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    # Only for type checkers; no runtime import of raycluster or ray.
    from geneva.runners.ray.raycluster import RayCluster  # pragma: no cover


class LocalRayContext:
    """Minimal context for conn.local_ray_context(). No cluster, no manifest."""

    manifest: ClassVar[None] = None
    name: ClassVar[Literal["local"]] = "local"
    namespace: ClassVar[None] = None
    clients: ClassVar[None] = None

    def __enter__(self) -> LocalRayContext:
        import ray

        existing = get_current_context()
        if existing is not None:
            raise RuntimeError(
                f"Cannot enter local_ray_context() while already in context: "
                f"{existing.name}. Exit the current context first."
            )
        if ray.is_initialized() and ray.util.client.ray.is_connected():  # type: ignore[attr-defined]
            raise RuntimeError(
                "Cannot enter local_ray_context() while Ray is connected to a remote "
                "cluster. Disconnect first with ray.shutdown()."
            )
        set_current_context(self)
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None) -> None:
        set_current_context(None)


# Thread-safe and async-safe context storage using ContextVar
_CURRENT_GENEVA_CONTEXT: ContextVar[RayCluster | LocalRayContext | None] = ContextVar(
    "geneva_context", default=None
)


def get_current_context() -> RayCluster | LocalRayContext | None:
    return _CURRENT_GENEVA_CONTEXT.get()


def set_current_context(
    rc: RayCluster | LocalRayContext | None,
) -> None:
    from geneva.runners.ray.raycluster import RayCluster

    if rc is not None and not isinstance(rc, (RayCluster, LocalRayContext)):
        raise ValueError("rc must be a RayCluster, LocalRayContext, or None")

    existing = _CURRENT_GENEVA_CONTEXT.get()
    if rc is not None and existing is not None and rc != existing:
        _LOG.warning(
            "Overwriting existing Geneva context %s with new context %s",
            existing,
            rc,
        )

    _CURRENT_GENEVA_CONTEXT.set(rc)

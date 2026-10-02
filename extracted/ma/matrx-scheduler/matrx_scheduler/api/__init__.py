"""
matrx_scheduler.api — FastAPI HTTP surface for the scheduler package.

These routes are dormant when matrx-scheduler is used as a pure library
(scanner + runner only). They activate when imported by a host app and
mounted on its FastAPI instance.

Mount example::

    from fastapi import FastAPI
    import matrx_scheduler

    app = FastAPI()
    matrx_scheduler.api.include_routers(app, prefix="/scheduler")

Default prefix is ``/scheduler`` (singular). Aidream's pre-existing
``/scheduling/*`` routes (created before this surface existed) are
intentionally distinct so both can coexist without URL conflicts:

  - aidream:                  POST /scheduling/run-now/{task_id}
  - matrx_scheduler package:  POST /scheduler/tasks/{task_id}/run-now

Aidream is NOT required to mount these -- they exist primarily for
matrx-local, which needs a complete HTTP surface and has no aidream
routes of its own.

Routes:

  * Task CRUD              -- POST/GET/PATCH/DELETE /tasks(/...)
  * Trigger CRUD           -- POST/GET/PATCH/DELETE /triggers(/...)
  * Run history            -- GET /runs(/...)
  * Manual fire            -- POST /tasks/{id}/run-now
  * Cron + next-due        -- POST /cron/validate, /cron/preview-fires,
                              /compute-next-due-at
  * Scanner status (admin) -- GET /status

Auth model: every write uses a per-request Supabase client built from
the caller's JWT. RLS is the single line of authority. The service-
role client (used by the scanner) is never accessible from these
routes. See ``matrx_scheduler.api.per_request`` for the client builder.
"""

from __future__ import annotations

from typing import Any

from matrx_scheduler.api.router_scheduler import router as scheduler_router


def include_routers(app: Any, *, prefix: str = "/scheduler") -> None:
    """
    Mount all scheduler routers on the given FastAPI app.

    Args:
        app: FastAPI instance (or anything exposing ``include_router``).
        prefix: URL prefix for the scheduler routes. Default ``/scheduler``.
    """
    app.include_router(scheduler_router, prefix=prefix, tags=["scheduler"])


__all__ = [
    "scheduler_router",
    "include_routers",
]

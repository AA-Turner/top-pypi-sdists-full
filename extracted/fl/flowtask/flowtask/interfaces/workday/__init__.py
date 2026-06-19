"""flowtask.interfaces.workday — Workday operational interface package.

Intentionally lightweight: this __init__.py imports NOTHING heavy (no zeep,
httpx, redis) so that ``import flowtask.interfaces`` stays fast (G7).

Heavy symbols (WorkdayService, WorkdayConfig) are exposed via this package
only when explicitly imported by the caller:

    from flowtask.interfaces.workday.config import WorkdayConfig
    from flowtask.interfaces.workday.service import WorkdayService  # (TASK-103)

The lazy registration in ``flowtask/interfaces/__init__.py`` (TASK-106) will
make these available through ``flowtask.interfaces.WorkdayService`` without
eagerly loading zeep at startup.
"""

"""``runlayer schedule`` — the per-user scheduler entrypoint.

One generic entrypoint instead of one hidden command per background task: the
packaging LaunchAgent (``com.runlayer.cli.schedule``) fires it on a fixed
cadence, and it runs every registered task whose gate says it is due, each
isolated (one task's failure never blocks the next), then exits 0. It must
never raise or exit non-zero — launchd would surface noise on every
unconfigured device.

Tasks may consult the backend for what needs to run; the registry iteration
and per-task gate isolate that polling from unrelated scheduled work.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

import structlog
import typer

from runlayer_cli.api import RunlayerClient
from runlayer_cli.commands.skills import _privileged_sync_context
from runlayer_cli.config import normalize_url
from runlayer_cli.mdm_config import (
    ManagedConfig,
    read_managed_config,
    resolve_sync_skills,
)
from runlayer_cli.uv_tool_cleanup import (
    cleanup_uv_tool,
    uv_tool_cleanup_completed,
    write_uv_tool_removed_marker,
)

logger = structlog.get_logger(__name__)


@dataclass(frozen=True)
class ScheduledTask:
    """One background task the per-user scheduler can run.

    ``should_run`` is a cheap, side-effect-free gate over the managed config
    snapshot; ``run`` receives the same snapshot so a tick is evaluated
    against one consistent config read.
    """

    name: str
    should_run: Callable[[ManagedConfig], bool]
    run: Callable[[ManagedConfig], None]


def _resolve_skill_sync_secret_for(managed: ManagedConfig) -> str | None:
    """Skill-sync secret from the tick's config snapshot.

    Dedicated MDM sync key, then the env fallback (Linux root-cron wrapper),
    then the org scan key — the ``resolve_skill_sync_secret`` precedence, but
    read off the snapshot instead of a second MDM disk read, so gate and run
    can't diverge if the plist changes mid-tick. The host-match gate that
    function applies is inherently satisfied here: host and key come from the
    same snapshot.
    """
    if not managed.get("host"):
        return None
    return (
        managed.get("skill_sync_org_api_key")
        or os.environ.get("RUNLAYER_SKILL_SYNC_API_KEY")
        or managed.get("org_api_key")
        or None
    )


def _skill_sync_should_run(managed: ManagedConfig) -> bool:
    """Skill sync writes user homes only; root/SYSTEM and unconfigured
    (no managed host/key) devices are silently not due.

    ``SyncSkills=false`` is NOT a skip: the task still runs to emit the
    ``disabled`` check-in so the backend can tell "intentionally off" from
    "never ran".
    """
    if _privileged_sync_context():
        return False
    return _resolve_skill_sync_secret_for(managed) is not None


def _run_skill_sync(managed: ManagedConfig) -> None:
    host = managed.get("host")
    secret = _resolve_skill_sync_secret_for(managed)
    if not host or not secret:  # re-checked so run() is safe standalone
        return

    client = RunlayerClient(hostname=normalize_url(host), secret=secret)

    # Deferred like commands/scan.py's device imports: the hot CLI startup
    # path registers this command without paying for the scan/check-in closure.
    from runlayer_cli.aiwatch_checkin import (  # noqa: PLC0415
        _make_device_context,
        _run_isolated,
        submit_skill_sync_checkin,
        submit_skill_sync_disabled_checkin,
    )

    if not resolve_sync_skills(managed):
        _run_isolated(
            "skill_sync",
            lambda: submit_skill_sync_disabled_checkin(
                client, ctx=_make_device_context(), tools=[]
            ),
        )
        return

    from runlayer_cli.scan.device import get_or_create_device_id  # noqa: PLC0415
    from runlayer_cli.skills.device_sync import sync_assigned_skills  # noqa: PLC0415

    report = sync_assigned_skills(
        client,
        username=managed.get("username"),
        device_id=get_or_create_device_id(),
    )
    if report is None:
        # Keep-state: unresolved identity or backend unreachable; no check-in.
        logger.debug("scheduled_skill_sync_kept_state")
        return

    _run_isolated(
        "skill_sync",
        lambda: submit_skill_sync_checkin(
            client, ctx=_make_device_context(), tools=[], report=report
        ),
    )
    logger.info(
        "scheduled_skill_sync_completed",
        installed=len(report.installed),
        updated=len(report.updated),
        removed=len(report.removed),
        restored=len(report.restored),
        up_to_date=len(report.up_to_date),
        skipped=len(report.skipped),
        errors=len(report.errors),
    )


def _resolve_ai_watch_config_secret_for(managed: ManagedConfig) -> str | None:
    """Resolve the config-linked org key without accepting an MDM setting."""
    if not managed.get("host"):
        return None
    candidates = (
        managed.get("org_api_key"),
        os.environ.get("RUNLAYER_API_KEY"),
        # Older Linux schedule wrappers export only this fallback. A dedicated
        # skill-sync key may return no linked AI Watch config, which is a no-op.
        os.environ.get("RUNLAYER_SKILL_SYNC_API_KEY"),
    )
    return next(
        (
            candidate
            for candidate in candidates
            if candidate is not None and candidate.startswith("rl_org_")
        ),
        None,
    )


def _uv_tool_cleanup_should_run(managed: ManagedConfig) -> bool:
    if _privileged_sync_context() or uv_tool_cleanup_completed():
        return False
    return _resolve_ai_watch_config_secret_for(managed) is not None


def _run_uv_tool_cleanup(managed: ManagedConfig) -> None:
    host = managed.get("host")
    secret = _resolve_ai_watch_config_secret_for(managed)
    if not host or not secret or uv_tool_cleanup_completed():
        return

    client = RunlayerClient(hostname=normalize_url(host), secret=secret)
    config = client.get_aiwatch_config()
    if config is None or config["remove_uv_tool"] is not True:
        return

    # The marker records the one configured attempt, not successful deletion.
    # This prevents an absent or locked legacy install from retrying hourly.
    removed = cleanup_uv_tool()
    write_uv_tool_removed_marker()
    logger.info("scheduled_uv_tool_cleanup_completed", removed=removed)


_TASKS: tuple[ScheduledTask, ...] = (
    ScheduledTask(
        name="skill_sync",
        should_run=_skill_sync_should_run,
        run=_run_skill_sync,
    ),
    # Keep cleanup last: it may delete the uv environment running this process.
    ScheduledTask(
        name="uv_tool_cleanup",
        should_run=_uv_tool_cleanup_should_run,
        run=_run_uv_tool_cleanup,
    ),
)


def schedule(
    all_users: Annotated[
        bool,
        typer.Option(
            "--all-users",
            help="Run once as each logged-on Windows user (SYSTEM task only)",
        ),
    ] = False,
) -> None:
    """Run due scheduled tasks once and exit; packaging provides the cadence."""
    if all_users:
        # Deferred like the check-in imports above: startup-perf only —
        # windows_users imports cleanly on all platforms.
        from runlayer_cli.scan.windows_users import (  # noqa: PLC0415
            run_all_users_schedule,
        )

        exit_code = run_all_users_schedule()
        if exit_code != 0:
            raise typer.Exit(exit_code)
        return

    try:
        managed = read_managed_config()
    except Exception as e:
        logger.warning("schedule_managed_config_unreadable", error=str(e))
        return
    for task in _TASKS:
        try:
            if not task.should_run(managed):
                logger.debug("scheduled_task_not_due", task=task.name)
                continue
            logger.debug("scheduled_task_start", task=task.name)
            task.run(managed)
        except Exception as e:
            # Isolation contract: a task blowing up must neither stop later
            # tasks nor flap the LaunchAgent.
            logger.warning("scheduled_task_failed", task=task.name, error=str(e))

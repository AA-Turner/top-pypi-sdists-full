"""Managed cron scheduler service for gateway-owned background execution."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
import os
from pathlib import Path
import sys
import time
from typing import Any

from apps.cli.runtime import CliRuntime
from apps.runtime_layout import default_cli_state_dir, default_profile_dir

from .plugins import GatewayManagedRuntime, GatewayPluginRegistry, default_gateway_runtime_path


CRON_SCHEDULER_TARGET = "scheduler"


@dataclass(slots=True)
class CronSchedulerService:
    app: Any
    default_cli_profile_dir: str | None = None
    default_cli_state_dir: str | None = None
    environ: Mapping[str, str] = field(default_factory=lambda: dict(os.environ))
    runtime_state_dir: Path | None = None
    service_key: str = "cron"

    def describe(self) -> Mapping[str, object]:
        payload: dict[str, object] = {
            "configured_transport": CRON_SCHEDULER_TARGET,
            "runtime": "managed-service",
        }
        try:
            runtime = self._cli_runtime()
            jobs = runtime.cron_runtime.list_jobs()
            active_jobs = tuple(job for job in jobs if job.status == "scheduled")
            due_jobs = runtime.cron_runtime.due_jobs()
            payload.update(
                {
                    "runtime_status": "ready",
                    "jobs": len(jobs),
                    "active_jobs": len(active_jobs),
                    "due_jobs": len(due_jobs),
                    "next_run_at": min(
                        (job.next_run_at for job in active_jobs if job.next_run_at is not None),
                        default=None,
                    ),
                }
            )
        except Exception as error:
            payload.update({"runtime_status": "unavailable", "runtime_error": str(error)})
        return payload

    def configured_runtime_target(self) -> str:
        return CRON_SCHEDULER_TARGET

    def managed_runtime(self, *, args: Any, target: str) -> GatewayManagedRuntime:
        normalized_target = _normalize_target(target)
        state_dir = Path(args.state_dir)
        return GatewayManagedRuntime(
            service_key=self.service_key,
            runtime_id=f"{self.service_key}:{normalized_target}",
            target=normalized_target,
            label="cron scheduler",
            pid_path=default_gateway_runtime_path(
                state_dir,
                service_key=self.service_key,
                target=normalized_target,
                suffix="pid",
            ),
            log_path=default_gateway_runtime_path(
                state_dir,
                service_key=self.service_key,
                target=normalized_target,
                suffix="log",
            ),
            record_path=default_gateway_runtime_path(
                state_dir,
                service_key=self.service_key,
                target=normalized_target,
                suffix="runtime.json",
            ),
        )

    def build_detached_runtime_command(self, *, args: Any, target: str) -> tuple[str, ...]:
        command = [
            sys.executable,
            "-m",
            "apps.launcher",
            "cron",
            "run",
            "--profile-dir",
            str(args.profile_dir),
            "--state-dir",
            str(args.state_dir),
            "--cli-profile-dir",
            str(args.cli_profile_dir),
            "--cli-state-dir",
            str(args.cli_state_dir),
            "--workspace-id",
            str(args.workspace_id),
            "--interval-seconds",
            str(getattr(args, "interval_seconds", 60.0)),
        ]
        return tuple(command)

    def prepare_managed_runtime(self, *, action: str, target: str) -> None:
        _normalize_target(target)

    def managed_runtime_log_hint(self, *, target: str) -> str:
        return "aegis cron logs --follow"

    def run_scheduler(self, *, interval_seconds: float = 60.0, once: bool = False) -> int:
        return run_cron_scheduler_loop(
            cli_profile_dir=self._cli_profile_dir(),
            cli_state_dir=self._cli_state_dir(),
            interval_seconds=interval_seconds,
            once=once,
        )

    def _cli_runtime(self) -> CliRuntime:
        return CliRuntime.create(
            profile_dir=self._cli_profile_dir(),
            state_dir=self._cli_state_dir(),
        )

    def _cli_profile_dir(self) -> Path:
        if self.default_cli_profile_dir:
            return Path(self.default_cli_profile_dir)
        profile_dir = getattr(self.app, "profile_dir", None)
        if profile_dir:
            return Path(str(profile_dir))
        return default_profile_dir(environ=self.environ)

    def _cli_state_dir(self) -> Path:
        if self.default_cli_state_dir:
            return Path(self.default_cli_state_dir)
        state_dir = getattr(self.app, "state_dir", None)
        if state_dir:
            candidate = Path(str(state_dir))
            if candidate.name == "gateway" and candidate.parent != candidate:
                return candidate.parent
            return candidate
        return default_cli_state_dir(environ=self.environ)


def run_cron_scheduler_loop(
    *,
    cli_profile_dir: Path,
    cli_state_dir: Path,
    interval_seconds: float = 60.0,
    once: bool = False,
) -> int:
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be greater than zero")
    runtime = CliRuntime.create(state_dir=cli_state_dir, profile_dir=cli_profile_dir)
    print(
        f"Aegis cron scheduler started (interval={interval_seconds:g}s, state={cli_state_dir})",
        flush=True,
    )
    while True:
        executions = runtime.run_due_cron_jobs_for_scheduler()
        for execution in executions:
            print(
                f"cron {execution.outcome}: {execution.job.job_id} {execution.job.name} - {execution.summary}",
                flush=True,
            )
        if once:
            return 0
        time.sleep(interval_seconds)


def register_cron_scheduler_service(registry: GatewayPluginRegistry) -> GatewayPluginRegistry:
    registry.register_service("cron", factory=build_cron_scheduler_service, enabled_by_default=True)
    return registry


def build_cron_scheduler_service(
    *,
    app: Any,
    default_cli_profile_dir: str | None = None,
    default_cli_state_dir: str | None = None,
    environ: Mapping[str, str] | None = None,
    runtime_state_dir: Path | None = None,
    **_: object,
) -> CronSchedulerService:
    return CronSchedulerService(
        app=app,
        default_cli_profile_dir=default_cli_profile_dir,
        default_cli_state_dir=default_cli_state_dir,
        environ=dict(environ or os.environ),
        runtime_state_dir=runtime_state_dir,
    )


def _normalize_target(value: object) -> str:
    normalized = str(value or CRON_SCHEDULER_TARGET).strip().lower().replace("_", "-")
    if normalized in {"configured", CRON_SCHEDULER_TARGET, "cron"}:
        return CRON_SCHEDULER_TARGET
    raise ValueError(f"unsupported cron scheduler target: {value}")


__all__ = [
    "CRON_SCHEDULER_TARGET",
    "CronSchedulerService",
    "build_cron_scheduler_service",
    "register_cron_scheduler_service",
    "run_cron_scheduler_loop",
]

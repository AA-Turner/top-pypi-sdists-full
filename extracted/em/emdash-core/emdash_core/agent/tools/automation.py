"""AutomationTool — lets the LLM agent manage cron jobs, heartbeat, and webhooks."""

from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool, ToolCategory, ToolResult

log = logging.getLogger(__name__)


class AutomationTool(BaseTool):
    """Add, remove, list, enable, disable, or configure scheduled automations.

    Schedule types:
    - ``at``   — one-shot at an ISO datetime
    - ``every``— recurring interval (``"30m"``, ``"2h"``, ``"1d"``, ``"1w"``)
    - ``cron`` — cron expression (``"0 9 * * 1-5"``)

    Execution modes:
    - ``main_session`` — inject event into the running conversation
    - ``isolated``     — spawn a fresh agent turn and deliver result
    """

    name = "manage_automation"
    description = (
        "Set reminders, schedule recurring tasks, and manage cron jobs. "
        "USE THIS when the user says 'remind me', 'every morning', 'check every', 'in 30 minutes', 'at 5pm', or any scheduling request. "
        "Actions: 'add' (create job), 'list' (show jobs), 'remove' (delete), "
        "'enable'/'disable' (toggle), 'status' (overview), 'configure' (cron/heartbeat/webhook settings). "
        "Before adding jobs, ensure cron is enabled via action='configure' with config={'cron_enabled': true}."
    )
    category = ToolCategory.COMMUNICATION

    def __init__(self) -> None:
        super().__init__(connection=False)

    # -- Schema --------------------------------------------------------------

    def get_schema(self) -> dict:
        return self._make_schema(
            {
                "action": {
                    "type": "string",
                    "enum": ["add", "remove", "list", "enable", "disable", "status", "configure"],
                    "description": "Action to perform.",
                },
                "name": {
                    "type": "string",
                    "description": "Job name (required for add).",
                },
                "job_id": {
                    "type": "string",
                    "description": "Job ID (for remove/enable/disable).",
                },
                "schedule_type": {
                    "type": "string",
                    "enum": ["at", "every", "cron"],
                    "description": "Schedule type: 'at' (one-shot datetime), 'every' (interval), 'cron' (expression).",
                },
                "schedule_value": {
                    "type": "string",
                    "description": "Schedule value: ISO datetime, interval ('30m'/'2h'/'1d'), or cron expression.",
                },
                "payload": {
                    "type": "string",
                    "description": "Message to send to the agent when the job fires.",
                },
                "mode": {
                    "type": "string",
                    "enum": ["main_session", "isolated"],
                    "description": "Execution mode: 'main_session' or 'isolated'.",
                },
                "config": {
                    "type": "object",
                    "description": "Configuration updates (for action='configure'). Keys: cron_enabled, heartbeat_enabled, heartbeat_interval, heartbeat_active_hours, heartbeat_payload, webhooks_enabled, max_concurrent_runs.",
                },
            },
            required=["action"],
        )

    # -- Execute -------------------------------------------------------------

    def execute(self, **kwargs: Any) -> ToolResult:
        action: str = kwargs.get("action", "")
        dispatch = {
            "add": self._add,
            "remove": self._remove,
            "list": self._list,
            "enable": self._enable,
            "disable": self._disable,
            "status": self._status,
            "configure": self._configure,
        }
        handler = dispatch.get(action)
        if handler is None:
            return ToolResult.error_result(
                f"Unknown action: {action}",
                suggestions=["Use one of: add, remove, list, enable, disable, status, configure"],
            )
        return handler(**kwargs)

    # -- Helpers -------------------------------------------------------------

    @staticmethod
    def _get_manager():
        from ...automation.manager import get_automation_manager
        return get_automation_manager()

    # -- Actions -------------------------------------------------------------

    def _add(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized (server not started?).")

        name = kwargs.get("name")
        schedule_type = kwargs.get("schedule_type")
        schedule_value = kwargs.get("schedule_value")
        payload = kwargs.get("payload")
        mode = kwargs.get("mode", "main_session")

        if not name:
            return ToolResult.error_result("'name' is required for add action.")
        if not schedule_type:
            return ToolResult.error_result("'schedule_type' is required for add action.")
        if not schedule_value:
            return ToolResult.error_result("'schedule_value' is required for add action.")
        if not payload:
            return ToolResult.error_result("'payload' is required for add action.")

        try:
            job = mgr.add_job(
                name=name,
                schedule_type=schedule_type,
                schedule_value=schedule_value,
                payload=payload,
                mode=mode,
            )
        except ValueError as e:
            return ToolResult.error_result(str(e))

        return ToolResult.success_result(data={
            "message": f"Job '{name}' created (id={job.id}).",
            "job": job.to_dict(),
        })

    def _remove(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized.")

        job_id = kwargs.get("job_id")
        if not job_id:
            return ToolResult.error_result("'job_id' is required for remove action.")

        if mgr.remove_job(job_id):
            return ToolResult.success_result(data={"message": f"Job {job_id} removed."})
        return ToolResult.error_result(f"Job {job_id} not found.")

    def _list(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized.")

        jobs = mgr.list_jobs()
        return ToolResult.success_result(data={"jobs": jobs, "count": len(jobs)})

    def _enable(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized.")

        job_id = kwargs.get("job_id")
        if not job_id:
            return ToolResult.error_result("'job_id' is required for enable action.")

        job = mgr.update_job(job_id, enabled=True)
        if job:
            return ToolResult.success_result(data={"message": f"Job {job_id} enabled.", "job": job.to_dict()})
        return ToolResult.error_result(f"Job {job_id} not found.")

    def _disable(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized.")

        job_id = kwargs.get("job_id")
        if not job_id:
            return ToolResult.error_result("'job_id' is required for disable action.")

        job = mgr.update_job(job_id, enabled=False)
        if job:
            return ToolResult.success_result(data={"message": f"Job {job_id} disabled.", "job": job.to_dict()})
        return ToolResult.error_result(f"Job {job_id} not found.")

    def _status(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized.")

        config = mgr.get_config()
        jobs = mgr.list_jobs()
        return ToolResult.success_result(data={
            "config": config.to_dict(),
            "jobs": jobs,
            "job_count": len(jobs),
        })

    def _configure(self, **kwargs: Any) -> ToolResult:
        mgr = self._get_manager()
        if mgr is None:
            return ToolResult.error_result("Automation manager not initialized.")

        config_updates = kwargs.get("config")
        if not config_updates or not isinstance(config_updates, dict):
            return ToolResult.error_result("'config' dict is required for configure action.")

        config = mgr.update_config(**config_updates)
        return ToolResult.success_result(data={
            "message": "Configuration updated.",
            "config": config.to_dict(),
        })

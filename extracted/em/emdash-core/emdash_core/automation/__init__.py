"""Automation subsystem — cron jobs, heartbeat, and webhooks for OpenAgent."""

from .manager import AutomationManager, get_automation_manager, set_automation_manager

__all__ = ["AutomationManager", "get_automation_manager", "set_automation_manager"]

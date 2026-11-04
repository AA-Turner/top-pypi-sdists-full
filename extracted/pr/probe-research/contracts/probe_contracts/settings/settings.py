"""SettingKey: the five settings `settings.json` holds; SetBy: who chose a value. One vocabulary for the
CLI, the Probe service and the Mac app (plan app-never-waits: settings are a file the service makes true)."""

from __future__ import annotations

from ..compat import StrEnum


class SettingKey(StrEnum):
    """A setting in `settings.json`. Transcripts and who records hold one value per coding agent."""

    SESSION_DEFAULT = "session_default"
    AUTO_UPDATE = "auto_update"
    TRANSCRIPTS = "transcripts"
    RECORDER = "recorder"
    WORKSPACE = "workspace"


class SetBy(StrEnum):
    """Who chose a setting's value: a person at a terminal, a coding agent, the Probe app, or an older Probe
    copy that wrote the live value directly (adopted by the service)."""

    PERSON = "person"
    AGENT = "agent"
    APP = "app"
    LEGACY = "legacy"

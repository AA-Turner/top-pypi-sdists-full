"""SettingKey: the seven settings `settings.json` holds; SetBy: who chose a value. One vocabulary for the
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
    #: The install profile, `full` or `runs` (Runs only, agent-prompt install D28). No keeper applies it:
    #: `probe install --profile` publishes and applies it itself; a machine that never chose is `full`.
    PROFILE = "profile"
    #: Who sets a chat's switch: `auto` (the main agent, by the work, until the researcher types `/probe`) or
    #: `manual` (the researcher). Probe auto mode, 2026-11-07.
    SESSION_CONTROL = "session_control"


class SetBy(StrEnum):
    """Who chose a setting's value: a person at a terminal, a coding agent, the Probe app, or an older Probe
    copy that wrote the live value directly (adopted by the service)."""

    PERSON = "person"
    AGENT = "agent"
    APP = "app"
    LEGACY = "legacy"

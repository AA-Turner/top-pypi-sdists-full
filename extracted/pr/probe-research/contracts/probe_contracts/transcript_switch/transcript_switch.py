"""TranscriptState: whether a coding agent's sessions upload as transcripts, and if not, why;
SwitchedBy: who turned them off. One vocabulary for the CLI, the server, the dashboard and the app."""

from __future__ import annotations

from ..compat import StrEnum


class TranscriptState(StrEnum):
    """One agent's (or the machine's) session transcripts. `off` is a choice, never a fault."""

    ON = "on"
    OFF = "off"
    AWAITING_INSTALL = "awaiting_install"
    NOT_PAIRED = "not_paired"
    KEY_REFUSED = "key_refused"
    PLUGIN_MISSING = "plugin_missing"
    NOT_RUNNING = "not_running"


class SwitchedBy(StrEnum):
    """Who turned transcripts off: a person at a terminal, a coding agent (no terminal), the Probe app."""

    PERSON = "person"
    AGENT = "agent"
    APP = "app"

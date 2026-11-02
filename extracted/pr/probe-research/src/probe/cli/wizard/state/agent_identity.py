"""which coding agent this run configures (PROBE_AGENT or the environment) and which Probe plugins it should carry."""

from __future__ import annotations
import os
import warnings
from contextlib import contextmanager
ENV_AGENT = "PROBE_AGENT"


class UnrecognizedAgentSourceWarning(UserWarning):
    """PROBE_AGENT was set to a value this CLI does not recognize.

    A WARNING plus a claude_code fallback, not an exception -- Mahit's call
    (2026-08-28): a typo'd or stale PROBE_AGENT on an existing machine used
    to silently work as claude_code, and a hard raise would turn that machine
    from quietly-working into broken on upgrade. So the boundary stays loud
    without regressing: the warning names the value and the accepted set on
    stderr, while behavior falls back to the pre-pi default. The DESTRUCTIVE
    half of the old silent-default bug class (pi reaching Claude Code's
    marketplace CLI) is guarded separately and still HARD-raises -- see
    plugin_cli.binary_name(), which a fallback here can never reach with an
    unrecognized value because this function only ever returns the three
    known sources.
    """


def tracking_plugin_name(source: str | None = None) -> str:
    """The Probe plugin this coding agent should carry: `probe-research-daemon`
    when its "Who records" is the daemon (`session_marker.recorder`), else
    `probe-research`. The one place install, detection, update and removal
    ask, so none of them can put the other profile's plugin back."""
    from probe.sdk import session_marker

    try:
        daemon = session_marker.recorder(source or agent_source()) == session_marker.RECORDER_DAEMON
    except Exception:  # noqa: BLE001 - an unreadable config is today's profile
        daemon = False
    return DAEMON_PLUGIN_NAME if daemon else TRACKING_PLUGIN_NAME


def agent_source() -> str:
    """Setup target: explicit override, then the coding-agent environment.

    pi has no environment-sniffing shortcut the way a Codex session does
    (there is no PROBE_TAP_SOURCE-equivalent pi sets on its own child
    processes) -- PROBE_AGENT=pi is the only way in.

    Three cases, not two:
      - unset or empty (after stripping) -> claude_code. This is "nothing was
        asked" and is the correct, load-bearing default: every existing
        install that never sets PROBE_AGENT depends on it. Do not change it.
      - a recognized value (claude/claude_code, codex, pi) -> that source.
      - a non-empty, unrecognized value -> a LOUD UnrecognizedAgentSourceWarning
        and the claude_code fallback. Same posture as the live-capture daemon
        normalizer, tap/config.py::capture_source(), and for the same reason:
        a machine that has quietly worked for months with a stale or typo'd
        PROBE_AGENT must not break on upgrade. The warning (not silence) is
        what keeps the misspelling discoverable; the fallback is what keeps
        it non-regressive. python -W error turns it back into a hard stop
        for anyone who wants the strict behavior.
    """
    from probe.foundation.harness_registry import get_registry

    registry = get_registry()
    raw = os.environ.get(ENV_AGENT) or ""
    explicit = raw.strip().lower()
    if not explicit:
        return registry.default
    harness = registry.find(explicit)
    if harness is not None and harness.installable:
        return harness.id
    accepted = ", ".join(name for h in registry.installable() for name in h.names)
    warnings.warn(
        f"{ENV_AGENT}={raw!r} is not a recognized agent source "
        f"(accepted: {accepted}); continuing as {registry.default}",
        UnrecognizedAgentSourceWarning,
        stacklevel=2,
    )
    return registry.default


@contextmanager
def agent_target(source: str):
    """Scope ENV_AGENT to one operation without leaking it to the caller.

    Nearly everything here resolves its target agent from the environment (see
    `agent_source`), so code that must act on a NAMED agent has to set it --
    and put it back, or the next call in the same process silently inherits a
    target nobody chose. One wizard run configures both agents in turn, which
    is exactly where that would bite.
    """
    previous = os.environ.get(ENV_AGENT)
    os.environ[ENV_AGENT] = source
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop(ENV_AGENT, None)
        else:
            os.environ[ENV_AGENT] = previous


def capture_plugin_name(source: str | None = None) -> str:
    return CODEX_TAP_PLUGIN_NAME if (source or agent_source()) == "codex" else TAP_PLUGIN_NAME
from probe.cli.wizard.state.state import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CODEX_TAP_PLUGIN_NAME,
    DAEMON_PLUGIN_NAME,
    TAP_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
)

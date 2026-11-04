"""Probe CLI telemetry: the install and import funnels, emitted in-process, fail-silent.

Events, funnel semantics, the contract (metadata only, async, gates): DESIGN.md (analytics.py).
"""

from __future__ import annotations
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from probe.analytics import core as core
from probe.foundation.tls.tls import ssl_context
from probe.analytics.outcomes import IdentityMode, InvokedBy, Via
from probe.analytics import sender  # call through the module: one binding for tests to patch
from probe.generated.transcript_switch import SwitchedBy
# Set only on a child's explicit desktop action, independently of its stdin TTY.
DESKTOP_HUMAN_ENV = "PROBE_DESKTOP_HUMAN"
DESKTOP_SURFACE = "desktop"
#: Who asked for a Probe service action (`SwitchedBy`'s word), set on its child (plan R30).
ASKED_BY_ENV = "PROBE_ASKED_BY"


def is_person_asking() -> bool:
    """Did a person at a terminal ask for the Probe service action this process runs?"""
    return os.environ.get(ASKED_BY_ENV) == SwitchedBy.PERSON.value


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


@dataclass
class TelemetryContext:
    """The session handle threaded through the wizard and backfill.

    Disabled, emit() is a no-op, so call sites never branch; `telemetry=None`
    parameters normalize through :func:`null_context`.
    """

    session_id: str
    via: str  # Via value
    invoked_by: str  # InvokedBy value (tty-based; robots are non-tty)
    enabled: bool = True
    #: Identity resolved AHEAD of the one flow that destroys its credential
    #: (:meth:`pin_identity`); None for every other event.
    pinned_identity: dict | None = None
    surface: str | None = None

    @classmethod
    def start(cls, *, via: str, interactive: bool, base_url: str | None) -> "TelemetryContext":
        # Killswitch + hosted gate, once per context, before the sender thread exists. Accepted: a
        # mid-session switch to self-host emits until exit (the per-batch gate guards identity).
        try:
            is_enabled = not core.telemetry_disabled() and core.hosted_base_url(base_url)
        except Exception:
            is_enabled = False
        desktop = (os.environ.get(DESKTOP_HUMAN_ENV) == "1"
                   and via in (Via.WIZARD, Via.COMMAND))
        # A terminal's action run by the Probe service keeps its asker, under `via: service`
        # (plan T26): the install funnel does not split between the two paths.
        for_terminal = (not desktop and via in (Via.WIZARD, Via.COMMAND)
                        and os.environ.get(ASKED_BY_ENV) in (SwitchedBy.PERSON.value, SwitchedBy.AGENT.value))
        person = is_person_asking()
        context = cls(
            session_id=uuid.uuid4().hex,
            via=Via.SERVICE if for_terminal else via,
            invoked_by=InvokedBy.HUMAN if interactive or desktop or person else InvokedBy.AUTOMATION,
            enabled=is_enabled,
            surface=DESKTOP_SURFACE if desktop else None,
        )
        if is_enabled:
            try:
                sender._ensure_sender()
            except Exception:
                context.enabled = False
        global _current
        _current = context
        return context

    def emit(
        self,
        event: str,
        *,
        identity_mode: str | None = None,
        **props,
    ) -> None:
        """Stamp emit-time truth and enqueue; returns in microseconds.

        identity_mode defaults to the config's token presence AT EMIT TIME, so a
        forgotten kwarg never mislabels an authenticated event. Pass it only to pin
        a mode the caller knows better than the config.
        """
        if not self.enabled:
            return
        try:
            if self.pinned_identity is not None and not identity_mode:
                # The config this would otherwise read is gone; the pin IS the
                # emit-time truth for these events.
                mode = IdentityMode.AUTHENTICATED
            else:
                mode = str(identity_mode) if identity_mode else identity_mode_from_config()
            properties = {
                "session_id": self.session_id,
                "via": self.via,
                "invoked_by": self.invoked_by,
                "identity_mode": mode,
            }
            if self.surface is not None:
                properties["surface"] = self.surface
            properties.update({k: v for k, v in props.items() if v is not None})
            # Same contract as core.build_batch: detected or absent, never a
            # placeholder that reads as Claude Code for a Codex or pi user.
            detected = core.detect_agent_label()
            if detected is not None:
                properties.setdefault("agent", detected)
            record = {
                "event": event,
                "identity_mode": mode,
                "timestamp": _now_iso(),
                "properties": properties,
            }
            if self.pinned_identity is not None:
                record["identity"] = self.pinned_identity
            sender._ensure_sender().put(record)
        except Exception:
            pass  # observability must never become observable


    def pin_identity(self) -> None:
        """Resolve this device's identity NOW, while its credential is present and valid.

        Uninstall's `finish_removal` revokes and clears the token before its event is
        sent, so send-time resolution would key it to `machine:<id>`, and every
        #probe-usage destination (filters on `email is_set`) would drop it. Usually a
        cache read; fail-soft (no pin, never a failed uninstall). Why: DESIGN.md (pin_identity).
        """
        if not self.enabled:
            return
        try:
            identity = core.resolve_identity(
                core.read_cli_config(), machine=core.machine_id(), context=ssl_context()
            )
            if identity.get("authenticated"):
                self.pinned_identity = identity
        except Exception:
            pass  # observability must never become observable


def null_context() -> TelemetryContext:
    return TelemetryContext(
        session_id="", via=Via.NONE, invoked_by=InvokedBy.AUTOMATION, enabled=False
    )


#: The context this PROCESS started (one per command: a process constant). Its one job:
#: stamp the approving session onto a durable import record. Why not a parameter: DESIGN.md.
_current: TelemetryContext | None = None


def current() -> TelemetryContext:
    """This process's context, or a disabled one. Never None, never raises."""
    return _current if _current is not None else null_context()


def track(event: str, **props) -> None:
    """Send one product event (an `Event` member or its EVENT_* name) under this
    process's ambient context: the one entry, callable from anywhere. A process that
    started no context sends nothing. Never raises."""
    current().emit(str(event), **props)  # str(member) is its wire name, on 3.10 too


def identity_mode_from_config() -> str:
    """anonymous|authenticated from token presence (env or config); no network.
    A PROBE_TOKEN env counts: it is authenticated everywhere else in the client."""
    try:
        if core.effective_token(core.read_cli_config()):
            return IdentityMode.AUTHENTICATED
    except Exception:
        pass
    return IdentityMode.ANONYMOUS

"""Turn lifecycle manager — single owner of busy state and turn transitions.

Every agent turn goes through: idle → active → (completing | interrupted) → idle.
This module owns those transitions and the invariants around them.

The app delegates all busy-state decisions here rather than scattering
``_set_status("...", busy=True/False)`` across dozens of call sites.
"""

from __future__ import annotations

import enum
import typing as t

from loguru import logger


class TurnPhase(enum.Enum):
    """Valid phases of a turn's lifecycle."""

    IDLE = "idle"
    """No turn active — composer enabled, user can type."""

    ACTIVE = "active"
    """Turn in progress — streaming events from the server."""

    AWAITING = "awaiting"
    """Server is waiting for human input (approval, text, etc.)."""

    INTERRUPTED = "interrupted"
    """Turn was cancelled by the user — transient, moves to IDLE."""


class TurnLifecycle:
    """Owns the busy flag, generation counter, and phase transitions.

    All turn state changes flow through this class.  The app reads
    ``phase`` and ``generation`` but never writes ``busy`` directly —
    it calls the transition methods instead.

    Parameters
    ----------
    set_status:
        Callback to update the app's ``status_text`` and ``busy`` reactives.
    set_composer_enabled:
        Callback to enable/disable the composer widget.
    focus_composer:
        Callback to give focus to the composer.
    """

    def __init__(
        self,
        *,
        set_status: t.Callable[[str, bool], None],
        set_composer_enabled: t.Callable[[bool], None],
        focus_composer: t.Callable[[], None],
    ) -> None:
        self._set_status = set_status
        self._set_composer_enabled = set_composer_enabled
        self._focus_composer = focus_composer

        self._phase: TurnPhase = TurnPhase.IDLE
        self._generation: int = 0
        self._owner: str | None = None

    # ------------------------------------------------------------------
    # Read-only state
    # ------------------------------------------------------------------

    @property
    def phase(self) -> TurnPhase:
        return self._phase

    @property
    def is_busy(self) -> bool:
        return self._phase in (TurnPhase.ACTIVE, TurnPhase.AWAITING)

    @property
    def generation(self) -> int:
        """Monotonic counter incremented on each new turn start."""
        return self._generation

    # ------------------------------------------------------------------
    # Transitions
    # ------------------------------------------------------------------

    def start_turn(self, status: str = "Thinking", *, owner: str | None = None) -> int:
        """Transition to ACTIVE and return the generation for this turn.

        Called at the top of ``_send_chat`` / ``_send_chat_to_agent`` /
        ``_execute_shell``.
        """
        self._generation += 1
        self._phase = TurnPhase.ACTIVE
        self._owner = owner
        self._set_status(status, True)
        logger.debug("Turn start | generation={} status={}", self._generation, status)
        return self._generation

    def enter_awaiting(self, status: str) -> None:
        """Transition from ACTIVE to AWAITING (server wants human input).

        Called when a ``userinputrequired`` event arrives.
        """
        if self._phase != TurnPhase.ACTIVE:
            logger.warning(
                "enter_awaiting called in phase {} (expected ACTIVE), proceeding anyway",
                self._phase.value,
            )
        self._phase = TurnPhase.AWAITING
        self._set_status(status, True)

    def resume_from_awaiting(self, status: str = "Resuming") -> None:
        """Transition from AWAITING back to ACTIVE (user responded).

        Called after sending a human input / permission response.
        """
        if self._phase != TurnPhase.AWAITING:
            logger.warning(
                "resume_from_awaiting called in phase {} (expected AWAITING)",
                self._phase.value,
            )
        self._phase = TurnPhase.ACTIVE
        self._set_status(status, True)

    def interrupt(self) -> int:
        """Transition to INTERRUPTED, then immediately to IDLE.

        Called by the escape / Ctrl+Q handler.  Returns the generation
        that was interrupted so callers can log or compare.

        Bumps the generation counter so any in-flight worker ``finally``
        blocks that call ``finish_turn`` with the old generation will
        see a mismatch and skip state changes.
        """
        old_gen = self._generation
        # Bump so stale finally blocks don't clobber us.
        self._generation += 1
        self._phase = TurnPhase.IDLE
        self._set_status("Interrupted", False)
        self._set_composer_enabled(True)
        self._focus_composer()
        logger.debug(
            "Turn interrupted | old_generation={} new_generation={}",
            old_gen,
            self._generation,
        )
        return old_gen

    def sync_projection(
        self,
        *,
        owner: str | None,
        phase: TurnPhase,
        status: str,
        authenticated: bool,
    ) -> None:
        """Project externally-owned session state into the visible lifecycle.

        This is used when the active session changes or when the UI is restored
        from stored session state. If the lifecycle ownership moves to a
        different session, the generation is bumped so stale worker cleanup from
        the previous owner cannot clobber the visible lifecycle.
        """
        if owner != self._owner:
            self._generation += 1
        self._owner = owner
        self._phase = phase
        self._set_status(status, phase is not TurnPhase.IDLE)
        self._set_composer_enabled(authenticated)

    def finish_turn(self, generation: int) -> bool:
        """Complete a turn normally — called from the worker ``finally`` block.

        Returns True if this call owns the transition (generation matches
        and phase is still ACTIVE/AWAITING).  Returns False if an
        interrupt or newer turn already took ownership — the caller
        should bail without touching any state.
        """
        if generation != self._generation:
            logger.debug(
                "finish_turn skipped | generation={} current={} (stale)",
                generation,
                self._generation,
            )
            return False

        if self._phase == TurnPhase.IDLE:
            # Already idle — interrupt got here first.
            logger.debug("finish_turn skipped | already idle")
            return False

        # We own the transition.
        self._phase = TurnPhase.IDLE
        logger.debug("Turn finished | generation={}", generation)
        return True

    def go_idle(self, *, authenticated: bool = True) -> None:
        """Unconditionally transition to IDLE with Ready status.

        For use after ``finish_turn`` returns True and the caller has
        completed any drain/queue logic.  Also used by non-turn paths
        (session creation, login, etc.) that need to reset to ready.
        """
        self._phase = TurnPhase.IDLE
        self._set_status("Ready", False)
        self._set_composer_enabled(authenticated)
        if authenticated:
            self._focus_composer()

    def go_idle_with_error(self, status: str, *, authenticated: bool = True) -> None:
        """Transition to IDLE with an error status (e.g. permission failure)."""
        self._phase = TurnPhase.IDLE
        self._set_status(status, False)
        self._set_composer_enabled(authenticated)
        if authenticated:
            self._focus_composer()

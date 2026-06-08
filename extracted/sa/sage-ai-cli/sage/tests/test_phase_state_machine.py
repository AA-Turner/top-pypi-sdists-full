"""Tests for phase state machine and structured events - P1 items 36-45.

Tests verify:
- Phase state machine transitions are valid
- Structured events are emitted correctly
- Phase validation works properly
- Phase completion is tracked
- Event ordering is guaranteed
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any

# =============================================================================
# Phase State Machine Implementation
# =============================================================================


class PhaseState(Enum):
    """States a phase can be in."""

    PENDING = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    FAILED = auto()
    SKIPPED = auto()
    BLOCKED = auto()


class Phase(Enum):
    """Workflow phases for SAGE operations."""

    CLASSIFY = auto()  # Classify the request
    EXPLORE = auto()  # Explore codebase
    ANALYZE = auto()  # Analyze findings
    PLAN = auto()  # Create execution plan
    IMPLEMENT = auto()  # Implement changes
    TEST = auto()  # Run tests
    VALIDATE = auto()  # Validate results
    SYNTHESIZE = auto()  # Synthesize output
    COMPLETE = auto()  # Mark completion


@dataclass
class PhaseTransition:
    """A phase state transition."""

    from_phase: Phase
    from_state: PhaseState
    to_state: PhaseState
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reason: str = ""


@dataclass
class StructuredEvent:
    """A structured event emitted during phase execution."""

    event_type: str
    phase: Phase
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    sequence_number: int = 0


@dataclass
class PhaseInfo:
    """Information about a phase's execution."""

    phase: Phase
    state: PhaseState = PhaseState.PENDING
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None
    result: Any = None
    attempts: int = 0
    max_attempts: int = 3


class PhaseStateMachine:
    """State machine for managing phase transitions."""

    # Valid state transitions
    VALID_TRANSITIONS: dict[PhaseState, set[PhaseState]] = {
        PhaseState.PENDING: {PhaseState.ACTIVE, PhaseState.SKIPPED, PhaseState.BLOCKED},
        PhaseState.ACTIVE: {PhaseState.COMPLETED, PhaseState.FAILED},
        PhaseState.COMPLETED: set(),  # Terminal state
        PhaseState.FAILED: {PhaseState.ACTIVE, PhaseState.SKIPPED},  # Can retry
        PhaseState.SKIPPED: set(),  # Terminal state
        PhaseState.BLOCKED: {PhaseState.PENDING, PhaseState.SKIPPED},
    }

    # Phase ordering
    PHASE_ORDER: list[Phase] = [
        Phase.CLASSIFY,
        Phase.EXPLORE,
        Phase.ANALYZE,
        Phase.PLAN,
        Phase.IMPLEMENT,
        Phase.TEST,
        Phase.VALIDATE,
        Phase.SYNTHESIZE,
        Phase.COMPLETE,
    ]

    def __init__(self):
        self.phases: dict[Phase, PhaseInfo] = {phase: PhaseInfo(phase=phase) for phase in Phase}
        self.transitions: list[PhaseTransition] = []
        self.events: list[StructuredEvent] = []
        self._event_counter = 0
        self._event_listeners: list[Callable[[StructuredEvent], None]] = []

    def can_transition(self, phase: Phase, to_state: PhaseState) -> bool:
        """Check if a transition is valid."""
        current_state = self.phases[phase].state
        return to_state in self.VALID_TRANSITIONS.get(current_state, set())

    def transition(self, phase: Phase, to_state: PhaseState, reason: str = "") -> bool:
        """Attempt to transition a phase to a new state."""
        if not self.can_transition(phase, to_state):
            return False

        from_state = self.phases[phase].state
        self.phases[phase].state = to_state

        # Update timestamps
        now = datetime.now().isoformat()
        if to_state == PhaseState.ACTIVE:
            self.phases[phase].started_at = now
            self.phases[phase].attempts += 1
        elif to_state in (PhaseState.COMPLETED, PhaseState.FAILED, PhaseState.SKIPPED):
            self.phases[phase].completed_at = now

        # Record transition
        transition = PhaseTransition(
            from_phase=phase,
            from_state=from_state,
            to_state=to_state,
            reason=reason,
        )
        self.transitions.append(transition)

        # Emit event
        self.emit_event(
            event_type="phase_transition",
            phase=phase,
            data={
                "from_state": from_state.name,
                "to_state": to_state.name,
                "reason": reason,
            },
        )

        return True

    def emit_event(
        self, event_type: str, phase: Phase, data: dict[str, Any] = None
    ) -> StructuredEvent:
        """Emit a structured event."""
        self._event_counter += 1
        event = StructuredEvent(
            event_type=event_type,
            phase=phase,
            data=data or {},
            sequence_number=self._event_counter,
        )
        self.events.append(event)

        # Notify listeners
        for listener in self._event_listeners:
            listener(event)

        return event

    def add_event_listener(self, listener: Callable[[StructuredEvent], None]) -> None:
        """Add an event listener."""
        self._event_listeners.append(listener)

    def get_current_phase(self) -> Phase | None:
        """Get the currently active phase."""
        for phase in self.PHASE_ORDER:
            if self.phases[phase].state == PhaseState.ACTIVE:
                return phase
        return None

    def get_next_phase(self, current: Phase) -> Phase | None:
        """Get the next phase in order."""
        try:
            idx = self.PHASE_ORDER.index(current)
            if idx + 1 < len(self.PHASE_ORDER):
                return self.PHASE_ORDER[idx + 1]
        except ValueError:
            pass
        return None

    def is_complete(self) -> bool:
        """Check if all phases are complete or skipped."""
        for phase in Phase:
            if self.phases[phase].state not in (
                PhaseState.COMPLETED,
                PhaseState.SKIPPED,
            ):
                return False
        return True

    def get_failed_phases(self) -> list[Phase]:
        """Get list of failed phases."""
        return [p for p in Phase if self.phases[p].state == PhaseState.FAILED]

    def get_phase_state(self, phase: Phase) -> PhaseState:
        """Get the current state of a phase."""
        return self.phases[phase].state

    def set_phase_result(self, phase: Phase, result: Any) -> None:
        """Set the result for a phase."""
        self.phases[phase].result = result

    def set_phase_error(self, phase: Phase, error: str) -> None:
        """Set an error for a phase."""
        self.phases[phase].error = error


class EventAggregator:
    """Aggregates and filters events."""

    def __init__(self):
        self.events: list[StructuredEvent] = []

    def add_event(self, event: StructuredEvent) -> None:
        """Add an event."""
        self.events.append(event)

    def get_events_by_type(self, event_type: str) -> list[StructuredEvent]:
        """Get events of a specific type."""
        return [e for e in self.events if e.event_type == event_type]

    def get_events_by_phase(self, phase: Phase) -> list[StructuredEvent]:
        """Get events for a specific phase."""
        return [e for e in self.events if e.phase == phase]

    def get_events_in_order(self) -> list[StructuredEvent]:
        """Get events sorted by sequence number."""
        return sorted(self.events, key=lambda e: e.sequence_number)


# =============================================================================
# Tests
# =============================================================================


class TestPhaseStateTransitions:
    """P1 item 36: Phase state machine transitions."""

    def test_pending_to_active_allowed(self):
        """Should allow transition from PENDING to ACTIVE."""
        sm = PhaseStateMachine()
        assert sm.can_transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        assert sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        assert sm.get_phase_state(Phase.CLASSIFY) == PhaseState.ACTIVE

    def test_pending_to_skipped_allowed(self):
        """Should allow transition from PENDING to SKIPPED."""
        sm = PhaseStateMachine()
        assert sm.can_transition(Phase.IMPLEMENT, PhaseState.SKIPPED)
        assert sm.transition(Phase.IMPLEMENT, PhaseState.SKIPPED, "Read-only mode")
        assert sm.get_phase_state(Phase.IMPLEMENT) == PhaseState.SKIPPED

    def test_active_to_completed_allowed(self):
        """Should allow transition from ACTIVE to COMPLETED."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        assert sm.can_transition(Phase.CLASSIFY, PhaseState.COMPLETED)
        assert sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)
        assert sm.get_phase_state(Phase.CLASSIFY) == PhaseState.COMPLETED

    def test_active_to_failed_allowed(self):
        """Should allow transition from ACTIVE to FAILED."""
        sm = PhaseStateMachine()
        sm.transition(Phase.ANALYZE, PhaseState.ACTIVE)
        assert sm.can_transition(Phase.ANALYZE, PhaseState.FAILED)
        sm.transition(Phase.ANALYZE, PhaseState.FAILED, "Analysis error")

    def test_completed_is_terminal(self):
        """COMPLETED should be a terminal state."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)

        # Cannot transition from COMPLETED
        assert not sm.can_transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        assert not sm.can_transition(Phase.CLASSIFY, PhaseState.FAILED)

    def test_failed_can_retry(self):
        """FAILED phases should allow retry (back to ACTIVE)."""
        sm = PhaseStateMachine()
        sm.transition(Phase.TEST, PhaseState.ACTIVE)
        sm.transition(Phase.TEST, PhaseState.FAILED)

        assert sm.can_transition(Phase.TEST, PhaseState.ACTIVE)
        assert sm.transition(Phase.TEST, PhaseState.ACTIVE)

    def test_invalid_transition_rejected(self):
        """Invalid transitions should be rejected."""
        sm = PhaseStateMachine()
        # Cannot go from PENDING to COMPLETED directly
        assert not sm.can_transition(Phase.PLAN, PhaseState.COMPLETED)
        assert not sm.transition(Phase.PLAN, PhaseState.COMPLETED)


class TestStructuredEvents:
    """P1 item 37: Structured event emission."""

    def test_event_emitted_on_transition(self):
        """Events should be emitted on phase transitions."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)

        assert len(sm.events) == 1
        event = sm.events[0]
        assert event.event_type == "phase_transition"
        assert event.phase == Phase.CLASSIFY

    def test_event_contains_transition_data(self):
        """Events should contain transition data."""
        sm = PhaseStateMachine()
        sm.transition(Phase.EXPLORE, PhaseState.ACTIVE, reason="Starting exploration")

        event = sm.events[0]
        assert event.data["from_state"] == "PENDING"
        assert event.data["to_state"] == "ACTIVE"
        assert event.data["reason"] == "Starting exploration"

    def test_events_have_sequence_numbers(self):
        """Events should have sequential sequence numbers."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)
        sm.transition(Phase.EXPLORE, PhaseState.ACTIVE)

        assert sm.events[0].sequence_number == 1
        assert sm.events[1].sequence_number == 2
        assert sm.events[2].sequence_number == 3

    def test_event_listeners_notified(self):
        """Event listeners should be notified."""
        sm = PhaseStateMachine()
        received_events = []

        sm.add_event_listener(lambda e: received_events.append(e))
        sm.transition(Phase.ANALYZE, PhaseState.ACTIVE)

        assert len(received_events) == 1
        assert received_events[0].phase == Phase.ANALYZE

    def test_custom_events_can_be_emitted(self):
        """Custom events can be emitted."""
        sm = PhaseStateMachine()
        event = sm.emit_event(
            event_type="file_read",
            phase=Phase.EXPLORE,
            data={"file": "src/main.py", "lines": 100},
        )

        assert event.event_type == "file_read"
        assert event.data["file"] == "src/main.py"


class TestPhaseValidation:
    """P1 item 38: Phase validation."""

    def test_phase_has_started_at_when_active(self):
        """Phase should have started_at when activated."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)

        assert sm.phases[Phase.CLASSIFY].started_at is not None

    def test_phase_has_completed_at_when_done(self):
        """Phase should have completed_at when done."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)

        assert sm.phases[Phase.CLASSIFY].completed_at is not None

    def test_attempt_counter_increments(self):
        """Attempt counter should increment on each activation."""
        sm = PhaseStateMachine()
        sm.transition(Phase.TEST, PhaseState.ACTIVE)
        assert sm.phases[Phase.TEST].attempts == 1

        sm.transition(Phase.TEST, PhaseState.FAILED)
        sm.transition(Phase.TEST, PhaseState.ACTIVE)
        assert sm.phases[Phase.TEST].attempts == 2

    def test_max_attempts_tracked(self):
        """Max attempts should be tracked."""
        sm = PhaseStateMachine()
        assert sm.phases[Phase.TEST].max_attempts == 3

    def test_phase_result_can_be_set(self):
        """Phase result can be set."""
        sm = PhaseStateMachine()
        sm.transition(Phase.ANALYZE, PhaseState.ACTIVE)
        sm.set_phase_result(Phase.ANALYZE, {"findings": ["issue1", "issue2"]})

        assert sm.phases[Phase.ANALYZE].result["findings"] == ["issue1", "issue2"]

    def test_phase_error_can_be_set(self):
        """Phase error can be set."""
        sm = PhaseStateMachine()
        sm.transition(Phase.IMPLEMENT, PhaseState.ACTIVE)
        sm.set_phase_error(Phase.IMPLEMENT, "Compilation failed")

        assert sm.phases[Phase.IMPLEMENT].error == "Compilation failed"


class TestPhaseCompletionTracking:
    """P1 item 39: Phase completion tracking."""

    def test_is_complete_when_all_done(self):
        """is_complete should return True when all phases are done."""
        sm = PhaseStateMachine()

        # Complete all phases
        for phase in Phase:
            sm.transition(phase, PhaseState.ACTIVE)
            sm.transition(phase, PhaseState.COMPLETED)

        assert sm.is_complete()

    def test_is_complete_with_skipped_phases(self):
        """Skipped phases should count as complete."""
        sm = PhaseStateMachine()

        for phase in Phase:
            if phase in (Phase.IMPLEMENT, Phase.TEST):
                sm.transition(phase, PhaseState.SKIPPED)
            else:
                sm.transition(phase, PhaseState.ACTIVE)
                sm.transition(phase, PhaseState.COMPLETED)

        assert sm.is_complete()

    def test_not_complete_with_pending(self):
        """Not complete if any phase is PENDING."""
        sm = PhaseStateMachine()
        assert not sm.is_complete()

    def test_not_complete_with_active(self):
        """Not complete if any phase is ACTIVE."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        assert not sm.is_complete()

    def test_get_failed_phases(self):
        """Should return list of failed phases."""
        sm = PhaseStateMachine()
        sm.transition(Phase.TEST, PhaseState.ACTIVE)
        sm.transition(Phase.TEST, PhaseState.FAILED)
        sm.transition(Phase.VALIDATE, PhaseState.ACTIVE)
        sm.transition(Phase.VALIDATE, PhaseState.FAILED)

        failed = sm.get_failed_phases()
        assert Phase.TEST in failed
        assert Phase.VALIDATE in failed
        assert len(failed) == 2


class TestEventOrdering:
    """P1 item 40: Event ordering guarantees."""

    def test_events_ordered_by_sequence(self):
        """Events should be orderable by sequence number."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.emit_event("custom1", Phase.CLASSIFY)
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)
        sm.emit_event("custom2", Phase.EXPLORE)

        # Events should be in order
        for i in range(len(sm.events) - 1):
            assert sm.events[i].sequence_number < sm.events[i + 1].sequence_number

    def test_event_aggregator_sorts_events(self):
        """Event aggregator should sort events."""
        aggregator = EventAggregator()

        # Add events out of order
        aggregator.add_event(StructuredEvent("a", Phase.CLASSIFY, sequence_number=3))
        aggregator.add_event(StructuredEvent("b", Phase.EXPLORE, sequence_number=1))
        aggregator.add_event(StructuredEvent("c", Phase.ANALYZE, sequence_number=2))

        ordered = aggregator.get_events_in_order()
        assert ordered[0].sequence_number == 1
        assert ordered[1].sequence_number == 2
        assert ordered[2].sequence_number == 3

    def test_filter_events_by_type(self):
        """Should filter events by type."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.emit_event("file_read", Phase.EXPLORE, {"file": "a.py"})
        sm.emit_event("file_read", Phase.EXPLORE, {"file": "b.py"})
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)

        aggregator = EventAggregator()
        for e in sm.events:
            aggregator.add_event(e)

        file_reads = aggregator.get_events_by_type("file_read")
        assert len(file_reads) == 2

    def test_filter_events_by_phase(self):
        """Should filter events by phase."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.emit_event("progress", Phase.CLASSIFY, {"percent": 50})
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)
        sm.transition(Phase.EXPLORE, PhaseState.ACTIVE)

        aggregator = EventAggregator()
        for e in sm.events:
            aggregator.add_event(e)

        classify_events = aggregator.get_events_by_phase(Phase.CLASSIFY)
        assert len(classify_events) >= 2  # At least transition + progress


class TestPhaseOrdering:
    """P1 item 41: Phase ordering."""

    def test_phase_order_defined(self):
        """Phase order should be defined."""
        sm = PhaseStateMachine()
        assert len(sm.PHASE_ORDER) == len(Phase)

    def test_get_next_phase(self):
        """Should get next phase in order."""
        sm = PhaseStateMachine()

        assert sm.get_next_phase(Phase.CLASSIFY) == Phase.EXPLORE
        assert sm.get_next_phase(Phase.EXPLORE) == Phase.ANALYZE
        assert sm.get_next_phase(Phase.COMPLETE) is None

    def test_get_current_phase(self):
        """Should get currently active phase."""
        sm = PhaseStateMachine()

        assert sm.get_current_phase() is None

        sm.transition(Phase.ANALYZE, PhaseState.ACTIVE)
        assert sm.get_current_phase() == Phase.ANALYZE


class TestTransitionHistory:
    """P1 item 42: Transition history."""

    def test_transitions_recorded(self):
        """Transitions should be recorded."""
        sm = PhaseStateMachine()
        sm.transition(Phase.CLASSIFY, PhaseState.ACTIVE)
        sm.transition(Phase.CLASSIFY, PhaseState.COMPLETED)

        assert len(sm.transitions) == 2

    def test_transition_has_from_and_to(self):
        """Transition should record from and to states."""
        sm = PhaseStateMachine()
        sm.transition(Phase.EXPLORE, PhaseState.ACTIVE)

        t = sm.transitions[0]
        assert t.from_state == PhaseState.PENDING
        assert t.to_state == PhaseState.ACTIVE

    def test_transition_has_timestamp(self):
        """Transition should have timestamp."""
        sm = PhaseStateMachine()
        sm.transition(Phase.PLAN, PhaseState.ACTIVE)

        assert sm.transitions[0].timestamp is not None

    def test_transition_has_reason(self):
        """Transition should record reason."""
        sm = PhaseStateMachine()
        sm.transition(Phase.IMPLEMENT, PhaseState.SKIPPED, reason="Read-only mode")

        assert sm.transitions[0].reason == "Read-only mode"


class TestBlockedState:
    """P1 item 43: Blocked state handling."""

    def test_pending_to_blocked_allowed(self):
        """Should allow PENDING to BLOCKED transition."""
        sm = PhaseStateMachine()
        assert sm.can_transition(Phase.IMPLEMENT, PhaseState.BLOCKED)
        sm.transition(Phase.IMPLEMENT, PhaseState.BLOCKED, "Missing dependency")

    def test_blocked_to_pending_allowed(self):
        """Should allow BLOCKED to PENDING transition (unblock)."""
        sm = PhaseStateMachine()
        sm.transition(Phase.TEST, PhaseState.BLOCKED)
        assert sm.can_transition(Phase.TEST, PhaseState.PENDING)
        sm.transition(Phase.TEST, PhaseState.PENDING, "Dependency resolved")

    def test_blocked_to_skipped_allowed(self):
        """Should allow BLOCKED to SKIPPED transition."""
        sm = PhaseStateMachine()
        sm.transition(Phase.VALIDATE, PhaseState.BLOCKED)
        assert sm.can_transition(Phase.VALIDATE, PhaseState.SKIPPED)


class TestPhaseInfo:
    """P1 item 44: Phase info dataclass."""

    def test_phase_info_defaults(self):
        """PhaseInfo should have correct defaults."""
        info = PhaseInfo(phase=Phase.CLASSIFY)

        assert info.state == PhaseState.PENDING
        assert info.started_at is None
        assert info.completed_at is None
        assert info.error is None
        assert info.result is None
        assert info.attempts == 0
        assert info.max_attempts == 3

    def test_phase_info_in_state_machine(self):
        """State machine should track PhaseInfo for each phase."""
        sm = PhaseStateMachine()

        for phase in Phase:
            assert phase in sm.phases
            assert sm.phases[phase].phase == phase


class TestEventDataIntegrity:
    """P1 item 45: Event data integrity."""

    def test_event_data_preserved(self):
        """Event data should be preserved."""
        sm = PhaseStateMachine()
        sm.emit_event(
            "analysis_result",
            Phase.ANALYZE,
            {"findings": ["a", "b"], "count": 2},
        )

        event = sm.events[-1]
        assert event.data["findings"] == ["a", "b"]
        assert event.data["count"] == 2

    def test_event_has_timestamp(self):
        """Events should have timestamps."""
        sm = PhaseStateMachine()
        sm.emit_event("test", Phase.TEST, {})

        assert sm.events[-1].timestamp is not None

    def test_empty_data_is_dict(self):
        """Empty data should be empty dict, not None."""
        event = StructuredEvent("test", Phase.CLASSIFY)
        assert event.data == {}
        assert isinstance(event.data, dict)

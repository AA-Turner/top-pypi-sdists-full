"""Session v1 read projection for the Vibe Agents remote transport.

Two things a future editor must not break.

It keeps every Turn, not only the latest, because the transport serves a paginated Turn
list. And the session it reports starts non-terminal even when the product row is already
finished: ``read_events`` stops as soon as the session reads terminated, so a terminal
fallback would end the stream before replaying anything. The true product snapshot is kept
aside for :meth:`reconcile_product_snapshot`, which applies it once the replay is done.

Only part of the canonical event set reaches a reader. vibe_agents serves history-entry,
turn, session-updated and callback events for a v1 session, and skips notices, errors and
session termination (``_PUBLIC_SESSION_V1_PAYLOAD_TYPES`` in the control plane's
``to_public_events``). A reported callback is answerable: the Host publishes the id its
answer route accepts, and ``resolved_callback_ids`` reports the resolution that
acknowledges the answer.

A Turn is listed as soon as the user message that started it is, not only from its own
events. The Runtime publishes ``turn_started`` once the ``pre_agent_turn`` Hook has decided,
but the Workflow publishes the message, with its Turn id, when the Runtime admits it. Until the
Turn's own events arrive, the projection lists that Turn as running, so a read during the Hook
finds the Turn that ``send_message`` or ``start_turn`` named. No event is relayed for it
until it ends. A Session that ends before the Turn starts ends it like a started Turn, with the
Session's termination, whether the product row or the stream reports the end. Only a Turn
whose message ``send_message`` was refused is not listed: the Workflow may have published the
message of one it refused because the Session was stopping. The transport names those Turns.
"""

from collections.abc import Set

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe_agents.sessions_client import AgentSessionResponse, ObservedControllerEventResponse
from mistralai.vibe_agents.sessions_client.rendered_session_v1 import RenderedSessionV1, parse_session_v1_event

from .event_ids import _EMPTY_CURSOR, _encode_event_id
from .product_session import build_session_from_product

# What the projection relays: a canonical event, or one this SDK has no model for, as it came.
type RelayedPayload = harness_session.SessionEvent | harness_session.UnknownEventPayload

_TURN_EVENTS = (
    harness_session.TurnStartedEvent,
    harness_session.TurnUpdatedEvent,
    harness_session.TurnTerminatedEvent,
)
# A Turn is live until it terminates. `blocked` is live too: the Session is waiting on a
# callback, not finished with the Turn.
_LIVE_TURN_STATUSES = frozenset({"running", "blocked"})


class VibeAgentsSessionV1Projection:
    """Accumulate a Session v1 ``/events`` stream into the Harness session view."""

    def __init__(
        self,
        product_session: AgentSessionResponse,
        *,
        refused_turn_ids: Set[str] = frozenset(),
    ) -> None:
        self.product_session = product_session
        self.product_cursor: str | None = None
        self.rendered = RenderedSessionV1()
        self.turns: dict[str, harness_session.TurnState] = {}
        # The `emittedAt` of the frame `apply` last accepted. The transport stamps relayed
        # events with it, so a v1 event keeps the time the server gave it instead of being
        # dated from whenever the session was last updated.
        self.last_emitted_at: int | None = None
        self._seen_sequences: set[str] = set()
        # The Turn a user message named that the stream has not started yet, listed as running.
        self._unstarted_turn_id: str | None = None
        # Turns of messages `send_message` was refused, shared with the transport that learns them.
        self._refused_turn_ids = refused_turn_ids
        # The events a frame yields beyond the one `apply` returns, drained by `take_pending_events`.
        self._pending_events: list[harness_session.SessionEvent] = []
        self._product_session_snapshot = build_session_from_product(product_session)
        self._fallback_session = self._product_session_snapshot
        if self._fallback_session.status == "terminated":
            self._fallback_session = self._fallback_session.model_copy(
                update={"status": "running", "termination": None}
            )

    @property
    def session(self) -> harness_session.Session:
        """What the stream reported, or a non-terminal view of the product row before that."""

        if self.rendered.session is not None:
            return self.rendered.session
        return self._fallback_session

    @property
    def resolved_callback_ids(self) -> set[str]:
        """Callback ids the stream reported resolved: a caller waits here for its answer to be taken."""

        return self.rendered.resolved_callback_ids

    @property
    def history(self) -> list[harness_session.HistoryEntry]:
        return self.rendered.entries

    @property
    def active_turn_id(self) -> str | None:
        """The live Turn, searched newest first because that is where it almost always is."""

        for turn in reversed(self.turns.values()):
            if turn.status in _LIVE_TURN_STATUSES:
                return turn.id
        return None

    def has_seen(self, sequence: str) -> bool:
        """Whether ``apply`` already took the frame at ``sequence``."""

        return sequence in self._seen_sequences

    def apply(self, observed: ObservedControllerEventResponse) -> RelayedPayload | None:
        """Fold one product frame and return the canonical event it carries.

        A ``session_updated`` that terminates the Session also ends its live Turns. It then
        returns nothing and queues the Turn terminations, followed by the event itself, for
        :meth:`take_pending_events`: a Turn's termination reads the Session as waiting, so it
        must come before the event that terminates the Session.
        """

        sequence = observed.sequence
        if sequence in self._seen_sequences:
            self.product_cursor = sequence
            return None
        self._seen_sequences.add(sequence)
        previous_cursor = self.product_cursor
        self.product_cursor = sequence

        parsed = parse_session_v1_event(observed.event)
        if parsed is None:
            # A frame this SDK cannot parse is dropped rather than raised on: each event stands
            # alone, so skipping one keeps the rest of the session readable.
            self.rendered.invalid_frame_count += 1
            return None
        self.rendered.apply_parsed_event(parsed)
        self.last_emitted_at = parsed.emitted_at
        payload = parsed.payload
        if isinstance(payload, harness_session.UnknownEventPayload):
            # A newer server may send an event this SDK has no model for. It is relayed as it
            # came: the raw protocol client yields it, and the typed event stream gives an
            # UnknownEvent for a new type and leaves out a known type with newer content.
            return payload
        if isinstance(payload, harness_session.HistoryEntryPatchedEvent) and not self.rendered.holds_entry(
            payload.entry_id
        ):
            # The entry's own frame was skipped as unreadable, so the caller never got the
            # entry and would reject a patch to it as out of sequence.
            return None
        if isinstance(payload, harness_session.HistoryEntryAddedEvent):
            self._list_turn_of_user_message(payload.entry)
        if isinstance(payload, harness_session.SessionUpdatedEvent) and payload.session.status == "terminated":
            # The control plane appends one when an ended Session is renamed or archived.
            terminated = self._terminate_live_turns(payload.session)
            if terminated:
                self._pending_events = [*terminated, payload]
                return None
        if isinstance(payload, _TURN_EVENTS):
            if payload.turn.id == self._unstarted_turn_id:
                self._unstarted_turn_id = None
            elif isinstance(payload, harness_session.TurnStartedEvent):
                self._drop_unstarted_turn()
            turn = self._with_start(payload, previous_cursor)
            self.turns[turn.id] = turn
            # The stream gives the same Turn as reads do, its start position included.
            return payload.model_copy(update={"turn": turn})
        return payload

    def _with_start(
        self,
        payload: harness_session.TurnStartedEvent
        | harness_session.TurnUpdatedEvent
        | harness_session.TurnTerminatedEvent,
        previous_cursor: str | None,
    ) -> harness_session.TurnState:
        """The Turn with its start position: the frame before its start, kept by its updates."""

        turn = payload.turn
        if turn.started_after_event_id is not None:
            return turn
        start: str | None
        if isinstance(payload, harness_session.TurnStartedEvent):
            start = _EMPTY_CURSOR if previous_cursor is None else _encode_event_id(previous_cursor)
        else:
            known = self.turns.get(turn.id)
            start = None if known is None else known.started_after_event_id
        return turn if start is None else turn.model_copy(update={"started_after_event_id": start})

    def _list_turn_of_user_message(self, entry: harness_session.HistoryEntry) -> None:
        """List the Turn a user message started as running until the stream starts it."""

        if not isinstance(entry, harness_session.MessageHistoryEntry) or entry.role != "user":
            return
        turn_id = entry.turn_id
        if turn_id is None or turn_id in self.turns or turn_id in self._refused_turn_ids:
            # A message that joins a Turn the stream already reported changes nothing.
            return
        self._drop_unstarted_turn()
        self.turns[turn_id] = harness_session.TurnState(id=turn_id, status="running")
        self._unstarted_turn_id = turn_id

    def drop_refused_turn(self) -> None:
        """Stop listing the unstarted Turn if the transport has since learned its message was refused."""

        if self._unstarted_turn_id in self._refused_turn_ids:
            self._drop_unstarted_turn()

    def _drop_unstarted_turn(self) -> None:
        """Stop listing the unstarted Turn: it will never start.

        Called when another Turn started or another message named a new Turn (while a Hook
        decides, the Session admits no other message), and when its message was refused.
        """

        if self._unstarted_turn_id is not None:
            del self.turns[self._unstarted_turn_id]
            self._unstarted_turn_id = None

    def take_pending_events(self) -> list[harness_session.SessionEvent]:
        """The events the last frame yielded beyond the one ``apply`` returned.

        Only a ``session_updated`` that terminates the Session with live Turns yields more than
        one: see :meth:`apply`.
        """

        pending, self._pending_events = self._pending_events, []
        return pending

    def state(self) -> harness_session.SessionState:
        session = self.session
        if self._unstarted_turn_id is not None and session.status == "waiting":
            # The stream reports the Session running once the Turn starts; the read lists it now.
            session = session.model_copy(update={"status": "running"})
        return harness_session.SessionState(
            session=session,
            active_turn_id=self.active_turn_id,
            history=harness_session.Page(items=list(self.history)),
            turns=harness_session.Page(items=list(self.turns.values())),
            active_callbacks=list(self.rendered.active_callbacks.values()),
        )

    def adopt_terminal_product(self, product: AgentSessionResponse) -> list[harness_session.TurnTerminatedEvent]:
        """Terminate the session from a freshly read product row.

        Session v1 never publishes ``session_terminated`` on read, deliberately, so a reader
        that waited for one would wait forever. The product row is the terminal signal, and it
        may have turned terminal after this projection was built, hence the fresh row.
        """

        self._product_session_snapshot = build_session_from_product(product)
        return self.reconcile_product_snapshot()

    def reconcile_product_snapshot(self) -> list[harness_session.TurnTerminatedEvent]:
        """Adopt a terminal product row the stream never reported.

        A Session can end without publishing an event (a Temporal timeout, an operator
        terminate), and v1 does not serve ``session_terminated`` on read at all, so the
        product row is the only place a termination shows up.

        Returns a ``TurnTerminatedEvent`` for each live Turn this terminates, including a Turn
        listed from its message that has not started, unless the transport learned that its
        message was refused: that one is no longer listed. An event reader relays them: a
        caller following that Turn would otherwise see the stream end without its outcome, and
        a failed Session would surface as a bare stream error instead of its failure. A
        snapshot read has no stream to relay them on and ignores them.
        """

        if not self._closed_by(self._product_session_snapshot):
            return []
        self.rendered.session = self._product_session_snapshot
        return self._terminate_live_turns(self._product_session_snapshot)

    def state_with_product(
        self, product: AgentSessionResponse
    ) -> tuple[harness_session.SessionState, list[harness_session.TurnTerminatedEvent]]:
        """The read state, closed by a terminal product row the stream has not reported.

        Returns the Turn terminations the closure adds, as :meth:`reconcile_product_snapshot`
        does. Unlike it, this leaves the projection as the stream built it, so the reader that
        keeps folding frames into it is not handed a closure it never observed. The rest of
        the Session comes from the stream: a rename or an archive is published in the same
        transaction that writes the row, so the stream is never behind a row read before it.
        """

        snapshot = build_session_from_product(product)
        if not self._closed_by(snapshot):
            return self.state(), []
        turns, terminated = _close_live_turns(self.turns, snapshot)
        state = self.state().model_copy(
            update={
                "session": snapshot,
                "active_turn_id": None,
                "turns": harness_session.Page(items=list(turns.values())),
            }
        )
        return state, terminated

    def _closed_by(self, snapshot: harness_session.Session) -> bool:
        # Compared against what the stream reported, not against `session`: that property
        # falls back to the product row, so reading it here would always look like agreement.
        if snapshot.status != "terminated":
            return False
        return self.rendered.session is None or self.rendered.session.status != "terminated"

    def _terminate_live_turns(self, session: harness_session.Session) -> list[harness_session.TurnTerminatedEvent]:
        """End every live Turn, started or not, with the termination of the ended Session.

        A Turn whose message the transport learned was refused is no longer listed instead.
        """

        self.drop_refused_turn()
        self.turns, terminated = _close_live_turns(self.turns, session)
        # It has ended: a later message must not drop it as a Turn that will never start.
        self._unstarted_turn_id = None
        return terminated


def _close_live_turns(
    turns: dict[str, harness_session.TurnState],
    session: harness_session.Session,
) -> tuple[dict[str, harness_session.TurnState], list[harness_session.TurnTerminatedEvent]]:
    """The Turns with every live one ended by the ended Session, and the terminations that adds."""

    termination = session.termination or harness_session.CancelledTermination(
        reason="Remote Session terminated without reporting the Turn",
    )
    closed = dict(turns)
    terminated: list[harness_session.TurnTerminatedEvent] = []
    for turn_id, turn in turns.items():
        if turn.status in _LIVE_TURN_STATUSES:
            closed[turn_id] = turn.model_copy(
                update={"status": "terminated", "completed_at": session.updated_at, "termination": termination}
            )
            terminated.append(harness_session.TurnTerminatedEvent(turn=closed[turn_id]))
    return closed, terminated


__all__ = ["VibeAgentsSessionV1Projection"]

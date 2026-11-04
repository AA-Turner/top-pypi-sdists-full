"""The state of the attention in a chat («estado de la atención en el chat»): the port of `atencion_en_chat` (api-chatty
`docs/atencion/estado-en-el-chat.md`).

One document per chat (unique index on `chat_id`). Only the attention runtime writes it; cintia-lambdas reads it straight
from Mongo, so the stored shape never changes. What the attention flow decided for the chat (the reason, who keeps it on
escalation, the AI's state and its turn) and the marks of what already happened once (the first reply to the reason,
the reply to a follow-up, the rebuild of the fixed chain, the message on handing over, who cut the follow-ups).

The port takes and answers these models, never the stored document: only the Mongo adapter knows the stored names
(Spanish), `_id` and the stored order. A read answers an `AttentionInChat` with only what it read (the projection of
`main`): a field it did not read is `ABSENT`, which is not `None` (a stored `None`).

One value is a payload and not fields (ADR-013, «Excepciones»): `ai` (`AiOnReason`, with its `AiResult`) is the
contract v1 with cintia-lambdas, whose keys and their order come from the reason's configuration and `ai_state`. It is
kept as it is, in its order, with read-only accessors; who writes it builds it (`ai_state`), as in `main`. A closed value stored with another shape than the one `main` writes (a key it does not write, another
order, not a mapping) is kept as `StoredAsIs`, verbatim: a read never fails on it and a write puts it back as it was.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterator, List, Mapping, Optional, Protocol, Tuple, Union


class _Absent:
    """Not read (outside the projection) or not stored: not the same as a stored `None`."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "ABSENT"

    def __bool__(self) -> bool:
        return False

    def __deepcopy__(self, memo):
        return self


ABSENT: Any = _Absent()


class _Unchanged:
    """`set_ai_follow_ups(..., fixed_chain=UNCHANGED)`: the fixed chain is not touched."""

    def __repr__(self) -> str:
        return "UNCHANGED"


UNCHANGED: Any = _Unchanged()

#: The changes of reason the AI made that a chat keeps (the last ones).
REASON_CHANGES_KEPT = 10


class Payload(Mapping[str, Any]):
    """A value kept as it was given or stored: its keys, their order and nested values. Immutable; `as_dict()` is a
    deep copy."""

    __slots__ = ("_data",)

    def __init__(self, data: Mapping[str, Any]):
        self._data = copy.deepcopy(dict(data))

    def __getitem__(self, key: str) -> Any:
        return copy.deepcopy(self._data[key])

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def as_dict(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data)

    def __eq__(self, other: object) -> bool:
        return type(other) is type(self) and list(self._data.items()) == list(other._data.items())  # type: ignore

    def __hash__(self) -> int:
        return id(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._data!r})"


class AiOnReason(Payload):
    """The AI's state on the reason (`ia`): the contract v1 with cintia-lambdas."""

    @property
    def state(self) -> Optional[str]:
        return self._data.get("estado")

    @property
    def turn_id(self) -> Optional[str]:
        return self._data.get("turno_id")

    @property
    def pending(self) -> Any:
        return self._data.get("pendiente")

    @property
    def sweep_attempts(self) -> Any:
        return self._data.get("barrido_intentos")

    @property
    def created_at(self) -> Any:
        return self._data.get("creado_at")

    @property
    def expires_at(self) -> Any:
        return self._data.get("vence_at")


class AiResult(Payload):
    """How the AI's turn ended (`ia.resultado`): what CINTIA reported, or why api-chatty closed it."""


class StoredAsIs(Payload):
    """A closed value stored with a shape `main` never writes: kept and written back verbatim."""

    def __init__(self, data: Any):  # noqa: D401 - any stored value, not only a mapping
        self._data = copy.deepcopy(data)

    def __iter__(self):
        return iter(self._data) if isinstance(self._data, Mapping) else iter(())

    def __len__(self) -> int:
        return len(self._data) if isinstance(self._data, Mapping) else 0

    def __getitem__(self, key: str) -> Any:
        return copy.deepcopy(self._data[key])

    @property
    def value(self) -> Any:
        return copy.deepcopy(self._data)


@dataclass(frozen=True)
class AssignOnEscalation:
    """Who keeps the chat when the AI escalates (`asignar_al_escalar`): the reason's `Asignacion` (`mode` nobody / fixed
    / round robin, the person or the team)."""
    mode: Any = ABSENT
    user_id: Any = ABSENT
    business_area_id: Any = ABSENT


@dataclass(frozen=True)
class ReasonReplyMark:
    """The fixed «if they reply» actions of the reason (or branch) wait for the client's first reply: `key` of the
    block, from `since` (an outgoing after it is the reason's reply) until `expires_at`; `applied_at` once claimed."""
    key: Any
    reason_id: Any
    since: Any
    expires_at: Any
    applied_at: Any = ABSENT


@dataclass(frozen=True)
class PersonRequest:
    """The client asked for a person (`by`: a phrase or the classifier)."""
    by: Any
    at: Any


@dataclass(frozen=True)
class AiFollowUps:
    """The AI follow-ups of the reason: the strategy and its key, or the block's own AI chain (`own`, with the agent
    that writes them when the AI does not stay)."""
    follow_up_strategy_id: Any = ABSENT
    key: Any = ABSENT
    own: Any = ABSENT
    agent_id: Any = ABSENT


@dataclass(frozen=True)
class FixedFollowUpChain:
    """The fixed chain the entry left for the chat; `rebuilt_by` is the incoming that last rebuilt it."""
    key: Any
    reason_id: Any = ABSENT
    rebuilt_at: Any = ABSENT
    rebuilt_by: Any = ABSENT


@dataclass(frozen=True)
class FollowUpsCut:
    """Who cut the follow-ups (`by`: one of `CUT_BY`)."""
    by: Any
    user_id: Any
    at: Any


@dataclass(frozen=True)
class EscalationMark:
    """The reason assigned on escalation a chat that had the AI (to ignore CINTIA's late release)."""
    mode: Any
    user_id: Any = ABSENT
    at: Any = ABSENT


@dataclass(frozen=True)
class HandOverMessageMark:
    """The «message on handing over» was claimed for this escalation (`key` = CINTIA's execution)."""
    key: Any
    at: Any


@dataclass(frozen=True)
class ReasonChange:
    """A change of reason the AI made."""
    at: Any
    from_reason_id: Any
    to_reason_id: Any
    turn_id: Any


Closed = Union[AssignOnEscalation, ReasonReplyMark, PersonRequest, AiFollowUps, FixedFollowUpChain, FollowUpsCut, EscalationMark,
               HandOverMessageMark, ReasonChange, StoredAsIs]


@dataclass(frozen=True)
class AttentionInChat:
    """The document of a chat, with only what was read: a field outside the read is `ABSENT`."""
    id: Any = ABSENT
    chat_id: Any = ABSENT
    company_id: Any = ABSENT
    reason_id: Any = ABSENT
    entered_at: Any = ABSENT
    created_at: Any = ABSENT
    updated_at: Any = ABSENT
    assign_on_escalation: Union[AssignOnEscalation, StoredAsIs, None, Any] = ABSENT
    ai: Union[AiOnReason, StoredAsIs, None, Any] = ABSENT
    reason_reply: Union[ReasonReplyMark, StoredAsIs, None, Any] = ABSENT
    person_request: Union[PersonRequest, StoredAsIs, None, Any] = ABSENT
    ai_follow_ups: Union[AiFollowUps, StoredAsIs, None, Any] = ABSENT
    fixed_chain: Union[FixedFollowUpChain, StoredAsIs, None, Any] = ABSENT
    cut: Union[FollowUpsCut, StoredAsIs, None, Any] = ABSENT
    escalation: Union[EscalationMark, StoredAsIs, None, Any] = ABSENT
    hand_over_message: Union[HandOverMessageMark, StoredAsIs, None, Any] = ABSENT
    reason_changes: Union[Tuple[Union[ReasonChange, StoredAsIs], ...], StoredAsIs, None, Any] = ABSENT
    follow_up_reply_id: Any = ABSENT
    follow_up_reply_at: Any = ABSENT
    #: Stored fields this version does not know, by their stored name, as they are.
    others: Mapping[str, Any] = field(default_factory=dict)


class AttentionInChatRepository(Protocol):
    """The state of the attention of each chat. By `chat_id` (the unique index) unless the method takes the company:
    `main`'s filters, which this port keeps (ADR-013 §5.5)."""

    async def record_entry(self, company_id: str, chat_id: str, *, reason_id: Optional[str],
                           assign_on_escalation: Optional[AssignOnEscalation], ai: Optional[AiOnReason],
                           now: datetime, clear_reason_reply: bool = True) -> None:
        """What this entry decided, over the previous one (creates the document); without the reason reply mark unless
        `clear_reason_reply` is False."""
        ...

    async def mark_reason_reply(self, company_id: str, chat_id: str, mark: Optional[ReasonReplyMark],
                                now: datetime) -> None:
        """Sets the reason reply mark (creates the document) or clears it (`None`, does not create one)."""
        ...

    async def claim_reason_reply(self, chat_id: str, *, arrived_at: datetime, last_outgoing_at: datetime,
                                 now: datetime) -> Optional[ReasonReplyMark]:
        """Atomic: applies the mark only if nobody did, the reason's reply went out after `since` and the incoming
        arrived by `expires_at`; answers the mark as it was, or None."""
        ...

    async def hand_over_ai(self, chat_id: str, turn_id: str, new: AiOnReason, *, now: datetime
                           ) -> Optional[AttentionInChat]:
        """Replaces the AI's state only if it was active with this turn; answers the document's id, or None."""
        ...

    async def mark_person_request(self, company_id: str, chat_id: str, *, by: str, now: datetime) -> None:
        """The client asked for a person (creates the document)."""
        ...

    async def put_ai(self, chat_id: str, *, ai: Optional[AiOnReason],
                     assign_on_escalation: Optional[AssignOnEscalation], now: datetime) -> None:
        """A new state for the AI, without touching the reason (does not create a document)."""
        ...

    async def of_the_company(self, company_id: str, since: datetime, limit: int,
                             until: Optional[datetime] = None) -> List[AttentionInChat]:
        """A page of the company's documents written in [since, until), newest first: chat, AI, AI follow-ups and when."""
        ...

    async def read(self, chat_id: str) -> Optional[AttentionInChat]:
        """The whole document, or None."""
        ...

    async def current_ai(self, company_id: str, chat_id: str, turn_id: str) -> Optional[AttentionInChat]:
        """The whole document, only if it is of the company and the AI is active with this turn."""
        ...

    async def close_ai(self, chat_id: str, turn_id: str, *, now: datetime, result: Optional[AiResult] = None,
                       clear_assignment: bool = False) -> Optional[AttentionInChat]:
        """Finishes the AI's state only if it was active with this turn; answers the whole document before, or None."""
        ...

    async def claim_reason_change(self, company_id: str, chat_id: str, turn_id: str, *, from_reason_id: Optional[str],
                                  to_reason_id: str, now: datetime, limit: int, since: datetime
                                  ) -> Optional[AttentionInChat]:
        """Atomic: with the AI active on this turn and fewer than `limit` changes by the AI since `since`, closes the
        state and records the change (the last `REASON_CHANGES_KEPT`); answers id and reason before, or None."""
        ...

    async def set_ai_follow_ups(self, company_id: str, chat_id: str, value: Optional[AiFollowUps], now: datetime, *,
                                fixed_chain: Any = UNCHANGED) -> Union[AiFollowUps, StoredAsIs, None]:
        """The AI follow-ups (and, if given, the fixed chain in the same write); creates the document unless it only
        clears. Answers the AI follow-ups before."""
        ...

    async def claim_follow_up_reply(self, company_id: str, chat_id: str, follow_up_id: str, now: datetime) -> bool:
        """Atomic: True for the one reply that applies «if they reply» of this follow-up (the unique index decides)."""
        ...

    async def ai_follow_ups(self, chat_id: str) -> Union[AiFollowUps, StoredAsIs, None]:
        ...

    async def fixed_chain(self, chat_id: str) -> Union[FixedFollowUpChain, StoredAsIs, None]:
        ...

    async def claim_rebuild(self, chat_id: str, incoming_id: str, now: datetime) -> bool:
        """Atomic: True for the one outgoing that rebuilds the fixed chain after this incoming (no document created)."""
        ...

    async def drop_fixed_chain(self, chat_id: str, now: datetime) -> None:
        ...

    async def mark_cut(self, company_id: str, chat_id: str, *, by: str, user_id: Optional[str], now: datetime) -> None:
        """Who cut the follow-ups (no document created)."""
        ...

    async def drop_fixed_chains_of_the_company(self, company_id: str) -> int:
        """Every fixed chain of the company (without touching `updated_at`); answers how many."""
        ...

    async def mark_escalation(self, chat_id: str, mark: EscalationMark) -> None:
        """No document created."""
        ...

    async def claim_hand_over_message(self, chat_id: str, key: str, now: datetime) -> Optional[bool]:
        """True: it is the caller's; False: already claimed with this key; None: the chat has no document."""
        ...

    async def release_hand_over_message(self, chat_id: str, key: str) -> None:
        ...

    async def escalation(self, chat_id: str) -> Union[EscalationMark, StoredAsIs, None]:
        ...

    async def clear_assignment(self, chat_id: str, now: datetime) -> Union[AiFollowUps, StoredAsIs, None]:
        """Without who keeps it on escalation nor AI follow-ups (no document created); answers the AI follow-ups
        before."""
        ...

    async def mark_after_turn(self, chat_id: str, turn_id: str, *, done: Mapping[str, Any], complete: bool,
                              now: datetime) -> None:
        """What the post-lock task already did, as keys of the AI's payload (`ia_puesta_at`, `turno_pedido_at`; any
        other key is written too, as in `main`), only while the AI with this turn is pending."""
        ...

    async def pending_after_turn(self, cutoff: datetime, limit: int) -> List[AttentionInChat]:
        """Of every company: active states whose post-lock task did not finish, created by `cutoff`, oldest first."""
        ...

    async def take_for_sweep(self, chat_id: str, turn_id: str, *, attempts_seen: int, now: datetime
                             ) -> Optional[AttentionInChat]:
        """Atomic: one more attempt only if the counter is still `attempts_seen`; answers the document after, or None."""
        ...

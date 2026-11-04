"""Contracts: the registry of every shared record, the vocabularies their fields use, the
product-analytics event catalog and the client-message vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel

from .analytics import EventCatalog
from .client_messages import (
    Action,
    Audience,
    ClientMessage,
    ClientMessageList,
    ClientRefusalBody,
    MessageCode,
    Severity,
)
from .records import (
    AnchorLevel,
    Artifact,
    ArtifactStatus,
    Experiment,
    LineageEntityType,
    LineageRelation,
    MetricPoint,
    ParentRelation,
    Project,
    ProjectKind,
    Record,
    Run,
    RunCounts,
    RunStatus,
    Span,
)
from .settings import SetBy, SettingKey
from .transcript_switch import SwitchedBy, TranscriptState


@dataclass(frozen=True)
class Contracts:
    """What codegen turns into every client's types, in the order it writes them."""

    #: The domain concepts, one class each.
    records: tuple[type[Record], ...]
    #: Plain models a record's field holds (`Run.counts`); written before the records.
    nested: tuple[type[BaseModel], ...]
    #: The closed vocabularies, written first.
    enums: tuple[type[Enum], ...]
    #: Every product-analytics event; each runtime's `Event` enum is drawn from it.
    events: EventCatalog
    #: What the server tells a client (client_messages/), enums first: its own generated files,
    #: so the stdlib-only tap and hooks get a copy.
    messages: tuple[type, ...] = ()
    #: Whether sessions upload as transcripts, and who turned them off (transcript_switch/).
    transcript_switch: tuple[type[Enum], ...] = ()
    #: The settings file's keys and writers (settings/).
    settings: tuple[type[Enum], ...] = ()


CONTRACTS = Contracts(
    records=(Run, Experiment, Project, Artifact, MetricPoint, Span),
    nested=(RunCounts,),
    enums=(
        RunStatus,
        ParentRelation,
        ProjectKind,
        ArtifactStatus,
        AnchorLevel,
        LineageEntityType,
        LineageRelation,
    ),
    events=EventCatalog.load(),
    messages=(Severity, Action, Audience, MessageCode, ClientMessage, ClientRefusalBody, ClientMessageList),
    transcript_switch=(TranscriptState, SwitchedBy),
    settings=(SettingKey, SetBy),
)

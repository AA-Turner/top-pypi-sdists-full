"""Contracts: the registry of every shared record, the vocabularies their fields use, the
product-analytics event and surface catalogs, the client-message vocabulary and the pin kinds."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel

from .analytics import EventCatalog, SurfaceCatalog
from .client_messages import (
    Action,
    Audience,
    ClientMessage,
    ClientMessageList,
    ClientRefusalBody,
    MessageCode,
    Severity,
)
from .pane_api import PaneApi
from .pins import Pins
from .records import (
    AnchorLevel,
    Artifact,
    ArtifactStatus,
    Command,
    CommandAnswer,
    CommandAsk,
    CommandClaim,
    CommandData,
    CommandKind,
    CommandState,
    EditActorKind,
    EditCounts,
    EditOp,
    EditPhase,
    EditState,
    EditTarget,
    Experiment,
    LineageEntityType,
    LineageRelation,
    MetricPoint,
    MoveSeriesArgs,
    ParentRelation,
    Project,
    ProjectKind,
    Record,
    RenameArgs,
    RevertArgs,
    Run,
    RunCounts,
    RunEdit,
    RunStatus,
    RunType,
    ScaleArgs,
    SetConfigArgs,
    ShiftStepArgs,
    ShiftTimeArgs,
    Span,
    WatchArgs,
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
    #: Every `surface` an event may carry; each runtime's `ProductSurface` enum is drawn from it.
    surfaces: SurfaceCatalog
    #: What the server tells a client (client_messages/), enums first: its own generated files,
    #: so the stdlib-only tap and hooks get a copy.
    messages: tuple[type, ...] = ()
    #: Whether sessions upload as transcripts, and who turned them off (transcript_switch/).
    transcript_switch: tuple[type[Enum], ...] = ()
    #: The settings file's keys and writers (settings/).
    settings: tuple[type[Enum], ...] = ()
    #: What a pane's code may call and its caps (pane_api/).
    pane_api: PaneApi | None = None
    #: What a project's Pinned area can hold (pins/).
    pins: Pins | None = None


CONTRACTS = Contracts(
    records=(Run, Experiment, Project, Artifact, MetricPoint, Span, RunEdit, Command),
    # An edit's target, counts and each op's arguments (records/edit.py; HideArgs has no fields); a command's
    # arguments, ask, claim and answer bodies and its live notice (records/command.py; CancelArgs and RetryArgs
    # have no fields).
    nested=(
        RunCounts,
        EditTarget,
        EditCounts,
        ShiftStepArgs,
        ShiftTimeArgs,
        ScaleArgs,
        RenameArgs,
        MoveSeriesArgs,
        SetConfigArgs,
        RevertArgs,
        WatchArgs,
        CommandAsk,
        CommandClaim,
        CommandAnswer,
        CommandData,
    ),
    enums=(
        RunStatus,
        RunType,
        ParentRelation,
        ProjectKind,
        ArtifactStatus,
        AnchorLevel,
        LineageEntityType,
        LineageRelation,
        EditOp,
        EditState,
        EditPhase,
        EditActorKind,
        CommandKind,
        CommandState,
    ),
    events=EventCatalog.load(),
    surfaces=SurfaceCatalog.load(),
    messages=(Severity, Action, Audience, MessageCode, ClientMessage, ClientRefusalBody, ClientMessageList),
    transcript_switch=(TranscriptState, SwitchedBy),
    settings=(SettingKey, SetBy),
    pane_api=PaneApi.load(),
    pins=Pins.load(),
)

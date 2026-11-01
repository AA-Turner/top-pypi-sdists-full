"""Contracts: the registry of every shared record, the vocabularies their fields use and the
product-analytics event catalog."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel

from .analytics import EventCatalog
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
)

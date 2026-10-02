r"""Contain all ingestors."""

from __future__ import annotations

__all__ = [
    "BaseIngestor",
    "DataclassIngestor",
    "FirstNIngestor",
    "InMemoryIngestor",
    "LastNIngestor",
    "MappingIngestor",
    "PickleIngestor",
    "ProcessorIngestor",
    "ShuffleIngestor",
    "TextIngestor",
    "resolve_ingestor",
]

from zenpyre.ingestors.base import BaseIngestor
from zenpyre.ingestors.dataclass import DataclassIngestor
from zenpyre.ingestors.first_n import FirstNIngestor
from zenpyre.ingestors.in_memory import InMemoryIngestor
from zenpyre.ingestors.last_n import LastNIngestor
from zenpyre.ingestors.mapping import MappingIngestor
from zenpyre.ingestors.pickle import PickleIngestor
from zenpyre.ingestors.processor import ProcessorIngestor
from zenpyre.ingestors.resolve import resolve_ingestor
from zenpyre.ingestors.shuffle import ShuffleIngestor
from zenpyre.ingestors.text import TextIngestor

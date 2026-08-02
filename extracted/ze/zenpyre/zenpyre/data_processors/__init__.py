r"""Contain data processors."""

from __future__ import annotations

__all__ = [
    "BaseProcessor",
    "FilterDocumentsByMetadataProcessor",
    "FilterDocumentsByMetadataRangeProcessor",
    "FilterDocumentsByMetadataValuesProcessor",
    "FirstNProcessor",
    "LambdaProcessor",
    "LastNProcessor",
    "SequenceProcessor",
    "SequentialProcessor",
    "ShuffleProcessor",
    "SortByKeyProcessor",
    "SortDocumentsByMetadataProcessor",
    "SortRecordsByMetadataProcessor",
    "resolve_data_processor",
]

from zenpyre.data_processors.base import BaseProcessor
from zenpyre.data_processors.filter_documents import FilterDocumentsByMetadataProcessor
from zenpyre.data_processors.filter_documents_range import (
    FilterDocumentsByMetadataRangeProcessor,
)
from zenpyre.data_processors.filter_documents_values import (
    FilterDocumentsByMetadataValuesProcessor,
)
from zenpyre.data_processors.first_n import FirstNProcessor
from zenpyre.data_processors.lambdaa import LambdaProcessor
from zenpyre.data_processors.last_n import LastNProcessor
from zenpyre.data_processors.resolve import resolve_data_processor
from zenpyre.data_processors.sequence import SequenceProcessor
from zenpyre.data_processors.sequential import SequentialProcessor
from zenpyre.data_processors.shuffle import ShuffleProcessor
from zenpyre.data_processors.sort_documents import SortDocumentsByMetadataProcessor
from zenpyre.data_processors.sort_key import SortByKeyProcessor
from zenpyre.data_processors.sort_records import SortRecordsByMetadataProcessor

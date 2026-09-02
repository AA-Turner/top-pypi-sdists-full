"""Sink classes for targets."""

from hotglue_singer_sdk.sinks.batch import BatchSink
from hotglue_singer_sdk.sinks.core import Sink
from hotglue_singer_sdk.sinks.record import RecordSink
from hotglue_singer_sdk.sinks.sql import SQLConnector, SQLSink

__all__ = [
    "BatchSink",
    "RecordSink",
    "Sink",
    "SQLSink",
    "SQLConnector",
]

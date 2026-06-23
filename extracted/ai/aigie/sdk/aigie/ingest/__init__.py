"""gRPC ingest client — sends finalized spans to the Kytte Ingest Gateway."""

from aigie.ingest.client import IngestClient
from aigie.ingest.mapper import span_to_proto

__all__ = ["IngestClient", "span_to_proto"]

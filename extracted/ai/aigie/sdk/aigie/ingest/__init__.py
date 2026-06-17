"""gRPC ingest client — sends finalized spans to the Kytte Ingest Gateway."""

from .client import IngestClient
from .mapper import span_to_proto

__all__ = ["IngestClient", "span_to_proto"]

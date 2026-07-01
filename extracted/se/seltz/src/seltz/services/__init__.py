"""Service layer with centralized protobuf imports for API version management."""

from typing import List, Optional, Tuple

# Centralized protobuf imports - update these when API version changes
from seltz_public_api.proto.v1.answer_pb2 import (
    AnswerRequest,
    AnswerResponse,
    AnswerStreamRequest,
    AnswerStreamResponse,
    Citation,
    Citations,
)
from seltz_public_api.proto.v1.answer_pb2_grpc import AnswerServiceStub
from seltz_public_api.proto.v1.seltz_pb2 import Document, SearchRequest, SearchResponse
from seltz_public_api.proto.v1.seltz_pb2_grpc import SeltzServiceStub

# Default per-call deadline (seconds) for unary RPCs, shared by all services.
DEFAULT_TIMEOUT_SECONDS = 30


def auth_metadata(api_key: Optional[str]) -> List[Tuple[str, str]]:
    """Build the gRPC metadata carrying the bearer token, if a key is set."""
    if api_key:
        return [("authorization", f"Bearer {api_key}")]
    return []


__all__ = [
    "SeltzServiceStub",
    "SearchRequest",
    "SearchResponse",
    "Document",
    "AnswerServiceStub",
    "AnswerRequest",
    "AnswerResponse",
    "AnswerStreamRequest",
    "AnswerStreamResponse",
    "Citation",
    "Citations",
    "DEFAULT_TIMEOUT_SECONDS",
    "auth_metadata",
]

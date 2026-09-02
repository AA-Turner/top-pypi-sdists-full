"""Type definitions for River client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class LoraConfig:
    """LoRA adapter configuration."""

    rank: int = 16
    train_attn: bool = True
    train_mlp: bool = True
    train_unembed: bool = False
    seed: int | None = None


@dataclass(frozen=True)
class TrainingDataArtifact:
    """Source bytes and expected digest for server-side integrity verification.

    The API hashes ``content`` itself and retains only the resulting manifest.
    Callers should verify their source files locally before constructing these
    objects, then bind the returned :class:`TrainingDataAttestation` to the
    model they create.
    """

    name: str
    expected_sha256: str
    content: bytes


@dataclass(frozen=True)
class AttestedTrainingDataArtifact:
    """Server-observed source-artifact digest and size."""

    name: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class TrainingDataAttestation:
    """A server-verified source-artifact manifest bound to one session."""

    training_data_attestation_id: str
    artifacts: list[AttestedTrainingDataArtifact]


@dataclass
class TopLogprob:
    """One top-K candidate token at a single position."""

    logprob: float
    token_id: int
    token: str = ""  # Decoded string; may be empty when detokenization is skipped.


@dataclass
class ExpertRouting:
    """Captured MoE expert routing for one sample.

    Populated when the caller passed ``return_expert_routing=True`` on
    the sample request and routing capture was available.

    To enable router replay / flip-rate metrics, splat the canonical
    per-datum keys via ``Sample.routing_datum_keys()`` rather than
    building them by hand:

        datum = {..., **sample.routing_datum_keys(required=True)}

    Current servers return routing captures as an opaque ``handle``; the
    splat yields ``expert_routing_handle``. ``topk_ids`` is retained for
    inspection and proto round-trip compatibility only; replay always
    recomputes the routing weights in the trainer.

    The shape header fields (``num_decoder_layers`` / ``top_k`` /
    ``layer_indices``) are *informational only* and let the user inspect
    capture metadata.

    Byte layout (when ids are present): ``[num_tokens, num_decoder_layers,
    top_k]`` row-major int16 little-endian. ``num_tokens = seqlen - 1``
    because routing capture omits the trailing position.
    """

    # Authoritative — the wire bytes themselves.
    topk_ids: bytes = b""
    # Informational shape header (see class docstring).
    num_tokens: int = 0
    num_decoder_layers: int = 0
    top_k: int = 0
    layer_indices: list[int] = field(default_factory=list)
    # Opaque, server-minted routing reference. The client round-trips just this
    # handle when routing replay or routing metrics are enabled.
    handle: str = ""


@dataclass
class Sample:
    """A generated sample.

    ``tokens`` contains generated token IDs when the response includes them;
    older responses may fall back to retokenizing ``text`` client-side.

    ``prompt_token_ids`` / ``top_logprobs`` / ``prompt_top_logprobs`` are
    ``None`` when the server did not provide them or the feature was not
    requested.

    ``expert_routing`` is populated when ``return_expert_routing=True``
    was passed on the request.

    ``metrics`` carries per-result scalar metrics; empty unless the
    originating request passed a recognized ``metrics_type`` token.
    """

    tokens: list[int]
    text: str
    logprobs: list[float]
    stop_reason: str  # "length", "stop", "eos"
    model_step: int  # Training step this was sampled from (for off-policy tracking)
    prompt_logprobs: list[float] | None = None
    request_id: str = ""  # River API operation ID for debugging
    prompt_token_ids: list[int] | None = None
    # Top-K alternatives at each output / prompt position, when the caller
    # set ``logprobs=K`` on the request. ``None`` when unused or unavailable.
    top_logprobs: list[list[TopLogprob]] | None = None
    prompt_top_logprobs: list[list[TopLogprob]] | None = None
    expert_routing: ExpertRouting | None = None
    # Per-result scalar metrics (see class docstring). Empty dict when the
    # request carried no recognized ``metrics_type`` token.
    metrics: dict[str, float] = field(default_factory=dict)

    def routing_datum_keys(self, *, required: bool = False) -> dict[str, bytes | str]:
        """Return the per-datum keys to splat into a ``forward_backward``
        datum when enabling ``force_routing_replay`` or
        ``compute_expert_flip_metric``.

        Returns an empty dict when this sample carries no routing capture and
        ``required`` is false. Raises ``ValueError`` when ``required`` is true
        and no routing handle is available.

        Example::

            data = []
            for sample in samples:
                datum = {
                    "input_ids": ...,
                    "advantages": ...,
                    **sample.routing_datum_keys(required=True),
                }
                data.append(datum)
        """
        if self.expert_routing is None:
            if required:
                raise ValueError(
                    "Sample has no MoE routing capture. Routing replay requires an "
                    "MoE model; sample with return_expert_routing=True before using "
                    "force_routing_replay or compute_expert_flip_metric."
                )
            return {}
        er = self.expert_routing
        if er.handle:
            return {"expert_routing_handle": er.handle.encode("utf-8")}
        if required:
            raise ValueError(
                "Sample has no MoE routing replay handle. Routing replay requires "
                "an MoE model and a current River API server; sample with "
                "return_expert_routing=True before using force_routing_replay or "
                "compute_expert_flip_metric."
            )
        return {}


@dataclass
class ForwardResult:
    """Result of forward or forward_backward pass."""

    metrics: dict[str, float]  # e.g., {"loss": 2.3, "tokens": 1024}
    logprobs: list | None = None  # Per-sample logprobs (list of numpy arrays), or None


@dataclass
class OptimStepResult:
    """Result of an optimizer step."""

    metrics: dict[str, float]  # e.g., {"step": 1, "lr": 1e-4, "grad_norm": 0.42}


@dataclass
class PendingOp:
    """A submitted but not-yet-resolved async operation.

    Returned by ``Model.submit_forward_backward()`` and
    ``Model.submit_optim_step()``. Call ``.result()`` to block until complete.
    """

    request_id: str
    _session: Any  # Session reference (for polling)
    _model_id: str
    _parse_result: Callable[[Any], ForwardResult | OptimStepResult]
    _timeout: float = 1800.0

    def result(
        self,
        *,
        before_poll: Callable[[], None] | None = None,
    ) -> ForwardResult | OptimStepResult:
        """Block until the operation completes and return the result."""
        kwargs: dict[str, Any] = {}
        if before_poll is not None:
            kwargs["before_poll"] = before_poll
        raw = self._session._wait_for_future(
            self.request_id,
            timeout=self._timeout,
            model_id=self._model_id,
            **kwargs,
        )
        return self._parse_result(raw)


@dataclass
class PendingSample:
    """A submitted but not-yet-resolved sampling operation."""

    request_id: str
    _session: Any
    _timeout: float
    _poll_interval: float
    _parse_result: Callable[[Any], list[list[Sample]]]
    _model_id: str | None = None

    def result(
        self,
        *,
        retry_connection_errors: bool = True,
        before_poll: Callable[[], None] | None = None,
    ) -> list[list[Sample]]:
        """Block until sampling completes and return grouped samples.

        ``retry_connection_errors=False`` exposes the first RetrieveFuture
        transport failure to callers that own a sealed retry policy.
        """
        kwargs: dict[str, Any] = {}
        if not retry_connection_errors:
            kwargs["retry_connection_errors"] = False
        if before_poll is not None:
            kwargs["before_poll"] = before_poll
        raw = self._session._wait_for_future(
            self.request_id,
            timeout=self._timeout,
            poll_interval=self._poll_interval,
            model_id=self._model_id,
            **kwargs,
        )
        if raw.WhichOneof("response") != "inference":
            raise RiverError(f"Unexpected response type: {raw.WhichOneof('response')}")
        return self._parse_result(raw.inference)


@dataclass
class ChatCompleteResult:
    """Result of a chat completion request."""

    response_json: str  # Full OpenAI-format response body (JSON string)
    status_code: int  # HTTP status code from the inference backend


@dataclass
class PromotedStreamingReplica:
    """Server-owned routing metadata for a promoted streaming replica."""

    checkpoint: str
    status: str
    base_url: str | None
    replica_id: str | None
    model: str
    base_model: str
    updated_at: str
    status_reason: str | None = None


@dataclass
class Checkpoint:
    """A saved model checkpoint."""

    path: str  # river://run-id/weights/name
    step: int
    checkpoint_type: str  # "training" or "inference"


class RiverError(Exception):
    """Base exception for River client errors."""


class RiverTimeoutError(RiverError):
    """Operation timed out while retaining its recoverable future ID."""

    def __init__(self, message: str, *, request_id: str | None = None):
        super().__init__(message)
        self.request_id = request_id


class CapacityError(RiverError):
    """No capacity available for the operation."""


class AuthenticationError(RiverError):
    """Authentication failed."""


class ModelNotFoundError(RiverError):
    """Model not found."""


class RiverConnectionError(RiverError):
    """Connection or communication error with the River API server.

    This wraps gRPC errors with a more user-friendly message while preserving
    the original error details for debugging.

    Attributes:
        message: Human-readable error message
        status_code: gRPC status code name (e.g., "UNAVAILABLE", "DEADLINE_EXCEEDED")
        details: Additional error details from the server
        original_error: The original gRPC RpcError for debugging
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: str | None = None,
        details: str | None = None,
        original_error: Exception | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        self.original_error = original_error

        # Build a clean error message
        parts = [message]
        if status_code:
            parts.append(f"[{status_code}]")
        if details:
            parts.append(f"- {details}")

        super().__init__(" ".join(parts))

    @classmethod
    def from_grpc_error(
        cls,
        error: Exception,
        context: str = "API call",
    ) -> "RiverConnectionError":
        """Create a RiverConnectionError from a gRPC RpcError."""
        import grpc

        if not isinstance(error, grpc.RpcError):
            return cls(f"{context} failed: {error}", original_error=error)

        code = error.code()  # type: ignore[union-attr]
        details = error.details()  # type: ignore[union-attr]

        code_messages = {
            grpc.StatusCode.UNAVAILABLE: "Server is unavailable. Check your network connection and endpoint.",
            grpc.StatusCode.DEADLINE_EXCEEDED: "Request timed out. The server may be overloaded.",
            grpc.StatusCode.UNAUTHENTICATED: "Authentication failed. Check your API key.",
            grpc.StatusCode.PERMISSION_DENIED: "Permission denied. You may not have access to this resource.",
            grpc.StatusCode.NOT_FOUND: "Resource not found.",
            grpc.StatusCode.ALREADY_EXISTS: "Resource already exists.",
            grpc.StatusCode.RESOURCE_EXHAUSTED: "Server capacity exceeded. Try again later.",
            grpc.StatusCode.FAILED_PRECONDITION: "Operation failed due to invalid state.",
            grpc.StatusCode.ABORTED: "Operation was aborted.",
            grpc.StatusCode.INTERNAL: "Internal server error.",
            grpc.StatusCode.UNKNOWN: "An unknown error occurred.",
            grpc.StatusCode.INVALID_ARGUMENT: "Invalid request parameters.",
            grpc.StatusCode.CANCELLED: "Request was cancelled.",
        }

        base_message = code_messages.get(code, f"{context} failed")
        status_name = code.name if code else "UNKNOWN"

        return cls(
            base_message,
            status_code=status_name,
            details=details,
            original_error=error,
        )


class SessionHeartbeatError(RiverConnectionError):
    """Session heartbeat was lost or rejected while a session was active."""

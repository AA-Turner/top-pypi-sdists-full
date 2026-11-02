"""The mandatory node-result envelope (Standardized Node Result System, Layer 1).

Every node executor returns ``NodeResult[T]`` — a discriminated union of
:class:`Success` (carrying the node's typed payload ``T``) and
:class:`Failure` (carrying a structured :class:`NodeError`). The envelope is
**engine-plane, not data-plane**: the scheduler is the ONLY consumer. On
Success it unwraps and the bare payload flows downstream exactly as before
(edge mappings, conditional predicates, channels, ``node_outcome.output``,
events, ``last_outputs`` all see ``T``); on Failure the structured error goes
to the outcome's ``error`` column and either parks the run, routes an ERROR
edge, or becomes an explicit fan-out hole (``on_item_failure='hole'``).

Contract (docs/workflow/NODE_RESULT_CONTRACT.md is the published reference):

- ``status`` is the discriminator: ``"success"`` | ``"error"``. No optionals
  within a branch — a Success ALWAYS has ``result``, a Failure ALWAYS has a
  complete ``NodeError``. Illegal states are unrepresentable.
- Payload models must NOT carry top-level fields named ``ok`` / ``success`` /
  ``error`` — envelope semantics live only in the envelope
  (``RESERVED_PAYLOAD_FIELDS``, CI-guarded). ``status`` inside a payload is
  legal (HTTP status codes etc.) — under engine unwrap it never shares a
  namespace with the envelope.
- ``NodeError.code`` shares one namespace with exception class names: the
  retry ladder matches ``RetryPolicy.retry_on`` entries against it, exactly
  as it matches raised exceptions' type names. Prefer stable snake_case codes
  (``"rate_limited"``, ``"parse_failed"``, ``"provider_error"``).
- ``NodeError.details`` is optional structure. Convention: a failed paid call
  puts its usage block under ``details["usage"]`` (the ``AiExecutionResult``
  usage shape) so cost settlement survives failure.

Construction goes through :func:`success` / :func:`failure` — never build the
models by hand in node code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeAlias, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.model import KindModel

T = TypeVar("T", bound=BaseModel)

# Envelope semantics live ONLY in the envelope. A payload model carrying one
# of these at its top level re-creates the pre-envelope ambiguity ("is this
# node failure or domain data?") — banned, CI-guarded
# (scripts/validate_action_standards.py). ``status`` is deliberately NOT
# reserved: under engine unwrap a payload's ``status`` (HTTP status, pipeline
# status) never collides with the envelope discriminator.
RESERVED_PAYLOAD_FIELDS = frozenset({"ok", "success", "error"})


class FieldProblem(KindModel, kind="field_problem"):
    """One field's problem, as a validator reported it — a kind of its own.

    The sectioned-not-flattened law (KINDS_EVERYWHERE_PLAN §4.4): a repeated
    nested structure inside a kind is minted as its own kind and NESTED, never
    smeared across the parent as parallel arrays. A failure can name many bad
    fields; each one is a self-describing instance a renderer can lay out as a
    row without knowing anything about its parent.

    Mirrors ``matrx_graph.failure.FieldProblem`` field for field — that model
    is the RUN-level failure's version of the same fact, and the two shapes
    must stay identical so one component renders both.
    """

    field: str
    """Dotted path from the validator's ``loc`` — "sources", "match.id"."""
    expected: str | None = None
    """What the contract asked for, in words: "at least 1 item"."""
    got: str | None = None
    """A SHORT rendering of what arrived. Truncated; never a full payload."""
    code: str | None = None
    """The validator's own type key ("missing", "too_short") — for metrics."""


class NodeError(KindModel, kind="node_error"):
    """Structured failure — the ONLY shape a node failure travels in, AND a
    registered kind (``node_error``, category ``runtime``).

    ERRORS ARE KINDS (KINDS_EVERYWHERE_PLAN §10d-B3). This dump rides ERROR
    edges, lands in ``workflow.node_outcome.error``, and ships on
    ``NodeFailedEvent.error``; until it carried ``__kind`` it was the one value
    in the engine that crossed every one of those boundaries anonymously — a
    raw dump the frontend could only print, an edge filter could not select,
    and a trigger could not subscribe to. It now says what it is, exactly like
    every success payload does.

    THE CORE HALF — set by every ``failure(...)`` call site:
    ``code`` — stable machine key (snake_case; shares the retry_on namespace
    with exception class names). ``message`` — human-readable. ``details`` —
    optional structured context (``details["usage"]`` carries billed usage
    for paid-but-failed calls).

    THE STRUCTURED HALF — filled in by the scheduler's failure ladder
    (``_fail_attempt``) from the raised exception or the node's own code, and
    OPTIONAL everywhere else. These fields are not new information: they are
    exactly the keys the persisted ``error`` column has carried since the
    structured-failure work, previously assembled as a loose dict BESIDE the
    NodeError instead of ON it. One model now expresses the whole persisted
    shape, so the column, the event, and the edge payload cannot drift into
    three dialects of the same failure.
    """

    code: str
    message: str
    details: dict[str, Any] | None = None

    #: The raised exception's class name (the persisted ``type`` key). Kept
    #: under its historical name — every existing consumer reads ``type``.
    type: str | None = None
    #: The reader-facing cause vocabulary (``matrx_graph.failure.Cause``).
    cause: str | None = None
    step_id: str | None = None
    step_label: str | None = None
    field: str | None = None
    expected: str | None = None
    got: str | None = None
    #: Every bad field, each a nested ``field_problem`` kind instance.
    fields: list[FieldProblem] = Field(default_factory=list)
    #: Duplicate of ``type`` under the structured half's own name — both keys
    #: are in the live column today and readers exist for each.
    error_type: str | None = None
    #: The full raw text, ANSI-stripped. Never dropped.
    technical: str | None = None

    def to_column(self) -> dict[str, Any]:
        """The dict shape for the jsonb ``error`` column and the wire.

        ``exclude_none`` so absent facts stay absent rather than persisting a
        wall of nulls (the rule ``RunFailure.to_column`` already follows), and
        an empty ``fields`` list is dropped for the same reason. The ``__kind``
        discriminator is NOT optional and never dropped — it is what makes the
        value self-describing wherever it lands.
        """
        payload = self.model_dump(mode="json", exclude_none=True)
        if not payload.get("fields"):
            payload.pop("fields", None)
        return payload


class Success(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="forbid")

    status: Literal["success"] = "success"
    result: T


class Failure(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["error"] = "error"
    error: NodeError


NodeResult: TypeAlias = Success[T] | Failure


def success(result: T) -> Success[T]:
    """Wrap a node's typed payload as a Success envelope."""
    return Success[type(result)](result=result)  # type: ignore[valid-type]


def failure(
    code: str,
    message: str,
    *,
    details: dict[str, Any] | None = None,
    technical: str | None = None,
) -> Failure:
    """Build a Failure envelope from a structured error. ``technical`` is the full raw text when
    ``message`` is a person's sentence that leaves it out (the scheduler keeps a node's own)."""
    return Failure(error=NodeError(code=code, message=message, details=details, technical=technical))


@dataclass(slots=True, frozen=True)
class InterpretedResult:
    """One executor return value, interpreted through the envelope protocol.

    Exactly one of ``payload`` / ``error`` is set.
    """

    payload: BaseModel | None
    error: NodeError | None


def interpret_node_result(output: Any) -> InterpretedResult:
    """Interpret an executor's return value — the helper every DIRECT-execute
    path outside the scheduler uses (node-test endpoint, tool.call inner
    dispatch, any future direct caller). The scheduler itself interprets
    inline (``_execute_invocation_body``) because it additionally runs the
    output_schema drift guard and the full failure ladder; the two MUST stay
    semantically identical — change one, change both.

    Raises ``TypeError`` for anything that is not a ``NodeResult`` —
    including a bare BaseModel payload (the pre-envelope legacy form,
    deleted at ratchet zero). The caller converts the TypeError into its
    own loud failure (the scheduler raises ExecutionError).
    """
    if isinstance(output, Failure):
        return InterpretedResult(payload=None, error=output.error)
    if isinstance(output, Success):
        return InterpretedResult(payload=output.result, error=None)
    raise TypeError(
        f"node executor returned {type(output).__name__}; expected "
        f"NodeResult[T] (Success/Failure). Bare payload returns were removed "
        f"at ratchet zero — wrap the payload with success(...)."
    )

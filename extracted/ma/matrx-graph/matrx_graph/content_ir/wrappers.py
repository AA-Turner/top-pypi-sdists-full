"""The runtime wrapper kinds — the canonical envelopes, built once.

THE LAYER MODEL (Arman, 2026-08-20 — plan of record:
``common-docs/systems/architecture/content-ir/FEATURE.md`` §4.1):

    "I think where the issue came in is someone misunderstood the wrapper we
    place for internal recognition of a step. And the fact that that wrapper is
    still holding data. And if that data is anything other than just a bunch of
    text, then it is an object itself that should be a kind in an ideal world."

Two categories, both kinds, nested, never merged:

* **Data kinds** (``category: data``) — pure portable shapes (``website``,
  ``web_search_results``). No runtime fields. They travel and render anywhere.
* **Runtime wrapper kinds** (``category: runtime``, this module) — the CLOSED
  set of envelopes carrying instance context, with data kinds nested inside as
  typed payloads.

The invariant that keeps them honest, in both directions:

    A wrapper NEVER absorbs payload fields.
    A payload NEVER carries runtime fields.

Adding "just one" field from the payload onto a wrapper (or a ``run_id`` onto a
data kind) is how the original corruption started; it is a defect, not a
shortcut.

THE EDGE CONTRACT (ratified 2026-08-20)
---------------------------------------
Workflow edges carry the **data kind only**. The wrapper exists at persistence
and at transport to the UI — where the packet must say which workflow, which
node, and then, nested inside, what the data IS. A node that genuinely needs
runtime context declares the WRAPPER kind as its ``input_kind`` and receives it
explicitly. This is how typed pipelines work everywhere: the function receives
the value, not the call stack.

THE AGENT OUTPUT CONTRACT
-------------------------
``AgentResult.content`` is a LIST of kind instances, in document order — the
same shape whether an agent returned one paragraph or a narrative with six
embedded structures. This is deliberately the Anthropic/OpenAI message-content
model: the simple case is a one-element list, so the 99% case pays nothing and
the complex case needs no second mechanism. See ``AgentResult`` below for the
full case-by-case contract.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import Field

from matrx_graph.content_ir.model import KindModel, kind_of
from matrx_graph.types.result import NodeError

__all__ = [
    "RuntimeWrapper",
    "NodeOutcomeWrapper",
    "RunResultWrapper",
    "AgentResultWrapper",
    "ToolResultWrapper",
    "KindPayload",
]

#: A payload is any kind instance — a model or its serialized form. Wrappers are
#: generic over it so a caller can keep full typing (``NodeOutcomeWrapper[
#: WebSearchResults]``) while the engine, which handles every node uniformly,
#: works with the permissive form.
KindPayload = TypeVar("KindPayload")


class RuntimeWrapper(KindModel, Generic[KindPayload]):
    """Shared base for every runtime wrapper kind.

    Concrete wrappers declare their slug and add ONLY runtime context fields.
    The payload always lives on ``output`` (or ``content`` for agents, which
    carry a list) and is a kind instance — never loose fields spread onto the
    wrapper.
    """

    #: Wall-clock timing of the wrapped work, when the producer knows it.
    started_at: str | None = None
    ended_at: str | None = None
    duration_ms: int | None = None

    #: WIRE ELISION MARKER — the twin of the ``__ir`` envelope's ``value_ref``
    #: (``content_ir.envelope.VALUE_REF_OUTPUT``). When a wrapper rides a frame
    #: that ALREADY carries the payload (``NodeCompletedEvent.output``, a run
    #: read response's ``output``), ``output`` is dropped and this names the
    #: sibling frame field holding it, so the same dict is never serialized
    #: twice per event / per persisted row. Its PRESENCE is the marker — never
    #: a bare ``output: null``, which is a legitimate empty payload. A consumer
    #: rehydrates at its ingest gate before anything else reads the wrapper.
    #: ``None`` = the payload is inline and the wrapper stands alone.
    #:
    #: It is a DECLARED field, not an injected key, for the same reason
    #: ``__kind`` is: ``extra="forbid"`` is the contract, and a marker the
    #: schema does not know about is a fatal one missed strip away.
    output_ref: str | None = None

    def payload_kind(self) -> str | None:
        """The kind slug of what this wrapper carries (``None`` when empty).

        This is what runtime kind propagation reads: a pass-through node's
        settled kind is the kind of what actually flowed, and this is how the
        engine asks without unwrapping or guessing.
        """
        return kind_of(getattr(self, "output", None))


class NodeOutcomeWrapper(RuntimeWrapper[KindPayload], kind="node_outcome"):
    """One node invocation's result, as it is persisted and sent to the UI.

    The packet Arman described: the front end receives this and knows which
    workflow, which node, and then — nested inside ``output`` — exactly what
    the data is, all the way down.
    """

    run_id: str
    node_id: str
    workflow_id: str | None = None
    step: int | None = None
    attempt: int = 1
    status: str = "completed"

    #: The node's declared output kind, as declared (``None`` for an undeclared
    #: node — which is a loud defect under the plan, never a silent NULL).
    output_kind: str | None = None
    #: The verdict from the kind catalog. ``None`` = never checked; a skipped
    #: check is NEVER renderable as a pass (``matrx_graph.kinds`` posture).
    output_kind_ok: bool | None = None
    output_kind_errors: list[str] | None = None

    output: KindPayload | None = None

    #: THE FAILURE MEMBER (plan §10d-B3). A node that FAILED is still a settled
    #: invocation, and its packet has exactly the same shape as a successful
    #: one — ``status="failed"`` with a ``node_error`` kind instance nested
    #: here instead of a data kind under ``output``. This is what lets a
    #: failure render through the registry (a real component keyed on
    #: ``node_error``) and route through kind-filtered edges and triggers,
    #: rather than being the one value on the wire the platform could only
    #: print raw. ``None`` on a successful outcome — never an empty error
    #: object, which would read as "failed with nothing to say".
    error: NodeError | None = None


class RunResultWrapper(RuntimeWrapper[KindPayload], kind="run_result"):
    """A whole workflow run's result — the workflow itself is a kind too.

    ``outputs`` is the typed half: one ``node_outcome`` per TERMINAL node, each
    carrying its own data kind nested inside — so a reader of a finished run
    gets the same packet a live ``node_completed`` gives (which workflow, which
    node, timing, verdict, and then what the data IS), without re-deriving it
    from the raw terminal map.

    ``output`` remains the run's terminal payload as the engine records it; on
    a frame that already carries it (a run read response), it is elided via
    ``output_ref`` rather than serialized twice.
    """

    run_id: str
    workflow_id: str
    status: str = "completed"
    output_kind: str | None = None
    output: KindPayload | None = None

    #: The terminal nodes' outcomes, each a self-describing ``node_outcome``
    #: instance with its data kind nested under its own ``output``.
    outputs: list[NodeOutcomeWrapper[Any]] = Field(default_factory=list)


class ToolResultWrapper(RuntimeWrapper[KindPayload], kind="tool_result"):
    """One tool invocation's result.

    The tool declares its result kind; the boundary wrapper validates and the
    payload arrives typed — the same law the node wrapper enforces, so a tool
    result is as routable as a node output.
    """

    tool_name: str
    call_id: str | None = None
    ok: bool = True
    error: str | None = None
    output_kind: str | None = None
    output: KindPayload | None = None


class AgentResultWrapper(RuntimeWrapper[Any], kind="agent_result"):
    """An agent invocation's result. ``content`` is ALWAYS a list of kinds.

    THE CONTRACT, case by case (settled with Arman, 2026-08-20). The guard he
    set: *don't complicate the 99% case for the 1%* — so there is exactly ONE
    shape, and the simple case is a one-element list:

    * **Plain prose** → ``content = [markdown]``. One element, nothing else to
      think about.
    * **Bound agent** (hard-bound via ``response_format_for_kind``) →
      ``content = [the bound kind instance]``; the node's declared
      ``output_kind`` names it. This is the clean, preferred form.
    * **Prose with embedded kinds** (XML blocks, fences, detected structures)
      → the narrative segments AND the detected instances, interleaved in
      document order, each fully typed. Six embedded kinds means six routable
      typed values out of one agent call — which is what makes kind-filtered
      edges and per-instance fan-out possible without any custom code.
    * **Provider JSON that is not a registered kind** → a generic structured
      instance (``parsed_json``): usable and renderable through the platform
      floor, but visibly anonymous and alarmed to its creator. That is the
      SMELL, and its fix is always the same — bind the agent.

    Detection is NOT re-implemented here. ``matrx_ai.processing.blocks``
    already parses agent output into kind envelopes on the chat path
    (``block_detector`` / ``StreamBlockProcessor`` / ``envelope``); the agent
    node consumes that result instead of the raw ``final_text`` string it
    passes today. One parser, shared by chat and workflows.

    ``final_text``-as-a-JSON-string is dead: it is what killed the kind at the
    agent boundary and forced hand-written projection nodes downstream.
    """

    #: Every content element is a kind instance (model or serialized payload),
    #: in document order.
    content: list[Any] = Field(default_factory=list)

    #: Run bookkeeping — the cost of the call, never the shape of the answer.
    model: str | None = None
    usage: dict[str, Any] | None = None
    stop_reason: str | None = None

    def primary(self) -> Any | None:
        """The single content element, when there is exactly one.

        The consumption sugar that keeps the 99% case trivial: mapping "the
        result" of a one-element content auto-unwraps to that instance, so an
        author who never thinks about lists never has to. Returns ``None`` when
        content is empty or holds several instances — those cases are handled
        by kind-filtered mapping (``instances_of``), which is explicit on
        purpose.
        """
        return self.content[0] if len(self.content) == 1 else None

    def instances_of(self, slug: str) -> list[Any]:
        """Every content element whose kind is ``slug``, in document order.

        This is what a kind-filtered edge resolves against: an edge declaring
        "carry ``website`` instances" fans exactly these downstream, and an
        edge whose kind never appeared simply does not fire.
        """
        return [item for item in self.content if kind_of(item) == slug]

    def content_kinds(self) -> list[str]:
        """The kind slugs present in ``content``, in document order.

        Includes duplicates: order and multiplicity are both meaningful when
        routing per instance.
        """
        return [slug for slug in (kind_of(item) for item in self.content) if slug]

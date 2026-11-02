from __future__ import annotations

from typing import Any, ClassVar


class MatrxGraphError(Exception):
    pass


class DefinitionError(MatrxGraphError):
    pass


class DraftConflictError(DefinitionError):
    """Optimistic-concurrency conflict on a draft save (audit P1-11).

    Raised when ``save_draft(expected_updated_at=...)`` finds the row was
    modified since the caller loaded it — two tabs / two users editing the
    same workflow. The caller surfaces it as HTTP 409; the client reloads
    and re-applies."""


class OutputContractError(DefinitionError):
    """A publish was refused because the workflow's IO declaration lies.

    SPEC-workflow-ui-contract §2.3: ``definition.output_kind`` must be a kind
    one of the workflow's deliverables actually produces (and
    ``input_kind`` a kind its entry nodes accept). This is a DISTINCT error
    from "definition not found" so the host maps it to a 422 the author can
    act on, never a generic 500.
    """


class CompilationError(MatrxGraphError):
    """A definition the engine refuses to turn into a runnable graph.

    ``issues`` carries the validation gate's FULL findings when the refusal
    came from `validate_definition` — one entry per problem, each with the
    node path it is about. It is empty for the single-cause refusals raised
    later in compilation (a bad edge declaration, an unparseable retry
    policy), whose whole story is already in ``str(exc)``.

    🚨 WHY IT EXISTS. The message alone named only the FIRST issue and sent
    the reader to the server logs, so a host could not tell anyone what was
    actually wrong. On 2026-09-11 that is exactly what happened: six nodes of
    the "Verification Desk" workflow failed the Plan-anchor check,
    `GET /workflows/{id}/run-form` answered 400, and the person looking at
    the run box was told "Bad request. Please check your input." — about
    input they had not typed, with the six named reasons nowhere they could
    reach. An error that knows six things and says one is a silent failure.
    """

    def __init__(self, message: str, *, issues: list[Any] | None = None) -> None:
        super().__init__(message)
        self.issues = list(issues or [])


class ExecutionError(MatrxGraphError):
    pass


class ResumeCannotFinishError(ExecutionError):
    """A checkpoint resumed on a graph it can never finish on (see
    ``executor/resume_preflight.py``). Raised before any step runs; each
    problem names its remedy (rerun from a step, or a fresh run)."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__(
            "This run cannot continue from this point: "
            + "; ".join(self.problems)
            + "."
        )


class EdgeRoutingError(ExecutionError):
    """A failure while routing a node's SUCCESSFUL output downstream.

    Raised by ``Scheduler._route_outputs`` for conditional-edge predicate
    failures and explicit edge-mapping misses. Subclasses ``ExecutionError``
    so existing handlers still catch it; carries the source ``node_id`` +
    ``edge_id`` so the scheduler can park the run as ERRORED with the
    failure attributed to a concrete node instead of dying terminally.
    """

    def __init__(self, message: str, *, node_id: str, edge_id: str) -> None:
        super().__init__(message)
        self.node_id = node_id
        self.edge_id = edge_id


class NodeFailureError(ExecutionError):
    """A node returned a ``Failure`` envelope that could not be routed.

    Raised by the scheduler when a node's returned ``Failure`` has exhausted
    its retries and the node has neither an outgoing ERROR edge nor
    ``on_item_failure='hole'`` (fanned invocations) — the park path,
    identical in behavior to a raised exception. Carries the structured
    ``NodeError`` so recovery surfaces the code/details, not just a string.
    """

    def __init__(self, node_id: str, node_error: object) -> None:
        code = getattr(node_error, "code", "error")
        message = getattr(node_error, "message", str(node_error))
        super().__init__(f"Node '{node_id}' failed: {code}: {message}")
        self.node_id = node_id
        self.node_error = node_error


class FanOutAllItemsFailedError(ExecutionError):
    """Every item fanned out to a fail-soft (``data.optional``) step failed (2026-10-22).

    ``data.optional`` lets SOME items of a fan-out fail while the run goes on. When EVERY item
    failed, the stage did nothing — continuing would prune everything after it and end the run
    ``completed``. The scheduler parks the run ERRORED on the target step with this error: the
    children's errors grouped by kind, with counts. ``on_item_failure='hole'`` and a fan-out
    whose failures route over an ERROR connection never raise it (something reaches the steps
    after them). ``errors`` items are ``NodeError``-like objects or their ``{code, message}``
    dumps (items that settled in an earlier step).
    """

    def __init__(self, *, node_id: str, label: str | None, errors: list[object]) -> None:
        groups: dict[str, int] = {}
        for err in errors:
            if isinstance(err, dict):
                code = err.get("code", "error")
                message = err.get("message", str(err))
            else:
                code = getattr(err, "code", "error")
                message = getattr(err, "message", str(err))
            key = f"{code}: {message}"
            groups[key] = groups.get(key, 0) + 1
        ordered = sorted(groups.items(), key=lambda kv: -kv[1])
        shown = "; ".join(f"{key[:300]} ×{n}" for key, n in ordered[:5])
        if len(ordered) > 5:
            shown += f"; (+{len(ordered) - 5} more kinds of error)"
        count = len(errors)
        name = f"'{label}' ({node_id})" if label else f"'{node_id}'"
        noun = "item" if count == 1 else "items"
        super().__init__(
            f"All {count} {noun} of step {name} failed, so nothing reached the steps after it: "
            f"{shown}"
        )
        self.node_id = node_id
        self.errors = errors


class NodeInputValidationError(ExecutionError):
    """A source node's run-form-seeded inputs failed deep validation against
    the compiled JSON Schema its run form was generated from (io.user_input).

    Raised by ``Scheduler._run_node`` BEFORE the node executes, so a
    wrong-typed / out-of-enum / missing-required value parks the run here with
    a per-field message instead of silently flowing downstream and surfacing
    as a confusing failure two steps later. Subclasses ``ExecutionError`` so
    existing handlers park the run as ERRORED attributed to this concrete
    node; carries ``node_id`` + the per-field ``field_errors`` for structured
    display. The permissive ``spec.input_schema`` (``extra="allow"``, zero
    fields) cannot enforce the author-defined field types — this is the guard
    that makes the declared contract real.
    """

    def __init__(self, message: str, *, node_id: str, field_errors: list[str]) -> None:
        super().__init__(message)
        self.node_id = node_id
        self.field_errors = field_errors


class UnresolvedVariableError(ExecutionError):
    """A node's static inputs reference a run variable (``{"$var": name}``)
    that has no value for this run — not in ``initial_variables``, no
    per-reference default, no declared default.

    Raised at input-resolution time (``resolve_var_refs`` strict mode) so the
    run parks ERRORED on the referencing node with a message naming the
    variable — never a silent empty string flowing downstream. References to
    UNDECLARED variables never get this far: they fail loudly at
    compile/validate time (CompilationError / ValidationIssue).
    """


class UnresolvedInputError(ExecutionError):
    """A node's static inputs reference a workflow input (``{"$input": name}``)
    that either is not on the compiled input surface (undeclared — loud by
    design, never a silent empty string) or landed no value for this run and
    has no default. Raised at input-resolution time in strict mode; the
    lenient introspection path reports the field unsatisfied instead.
    """


class ChannelError(MatrxGraphError):
    pass


class CheckpointError(MatrxGraphError):
    pass


class CheckpointWriteFailedError(CheckpointError):
    """The run's progress could not be saved, and the run dies for OUR reason.

    Raised only after the checkpoint write has spent its whole retry budget
    (``workflow.checkpoint_write`` knobs). It carries the honest sentence the
    person sees — the size of the row we failed to write included, because on
    2026-09-12 run ``053e8b72`` died on a 1.1 MB checkpoint under database load
    and was reported to her as "This account needs an age check before AI can
    run" (a message-regex read the documents inside the ORM's rendered args).

    ``person_message`` is honored by ``matrx_graph.failure.failure_from_exception``:
    an exception that already knows how to say it in plain English is believed
    rather than re-derived.
    """

    def __init__(
        self,
        *,
        run_id: str,
        checkpoint_id: str,
        step: int,
        payload_bytes: int,
        attempts: int,
        original_error: BaseException,
    ) -> None:
        self.run_id = run_id
        self.checkpoint_id = checkpoint_id
        self.step = step
        self.payload_bytes = payload_bytes
        self.attempts = attempts
        self.original_error = original_error
        size_mb = payload_bytes / 1_048_576
        super().__init__(
            f"checkpoint {checkpoint_id} (run {run_id}, step {step}) could not be "
            f"written after {attempts} attempt(s): the row carries "
            f"{payload_bytes:,} bytes ({size_mb:.2f} MB) of step state. "
            f"Underlying: {type(original_error).__name__}: {original_error}"
        )
        self.person_message = (
            "We couldn't save this run's progress, so it stopped — nothing you "
            f"did caused it. The step's saved state had grown to {size_mb:.1f} MB "
            "and our database didn't finish storing it in time. Start the run "
            "again, and if it keeps happening, split the work into smaller "
            "batches or tell us so we can raise the limit."
        )


class NodeRegistryError(MatrxGraphError):
    pass


class GraphInterrupt(MatrxGraphError):
    def __init__(self, node_id: str, payload: dict[str, object]) -> None:
        super().__init__(f"Graph interrupted at node '{node_id}'")
        self.node_id = node_id
        self.payload = payload


#: Interrupt-payload marker: the question belongs to someone this step is
#: waiting on (a called workflow), so the person's answer is HANDED to the step
#: when it runs again — never recorded as the step's own output. Set by the step
#: that relays the question (``subgraph.call``); read by ``Scheduler.resume``.
FORWARDS_ANSWER_KEY = "forwards_answer"


def forwards_answer(interrupt_payload: object) -> bool:
    """True when a park relays another run's question (either interrupt shape:
    the run-row ``{"node_id", "payload"}`` envelope or the bare node payload)."""
    if not isinstance(interrupt_payload, dict):
        return False
    inner = interrupt_payload.get("payload")
    payload = inner if isinstance(inner, dict) else interrupt_payload
    return payload.get(FORWARDS_ANSWER_KEY) is True


class NodeTimeoutError(MatrxGraphError):
    """A node exceeded its configured timeout.

    Raised by the scheduler when ``NodeSpec.timeout_ms`` elapses without the
    executor returning. The exception's class name (``"NodeTimeoutError"``)
    is what callers should put in ``RetryPolicy.retry_on`` to make timeouts
    retryable. Otherwise the failure surfaces like any other exception —
    parks the run as ERRORED, recovery API can retry.
    """

    #: Where the elapsed ceiling came from — the workflow author's own
    #: ``NodeSpec.timeout_ms`` (``"declared"``) or the platform's step wall
    #: clock (``"platform"``, knob ``workflow.step_clock.default_step_seconds``).
    #: The two have different remedies, so the sentence a person reads names
    #: which one stopped their run and what to do about it.
    _REMEDY: ClassVar[dict[str, str]] = {
        "declared": (
            "This step declares its own time limit. Raise that step's timeout if the "
            "work honestly takes this long, or find out what it was waiting for."
        ),
        "platform": (
            "Nothing this step was waiting on answered in time — most often a model or "
            "tool call that stalled with the connection still open. The step was "
            "canceled rather than left hanging. Run it again; if it keeps taking "
            "longer than the limit, an admin can raise "
            "'workflow.step_clock.default_step_seconds'."
        ),
    }

    def __init__(
        self, node_id: str, timeout_ms: int, attempt: int, *, source: str = "declared"
    ) -> None:
        remedy = self._REMEDY.get(source, self._REMEDY["declared"])
        elapsed = f"{timeout_ms}ms" if timeout_ms < 1000 else f"{timeout_ms / 1000:.0f}s"
        super().__init__(
            f"Step '{node_id}' was stopped after {elapsed} "
            f"(attempt {attempt}) — it passed the "
            f"{'time limit set on this step' if source == 'declared' else 'time limit every step gets'}. "
            f"{remedy}"
        )
        self.node_id = node_id
        self.timeout_ms = timeout_ms
        self.attempt = attempt
        self.source = source
        #: Honored by ``matrx_graph.failure.failure_from_exception``: an
        #: exception that already knows how to say it in plain English is
        #: believed rather than re-derived. Without this the run's error reads
        #: "This step ran past its time limit and was stopped." — true, and a
        #: shrug: it names no step, no ceiling and no remedy, which is exactly
        #: the silent-failure shape this whole fix exists to close.
        self.person_message = (
            f"The step '{node_id}' was stopped after {elapsed} because it passed "
            f"the {'time limit its author set for it' if source == 'declared' else 'time limit every step gets'}. "
            f"{remedy}"
        )


class ActionAuthorizationError(MatrxGraphError, PermissionError):
    """An ``admin_only`` action was invoked by a non-admin caller.

    Raised by ``_ActionExecutor.execute`` — the single convergence point for
    both a directly-dispatched registered node (scheduler) and the dynamic
    ``tool.call`` node (``resolve_action_executor`` → same registered
    adapter) — before the wrapped function ever runs. Subclasses
    ``PermissionError`` so callers can catch the standard-library type
    without importing this module; subclasses ``MatrxGraphError`` so it's
    also catchable alongside every other engine failure. Surfaces like any
    other node exception: the scheduler parks the run as ERRORED and records
    the failure, it is NOT retried (not in any executor's default
    ``retry_on``), and the message names the action + caller so the cause is
    obvious in the run's error event.
    """

    def __init__(self, action_name: str, *, user_id: str | None) -> None:
        who = user_id or "<no user_id>"
        super().__init__(
            f"Action '{action_name}' is admin-only and cannot be run by non-admin caller '{who}'."
        )
        self.action_name = action_name
        self.user_id = user_id

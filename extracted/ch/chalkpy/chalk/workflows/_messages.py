from __future__ import annotations

import contextlib
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Iterator, Mapping, Sequence

from chalk.workflows._context import current_orchestrator, local_messages_var

# The one signal the Chalk API server delivers every message on; the message's own name is in
# the envelope. Must match WorkflowMessageSignalName in go-api-server's workfloworchestrator.
WORKFLOW_MESSAGE_SIGNAL = "chalk.workflow_message"


@dataclass(frozen=True)
class WorkflowMessage:
    """A message delivered to a running workflow, e.g. a reviewer's decision.

    `sender_kind` and `sender_id` identify who sent it. For a message sent through the Chalk
    API server (`ChalkClient.send_workflow_message`), they are authenticated by the server
    (for example `"user"` and a user id, or `"service_token"` and a token id) and cannot be
    set by the sender, so a workflow can use them to decide whose decisions to accept.

    A message sent by another workflow with `chalk.workflows.send_message` has `sender_kind`
    `"workflow"` and the sending workflow's id as `sender_id`. Those are written by the
    sending workflow itself and do not pass through the API server, so they are not
    authenticated: do not use them to authorize a decision.
    """

    name: str
    payload: Any
    sender_kind: str
    sender_id: str
    sent_at: str


class WorkflowMessageTimeoutError(TimeoutError):
    """Raised by `wait_for_message` when no message arrives within its timeout."""


def message_from_envelope(envelope: Mapping[str, Any]) -> WorkflowMessage:
    sender = envelope.get("sender") or {}
    return WorkflowMessage(
        name=str(envelope.get("name", "")),
        payload=envelope.get("payload"),
        sender_kind=str(sender.get("kind", "")),
        sender_id=str(sender.get("id", "")),
        sent_at=str(envelope.get("sent_at", "")),
    )


async def wait_for_message(name: str, *, timeout: timedelta | None = None) -> WorkflowMessage:
    """Wait inside a `@workflow` for the next message named `name`.

    Messages are sent with `ChalkClient.send_workflow_message(workflow_id, name, payload)`
    (or the `SendWorkflowMessage` API). A message that arrives before the workflow starts
    waiting is kept, and messages with the same name are returned in the order they arrived.
    Waiting is durable: the run can wait for days, across worker restarts and scale-to-zero.

    Parameters
    ----------
    name
        The message name to wait for, e.g. `"review"`.
    timeout
        How long to wait. `None` waits indefinitely.

    Raises
    ------
    WorkflowMessageTimeoutError
        If no message named `name` arrives within `timeout`.

    Examples
    --------
    >>> from datetime import timedelta
    >>> from chalk.workflows import task, wait_for_message, workflow
    >>> @workflow
    ... async def review_flagged_account(account_id: str) -> str:
    ...     review = await wait_for_message("review", timeout=timedelta(days=2))
    ...     return "approved" if review.payload["approved"] else "rejected"
    """
    orchestrator = current_orchestrator()
    if orchestrator is None:
        raise RuntimeError("wait_for_message can only be called inside a @workflow")
    return await orchestrator.wait_for_message(name, timeout)


async def send_message(workflow_id: str, name: str, payload: Any) -> None:
    """Send a message from inside a `@workflow` to another running workflow.

    The receiving workflow gets it from `wait_for_message(name)`, with `sender_kind`
    `"workflow"` and this workflow's id as `sender_id`. Use it, for example, for a child
    started with `start_child` to report back to its parent (see `parent_workflow_id`), or to
    reply to the `sender_id` of a message from another workflow.

    The message is delivered by the workflow orchestrator directly, not through the Chalk API
    server, and is recorded in this workflow's history, so the workflow lineage view shows it
    as a message edge from this workflow to `workflow_id`. Because it does not pass through
    the API server, the sender is self-declared rather than authenticated as it is for
    `ChalkClient.send_workflow_message`; see `WorkflowMessage`.

    Parameters
    ----------
    workflow_id
        The id of the running workflow to message.
    name
        The message name the receiver waits for.
    payload
        The message body. Must be JSON-serializable.

    Examples
    --------
    >>> from chalk.workflows import send_message, wait_for_message, workflow
    >>> @workflow
    ... async def echo() -> None:
    ...     ping = await wait_for_message("ping")
    ...     await send_message(ping.sender_id, "pong", ping.payload)
    """
    orchestrator = current_orchestrator()
    if orchestrator is None:
        raise RuntimeError(
            "chalk.workflows.send_message can only be called inside a @workflow; "
            + "use ChalkClient.send_workflow_message to message a workflow from outside one"
        )
    await orchestrator.send_message(workflow_id, name, payload)


@contextlib.contextmanager
def local_messages(messages: Sequence[tuple[str, Any]]) -> Iterator[None]:
    """Queue messages for workflows invoked directly in this process, such as in unit tests.

    A workflow called as a plain coroutine runs on a local orchestrator that no one can send
    messages to; inside this context its `wait_for_message` calls receive these instead, in
    order, with `sender_kind` `"local"`.

    >>> with local_messages([("review", {"approved": True})]):  # doctest: +SKIP
    ...     assert await review_flagged_account("acct-1") == "approved"
    """
    queued = [
        message_from_envelope({"name": name, "payload": payload, "sender": {"kind": "local", "id": ""}})
        for name, payload in messages
    ]
    token = local_messages_var.set(queued)
    try:
        yield
    finally:
        local_messages_var.reset(token)

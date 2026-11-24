from __future__ import annotations

from typing import Any, TypedDict
from urllib.parse import urlencode

from bitfab.http import HttpClient

SANDBOX_STORES_PATH = "/api/sdk/sandboxStores"


class SandboxStore(TypedDict):
    """One sandbox's saved state for one trace.

    A replay of that trace starts the sandbox from it.

    Attributes:
        sandbox: The sandbox's name, such as ``"Gmail"``.
        traceId: The trace the state belongs to.
        state: The sandbox's state, in the shape its ``start`` returns.
        createdAt: When it was first saved (ISO 8601).
        updatedAt: When it last changed (ISO 8601).
    """

    sandbox: str
    traceId: str
    state: Any
    createdAt: str
    updatedAt: str


class SandboxStoresClient:
    """Sandbox state saved per trace, one row per sandbox and trace.

    When a replay runs with a sandbox on, that sandbox starts from the state
    saved for the replayed trace, or from the trace as usual when none is
    saved, and its state is saved to the new replay trace after each write
    and when the item finishes. Sandboxes that are off are neither read nor
    saved.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def get(self, sandbox: str, trace_id: str) -> SandboxStore | None:
        """The state saved for one sandbox and trace, or ``None`` when there is none.

        Args:
            sandbox: The sandbox's name, such as ``"Gmail"``.
            trace_id: The trace the state belongs to.
        """
        query = urlencode({"sandbox": sandbox, "traceId": trace_id})
        return self._http_client.get(f"{SANDBOX_STORES_PATH}?{query}")["sandboxStore"]

    def list_for_trace(self, trace_id: str) -> list[SandboxStore]:
        """Every sandbox's saved state for a trace, by sandbox name."""
        query = urlencode({"traceId": trace_id})
        return self._http_client.get(f"{SANDBOX_STORES_PATH}?{query}")["sandboxStores"]

    def seed(self, sandbox: str, trace_id: str, state: Any) -> SandboxStore:
        """Save the state one sandbox starts from when this trace is replayed.

        Replaces any state saved for that sandbox and trace. Other sandboxes'
        state for the trace is untouched.

        Args:
            sandbox: The sandbox's name, such as ``"Gmail"``.
            trace_id: The trace whose replays start from it.
            state: The starting state, in the shape that sandbox's ``start``
                returns (for Gmail, a list of messages, one mailbox, or
                ``{"mailboxes": [...]}``; for GitHub, a snapshot). It must be
                JSON.
        """
        written = write_sandbox_stores(self._http_client, trace_id, {sandbox: state})
        if not written:
            raise RuntimeError(
                f"The server did not return the {sandbox} state it saved for "
                f"trace {trace_id}."
            )
        return written[0]

    def reset(self, sandbox: str, trace_id: str) -> bool:
        """Delete the state saved for one sandbox and trace.

        A replay of the trace then starts that sandbox from the trace again.
        Returns whether there was state to delete. Other sandboxes' state is
        untouched.
        """
        return self._http_client.request(
            f"{SANDBOX_STORES_PATH}/reset", {"sandbox": sandbox, "traceId": trace_id}
        )["deleted"]


def read_sandbox_store_state(
    http_client: HttpClient, sandbox: str, trace_id: str
) -> dict[str, Any] | None:
    query = urlencode({"sandbox": sandbox, "traceId": trace_id})
    found = http_client.get(f"{SANDBOX_STORES_PATH}?{query}").get("sandboxStore")
    return None if found is None else {"state": found.get("state")}


def write_sandbox_stores(
    http_client: HttpClient, trace_id: str, sandboxes: dict[str, Any]
) -> list[SandboxStore]:
    return http_client.request(
        f"{SANDBOX_STORES_PATH}/write", {"traceId": trace_id, "sandboxes": sandboxes}
    ).get("sandboxStores", [])

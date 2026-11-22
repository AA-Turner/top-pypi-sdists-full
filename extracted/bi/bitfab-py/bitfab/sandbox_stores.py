from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, TypedDict
from urllib.parse import quote, urlencode

from bitfab.http import HttpClient

SANDBOX_STORES_PATH = "/api/sdk/sandboxStores"


class SandboxStoreEntry(TypedDict):
    """One sandbox's state in a sandbox store.

    Attributes:
        sandbox: The sandbox's name, such as ``"Gmail"``.
        state: What the sandbox starts from the next time the trace is
            replayed: the end state its last replay left, or the seed when it
            has none.
        updatedAt: When it last changed (ISO 8601).
        traceId: The trace this state belongs to, or ``None`` for a seed.
    """

    sandbox: str
    state: Any
    updatedAt: str
    traceId: str | None


class SandboxStore(TypedDict):
    """A named, saved state for an organization's sandboxes, kept apart from traces.

    Attributes:
        id: The store's id.
        name: The name it is addressed by.
        entries: One entry per sandbox, by sandbox name: the seeds, or, when
            read for a trace, that trace's own state with the seeds filling
            in the sandboxes it has none for.
        recentTraceIds: The 100 traces most recently linked to it, newest
            first.
    """

    id: str
    name: str
    createdAt: str
    updatedAt: str
    entries: list[SandboxStoreEntry]
    recentTraceIds: list[str]


class SandboxStoreSummary(TypedDict):
    id: str
    name: str


class SandboxStoreLink(TypedDict):
    """What ``link_traces`` linked.

    Attributes:
        sandboxStore: The store, created if it did not exist.
        linkedTraceIds: The traces now linked to it. A trace outside the API
            key's organization is left out.
    """

    sandboxStore: SandboxStoreSummary
    linkedTraceIds: list[str]


class SandboxStoresClient:
    """Sandbox stores: named state that sandboxes read from and write to across replays.

    Each trace has its own state in a store. A replay run with
    ``sandbox_store=name`` starts each sandbox from the replayed trace's state
    for it, else from the store's seed, else from the trace as usual, and
    writes each sandbox's end state back for that trace when the item
    finishes, so the next replay of the same trace sees it. The state never
    lives on a trace; replay traces are linked to the store they used.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def get(self, name: str, trace_id: str | None = None) -> SandboxStore | None:
        """Read a sandbox store by name, or ``None`` when it does not exist.

        Args:
            name: The store to read.
            trace_id: Read the state this trace starts from: its own entries,
                with the seeds for any sandbox it has none for. ``None``
                (default) reads the seeds.
        """
        params = {"name": name}
        if trace_id is not None:
            params["traceId"] = trace_id
        query = urlencode(params)
        return self._http_client.get(f"{SANDBOX_STORES_PATH}?{query}")["sandboxStore"]

    def seed(self, name: str, sandboxes: Mapping[str, Any]) -> SandboxStore:
        """Put starting state into a sandbox store before any replay uses it.

        Args:
            name: The store to seed, created if it does not exist.
            sandboxes: State by sandbox name, such as
                ``{"Gmail": {"emailAddress": "ceo@acme.com", "messages": [...]}}``.
                Each value takes the shape that sandbox's ``start`` returns
                (for Gmail, a list of messages, one mailbox, or
                ``{"mailboxes": [...]}``; for GitHub, a snapshot). It must be
                JSON. Every trace without its own state for a sandbox starts
                from its seed. A sandbox named here replaces its seed; a
                sandbox left out keeps its seed. State replays already wrote
                for a trace is kept.
        """
        if not sandboxes:
            raise ValueError("sandboxes must name at least one sandbox to seed.")
        return self._http_client.request(
            f"{SANDBOX_STORES_PATH}/seed",
            {"name": name, "sandboxes": dict(sandboxes)},
        )["sandboxStore"]

    def link_traces(self, name: str, trace_ids: Sequence[str]) -> SandboxStoreLink:
        """Link traces to a sandbox store without storing its state on them.

        A replay run with ``sandbox_store`` links its replay traces itself.
        Use this for any other trace that belongs with the store, such as
        the production trace a store was seeded from.
        """
        if not trace_ids:
            raise ValueError("trace_ids must name at least one trace to link.")
        return self._http_client.request(
            f"{SANDBOX_STORES_PATH}/traces",
            {"name": name, "traceIds": list(trace_ids)},
        )

    def list_for_trace(self, trace_id: str) -> list[SandboxStoreSummary]:
        """The sandbox stores a trace is linked to, by name."""
        return self._http_client.get(
            f"/api/sdk/traces/{quote(trace_id, safe='')}/sandboxStores"
        )["sandboxStores"]


def write_sandbox_store(
    http_client: HttpClient, name: str, trace_id: str, sandboxes: dict[str, Any]
) -> list[SandboxStoreEntry]:
    return http_client.request(
        f"{SANDBOX_STORES_PATH}/write",
        {"name": name, "traceId": trace_id, "sandboxes": sandboxes},
    )["entries"]

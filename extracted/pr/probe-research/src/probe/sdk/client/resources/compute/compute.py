"""ComputeMixin, Client's methods: the team's GPU nodes and clusters as their node daemons report them, and
the enrollment tokens that join new nodes (probe-node P0; twin: app/compute)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import quote

from .... import errors


class ComputeMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client.

    Reads and token writes are sent straight, never queued: a token is shown once, and a refusal is the
    answer the caller acts on. Each answer is read tolerantly: a bare list or `{"<items>": [...]}`."""

    def list_compute_nodes(
        self,
        *,
        state: str | None = None,
        capacity: str | None = None,
        provider: str | None = None,
        cluster: str | None = None,
    ) -> list[dict[str, Any]]:
        """``GET /v1/compute/nodes``: the team's nodes, each with its cluster, GPUs and last report."""
        query = {key: value for key, value in (("state", state), ("capacity", capacity),
                                                ("provider", provider), ("cluster", cluster)) if value}
        return get_items(self.transport.get("/v1/compute/nodes", params=query or None), "nodes")

    def get_compute_node(self, node_id: str) -> dict[str, Any]:
        """``GET /v1/compute/nodes/{id}``: one node, each GPU with who is on it."""
        answer = self.transport.get(f"/v1/compute/nodes/{_quote(node_id)}")
        return dict(answer.get("node", answer)) if isinstance(answer, Mapping) else {}

    def list_compute_clusters(self) -> list[dict[str, Any]]:
        """``GET /v1/compute/clusters``."""
        return get_items(self.transport.get("/v1/compute/clusters"), "clusters")

    def list_cluster_machines(self, cluster: str, *, status: str | None = None) -> list[dict[str, Any]]:
        """``GET /v1/compute/clusters/{id or key}/machines``: the machines Probe expects there, with status."""
        query = {"status": status} if status else None
        return get_items(self.transport.get(f"/v1/compute/clusters/{_quote(cluster)}/machines", params=query),
                         "machines")

    def register_cluster_machines(self, page: Mapping[str, Any]) -> dict[str, Any]:
        """``POST /v1/compute/clusters/machines``: one page of a connected cluster's machine list (T7)."""
        return dict(self.transport.post("/v1/compute/clusters/machines", dict(page)) or {})

    def create_enrollment_token(
        self,
        name: str,
        *,
        labels: Mapping[str, str] | None = None,
        max_nodes: int | None = None,
        expires_in_seconds: int | None = None,
        runs_submit_key_id: str | None = None,
    ) -> dict[str, Any]:
        """``POST /v1/compute/enrollment-tokens``: the new token, its secret included this once.
        ``runs_submit_key_id``: a SkyPilot queue reader's server key (yours), revoked with the token's cluster."""
        if not str(name or "").strip():
            raise errors.ValidationError("name the enrollment token")
        body: dict[str, Any] = {"name": str(name).strip()}
        if labels:
            body["labels"] = dict(labels)
        if max_nodes is not None:
            body["max_nodes"] = int(max_nodes)
        if expires_in_seconds is not None:
            body["expires_in_seconds"] = int(expires_in_seconds)
        if runs_submit_key_id:
            body["runs_submit_key_id"] = str(runs_submit_key_id)
        return dict(self.transport.post("/v1/compute/enrollment-tokens", body) or {})

    def list_enrollment_tokens(self) -> list[dict[str, Any]]:
        """``GET /v1/compute/enrollment-tokens``: the team's tokens, never their secrets."""
        return get_items(self.transport.get("/v1/compute/enrollment-tokens"), "tokens")

    def revoke_enrollment_token(self, token_id: str, *, should_revoke_nodes: bool = False) -> None:
        """``DELETE /v1/compute/enrollment-tokens/{id}``: no new node joins with it; joined nodes stay, unless
        ``should_revoke_nodes`` (``?revoke_nodes=true``), which revokes the nodes it enrolled too."""
        query = {"revoke_nodes": "true"} if should_revoke_nodes else None
        self.transport.request("DELETE", f"/v1/compute/enrollment-tokens/{_quote(token_id)}", params=query,
                               idempotent=True)


def get_items(answer: Any, key: str) -> list[dict[str, Any]]:
    """A list answer as is; an object's ``key`` (or ``items``) list; anything else, empty."""
    if isinstance(answer, Mapping):
        answer = answer.get(key, answer.get("items"))
    return [dict(item) for item in answer or () if isinstance(item, Mapping)] if isinstance(answer, list) else []


def _quote(segment: str) -> str:
    value = str(segment or "").strip().removeprefix("id:")
    if not value:
        raise errors.ValidationError("name the node or token: an id can't be empty")
    return quote(value, safe="")

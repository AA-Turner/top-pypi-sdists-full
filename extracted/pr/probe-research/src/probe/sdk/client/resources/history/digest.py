"""DigestResource (client.digest, typed reads) and DigestMixin, Client's methods: the team's research
directions (the digest's tree and one direction's card) and a workspace's digest (twins:
app/generation/directions, app/generation/kinds/workspace_digest)."""

from __future__ import annotations

from .....generated.models import DirectionCard, DirectionTree, WorkspaceDigestOut
from ...resource import Resource


class DigestMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def get_direction_tree(self) -> dict:
        """``GET /v1/directions``: the team's research directions, as the digest groups its work."""
        return self.transport.get("/v1/directions")

    def get_direction(self, direction_id: str) -> dict:
        """``GET /v1/directions/{id}``: one direction's card (its work, findings and next steps)."""
        return self.transport.get(f"/v1/directions/{direction_id}")

    def get_workspace_digest(self, *, workspace_id: str | None = None) -> dict:
        """``GET /v1/workspace-digest``: what changed in a workspace (the caller's default without one)."""
        filters = {"workspace_id": workspace_id} if workspace_id is not None else None
        return self.transport.get("/v1/workspace-digest", params=filters)


class DigestResource(Resource):
    """`client.digest`: typed directions and workspace digest reads."""

    __slots__ = ()

    def get_directions(self) -> DirectionTree:
        """`Client.get_direction_tree` as a `DirectionTree`."""
        return self._to_model(DirectionTree, self._client.get_direction_tree())

    def get_direction(self, direction_id: str) -> DirectionCard:
        """`Client.get_direction` as a `DirectionCard`."""
        return self._to_model(DirectionCard, self._client.get_direction(direction_id))

    def get_workspace(self, *, workspace_id: str | None = None) -> WorkspaceDigestOut:
        """`Client.get_workspace_digest` as a `WorkspaceDigestOut`."""
        return self._to_model(WorkspaceDigestOut, self._client.get_workspace_digest(workspace_id=workspace_id))

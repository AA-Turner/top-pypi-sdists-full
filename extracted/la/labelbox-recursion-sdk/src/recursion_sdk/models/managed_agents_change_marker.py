from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_change_marker_kind import ManagedAgentsChangeMarkerKind
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsChangeMarker")



@_attrs_define
class ManagedAgentsChangeMarker:
    """ Immutable target-agent version or model-change marker aligned with the Overview timeline.

        Example:
            {'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'from_model':
                'example', 'kind': 'agent_version', 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'to_model':
                'example', 'version_number': 1}

        Attributes:
            agent_version_id (UUID): Immutable target-agent version beginning at this marker.
            at (datetime.datetime): UTC timestamp when this immutable agent version was created.
            kind (ManagedAgentsChangeMarkerKind): Whether this marker denotes any version boundary or specifically a model
                change.
            target_agent_id (UUID): Selected target agent whose immutable history supplies the marker.
            version_number (int): Monotonic human-readable version number of the target agent.
            from_model (str | Unset): Model used by the immediately preceding version for a model-change marker.
            to_model (str | Unset): Model introduced by this version for a model-change marker.
     """

    agent_version_id: UUID
    at: datetime.datetime
    kind: ManagedAgentsChangeMarkerKind
    target_agent_id: UUID
    version_number: int
    from_model: str | Unset = UNSET
    to_model: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_version_id = str(self.agent_version_id)

        at = self.at.isoformat()

        kind = self.kind.value

        target_agent_id = str(self.target_agent_id)

        version_number = self.version_number

        from_model = self.from_model

        to_model = self.to_model


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_version_id": agent_version_id,
            "at": at,
            "kind": kind,
            "target_agent_id": target_agent_id,
            "version_number": version_number,
        })
        if from_model is not UNSET:
            field_dict["from_model"] = from_model
        if to_model is not UNSET:
            field_dict["to_model"] = to_model

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_version_id = UUID(d.pop("agent_version_id"))




        at = datetime.datetime.fromisoformat(d.pop("at"))




        kind = ManagedAgentsChangeMarkerKind(d.pop("kind"))




        target_agent_id = UUID(d.pop("target_agent_id"))




        version_number = d.pop("version_number")

        from_model = d.pop("from_model", UNSET)

        to_model = d.pop("to_model", UNSET)

        managed_agents_change_marker = cls(
            agent_version_id=agent_version_id,
            at=at,
            kind=kind,
            target_agent_id=target_agent_id,
            version_number=version_number,
            from_model=from_model,
            to_model=to_model,
        )

        return managed_agents_change_marker


from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_model_cost_node_list_response_scope import ManagedAgentsSessionModelCostNodeListResponseScope
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_session_model_cost_node_response import ManagedAgentsSessionModelCostNodeResponse





T = TypeVar("T", bound="ManagedAgentsSessionModelCostNodeListResponse")



@_attrs_define
class ManagedAgentsSessionModelCostNodeListResponse:
    """ One page of the session hierarchy behind a model-cost read, paginated independently of the attempt detail so a wide
    tree cannot crowd out attempts.

        Example:
            {'model_cost_snapshot_token': 'example', 'next_page_token': 'example', 'read_timestamp': '2026-02-18T09:30:00Z',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_nodes': [{'model_costs':
                {'self': {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'tree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}, 'parent_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'root_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example'}]}

        Attributes:
            model_cost_snapshot_token (str): Signed organization/session/scope-bound token that pins companion model-cost
                reads to this exact snapshot.
            read_timestamp (datetime.datetime): RFC 3339 timestamp of the database snapshot these rollups were read from.
            scope (ManagedAgentsSessionModelCostNodeListResponseScope): How far the hierarchy read reached from that
                session: this session alone (self), this session and its descendants (subtree), or every session under the same
                root (tree).
            session_id (str): Session the read was scoped to (UUID).
            session_nodes (list[ManagedAgentsSessionModelCostNodeResponse] | None): Sessions in scope, ordered by
                session_path then session_id, up to the requested limit.
            next_page_token (str | Unset): Continuation for the next page, passed back as page_token. Absent on the last
                page, and bound to this organization, session, scope, limit, and snapshot.
     """

    model_cost_snapshot_token: str
    read_timestamp: datetime.datetime
    scope: ManagedAgentsSessionModelCostNodeListResponseScope
    session_id: str
    session_nodes: list[ManagedAgentsSessionModelCostNodeResponse] | None
    next_page_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_model_cost_node_response import ManagedAgentsSessionModelCostNodeResponse # noqa: PLC0415
        model_cost_snapshot_token = self.model_cost_snapshot_token

        read_timestamp = self.read_timestamp.isoformat()

        scope = self.scope.value

        session_id = self.session_id

        session_nodes: list[dict[str, Any]] | None
        if isinstance(self.session_nodes, list):
            session_nodes = []
            for session_nodes_type_0_item_data in self.session_nodes:
                session_nodes_type_0_item = session_nodes_type_0_item_data.to_dict()
                session_nodes.append(session_nodes_type_0_item)


        else:
            session_nodes = self.session_nodes

        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "model_cost_snapshot_token": model_cost_snapshot_token,
            "read_timestamp": read_timestamp,
            "scope": scope,
            "session_id": session_id,
            "session_nodes": session_nodes,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_model_cost_node_response import ManagedAgentsSessionModelCostNodeResponse # noqa: PLC0415
        d = dict(src_dict)
        model_cost_snapshot_token = d.pop("model_cost_snapshot_token")

        read_timestamp = datetime.datetime.fromisoformat(d.pop("read_timestamp"))




        scope = ManagedAgentsSessionModelCostNodeListResponseScope(d.pop("scope"))




        session_id = d.pop("session_id")

        def _parse_session_nodes(data: object) -> list[ManagedAgentsSessionModelCostNodeResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                session_nodes_type_0 = []
                _session_nodes_type_0 = data
                for session_nodes_type_0_item_data in (_session_nodes_type_0):
                    session_nodes_type_0_item = ManagedAgentsSessionModelCostNodeResponse.from_dict(session_nodes_type_0_item_data)



                    session_nodes_type_0.append(session_nodes_type_0_item)

                return session_nodes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSessionModelCostNodeResponse] | None, data)

        session_nodes = _parse_session_nodes(d.pop("session_nodes"))


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_session_model_cost_node_list_response = cls(
            model_cost_snapshot_token=model_cost_snapshot_token,
            read_timestamp=read_timestamp,
            scope=scope,
            session_id=session_id,
            session_nodes=session_nodes,
            next_page_token=next_page_token,
        )


        managed_agents_session_model_cost_node_list_response.additional_properties = d
        return managed_agents_session_model_cost_node_list_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

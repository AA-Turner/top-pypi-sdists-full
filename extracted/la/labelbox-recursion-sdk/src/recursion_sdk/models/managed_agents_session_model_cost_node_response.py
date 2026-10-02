from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse





T = TypeVar("T", bound="ManagedAgentsSessionModelCostNodeResponse")



@_attrs_define
class ManagedAgentsSessionModelCostNodeResponse:
    """ One session of a tree with its own model-cost rollups, so a tree total can be attributed to the sessions that
    produced it.

        Example:
            {'model_costs': {'self': {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example',
                'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree':
                {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'tree': {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}, 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'root_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'session_path': 'example'}

        Attributes:
            model_costs (ManagedAgentsSessionModelCostSummariesResponse): One session's three scope rollups, read from a
                single database snapshot so self, subtree, and tree cannot disagree with one another. Example: {'self':
                {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'tree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}.
            root_session_id (str): Root session of the tree this session belongs to (UUID). Equal to session_id for a root
                session.
            session_id (str): Identifier for this session (UUID).
            session_path (str): Position of this session within its tree, as a slash-delimited path of session ids. "/" for
                a root session.
            parent_session_id (str | Unset): Session that created this one (UUID). Empty on a root session.
     """

    model_costs: ManagedAgentsSessionModelCostSummariesResponse
    root_session_id: str
    session_id: str
    session_path: str
    parent_session_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse # noqa: PLC0415
        model_costs = self.model_costs.to_dict()

        root_session_id = self.root_session_id

        session_id = self.session_id

        session_path = self.session_path

        parent_session_id = self.parent_session_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "model_costs": model_costs,
            "root_session_id": root_session_id,
            "session_id": session_id,
            "session_path": session_path,
        })
        if parent_session_id is not UNSET:
            field_dict["parent_session_id"] = parent_session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse # noqa: PLC0415
        d = dict(src_dict)
        model_costs = ManagedAgentsSessionModelCostSummariesResponse.from_dict(d.pop("model_costs"))




        root_session_id = d.pop("root_session_id")

        session_id = d.pop("session_id")

        session_path = d.pop("session_path")

        parent_session_id = d.pop("parent_session_id", UNSET)

        managed_agents_session_model_cost_node_response = cls(
            model_costs=model_costs,
            root_session_id=root_session_id,
            session_id=session_id,
            session_path=session_path,
            parent_session_id=parent_session_id,
        )


        managed_agents_session_model_cost_node_response.additional_properties = d
        return managed_agents_session_model_cost_node_response

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

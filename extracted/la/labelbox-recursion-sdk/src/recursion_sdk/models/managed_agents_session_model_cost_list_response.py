from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse





T = TypeVar("T", bound="ManagedAgentsSessionModelCostListResponse")



@_attrs_define
class ManagedAgentsSessionModelCostListResponse:
    """ Model-cost rollups for a batch of sessions, so a list view can show spend per row without one read per session.

        Example:
            {'session_model_costs': [{'self': {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count':
                'example', 'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree':
                {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'tree': {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}]}

        Attributes:
            session_model_costs (list[ManagedAgentsSessionModelCostSummariesResponse] | None): One entry per requested
                session id, in request order and repeated when an id is asked for more than once. Authorization is all-or-
                nothing: if any requested id is unknown or outside the caller's organization or access policy, the whole request
                returns 404 rather than a short array.
     """

    session_model_costs: list[ManagedAgentsSessionModelCostSummariesResponse] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse # noqa: PLC0415
        session_model_costs: list[dict[str, Any]] | None
        if isinstance(self.session_model_costs, list):
            session_model_costs = []
            for session_model_costs_type_0_item_data in self.session_model_costs:
                session_model_costs_type_0_item = session_model_costs_type_0_item_data.to_dict()
                session_model_costs.append(session_model_costs_type_0_item)


        else:
            session_model_costs = self.session_model_costs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "session_model_costs": session_model_costs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse # noqa: PLC0415
        d = dict(src_dict)
        def _parse_session_model_costs(data: object) -> list[ManagedAgentsSessionModelCostSummariesResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                session_model_costs_type_0 = []
                _session_model_costs_type_0 = data
                for session_model_costs_type_0_item_data in (_session_model_costs_type_0):
                    session_model_costs_type_0_item = ManagedAgentsSessionModelCostSummariesResponse.from_dict(session_model_costs_type_0_item_data)



                    session_model_costs_type_0.append(session_model_costs_type_0_item)

                return session_model_costs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSessionModelCostSummariesResponse] | None, data)

        session_model_costs = _parse_session_model_costs(d.pop("session_model_costs"))


        managed_agents_session_model_cost_list_response = cls(
            session_model_costs=session_model_costs,
        )


        managed_agents_session_model_cost_list_response.additional_properties = d
        return managed_agents_session_model_cost_list_response

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_status import ManagedAgentsSessionStatus
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsEvaluationSelectorRequest")



@_attrs_define
class ManagedAgentsEvaluationSelectorRequest:
    """ A bounded evaluation target selector: explicit session ids, or statuses plus a newest-first limit.

        Example:
            {'limit': 1, 'session_ids': ['example'], 'statuses': ['active']}

        Attributes:
            limit (int | Unset): Maximum newest matching sessions selected by statuses.
            session_ids (list[str] | Unset): Explicit target session ids. Every id must be an eligible session visible to
                the caller or no run is created.
            statuses (list[ManagedAgentsSessionStatus] | Unset): Eligible target statuses. Used with limit to choose the
                newest matching sessions.
     """

    limit: int | Unset = UNSET
    session_ids: list[str] | Unset = UNSET
    statuses: list[ManagedAgentsSessionStatus] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        session_ids: list[str] | Unset = UNSET
        if not isinstance(self.session_ids, Unset):
            session_ids = self.session_ids



        statuses: list[str] | Unset = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = []
            for statuses_item_data in self.statuses:
                statuses_item = statuses_item_data.value
                statuses.append(statuses_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if limit is not UNSET:
            field_dict["limit"] = limit
        if session_ids is not UNSET:
            field_dict["session_ids"] = session_ids
        if statuses is not UNSET:
            field_dict["statuses"] = statuses

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit", UNSET)

        session_ids = cast(list[str], d.pop("session_ids", UNSET))


        _statuses = d.pop("statuses", UNSET)
        statuses: list[ManagedAgentsSessionStatus] | Unset = UNSET
        if _statuses is not UNSET:
            statuses = []
            for statuses_item_data in _statuses:
                statuses_item = ManagedAgentsSessionStatus(statuses_item_data)



                statuses.append(statuses_item)


        managed_agents_evaluation_selector_request = cls(
            limit=limit,
            session_ids=session_ids,
            statuses=statuses,
        )


        managed_agents_evaluation_selector_request.additional_properties = d
        return managed_agents_evaluation_selector_request

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

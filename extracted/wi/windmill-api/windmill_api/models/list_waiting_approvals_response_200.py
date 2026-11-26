from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_waiting_approvals_response_200_approvals_item import ListWaitingApprovalsResponse200ApprovalsItem


T = TypeVar("T", bound="ListWaitingApprovalsResponse200")


@_attrs_define
class ListWaitingApprovalsResponse200:
    """
    Attributes:
        approvals (List['ListWaitingApprovalsResponse200ApprovalsItem']): the most recent of the listed runs, at most
            100
        total (int): how many runs are listed in all
    """

    approvals: List["ListWaitingApprovalsResponse200ApprovalsItem"]
    total: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approvals = []
        for approvals_item_data in self.approvals:
            approvals_item = approvals_item_data.to_dict()

            approvals.append(approvals_item)

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "approvals": approvals,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_waiting_approvals_response_200_approvals_item import (
            ListWaitingApprovalsResponse200ApprovalsItem,
        )

        d = src_dict.copy()
        approvals = []
        _approvals = d.pop("approvals")
        for approvals_item_data in _approvals:
            approvals_item = ListWaitingApprovalsResponse200ApprovalsItem.from_dict(approvals_item_data)

            approvals.append(approvals_item)

        total = d.pop("total")

        list_waiting_approvals_response_200 = cls(
            approvals=approvals,
            total=total,
        )

        list_waiting_approvals_response_200.additional_properties = d
        return list_waiting_approvals_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

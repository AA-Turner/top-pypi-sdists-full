from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_nested_approvals_response_200_approvals_item import ListNestedApprovalsResponse200ApprovalsItem


T = TypeVar("T", bound="ListNestedApprovalsResponse200")


@_attrs_define
class ListNestedApprovalsResponse200:
    """
    Attributes:
        approvals (List['ListNestedApprovalsResponse200ApprovalsItem']):
        more (bool): more nested runs than are read, typically a loop with an approval in every iteration: their
            approvals are on those runs' own pages
    """

    approvals: List["ListNestedApprovalsResponse200ApprovalsItem"]
    more: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approvals = []
        for approvals_item_data in self.approvals:
            approvals_item = approvals_item_data.to_dict()

            approvals.append(approvals_item)

        more = self.more

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "approvals": approvals,
                "more": more,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_nested_approvals_response_200_approvals_item import (
            ListNestedApprovalsResponse200ApprovalsItem,
        )

        d = src_dict.copy()
        approvals = []
        _approvals = d.pop("approvals")
        for approvals_item_data in _approvals:
            approvals_item = ListNestedApprovalsResponse200ApprovalsItem.from_dict(approvals_item_data)

            approvals.append(approvals_item)

        more = d.pop("more")

        list_nested_approvals_response_200 = cls(
            approvals=approvals,
            more=more,
        )

        list_nested_approvals_response_200.additional_properties = d
        return list_nested_approvals_response_200

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

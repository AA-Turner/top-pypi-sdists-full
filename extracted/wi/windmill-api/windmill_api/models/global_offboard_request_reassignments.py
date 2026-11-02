from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.global_offboard_request_reassignments_additional_property import (
        GlobalOffboardRequestReassignmentsAdditionalProperty,
    )


T = TypeVar("T", bound="GlobalOffboardRequestReassignments")


@_attrs_define
class GlobalOffboardRequestReassignments:
    """Map of workspace_id to reassignment config"""

    additional_properties: Dict[str, "GlobalOffboardRequestReassignmentsAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.global_offboard_request_reassignments_additional_property import (
            GlobalOffboardRequestReassignmentsAdditionalProperty,
        )

        d = src_dict.copy()
        global_offboard_request_reassignments = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GlobalOffboardRequestReassignmentsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        global_offboard_request_reassignments.additional_properties = additional_properties
        return global_offboard_request_reassignments

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GlobalOffboardRequestReassignmentsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GlobalOffboardRequestReassignmentsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_external_instance_pg_status_response_200_last_setup_steps_item_status import (
    GetExternalInstancePgStatusResponse200LastSetupStepsItemStatus,
)

T = TypeVar("T", bound="GetExternalInstancePgStatusResponse200LastSetupStepsItem")


@_attrs_define
class GetExternalInstancePgStatusResponse200LastSetupStepsItem:
    """
    Attributes:
        name (str):
        status (GetExternalInstancePgStatusResponse200LastSetupStepsItemStatus):
        message (str):
    """

    name: str
    status: GetExternalInstancePgStatusResponse200LastSetupStepsItemStatus
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        status = self.status.value

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "status": status,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        status = GetExternalInstancePgStatusResponse200LastSetupStepsItemStatus(d.pop("status"))

        message = d.pop("message")

        get_external_instance_pg_status_response_200_last_setup_steps_item = cls(
            name=name,
            status=status,
            message=message,
        )

        get_external_instance_pg_status_response_200_last_setup_steps_item.additional_properties = d
        return get_external_instance_pg_status_response_200_last_setup_steps_item

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

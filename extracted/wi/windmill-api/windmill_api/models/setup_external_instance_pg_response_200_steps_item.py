from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.setup_external_instance_pg_response_200_steps_item_status import (
    SetupExternalInstancePgResponse200StepsItemStatus,
)

T = TypeVar("T", bound="SetupExternalInstancePgResponse200StepsItem")


@_attrs_define
class SetupExternalInstancePgResponse200StepsItem:
    """
    Attributes:
        name (str):
        status (SetupExternalInstancePgResponse200StepsItemStatus):
        message (str):
    """

    name: str
    status: SetupExternalInstancePgResponse200StepsItemStatus
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

        status = SetupExternalInstancePgResponse200StepsItemStatus(d.pop("status"))

        message = d.pop("message")

        setup_external_instance_pg_response_200_steps_item = cls(
            name=name,
            status=status,
            message=message,
        )

        setup_external_instance_pg_response_200_steps_item.additional_properties = d
        return setup_external_instance_pg_response_200_steps_item

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

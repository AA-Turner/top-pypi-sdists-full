from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.external_instance_pg_setup_step_status import ExternalInstancePgSetupStepStatus

T = TypeVar("T", bound="ExternalInstancePgSetupStep")


@_attrs_define
class ExternalInstancePgSetupStep:
    """
    Attributes:
        name (str):
        status (ExternalInstancePgSetupStepStatus):
        message (str):
    """

    name: str
    status: ExternalInstancePgSetupStepStatus
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

        status = ExternalInstancePgSetupStepStatus(d.pop("status"))

        message = d.pop("message")

        external_instance_pg_setup_step = cls(
            name=name,
            status=status,
            message=message,
        )

        external_instance_pg_setup_step.additional_properties = d
        return external_instance_pg_setup_step

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

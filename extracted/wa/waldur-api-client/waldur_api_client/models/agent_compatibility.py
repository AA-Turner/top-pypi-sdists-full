from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_compatibility_status_enum import AgentCompatibilityStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentCompatibility")


@_attrs_define
class AgentCompatibility:
    """
    Attributes:
        status (AgentCompatibilityStatusEnum):
        message (str):
        minimum_required (Union[Unset, str]):
    """

    status: AgentCompatibilityStatusEnum
    message: str
    minimum_required: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message = self.message

        minimum_required = self.minimum_required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
            }
        )
        if minimum_required is not UNSET:
            field_dict["minimum_required"] = minimum_required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = AgentCompatibilityStatusEnum(d.pop("status"))

        message = d.pop("message")

        minimum_required = d.pop("minimum_required", UNSET)

        agent_compatibility = cls(
            status=status,
            message=message,
            minimum_required=minimum_required,
        )

        agent_compatibility.additional_properties = d
        return agent_compatibility

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

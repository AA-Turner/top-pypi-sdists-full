from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.membership_control_enum import MembershipControlEnum

T = TypeVar("T", bound="SetMembershipControlRequest")


@_attrs_define
class SetMembershipControlRequest:
    """
    Attributes:
        membership_control (Union[MembershipControlEnum, None]):
    """

    membership_control: Union[MembershipControlEnum, None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        membership_control: Union[None, str]
        if isinstance(self.membership_control, MembershipControlEnum):
            membership_control = self.membership_control.value
        else:
            membership_control = self.membership_control

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "membership_control": membership_control,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_membership_control(data: object) -> Union[MembershipControlEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                membership_control_type_0 = MembershipControlEnum(data)

                return membership_control_type_0
            except:  # noqa: E722
                pass
            return cast(Union[MembershipControlEnum, None], data)

        membership_control = _parse_membership_control(d.pop("membership_control"))

        set_membership_control_request = cls(
            membership_control=membership_control,
        )

        set_membership_control_request.additional_properties = d
        return set_membership_control_request

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

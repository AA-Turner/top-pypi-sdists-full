from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateActionsRequest")


@_attrs_define
class UpdateActionsRequest:
    """
    Attributes:
        provider_action_type (Union[None, Unset, str]): Optional provider action type to update. If not provided,
            updates all providers.
    """

    provider_action_type: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider_action_type: Union[None, Unset, str]
        if isinstance(self.provider_action_type, Unset):
            provider_action_type = UNSET
        else:
            provider_action_type = self.provider_action_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider_action_type is not UNSET:
            field_dict["provider_action_type"] = provider_action_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_provider_action_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provider_action_type = _parse_provider_action_type(d.pop("provider_action_type", UNSET))

        update_actions_request = cls(
            provider_action_type=provider_action_type,
        )

        update_actions_request.additional_properties = d
        return update_actions_request

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

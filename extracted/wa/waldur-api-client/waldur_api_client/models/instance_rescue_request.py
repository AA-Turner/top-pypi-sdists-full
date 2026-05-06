from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstanceRescueRequest")


@_attrs_define
class InstanceRescueRequest:
    """
    Attributes:
        rescue_image (Union[None, Unset, str]): Optional rescue image. Required for volume-backed instances; must be a
            Glance image with hw_rescue_device or hw_rescue_bus set (a 'stable device rescue' image).
    """

    rescue_image: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rescue_image: Union[None, Unset, str]
        if isinstance(self.rescue_image, Unset):
            rescue_image = UNSET
        else:
            rescue_image = self.rescue_image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rescue_image is not UNSET:
            field_dict["rescue_image"] = rescue_image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rescue_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rescue_image = _parse_rescue_image(d.pop("rescue_image", UNSET))

        instance_rescue_request = cls(
            rescue_image=rescue_image,
        )

        instance_rescue_request.additional_properties = d
        return instance_rescue_request

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

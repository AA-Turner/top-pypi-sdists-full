from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingProfileBindRequest")


@_attrs_define
class OfferingProfileBindRequest:
    """
    Attributes:
        profile (Union[None, UUID, Unset]): OfferingProfile UUID to bind to. Pass null to unbind.
    """

    profile: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile: Union[None, Unset, str]
        if isinstance(self.profile, Unset):
            profile = UNSET
        elif isinstance(self.profile, UUID):
            profile = str(self.profile)
        else:
            profile = self.profile

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_profile(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                profile_type_0 = UUID(data)

                return profile_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        profile = _parse_profile(d.pop("profile", UNSET))

        offering_profile_bind_request = cls(
            profile=profile,
        )

        offering_profile_bind_request.additional_properties = d
        return offering_profile_bind_request

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.services_status_list_dto_item_details_additional_property_type_5 import ServicesStatusListDtoItemDetailsAdditionalPropertyType5





T = TypeVar("T", bound="ServicesStatusListDtoItemDetails")



@_attrs_define
class ServicesStatusListDtoItemDetails:
    """ Provider-specific status payload (HTTP code, latency, error message, etc.).

     """

    additional_properties: dict[str, bool | float | list[Any] | None | ServicesStatusListDtoItemDetailsAdditionalPropertyType5 | str] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.services_status_list_dto_item_details_additional_property_type_5 import ServicesStatusListDtoItemDetailsAdditionalPropertyType5 # noqa: PLC0415
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            
            if isinstance(prop, list):
                field_dict[prop_name] = prop


            elif isinstance(prop, ServicesStatusListDtoItemDetailsAdditionalPropertyType5):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.services_status_list_dto_item_details_additional_property_type_5 import ServicesStatusListDtoItemDetailsAdditionalPropertyType5 # noqa: PLC0415
        d = dict(src_dict)
        services_status_list_dto_item_details = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            def _parse_additional_property(data: object) -> bool | float | list[Any] | None | ServicesStatusListDtoItemDetailsAdditionalPropertyType5 | str:
                if data is None:
                    return data
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_4 = cast(list[Any], data)

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_5 = ServicesStatusListDtoItemDetailsAdditionalPropertyType5.from_dict(data)



                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(bool | float | list[Any] | None | ServicesStatusListDtoItemDetailsAdditionalPropertyType5 | str, data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        services_status_list_dto_item_details.additional_properties = additional_properties
        return services_status_list_dto_item_details

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> bool | float | list[Any] | None | ServicesStatusListDtoItemDetailsAdditionalPropertyType5 | str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: bool | float | list[Any] | None | ServicesStatusListDtoItemDetailsAdditionalPropertyType5 | str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

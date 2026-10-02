from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_mapping import OfferingMapping


T = TypeVar("T", bound="OfferingMappingMap")


@_attrs_define
class OfferingMappingMap:
    """
    Attributes:
        field_ (Union['OfferingMapping', None]):
    """

    field_: Union["OfferingMapping", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.offering_mapping import OfferingMapping

        field_: Union[None, dict[str, Any]]
        if isinstance(self.field_, OfferingMapping):
            field_ = self.field_.to_dict()
        else:
            field_ = self.field_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "*": field_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_mapping import OfferingMapping

        d = dict(src_dict)

        def _parse_field_(data: object) -> Union["OfferingMapping", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                type_1 = OfferingMapping.from_dict(data)

                return type_1
            except:  # noqa: E722
                pass
            return cast(Union["OfferingMapping", None], data)

        field_ = _parse_field_(d.pop("*"))

        offering_mapping_map = cls(
            field_=field_,
        )

        offering_mapping_map.additional_properties = d
        return offering_mapping_map

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

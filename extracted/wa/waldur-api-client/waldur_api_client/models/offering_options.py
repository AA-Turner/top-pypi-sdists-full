from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_options_options import OfferingOptionsOptions


T = TypeVar("T", bound="OfferingOptions")


@_attrs_define
class OfferingOptions:
    """
    Attributes:
        order (Union[Unset, list[str]]):
        options (Union[Unset, OfferingOptionsOptions]):
    """

    order: Union[Unset, list[str]] = UNSET
    options: Union[Unset, "OfferingOptionsOptions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order: Union[Unset, list[str]] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_options_options import OfferingOptionsOptions

        d = dict(src_dict)
        order = cast(list[str], d.pop("order", UNSET))

        _options = d.pop("options", UNSET)
        options: Union[Unset, OfferingOptionsOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = OfferingOptionsOptions.from_dict(_options)

        offering_options = cls(
            order=order,
            options=options,
        )

        offering_options.additional_properties = d
        return offering_options

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

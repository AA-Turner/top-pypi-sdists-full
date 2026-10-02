from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_type_enum import AttributeTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attribute_request_default_type_0 import AttributeRequestDefaultType0


T = TypeVar("T", bound="AttributeRequest")


@_attrs_define
class AttributeRequest:
    """
    Attributes:
        key (str):
        title (str):
        section (str):
        type_ (AttributeTypeEnum):
        required (Union[Unset, bool]): A value must be provided for the attribute.
        default (Union['AttributeRequestDefaultType0', None, Unset]):
    """

    key: str
    title: str
    section: str
    type_: AttributeTypeEnum
    required: Union[Unset, bool] = UNSET
    default: Union["AttributeRequestDefaultType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.attribute_request_default_type_0 import AttributeRequestDefaultType0

        key = self.key

        title = self.title

        section = self.section

        type_ = self.type_.value

        required = self.required

        default: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default, Unset):
            default = UNSET
        elif isinstance(self.default, AttributeRequestDefaultType0):
            default = self.default.to_dict()
        else:
            default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "title": title,
                "section": section,
                "type": type_,
            }
        )
        if required is not UNSET:
            field_dict["required"] = required
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attribute_request_default_type_0 import AttributeRequestDefaultType0

        d = dict(src_dict)
        key = d.pop("key")

        title = d.pop("title")

        section = d.pop("section")

        type_ = AttributeTypeEnum(d.pop("type"))

        required = d.pop("required", UNSET)

        def _parse_default(data: object) -> Union["AttributeRequestDefaultType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_type_0 = AttributeRequestDefaultType0.from_dict(data)

                return default_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AttributeRequestDefaultType0", None, Unset], data)

        default = _parse_default(d.pop("default", UNSET))

        attribute_request = cls(
            key=key,
            title=title,
            section=section,
            type_=type_,
            required=required,
            default=default,
        )

        attribute_request.additional_properties = d
        return attribute_request

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

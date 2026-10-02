from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_type_enum import AttributeTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_attribute_request_default_type_0 import PatchedAttributeRequestDefaultType0


T = TypeVar("T", bound="PatchedAttributeRequest")


@_attrs_define
class PatchedAttributeRequest:
    """
    Attributes:
        key (Union[Unset, str]):
        title (Union[Unset, str]):
        section (Union[Unset, str]):
        type_ (Union[Unset, AttributeTypeEnum]):
        required (Union[Unset, bool]): A value must be provided for the attribute.
        default (Union['PatchedAttributeRequestDefaultType0', None, Unset]):
    """

    key: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    section: Union[Unset, str] = UNSET
    type_: Union[Unset, AttributeTypeEnum] = UNSET
    required: Union[Unset, bool] = UNSET
    default: Union["PatchedAttributeRequestDefaultType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.patched_attribute_request_default_type_0 import PatchedAttributeRequestDefaultType0

        key = self.key

        title = self.title

        section = self.section

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        required = self.required

        default: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default, Unset):
            default = UNSET
        elif isinstance(self.default, PatchedAttributeRequestDefaultType0):
            default = self.default.to_dict()
        else:
            default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if title is not UNSET:
            field_dict["title"] = title
        if section is not UNSET:
            field_dict["section"] = section
        if type_ is not UNSET:
            field_dict["type"] = type_
        if required is not UNSET:
            field_dict["required"] = required
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_attribute_request_default_type_0 import PatchedAttributeRequestDefaultType0

        d = dict(src_dict)
        key = d.pop("key", UNSET)

        title = d.pop("title", UNSET)

        section = d.pop("section", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AttributeTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AttributeTypeEnum(_type_)

        required = d.pop("required", UNSET)

        def _parse_default(data: object) -> Union["PatchedAttributeRequestDefaultType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_type_0 = PatchedAttributeRequestDefaultType0.from_dict(data)

                return default_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PatchedAttributeRequestDefaultType0", None, Unset], data)

        default = _parse_default(d.pop("default", UNSET))

        patched_attribute_request = cls(
            key=key,
            title=title,
            section=section,
            type_=type_,
            required=required,
            default=default,
        )

        patched_attribute_request.additional_properties = d
        return patched_attribute_request

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

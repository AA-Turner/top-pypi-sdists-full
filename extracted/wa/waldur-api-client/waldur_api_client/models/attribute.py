import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.attribute_type_enum import AttributeTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attribute_default_type_0 import AttributeDefaultType0


T = TypeVar("T", bound="Attribute")


@_attrs_define
class Attribute:
    """
    Attributes:
        url (str):
        uuid (UUID):
        key (str):
        created (datetime.datetime):
        title (str):
        section (str):
        section_title (str):
        type_ (AttributeTypeEnum):
        required (Union[Unset, bool]): A value must be provided for the attribute.
        default (Union['AttributeDefaultType0', None, Unset]):
    """

    url: str
    uuid: UUID
    key: str
    created: datetime.datetime
    title: str
    section: str
    section_title: str
    type_: AttributeTypeEnum
    required: Union[Unset, bool] = UNSET
    default: Union["AttributeDefaultType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.attribute_default_type_0 import AttributeDefaultType0

        url = self.url

        uuid = str(self.uuid)

        key = self.key

        created = self.created.isoformat()

        title = self.title

        section = self.section

        section_title = self.section_title

        type_ = self.type_.value

        required = self.required

        default: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default, Unset):
            default = UNSET
        elif isinstance(self.default, AttributeDefaultType0):
            default = self.default.to_dict()
        else:
            default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "key": key,
                "created": created,
                "title": title,
                "section": section,
                "section_title": section_title,
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
        from ..models.attribute_default_type_0 import AttributeDefaultType0

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        key = d.pop("key")

        created = isoparse(d.pop("created"))

        title = d.pop("title")

        section = d.pop("section")

        section_title = d.pop("section_title")

        type_ = AttributeTypeEnum(d.pop("type"))

        required = d.pop("required", UNSET)

        def _parse_default(data: object) -> Union["AttributeDefaultType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_type_0 = AttributeDefaultType0.from_dict(data)

                return default_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AttributeDefaultType0", None, Unset], data)

        default = _parse_default(d.pop("default", UNSET))

        attribute = cls(
            url=url,
            uuid=uuid,
            key=key,
            created=created,
            title=title,
            section=section,
            section_title=section_title,
            type_=type_,
            required=required,
            default=default,
        )

        attribute.additional_properties = d
        return attribute

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

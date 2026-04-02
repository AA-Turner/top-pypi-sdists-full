from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="OrderAttachmentRequestForm")


@_attrs_define
class OrderAttachmentRequestForm:
    """
    Attributes:
        attachment (Union[File, None, Unset]):
    """

    attachment: Union[File, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attachment: Union[None, Unset, types.FileTypes]
        if isinstance(self.attachment, Unset):
            attachment = UNSET
        elif isinstance(self.attachment, File):
            attachment = self.attachment.to_tuple()

        else:
            attachment = self.attachment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attachment is not UNSET:
            field_dict["attachment"] = attachment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_attachment(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                attachment_type_0 = File(payload=BytesIO(data))

                return attachment_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        attachment = _parse_attachment(d.pop("attachment", UNSET))

        order_attachment_request_form = cls(
            attachment=attachment,
        )

        order_attachment_request_form.additional_properties = d
        return order_attachment_request_form

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

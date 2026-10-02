from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="OrderProviderInfoRequestMultipart")


@_attrs_define
class OrderProviderInfoRequestMultipart:
    """
    Attributes:
        provider_message (Union[Unset, str]):
        provider_message_url (Union[Unset, str]):
        provider_message_attachment (Union[Unset, File]):
    """

    provider_message: Union[Unset, str] = UNSET
    provider_message_url: Union[Unset, str] = UNSET
    provider_message_attachment: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider_message = self.provider_message

        provider_message_url = self.provider_message_url

        provider_message_attachment: Union[Unset, types.FileTypes] = UNSET
        if not isinstance(self.provider_message_attachment, Unset):
            provider_message_attachment = self.provider_message_attachment.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider_message is not UNSET:
            field_dict["provider_message"] = provider_message
        if provider_message_url is not UNSET:
            field_dict["provider_message_url"] = provider_message_url
        if provider_message_attachment is not UNSET:
            field_dict["provider_message_attachment"] = provider_message_attachment

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.provider_message, Unset):
            files.append(("provider_message", (None, str(self.provider_message).encode(), "text/plain")))

        if not isinstance(self.provider_message_url, Unset):
            files.append(("provider_message_url", (None, str(self.provider_message_url).encode(), "text/plain")))

        if not isinstance(self.provider_message_attachment, Unset):
            files.append(("provider_message_attachment", self.provider_message_attachment.to_tuple()))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_message = d.pop("provider_message", UNSET)

        provider_message_url = d.pop("provider_message_url", UNSET)

        _provider_message_attachment = d.pop("provider_message_attachment", UNSET)
        provider_message_attachment: Union[Unset, File]
        if isinstance(_provider_message_attachment, Unset):
            provider_message_attachment = UNSET
        else:
            provider_message_attachment = File(payload=BytesIO(_provider_message_attachment))

        order_provider_info_request_multipart = cls(
            provider_message=provider_message,
            provider_message_url=provider_message_url,
            provider_message_attachment=provider_message_attachment,
        )

        order_provider_info_request_multipart.additional_properties = d
        return order_provider_info_request_multipart

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

from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingUserServiceProviderComment")


@_attrs_define
class OfferingUserServiceProviderComment:
    """
    Attributes:
        service_provider_comment (Union[Unset, str]):
        service_provider_comment_url (Union[Unset, str]): URL link for additional information or actions related to
            service provider comment
    """

    service_provider_comment: Union[Unset, str] = UNSET
    service_provider_comment_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_provider_comment = self.service_provider_comment

        service_provider_comment_url = self.service_provider_comment_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service_provider_comment is not UNSET:
            field_dict["service_provider_comment"] = service_provider_comment
        if service_provider_comment_url is not UNSET:
            field_dict["service_provider_comment_url"] = service_provider_comment_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_provider_comment = d.pop("service_provider_comment", UNSET)

        service_provider_comment_url = d.pop("service_provider_comment_url", UNSET)

        offering_user_service_provider_comment = cls(
            service_provider_comment=service_provider_comment,
            service_provider_comment_url=service_provider_comment_url,
        )

        offering_user_service_provider_comment.additional_properties = d
        return offering_user_service_provider_comment

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

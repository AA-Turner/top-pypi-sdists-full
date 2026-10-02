from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerProfilesConnectOrcidRetrieveResponse200")


@_attrs_define
class ReviewerProfilesConnectOrcidRetrieveResponse200:
    """
    Attributes:
        authorization_url (Union[Unset, str]):
    """

    authorization_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        authorization_url = self.authorization_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if authorization_url is not UNSET:
            field_dict["authorization_url"] = authorization_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        authorization_url = d.pop("authorization_url", UNSET)

        reviewer_profiles_connect_orcid_retrieve_response_200 = cls(
            authorization_url=authorization_url,
        )

        reviewer_profiles_connect_orcid_retrieve_response_200.additional_properties = d
        return reviewer_profiles_connect_orcid_retrieve_response_200

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

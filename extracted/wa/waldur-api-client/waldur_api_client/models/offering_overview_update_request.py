from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingOverviewUpdateRequest")


@_attrs_define
class OfferingOverviewUpdateRequest:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        full_description (Union[Unset, str]):
        privacy_policy_link (Union[Unset, str]):
        access_url (Union[Unset, str]): Publicly accessible offering access URL
        getting_started (Union[Unset, str]):
        integration_guide (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
    """

    name: str
    description: Union[Unset, str] = UNSET
    full_description: Union[Unset, str] = UNSET
    privacy_policy_link: Union[Unset, str] = UNSET
    access_url: Union[Unset, str] = UNSET
    getting_started: Union[Unset, str] = UNSET
    integration_guide: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        full_description = self.full_description

        privacy_policy_link = self.privacy_policy_link

        access_url = self.access_url

        getting_started = self.getting_started

        integration_guide = self.integration_guide

        slug = self.slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if full_description is not UNSET:
            field_dict["full_description"] = full_description
        if privacy_policy_link is not UNSET:
            field_dict["privacy_policy_link"] = privacy_policy_link
        if access_url is not UNSET:
            field_dict["access_url"] = access_url
        if getting_started is not UNSET:
            field_dict["getting_started"] = getting_started
        if integration_guide is not UNSET:
            field_dict["integration_guide"] = integration_guide
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        full_description = d.pop("full_description", UNSET)

        privacy_policy_link = d.pop("privacy_policy_link", UNSET)

        access_url = d.pop("access_url", UNSET)

        getting_started = d.pop("getting_started", UNSET)

        integration_guide = d.pop("integration_guide", UNSET)

        slug = d.pop("slug", UNSET)

        offering_overview_update_request = cls(
            name=name,
            description=description,
            full_description=full_description,
            privacy_policy_link=privacy_policy_link,
            access_url=access_url,
            getting_started=getting_started,
            integration_guide=integration_guide,
            slug=slug,
        )

        offering_overview_update_request.additional_properties = d
        return offering_overview_update_request

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

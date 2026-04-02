import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_group import OrganizationGroup


T = TypeVar("T", bound="GoogleCredentials")


@_attrs_define
class GoogleCredentials:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        enable_notifications (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        customer_image (Union[Unset, str]):
        customer_abbreviation (Union[Unset, str]):
        customer_slug (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_country (Union[Unset, str]):
        image (Union[None, Unset, str]):
        organization_groups (Union[Unset, list['OrganizationGroup']]):
        offering_count (Union[Unset, int]):
        allowed_domains (Union[Unset, Any]): List of allowed domains for offering endpoints. Only staff can modify this
            field.
        calendar_token (Union[Unset, str]):
        calendar_refresh_token (Union[Unset, str]):
        google_auth_url (Union[Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    enable_notifications: Union[Unset, bool] = UNSET
    customer: Union[Unset, str] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_image: Union[Unset, str] = UNSET
    customer_abbreviation: Union[Unset, str] = UNSET
    customer_slug: Union[Unset, str] = UNSET
    customer_native_name: Union[Unset, str] = UNSET
    customer_country: Union[Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    organization_groups: Union[Unset, list["OrganizationGroup"]] = UNSET
    offering_count: Union[Unset, int] = UNSET
    allowed_domains: Union[Unset, Any] = UNSET
    calendar_token: Union[Unset, str] = UNSET
    calendar_refresh_token: Union[Unset, str] = UNSET
    google_auth_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        description = self.description

        enable_notifications = self.enable_notifications

        customer = self.customer

        customer_name = self.customer_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_image = self.customer_image

        customer_abbreviation = self.customer_abbreviation

        customer_slug = self.customer_slug

        customer_native_name = self.customer_native_name

        customer_country = self.customer_country

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        organization_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = []
            for organization_groups_item_data in self.organization_groups:
                organization_groups_item = organization_groups_item_data.to_dict()
                organization_groups.append(organization_groups_item)

        offering_count = self.offering_count

        allowed_domains = self.allowed_domains

        calendar_token = self.calendar_token

        calendar_refresh_token = self.calendar_refresh_token

        google_auth_url = self.google_auth_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if description is not UNSET:
            field_dict["description"] = description
        if enable_notifications is not UNSET:
            field_dict["enable_notifications"] = enable_notifications
        if customer is not UNSET:
            field_dict["customer"] = customer
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_image is not UNSET:
            field_dict["customer_image"] = customer_image
        if customer_abbreviation is not UNSET:
            field_dict["customer_abbreviation"] = customer_abbreviation
        if customer_slug is not UNSET:
            field_dict["customer_slug"] = customer_slug
        if customer_native_name is not UNSET:
            field_dict["customer_native_name"] = customer_native_name
        if customer_country is not UNSET:
            field_dict["customer_country"] = customer_country
        if image is not UNSET:
            field_dict["image"] = image
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if offering_count is not UNSET:
            field_dict["offering_count"] = offering_count
        if allowed_domains is not UNSET:
            field_dict["allowed_domains"] = allowed_domains
        if calendar_token is not UNSET:
            field_dict["calendar_token"] = calendar_token
        if calendar_refresh_token is not UNSET:
            field_dict["calendar_refresh_token"] = calendar_refresh_token
        if google_auth_url is not UNSET:
            field_dict["google_auth_url"] = google_auth_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_group import OrganizationGroup

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        description = d.pop("description", UNSET)

        enable_notifications = d.pop("enable_notifications", UNSET)

        customer = d.pop("customer", UNSET)

        customer_name = d.pop("customer_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_image = d.pop("customer_image", UNSET)

        customer_abbreviation = d.pop("customer_abbreviation", UNSET)

        customer_slug = d.pop("customer_slug", UNSET)

        customer_native_name = d.pop("customer_native_name", UNSET)

        customer_country = d.pop("customer_country", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        organization_groups = []
        _organization_groups = d.pop("organization_groups", UNSET)
        for organization_groups_item_data in _organization_groups or []:
            organization_groups_item = OrganizationGroup.from_dict(organization_groups_item_data)

            organization_groups.append(organization_groups_item)

        offering_count = d.pop("offering_count", UNSET)

        allowed_domains = d.pop("allowed_domains", UNSET)

        calendar_token = d.pop("calendar_token", UNSET)

        calendar_refresh_token = d.pop("calendar_refresh_token", UNSET)

        google_auth_url = d.pop("google_auth_url", UNSET)

        google_credentials = cls(
            url=url,
            uuid=uuid,
            created=created,
            description=description,
            enable_notifications=enable_notifications,
            customer=customer,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            customer_image=customer_image,
            customer_abbreviation=customer_abbreviation,
            customer_slug=customer_slug,
            customer_native_name=customer_native_name,
            customer_country=customer_country,
            image=image,
            organization_groups=organization_groups,
            offering_count=offering_count,
            allowed_domains=allowed_domains,
            calendar_token=calendar_token,
            calendar_refresh_token=calendar_refresh_token,
            google_auth_url=google_auth_url,
        )

        google_credentials.additional_properties = d
        return google_credentials

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

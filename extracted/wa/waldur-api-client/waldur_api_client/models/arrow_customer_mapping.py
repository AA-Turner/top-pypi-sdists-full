import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowCustomerMapping")


@_attrs_define
class ArrowCustomerMapping:
    """
    Attributes:
        uuid (UUID):
        url (str):
        settings (str):
        settings_uuid (UUID):
        arrow_reference (str): Arrow customer ID (e.g., 'XSP661245')
        waldur_customer (str):
        waldur_customer_uuid (UUID):
        waldur_customer_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        arrow_company_name (Union[Unset, str]): Arrow company name
        is_active (Union[Unset, bool]): Whether this mapping is active
    """

    uuid: UUID
    url: str
    settings: str
    settings_uuid: UUID
    arrow_reference: str
    waldur_customer: str
    waldur_customer_uuid: UUID
    waldur_customer_name: str
    created: datetime.datetime
    modified: datetime.datetime
    arrow_company_name: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        settings = self.settings

        settings_uuid = str(self.settings_uuid)

        arrow_reference = self.arrow_reference

        waldur_customer = self.waldur_customer

        waldur_customer_uuid = str(self.waldur_customer_uuid)

        waldur_customer_name = self.waldur_customer_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        arrow_company_name = self.arrow_company_name

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "settings": settings,
                "settings_uuid": settings_uuid,
                "arrow_reference": arrow_reference,
                "waldur_customer": waldur_customer,
                "waldur_customer_uuid": waldur_customer_uuid,
                "waldur_customer_name": waldur_customer_name,
                "created": created,
                "modified": modified,
            }
        )
        if arrow_company_name is not UNSET:
            field_dict["arrow_company_name"] = arrow_company_name
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        settings = d.pop("settings")

        settings_uuid = UUID(d.pop("settings_uuid"))

        arrow_reference = d.pop("arrow_reference")

        waldur_customer = d.pop("waldur_customer")

        waldur_customer_uuid = UUID(d.pop("waldur_customer_uuid"))

        waldur_customer_name = d.pop("waldur_customer_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        arrow_company_name = d.pop("arrow_company_name", UNSET)

        is_active = d.pop("is_active", UNSET)

        arrow_customer_mapping = cls(
            uuid=uuid,
            url=url,
            settings=settings,
            settings_uuid=settings_uuid,
            arrow_reference=arrow_reference,
            waldur_customer=waldur_customer,
            waldur_customer_uuid=waldur_customer_uuid,
            waldur_customer_name=waldur_customer_name,
            created=created,
            modified=modified,
            arrow_company_name=arrow_company_name,
            is_active=is_active,
        )

        arrow_customer_mapping.additional_properties = d
        return arrow_customer_mapping

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

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RemoteOfferingCreateRequest")


@_attrs_define
class RemoteOfferingCreateRequest:
    """
    Attributes:
        api_url (str):
        token (str):
        remote_offering_uuid (UUID):
        local_category_uuid (UUID):
        local_customer_uuid (UUID):
        remote_customer_uuid (UUID):
    """

    api_url: str
    token: str
    remote_offering_uuid: UUID
    local_category_uuid: UUID
    local_customer_uuid: UUID
    remote_customer_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        token = self.token

        remote_offering_uuid = str(self.remote_offering_uuid)

        local_category_uuid = str(self.local_category_uuid)

        local_customer_uuid = str(self.local_customer_uuid)

        remote_customer_uuid = str(self.remote_customer_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_url": api_url,
                "token": token,
                "remote_offering_uuid": remote_offering_uuid,
                "local_category_uuid": local_category_uuid,
                "local_customer_uuid": local_customer_uuid,
                "remote_customer_uuid": remote_customer_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_url = d.pop("api_url")

        token = d.pop("token")

        remote_offering_uuid = UUID(d.pop("remote_offering_uuid"))

        local_category_uuid = UUID(d.pop("local_category_uuid"))

        local_customer_uuid = UUID(d.pop("local_customer_uuid"))

        remote_customer_uuid = UUID(d.pop("remote_customer_uuid"))

        remote_offering_create_request = cls(
            api_url=api_url,
            token=token,
            remote_offering_uuid=remote_offering_uuid,
            local_category_uuid=local_category_uuid,
            local_customer_uuid=local_customer_uuid,
            remote_customer_uuid=remote_customer_uuid,
        )

        remote_offering_create_request.additional_properties = d
        return remote_offering_create_request

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

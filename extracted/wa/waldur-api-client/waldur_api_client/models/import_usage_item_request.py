from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportUsageItemRequest")


@_attrs_define
class ImportUsageItemRequest:
    """
    Attributes:
        name (str):
        unit_price (str):
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        article_code (Union[Unset, str]):
        service_provider_name (Union[Unset, str]):
        offering_name (Union[Unset, str]):
        plan_name (Union[Unset, str]):
    """

    name: str
    unit_price: str
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    article_code: Union[Unset, str] = UNSET
    service_provider_name: Union[Unset, str] = UNSET
    offering_name: Union[Unset, str] = UNSET
    plan_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        unit_price = self.unit_price

        customer_name = self.customer_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        article_code = self.article_code

        service_provider_name = self.service_provider_name

        offering_name = self.offering_name

        plan_name = self.plan_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "unit_price": unit_price,
            }
        )
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if article_code is not UNSET:
            field_dict["article_code"] = article_code
        if service_provider_name is not UNSET:
            field_dict["service_provider_name"] = service_provider_name
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if plan_name is not UNSET:
            field_dict["plan_name"] = plan_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        unit_price = d.pop("unit_price")

        customer_name = d.pop("customer_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        article_code = d.pop("article_code", UNSET)

        service_provider_name = d.pop("service_provider_name", UNSET)

        offering_name = d.pop("offering_name", UNSET)

        plan_name = d.pop("plan_name", UNSET)

        import_usage_item_request = cls(
            name=name,
            unit_price=unit_price,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            article_code=article_code,
            service_provider_name=service_provider_name,
            offering_name=offering_name,
            plan_name=plan_name,
        )

        import_usage_item_request.additional_properties = d
        return import_usage_item_request

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

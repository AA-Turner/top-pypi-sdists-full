import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_unit import BillingUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.invoice_item_details import InvoiceItemDetails


T = TypeVar("T", bound="InvoiceItem")


@_attrs_define
class InvoiceItem:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        url (Union[Unset, str]):
        name (Union[Unset, str]):
        price (Union[Unset, float]):
        tax (Union[Unset, str]):
        total (Union[Unset, str]):
        unit_price (Union[Unset, str]):
        unit (Union[Unset, BillingUnit]):
        factor (Union[Unset, int]):
        measured_unit (Union[Unset, str]):
        start (Union[Unset, datetime.datetime]): Date and time when item usage has started.
        end (Union[Unset, datetime.datetime]): Date and time when item usage has ended.
        article_code (Union[Unset, str]):
        project_name (Union[Unset, str]):
        project_uuid (Union[None, UUID, Unset]):
        quantity (Union[Unset, str]):
        details (Union[Unset, InvoiceItemDetails]):
        resource (Union[None, Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        resource_name (Union[Unset, str]):
        billing_type (Union[Unset, str]):
        backend_uuid (Union[None, UUID, Unset]):
        credit (Union[Unset, bool]):
    """

    uuid: Union[Unset, UUID] = UNSET
    url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    price: Union[Unset, float] = UNSET
    tax: Union[Unset, str] = UNSET
    total: Union[Unset, str] = UNSET
    unit_price: Union[Unset, str] = UNSET
    unit: Union[Unset, BillingUnit] = UNSET
    factor: Union[Unset, int] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    end: Union[Unset, datetime.datetime] = UNSET
    article_code: Union[Unset, str] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[None, UUID, Unset] = UNSET
    quantity: Union[Unset, str] = UNSET
    details: Union[Unset, "InvoiceItemDetails"] = UNSET
    resource: Union[None, Unset, str] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    resource_name: Union[Unset, str] = UNSET
    billing_type: Union[Unset, str] = UNSET
    backend_uuid: Union[None, UUID, Unset] = UNSET
    credit: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        url = self.url

        name = self.name

        price = self.price

        tax = self.tax

        total = self.total

        unit_price = self.unit_price

        unit: Union[Unset, str] = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        factor = self.factor

        measured_unit = self.measured_unit

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        article_code = self.article_code

        project_name = self.project_name

        project_uuid: Union[None, Unset, str]
        if isinstance(self.project_uuid, Unset):
            project_uuid = UNSET
        elif isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        quantity = self.quantity

        details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        else:
            resource = self.resource

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        billing_type = self.billing_type

        backend_uuid: Union[None, Unset, str]
        if isinstance(self.backend_uuid, Unset):
            backend_uuid = UNSET
        elif isinstance(self.backend_uuid, UUID):
            backend_uuid = str(self.backend_uuid)
        else:
            backend_uuid = self.backend_uuid

        credit = self.credit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if price is not UNSET:
            field_dict["price"] = price
        if tax is not UNSET:
            field_dict["tax"] = tax
        if total is not UNSET:
            field_dict["total"] = total
        if unit_price is not UNSET:
            field_dict["unit_price"] = unit_price
        if unit is not UNSET:
            field_dict["unit"] = unit
        if factor is not UNSET:
            field_dict["factor"] = factor
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if article_code is not UNSET:
            field_dict["article_code"] = article_code
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if details is not UNSET:
            field_dict["details"] = details
        if resource is not UNSET:
            field_dict["resource"] = resource
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if resource_name is not UNSET:
            field_dict["resource_name"] = resource_name
        if billing_type is not UNSET:
            field_dict["billing_type"] = billing_type
        if backend_uuid is not UNSET:
            field_dict["backend_uuid"] = backend_uuid
        if credit is not UNSET:
            field_dict["credit"] = credit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invoice_item_details import InvoiceItemDetails

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        price = d.pop("price", UNSET)

        tax = d.pop("tax", UNSET)

        total = d.pop("total", UNSET)

        unit_price = d.pop("unit_price", UNSET)

        _unit = d.pop("unit", UNSET)
        unit: Union[Unset, BillingUnit]
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = BillingUnit(_unit)

        factor = d.pop("factor", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.datetime]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        article_code = d.pop("article_code", UNSET)

        project_name = d.pop("project_name", UNSET)

        def _parse_project_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid", UNSET))

        quantity = d.pop("quantity", UNSET)

        _details = d.pop("details", UNSET)
        details: Union[Unset, InvoiceItemDetails]
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = InvoiceItemDetails.from_dict(_details)

        def _parse_resource(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource = _parse_resource(d.pop("resource", UNSET))

        _resource_uuid = d.pop("resource_uuid", UNSET)
        resource_uuid: Union[Unset, UUID]
        if isinstance(_resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = UUID(_resource_uuid)

        resource_name = d.pop("resource_name", UNSET)

        billing_type = d.pop("billing_type", UNSET)

        def _parse_backend_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                backend_uuid_type_0 = UUID(data)

                return backend_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        backend_uuid = _parse_backend_uuid(d.pop("backend_uuid", UNSET))

        credit = d.pop("credit", UNSET)

        invoice_item = cls(
            uuid=uuid,
            url=url,
            name=name,
            price=price,
            tax=tax,
            total=total,
            unit_price=unit_price,
            unit=unit,
            factor=factor,
            measured_unit=measured_unit,
            start=start,
            end=end,
            article_code=article_code,
            project_name=project_name,
            project_uuid=project_uuid,
            quantity=quantity,
            details=details,
            resource=resource,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            billing_type=billing_type,
            backend_uuid=backend_uuid,
            credit=credit,
        )

        invoice_item.additional_properties = d
        return invoice_item

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

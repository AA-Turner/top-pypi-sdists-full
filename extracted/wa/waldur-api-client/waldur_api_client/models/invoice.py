import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.invoice_state_enum import InvoiceStateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customer_details import CustomerDetails
    from ..models.invoice_item import InvoiceItem


T = TypeVar("T", bound="Invoice")


@_attrs_define
class Invoice:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        number (Union[Unset, int]):
        customer (Union[Unset, str]):
        price (Union[Unset, str]):
        tax (Union[Unset, str]):
        total (Union[Unset, str]):
        state (Union[Unset, InvoiceStateEnum]):
        year (Union[Unset, int]):
        month (Union[Unset, int]):
        issuer_details (Union[Unset, CustomerDetails]):
        invoice_date (Union[None, Unset, datetime.date]): Date then invoice moved from state pending to created.
        due_date (Union[Unset, datetime.date]):
        customer_details (Union[Unset, CustomerDetails]):
        items (Union[Unset, list['InvoiceItem']]):
        backend_id (Union[Unset, str]):
        payment_url (Union[Unset, str]): URL for initiating payment via payment gateway.
        reference_number (Union[Unset, str]): Reference number associated with the invoice.
        compensations (Union[Unset, float]):
        incurred_costs (Union[Unset, float]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    number: Union[Unset, int] = UNSET
    customer: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    tax: Union[Unset, str] = UNSET
    total: Union[Unset, str] = UNSET
    state: Union[Unset, InvoiceStateEnum] = UNSET
    year: Union[Unset, int] = UNSET
    month: Union[Unset, int] = UNSET
    issuer_details: Union[Unset, "CustomerDetails"] = UNSET
    invoice_date: Union[None, Unset, datetime.date] = UNSET
    due_date: Union[Unset, datetime.date] = UNSET
    customer_details: Union[Unset, "CustomerDetails"] = UNSET
    items: Union[Unset, list["InvoiceItem"]] = UNSET
    backend_id: Union[Unset, str] = UNSET
    payment_url: Union[Unset, str] = UNSET
    reference_number: Union[Unset, str] = UNSET
    compensations: Union[Unset, float] = UNSET
    incurred_costs: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        number = self.number

        customer = self.customer

        price = self.price

        tax = self.tax

        total = self.total

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        year = self.year

        month = self.month

        issuer_details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuer_details, Unset):
            issuer_details = self.issuer_details.to_dict()

        invoice_date: Union[None, Unset, str]
        if isinstance(self.invoice_date, Unset):
            invoice_date = UNSET
        elif isinstance(self.invoice_date, datetime.date):
            invoice_date = self.invoice_date.isoformat()
        else:
            invoice_date = self.invoice_date

        due_date: Union[Unset, str] = UNSET
        if not isinstance(self.due_date, Unset):
            due_date = self.due_date.isoformat()

        customer_details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.customer_details, Unset):
            customer_details = self.customer_details.to_dict()

        items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        backend_id = self.backend_id

        payment_url = self.payment_url

        reference_number = self.reference_number

        compensations = self.compensations

        incurred_costs = self.incurred_costs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if number is not UNSET:
            field_dict["number"] = number
        if customer is not UNSET:
            field_dict["customer"] = customer
        if price is not UNSET:
            field_dict["price"] = price
        if tax is not UNSET:
            field_dict["tax"] = tax
        if total is not UNSET:
            field_dict["total"] = total
        if state is not UNSET:
            field_dict["state"] = state
        if year is not UNSET:
            field_dict["year"] = year
        if month is not UNSET:
            field_dict["month"] = month
        if issuer_details is not UNSET:
            field_dict["issuer_details"] = issuer_details
        if invoice_date is not UNSET:
            field_dict["invoice_date"] = invoice_date
        if due_date is not UNSET:
            field_dict["due_date"] = due_date
        if customer_details is not UNSET:
            field_dict["customer_details"] = customer_details
        if items is not UNSET:
            field_dict["items"] = items
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if payment_url is not UNSET:
            field_dict["payment_url"] = payment_url
        if reference_number is not UNSET:
            field_dict["reference_number"] = reference_number
        if compensations is not UNSET:
            field_dict["compensations"] = compensations
        if incurred_costs is not UNSET:
            field_dict["incurred_costs"] = incurred_costs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_details import CustomerDetails
        from ..models.invoice_item import InvoiceItem

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        number = d.pop("number", UNSET)

        customer = d.pop("customer", UNSET)

        price = d.pop("price", UNSET)

        tax = d.pop("tax", UNSET)

        total = d.pop("total", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, InvoiceStateEnum]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = InvoiceStateEnum(_state)

        year = d.pop("year", UNSET)

        month = d.pop("month", UNSET)

        _issuer_details = d.pop("issuer_details", UNSET)
        issuer_details: Union[Unset, CustomerDetails]
        if isinstance(_issuer_details, Unset):
            issuer_details = UNSET
        else:
            issuer_details = CustomerDetails.from_dict(_issuer_details)

        def _parse_invoice_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                invoice_date_type_0 = isoparse(data).date()

                return invoice_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        invoice_date = _parse_invoice_date(d.pop("invoice_date", UNSET))

        _due_date = d.pop("due_date", UNSET)
        due_date: Union[Unset, datetime.date]
        if isinstance(_due_date, Unset):
            due_date = UNSET
        else:
            due_date = isoparse(_due_date).date()

        _customer_details = d.pop("customer_details", UNSET)
        customer_details: Union[Unset, CustomerDetails]
        if isinstance(_customer_details, Unset):
            customer_details = UNSET
        else:
            customer_details = CustomerDetails.from_dict(_customer_details)

        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = InvoiceItem.from_dict(items_item_data)

            items.append(items_item)

        backend_id = d.pop("backend_id", UNSET)

        payment_url = d.pop("payment_url", UNSET)

        reference_number = d.pop("reference_number", UNSET)

        compensations = d.pop("compensations", UNSET)

        incurred_costs = d.pop("incurred_costs", UNSET)

        invoice = cls(
            url=url,
            uuid=uuid,
            number=number,
            customer=customer,
            price=price,
            tax=tax,
            total=total,
            state=state,
            year=year,
            month=month,
            issuer_details=issuer_details,
            invoice_date=invoice_date,
            due_date=due_date,
            customer_details=customer_details,
            items=items,
            backend_id=backend_id,
            payment_url=payment_url,
            reference_number=reference_number,
            compensations=compensations,
            incurred_costs=incurred_costs,
        )

        invoice.additional_properties = d
        return invoice

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

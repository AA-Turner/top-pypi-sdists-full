from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sync_resources_response_errors_item import SyncResourcesResponseErrorsItem


T = TypeVar("T", bound="SyncResourcesResponse")


@_attrs_define
class SyncResourcesResponse:
    """
    Attributes:
        synced (int):
        created (int):
        updated (int):
        orders_created (Union[Unset, int]):
        customers_created (Union[Unset, int]):
        projects_created (Union[Unset, int]):
        mappings_created (Union[Unset, int]):
        invoices_created (Union[Unset, int]):
        invoice_items_created (Union[Unset, int]):
        errors (Union[Unset, list['SyncResourcesResponseErrorsItem']]):
    """

    synced: int
    created: int
    updated: int
    orders_created: Union[Unset, int] = UNSET
    customers_created: Union[Unset, int] = UNSET
    projects_created: Union[Unset, int] = UNSET
    mappings_created: Union[Unset, int] = UNSET
    invoices_created: Union[Unset, int] = UNSET
    invoice_items_created: Union[Unset, int] = UNSET
    errors: Union[Unset, list["SyncResourcesResponseErrorsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        synced = self.synced

        created = self.created

        updated = self.updated

        orders_created = self.orders_created

        customers_created = self.customers_created

        projects_created = self.projects_created

        mappings_created = self.mappings_created

        invoices_created = self.invoices_created

        invoice_items_created = self.invoice_items_created

        errors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()
                errors.append(errors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "synced": synced,
                "created": created,
                "updated": updated,
            }
        )
        if orders_created is not UNSET:
            field_dict["orders_created"] = orders_created
        if customers_created is not UNSET:
            field_dict["customers_created"] = customers_created
        if projects_created is not UNSET:
            field_dict["projects_created"] = projects_created
        if mappings_created is not UNSET:
            field_dict["mappings_created"] = mappings_created
        if invoices_created is not UNSET:
            field_dict["invoices_created"] = invoices_created
        if invoice_items_created is not UNSET:
            field_dict["invoice_items_created"] = invoice_items_created
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sync_resources_response_errors_item import SyncResourcesResponseErrorsItem

        d = dict(src_dict)
        synced = d.pop("synced")

        created = d.pop("created")

        updated = d.pop("updated")

        orders_created = d.pop("orders_created", UNSET)

        customers_created = d.pop("customers_created", UNSET)

        projects_created = d.pop("projects_created", UNSET)

        mappings_created = d.pop("mappings_created", UNSET)

        invoices_created = d.pop("invoices_created", UNSET)

        invoice_items_created = d.pop("invoice_items_created", UNSET)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = SyncResourcesResponseErrorsItem.from_dict(errors_item_data)

            errors.append(errors_item)

        sync_resources_response = cls(
            synced=synced,
            created=created,
            updated=updated,
            orders_created=orders_created,
            customers_created=customers_created,
            projects_created=projects_created,
            mappings_created=mappings_created,
            invoices_created=invoices_created,
            invoice_items_created=invoice_items_created,
            errors=errors,
        )

        sync_resources_response.additional_properties = d
        return sync_resources_response

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

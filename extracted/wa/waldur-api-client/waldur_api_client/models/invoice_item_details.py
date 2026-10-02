from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_limit_period import ResourceLimitPeriod


T = TypeVar("T", bound="InvoiceItemDetails")


@_attrs_define
class InvoiceItemDetails:
    """
    Attributes:
        resource_name (Union[Unset, str]): Name of the marketplace resource
        resource_uuid (Union[Unset, UUID]): UUID of the marketplace resource
        plan_name (Union[Unset, str]): Name of the pricing plan
        plan_uuid (Union[Unset, UUID]): UUID of the pricing plan
        offering_type (Union[Unset, str]): Type of the offering
        offering_name (Union[Unset, str]): Name of the offering
        offering_uuid (Union[Unset, UUID]): UUID of the offering
        service_provider_name (Union[Unset, str]): Name of the service provider
        service_provider_uuid (Union[Unset, UUID]): UUID of the service provider
        plan_component_id (Union[Unset, int]): ID of the plan component
        offering_component_type (Union[Unset, str]): Type of the offering component
        offering_component_name (Union[Unset, str]): Name of the offering component
        resource_limit_periods (Union[Unset, list['ResourceLimitPeriod']]): List of resource limit periods for this
            invoice item
    """

    resource_name: Union[Unset, str] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    plan_name: Union[Unset, str] = UNSET
    plan_uuid: Union[Unset, UUID] = UNSET
    offering_type: Union[Unset, str] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    service_provider_name: Union[Unset, str] = UNSET
    service_provider_uuid: Union[Unset, UUID] = UNSET
    plan_component_id: Union[Unset, int] = UNSET
    offering_component_type: Union[Unset, str] = UNSET
    offering_component_name: Union[Unset, str] = UNSET
    resource_limit_periods: Union[Unset, list["ResourceLimitPeriod"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_name = self.resource_name

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        plan_name = self.plan_name

        plan_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.plan_uuid, Unset):
            plan_uuid = str(self.plan_uuid)

        offering_type = self.offering_type

        offering_name = self.offering_name

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        service_provider_name = self.service_provider_name

        service_provider_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.service_provider_uuid, Unset):
            service_provider_uuid = str(self.service_provider_uuid)

        plan_component_id = self.plan_component_id

        offering_component_type = self.offering_component_type

        offering_component_name = self.offering_component_name

        resource_limit_periods: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.resource_limit_periods, Unset):
            resource_limit_periods = []
            for resource_limit_periods_item_data in self.resource_limit_periods:
                resource_limit_periods_item = resource_limit_periods_item_data.to_dict()
                resource_limit_periods.append(resource_limit_periods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource_name is not UNSET:
            field_dict["resource_name"] = resource_name
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if plan_name is not UNSET:
            field_dict["plan_name"] = plan_name
        if plan_uuid is not UNSET:
            field_dict["plan_uuid"] = plan_uuid
        if offering_type is not UNSET:
            field_dict["offering_type"] = offering_type
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if service_provider_name is not UNSET:
            field_dict["service_provider_name"] = service_provider_name
        if service_provider_uuid is not UNSET:
            field_dict["service_provider_uuid"] = service_provider_uuid
        if plan_component_id is not UNSET:
            field_dict["plan_component_id"] = plan_component_id
        if offering_component_type is not UNSET:
            field_dict["offering_component_type"] = offering_component_type
        if offering_component_name is not UNSET:
            field_dict["offering_component_name"] = offering_component_name
        if resource_limit_periods is not UNSET:
            field_dict["resource_limit_periods"] = resource_limit_periods

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_limit_period import ResourceLimitPeriod

        d = dict(src_dict)
        resource_name = d.pop("resource_name", UNSET)

        _resource_uuid = d.pop("resource_uuid", UNSET)
        resource_uuid: Union[Unset, UUID]
        if isinstance(_resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = UUID(_resource_uuid)

        plan_name = d.pop("plan_name", UNSET)

        _plan_uuid = d.pop("plan_uuid", UNSET)
        plan_uuid: Union[Unset, UUID]
        if isinstance(_plan_uuid, Unset):
            plan_uuid = UNSET
        else:
            plan_uuid = UUID(_plan_uuid)

        offering_type = d.pop("offering_type", UNSET)

        offering_name = d.pop("offering_name", UNSET)

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        service_provider_name = d.pop("service_provider_name", UNSET)

        _service_provider_uuid = d.pop("service_provider_uuid", UNSET)
        service_provider_uuid: Union[Unset, UUID]
        if isinstance(_service_provider_uuid, Unset):
            service_provider_uuid = UNSET
        else:
            service_provider_uuid = UUID(_service_provider_uuid)

        plan_component_id = d.pop("plan_component_id", UNSET)

        offering_component_type = d.pop("offering_component_type", UNSET)

        offering_component_name = d.pop("offering_component_name", UNSET)

        resource_limit_periods = []
        _resource_limit_periods = d.pop("resource_limit_periods", UNSET)
        for resource_limit_periods_item_data in _resource_limit_periods or []:
            resource_limit_periods_item = ResourceLimitPeriod.from_dict(resource_limit_periods_item_data)

            resource_limit_periods.append(resource_limit_periods_item)

        invoice_item_details = cls(
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            plan_name=plan_name,
            plan_uuid=plan_uuid,
            offering_type=offering_type,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            service_provider_name=service_provider_name,
            service_provider_uuid=service_provider_uuid,
            plan_component_id=plan_component_id,
            offering_component_type=offering_component_type,
            offering_component_name=offering_component_name,
            resource_limit_periods=resource_limit_periods,
        )

        invoice_item_details.additional_properties = d
        return invoice_item_details

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

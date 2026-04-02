import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.request_types import RequestTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.azure_sql_server_create_order_attributes import AzureSQLServerCreateOrderAttributes
    from ..models.azure_virtual_machine_create_order_attributes import AzureVirtualMachineCreateOrderAttributes
    from ..models.generic_order_attributes import GenericOrderAttributes
    from ..models.marketplace_open_portal_create_order_attributes import MarketplaceOpenPortalCreateOrderAttributes
    from ..models.marketplace_open_portal_remote_create_order_attributes import (
        MarketplaceOpenPortalRemoteCreateOrderAttributes,
    )
    from ..models.open_stack_instance_create_order_attributes import OpenStackInstanceCreateOrderAttributes
    from ..models.open_stack_tenant_create_order_attributes import OpenStackTenantCreateOrderAttributes
    from ..models.open_stack_volume_create_order_attributes import OpenStackVolumeCreateOrderAttributes
    from ..models.order_create_request_limits import OrderCreateRequestLimits
    from ..models.slurm_invoices_slurm_package_create_order_attributes import (
        SlurmInvoicesSlurmPackageCreateOrderAttributes,
    )
    from ..models.v_mware_virtual_machine_create_order_attributes import VMwareVirtualMachineCreateOrderAttributes


T = TypeVar("T", bound="OrderCreateRequest")


@_attrs_define
class OrderCreateRequest:
    """
    Attributes:
        offering (str):
        project (str):
        plan (Union[Unset, str]):
        attributes (Union['AzureSQLServerCreateOrderAttributes', 'AzureVirtualMachineCreateOrderAttributes',
            'GenericOrderAttributes', 'MarketplaceOpenPortalCreateOrderAttributes',
            'MarketplaceOpenPortalRemoteCreateOrderAttributes', 'OpenStackInstanceCreateOrderAttributes',
            'OpenStackTenantCreateOrderAttributes', 'OpenStackVolumeCreateOrderAttributes',
            'SlurmInvoicesSlurmPackageCreateOrderAttributes', 'VMwareVirtualMachineCreateOrderAttributes', Unset]):
            Attributes structure depends on the offering type specified in the parent object. Can also be a generic object
            for offerings without a specific attributes schema.
        limits (Union[Unset, OrderCreateRequestLimits]):
        accepting_terms_of_service (Union[Unset, bool]):
        callback_url (Union[None, Unset, str]):
        request_comment (Union[None, Unset, str]):
        type_ (Union[Unset, RequestTypes]):  Default: RequestTypes.CREATE.
        start_date (Union[None, Unset, datetime.date]): Enables delayed processing of resource provisioning order.
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
    """

    offering: str
    project: str
    plan: Union[Unset, str] = UNSET
    attributes: Union[
        "AzureSQLServerCreateOrderAttributes",
        "AzureVirtualMachineCreateOrderAttributes",
        "GenericOrderAttributes",
        "MarketplaceOpenPortalCreateOrderAttributes",
        "MarketplaceOpenPortalRemoteCreateOrderAttributes",
        "OpenStackInstanceCreateOrderAttributes",
        "OpenStackTenantCreateOrderAttributes",
        "OpenStackVolumeCreateOrderAttributes",
        "SlurmInvoicesSlurmPackageCreateOrderAttributes",
        "VMwareVirtualMachineCreateOrderAttributes",
        Unset,
    ] = UNSET
    limits: Union[Unset, "OrderCreateRequestLimits"] = UNSET
    accepting_terms_of_service: Union[Unset, bool] = UNSET
    callback_url: Union[None, Unset, str] = UNSET
    request_comment: Union[None, Unset, str] = UNSET
    type_: Union[Unset, RequestTypes] = RequestTypes.CREATE
    start_date: Union[None, Unset, datetime.date] = UNSET
    slug: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.azure_sql_server_create_order_attributes import AzureSQLServerCreateOrderAttributes
        from ..models.azure_virtual_machine_create_order_attributes import AzureVirtualMachineCreateOrderAttributes
        from ..models.marketplace_open_portal_create_order_attributes import MarketplaceOpenPortalCreateOrderAttributes
        from ..models.marketplace_open_portal_remote_create_order_attributes import (
            MarketplaceOpenPortalRemoteCreateOrderAttributes,
        )
        from ..models.open_stack_instance_create_order_attributes import OpenStackInstanceCreateOrderAttributes
        from ..models.open_stack_tenant_create_order_attributes import OpenStackTenantCreateOrderAttributes
        from ..models.open_stack_volume_create_order_attributes import OpenStackVolumeCreateOrderAttributes
        from ..models.slurm_invoices_slurm_package_create_order_attributes import (
            SlurmInvoicesSlurmPackageCreateOrderAttributes,
        )
        from ..models.v_mware_virtual_machine_create_order_attributes import VMwareVirtualMachineCreateOrderAttributes

        offering = self.offering

        project = self.project

        plan = self.plan

        attributes: Union[Unset, dict[str, Any]]
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, AzureVirtualMachineCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, AzureSQLServerCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, MarketplaceOpenPortalCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, MarketplaceOpenPortalRemoteCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, OpenStackTenantCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, OpenStackInstanceCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, OpenStackVolumeCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, SlurmInvoicesSlurmPackageCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        elif isinstance(self.attributes, VMwareVirtualMachineCreateOrderAttributes):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        accepting_terms_of_service = self.accepting_terms_of_service

        callback_url: Union[None, Unset, str]
        if isinstance(self.callback_url, Unset):
            callback_url = UNSET
        else:
            callback_url = self.callback_url

        request_comment: Union[None, Unset, str]
        if isinstance(self.request_comment, Unset):
            request_comment = UNSET
        else:
            request_comment = self.request_comment

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        start_date: Union[None, Unset, str]
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        slug = self.slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
                "project": project,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if accepting_terms_of_service is not UNSET:
            field_dict["accepting_terms_of_service"] = accepting_terms_of_service
        if callback_url is not UNSET:
            field_dict["callback_url"] = callback_url
        if request_comment is not UNSET:
            field_dict["request_comment"] = request_comment
        if type_ is not UNSET:
            field_dict["type"] = type_
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.azure_sql_server_create_order_attributes import AzureSQLServerCreateOrderAttributes
        from ..models.azure_virtual_machine_create_order_attributes import AzureVirtualMachineCreateOrderAttributes
        from ..models.generic_order_attributes import GenericOrderAttributes
        from ..models.marketplace_open_portal_create_order_attributes import MarketplaceOpenPortalCreateOrderAttributes
        from ..models.marketplace_open_portal_remote_create_order_attributes import (
            MarketplaceOpenPortalRemoteCreateOrderAttributes,
        )
        from ..models.open_stack_instance_create_order_attributes import OpenStackInstanceCreateOrderAttributes
        from ..models.open_stack_tenant_create_order_attributes import OpenStackTenantCreateOrderAttributes
        from ..models.open_stack_volume_create_order_attributes import OpenStackVolumeCreateOrderAttributes
        from ..models.order_create_request_limits import OrderCreateRequestLimits
        from ..models.slurm_invoices_slurm_package_create_order_attributes import (
            SlurmInvoicesSlurmPackageCreateOrderAttributes,
        )
        from ..models.v_mware_virtual_machine_create_order_attributes import VMwareVirtualMachineCreateOrderAttributes

        d = dict(src_dict)
        offering = d.pop("offering")

        project = d.pop("project")

        plan = d.pop("plan", UNSET)

        def _parse_attributes(
            data: object,
        ) -> Union[
            "AzureSQLServerCreateOrderAttributes",
            "AzureVirtualMachineCreateOrderAttributes",
            "GenericOrderAttributes",
            "MarketplaceOpenPortalCreateOrderAttributes",
            "MarketplaceOpenPortalRemoteCreateOrderAttributes",
            "OpenStackInstanceCreateOrderAttributes",
            "OpenStackTenantCreateOrderAttributes",
            "OpenStackVolumeCreateOrderAttributes",
            "SlurmInvoicesSlurmPackageCreateOrderAttributes",
            "VMwareVirtualMachineCreateOrderAttributes",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_0 = AzureVirtualMachineCreateOrderAttributes.from_dict(data)

                return attributes_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_1 = AzureSQLServerCreateOrderAttributes.from_dict(data)

                return attributes_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_2 = MarketplaceOpenPortalCreateOrderAttributes.from_dict(data)

                return attributes_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_3 = MarketplaceOpenPortalRemoteCreateOrderAttributes.from_dict(data)

                return attributes_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_4 = OpenStackTenantCreateOrderAttributes.from_dict(data)

                return attributes_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_5 = OpenStackInstanceCreateOrderAttributes.from_dict(data)

                return attributes_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_6 = OpenStackVolumeCreateOrderAttributes.from_dict(data)

                return attributes_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_7 = SlurmInvoicesSlurmPackageCreateOrderAttributes.from_dict(data)

                return attributes_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_8 = VMwareVirtualMachineCreateOrderAttributes.from_dict(data)

                return attributes_type_8
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            attributes_type_9 = GenericOrderAttributes.from_dict(data)

            return attributes_type_9

        attributes = _parse_attributes(d.pop("attributes", UNSET))

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, OrderCreateRequestLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = OrderCreateRequestLimits.from_dict(_limits)

        accepting_terms_of_service = d.pop("accepting_terms_of_service", UNSET)

        def _parse_callback_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        callback_url = _parse_callback_url(d.pop("callback_url", UNSET))

        def _parse_request_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        request_comment = _parse_request_comment(d.pop("request_comment", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, RequestTypes]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = RequestTypes(_type_)

        def _parse_start_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        slug = d.pop("slug", UNSET)

        order_create_request = cls(
            offering=offering,
            project=project,
            plan=plan,
            attributes=attributes,
            limits=limits,
            accepting_terms_of_service=accepting_terms_of_service,
            callback_url=callback_url,
            request_comment=request_comment,
            type_=type_,
            start_date=start_date,
            slug=slug,
        )

        order_create_request.additional_properties = d
        return order_create_request

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

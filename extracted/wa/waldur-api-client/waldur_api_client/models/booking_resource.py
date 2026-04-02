import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_unit import BillingUnit
from ..models.offering_state import OfferingState
from ..models.resource_state import ResourceState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.backend_metadata import BackendMetadata
    from ..models.booking_resource_attributes import BookingResourceAttributes
    from ..models.booking_resource_current_usages import BookingResourceCurrentUsages
    from ..models.booking_resource_limit_usage import BookingResourceLimitUsage
    from ..models.booking_resource_limits import BookingResourceLimits
    from ..models.booking_resource_renewal_date_type_0 import BookingResourceRenewalDateType0
    from ..models.booking_slot import BookingSlot
    from ..models.nested_endpoint import NestedEndpoint
    from ..models.offering_component import OfferingComponent
    from ..models.order_details import OrderDetails
    from ..models.report_section import ReportSection


T = TypeVar("T", bound="BookingResource")


@_attrs_define
class BookingResource:
    """
    Attributes:
        offering (Union[Unset, str]):
        offering_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        offering_description (Union[Unset, str]):
        offering_image (Union[Unset, str]):
        offering_thumbnail (Union[Unset, str]):
        offering_type (Union[Unset, str]):
        offering_shared (Union[Unset, bool]): Accessible to all customers.
        offering_billable (Union[Unset, bool]): Purchase and usage is invoiced.
        offering_plugin_options (Union[Unset, Any]): Public data used by specific plugin, such as storage mode for
            OpenStack.
        provider_name (Union[Unset, str]):
        provider_uuid (Union[Unset, UUID]):
        provider_slug (Union[Unset, str]):
        category_title (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        category_icon (Union[Unset, str]):
        plan (Union[Unset, str]):
        plan_unit (Union[BillingUnit, None, Unset]):
        plan_name (Union[None, Unset, str]):
        plan_uuid (Union[None, UUID, Unset]):
        plan_description (Union[None, Unset, str]):
        attributes (Union[Unset, BookingResourceAttributes]):
        limits (Union[Unset, BookingResourceLimits]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        url (Union[Unset, str]):
        scope (Union[Unset, str]):
        description (Union[Unset, str]):
        state (Union[Unset, ResourceState]):
        resource_uuid (Union[None, UUID, Unset]):
        backend_id (Union[Unset, str]):
        effective_id (Union[Unset, str]):
        resource_type (Union[None, Unset, str]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_description (Union[Unset, str]):
        project_end_date (Union[None, Unset, datetime.date]): The date is inclusive. Once reached, all project resource
            will be scheduled for termination.
        project_end_date_requested_by (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        offering_slug (Union[Unset, str]):
        parent_offering_uuid (Union[Unset, UUID]):
        parent_offering_name (Union[Unset, str]):
        parent_offering_slug (Union[Unset, str]):
        offering_backend_id (Union[Unset, str]):
        parent_uuid (Union[Unset, UUID]):
        parent_name (Union[Unset, str]):
        backend_metadata (Union[Unset, BackendMetadata]):
        is_usage_based (Union[Unset, bool]): Returns True if the resource has usage-based components that track variable
            consumption.
        is_limit_based (Union[Unset, bool]): Returns True if the resource has limit-based components with user-
            adjustable quotas.
        name (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        current_usages (Union[Unset, BookingResourceCurrentUsages]): Dictionary mapping component types to their latest
            reported usage amounts.
        can_terminate (Union[Unset, bool]):
        report (Union[Unset, list['ReportSection']]):
        end_date (Union[None, Unset, datetime.date]): The date is inclusive. Once reached, a resource will be scheduled
            for termination.
        end_date_requested_by (Union[None, Unset, str]):
        username (Union[None, Unset, str]):
        limit_usage (Union[Unset, BookingResourceLimitUsage]): Dictionary mapping limit-based component types to their
            consumed usage. For monthly periods, maps from current_usages; for longer periods, aggregates historical usage.
        downscaled (Union[Unset, bool]):
        restrict_member_access (Union[Unset, bool]):
        paused (Union[Unset, bool]):
        endpoints (Union[Unset, list['NestedEndpoint']]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        options (Union[Unset, Any]):
        available_actions (Union[Unset, list[str]]):
        last_sync (Union[Unset, datetime.datetime]):
        order_in_progress (Union['OrderDetails', None, Unset]):
        creation_order (Union['OrderDetails', None, Unset]):
        service_settings_uuid (Union[Unset, UUID]):
        project_slug (Union[Unset, str]):
        customer_slug (Union[Unset, str]):
        user_requires_reconsent (Union[Unset, bool]): Check if the current user needs to re-consent for this resource's
            offering.
        renewal_date (Union['BookingResourceRenewalDateType0', None, Unset]):
        offering_state (Union[Unset, OfferingState]):
        offering_components (Union[Unset, list['OfferingComponent']]):
        created_by (Union[Unset, str]):
        created_by_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and
            @/./+/-/_ characters
        created_by_full_name (Union[Unset, str]):
        consumer_reviewed_by (Union[Unset, str]):
        consumer_reviewed_by_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers
            and @/./+/-/_ characters
        consumer_reviewed_by_full_name (Union[Unset, str]):
        slots (Union[Unset, list['BookingSlot']]):
    """

    offering: Union[Unset, str] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    offering_description: Union[Unset, str] = UNSET
    offering_image: Union[Unset, str] = UNSET
    offering_thumbnail: Union[Unset, str] = UNSET
    offering_type: Union[Unset, str] = UNSET
    offering_shared: Union[Unset, bool] = UNSET
    offering_billable: Union[Unset, bool] = UNSET
    offering_plugin_options: Union[Unset, Any] = UNSET
    provider_name: Union[Unset, str] = UNSET
    provider_uuid: Union[Unset, UUID] = UNSET
    provider_slug: Union[Unset, str] = UNSET
    category_title: Union[Unset, str] = UNSET
    category_uuid: Union[Unset, UUID] = UNSET
    category_icon: Union[Unset, str] = UNSET
    plan: Union[Unset, str] = UNSET
    plan_unit: Union[BillingUnit, None, Unset] = UNSET
    plan_name: Union[None, Unset, str] = UNSET
    plan_uuid: Union[None, UUID, Unset] = UNSET
    plan_description: Union[None, Unset, str] = UNSET
    attributes: Union[Unset, "BookingResourceAttributes"] = UNSET
    limits: Union[Unset, "BookingResourceLimits"] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    url: Union[Unset, str] = UNSET
    scope: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, ResourceState] = UNSET
    resource_uuid: Union[None, UUID, Unset] = UNSET
    backend_id: Union[Unset, str] = UNSET
    effective_id: Union[Unset, str] = UNSET
    resource_type: Union[None, Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_description: Union[Unset, str] = UNSET
    project_end_date: Union[None, Unset, datetime.date] = UNSET
    project_end_date_requested_by: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    offering_slug: Union[Unset, str] = UNSET
    parent_offering_uuid: Union[Unset, UUID] = UNSET
    parent_offering_name: Union[Unset, str] = UNSET
    parent_offering_slug: Union[Unset, str] = UNSET
    offering_backend_id: Union[Unset, str] = UNSET
    parent_uuid: Union[Unset, UUID] = UNSET
    parent_name: Union[Unset, str] = UNSET
    backend_metadata: Union[Unset, "BackendMetadata"] = UNSET
    is_usage_based: Union[Unset, bool] = UNSET
    is_limit_based: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    current_usages: Union[Unset, "BookingResourceCurrentUsages"] = UNSET
    can_terminate: Union[Unset, bool] = UNSET
    report: Union[Unset, list["ReportSection"]] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    end_date_requested_by: Union[None, Unset, str] = UNSET
    username: Union[None, Unset, str] = UNSET
    limit_usage: Union[Unset, "BookingResourceLimitUsage"] = UNSET
    downscaled: Union[Unset, bool] = UNSET
    restrict_member_access: Union[Unset, bool] = UNSET
    paused: Union[Unset, bool] = UNSET
    endpoints: Union[Unset, list["NestedEndpoint"]] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    options: Union[Unset, Any] = UNSET
    available_actions: Union[Unset, list[str]] = UNSET
    last_sync: Union[Unset, datetime.datetime] = UNSET
    order_in_progress: Union["OrderDetails", None, Unset] = UNSET
    creation_order: Union["OrderDetails", None, Unset] = UNSET
    service_settings_uuid: Union[Unset, UUID] = UNSET
    project_slug: Union[Unset, str] = UNSET
    customer_slug: Union[Unset, str] = UNSET
    user_requires_reconsent: Union[Unset, bool] = UNSET
    renewal_date: Union["BookingResourceRenewalDateType0", None, Unset] = UNSET
    offering_state: Union[Unset, OfferingState] = UNSET
    offering_components: Union[Unset, list["OfferingComponent"]] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_by_username: Union[Unset, str] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    consumer_reviewed_by: Union[Unset, str] = UNSET
    consumer_reviewed_by_username: Union[Unset, str] = UNSET
    consumer_reviewed_by_full_name: Union[Unset, str] = UNSET
    slots: Union[Unset, list["BookingSlot"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.booking_resource_renewal_date_type_0 import BookingResourceRenewalDateType0
        from ..models.order_details import OrderDetails

        offering = self.offering

        offering_name = self.offering_name

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        offering_description = self.offering_description

        offering_image = self.offering_image

        offering_thumbnail = self.offering_thumbnail

        offering_type = self.offering_type

        offering_shared = self.offering_shared

        offering_billable = self.offering_billable

        offering_plugin_options = self.offering_plugin_options

        provider_name = self.provider_name

        provider_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.provider_uuid, Unset):
            provider_uuid = str(self.provider_uuid)

        provider_slug = self.provider_slug

        category_title = self.category_title

        category_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.category_uuid, Unset):
            category_uuid = str(self.category_uuid)

        category_icon = self.category_icon

        plan = self.plan

        plan_unit: Union[None, Unset, str]
        if isinstance(self.plan_unit, Unset):
            plan_unit = UNSET
        elif isinstance(self.plan_unit, BillingUnit):
            plan_unit = self.plan_unit.value
        else:
            plan_unit = self.plan_unit

        plan_name: Union[None, Unset, str]
        if isinstance(self.plan_name, Unset):
            plan_name = UNSET
        else:
            plan_name = self.plan_name

        plan_uuid: Union[None, Unset, str]
        if isinstance(self.plan_uuid, Unset):
            plan_uuid = UNSET
        elif isinstance(self.plan_uuid, UUID):
            plan_uuid = str(self.plan_uuid)
        else:
            plan_uuid = self.plan_uuid

        plan_description: Union[None, Unset, str]
        if isinstance(self.plan_description, Unset):
            plan_description = UNSET
        else:
            plan_description = self.plan_description

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        url = self.url

        scope = self.scope

        description = self.description

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        elif isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        backend_id = self.backend_id

        effective_id = self.effective_id

        resource_type: Union[None, Unset, str]
        if isinstance(self.resource_type, Unset):
            resource_type = UNSET
        else:
            resource_type = self.resource_type

        project = self.project

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        project_name = self.project_name

        project_description = self.project_description

        project_end_date: Union[None, Unset, str]
        if isinstance(self.project_end_date, Unset):
            project_end_date = UNSET
        elif isinstance(self.project_end_date, datetime.date):
            project_end_date = self.project_end_date.isoformat()
        else:
            project_end_date = self.project_end_date

        project_end_date_requested_by = self.project_end_date_requested_by

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        offering_slug = self.offering_slug

        parent_offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.parent_offering_uuid, Unset):
            parent_offering_uuid = str(self.parent_offering_uuid)

        parent_offering_name = self.parent_offering_name

        parent_offering_slug = self.parent_offering_slug

        offering_backend_id = self.offering_backend_id

        parent_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.parent_uuid, Unset):
            parent_uuid = str(self.parent_uuid)

        parent_name = self.parent_name

        backend_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.backend_metadata, Unset):
            backend_metadata = self.backend_metadata.to_dict()

        is_usage_based = self.is_usage_based

        is_limit_based = self.is_limit_based

        name = self.name

        slug = self.slug

        current_usages: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.current_usages, Unset):
            current_usages = self.current_usages.to_dict()

        can_terminate = self.can_terminate

        report: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.report, Unset):
            report = []
            for report_item_data in self.report:
                report_item = report_item_data.to_dict()
                report.append(report_item)

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        end_date_requested_by: Union[None, Unset, str]
        if isinstance(self.end_date_requested_by, Unset):
            end_date_requested_by = UNSET
        else:
            end_date_requested_by = self.end_date_requested_by

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        limit_usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limit_usage, Unset):
            limit_usage = self.limit_usage.to_dict()

        downscaled = self.downscaled

        restrict_member_access = self.restrict_member_access

        paused = self.paused

        endpoints: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.endpoints, Unset):
            endpoints = []
            for endpoints_item_data in self.endpoints:
                endpoints_item = endpoints_item_data.to_dict()
                endpoints.append(endpoints_item)

        error_message = self.error_message

        error_traceback = self.error_traceback

        options = self.options

        available_actions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.available_actions, Unset):
            available_actions = self.available_actions

        last_sync: Union[Unset, str] = UNSET
        if not isinstance(self.last_sync, Unset):
            last_sync = self.last_sync.isoformat()

        order_in_progress: Union[None, Unset, dict[str, Any]]
        if isinstance(self.order_in_progress, Unset):
            order_in_progress = UNSET
        elif isinstance(self.order_in_progress, OrderDetails):
            order_in_progress = self.order_in_progress.to_dict()
        else:
            order_in_progress = self.order_in_progress

        creation_order: Union[None, Unset, dict[str, Any]]
        if isinstance(self.creation_order, Unset):
            creation_order = UNSET
        elif isinstance(self.creation_order, OrderDetails):
            creation_order = self.creation_order.to_dict()
        else:
            creation_order = self.creation_order

        service_settings_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.service_settings_uuid, Unset):
            service_settings_uuid = str(self.service_settings_uuid)

        project_slug = self.project_slug

        customer_slug = self.customer_slug

        user_requires_reconsent = self.user_requires_reconsent

        renewal_date: Union[None, Unset, dict[str, Any]]
        if isinstance(self.renewal_date, Unset):
            renewal_date = UNSET
        elif isinstance(self.renewal_date, BookingResourceRenewalDateType0):
            renewal_date = self.renewal_date.to_dict()
        else:
            renewal_date = self.renewal_date

        offering_state: Union[Unset, str] = UNSET
        if not isinstance(self.offering_state, Unset):
            offering_state = self.offering_state.value

        offering_components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.offering_components, Unset):
            offering_components = []
            for offering_components_item_data in self.offering_components:
                offering_components_item = offering_components_item_data.to_dict()
                offering_components.append(offering_components_item)

        created_by = self.created_by

        created_by_username = self.created_by_username

        created_by_full_name = self.created_by_full_name

        consumer_reviewed_by = self.consumer_reviewed_by

        consumer_reviewed_by_username = self.consumer_reviewed_by_username

        consumer_reviewed_by_full_name = self.consumer_reviewed_by_full_name

        slots: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.slots, Unset):
            slots = []
            for slots_item_data in self.slots:
                slots_item = slots_item_data.to_dict()
                slots.append(slots_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offering is not UNSET:
            field_dict["offering"] = offering
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if offering_description is not UNSET:
            field_dict["offering_description"] = offering_description
        if offering_image is not UNSET:
            field_dict["offering_image"] = offering_image
        if offering_thumbnail is not UNSET:
            field_dict["offering_thumbnail"] = offering_thumbnail
        if offering_type is not UNSET:
            field_dict["offering_type"] = offering_type
        if offering_shared is not UNSET:
            field_dict["offering_shared"] = offering_shared
        if offering_billable is not UNSET:
            field_dict["offering_billable"] = offering_billable
        if offering_plugin_options is not UNSET:
            field_dict["offering_plugin_options"] = offering_plugin_options
        if provider_name is not UNSET:
            field_dict["provider_name"] = provider_name
        if provider_uuid is not UNSET:
            field_dict["provider_uuid"] = provider_uuid
        if provider_slug is not UNSET:
            field_dict["provider_slug"] = provider_slug
        if category_title is not UNSET:
            field_dict["category_title"] = category_title
        if category_uuid is not UNSET:
            field_dict["category_uuid"] = category_uuid
        if category_icon is not UNSET:
            field_dict["category_icon"] = category_icon
        if plan is not UNSET:
            field_dict["plan"] = plan
        if plan_unit is not UNSET:
            field_dict["plan_unit"] = plan_unit
        if plan_name is not UNSET:
            field_dict["plan_name"] = plan_name
        if plan_uuid is not UNSET:
            field_dict["plan_uuid"] = plan_uuid
        if plan_description is not UNSET:
            field_dict["plan_description"] = plan_description
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if url is not UNSET:
            field_dict["url"] = url
        if scope is not UNSET:
            field_dict["scope"] = scope
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if effective_id is not UNSET:
            field_dict["effective_id"] = effective_id
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if project is not UNSET:
            field_dict["project"] = project
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_description is not UNSET:
            field_dict["project_description"] = project_description
        if project_end_date is not UNSET:
            field_dict["project_end_date"] = project_end_date
        if project_end_date_requested_by is not UNSET:
            field_dict["project_end_date_requested_by"] = project_end_date_requested_by
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if offering_slug is not UNSET:
            field_dict["offering_slug"] = offering_slug
        if parent_offering_uuid is not UNSET:
            field_dict["parent_offering_uuid"] = parent_offering_uuid
        if parent_offering_name is not UNSET:
            field_dict["parent_offering_name"] = parent_offering_name
        if parent_offering_slug is not UNSET:
            field_dict["parent_offering_slug"] = parent_offering_slug
        if offering_backend_id is not UNSET:
            field_dict["offering_backend_id"] = offering_backend_id
        if parent_uuid is not UNSET:
            field_dict["parent_uuid"] = parent_uuid
        if parent_name is not UNSET:
            field_dict["parent_name"] = parent_name
        if backend_metadata is not UNSET:
            field_dict["backend_metadata"] = backend_metadata
        if is_usage_based is not UNSET:
            field_dict["is_usage_based"] = is_usage_based
        if is_limit_based is not UNSET:
            field_dict["is_limit_based"] = is_limit_based
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if current_usages is not UNSET:
            field_dict["current_usages"] = current_usages
        if can_terminate is not UNSET:
            field_dict["can_terminate"] = can_terminate
        if report is not UNSET:
            field_dict["report"] = report
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if end_date_requested_by is not UNSET:
            field_dict["end_date_requested_by"] = end_date_requested_by
        if username is not UNSET:
            field_dict["username"] = username
        if limit_usage is not UNSET:
            field_dict["limit_usage"] = limit_usage
        if downscaled is not UNSET:
            field_dict["downscaled"] = downscaled
        if restrict_member_access is not UNSET:
            field_dict["restrict_member_access"] = restrict_member_access
        if paused is not UNSET:
            field_dict["paused"] = paused
        if endpoints is not UNSET:
            field_dict["endpoints"] = endpoints
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if options is not UNSET:
            field_dict["options"] = options
        if available_actions is not UNSET:
            field_dict["available_actions"] = available_actions
        if last_sync is not UNSET:
            field_dict["last_sync"] = last_sync
        if order_in_progress is not UNSET:
            field_dict["order_in_progress"] = order_in_progress
        if creation_order is not UNSET:
            field_dict["creation_order"] = creation_order
        if service_settings_uuid is not UNSET:
            field_dict["service_settings_uuid"] = service_settings_uuid
        if project_slug is not UNSET:
            field_dict["project_slug"] = project_slug
        if customer_slug is not UNSET:
            field_dict["customer_slug"] = customer_slug
        if user_requires_reconsent is not UNSET:
            field_dict["user_requires_reconsent"] = user_requires_reconsent
        if renewal_date is not UNSET:
            field_dict["renewal_date"] = renewal_date
        if offering_state is not UNSET:
            field_dict["offering_state"] = offering_state
        if offering_components is not UNSET:
            field_dict["offering_components"] = offering_components
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_by_username is not UNSET:
            field_dict["created_by_username"] = created_by_username
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if consumer_reviewed_by is not UNSET:
            field_dict["consumer_reviewed_by"] = consumer_reviewed_by
        if consumer_reviewed_by_username is not UNSET:
            field_dict["consumer_reviewed_by_username"] = consumer_reviewed_by_username
        if consumer_reviewed_by_full_name is not UNSET:
            field_dict["consumer_reviewed_by_full_name"] = consumer_reviewed_by_full_name
        if slots is not UNSET:
            field_dict["slots"] = slots

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backend_metadata import BackendMetadata
        from ..models.booking_resource_attributes import BookingResourceAttributes
        from ..models.booking_resource_current_usages import BookingResourceCurrentUsages
        from ..models.booking_resource_limit_usage import BookingResourceLimitUsage
        from ..models.booking_resource_limits import BookingResourceLimits
        from ..models.booking_resource_renewal_date_type_0 import BookingResourceRenewalDateType0
        from ..models.booking_slot import BookingSlot
        from ..models.nested_endpoint import NestedEndpoint
        from ..models.offering_component import OfferingComponent
        from ..models.order_details import OrderDetails
        from ..models.report_section import ReportSection

        d = dict(src_dict)
        offering = d.pop("offering", UNSET)

        offering_name = d.pop("offering_name", UNSET)

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        offering_description = d.pop("offering_description", UNSET)

        offering_image = d.pop("offering_image", UNSET)

        offering_thumbnail = d.pop("offering_thumbnail", UNSET)

        offering_type = d.pop("offering_type", UNSET)

        offering_shared = d.pop("offering_shared", UNSET)

        offering_billable = d.pop("offering_billable", UNSET)

        offering_plugin_options = d.pop("offering_plugin_options", UNSET)

        provider_name = d.pop("provider_name", UNSET)

        _provider_uuid = d.pop("provider_uuid", UNSET)
        provider_uuid: Union[Unset, UUID]
        if isinstance(_provider_uuid, Unset):
            provider_uuid = UNSET
        else:
            provider_uuid = UUID(_provider_uuid)

        provider_slug = d.pop("provider_slug", UNSET)

        category_title = d.pop("category_title", UNSET)

        _category_uuid = d.pop("category_uuid", UNSET)
        category_uuid: Union[Unset, UUID]
        if isinstance(_category_uuid, Unset):
            category_uuid = UNSET
        else:
            category_uuid = UUID(_category_uuid)

        category_icon = d.pop("category_icon", UNSET)

        plan = d.pop("plan", UNSET)

        def _parse_plan_unit(data: object) -> Union[BillingUnit, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_unit_type_1 = BillingUnit(data)

                return plan_unit_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BillingUnit, None, Unset], data)

        plan_unit = _parse_plan_unit(d.pop("plan_unit", UNSET))

        def _parse_plan_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan_name = _parse_plan_name(d.pop("plan_name", UNSET))

        def _parse_plan_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_uuid_type_0 = UUID(data)

                return plan_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        plan_uuid = _parse_plan_uuid(d.pop("plan_uuid", UNSET))

        def _parse_plan_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan_description = _parse_plan_description(d.pop("plan_description", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, BookingResourceAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = BookingResourceAttributes.from_dict(_attributes)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, BookingResourceLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = BookingResourceLimits.from_dict(_limits)

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

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        url = d.pop("url", UNSET)

        scope = d.pop("scope", UNSET)

        description = d.pop("description", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, ResourceState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = ResourceState(_state)

        def _parse_resource_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        backend_id = d.pop("backend_id", UNSET)

        effective_id = d.pop("effective_id", UNSET)

        def _parse_resource_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource_type = _parse_resource_type(d.pop("resource_type", UNSET))

        project = d.pop("project", UNSET)

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        project_name = d.pop("project_name", UNSET)

        project_description = d.pop("project_description", UNSET)

        def _parse_project_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_end_date_type_0 = isoparse(data).date()

                return project_end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        project_end_date = _parse_project_end_date(d.pop("project_end_date", UNSET))

        project_end_date_requested_by = d.pop("project_end_date_requested_by", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        offering_slug = d.pop("offering_slug", UNSET)

        _parent_offering_uuid = d.pop("parent_offering_uuid", UNSET)
        parent_offering_uuid: Union[Unset, UUID]
        if isinstance(_parent_offering_uuid, Unset):
            parent_offering_uuid = UNSET
        else:
            parent_offering_uuid = UUID(_parent_offering_uuid)

        parent_offering_name = d.pop("parent_offering_name", UNSET)

        parent_offering_slug = d.pop("parent_offering_slug", UNSET)

        offering_backend_id = d.pop("offering_backend_id", UNSET)

        _parent_uuid = d.pop("parent_uuid", UNSET)
        parent_uuid: Union[Unset, UUID]
        if isinstance(_parent_uuid, Unset):
            parent_uuid = UNSET
        else:
            parent_uuid = UUID(_parent_uuid)

        parent_name = d.pop("parent_name", UNSET)

        _backend_metadata = d.pop("backend_metadata", UNSET)
        backend_metadata: Union[Unset, BackendMetadata]
        if isinstance(_backend_metadata, Unset):
            backend_metadata = UNSET
        else:
            backend_metadata = BackendMetadata.from_dict(_backend_metadata)

        is_usage_based = d.pop("is_usage_based", UNSET)

        is_limit_based = d.pop("is_limit_based", UNSET)

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        _current_usages = d.pop("current_usages", UNSET)
        current_usages: Union[Unset, BookingResourceCurrentUsages]
        if isinstance(_current_usages, Unset):
            current_usages = UNSET
        else:
            current_usages = BookingResourceCurrentUsages.from_dict(_current_usages)

        can_terminate = d.pop("can_terminate", UNSET)

        report = []
        _report = d.pop("report", UNSET)
        for report_item_data in _report or []:
            report_item = ReportSection.from_dict(report_item_data)

            report.append(report_item)

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        def _parse_end_date_requested_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end_date_requested_by = _parse_end_date_requested_by(d.pop("end_date_requested_by", UNSET))

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        _limit_usage = d.pop("limit_usage", UNSET)
        limit_usage: Union[Unset, BookingResourceLimitUsage]
        if isinstance(_limit_usage, Unset):
            limit_usage = UNSET
        else:
            limit_usage = BookingResourceLimitUsage.from_dict(_limit_usage)

        downscaled = d.pop("downscaled", UNSET)

        restrict_member_access = d.pop("restrict_member_access", UNSET)

        paused = d.pop("paused", UNSET)

        endpoints = []
        _endpoints = d.pop("endpoints", UNSET)
        for endpoints_item_data in _endpoints or []:
            endpoints_item = NestedEndpoint.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        options = d.pop("options", UNSET)

        available_actions = cast(list[str], d.pop("available_actions", UNSET))

        _last_sync = d.pop("last_sync", UNSET)
        last_sync: Union[Unset, datetime.datetime]
        if isinstance(_last_sync, Unset):
            last_sync = UNSET
        else:
            last_sync = isoparse(_last_sync)

        def _parse_order_in_progress(data: object) -> Union["OrderDetails", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                order_in_progress_type_1 = OrderDetails.from_dict(data)

                return order_in_progress_type_1
            except:  # noqa: E722
                pass
            return cast(Union["OrderDetails", None, Unset], data)

        order_in_progress = _parse_order_in_progress(d.pop("order_in_progress", UNSET))

        def _parse_creation_order(data: object) -> Union["OrderDetails", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                creation_order_type_1 = OrderDetails.from_dict(data)

                return creation_order_type_1
            except:  # noqa: E722
                pass
            return cast(Union["OrderDetails", None, Unset], data)

        creation_order = _parse_creation_order(d.pop("creation_order", UNSET))

        _service_settings_uuid = d.pop("service_settings_uuid", UNSET)
        service_settings_uuid: Union[Unset, UUID]
        if isinstance(_service_settings_uuid, Unset):
            service_settings_uuid = UNSET
        else:
            service_settings_uuid = UUID(_service_settings_uuid)

        project_slug = d.pop("project_slug", UNSET)

        customer_slug = d.pop("customer_slug", UNSET)

        user_requires_reconsent = d.pop("user_requires_reconsent", UNSET)

        def _parse_renewal_date(data: object) -> Union["BookingResourceRenewalDateType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                renewal_date_type_0 = BookingResourceRenewalDateType0.from_dict(data)

                return renewal_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BookingResourceRenewalDateType0", None, Unset], data)

        renewal_date = _parse_renewal_date(d.pop("renewal_date", UNSET))

        _offering_state = d.pop("offering_state", UNSET)
        offering_state: Union[Unset, OfferingState]
        if isinstance(_offering_state, Unset):
            offering_state = UNSET
        else:
            offering_state = OfferingState(_offering_state)

        offering_components = []
        _offering_components = d.pop("offering_components", UNSET)
        for offering_components_item_data in _offering_components or []:
            offering_components_item = OfferingComponent.from_dict(offering_components_item_data)

            offering_components.append(offering_components_item)

        created_by = d.pop("created_by", UNSET)

        created_by_username = d.pop("created_by_username", UNSET)

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        consumer_reviewed_by = d.pop("consumer_reviewed_by", UNSET)

        consumer_reviewed_by_username = d.pop("consumer_reviewed_by_username", UNSET)

        consumer_reviewed_by_full_name = d.pop("consumer_reviewed_by_full_name", UNSET)

        slots = []
        _slots = d.pop("slots", UNSET)
        for slots_item_data in _slots or []:
            slots_item = BookingSlot.from_dict(slots_item_data)

            slots.append(slots_item)

        booking_resource = cls(
            offering=offering,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            offering_description=offering_description,
            offering_image=offering_image,
            offering_thumbnail=offering_thumbnail,
            offering_type=offering_type,
            offering_shared=offering_shared,
            offering_billable=offering_billable,
            offering_plugin_options=offering_plugin_options,
            provider_name=provider_name,
            provider_uuid=provider_uuid,
            provider_slug=provider_slug,
            category_title=category_title,
            category_uuid=category_uuid,
            category_icon=category_icon,
            plan=plan,
            plan_unit=plan_unit,
            plan_name=plan_name,
            plan_uuid=plan_uuid,
            plan_description=plan_description,
            attributes=attributes,
            limits=limits,
            uuid=uuid,
            created=created,
            modified=modified,
            url=url,
            scope=scope,
            description=description,
            state=state,
            resource_uuid=resource_uuid,
            backend_id=backend_id,
            effective_id=effective_id,
            resource_type=resource_type,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            project_description=project_description,
            project_end_date=project_end_date,
            project_end_date_requested_by=project_end_date_requested_by,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            offering_slug=offering_slug,
            parent_offering_uuid=parent_offering_uuid,
            parent_offering_name=parent_offering_name,
            parent_offering_slug=parent_offering_slug,
            offering_backend_id=offering_backend_id,
            parent_uuid=parent_uuid,
            parent_name=parent_name,
            backend_metadata=backend_metadata,
            is_usage_based=is_usage_based,
            is_limit_based=is_limit_based,
            name=name,
            slug=slug,
            current_usages=current_usages,
            can_terminate=can_terminate,
            report=report,
            end_date=end_date,
            end_date_requested_by=end_date_requested_by,
            username=username,
            limit_usage=limit_usage,
            downscaled=downscaled,
            restrict_member_access=restrict_member_access,
            paused=paused,
            endpoints=endpoints,
            error_message=error_message,
            error_traceback=error_traceback,
            options=options,
            available_actions=available_actions,
            last_sync=last_sync,
            order_in_progress=order_in_progress,
            creation_order=creation_order,
            service_settings_uuid=service_settings_uuid,
            project_slug=project_slug,
            customer_slug=customer_slug,
            user_requires_reconsent=user_requires_reconsent,
            renewal_date=renewal_date,
            offering_state=offering_state,
            offering_components=offering_components,
            created_by=created_by,
            created_by_username=created_by_username,
            created_by_full_name=created_by_full_name,
            consumer_reviewed_by=consumer_reviewed_by,
            consumer_reviewed_by_username=consumer_reviewed_by_username,
            consumer_reviewed_by_full_name=consumer_reviewed_by_full_name,
            slots=slots,
        )

        booking_resource.additional_properties = d
        return booking_resource

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

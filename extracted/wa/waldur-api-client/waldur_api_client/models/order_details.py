import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_unit import BillingUnit
from ..models.order_state import OrderState
from ..models.request_types import RequestTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.issue_reference import IssueReference
    from ..models.order_details_limits import OrderDetailsLimits


T = TypeVar("T", bound="OrderDetails")


@_attrs_define
class OrderDetails:
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
        attributes (Union[Unset, Any]):
        limits (Union[Unset, OrderDetailsLimits]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        resource_uuid (Union[None, UUID, Unset]):
        resource_type (Union[None, Unset, str]):
        resource_name (Union[Unset, str]):
        cost (Union[None, Unset, str]):
        state (Union[Unset, OrderState]):
        output (Union[Unset, str]):
        marketplace_resource_uuid (Union[Unset, UUID]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        callback_url (Union[None, Unset, str]):
        completed_at (Union[None, Unset, datetime.datetime]):
        request_comment (Union[None, Unset, str]):
        attachment (Union[None, Unset, str]):
        type_ (Union[Unset, RequestTypes]):  Default: RequestTypes.CREATE.
        start_date (Union[None, Unset, datetime.date]): Enables delayed processing of resource provisioning order.
        slug (Union[Unset, str]):
        url (Union[Unset, str]):
        consumer_reviewed_by (Union[None, Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers
            and @/./+/-/_ characters
        consumer_reviewed_by_full_name (Union[None, Unset, str]):
        consumer_reviewed_by_username (Union[None, Unset, str]): Required. 128 characters or fewer. Lowercase letters,
            numbers and @/./+/-/_ characters
        consumer_reviewed_at (Union[None, Unset, datetime.datetime]):
        provider_reviewed_by (Union[None, Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers
            and @/./+/-/_ characters
        provider_reviewed_by_full_name (Union[None, Unset, str]):
        provider_reviewed_by_username (Union[None, Unset, str]): Required. 128 characters or fewer. Lowercase letters,
            numbers and @/./+/-/_ characters
        provider_reviewed_at (Union[None, Unset, datetime.datetime]):
        created_by_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and
            @/./+/-/_ characters
        created_by_full_name (Union[Unset, str]):
        created_by_civil_number (Union[None, Unset, str]):
        created_by_email (Union[None, Unset, str]):
        created_by_organization (Union[None, Unset, str]):
        created_by_organization_registry_code (Union[None, Unset, str]): Company registration code of the user's
            organization, if known
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        customer_slug (Union[Unset, str]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        project_description (Union[Unset, str]):
        project_slug (Union[Unset, str]):
        old_plan_name (Union[None, Unset, str]):
        new_plan_name (Union[None, Unset, str]):
        old_plan_uuid (Union[None, UUID, Unset]):
        new_plan_uuid (Union[None, UUID, Unset]):
        old_cost_estimate (Union[Unset, float]):
        new_cost_estimate (Union[None, Unset, str]):
        can_terminate (Union[Unset, bool]):
        fixed_price (Union[Unset, float]):
        activation_price (Union[Unset, float]):
        termination_comment (Union[None, Unset, str]):
        backend_id (Union[Unset, str]):
        order_subtype (Union[None, Unset, str]):
        provider_message (Union[Unset, str]):
        provider_message_url (Union[Unset, str]):
        provider_message_attachment (Union[None, Unset, str]):
        consumer_message (Union[Unset, str]):
        consumer_message_attachment (Union[None, Unset, str]):
        consumer_rejection_comment (Union[Unset, str]):
        provider_rejection_comment (Union[Unset, str]):
        issue (Union['IssueReference', None, Unset]):
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
    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, "OrderDetailsLimits"] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    resource_uuid: Union[None, UUID, Unset] = UNSET
    resource_type: Union[None, Unset, str] = UNSET
    resource_name: Union[Unset, str] = UNSET
    cost: Union[None, Unset, str] = UNSET
    state: Union[Unset, OrderState] = UNSET
    output: Union[Unset, str] = UNSET
    marketplace_resource_uuid: Union[Unset, UUID] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    callback_url: Union[None, Unset, str] = UNSET
    completed_at: Union[None, Unset, datetime.datetime] = UNSET
    request_comment: Union[None, Unset, str] = UNSET
    attachment: Union[None, Unset, str] = UNSET
    type_: Union[Unset, RequestTypes] = RequestTypes.CREATE
    start_date: Union[None, Unset, datetime.date] = UNSET
    slug: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    consumer_reviewed_by: Union[None, Unset, str] = UNSET
    consumer_reviewed_by_full_name: Union[None, Unset, str] = UNSET
    consumer_reviewed_by_username: Union[None, Unset, str] = UNSET
    consumer_reviewed_at: Union[None, Unset, datetime.datetime] = UNSET
    provider_reviewed_by: Union[None, Unset, str] = UNSET
    provider_reviewed_by_full_name: Union[None, Unset, str] = UNSET
    provider_reviewed_by_username: Union[None, Unset, str] = UNSET
    provider_reviewed_at: Union[None, Unset, datetime.datetime] = UNSET
    created_by_username: Union[Unset, str] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    created_by_civil_number: Union[None, Unset, str] = UNSET
    created_by_email: Union[None, Unset, str] = UNSET
    created_by_organization: Union[None, Unset, str] = UNSET
    created_by_organization_registry_code: Union[None, Unset, str] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_slug: Union[Unset, str] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    project_description: Union[Unset, str] = UNSET
    project_slug: Union[Unset, str] = UNSET
    old_plan_name: Union[None, Unset, str] = UNSET
    new_plan_name: Union[None, Unset, str] = UNSET
    old_plan_uuid: Union[None, UUID, Unset] = UNSET
    new_plan_uuid: Union[None, UUID, Unset] = UNSET
    old_cost_estimate: Union[Unset, float] = UNSET
    new_cost_estimate: Union[None, Unset, str] = UNSET
    can_terminate: Union[Unset, bool] = UNSET
    fixed_price: Union[Unset, float] = UNSET
    activation_price: Union[Unset, float] = UNSET
    termination_comment: Union[None, Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    order_subtype: Union[None, Unset, str] = UNSET
    provider_message: Union[Unset, str] = UNSET
    provider_message_url: Union[Unset, str] = UNSET
    provider_message_attachment: Union[None, Unset, str] = UNSET
    consumer_message: Union[Unset, str] = UNSET
    consumer_message_attachment: Union[None, Unset, str] = UNSET
    consumer_rejection_comment: Union[Unset, str] = UNSET
    provider_rejection_comment: Union[Unset, str] = UNSET
    issue: Union["IssueReference", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.issue_reference import IssueReference

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

        attributes = self.attributes

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

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        elif isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        resource_type: Union[None, Unset, str]
        if isinstance(self.resource_type, Unset):
            resource_type = UNSET
        else:
            resource_type = self.resource_type

        resource_name = self.resource_name

        cost: Union[None, Unset, str]
        if isinstance(self.cost, Unset):
            cost = UNSET
        else:
            cost = self.cost

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        output = self.output

        marketplace_resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.marketplace_resource_uuid, Unset):
            marketplace_resource_uuid = str(self.marketplace_resource_uuid)

        error_message = self.error_message

        error_traceback = self.error_traceback

        callback_url: Union[None, Unset, str]
        if isinstance(self.callback_url, Unset):
            callback_url = UNSET
        else:
            callback_url = self.callback_url

        completed_at: Union[None, Unset, str]
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        request_comment: Union[None, Unset, str]
        if isinstance(self.request_comment, Unset):
            request_comment = UNSET
        else:
            request_comment = self.request_comment

        attachment: Union[None, Unset, str]
        if isinstance(self.attachment, Unset):
            attachment = UNSET
        else:
            attachment = self.attachment

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

        url = self.url

        consumer_reviewed_by: Union[None, Unset, str]
        if isinstance(self.consumer_reviewed_by, Unset):
            consumer_reviewed_by = UNSET
        else:
            consumer_reviewed_by = self.consumer_reviewed_by

        consumer_reviewed_by_full_name: Union[None, Unset, str]
        if isinstance(self.consumer_reviewed_by_full_name, Unset):
            consumer_reviewed_by_full_name = UNSET
        else:
            consumer_reviewed_by_full_name = self.consumer_reviewed_by_full_name

        consumer_reviewed_by_username: Union[None, Unset, str]
        if isinstance(self.consumer_reviewed_by_username, Unset):
            consumer_reviewed_by_username = UNSET
        else:
            consumer_reviewed_by_username = self.consumer_reviewed_by_username

        consumer_reviewed_at: Union[None, Unset, str]
        if isinstance(self.consumer_reviewed_at, Unset):
            consumer_reviewed_at = UNSET
        elif isinstance(self.consumer_reviewed_at, datetime.datetime):
            consumer_reviewed_at = self.consumer_reviewed_at.isoformat()
        else:
            consumer_reviewed_at = self.consumer_reviewed_at

        provider_reviewed_by: Union[None, Unset, str]
        if isinstance(self.provider_reviewed_by, Unset):
            provider_reviewed_by = UNSET
        else:
            provider_reviewed_by = self.provider_reviewed_by

        provider_reviewed_by_full_name: Union[None, Unset, str]
        if isinstance(self.provider_reviewed_by_full_name, Unset):
            provider_reviewed_by_full_name = UNSET
        else:
            provider_reviewed_by_full_name = self.provider_reviewed_by_full_name

        provider_reviewed_by_username: Union[None, Unset, str]
        if isinstance(self.provider_reviewed_by_username, Unset):
            provider_reviewed_by_username = UNSET
        else:
            provider_reviewed_by_username = self.provider_reviewed_by_username

        provider_reviewed_at: Union[None, Unset, str]
        if isinstance(self.provider_reviewed_at, Unset):
            provider_reviewed_at = UNSET
        elif isinstance(self.provider_reviewed_at, datetime.datetime):
            provider_reviewed_at = self.provider_reviewed_at.isoformat()
        else:
            provider_reviewed_at = self.provider_reviewed_at

        created_by_username = self.created_by_username

        created_by_full_name = self.created_by_full_name

        created_by_civil_number: Union[None, Unset, str]
        if isinstance(self.created_by_civil_number, Unset):
            created_by_civil_number = UNSET
        else:
            created_by_civil_number = self.created_by_civil_number

        created_by_email: Union[None, Unset, str]
        if isinstance(self.created_by_email, Unset):
            created_by_email = UNSET
        else:
            created_by_email = self.created_by_email

        created_by_organization: Union[None, Unset, str]
        if isinstance(self.created_by_organization, Unset):
            created_by_organization = UNSET
        else:
            created_by_organization = self.created_by_organization

        created_by_organization_registry_code: Union[None, Unset, str]
        if isinstance(self.created_by_organization_registry_code, Unset):
            created_by_organization_registry_code = UNSET
        else:
            created_by_organization_registry_code = self.created_by_organization_registry_code

        customer_name = self.customer_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_slug = self.customer_slug

        project_name = self.project_name

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        project_description = self.project_description

        project_slug = self.project_slug

        old_plan_name: Union[None, Unset, str]
        if isinstance(self.old_plan_name, Unset):
            old_plan_name = UNSET
        else:
            old_plan_name = self.old_plan_name

        new_plan_name: Union[None, Unset, str]
        if isinstance(self.new_plan_name, Unset):
            new_plan_name = UNSET
        else:
            new_plan_name = self.new_plan_name

        old_plan_uuid: Union[None, Unset, str]
        if isinstance(self.old_plan_uuid, Unset):
            old_plan_uuid = UNSET
        elif isinstance(self.old_plan_uuid, UUID):
            old_plan_uuid = str(self.old_plan_uuid)
        else:
            old_plan_uuid = self.old_plan_uuid

        new_plan_uuid: Union[None, Unset, str]
        if isinstance(self.new_plan_uuid, Unset):
            new_plan_uuid = UNSET
        elif isinstance(self.new_plan_uuid, UUID):
            new_plan_uuid = str(self.new_plan_uuid)
        else:
            new_plan_uuid = self.new_plan_uuid

        old_cost_estimate = self.old_cost_estimate

        new_cost_estimate: Union[None, Unset, str]
        if isinstance(self.new_cost_estimate, Unset):
            new_cost_estimate = UNSET
        else:
            new_cost_estimate = self.new_cost_estimate

        can_terminate = self.can_terminate

        fixed_price = self.fixed_price

        activation_price = self.activation_price

        termination_comment: Union[None, Unset, str]
        if isinstance(self.termination_comment, Unset):
            termination_comment = UNSET
        else:
            termination_comment = self.termination_comment

        backend_id = self.backend_id

        order_subtype: Union[None, Unset, str]
        if isinstance(self.order_subtype, Unset):
            order_subtype = UNSET
        else:
            order_subtype = self.order_subtype

        provider_message = self.provider_message

        provider_message_url = self.provider_message_url

        provider_message_attachment: Union[None, Unset, str]
        if isinstance(self.provider_message_attachment, Unset):
            provider_message_attachment = UNSET
        else:
            provider_message_attachment = self.provider_message_attachment

        consumer_message = self.consumer_message

        consumer_message_attachment: Union[None, Unset, str]
        if isinstance(self.consumer_message_attachment, Unset):
            consumer_message_attachment = UNSET
        else:
            consumer_message_attachment = self.consumer_message_attachment

        consumer_rejection_comment = self.consumer_rejection_comment

        provider_rejection_comment = self.provider_rejection_comment

        issue: Union[None, Unset, dict[str, Any]]
        if isinstance(self.issue, Unset):
            issue = UNSET
        elif isinstance(self.issue, IssueReference):
            issue = self.issue.to_dict()
        else:
            issue = self.issue

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
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if resource_name is not UNSET:
            field_dict["resource_name"] = resource_name
        if cost is not UNSET:
            field_dict["cost"] = cost
        if state is not UNSET:
            field_dict["state"] = state
        if output is not UNSET:
            field_dict["output"] = output
        if marketplace_resource_uuid is not UNSET:
            field_dict["marketplace_resource_uuid"] = marketplace_resource_uuid
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if callback_url is not UNSET:
            field_dict["callback_url"] = callback_url
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if request_comment is not UNSET:
            field_dict["request_comment"] = request_comment
        if attachment is not UNSET:
            field_dict["attachment"] = attachment
        if type_ is not UNSET:
            field_dict["type"] = type_
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if slug is not UNSET:
            field_dict["slug"] = slug
        if url is not UNSET:
            field_dict["url"] = url
        if consumer_reviewed_by is not UNSET:
            field_dict["consumer_reviewed_by"] = consumer_reviewed_by
        if consumer_reviewed_by_full_name is not UNSET:
            field_dict["consumer_reviewed_by_full_name"] = consumer_reviewed_by_full_name
        if consumer_reviewed_by_username is not UNSET:
            field_dict["consumer_reviewed_by_username"] = consumer_reviewed_by_username
        if consumer_reviewed_at is not UNSET:
            field_dict["consumer_reviewed_at"] = consumer_reviewed_at
        if provider_reviewed_by is not UNSET:
            field_dict["provider_reviewed_by"] = provider_reviewed_by
        if provider_reviewed_by_full_name is not UNSET:
            field_dict["provider_reviewed_by_full_name"] = provider_reviewed_by_full_name
        if provider_reviewed_by_username is not UNSET:
            field_dict["provider_reviewed_by_username"] = provider_reviewed_by_username
        if provider_reviewed_at is not UNSET:
            field_dict["provider_reviewed_at"] = provider_reviewed_at
        if created_by_username is not UNSET:
            field_dict["created_by_username"] = created_by_username
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_civil_number is not UNSET:
            field_dict["created_by_civil_number"] = created_by_civil_number
        if created_by_email is not UNSET:
            field_dict["created_by_email"] = created_by_email
        if created_by_organization is not UNSET:
            field_dict["created_by_organization"] = created_by_organization
        if created_by_organization_registry_code is not UNSET:
            field_dict["created_by_organization_registry_code"] = created_by_organization_registry_code
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_slug is not UNSET:
            field_dict["customer_slug"] = customer_slug
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if project_description is not UNSET:
            field_dict["project_description"] = project_description
        if project_slug is not UNSET:
            field_dict["project_slug"] = project_slug
        if old_plan_name is not UNSET:
            field_dict["old_plan_name"] = old_plan_name
        if new_plan_name is not UNSET:
            field_dict["new_plan_name"] = new_plan_name
        if old_plan_uuid is not UNSET:
            field_dict["old_plan_uuid"] = old_plan_uuid
        if new_plan_uuid is not UNSET:
            field_dict["new_plan_uuid"] = new_plan_uuid
        if old_cost_estimate is not UNSET:
            field_dict["old_cost_estimate"] = old_cost_estimate
        if new_cost_estimate is not UNSET:
            field_dict["new_cost_estimate"] = new_cost_estimate
        if can_terminate is not UNSET:
            field_dict["can_terminate"] = can_terminate
        if fixed_price is not UNSET:
            field_dict["fixed_price"] = fixed_price
        if activation_price is not UNSET:
            field_dict["activation_price"] = activation_price
        if termination_comment is not UNSET:
            field_dict["termination_comment"] = termination_comment
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if order_subtype is not UNSET:
            field_dict["order_subtype"] = order_subtype
        if provider_message is not UNSET:
            field_dict["provider_message"] = provider_message
        if provider_message_url is not UNSET:
            field_dict["provider_message_url"] = provider_message_url
        if provider_message_attachment is not UNSET:
            field_dict["provider_message_attachment"] = provider_message_attachment
        if consumer_message is not UNSET:
            field_dict["consumer_message"] = consumer_message
        if consumer_message_attachment is not UNSET:
            field_dict["consumer_message_attachment"] = consumer_message_attachment
        if consumer_rejection_comment is not UNSET:
            field_dict["consumer_rejection_comment"] = consumer_rejection_comment
        if provider_rejection_comment is not UNSET:
            field_dict["provider_rejection_comment"] = provider_rejection_comment
        if issue is not UNSET:
            field_dict["issue"] = issue

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.issue_reference import IssueReference
        from ..models.order_details_limits import OrderDetailsLimits

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

        attributes = d.pop("attributes", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, OrderDetailsLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = OrderDetailsLimits.from_dict(_limits)

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

        def _parse_resource_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource_type = _parse_resource_type(d.pop("resource_type", UNSET))

        resource_name = d.pop("resource_name", UNSET)

        def _parse_cost(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cost = _parse_cost(d.pop("cost", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, OrderState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = OrderState(_state)

        output = d.pop("output", UNSET)

        _marketplace_resource_uuid = d.pop("marketplace_resource_uuid", UNSET)
        marketplace_resource_uuid: Union[Unset, UUID]
        if isinstance(_marketplace_resource_uuid, Unset):
            marketplace_resource_uuid = UNSET
        else:
            marketplace_resource_uuid = UUID(_marketplace_resource_uuid)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        def _parse_callback_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        callback_url = _parse_callback_url(d.pop("callback_url", UNSET))

        def _parse_completed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_request_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        request_comment = _parse_request_comment(d.pop("request_comment", UNSET))

        def _parse_attachment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        attachment = _parse_attachment(d.pop("attachment", UNSET))

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

        url = d.pop("url", UNSET)

        def _parse_consumer_reviewed_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        consumer_reviewed_by = _parse_consumer_reviewed_by(d.pop("consumer_reviewed_by", UNSET))

        def _parse_consumer_reviewed_by_full_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        consumer_reviewed_by_full_name = _parse_consumer_reviewed_by_full_name(
            d.pop("consumer_reviewed_by_full_name", UNSET)
        )

        def _parse_consumer_reviewed_by_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        consumer_reviewed_by_username = _parse_consumer_reviewed_by_username(
            d.pop("consumer_reviewed_by_username", UNSET)
        )

        def _parse_consumer_reviewed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                consumer_reviewed_at_type_0 = isoparse(data)

                return consumer_reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        consumer_reviewed_at = _parse_consumer_reviewed_at(d.pop("consumer_reviewed_at", UNSET))

        def _parse_provider_reviewed_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provider_reviewed_by = _parse_provider_reviewed_by(d.pop("provider_reviewed_by", UNSET))

        def _parse_provider_reviewed_by_full_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provider_reviewed_by_full_name = _parse_provider_reviewed_by_full_name(
            d.pop("provider_reviewed_by_full_name", UNSET)
        )

        def _parse_provider_reviewed_by_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provider_reviewed_by_username = _parse_provider_reviewed_by_username(
            d.pop("provider_reviewed_by_username", UNSET)
        )

        def _parse_provider_reviewed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provider_reviewed_at_type_0 = isoparse(data)

                return provider_reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        provider_reviewed_at = _parse_provider_reviewed_at(d.pop("provider_reviewed_at", UNSET))

        created_by_username = d.pop("created_by_username", UNSET)

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        def _parse_created_by_civil_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_civil_number = _parse_created_by_civil_number(d.pop("created_by_civil_number", UNSET))

        def _parse_created_by_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_email = _parse_created_by_email(d.pop("created_by_email", UNSET))

        def _parse_created_by_organization(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_organization = _parse_created_by_organization(d.pop("created_by_organization", UNSET))

        def _parse_created_by_organization_registry_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_organization_registry_code = _parse_created_by_organization_registry_code(
            d.pop("created_by_organization_registry_code", UNSET)
        )

        customer_name = d.pop("customer_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_slug = d.pop("customer_slug", UNSET)

        project_name = d.pop("project_name", UNSET)

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        project_description = d.pop("project_description", UNSET)

        project_slug = d.pop("project_slug", UNSET)

        def _parse_old_plan_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        old_plan_name = _parse_old_plan_name(d.pop("old_plan_name", UNSET))

        def _parse_new_plan_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_plan_name = _parse_new_plan_name(d.pop("new_plan_name", UNSET))

        def _parse_old_plan_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                old_plan_uuid_type_0 = UUID(data)

                return old_plan_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        old_plan_uuid = _parse_old_plan_uuid(d.pop("old_plan_uuid", UNSET))

        def _parse_new_plan_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                new_plan_uuid_type_0 = UUID(data)

                return new_plan_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        new_plan_uuid = _parse_new_plan_uuid(d.pop("new_plan_uuid", UNSET))

        old_cost_estimate = d.pop("old_cost_estimate", UNSET)

        def _parse_new_cost_estimate(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_cost_estimate = _parse_new_cost_estimate(d.pop("new_cost_estimate", UNSET))

        can_terminate = d.pop("can_terminate", UNSET)

        fixed_price = d.pop("fixed_price", UNSET)

        activation_price = d.pop("activation_price", UNSET)

        def _parse_termination_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        termination_comment = _parse_termination_comment(d.pop("termination_comment", UNSET))

        backend_id = d.pop("backend_id", UNSET)

        def _parse_order_subtype(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        order_subtype = _parse_order_subtype(d.pop("order_subtype", UNSET))

        provider_message = d.pop("provider_message", UNSET)

        provider_message_url = d.pop("provider_message_url", UNSET)

        def _parse_provider_message_attachment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provider_message_attachment = _parse_provider_message_attachment(d.pop("provider_message_attachment", UNSET))

        consumer_message = d.pop("consumer_message", UNSET)

        def _parse_consumer_message_attachment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        consumer_message_attachment = _parse_consumer_message_attachment(d.pop("consumer_message_attachment", UNSET))

        consumer_rejection_comment = d.pop("consumer_rejection_comment", UNSET)

        provider_rejection_comment = d.pop("provider_rejection_comment", UNSET)

        def _parse_issue(data: object) -> Union["IssueReference", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                issue_type_1 = IssueReference.from_dict(data)

                return issue_type_1
            except:  # noqa: E722
                pass
            return cast(Union["IssueReference", None, Unset], data)

        issue = _parse_issue(d.pop("issue", UNSET))

        order_details = cls(
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
            resource_uuid=resource_uuid,
            resource_type=resource_type,
            resource_name=resource_name,
            cost=cost,
            state=state,
            output=output,
            marketplace_resource_uuid=marketplace_resource_uuid,
            error_message=error_message,
            error_traceback=error_traceback,
            callback_url=callback_url,
            completed_at=completed_at,
            request_comment=request_comment,
            attachment=attachment,
            type_=type_,
            start_date=start_date,
            slug=slug,
            url=url,
            consumer_reviewed_by=consumer_reviewed_by,
            consumer_reviewed_by_full_name=consumer_reviewed_by_full_name,
            consumer_reviewed_by_username=consumer_reviewed_by_username,
            consumer_reviewed_at=consumer_reviewed_at,
            provider_reviewed_by=provider_reviewed_by,
            provider_reviewed_by_full_name=provider_reviewed_by_full_name,
            provider_reviewed_by_username=provider_reviewed_by_username,
            provider_reviewed_at=provider_reviewed_at,
            created_by_username=created_by_username,
            created_by_full_name=created_by_full_name,
            created_by_civil_number=created_by_civil_number,
            created_by_email=created_by_email,
            created_by_organization=created_by_organization,
            created_by_organization_registry_code=created_by_organization_registry_code,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            customer_slug=customer_slug,
            project_name=project_name,
            project_uuid=project_uuid,
            project_description=project_description,
            project_slug=project_slug,
            old_plan_name=old_plan_name,
            new_plan_name=new_plan_name,
            old_plan_uuid=old_plan_uuid,
            new_plan_uuid=new_plan_uuid,
            old_cost_estimate=old_cost_estimate,
            new_cost_estimate=new_cost_estimate,
            can_terminate=can_terminate,
            fixed_price=fixed_price,
            activation_price=activation_price,
            termination_comment=termination_comment,
            backend_id=backend_id,
            order_subtype=order_subtype,
            provider_message=provider_message,
            provider_message_url=provider_message_url,
            provider_message_attachment=provider_message_attachment,
            consumer_message=consumer_message,
            consumer_message_attachment=consumer_message_attachment,
            consumer_rejection_comment=consumer_rejection_comment,
            provider_rejection_comment=provider_rejection_comment,
            issue=issue,
        )

        order_details.additional_properties = d
        return order_details

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

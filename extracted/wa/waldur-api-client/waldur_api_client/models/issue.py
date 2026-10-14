import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.issue_processing_log import IssueProcessingLog
    from ..models.issue_provider_ticket_info_type_0 import IssueProviderTicketInfoType0
    from ..models.nested_feedback import NestedFeedback


T = TypeVar("T", bound="Issue")


@_attrs_define
class Issue:
    """
    Attributes:
        url (str):
        uuid (UUID):
        type_ (str):
        key (str):
        backend_id (Union[None, str]):
        backend_name (Union[None, str]):
        summary (str):
        status (str):
        resolution (str):
        caller_uuid (Union[None, UUID]):
        caller_full_name (Union[None, str]):
        reporter (str):
        reporter_uuid (Union[None, UUID]):
        reporter_name (Union[None, str]):
        assignee_uuid (Union[None, UUID]):
        assignee_name (Union[None, str]):
        customer_uuid (Union[None, UUID]):
        customer_name (Union[None, str]):
        project_uuid (Union[None, UUID]):
        project_name (Union[None, str]):
        resource_type (str):
        resource_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        feedback (Union['NestedFeedback', None]):
        resolved (Union[None, bool]):
        update_is_available (bool):
        destroy_is_available (bool):
        available_statuses (list[str]):
        add_comment_is_available (bool):
        add_attachment_is_available (bool):
        order_uuid (Union[None, str]): Return order UUID if the issue's resource is an Order.
        order_project_uuid (Union[None, str]): Return order's project UUID if the issue's resource is an Order.
        order_customer_uuid (Union[None, str]): Return order's customer UUID if the issue's resource is an Order.
        order_resource_name (Union[None, str]): Return order's resource name if the issue's resource is an Order.
        first_response_deadline (Union[None, datetime.datetime]): Deadline for first response from support staff.
        resolution_deadline (Union[None, datetime.datetime]): Deadline for issue resolution.
        first_response_at (Union[None, datetime.datetime]): Timestamp of first response from support staff.
        sla_breached (bool): Whether SLA has been breached for this issue.
        sla_status (str):
        parent_issue (str):
        provider_helpdesk (str):
        is_escalated (bool): Whether this issue has been escalated.
        escalated_at (Union[None, datetime.datetime]): When the issue was escalated.
        escalation_reason (str): Reason for escalation.
        is_routed (bool):
        provider_ticket_info (Union['IssueProviderTicketInfoType0', None]):
        remote_id (Union[None, Unset, str]):
        link (Union[Unset, str]): Link to issue in support system.
        description (Union[Unset, str]):
        priority (Union[Unset, str]):
        caller (Union[None, Unset, str]):
        assignee (Union[None, Unset, str]):
        customer (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
        resource (Union[Unset, str]):
        offering (Union[None, UUID, Unset]):
        template (Union[None, Unset, str]):
        processing_log (Union[Unset, IssueProcessingLog]): Internal processing log for debugging order lifecycle events.
            Visible only to staff.
    """

    url: str
    uuid: UUID
    type_: str
    key: str
    backend_id: Union[None, str]
    backend_name: Union[None, str]
    summary: str
    status: str
    resolution: str
    caller_uuid: Union[None, UUID]
    caller_full_name: Union[None, str]
    reporter: str
    reporter_uuid: Union[None, UUID]
    reporter_name: Union[None, str]
    assignee_uuid: Union[None, UUID]
    assignee_name: Union[None, str]
    customer_uuid: Union[None, UUID]
    customer_name: Union[None, str]
    project_uuid: Union[None, UUID]
    project_name: Union[None, str]
    resource_type: str
    resource_name: str
    created: datetime.datetime
    modified: datetime.datetime
    feedback: Union["NestedFeedback", None]
    resolved: Union[None, bool]
    update_is_available: bool
    destroy_is_available: bool
    available_statuses: list[str]
    add_comment_is_available: bool
    add_attachment_is_available: bool
    order_uuid: Union[None, str]
    order_project_uuid: Union[None, str]
    order_customer_uuid: Union[None, str]
    order_resource_name: Union[None, str]
    first_response_deadline: Union[None, datetime.datetime]
    resolution_deadline: Union[None, datetime.datetime]
    first_response_at: Union[None, datetime.datetime]
    sla_breached: bool
    sla_status: str
    parent_issue: str
    provider_helpdesk: str
    is_escalated: bool
    escalated_at: Union[None, datetime.datetime]
    escalation_reason: str
    is_routed: bool
    provider_ticket_info: Union["IssueProviderTicketInfoType0", None]
    remote_id: Union[None, Unset, str] = UNSET
    link: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    priority: Union[Unset, str] = UNSET
    caller: Union[None, Unset, str] = UNSET
    assignee: Union[None, Unset, str] = UNSET
    customer: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    resource: Union[Unset, str] = UNSET
    offering: Union[None, UUID, Unset] = UNSET
    template: Union[None, Unset, str] = UNSET
    processing_log: Union[Unset, "IssueProcessingLog"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.issue_provider_ticket_info_type_0 import IssueProviderTicketInfoType0
        from ..models.nested_feedback import NestedFeedback

        url = self.url

        uuid = str(self.uuid)

        type_ = self.type_

        key = self.key

        backend_id: Union[None, str]
        backend_id = self.backend_id

        backend_name: Union[None, str]
        backend_name = self.backend_name

        summary = self.summary

        status = self.status

        resolution = self.resolution

        caller_uuid: Union[None, str]
        if isinstance(self.caller_uuid, UUID):
            caller_uuid = str(self.caller_uuid)
        else:
            caller_uuid = self.caller_uuid

        caller_full_name: Union[None, str]
        caller_full_name = self.caller_full_name

        reporter = self.reporter

        reporter_uuid: Union[None, str]
        if isinstance(self.reporter_uuid, UUID):
            reporter_uuid = str(self.reporter_uuid)
        else:
            reporter_uuid = self.reporter_uuid

        reporter_name: Union[None, str]
        reporter_name = self.reporter_name

        assignee_uuid: Union[None, str]
        if isinstance(self.assignee_uuid, UUID):
            assignee_uuid = str(self.assignee_uuid)
        else:
            assignee_uuid = self.assignee_uuid

        assignee_name: Union[None, str]
        assignee_name = self.assignee_name

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        project_uuid: Union[None, str]
        if isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        project_name: Union[None, str]
        project_name = self.project_name

        resource_type = self.resource_type

        resource_name = self.resource_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        feedback: Union[None, dict[str, Any]]
        if isinstance(self.feedback, NestedFeedback):
            feedback = self.feedback.to_dict()
        else:
            feedback = self.feedback

        resolved: Union[None, bool]
        resolved = self.resolved

        update_is_available = self.update_is_available

        destroy_is_available = self.destroy_is_available

        available_statuses = self.available_statuses

        add_comment_is_available = self.add_comment_is_available

        add_attachment_is_available = self.add_attachment_is_available

        order_uuid: Union[None, str]
        order_uuid = self.order_uuid

        order_project_uuid: Union[None, str]
        order_project_uuid = self.order_project_uuid

        order_customer_uuid: Union[None, str]
        order_customer_uuid = self.order_customer_uuid

        order_resource_name: Union[None, str]
        order_resource_name = self.order_resource_name

        first_response_deadline: Union[None, str]
        if isinstance(self.first_response_deadline, datetime.datetime):
            first_response_deadline = self.first_response_deadline.isoformat()
        else:
            first_response_deadline = self.first_response_deadline

        resolution_deadline: Union[None, str]
        if isinstance(self.resolution_deadline, datetime.datetime):
            resolution_deadline = self.resolution_deadline.isoformat()
        else:
            resolution_deadline = self.resolution_deadline

        first_response_at: Union[None, str]
        if isinstance(self.first_response_at, datetime.datetime):
            first_response_at = self.first_response_at.isoformat()
        else:
            first_response_at = self.first_response_at

        sla_breached = self.sla_breached

        sla_status = self.sla_status

        parent_issue = self.parent_issue

        provider_helpdesk = self.provider_helpdesk

        is_escalated = self.is_escalated

        escalated_at: Union[None, str]
        if isinstance(self.escalated_at, datetime.datetime):
            escalated_at = self.escalated_at.isoformat()
        else:
            escalated_at = self.escalated_at

        escalation_reason = self.escalation_reason

        is_routed = self.is_routed

        provider_ticket_info: Union[None, dict[str, Any]]
        if isinstance(self.provider_ticket_info, IssueProviderTicketInfoType0):
            provider_ticket_info = self.provider_ticket_info.to_dict()
        else:
            provider_ticket_info = self.provider_ticket_info

        remote_id: Union[None, Unset, str]
        if isinstance(self.remote_id, Unset):
            remote_id = UNSET
        else:
            remote_id = self.remote_id

        link = self.link

        description = self.description

        priority = self.priority

        caller: Union[None, Unset, str]
        if isinstance(self.caller, Unset):
            caller = UNSET
        else:
            caller = self.caller

        assignee: Union[None, Unset, str]
        if isinstance(self.assignee, Unset):
            assignee = UNSET
        else:
            assignee = self.assignee

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        resource = self.resource

        offering: Union[None, Unset, str]
        if isinstance(self.offering, Unset):
            offering = UNSET
        elif isinstance(self.offering, UUID):
            offering = str(self.offering)
        else:
            offering = self.offering

        template: Union[None, Unset, str]
        if isinstance(self.template, Unset):
            template = UNSET
        else:
            template = self.template

        processing_log: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.processing_log, Unset):
            processing_log = self.processing_log.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "type": type_,
                "key": key,
                "backend_id": backend_id,
                "backend_name": backend_name,
                "summary": summary,
                "status": status,
                "resolution": resolution,
                "caller_uuid": caller_uuid,
                "caller_full_name": caller_full_name,
                "reporter": reporter,
                "reporter_uuid": reporter_uuid,
                "reporter_name": reporter_name,
                "assignee_uuid": assignee_uuid,
                "assignee_name": assignee_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "resource_type": resource_type,
                "resource_name": resource_name,
                "created": created,
                "modified": modified,
                "feedback": feedback,
                "resolved": resolved,
                "update_is_available": update_is_available,
                "destroy_is_available": destroy_is_available,
                "available_statuses": available_statuses,
                "add_comment_is_available": add_comment_is_available,
                "add_attachment_is_available": add_attachment_is_available,
                "order_uuid": order_uuid,
                "order_project_uuid": order_project_uuid,
                "order_customer_uuid": order_customer_uuid,
                "order_resource_name": order_resource_name,
                "first_response_deadline": first_response_deadline,
                "resolution_deadline": resolution_deadline,
                "first_response_at": first_response_at,
                "sla_breached": sla_breached,
                "sla_status": sla_status,
                "parent_issue": parent_issue,
                "provider_helpdesk": provider_helpdesk,
                "is_escalated": is_escalated,
                "escalated_at": escalated_at,
                "escalation_reason": escalation_reason,
                "is_routed": is_routed,
                "provider_ticket_info": provider_ticket_info,
            }
        )
        if remote_id is not UNSET:
            field_dict["remote_id"] = remote_id
        if link is not UNSET:
            field_dict["link"] = link
        if description is not UNSET:
            field_dict["description"] = description
        if priority is not UNSET:
            field_dict["priority"] = priority
        if caller is not UNSET:
            field_dict["caller"] = caller
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if customer is not UNSET:
            field_dict["customer"] = customer
        if project is not UNSET:
            field_dict["project"] = project
        if resource is not UNSET:
            field_dict["resource"] = resource
        if offering is not UNSET:
            field_dict["offering"] = offering
        if template is not UNSET:
            field_dict["template"] = template
        if processing_log is not UNSET:
            field_dict["processing_log"] = processing_log

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.issue_processing_log import IssueProcessingLog
        from ..models.issue_provider_ticket_info_type_0 import IssueProviderTicketInfoType0
        from ..models.nested_feedback import NestedFeedback

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        type_ = d.pop("type")

        key = d.pop("key")

        def _parse_backend_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id"))

        def _parse_backend_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        backend_name = _parse_backend_name(d.pop("backend_name"))

        summary = d.pop("summary")

        status = d.pop("status")

        resolution = d.pop("resolution")

        def _parse_caller_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                caller_uuid_type_0 = UUID(data)

                return caller_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        caller_uuid = _parse_caller_uuid(d.pop("caller_uuid"))

        def _parse_caller_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        caller_full_name = _parse_caller_full_name(d.pop("caller_full_name"))

        reporter = d.pop("reporter")

        def _parse_reporter_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reporter_uuid_type_0 = UUID(data)

                return reporter_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        reporter_uuid = _parse_reporter_uuid(d.pop("reporter_uuid"))

        def _parse_reporter_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reporter_name = _parse_reporter_name(d.pop("reporter_name"))

        def _parse_assignee_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                assignee_uuid_type_0 = UUID(data)

                return assignee_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        assignee_uuid = _parse_assignee_uuid(d.pop("assignee_uuid"))

        def _parse_assignee_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        assignee_name = _parse_assignee_name(d.pop("assignee_name"))

        def _parse_customer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        def _parse_project_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid"))

        def _parse_project_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_name = _parse_project_name(d.pop("project_name"))

        resource_type = d.pop("resource_type")

        resource_name = d.pop("resource_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_feedback(data: object) -> Union["NestedFeedback", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                feedback_type_1 = NestedFeedback.from_dict(data)

                return feedback_type_1
            except:  # noqa: E722
                pass
            return cast(Union["NestedFeedback", None], data)

        feedback = _parse_feedback(d.pop("feedback"))

        def _parse_resolved(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        resolved = _parse_resolved(d.pop("resolved"))

        update_is_available = d.pop("update_is_available")

        destroy_is_available = d.pop("destroy_is_available")

        available_statuses = cast(list[str], d.pop("available_statuses"))

        add_comment_is_available = d.pop("add_comment_is_available")

        add_attachment_is_available = d.pop("add_attachment_is_available")

        def _parse_order_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        order_uuid = _parse_order_uuid(d.pop("order_uuid"))

        def _parse_order_project_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        order_project_uuid = _parse_order_project_uuid(d.pop("order_project_uuid"))

        def _parse_order_customer_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        order_customer_uuid = _parse_order_customer_uuid(d.pop("order_customer_uuid"))

        def _parse_order_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        order_resource_name = _parse_order_resource_name(d.pop("order_resource_name"))

        def _parse_first_response_deadline(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_response_deadline_type_0 = isoparse(data)

                return first_response_deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        first_response_deadline = _parse_first_response_deadline(d.pop("first_response_deadline"))

        def _parse_resolution_deadline(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolution_deadline_type_0 = isoparse(data)

                return resolution_deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        resolution_deadline = _parse_resolution_deadline(d.pop("resolution_deadline"))

        def _parse_first_response_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_response_at_type_0 = isoparse(data)

                return first_response_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        first_response_at = _parse_first_response_at(d.pop("first_response_at"))

        sla_breached = d.pop("sla_breached")

        sla_status = d.pop("sla_status")

        parent_issue = d.pop("parent_issue")

        provider_helpdesk = d.pop("provider_helpdesk")

        is_escalated = d.pop("is_escalated")

        def _parse_escalated_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                escalated_at_type_0 = isoparse(data)

                return escalated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        escalated_at = _parse_escalated_at(d.pop("escalated_at"))

        escalation_reason = d.pop("escalation_reason")

        is_routed = d.pop("is_routed")

        def _parse_provider_ticket_info(data: object) -> Union["IssueProviderTicketInfoType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                provider_ticket_info_type_0 = IssueProviderTicketInfoType0.from_dict(data)

                return provider_ticket_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["IssueProviderTicketInfoType0", None], data)

        provider_ticket_info = _parse_provider_ticket_info(d.pop("provider_ticket_info"))

        def _parse_remote_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remote_id = _parse_remote_id(d.pop("remote_id", UNSET))

        link = d.pop("link", UNSET)

        description = d.pop("description", UNSET)

        priority = d.pop("priority", UNSET)

        def _parse_caller(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        caller = _parse_caller(d.pop("caller", UNSET))

        def _parse_assignee(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        assignee = _parse_assignee(d.pop("assignee", UNSET))

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        resource = d.pop("resource", UNSET)

        def _parse_offering(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offering_type_0 = UUID(data)

                return offering_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        offering = _parse_offering(d.pop("offering", UNSET))

        def _parse_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        template = _parse_template(d.pop("template", UNSET))

        _processing_log = d.pop("processing_log", UNSET)
        processing_log: Union[Unset, IssueProcessingLog]
        if isinstance(_processing_log, Unset):
            processing_log = UNSET
        else:
            processing_log = IssueProcessingLog.from_dict(_processing_log)

        issue = cls(
            url=url,
            uuid=uuid,
            type_=type_,
            key=key,
            backend_id=backend_id,
            backend_name=backend_name,
            summary=summary,
            status=status,
            resolution=resolution,
            caller_uuid=caller_uuid,
            caller_full_name=caller_full_name,
            reporter=reporter,
            reporter_uuid=reporter_uuid,
            reporter_name=reporter_name,
            assignee_uuid=assignee_uuid,
            assignee_name=assignee_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            project_uuid=project_uuid,
            project_name=project_name,
            resource_type=resource_type,
            resource_name=resource_name,
            created=created,
            modified=modified,
            feedback=feedback,
            resolved=resolved,
            update_is_available=update_is_available,
            destroy_is_available=destroy_is_available,
            available_statuses=available_statuses,
            add_comment_is_available=add_comment_is_available,
            add_attachment_is_available=add_attachment_is_available,
            order_uuid=order_uuid,
            order_project_uuid=order_project_uuid,
            order_customer_uuid=order_customer_uuid,
            order_resource_name=order_resource_name,
            first_response_deadline=first_response_deadline,
            resolution_deadline=resolution_deadline,
            first_response_at=first_response_at,
            sla_breached=sla_breached,
            sla_status=sla_status,
            parent_issue=parent_issue,
            provider_helpdesk=provider_helpdesk,
            is_escalated=is_escalated,
            escalated_at=escalated_at,
            escalation_reason=escalation_reason,
            is_routed=is_routed,
            provider_ticket_info=provider_ticket_info,
            remote_id=remote_id,
            link=link,
            description=description,
            priority=priority,
            caller=caller,
            assignee=assignee,
            customer=customer,
            project=project,
            resource=resource,
            offering=offering,
            template=template,
            processing_log=processing_log,
        )

        issue.additional_properties = d
        return issue

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

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.membership_control_enum import MembershipControlEnum
from ..models.remote_project_state_enum import RemoteProjectStateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_details import AwardDetails
    from ..models.link import Link
    from ..models.note import Note
    from ..models.remote_project_breakdown import RemoteProjectBreakdown


T = TypeVar("T", bound="RemoteProject")


@_attrs_define
class RemoteProject:
    """
    Attributes:
        uuid (UUID):
        destination (str): Routing path from the local portal to the remote resource, e.g. 'airr.brics.isambard-ai'.
            Never changes after creation.
        resource_uuid (Union[None, UUID]):
        resource_name (Union[None, str]):
        state_display (str):
        allocation_string (Union[None, str]):
        link_award (Union['Link', None]):
        link_call (Union['Link', None]):
        link_project (Union['Link', None]):
        link_renewal (Union['Link', None]):
        allowed_domains (Union[None, list[str]]):
        breakdown (RemoteProjectBreakdown):
        last_sent_details (Union['AwardDetails', None]):
        last_confirmed_details (Union['AwardDetails', None]):
        pending_details (Union['AwardDetails', None]):
        award_details (Union['AwardDetails', None]):
        notes (Union[None, list['Note']]):
        earliest_approve (datetime.datetime):
        has_pending_change (bool):
        current_project_name (str):
        current_project_uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        identifier (Union[None, Unset, str]): Stable remote project identifier, e.g. 'u6ac.brics'.  Uniquely identifies
            the project on the remote portal and never changes.  Null while the project is pending first approval.
        state (Union[Unset, RemoteProjectStateEnum]):
        current_allocation (Union[Unset, str]): Latest confirmed allocation (credits) for this project.  Updated
            whenever a RemoteProjectAllocationEntry is confirmed.
        pending_allocation (Union[None, Unset, str]): Allocation value currently under review on the remote portal.
            Null when no allocation change is pending.
        membership_control (Union[BlankEnum, MembershipControlEnum, None, Unset]): Policy controlling whether the remote
            portal may independently modify project membership or roles.
        pending_since (Union[None, Unset, datetime.datetime]): When the currently pending change was submitted.
        error_message (Union[Unset, str]): The most recent rejection or error message received from the remote portal.
            Cleared when the state transitions to ACTIVE.
        last_contact_time (Union[None, Unset, datetime.datetime]): The most recent time the remote portal acknowledged
            anything about this project (confirmation, usage report, get_award response, etc.).  Used to detect connectivity
            issues and to trigger a transition to the STALE state.
    """

    uuid: UUID
    destination: str
    resource_uuid: Union[None, UUID]
    resource_name: Union[None, str]
    state_display: str
    allocation_string: Union[None, str]
    link_award: Union["Link", None]
    link_call: Union["Link", None]
    link_project: Union["Link", None]
    link_renewal: Union["Link", None]
    allowed_domains: Union[None, list[str]]
    breakdown: "RemoteProjectBreakdown"
    last_sent_details: Union["AwardDetails", None]
    last_confirmed_details: Union["AwardDetails", None]
    pending_details: Union["AwardDetails", None]
    award_details: Union["AwardDetails", None]
    notes: Union[None, list["Note"]]
    earliest_approve: datetime.datetime
    has_pending_change: bool
    current_project_name: str
    current_project_uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    identifier: Union[None, Unset, str] = UNSET
    state: Union[Unset, RemoteProjectStateEnum] = UNSET
    current_allocation: Union[Unset, str] = UNSET
    pending_allocation: Union[None, Unset, str] = UNSET
    membership_control: Union[BlankEnum, MembershipControlEnum, None, Unset] = UNSET
    pending_since: Union[None, Unset, datetime.datetime] = UNSET
    error_message: Union[Unset, str] = UNSET
    last_contact_time: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_details import AwardDetails
        from ..models.link import Link

        uuid = str(self.uuid)

        destination = self.destination

        resource_uuid: Union[None, str]
        if isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        resource_name: Union[None, str]
        resource_name = self.resource_name

        state_display = self.state_display

        allocation_string: Union[None, str]
        allocation_string = self.allocation_string

        link_award: Union[None, dict[str, Any]]
        if isinstance(self.link_award, Link):
            link_award = self.link_award.to_dict()
        else:
            link_award = self.link_award

        link_call: Union[None, dict[str, Any]]
        if isinstance(self.link_call, Link):
            link_call = self.link_call.to_dict()
        else:
            link_call = self.link_call

        link_project: Union[None, dict[str, Any]]
        if isinstance(self.link_project, Link):
            link_project = self.link_project.to_dict()
        else:
            link_project = self.link_project

        link_renewal: Union[None, dict[str, Any]]
        if isinstance(self.link_renewal, Link):
            link_renewal = self.link_renewal.to_dict()
        else:
            link_renewal = self.link_renewal

        allowed_domains: Union[None, list[str]]
        if isinstance(self.allowed_domains, list):
            allowed_domains = self.allowed_domains

        else:
            allowed_domains = self.allowed_domains

        breakdown = self.breakdown.to_dict()

        last_sent_details: Union[None, dict[str, Any]]
        if isinstance(self.last_sent_details, AwardDetails):
            last_sent_details = self.last_sent_details.to_dict()
        else:
            last_sent_details = self.last_sent_details

        last_confirmed_details: Union[None, dict[str, Any]]
        if isinstance(self.last_confirmed_details, AwardDetails):
            last_confirmed_details = self.last_confirmed_details.to_dict()
        else:
            last_confirmed_details = self.last_confirmed_details

        pending_details: Union[None, dict[str, Any]]
        if isinstance(self.pending_details, AwardDetails):
            pending_details = self.pending_details.to_dict()
        else:
            pending_details = self.pending_details

        award_details: Union[None, dict[str, Any]]
        if isinstance(self.award_details, AwardDetails):
            award_details = self.award_details.to_dict()
        else:
            award_details = self.award_details

        notes: Union[None, list[dict[str, Any]]]
        if isinstance(self.notes, list):
            notes = []
            for notes_type_0_item_data in self.notes:
                notes_type_0_item = notes_type_0_item_data.to_dict()
                notes.append(notes_type_0_item)

        else:
            notes = self.notes

        earliest_approve = self.earliest_approve.isoformat()

        has_pending_change = self.has_pending_change

        current_project_name = self.current_project_name

        current_project_uuid = str(self.current_project_uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        identifier: Union[None, Unset, str]
        if isinstance(self.identifier, Unset):
            identifier = UNSET
        else:
            identifier = self.identifier

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        current_allocation = self.current_allocation

        pending_allocation: Union[None, Unset, str]
        if isinstance(self.pending_allocation, Unset):
            pending_allocation = UNSET
        else:
            pending_allocation = self.pending_allocation

        membership_control: Union[None, Unset, str]
        if isinstance(self.membership_control, Unset):
            membership_control = UNSET
        elif isinstance(self.membership_control, MembershipControlEnum):
            membership_control = self.membership_control.value
        elif isinstance(self.membership_control, BlankEnum):
            membership_control = self.membership_control.value
        else:
            membership_control = self.membership_control

        pending_since: Union[None, Unset, str]
        if isinstance(self.pending_since, Unset):
            pending_since = UNSET
        elif isinstance(self.pending_since, datetime.datetime):
            pending_since = self.pending_since.isoformat()
        else:
            pending_since = self.pending_since

        error_message = self.error_message

        last_contact_time: Union[None, Unset, str]
        if isinstance(self.last_contact_time, Unset):
            last_contact_time = UNSET
        elif isinstance(self.last_contact_time, datetime.datetime):
            last_contact_time = self.last_contact_time.isoformat()
        else:
            last_contact_time = self.last_contact_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "destination": destination,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "state_display": state_display,
                "allocation_string": allocation_string,
                "link_award": link_award,
                "link_call": link_call,
                "link_project": link_project,
                "link_renewal": link_renewal,
                "allowed_domains": allowed_domains,
                "breakdown": breakdown,
                "last_sent_details": last_sent_details,
                "last_confirmed_details": last_confirmed_details,
                "pending_details": pending_details,
                "award_details": award_details,
                "notes": notes,
                "earliest_approve": earliest_approve,
                "has_pending_change": has_pending_change,
                "current_project_name": current_project_name,
                "current_project_uuid": current_project_uuid,
                "created": created,
                "modified": modified,
            }
        )
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if state is not UNSET:
            field_dict["state"] = state
        if current_allocation is not UNSET:
            field_dict["current_allocation"] = current_allocation
        if pending_allocation is not UNSET:
            field_dict["pending_allocation"] = pending_allocation
        if membership_control is not UNSET:
            field_dict["membership_control"] = membership_control
        if pending_since is not UNSET:
            field_dict["pending_since"] = pending_since
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if last_contact_time is not UNSET:
            field_dict["last_contact_time"] = last_contact_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_details import AwardDetails
        from ..models.link import Link
        from ..models.note import Note
        from ..models.remote_project_breakdown import RemoteProjectBreakdown

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        destination = d.pop("destination")

        def _parse_resource_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid"))

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        state_display = d.pop("state_display")

        def _parse_allocation_string(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        allocation_string = _parse_allocation_string(d.pop("allocation_string"))

        def _parse_link_award(data: object) -> Union["Link", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                link_award_type_1 = Link.from_dict(data)

                return link_award_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Link", None], data)

        link_award = _parse_link_award(d.pop("link_award"))

        def _parse_link_call(data: object) -> Union["Link", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                link_call_type_1 = Link.from_dict(data)

                return link_call_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Link", None], data)

        link_call = _parse_link_call(d.pop("link_call"))

        def _parse_link_project(data: object) -> Union["Link", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                link_project_type_1 = Link.from_dict(data)

                return link_project_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Link", None], data)

        link_project = _parse_link_project(d.pop("link_project"))

        def _parse_link_renewal(data: object) -> Union["Link", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                link_renewal_type_1 = Link.from_dict(data)

                return link_renewal_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Link", None], data)

        link_renewal = _parse_link_renewal(d.pop("link_renewal"))

        def _parse_allowed_domains(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0 = cast(list[str], data)

                return allowed_domains_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        allowed_domains = _parse_allowed_domains(d.pop("allowed_domains"))

        breakdown = RemoteProjectBreakdown.from_dict(d.pop("breakdown"))

        def _parse_last_sent_details(data: object) -> Union["AwardDetails", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_sent_details_type_1 = AwardDetails.from_dict(data)

                return last_sent_details_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetails", None], data)

        last_sent_details = _parse_last_sent_details(d.pop("last_sent_details"))

        def _parse_last_confirmed_details(data: object) -> Union["AwardDetails", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_confirmed_details_type_1 = AwardDetails.from_dict(data)

                return last_confirmed_details_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetails", None], data)

        last_confirmed_details = _parse_last_confirmed_details(d.pop("last_confirmed_details"))

        def _parse_pending_details(data: object) -> Union["AwardDetails", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pending_details_type_1 = AwardDetails.from_dict(data)

                return pending_details_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetails", None], data)

        pending_details = _parse_pending_details(d.pop("pending_details"))

        def _parse_award_details(data: object) -> Union["AwardDetails", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                award_details_type_1 = AwardDetails.from_dict(data)

                return award_details_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetails", None], data)

        award_details = _parse_award_details(d.pop("award_details"))

        def _parse_notes(data: object) -> Union[None, list["Note"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                notes_type_0 = []
                _notes_type_0 = data
                for notes_type_0_item_data in _notes_type_0:
                    notes_type_0_item = Note.from_dict(notes_type_0_item_data)

                    notes_type_0.append(notes_type_0_item)

                return notes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["Note"]], data)

        notes = _parse_notes(d.pop("notes"))

        earliest_approve = isoparse(d.pop("earliest_approve"))

        has_pending_change = d.pop("has_pending_change")

        current_project_name = d.pop("current_project_name")

        current_project_uuid = UUID(d.pop("current_project_uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_identifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        identifier = _parse_identifier(d.pop("identifier", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, RemoteProjectStateEnum]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = RemoteProjectStateEnum(_state)

        current_allocation = d.pop("current_allocation", UNSET)

        def _parse_pending_allocation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pending_allocation = _parse_pending_allocation(d.pop("pending_allocation", UNSET))

        def _parse_membership_control(data: object) -> Union[BlankEnum, MembershipControlEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                membership_control_type_0 = MembershipControlEnum(data)

                return membership_control_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                membership_control_type_1 = BlankEnum(data)

                return membership_control_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, MembershipControlEnum, None, Unset], data)

        membership_control = _parse_membership_control(d.pop("membership_control", UNSET))

        def _parse_pending_since(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pending_since_type_0 = isoparse(data)

                return pending_since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        pending_since = _parse_pending_since(d.pop("pending_since", UNSET))

        error_message = d.pop("error_message", UNSET)

        def _parse_last_contact_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_contact_time_type_0 = isoparse(data)

                return last_contact_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_contact_time = _parse_last_contact_time(d.pop("last_contact_time", UNSET))

        remote_project = cls(
            uuid=uuid,
            destination=destination,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            state_display=state_display,
            allocation_string=allocation_string,
            link_award=link_award,
            link_call=link_call,
            link_project=link_project,
            link_renewal=link_renewal,
            allowed_domains=allowed_domains,
            breakdown=breakdown,
            last_sent_details=last_sent_details,
            last_confirmed_details=last_confirmed_details,
            pending_details=pending_details,
            award_details=award_details,
            notes=notes,
            earliest_approve=earliest_approve,
            has_pending_change=has_pending_change,
            current_project_name=current_project_name,
            current_project_uuid=current_project_uuid,
            created=created,
            modified=modified,
            identifier=identifier,
            state=state,
            current_allocation=current_allocation,
            pending_allocation=pending_allocation,
            membership_control=membership_control,
            pending_since=pending_since,
            error_message=error_message,
            last_contact_time=last_contact_time,
        )

        remote_project.additional_properties = d
        return remote_project

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

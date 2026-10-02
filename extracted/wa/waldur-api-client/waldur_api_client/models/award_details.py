import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.membership_control_enum import MembershipControlEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_details_breakdown import AwardDetailsBreakdown
    from ..models.award_details_members_type_0 import AwardDetailsMembersType0
    from ..models.link import Link
    from ..models.note import Note


T = TypeVar("T", bound="AwardDetails")


@_attrs_define
class AwardDetails:
    """
    Attributes:
        name (Union[None, str]): The name of the project
        template (Union[None, str]): The template used for the project
        key (Union[None, str]): Shared secret required to access a particular project template
        description (Union[None, str]): The description of the project
        members (Union['AwardDetailsMembersType0', None]): Email addresses of project members (keys) and their roles
            (values)
        start_date (Union[None, datetime.date]): Proposed start date of the project
        end_date (Union[None, datetime.date]): Proposed end date of the project
        allocation (Union[None, str]): The allocation of resource for this project (e.g. "1000 NHR")
        notes (list['Note']): Notes attached to this award (append-only log)
        allowed_domains (Union[None, list[str]]): Allowed email domain glob patterns. null means all domains are
            allowed; [] means none are.
        breakdown (Union[Unset, AwardDetailsBreakdown]): Free-form breakdown of the allocation into named components
        award (Union[Unset, Link]):
        call (Union[Unset, Link]):
        project_link (Union[Unset, Link]):
        renewal (Union[Unset, Link]):
        earliest_approve (Union[Unset, datetime.datetime]): Earliest UTC time at which this award may be approved
        membership_control (Union[Unset, MembershipControlEnum]):
    """

    name: Union[None, str]
    template: Union[None, str]
    key: Union[None, str]
    description: Union[None, str]
    members: Union["AwardDetailsMembersType0", None]
    start_date: Union[None, datetime.date]
    end_date: Union[None, datetime.date]
    allocation: Union[None, str]
    notes: list["Note"]
    allowed_domains: Union[None, list[str]]
    breakdown: Union[Unset, "AwardDetailsBreakdown"] = UNSET
    award: Union[Unset, "Link"] = UNSET
    call: Union[Unset, "Link"] = UNSET
    project_link: Union[Unset, "Link"] = UNSET
    renewal: Union[Unset, "Link"] = UNSET
    earliest_approve: Union[Unset, datetime.datetime] = UNSET
    membership_control: Union[Unset, MembershipControlEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_details_members_type_0 import AwardDetailsMembersType0

        name: Union[None, str]
        name = self.name

        template: Union[None, str]
        template = self.template

        key: Union[None, str]
        key = self.key

        description: Union[None, str]
        description = self.description

        members: Union[None, dict[str, Any]]
        if isinstance(self.members, AwardDetailsMembersType0):
            members = self.members.to_dict()
        else:
            members = self.members

        start_date: Union[None, str]
        if isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: Union[None, str]
        if isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        allocation: Union[None, str]
        allocation = self.allocation

        notes = []
        for notes_item_data in self.notes:
            notes_item = notes_item_data.to_dict()
            notes.append(notes_item)

        allowed_domains: Union[None, list[str]]
        if isinstance(self.allowed_domains, list):
            allowed_domains = self.allowed_domains

        else:
            allowed_domains = self.allowed_domains

        breakdown: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.breakdown, Unset):
            breakdown = self.breakdown.to_dict()

        award: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.award, Unset):
            award = self.award.to_dict()

        call: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.call, Unset):
            call = self.call.to_dict()

        project_link: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.project_link, Unset):
            project_link = self.project_link.to_dict()

        renewal: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.renewal, Unset):
            renewal = self.renewal.to_dict()

        earliest_approve: Union[Unset, str] = UNSET
        if not isinstance(self.earliest_approve, Unset):
            earliest_approve = self.earliest_approve.isoformat()

        membership_control: Union[Unset, str] = UNSET
        if not isinstance(self.membership_control, Unset):
            membership_control = self.membership_control.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "template": template,
                "key": key,
                "description": description,
                "members": members,
                "start_date": start_date,
                "end_date": end_date,
                "allocation": allocation,
                "notes": notes,
                "allowed_domains": allowed_domains,
            }
        )
        if breakdown is not UNSET:
            field_dict["breakdown"] = breakdown
        if award is not UNSET:
            field_dict["award"] = award
        if call is not UNSET:
            field_dict["call"] = call
        if project_link is not UNSET:
            field_dict["project_link"] = project_link
        if renewal is not UNSET:
            field_dict["renewal"] = renewal
        if earliest_approve is not UNSET:
            field_dict["earliest_approve"] = earliest_approve
        if membership_control is not UNSET:
            field_dict["membership_control"] = membership_control

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_details_breakdown import AwardDetailsBreakdown
        from ..models.award_details_members_type_0 import AwardDetailsMembersType0
        from ..models.link import Link
        from ..models.note import Note

        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_template(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        template = _parse_template(d.pop("template"))

        def _parse_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        key = _parse_key(d.pop("key"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        def _parse_members(data: object) -> Union["AwardDetailsMembersType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                members_type_0 = AwardDetailsMembersType0.from_dict(data)

                return members_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetailsMembersType0", None], data)

        members = _parse_members(d.pop("members"))

        def _parse_start_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date"))

        def _parse_end_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date"))

        def _parse_allocation(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        allocation = _parse_allocation(d.pop("allocation"))

        notes = []
        _notes = d.pop("notes")
        for notes_item_data in _notes:
            notes_item = Note.from_dict(notes_item_data)

            notes.append(notes_item)

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

        _breakdown = d.pop("breakdown", UNSET)
        breakdown: Union[Unset, AwardDetailsBreakdown]
        if isinstance(_breakdown, Unset):
            breakdown = UNSET
        else:
            breakdown = AwardDetailsBreakdown.from_dict(_breakdown)

        _award = d.pop("award", UNSET)
        award: Union[Unset, Link]
        if isinstance(_award, Unset):
            award = UNSET
        else:
            award = Link.from_dict(_award)

        _call = d.pop("call", UNSET)
        call: Union[Unset, Link]
        if isinstance(_call, Unset):
            call = UNSET
        else:
            call = Link.from_dict(_call)

        _project_link = d.pop("project_link", UNSET)
        project_link: Union[Unset, Link]
        if isinstance(_project_link, Unset):
            project_link = UNSET
        else:
            project_link = Link.from_dict(_project_link)

        _renewal = d.pop("renewal", UNSET)
        renewal: Union[Unset, Link]
        if isinstance(_renewal, Unset):
            renewal = UNSET
        else:
            renewal = Link.from_dict(_renewal)

        _earliest_approve = d.pop("earliest_approve", UNSET)
        earliest_approve: Union[Unset, datetime.datetime]
        if isinstance(_earliest_approve, Unset):
            earliest_approve = UNSET
        else:
            earliest_approve = isoparse(_earliest_approve)

        _membership_control = d.pop("membership_control", UNSET)
        membership_control: Union[Unset, MembershipControlEnum]
        if isinstance(_membership_control, Unset):
            membership_control = UNSET
        else:
            membership_control = MembershipControlEnum(_membership_control)

        award_details = cls(
            name=name,
            template=template,
            key=key,
            description=description,
            members=members,
            start_date=start_date,
            end_date=end_date,
            allocation=allocation,
            notes=notes,
            allowed_domains=allowed_domains,
            breakdown=breakdown,
            award=award,
            call=call,
            project_link=project_link,
            renewal=renewal,
            earliest_approve=earliest_approve,
            membership_control=membership_control,
        )

        award_details.additional_properties = d
        return award_details

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

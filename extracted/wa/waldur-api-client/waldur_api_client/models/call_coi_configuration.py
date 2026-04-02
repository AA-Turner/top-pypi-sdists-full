import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.invitation_proposal_disclosure_enum import InvitationProposalDisclosureEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CallCOIConfiguration")


@_attrs_define
class CallCOIConfiguration:
    """
    Attributes:
        uuid (UUID):
        call (str):
        call_uuid (UUID):
        call_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        coauthorship_lookback_years (Union[Unset, int]): Years to look back for co-authorship detection
        coauthorship_threshold_papers (Union[Unset, int]): Minimum shared papers to trigger COI
        institutional_lookback_years (Union[Unset, int]): Years to look back for former institution detection
        include_same_department (Union[Unset, bool]): Detect same-department as COI
        include_same_institution (Union[Unset, bool]): Detect same-institution as COI
        recusal_required_types (Union[Unset, list[str]]): COI types requiring automatic recusal
        management_allowed_types (Union[Unset, list[str]]): COI types allowing management plan
        disclosure_only_types (Union[Unset, list[str]]): COI types requiring disclosure only
        auto_detect_coauthorship (Union[Unset, bool]): Enable automated co-authorship detection
        auto_detect_institutional (Union[Unset, bool]): Enable automated institutional affiliation detection
        auto_detect_named_personnel (Union[Unset, bool]): Enable detection of reviewer named in proposals
        invitation_proposal_disclosure (Union[Unset, InvitationProposalDisclosureEnum]):
    """

    uuid: UUID
    call: str
    call_uuid: UUID
    call_name: str
    created: datetime.datetime
    modified: datetime.datetime
    coauthorship_lookback_years: Union[Unset, int] = UNSET
    coauthorship_threshold_papers: Union[Unset, int] = UNSET
    institutional_lookback_years: Union[Unset, int] = UNSET
    include_same_department: Union[Unset, bool] = UNSET
    include_same_institution: Union[Unset, bool] = UNSET
    recusal_required_types: Union[Unset, list[str]] = UNSET
    management_allowed_types: Union[Unset, list[str]] = UNSET
    disclosure_only_types: Union[Unset, list[str]] = UNSET
    auto_detect_coauthorship: Union[Unset, bool] = UNSET
    auto_detect_institutional: Union[Unset, bool] = UNSET
    auto_detect_named_personnel: Union[Unset, bool] = UNSET
    invitation_proposal_disclosure: Union[Unset, InvitationProposalDisclosureEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        call = self.call

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        coauthorship_lookback_years = self.coauthorship_lookback_years

        coauthorship_threshold_papers = self.coauthorship_threshold_papers

        institutional_lookback_years = self.institutional_lookback_years

        include_same_department = self.include_same_department

        include_same_institution = self.include_same_institution

        recusal_required_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.recusal_required_types, Unset):
            recusal_required_types = self.recusal_required_types

        management_allowed_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.management_allowed_types, Unset):
            management_allowed_types = self.management_allowed_types

        disclosure_only_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.disclosure_only_types, Unset):
            disclosure_only_types = self.disclosure_only_types

        auto_detect_coauthorship = self.auto_detect_coauthorship

        auto_detect_institutional = self.auto_detect_institutional

        auto_detect_named_personnel = self.auto_detect_named_personnel

        invitation_proposal_disclosure: Union[Unset, str] = UNSET
        if not isinstance(self.invitation_proposal_disclosure, Unset):
            invitation_proposal_disclosure = self.invitation_proposal_disclosure.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "call": call,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "created": created,
                "modified": modified,
            }
        )
        if coauthorship_lookback_years is not UNSET:
            field_dict["coauthorship_lookback_years"] = coauthorship_lookback_years
        if coauthorship_threshold_papers is not UNSET:
            field_dict["coauthorship_threshold_papers"] = coauthorship_threshold_papers
        if institutional_lookback_years is not UNSET:
            field_dict["institutional_lookback_years"] = institutional_lookback_years
        if include_same_department is not UNSET:
            field_dict["include_same_department"] = include_same_department
        if include_same_institution is not UNSET:
            field_dict["include_same_institution"] = include_same_institution
        if recusal_required_types is not UNSET:
            field_dict["recusal_required_types"] = recusal_required_types
        if management_allowed_types is not UNSET:
            field_dict["management_allowed_types"] = management_allowed_types
        if disclosure_only_types is not UNSET:
            field_dict["disclosure_only_types"] = disclosure_only_types
        if auto_detect_coauthorship is not UNSET:
            field_dict["auto_detect_coauthorship"] = auto_detect_coauthorship
        if auto_detect_institutional is not UNSET:
            field_dict["auto_detect_institutional"] = auto_detect_institutional
        if auto_detect_named_personnel is not UNSET:
            field_dict["auto_detect_named_personnel"] = auto_detect_named_personnel
        if invitation_proposal_disclosure is not UNSET:
            field_dict["invitation_proposal_disclosure"] = invitation_proposal_disclosure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        coauthorship_lookback_years = d.pop("coauthorship_lookback_years", UNSET)

        coauthorship_threshold_papers = d.pop("coauthorship_threshold_papers", UNSET)

        institutional_lookback_years = d.pop("institutional_lookback_years", UNSET)

        include_same_department = d.pop("include_same_department", UNSET)

        include_same_institution = d.pop("include_same_institution", UNSET)

        recusal_required_types = cast(list[str], d.pop("recusal_required_types", UNSET))

        management_allowed_types = cast(list[str], d.pop("management_allowed_types", UNSET))

        disclosure_only_types = cast(list[str], d.pop("disclosure_only_types", UNSET))

        auto_detect_coauthorship = d.pop("auto_detect_coauthorship", UNSET)

        auto_detect_institutional = d.pop("auto_detect_institutional", UNSET)

        auto_detect_named_personnel = d.pop("auto_detect_named_personnel", UNSET)

        _invitation_proposal_disclosure = d.pop("invitation_proposal_disclosure", UNSET)
        invitation_proposal_disclosure: Union[Unset, InvitationProposalDisclosureEnum]
        if isinstance(_invitation_proposal_disclosure, Unset):
            invitation_proposal_disclosure = UNSET
        else:
            invitation_proposal_disclosure = InvitationProposalDisclosureEnum(_invitation_proposal_disclosure)

        call_coi_configuration = cls(
            uuid=uuid,
            call=call,
            call_uuid=call_uuid,
            call_name=call_name,
            created=created,
            modified=modified,
            coauthorship_lookback_years=coauthorship_lookback_years,
            coauthorship_threshold_papers=coauthorship_threshold_papers,
            institutional_lookback_years=institutional_lookback_years,
            include_same_department=include_same_department,
            include_same_institution=include_same_institution,
            recusal_required_types=recusal_required_types,
            management_allowed_types=management_allowed_types,
            disclosure_only_types=disclosure_only_types,
            auto_detect_coauthorship=auto_detect_coauthorship,
            auto_detect_institutional=auto_detect_institutional,
            auto_detect_named_personnel=auto_detect_named_personnel,
            invitation_proposal_disclosure=invitation_proposal_disclosure,
        )

        call_coi_configuration.additional_properties = d
        return call_coi_configuration

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

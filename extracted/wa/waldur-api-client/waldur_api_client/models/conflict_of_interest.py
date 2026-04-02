import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.coi_severity_level import COISeverityLevel
from ..models.coi_type_enum import CoiTypeEnum
from ..models.conflict_of_interest_status_enum import ConflictOfInterestStatusEnum
from ..models.detection_method_enum import DetectionMethodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConflictOfInterest")


@_attrs_define
class ConflictOfInterest:
    """
    Attributes:
        url (str):
        uuid (UUID):
        reviewer (str):
        reviewer_uuid (UUID):
        reviewer_name (str):
        proposal (Union[None, str]):
        proposal_uuid (UUID):
        proposal_name (str):
        round_uuid (UUID):
        round_name (str):
        call (str):
        call_uuid (UUID):
        call_name (str):
        coi_type (CoiTypeEnum):
        coi_type_display (str):
        severity (COISeverityLevel):
        severity_display (str):
        detection_method (DetectionMethodEnum):
        detected_at (datetime.datetime):
        evidence_description (str):
        evidence_data (Any): Structured evidence: {"papers": [...], "affiliation_overlap": {...}}
        status_display (str):
        reviewed_by (Union[None, str]):
        reviewed_by_name (str):
        reviewed_at (Union[None, datetime.datetime]):
        conflicting_user (Union[None, str]): Specific person causing conflict
        conflicting_user_name (str):
        conflicting_organization (Union[None, str]):
        conflicting_organization_name (str):
        created (datetime.datetime):
        status (Union[Unset, ConflictOfInterestStatusEnum]):
        review_notes (Union[Unset, str]):
        management_plan (Union[Unset, str]): If waived, how is it managed
    """

    url: str
    uuid: UUID
    reviewer: str
    reviewer_uuid: UUID
    reviewer_name: str
    proposal: Union[None, str]
    proposal_uuid: UUID
    proposal_name: str
    round_uuid: UUID
    round_name: str
    call: str
    call_uuid: UUID
    call_name: str
    coi_type: CoiTypeEnum
    coi_type_display: str
    severity: COISeverityLevel
    severity_display: str
    detection_method: DetectionMethodEnum
    detected_at: datetime.datetime
    evidence_description: str
    evidence_data: Any
    status_display: str
    reviewed_by: Union[None, str]
    reviewed_by_name: str
    reviewed_at: Union[None, datetime.datetime]
    conflicting_user: Union[None, str]
    conflicting_user_name: str
    conflicting_organization: Union[None, str]
    conflicting_organization_name: str
    created: datetime.datetime
    status: Union[Unset, ConflictOfInterestStatusEnum] = UNSET
    review_notes: Union[Unset, str] = UNSET
    management_plan: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        reviewer = self.reviewer

        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        proposal: Union[None, str]
        proposal = self.proposal

        proposal_uuid = str(self.proposal_uuid)

        proposal_name = self.proposal_name

        round_uuid = str(self.round_uuid)

        round_name = self.round_name

        call = self.call

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        coi_type = self.coi_type.value

        coi_type_display = self.coi_type_display

        severity = self.severity.value

        severity_display = self.severity_display

        detection_method = self.detection_method.value

        detected_at = self.detected_at.isoformat()

        evidence_description = self.evidence_description

        evidence_data = self.evidence_data

        status_display = self.status_display

        reviewed_by: Union[None, str]
        reviewed_by = self.reviewed_by

        reviewed_by_name = self.reviewed_by_name

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        conflicting_user: Union[None, str]
        conflicting_user = self.conflicting_user

        conflicting_user_name = self.conflicting_user_name

        conflicting_organization: Union[None, str]
        conflicting_organization = self.conflicting_organization

        conflicting_organization_name = self.conflicting_organization_name

        created = self.created.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        review_notes = self.review_notes

        management_plan = self.management_plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "reviewer": reviewer,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "proposal": proposal,
                "proposal_uuid": proposal_uuid,
                "proposal_name": proposal_name,
                "round_uuid": round_uuid,
                "round_name": round_name,
                "call": call,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "coi_type": coi_type,
                "coi_type_display": coi_type_display,
                "severity": severity,
                "severity_display": severity_display,
                "detection_method": detection_method,
                "detected_at": detected_at,
                "evidence_description": evidence_description,
                "evidence_data": evidence_data,
                "status_display": status_display,
                "reviewed_by": reviewed_by,
                "reviewed_by_name": reviewed_by_name,
                "reviewed_at": reviewed_at,
                "conflicting_user": conflicting_user,
                "conflicting_user_name": conflicting_user_name,
                "conflicting_organization": conflicting_organization,
                "conflicting_organization_name": conflicting_organization_name,
                "created": created,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if review_notes is not UNSET:
            field_dict["review_notes"] = review_notes
        if management_plan is not UNSET:
            field_dict["management_plan"] = management_plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        reviewer = d.pop("reviewer")

        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        def _parse_proposal(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        proposal = _parse_proposal(d.pop("proposal"))

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_name = d.pop("proposal_name")

        round_uuid = UUID(d.pop("round_uuid"))

        round_name = d.pop("round_name")

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        coi_type = CoiTypeEnum(d.pop("coi_type"))

        coi_type_display = d.pop("coi_type_display")

        severity = COISeverityLevel(d.pop("severity"))

        severity_display = d.pop("severity_display")

        detection_method = DetectionMethodEnum(d.pop("detection_method"))

        detected_at = isoparse(d.pop("detected_at"))

        evidence_description = d.pop("evidence_description")

        evidence_data = d.pop("evidence_data")

        status_display = d.pop("status_display")

        def _parse_reviewed_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by"))

        reviewed_by_name = d.pop("reviewed_by_name")

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        def _parse_conflicting_user(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        conflicting_user = _parse_conflicting_user(d.pop("conflicting_user"))

        conflicting_user_name = d.pop("conflicting_user_name")

        def _parse_conflicting_organization(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        conflicting_organization = _parse_conflicting_organization(d.pop("conflicting_organization"))

        conflicting_organization_name = d.pop("conflicting_organization_name")

        created = isoparse(d.pop("created"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, ConflictOfInterestStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ConflictOfInterestStatusEnum(_status)

        review_notes = d.pop("review_notes", UNSET)

        management_plan = d.pop("management_plan", UNSET)

        conflict_of_interest = cls(
            url=url,
            uuid=uuid,
            reviewer=reviewer,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            proposal=proposal,
            proposal_uuid=proposal_uuid,
            proposal_name=proposal_name,
            round_uuid=round_uuid,
            round_name=round_name,
            call=call,
            call_uuid=call_uuid,
            call_name=call_name,
            coi_type=coi_type,
            coi_type_display=coi_type_display,
            severity=severity,
            severity_display=severity_display,
            detection_method=detection_method,
            detected_at=detected_at,
            evidence_description=evidence_description,
            evidence_data=evidence_data,
            status_display=status_display,
            reviewed_by=reviewed_by,
            reviewed_by_name=reviewed_by_name,
            reviewed_at=reviewed_at,
            conflicting_user=conflicting_user,
            conflicting_user_name=conflicting_user_name,
            conflicting_organization=conflicting_organization,
            conflicting_organization_name=conflicting_organization_name,
            created=created,
            status=status,
            review_notes=review_notes,
            management_plan=management_plan,
        )

        conflict_of_interest.additional_properties = d
        return conflict_of_interest

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

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.assignment_item_status import AssignmentItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssignmentItem")


@_attrs_define
class AssignmentItem:
    """
    Attributes:
        url (str):
        uuid (UUID):
        batch (str):
        proposal (str):
        proposal_uuid (UUID):
        proposal_name (str):
        proposal_slug (str):
        status (AssignmentItemStatus):
        status_display (str):
        affinity_score (Union[None, float]): Affinity score used for assignment (0-1).
        has_coi (bool): Whether COI was detected during pre-check.
        coi_count (int): Count of COI records blocking this assignment.
        responded_at (Union[None, datetime.datetime]):
        review (Union[None, str]): The Review record created when this assignment was accepted.
        review_uuid (UUID):
        reassign_count (int): Number of times this proposal has been reassigned.
        created (datetime.datetime):
        decline_reason (Union[Unset, str]): Reason provided by reviewer for declining.
    """

    url: str
    uuid: UUID
    batch: str
    proposal: str
    proposal_uuid: UUID
    proposal_name: str
    proposal_slug: str
    status: AssignmentItemStatus
    status_display: str
    affinity_score: Union[None, float]
    has_coi: bool
    coi_count: int
    responded_at: Union[None, datetime.datetime]
    review: Union[None, str]
    review_uuid: UUID
    reassign_count: int
    created: datetime.datetime
    decline_reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        batch = self.batch

        proposal = self.proposal

        proposal_uuid = str(self.proposal_uuid)

        proposal_name = self.proposal_name

        proposal_slug = self.proposal_slug

        status = self.status.value

        status_display = self.status_display

        affinity_score: Union[None, float]
        affinity_score = self.affinity_score

        has_coi = self.has_coi

        coi_count = self.coi_count

        responded_at: Union[None, str]
        if isinstance(self.responded_at, datetime.datetime):
            responded_at = self.responded_at.isoformat()
        else:
            responded_at = self.responded_at

        review: Union[None, str]
        review = self.review

        review_uuid = str(self.review_uuid)

        reassign_count = self.reassign_count

        created = self.created.isoformat()

        decline_reason = self.decline_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "batch": batch,
                "proposal": proposal,
                "proposal_uuid": proposal_uuid,
                "proposal_name": proposal_name,
                "proposal_slug": proposal_slug,
                "status": status,
                "status_display": status_display,
                "affinity_score": affinity_score,
                "has_coi": has_coi,
                "coi_count": coi_count,
                "responded_at": responded_at,
                "review": review,
                "review_uuid": review_uuid,
                "reassign_count": reassign_count,
                "created": created,
            }
        )
        if decline_reason is not UNSET:
            field_dict["decline_reason"] = decline_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        batch = d.pop("batch")

        proposal = d.pop("proposal")

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_name = d.pop("proposal_name")

        proposal_slug = d.pop("proposal_slug")

        status = AssignmentItemStatus(d.pop("status"))

        status_display = d.pop("status_display")

        def _parse_affinity_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        affinity_score = _parse_affinity_score(d.pop("affinity_score"))

        has_coi = d.pop("has_coi")

        coi_count = d.pop("coi_count")

        def _parse_responded_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                responded_at_type_0 = isoparse(data)

                return responded_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        responded_at = _parse_responded_at(d.pop("responded_at"))

        def _parse_review(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        review = _parse_review(d.pop("review"))

        review_uuid = UUID(d.pop("review_uuid"))

        reassign_count = d.pop("reassign_count")

        created = isoparse(d.pop("created"))

        decline_reason = d.pop("decline_reason", UNSET)

        assignment_item = cls(
            url=url,
            uuid=uuid,
            batch=batch,
            proposal=proposal,
            proposal_uuid=proposal_uuid,
            proposal_name=proposal_name,
            proposal_slug=proposal_slug,
            status=status,
            status_display=status_display,
            affinity_score=affinity_score,
            has_coi=has_coi,
            coi_count=coi_count,
            responded_at=responded_at,
            review=review,
            review_uuid=review_uuid,
            reassign_count=reassign_count,
            created=created,
            decline_reason=decline_reason,
        )

        assignment_item.additional_properties = d
        return assignment_item

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

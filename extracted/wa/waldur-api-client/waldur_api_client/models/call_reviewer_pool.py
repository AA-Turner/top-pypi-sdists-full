import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.invitation_status_enum import InvitationStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_reviewer_pool_coi_by_severity import CallReviewerPoolCoiBySeverity


T = TypeVar("T", bound="CallReviewerPool")


@_attrs_define
class CallReviewerPool:
    """
    Attributes:
        url (str):
        uuid (UUID):
        call (str):
        call_uuid (UUID):
        call_name (str):
        reviewer (Union[None, str]):
        reviewer_uuid (Union[None, str]): Get reviewer profile UUID if available.
        reviewer_name (Union[None, str]): Get reviewer name from profile or invited_user.
        reviewer_email (Union[None, str]): Get email from profile, invited_user, or invited_email.
        has_profile (bool): Check if reviewer has a profile.
        invited_email (str): Email address for direct invitations
        invited_user (Union[None, str]): Waldur user if email matches existing account
        invited_user_name (str):
        invited_at (datetime.datetime):
        invitation_status (InvitationStatusEnum):
        invitation_status_display (str):
        response_date (Union[None, datetime.datetime]):
        decline_reason (str):
        current_assignments (int):
        invited_by_name (str):
        invitation_token (str):
        invitation_expires_at (Union[None, datetime.datetime]):
        created (datetime.datetime):
        coi_count (int): Count total COIs for this reviewer in this call.
        coi_by_severity (CallReviewerPoolCoiBySeverity): Count COIs by severity level.
        reviews_pending (int): Legacy field - always returns 0.

            Previously counted reviews in 'created' state, but that state
            has been removed. Reviews are now created directly in 'in_review' state.
            Kept for backwards compatibility with frontend.
        reviews_in_progress (int): Count reviews in 'in_review' state.
        reviews_completed (int): Count reviews in 'submitted' state.
        max_assignments (Union[Unset, int]):
        expertise_match_score (Union[None, Unset, float]): Calculated affinity to call topics (0-1)
    """

    url: str
    uuid: UUID
    call: str
    call_uuid: UUID
    call_name: str
    reviewer: Union[None, str]
    reviewer_uuid: Union[None, str]
    reviewer_name: Union[None, str]
    reviewer_email: Union[None, str]
    has_profile: bool
    invited_email: str
    invited_user: Union[None, str]
    invited_user_name: str
    invited_at: datetime.datetime
    invitation_status: InvitationStatusEnum
    invitation_status_display: str
    response_date: Union[None, datetime.datetime]
    decline_reason: str
    current_assignments: int
    invited_by_name: str
    invitation_token: str
    invitation_expires_at: Union[None, datetime.datetime]
    created: datetime.datetime
    coi_count: int
    coi_by_severity: "CallReviewerPoolCoiBySeverity"
    reviews_pending: int
    reviews_in_progress: int
    reviews_completed: int
    max_assignments: Union[Unset, int] = UNSET
    expertise_match_score: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        call = self.call

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        reviewer: Union[None, str]
        reviewer = self.reviewer

        reviewer_uuid: Union[None, str]
        reviewer_uuid = self.reviewer_uuid

        reviewer_name: Union[None, str]
        reviewer_name = self.reviewer_name

        reviewer_email: Union[None, str]
        reviewer_email = self.reviewer_email

        has_profile = self.has_profile

        invited_email = self.invited_email

        invited_user: Union[None, str]
        invited_user = self.invited_user

        invited_user_name = self.invited_user_name

        invited_at = self.invited_at.isoformat()

        invitation_status = self.invitation_status.value

        invitation_status_display = self.invitation_status_display

        response_date: Union[None, str]
        if isinstance(self.response_date, datetime.datetime):
            response_date = self.response_date.isoformat()
        else:
            response_date = self.response_date

        decline_reason = self.decline_reason

        current_assignments = self.current_assignments

        invited_by_name = self.invited_by_name

        invitation_token = self.invitation_token

        invitation_expires_at: Union[None, str]
        if isinstance(self.invitation_expires_at, datetime.datetime):
            invitation_expires_at = self.invitation_expires_at.isoformat()
        else:
            invitation_expires_at = self.invitation_expires_at

        created = self.created.isoformat()

        coi_count = self.coi_count

        coi_by_severity = self.coi_by_severity.to_dict()

        reviews_pending = self.reviews_pending

        reviews_in_progress = self.reviews_in_progress

        reviews_completed = self.reviews_completed

        max_assignments = self.max_assignments

        expertise_match_score: Union[None, Unset, float]
        if isinstance(self.expertise_match_score, Unset):
            expertise_match_score = UNSET
        else:
            expertise_match_score = self.expertise_match_score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "call": call,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "reviewer": reviewer,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "reviewer_email": reviewer_email,
                "has_profile": has_profile,
                "invited_email": invited_email,
                "invited_user": invited_user,
                "invited_user_name": invited_user_name,
                "invited_at": invited_at,
                "invitation_status": invitation_status,
                "invitation_status_display": invitation_status_display,
                "response_date": response_date,
                "decline_reason": decline_reason,
                "current_assignments": current_assignments,
                "invited_by_name": invited_by_name,
                "invitation_token": invitation_token,
                "invitation_expires_at": invitation_expires_at,
                "created": created,
                "coi_count": coi_count,
                "coi_by_severity": coi_by_severity,
                "reviews_pending": reviews_pending,
                "reviews_in_progress": reviews_in_progress,
                "reviews_completed": reviews_completed,
            }
        )
        if max_assignments is not UNSET:
            field_dict["max_assignments"] = max_assignments
        if expertise_match_score is not UNSET:
            field_dict["expertise_match_score"] = expertise_match_score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_reviewer_pool_coi_by_severity import CallReviewerPoolCoiBySeverity

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        def _parse_reviewer(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer = _parse_reviewer(d.pop("reviewer"))

        def _parse_reviewer_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_uuid = _parse_reviewer_uuid(d.pop("reviewer_uuid"))

        def _parse_reviewer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_name = _parse_reviewer_name(d.pop("reviewer_name"))

        def _parse_reviewer_email(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_email = _parse_reviewer_email(d.pop("reviewer_email"))

        has_profile = d.pop("has_profile")

        invited_email = d.pop("invited_email")

        def _parse_invited_user(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        invited_user = _parse_invited_user(d.pop("invited_user"))

        invited_user_name = d.pop("invited_user_name")

        invited_at = isoparse(d.pop("invited_at"))

        invitation_status = InvitationStatusEnum(d.pop("invitation_status"))

        invitation_status_display = d.pop("invitation_status_display")

        def _parse_response_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                response_date_type_0 = isoparse(data)

                return response_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        response_date = _parse_response_date(d.pop("response_date"))

        decline_reason = d.pop("decline_reason")

        current_assignments = d.pop("current_assignments")

        invited_by_name = d.pop("invited_by_name")

        invitation_token = d.pop("invitation_token")

        def _parse_invitation_expires_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                invitation_expires_at_type_0 = isoparse(data)

                return invitation_expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        invitation_expires_at = _parse_invitation_expires_at(d.pop("invitation_expires_at"))

        created = isoparse(d.pop("created"))

        coi_count = d.pop("coi_count")

        coi_by_severity = CallReviewerPoolCoiBySeverity.from_dict(d.pop("coi_by_severity"))

        reviews_pending = d.pop("reviews_pending")

        reviews_in_progress = d.pop("reviews_in_progress")

        reviews_completed = d.pop("reviews_completed")

        max_assignments = d.pop("max_assignments", UNSET)

        def _parse_expertise_match_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        expertise_match_score = _parse_expertise_match_score(d.pop("expertise_match_score", UNSET))

        call_reviewer_pool = cls(
            url=url,
            uuid=uuid,
            call=call,
            call_uuid=call_uuid,
            call_name=call_name,
            reviewer=reviewer,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            reviewer_email=reviewer_email,
            has_profile=has_profile,
            invited_email=invited_email,
            invited_user=invited_user,
            invited_user_name=invited_user_name,
            invited_at=invited_at,
            invitation_status=invitation_status,
            invitation_status_display=invitation_status_display,
            response_date=response_date,
            decline_reason=decline_reason,
            current_assignments=current_assignments,
            invited_by_name=invited_by_name,
            invitation_token=invitation_token,
            invitation_expires_at=invitation_expires_at,
            created=created,
            coi_count=coi_count,
            coi_by_severity=coi_by_severity,
            reviews_pending=reviews_pending,
            reviews_in_progress=reviews_in_progress,
            reviews_completed=reviews_completed,
            max_assignments=max_assignments,
            expertise_match_score=expertise_match_score,
        )

        call_reviewer_pool.additional_properties = d
        return call_reviewer_pool

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

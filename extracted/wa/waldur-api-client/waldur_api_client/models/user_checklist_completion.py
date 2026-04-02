import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.offering_user import OfferingUser


T = TypeVar("T", bound="UserChecklistCompletion")


@_attrs_define
class UserChecklistCompletion:
    """
    Attributes:
        uuid (UUID):
        offering_user (OfferingUser):
        offering_user_uuid (Union[None, str]):
        offering_name (Union[None, str]):
        offering_uuid (Union[None, str]):
        customer_provider_uuid (Union[None, str]):
        customer_provider_name (Union[None, str]):
        checklist_uuid (str):
        checklist_name (str):
        checklist_description (str):
        is_completed (bool): Whether all required questions have been answered
        completion_percentage (float):
        unanswered_required_questions (int):
        requires_review (bool): Whether any answers triggered review requirements
        reviewed_by (Union[None, int]): User who reviewed the checklist completion
        reviewed_at (Union[None, datetime.datetime]):
        review_notes (str): Notes from the reviewer
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    offering_user: "OfferingUser"
    offering_user_uuid: Union[None, str]
    offering_name: Union[None, str]
    offering_uuid: Union[None, str]
    customer_provider_uuid: Union[None, str]
    customer_provider_name: Union[None, str]
    checklist_uuid: str
    checklist_name: str
    checklist_description: str
    is_completed: bool
    completion_percentage: float
    unanswered_required_questions: int
    requires_review: bool
    reviewed_by: Union[None, int]
    reviewed_at: Union[None, datetime.datetime]
    review_notes: str
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        offering_user = self.offering_user.to_dict()

        offering_user_uuid: Union[None, str]
        offering_user_uuid = self.offering_user_uuid

        offering_name: Union[None, str]
        offering_name = self.offering_name

        offering_uuid: Union[None, str]
        offering_uuid = self.offering_uuid

        customer_provider_uuid: Union[None, str]
        customer_provider_uuid = self.customer_provider_uuid

        customer_provider_name: Union[None, str]
        customer_provider_name = self.customer_provider_name

        checklist_uuid = self.checklist_uuid

        checklist_name = self.checklist_name

        checklist_description = self.checklist_description

        is_completed = self.is_completed

        completion_percentage = self.completion_percentage

        unanswered_required_questions = self.unanswered_required_questions

        requires_review = self.requires_review

        reviewed_by: Union[None, int]
        reviewed_by = self.reviewed_by

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        review_notes = self.review_notes

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "offering_user": offering_user,
                "offering_user_uuid": offering_user_uuid,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "customer_provider_uuid": customer_provider_uuid,
                "customer_provider_name": customer_provider_name,
                "checklist_uuid": checklist_uuid,
                "checklist_name": checklist_name,
                "checklist_description": checklist_description,
                "is_completed": is_completed,
                "completion_percentage": completion_percentage,
                "unanswered_required_questions": unanswered_required_questions,
                "requires_review": requires_review,
                "reviewed_by": reviewed_by,
                "reviewed_at": reviewed_at,
                "review_notes": review_notes,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_user import OfferingUser

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        offering_user = OfferingUser.from_dict(d.pop("offering_user"))

        def _parse_offering_user_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_user_uuid = _parse_offering_user_uuid(d.pop("offering_user_uuid"))

        def _parse_offering_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_name = _parse_offering_name(d.pop("offering_name"))

        def _parse_offering_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_uuid = _parse_offering_uuid(d.pop("offering_uuid"))

        def _parse_customer_provider_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_provider_uuid = _parse_customer_provider_uuid(d.pop("customer_provider_uuid"))

        def _parse_customer_provider_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_provider_name = _parse_customer_provider_name(d.pop("customer_provider_name"))

        checklist_uuid = d.pop("checklist_uuid")

        checklist_name = d.pop("checklist_name")

        checklist_description = d.pop("checklist_description")

        is_completed = d.pop("is_completed")

        completion_percentage = d.pop("completion_percentage")

        unanswered_required_questions = d.pop("unanswered_required_questions")

        requires_review = d.pop("requires_review")

        def _parse_reviewed_by(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by"))

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

        review_notes = d.pop("review_notes")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        user_checklist_completion = cls(
            uuid=uuid,
            offering_user=offering_user,
            offering_user_uuid=offering_user_uuid,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            customer_provider_uuid=customer_provider_uuid,
            customer_provider_name=customer_provider_name,
            checklist_uuid=checklist_uuid,
            checklist_name=checklist_name,
            checklist_description=checklist_description,
            is_completed=is_completed,
            completion_percentage=completion_percentage,
            unanswered_required_questions=unanswered_required_questions,
            requires_review=requires_review,
            reviewed_by=reviewed_by,
            reviewed_at=reviewed_at,
            review_notes=review_notes,
            created=created,
            modified=modified,
        )

        user_checklist_completion.additional_properties = d
        return user_checklist_completion

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

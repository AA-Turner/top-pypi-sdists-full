import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingQuestionMetadata")


@_attrs_define
class OnboardingQuestionMetadata:
    """
    Attributes:
        uuid (UUID):
        url (str):
        checklist_name (str):
        question (str):
        question_uuid (UUID):
        question_description (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        maps_to_customer_field (Union[Unset, str]): Customer model field name to map this answer to (e.g.,
            'registration_code', 'email', 'vat_code')
        intent_field (Union[Unset, str]): Type of intent/purpose field (e.g., 'intent', 'registration_purpose') - stays
            with verification
    """

    uuid: UUID
    url: str
    checklist_name: str
    question: str
    question_uuid: UUID
    question_description: str
    created: datetime.datetime
    modified: datetime.datetime
    maps_to_customer_field: Union[Unset, str] = UNSET
    intent_field: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        checklist_name = self.checklist_name

        question = self.question

        question_uuid = str(self.question_uuid)

        question_description = self.question_description

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        maps_to_customer_field = self.maps_to_customer_field

        intent_field = self.intent_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "checklist_name": checklist_name,
                "question": question,
                "question_uuid": question_uuid,
                "question_description": question_description,
                "created": created,
                "modified": modified,
            }
        )
        if maps_to_customer_field is not UNSET:
            field_dict["maps_to_customer_field"] = maps_to_customer_field
        if intent_field is not UNSET:
            field_dict["intent_field"] = intent_field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        checklist_name = d.pop("checklist_name")

        question = d.pop("question")

        question_uuid = UUID(d.pop("question_uuid"))

        question_description = d.pop("question_description")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        maps_to_customer_field = d.pop("maps_to_customer_field", UNSET)

        intent_field = d.pop("intent_field", UNSET)

        onboarding_question_metadata = cls(
            uuid=uuid,
            url=url,
            checklist_name=checklist_name,
            question=question,
            question_uuid=question_uuid,
            question_description=question_description,
            created=created,
            modified=modified,
            maps_to_customer_field=maps_to_customer_field,
            intent_field=intent_field,
        )

        onboarding_question_metadata.additional_properties = d
        return onboarding_question_metadata

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

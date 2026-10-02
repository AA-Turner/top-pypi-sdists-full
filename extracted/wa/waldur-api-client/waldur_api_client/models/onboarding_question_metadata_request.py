from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingQuestionMetadataRequest")


@_attrs_define
class OnboardingQuestionMetadataRequest:
    """
    Attributes:
        question (str):
        maps_to_customer_field (Union[Unset, str]): Customer model field name to map this answer to (e.g.,
            'registration_code', 'email', 'vat_code')
        intent_field (Union[Unset, str]): Type of intent/purpose field (e.g., 'intent', 'registration_purpose') - stays
            with verification
    """

    question: str
    maps_to_customer_field: Union[Unset, str] = UNSET
    intent_field: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        maps_to_customer_field = self.maps_to_customer_field

        intent_field = self.intent_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question": question,
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
        question = d.pop("question")

        maps_to_customer_field = d.pop("maps_to_customer_field", UNSET)

        intent_field = d.pop("intent_field", UNSET)

        onboarding_question_metadata_request = cls(
            question=question,
            maps_to_customer_field=maps_to_customer_field,
            intent_field=intent_field,
        )

        onboarding_question_metadata_request.additional_properties = d
        return onboarding_question_metadata_request

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

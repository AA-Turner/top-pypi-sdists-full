from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingJustificationCreateRequest")


@_attrs_define
class OnboardingJustificationCreateRequest:
    """
    Attributes:
        verification_uuid (UUID): UUID of the OnboardingVerification to justify
        user_justification (Union[Unset, str]): User's explanation for why they should be authorized
    """

    verification_uuid: UUID
    user_justification: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        verification_uuid = str(self.verification_uuid)

        user_justification = self.user_justification

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "verification_uuid": verification_uuid,
            }
        )
        if user_justification is not UNSET:
            field_dict["user_justification"] = user_justification

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        verification_uuid = UUID(d.pop("verification_uuid"))

        user_justification = d.pop("user_justification", UNSET)

        onboarding_justification_create_request = cls(
            verification_uuid=verification_uuid,
            user_justification=user_justification,
        )

        onboarding_justification_create_request.additional_properties = d
        return onboarding_justification_create_request

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

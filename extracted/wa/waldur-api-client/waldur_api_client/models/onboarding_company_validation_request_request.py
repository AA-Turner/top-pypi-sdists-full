from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.validation_method_enum import ValidationMethodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingCompanyValidationRequestRequest")


@_attrs_define
class OnboardingCompanyValidationRequestRequest:
    """
    Attributes:
        validation_method (Union[BlankEnum, Unset, ValidationMethodEnum]): Automatic validation method (e.g.,
            'ariregister', 'wirtschaftscompass', 'bolagsverket'). Leave empty for manual validation.
        country (Union[Unset, str]): ISO country code (e.g., 'EE', 'AT') - optional, for display context
        legal_person_identifier (Union[Unset, str]): Official company registration code
        legal_name (Union[Unset, str]): Company name (optional)
    """

    validation_method: Union[BlankEnum, Unset, ValidationMethodEnum] = UNSET
    country: Union[Unset, str] = UNSET
    legal_person_identifier: Union[Unset, str] = UNSET
    legal_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        validation_method: Union[Unset, str]
        if isinstance(self.validation_method, Unset):
            validation_method = UNSET
        elif isinstance(self.validation_method, ValidationMethodEnum):
            validation_method = self.validation_method.value
        else:
            validation_method = self.validation_method.value

        country = self.country

        legal_person_identifier = self.legal_person_identifier

        legal_name = self.legal_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if validation_method is not UNSET:
            field_dict["validation_method"] = validation_method
        if country is not UNSET:
            field_dict["country"] = country
        if legal_person_identifier is not UNSET:
            field_dict["legal_person_identifier"] = legal_person_identifier
        if legal_name is not UNSET:
            field_dict["legal_name"] = legal_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_validation_method(data: object) -> Union[BlankEnum, Unset, ValidationMethodEnum]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                validation_method_type_0 = ValidationMethodEnum(data)

                return validation_method_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            validation_method_type_1 = BlankEnum(data)

            return validation_method_type_1

        validation_method = _parse_validation_method(d.pop("validation_method", UNSET))

        country = d.pop("country", UNSET)

        legal_person_identifier = d.pop("legal_person_identifier", UNSET)

        legal_name = d.pop("legal_name", UNSET)

        onboarding_company_validation_request_request = cls(
            validation_method=validation_method,
            country=country,
            legal_person_identifier=legal_person_identifier,
            legal_name=legal_name,
        )

        onboarding_company_validation_request_request.additional_properties = d
        return onboarding_company_validation_request_request

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

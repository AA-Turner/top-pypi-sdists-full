from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.person_identifier_fields_response_person_identifier_fields import (
        PersonIdentifierFieldsResponsePersonIdentifierFields,
    )


T = TypeVar("T", bound="PersonIdentifierFieldsResponse")


@_attrs_define
class PersonIdentifierFieldsResponse:
    """
    Attributes:
        validation_method (str): The validation method identifier
        person_identifier_fields (PersonIdentifierFieldsResponsePersonIdentifierFields): Field specification for person
            identification. For simple identifiers: {type: 'string', field: 'civil_number', ...}. For composite identifiers:
            {type: 'object', fields: {...}}
    """

    validation_method: str
    person_identifier_fields: "PersonIdentifierFieldsResponsePersonIdentifierFields"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        validation_method = self.validation_method

        person_identifier_fields = self.person_identifier_fields.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "validation_method": validation_method,
                "person_identifier_fields": person_identifier_fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_identifier_fields_response_person_identifier_fields import (
            PersonIdentifierFieldsResponsePersonIdentifierFields,
        )

        d = dict(src_dict)
        validation_method = d.pop("validation_method")

        person_identifier_fields = PersonIdentifierFieldsResponsePersonIdentifierFields.from_dict(
            d.pop("person_identifier_fields")
        )

        person_identifier_fields_response = cls(
            validation_method=validation_method,
            person_identifier_fields=person_identifier_fields,
        )

        person_identifier_fields_response.additional_properties = d
        return person_identifier_fields_response

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

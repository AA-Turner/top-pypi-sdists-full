import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingRunValidationRequestRequest")


@_attrs_define
class OnboardingRunValidationRequestRequest:
    """
    Attributes:
        civil_number (Union[Unset, str]): Personal identifier (temporary workaround for Estonian civil_number)
        first_name (Union[Unset, str]): User's first name (temporary workaround for Austrian validation)
        last_name (Union[Unset, str]): User's last name (temporary workaround for Austrian validation)
        birth_date (Union[None, Unset, datetime.date]): User's birth date (temporary workaround for Austrian validation)
    """

    civil_number: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        civil_number = self.civil_number

        first_name = self.first_name

        last_name = self.last_name

        birth_date: Union[None, Unset, str]
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if civil_number is not UNSET:
            field_dict["civil_number"] = civil_number
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        civil_number = d.pop("civil_number", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        def _parse_birth_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birth_date_type_0 = isoparse(data).date()

                return birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        birth_date = _parse_birth_date(d.pop("birth_date", UNSET))

        onboarding_run_validation_request_request = cls(
            civil_number=civil_number,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
        )

        onboarding_run_validation_request_request.additional_properties = d
        return onboarding_run_validation_request_request

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

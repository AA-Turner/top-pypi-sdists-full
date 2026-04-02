import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="IdentityBridgeRequestRequest")


@_attrs_define
class IdentityBridgeRequestRequest:
    """
    Attributes:
        username (str): CUID / username of the user to create or update.
        source (str): ISD source identifier, e.g. 'isd:puhuri'. Must match ^[a-z]+:[a-zA-Z0-9._-]+$.
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
        email (Union[Unset, str]):
        organization (Union[Unset, str]):
        affiliations (Union[Unset, list[str]]):
        civil_number (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        identity_source (Union[Unset, str]):
        gender (Union[None, Unset, int]):
        personal_title (Union[Unset, str]):
        birth_date (Union[None, Unset, datetime.date]):
        place_of_birth (Union[Unset, str]):
        country_of_residence (Union[Unset, str]):
        nationality (Union[Unset, str]):
        nationalities (Union[Unset, list[str]]):
        organization_country (Union[Unset, str]):
        organization_type (Union[Unset, str]):
        eduperson_assurance (Union[Unset, list[str]]):
    """

    username: str
    source: str
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    affiliations: Union[Unset, list[str]] = UNSET
    civil_number: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    identity_source: Union[Unset, str] = UNSET
    gender: Union[None, Unset, int] = UNSET
    personal_title: Union[Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    place_of_birth: Union[Unset, str] = UNSET
    country_of_residence: Union[Unset, str] = UNSET
    nationality: Union[Unset, str] = UNSET
    nationalities: Union[Unset, list[str]] = UNSET
    organization_country: Union[Unset, str] = UNSET
    organization_type: Union[Unset, str] = UNSET
    eduperson_assurance: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        source = self.source

        first_name = self.first_name

        last_name = self.last_name

        email = self.email

        organization = self.organization

        affiliations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.affiliations, Unset):
            affiliations = self.affiliations

        civil_number = self.civil_number

        phone_number = self.phone_number

        identity_source = self.identity_source

        gender: Union[None, Unset, int]
        if isinstance(self.gender, Unset):
            gender = UNSET
        else:
            gender = self.gender

        personal_title = self.personal_title

        birth_date: Union[None, Unset, str]
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        place_of_birth = self.place_of_birth

        country_of_residence = self.country_of_residence

        nationality = self.nationality

        nationalities: Union[Unset, list[str]] = UNSET
        if not isinstance(self.nationalities, Unset):
            nationalities = self.nationalities

        organization_country = self.organization_country

        organization_type = self.organization_type

        eduperson_assurance: Union[Unset, list[str]] = UNSET
        if not isinstance(self.eduperson_assurance, Unset):
            eduperson_assurance = self.eduperson_assurance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "source": source,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if organization is not UNSET:
            field_dict["organization"] = organization
        if affiliations is not UNSET:
            field_dict["affiliations"] = affiliations
        if civil_number is not UNSET:
            field_dict["civil_number"] = civil_number
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if identity_source is not UNSET:
            field_dict["identity_source"] = identity_source
        if gender is not UNSET:
            field_dict["gender"] = gender
        if personal_title is not UNSET:
            field_dict["personal_title"] = personal_title
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if place_of_birth is not UNSET:
            field_dict["place_of_birth"] = place_of_birth
        if country_of_residence is not UNSET:
            field_dict["country_of_residence"] = country_of_residence
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if nationalities is not UNSET:
            field_dict["nationalities"] = nationalities
        if organization_country is not UNSET:
            field_dict["organization_country"] = organization_country
        if organization_type is not UNSET:
            field_dict["organization_type"] = organization_type
        if eduperson_assurance is not UNSET:
            field_dict["eduperson_assurance"] = eduperson_assurance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        source = d.pop("source")

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        email = d.pop("email", UNSET)

        organization = d.pop("organization", UNSET)

        affiliations = cast(list[str], d.pop("affiliations", UNSET))

        civil_number = d.pop("civil_number", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        identity_source = d.pop("identity_source", UNSET)

        def _parse_gender(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        gender = _parse_gender(d.pop("gender", UNSET))

        personal_title = d.pop("personal_title", UNSET)

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

        place_of_birth = d.pop("place_of_birth", UNSET)

        country_of_residence = d.pop("country_of_residence", UNSET)

        nationality = d.pop("nationality", UNSET)

        nationalities = cast(list[str], d.pop("nationalities", UNSET))

        organization_country = d.pop("organization_country", UNSET)

        organization_type = d.pop("organization_type", UNSET)

        eduperson_assurance = cast(list[str], d.pop("eduperson_assurance", UNSET))

        identity_bridge_request_request = cls(
            username=username,
            source=source,
            first_name=first_name,
            last_name=last_name,
            email=email,
            organization=organization,
            affiliations=affiliations,
            civil_number=civil_number,
            phone_number=phone_number,
            identity_source=identity_source,
            gender=gender,
            personal_title=personal_title,
            birth_date=birth_date,
            place_of_birth=place_of_birth,
            country_of_residence=country_of_residence,
            nationality=nationality,
            nationalities=nationalities,
            organization_country=organization_country,
            organization_type=organization_type,
            eduperson_assurance=eduperson_assurance,
        )

        identity_bridge_request_request.additional_properties = d
        return identity_bridge_request_request

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

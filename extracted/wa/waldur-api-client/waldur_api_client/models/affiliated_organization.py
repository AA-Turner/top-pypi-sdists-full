import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliatedOrganization")


@_attrs_define
class AffiliatedOrganization:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        url (Union[Unset, str]):
        name (Union[Unset, str]):
        code (Union[Unset, str]): Unique short identifier, e.g. CERN, EMBL.
        abbreviation (Union[Unset, str]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        homepage (Union[Unset, str]):
        country (Union[Unset, str]):
        address (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        projects_count (Union[Unset, int]): Number of active projects affiliated with this organization
    """

    uuid: Union[Unset, UUID] = UNSET
    url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    abbreviation: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    homepage: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    projects_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        url = self.url

        name = self.name

        code = self.code

        abbreviation = self.abbreviation

        description = self.description

        email = self.email

        homepage = self.homepage

        country = self.country

        address = self.address

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        projects_count = self.projects_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if code is not UNSET:
            field_dict["code"] = code
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if description is not UNSET:
            field_dict["description"] = description
        if email is not UNSET:
            field_dict["email"] = email
        if homepage is not UNSET:
            field_dict["homepage"] = homepage
        if country is not UNSET:
            field_dict["country"] = country
        if address is not UNSET:
            field_dict["address"] = address
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if projects_count is not UNSET:
            field_dict["projects_count"] = projects_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        code = d.pop("code", UNSET)

        abbreviation = d.pop("abbreviation", UNSET)

        description = d.pop("description", UNSET)

        email = d.pop("email", UNSET)

        homepage = d.pop("homepage", UNSET)

        country = d.pop("country", UNSET)

        address = d.pop("address", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        projects_count = d.pop("projects_count", UNSET)

        affiliated_organization = cls(
            uuid=uuid,
            url=url,
            name=name,
            code=code,
            abbreviation=abbreviation,
            description=description,
            email=email,
            homepage=homepage,
            country=country,
            address=address,
            created=created,
            modified=modified,
            projects_count=projects_count,
        )

        affiliated_organization.additional_properties = d
        return affiliated_organization

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

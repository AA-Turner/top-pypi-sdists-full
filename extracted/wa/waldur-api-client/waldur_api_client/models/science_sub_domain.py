import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScienceSubDomain")


@_attrs_define
class ScienceSubDomain:
    """
    Attributes:
        uuid (UUID):
        url (str):
        name (str):
        domain (str):
        domain_uuid (UUID):
        domain_name (str):
        domain_code (str): Domain code (e.g. '1'). Auto-derived if left blank.
        created (datetime.datetime):
        modified (datetime.datetime):
        projects_count (int): Number of active projects using this sub-domain
        code (Union[Unset, str]): Sub-domain code (e.g. '1.1'). Auto-derived from domain code if left blank.
    """

    uuid: UUID
    url: str
    name: str
    domain: str
    domain_uuid: UUID
    domain_name: str
    domain_code: str
    created: datetime.datetime
    modified: datetime.datetime
    projects_count: int
    code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        name = self.name

        domain = self.domain

        domain_uuid = str(self.domain_uuid)

        domain_name = self.domain_name

        domain_code = self.domain_code

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        projects_count = self.projects_count

        code = self.code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "name": name,
                "domain": domain,
                "domain_uuid": domain_uuid,
                "domain_name": domain_name,
                "domain_code": domain_code,
                "created": created,
                "modified": modified,
                "projects_count": projects_count,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        name = d.pop("name")

        domain = d.pop("domain")

        domain_uuid = UUID(d.pop("domain_uuid"))

        domain_name = d.pop("domain_name")

        domain_code = d.pop("domain_code")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        projects_count = d.pop("projects_count")

        code = d.pop("code", UNSET)

        science_sub_domain = cls(
            uuid=uuid,
            url=url,
            name=name,
            domain=domain,
            domain_uuid=domain_uuid,
            domain_name=domain_name,
            domain_code=domain_code,
            created=created,
            modified=modified,
            projects_count=projects_count,
            code=code,
        )

        science_sub_domain.additional_properties = d
        return science_sub_domain

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

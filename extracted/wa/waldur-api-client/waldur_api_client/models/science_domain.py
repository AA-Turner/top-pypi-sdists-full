import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScienceDomain")


@_attrs_define
class ScienceDomain:
    """
    Attributes:
        uuid (UUID):
        url (str):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        subdomains_count (int): Number of sub-domains in this domain
        code (Union[Unset, str]): Domain code (e.g. '1'). Auto-derived if left blank.
    """

    uuid: UUID
    url: str
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    subdomains_count: int
    code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        subdomains_count = self.subdomains_count

        code = self.code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "name": name,
                "created": created,
                "modified": modified,
                "subdomains_count": subdomains_count,
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

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        subdomains_count = d.pop("subdomains_count")

        code = d.pop("code", UNSET)

        science_domain = cls(
            uuid=uuid,
            url=url,
            name=name,
            created=created,
            modified=modified,
            subdomains_count=subdomains_count,
            code=code,
        )

        science_domain.additional_properties = d
        return science_domain

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

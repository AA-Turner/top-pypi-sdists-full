from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerCandidate")


@_attrs_define
class CustomerCandidate:
    """
    Attributes:
        uuid (UUID):
        name (str):
        url (Union[None, str]):
        abbreviation (Union[Unset, str]):
    """

    uuid: UUID
    name: str
    url: Union[None, str]
    abbreviation: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        url: Union[None, str]
        url = self.url

        abbreviation = self.abbreviation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "url": url,
            }
        )
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        def _parse_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        url = _parse_url(d.pop("url"))

        abbreviation = d.pop("abbreviation", UNSET)

        customer_candidate = cls(
            uuid=uuid,
            name=name,
            url=url,
            abbreviation=abbreviation,
        )

        customer_candidate.additional_properties = d
        return customer_candidate

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

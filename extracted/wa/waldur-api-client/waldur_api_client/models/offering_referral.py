from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingReferral")


@_attrs_define
class OfferingReferral:
    """
    Attributes:
        url (str):
        uuid (UUID):
        scope (str):
        scope_uuid (UUID):
        pid (Union[Unset, str]):
        relation_type (Union[Unset, str]):
        resource_type (Union[Unset, str]):
        creator (Union[Unset, str]):
        publisher (Union[Unset, str]):
        published (Union[Unset, str]):
        title (Union[Unset, str]):
        referral_url (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    scope: str
    scope_uuid: UUID
    pid: Union[Unset, str] = UNSET
    relation_type: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    creator: Union[Unset, str] = UNSET
    publisher: Union[Unset, str] = UNSET
    published: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    referral_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        scope = self.scope

        scope_uuid = str(self.scope_uuid)

        pid = self.pid

        relation_type = self.relation_type

        resource_type = self.resource_type

        creator = self.creator

        publisher = self.publisher

        published = self.published

        title = self.title

        referral_url = self.referral_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "scope": scope,
                "scope_uuid": scope_uuid,
            }
        )
        if pid is not UNSET:
            field_dict["pid"] = pid
        if relation_type is not UNSET:
            field_dict["relation_type"] = relation_type
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if creator is not UNSET:
            field_dict["creator"] = creator
        if publisher is not UNSET:
            field_dict["publisher"] = publisher
        if published is not UNSET:
            field_dict["published"] = published
        if title is not UNSET:
            field_dict["title"] = title
        if referral_url is not UNSET:
            field_dict["referral_url"] = referral_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        scope = d.pop("scope")

        scope_uuid = UUID(d.pop("scope_uuid"))

        pid = d.pop("pid", UNSET)

        relation_type = d.pop("relation_type", UNSET)

        resource_type = d.pop("resource_type", UNSET)

        creator = d.pop("creator", UNSET)

        publisher = d.pop("publisher", UNSET)

        published = d.pop("published", UNSET)

        title = d.pop("title", UNSET)

        referral_url = d.pop("referral_url", UNSET)

        offering_referral = cls(
            url=url,
            uuid=uuid,
            scope=scope,
            scope_uuid=scope_uuid,
            pid=pid,
            relation_type=relation_type,
            resource_type=resource_type,
            creator=creator,
            publisher=publisher,
            published=published,
            title=title,
            referral_url=referral_url,
        )

        offering_referral.additional_properties = d
        return offering_referral

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

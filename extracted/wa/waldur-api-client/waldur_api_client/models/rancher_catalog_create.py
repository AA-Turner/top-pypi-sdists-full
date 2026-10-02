import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.rancher_catalog_scope_type import RancherCatalogScopeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherCatalogCreate")


@_attrs_define
class RancherCatalogCreate:
    """
    Attributes:
        uuid (UUID):
        url (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        name (str):
        catalog_url (str):
        branch (str):
        commit (str):
        runtime_state (str):
        scope (str):
        scope_type (RancherCatalogScopeType):
        description (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
    """

    uuid: UUID
    url: str
    created: datetime.datetime
    modified: datetime.datetime
    name: str
    catalog_url: str
    branch: str
    commit: str
    runtime_state: str
    scope: str
    scope_type: RancherCatalogScopeType
    description: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        name = self.name

        catalog_url = self.catalog_url

        branch = self.branch

        commit = self.commit

        runtime_state = self.runtime_state

        scope = self.scope

        scope_type = self.scope_type.value

        description = self.description

        username = self.username

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "created": created,
                "modified": modified,
                "name": name,
                "catalog_url": catalog_url,
                "branch": branch,
                "commit": commit,
                "runtime_state": runtime_state,
                "scope": scope,
                "scope_type": scope_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        name = d.pop("name")

        catalog_url = d.pop("catalog_url")

        branch = d.pop("branch")

        commit = d.pop("commit")

        runtime_state = d.pop("runtime_state")

        scope = d.pop("scope")

        scope_type = RancherCatalogScopeType(d.pop("scope_type"))

        description = d.pop("description", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        rancher_catalog_create = cls(
            uuid=uuid,
            url=url,
            created=created,
            modified=modified,
            name=name,
            catalog_url=catalog_url,
            branch=branch,
            commit=commit,
            runtime_state=runtime_state,
            scope=scope,
            scope_type=scope_type,
            description=description,
            username=username,
            password=password,
        )

        rancher_catalog_create.additional_properties = d
        return rancher_catalog_create

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

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.rancher_catalog_scope_type import RancherCatalogScopeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherCatalog")


@_attrs_define
class RancherCatalog:
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

        rancher_catalog = cls(
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
        )

        rancher_catalog.additional_properties = d
        return rancher_catalog

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

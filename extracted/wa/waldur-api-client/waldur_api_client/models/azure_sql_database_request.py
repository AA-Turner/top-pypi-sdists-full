from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AzureSqlDatabaseRequest")


@_attrs_define
class AzureSqlDatabaseRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        server (str):
        description (Union[Unset, str]):
        charset (Union[None, Unset, str]):
        collation (Union[None, Unset, str]):
    """

    name: str
    service_settings: str
    project: str
    server: str
    description: Union[Unset, str] = UNSET
    charset: Union[None, Unset, str] = UNSET
    collation: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        server = self.server

        description = self.description

        charset: Union[None, Unset, str]
        if isinstance(self.charset, Unset):
            charset = UNSET
        else:
            charset = self.charset

        collation: Union[None, Unset, str]
        if isinstance(self.collation, Unset):
            collation = UNSET
        else:
            collation = self.collation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "server": server,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if charset is not UNSET:
            field_dict["charset"] = charset
        if collation is not UNSET:
            field_dict["collation"] = collation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        server = d.pop("server")

        description = d.pop("description", UNSET)

        def _parse_charset(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        charset = _parse_charset(d.pop("charset", UNSET))

        def _parse_collation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        collation = _parse_collation(d.pop("collation", UNSET))

        azure_sql_database_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            server=server,
            description=description,
            charset=charset,
            collation=collation,
        )

        azure_sql_database_request.additional_properties = d
        return azure_sql_database_request

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

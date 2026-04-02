import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentIdentityRequest")


@_attrs_define
class AgentIdentityRequest:
    """
    Attributes:
        offering (UUID): UUID of an offering with a site-agent compatible type.
        name (str):
        version (Union[None, Unset, str]):
        dependencies (Union[Unset, Any]):
        config_file_path (Union[None, Unset, str]): Example: '/etc/waldur/agent.yaml'
        config_file_content (Union[None, Unset, str]):
        last_restarted (Union[Unset, datetime.datetime]):
    """

    offering: UUID
    name: str
    version: Union[None, Unset, str] = UNSET
    dependencies: Union[Unset, Any] = UNSET
    config_file_path: Union[None, Unset, str] = UNSET
    config_file_content: Union[None, Unset, str] = UNSET
    last_restarted: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering = str(self.offering)

        name = self.name

        version: Union[None, Unset, str]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        dependencies = self.dependencies

        config_file_path: Union[None, Unset, str]
        if isinstance(self.config_file_path, Unset):
            config_file_path = UNSET
        else:
            config_file_path = self.config_file_path

        config_file_content: Union[None, Unset, str]
        if isinstance(self.config_file_content, Unset):
            config_file_content = UNSET
        else:
            config_file_content = self.config_file_content

        last_restarted: Union[Unset, str] = UNSET
        if not isinstance(self.last_restarted, Unset):
            last_restarted = self.last_restarted.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
                "name": name,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if dependencies is not UNSET:
            field_dict["dependencies"] = dependencies
        if config_file_path is not UNSET:
            field_dict["config_file_path"] = config_file_path
        if config_file_content is not UNSET:
            field_dict["config_file_content"] = config_file_content
        if last_restarted is not UNSET:
            field_dict["last_restarted"] = last_restarted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering = UUID(d.pop("offering"))

        name = d.pop("name")

        def _parse_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        version = _parse_version(d.pop("version", UNSET))

        dependencies = d.pop("dependencies", UNSET)

        def _parse_config_file_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        config_file_path = _parse_config_file_path(d.pop("config_file_path", UNSET))

        def _parse_config_file_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        config_file_content = _parse_config_file_content(d.pop("config_file_content", UNSET))

        _last_restarted = d.pop("last_restarted", UNSET)
        last_restarted: Union[Unset, datetime.datetime]
        if isinstance(_last_restarted, Unset):
            last_restarted = UNSET
        else:
            last_restarted = isoparse(_last_restarted)

        agent_identity_request = cls(
            offering=offering,
            name=name,
            version=version,
            dependencies=dependencies,
            config_file_path=config_file_path,
            config_file_content=config_file_content,
            last_restarted=last_restarted,
        )

        agent_identity_request.additional_properties = d
        return agent_identity_request

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

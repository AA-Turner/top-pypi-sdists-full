import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_agent_service import NestedAgentService


T = TypeVar("T", bound="AgentIdentity")


@_attrs_define
class AgentIdentity:
    """
    Attributes:
        uuid (UUID):
        url (str):
        offering (UUID): UUID of an offering with a site-agent compatible type.
        created_by (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        services (list['NestedAgentService']):
        version (Union[None, Unset, str]):
        dependencies (Union[Unset, Any]):
        config_file_path (Union[None, Unset, str]): Example: '/etc/waldur/agent.yaml'
        config_file_content (Union[None, Unset, str]):
        last_restarted (Union[Unset, datetime.datetime]):
    """

    uuid: UUID
    url: str
    offering: UUID
    created_by: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    services: list["NestedAgentService"]
    version: Union[None, Unset, str] = UNSET
    dependencies: Union[Unset, Any] = UNSET
    config_file_path: Union[None, Unset, str] = UNSET
    config_file_content: Union[None, Unset, str] = UNSET
    last_restarted: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        offering = str(self.offering)

        created_by = str(self.created_by)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        services = []
        for services_item_data in self.services:
            services_item = services_item_data.to_dict()
            services.append(services_item)

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
                "uuid": uuid,
                "url": url,
                "offering": offering,
                "created_by": created_by,
                "name": name,
                "created": created,
                "modified": modified,
                "services": services,
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
        from ..models.nested_agent_service import NestedAgentService

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        offering = UUID(d.pop("offering"))

        created_by = UUID(d.pop("created_by"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        services = []
        _services = d.pop("services")
        for services_item_data in _services:
            services_item = NestedAgentService.from_dict(services_item_data)

            services.append(services_item)

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

        agent_identity = cls(
            uuid=uuid,
            url=url,
            offering=offering,
            created_by=created_by,
            name=name,
            created=created,
            modified=modified,
            services=services,
            version=version,
            dependencies=dependencies,
            config_file_path=config_file_path,
            config_file_content=config_file_content,
            last_restarted=last_restarted,
        )

        agent_identity.additional_properties = d
        return agent_identity

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

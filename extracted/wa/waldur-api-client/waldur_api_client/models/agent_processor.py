import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentProcessor")


@_attrs_define
class AgentProcessor:
    """
    Attributes:
        uuid (UUID):
        url (str):
        service (UUID):
        service_name (str):
        name (str):
        backend_type (str): Type of the backend, for example SLURM.
        created (datetime.datetime):
        modified (datetime.datetime):
        last_run (Union[None, Unset, datetime.datetime]):
        backend_version (Union[None, Unset, str]):
    """

    uuid: UUID
    url: str
    service: UUID
    service_name: str
    name: str
    backend_type: str
    created: datetime.datetime
    modified: datetime.datetime
    last_run: Union[None, Unset, datetime.datetime] = UNSET
    backend_version: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        service = str(self.service)

        service_name = self.service_name

        name = self.name

        backend_type = self.backend_type

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        last_run: Union[None, Unset, str]
        if isinstance(self.last_run, Unset):
            last_run = UNSET
        elif isinstance(self.last_run, datetime.datetime):
            last_run = self.last_run.isoformat()
        else:
            last_run = self.last_run

        backend_version: Union[None, Unset, str]
        if isinstance(self.backend_version, Unset):
            backend_version = UNSET
        else:
            backend_version = self.backend_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "service": service,
                "service_name": service_name,
                "name": name,
                "backend_type": backend_type,
                "created": created,
                "modified": modified,
            }
        )
        if last_run is not UNSET:
            field_dict["last_run"] = last_run
        if backend_version is not UNSET:
            field_dict["backend_version"] = backend_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        service = UUID(d.pop("service"))

        service_name = d.pop("service_name")

        name = d.pop("name")

        backend_type = d.pop("backend_type")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_last_run(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_run_type_0 = isoparse(data)

                return last_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_run = _parse_last_run(d.pop("last_run", UNSET))

        def _parse_backend_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_version = _parse_backend_version(d.pop("backend_version", UNSET))

        agent_processor = cls(
            uuid=uuid,
            url=url,
            service=service,
            service_name=service_name,
            name=name,
            backend_type=backend_type,
            created=created,
            modified=modified,
            last_run=last_run,
            backend_version=backend_version,
        )

        agent_processor.additional_properties = d
        return agent_processor

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

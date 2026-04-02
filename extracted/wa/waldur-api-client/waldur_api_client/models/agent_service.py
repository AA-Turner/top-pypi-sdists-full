import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_service_state import AgentServiceState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_agent_processor import NestedAgentProcessor


T = TypeVar("T", bound="AgentService")


@_attrs_define
class AgentService:
    """
    Attributes:
        uuid (UUID):
        url (str):
        identity (UUID):
        identity_name (str):
        name (str):
        state (AgentServiceState):
        created (datetime.datetime):
        modified (datetime.datetime):
        processors (list['NestedAgentProcessor']):
        mode (Union[None, Unset, str]):
        statistics (Union[Unset, Any]):
    """

    uuid: UUID
    url: str
    identity: UUID
    identity_name: str
    name: str
    state: AgentServiceState
    created: datetime.datetime
    modified: datetime.datetime
    processors: list["NestedAgentProcessor"]
    mode: Union[None, Unset, str] = UNSET
    statistics: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        identity = str(self.identity)

        identity_name = self.identity_name

        name = self.name

        state = self.state.value

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        processors = []
        for processors_item_data in self.processors:
            processors_item = processors_item_data.to_dict()
            processors.append(processors_item)

        mode: Union[None, Unset, str]
        if isinstance(self.mode, Unset):
            mode = UNSET
        else:
            mode = self.mode

        statistics = self.statistics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "identity": identity,
                "identity_name": identity_name,
                "name": name,
                "state": state,
                "created": created,
                "modified": modified,
                "processors": processors,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if statistics is not UNSET:
            field_dict["statistics"] = statistics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_agent_processor import NestedAgentProcessor

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        identity = UUID(d.pop("identity"))

        identity_name = d.pop("identity_name")

        name = d.pop("name")

        state = AgentServiceState(d.pop("state"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        processors = []
        _processors = d.pop("processors")
        for processors_item_data in _processors:
            processors_item = NestedAgentProcessor.from_dict(processors_item_data)

            processors.append(processors_item)

        def _parse_mode(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mode = _parse_mode(d.pop("mode", UNSET))

        statistics = d.pop("statistics", UNSET)

        agent_service = cls(
            uuid=uuid,
            url=url,
            identity=identity,
            identity_name=identity_name,
            name=name,
            state=state,
            created=created,
            modified=modified,
            processors=processors,
            mode=mode,
            statistics=statistics,
        )

        agent_service.additional_properties = d
        return agent_service

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

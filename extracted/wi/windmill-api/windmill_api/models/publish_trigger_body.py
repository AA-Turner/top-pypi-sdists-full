from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_trigger_body_config import PublishTriggerBodyConfig


T = TypeVar("T", bound="PublishTriggerBody")


@_attrs_define
class PublishTriggerBody:
    """
    Attributes:
        path (str):
        kind (str):
        config (PublishTriggerBodyConfig):
        summary (Union[Unset, None, str]):
        description (Union[Unset, None, str]):
        script_ask_id (Union[Unset, None, int]):
        flow_id (Union[Unset, None, int]):
    """

    path: str
    kind: str
    config: "PublishTriggerBodyConfig"
    summary: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    script_ask_id: Union[Unset, None, int] = UNSET
    flow_id: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind
        config = self.config.to_dict()

        summary = self.summary
        description = self.description
        script_ask_id = self.script_ask_id
        flow_id = self.flow_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
                "config": config,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if script_ask_id is not UNSET:
            field_dict["script_ask_id"] = script_ask_id
        if flow_id is not UNSET:
            field_dict["flow_id"] = flow_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_trigger_body_config import PublishTriggerBodyConfig

        d = src_dict.copy()
        path = d.pop("path")

        kind = d.pop("kind")

        config = PublishTriggerBodyConfig.from_dict(d.pop("config"))

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        script_ask_id = d.pop("script_ask_id", UNSET)

        flow_id = d.pop("flow_id", UNSET)

        publish_trigger_body = cls(
            path=path,
            kind=kind,
            config=config,
            summary=summary,
            description=description,
            script_ask_id=script_ask_id,
            flow_id=flow_id,
        )

        publish_trigger_body.additional_properties = d
        return publish_trigger_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

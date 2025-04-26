from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateNatsTriggerJsonBody")


@_attrs_define
class CreateNatsTriggerJsonBody:
    """
    Attributes:
        path (str):
        script_path (str):
        is_flow (bool):
        nats_resource_path (str):
        use_jetstream (bool):
        subjects (List[str]):
        stream_name (Union[Unset, str]):
        consumer_name (Union[Unset, str]):
        enabled (Union[Unset, bool]):
    """

    path: str
    script_path: str
    is_flow: bool
    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    stream_name: Union[Unset, str] = UNSET
    consumer_name: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        nats_resource_path = self.nats_resource_path
        use_jetstream = self.use_jetstream
        subjects = self.subjects

        stream_name = self.stream_name
        consumer_name = self.consumer_name
        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "nats_resource_path": nats_resource_path,
                "use_jetstream": use_jetstream,
                "subjects": subjects,
            }
        )
        if stream_name is not UNSET:
            field_dict["stream_name"] = stream_name
        if consumer_name is not UNSET:
            field_dict["consumer_name"] = consumer_name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        nats_resource_path = d.pop("nats_resource_path")

        use_jetstream = d.pop("use_jetstream")

        subjects = cast(List[str], d.pop("subjects"))

        stream_name = d.pop("stream_name", UNSET)

        consumer_name = d.pop("consumer_name", UNSET)

        enabled = d.pop("enabled", UNSET)

        create_nats_trigger_json_body = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            nats_resource_path=nats_resource_path,
            use_jetstream=use_jetstream,
            subjects=subjects,
            stream_name=stream_name,
            consumer_name=consumer_name,
            enabled=enabled,
        )

        create_nats_trigger_json_body.additional_properties = d
        return create_nats_trigger_json_body

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

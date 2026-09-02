from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAmqpTriggerJsonBodyOptions")


@_attrs_define
class CreateAmqpTriggerJsonBodyOptions:
    """Optional consumer options (queue declaration, prefetch)

    Attributes:
        declare_queue (Union[Unset, bool]): Declare the queue (durable) before consuming; when false the queue is
            declared passively and must already exist
        prefetch_count (Union[Unset, int]): Maximum number of unacknowledged messages the broker delivers at once
            (1-65535)
    """

    declare_queue: Union[Unset, bool] = UNSET
    prefetch_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        declare_queue = self.declare_queue
        prefetch_count = self.prefetch_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if declare_queue is not UNSET:
            field_dict["declare_queue"] = declare_queue
        if prefetch_count is not UNSET:
            field_dict["prefetch_count"] = prefetch_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        declare_queue = d.pop("declare_queue", UNSET)

        prefetch_count = d.pop("prefetch_count", UNSET)

        create_amqp_trigger_json_body_options = cls(
            declare_queue=declare_queue,
            prefetch_count=prefetch_count,
        )

        create_amqp_trigger_json_body_options.additional_properties = d
        return create_amqp_trigger_json_body_options

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

from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestAmqpConnectionJsonBody")


@_attrs_define
class TestAmqpConnectionJsonBody:
    """
    Attributes:
        amqp_resource_path (str): Path to the AMQP resource containing broker connection configuration
    """

    amqp_resource_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amqp_resource_path = self.amqp_resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amqp_resource_path": amqp_resource_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amqp_resource_path = d.pop("amqp_resource_path")

        test_amqp_connection_json_body = cls(
            amqp_resource_path=amqp_resource_path,
        )

        test_amqp_connection_json_body.additional_properties = d
        return test_amqp_connection_json_body

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

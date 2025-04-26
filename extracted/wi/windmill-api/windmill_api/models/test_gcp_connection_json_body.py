from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.test_gcp_connection_json_body_connection import TestGcpConnectionJsonBodyConnection


T = TypeVar("T", bound="TestGcpConnectionJsonBody")


@_attrs_define
class TestGcpConnectionJsonBody:
    """
    Attributes:
        connection (TestGcpConnectionJsonBodyConnection):
    """

    connection: "TestGcpConnectionJsonBodyConnection"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connection = self.connection.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connection": connection,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_gcp_connection_json_body_connection import TestGcpConnectionJsonBodyConnection

        d = src_dict.copy()
        connection = TestGcpConnectionJsonBodyConnection.from_dict(d.pop("connection"))

        test_gcp_connection_json_body = cls(
            connection=connection,
        )

        test_gcp_connection_json_body.additional_properties = d
        return test_gcp_connection_json_body

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

from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDataTableConnectionResponse200")


@_attrs_define
class TestDataTableConnectionResponse200:
    """
    Attributes:
        user (str):
        can_create_table (bool):
        can_create_schema (bool):
        migrations_table_exists (bool):
        suggested_grants (List[str]):
        schema (Optional[str]):
        suggested_search_path (Union[Unset, str]):
    """

    user: str
    can_create_table: bool
    can_create_schema: bool
    migrations_table_exists: bool
    suggested_grants: List[str]
    schema: Optional[str]
    suggested_search_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user = self.user
        can_create_table = self.can_create_table
        can_create_schema = self.can_create_schema
        migrations_table_exists = self.migrations_table_exists
        suggested_grants = self.suggested_grants

        schema = self.schema
        suggested_search_path = self.suggested_search_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "can_create_table": can_create_table,
                "can_create_schema": can_create_schema,
                "migrations_table_exists": migrations_table_exists,
                "suggested_grants": suggested_grants,
                "schema": schema,
            }
        )
        if suggested_search_path is not UNSET:
            field_dict["suggested_search_path"] = suggested_search_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user = d.pop("user")

        can_create_table = d.pop("can_create_table")

        can_create_schema = d.pop("can_create_schema")

        migrations_table_exists = d.pop("migrations_table_exists")

        suggested_grants = cast(List[str], d.pop("suggested_grants"))

        schema = d.pop("schema")

        suggested_search_path = d.pop("suggested_search_path", UNSET)

        test_data_table_connection_response_200 = cls(
            user=user,
            can_create_table=can_create_table,
            can_create_schema=can_create_schema,
            migrations_table_exists=migrations_table_exists,
            suggested_grants=suggested_grants,
            schema=schema,
            suggested_search_path=suggested_search_path,
        )

        test_data_table_connection_response_200.additional_properties = d
        return test_data_table_connection_response_200

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

from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset


T = TypeVar("T", bound="MultiQueryJsonBodyQueriesItem")


@attr.s(auto_attribs=True)
class MultiQueryJsonBodyQueriesItem:
    """
    ### Attributes:
    * `query_id (str)`: None
    * `sql (str)`: None
    """

    query_id: str
    sql: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_id = self.query_id
        sql = self.sql

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query_id": query_id,
                "sql": sql,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_id = d.pop("query_id")

        sql = d.pop("sql")

        multi_query_json_body_queries_item = cls(
            query_id=query_id,
            sql=sql,
        )

        multi_query_json_body_queries_item.additional_properties = d
        return multi_query_json_body_queries_item

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

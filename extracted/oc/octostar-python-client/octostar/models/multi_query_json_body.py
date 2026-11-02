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

from typing import cast, List
from typing import Dict
from typing import cast

if TYPE_CHECKING:
    from ..models.multi_query_json_body_queries_item import (
        MultiQueryJsonBodyQueriesItem,
    )


T = TypeVar("T", bound="MultiQueryJsonBody")


@attr.s(auto_attribs=True)
class MultiQueryJsonBody:
    """The SQL queries to be executed

    ### Attributes:
    * `queries (List['MultiQueryJsonBodyQueriesItem'])`: None
    """

    queries: List["MultiQueryJsonBodyQueriesItem"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.multi_query_json_body_queries_item import (
            MultiQueryJsonBodyQueriesItem,
        )

        queries = []
        for queries_item_data in self.queries:
            queries_item = queries_item_data.to_dict()

            queries.append(queries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queries": queries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.multi_query_json_body_queries_item import (
            MultiQueryJsonBodyQueriesItem,
        )

        d = src_dict.copy()
        queries = []
        _queries = d.pop("queries")
        for queries_item_data in _queries:
            queries_item = MultiQueryJsonBodyQueriesItem.from_dict(queries_item_data)

            queries.append(queries_item)

        multi_query_json_body = cls(
            queries=queries,
        )

        multi_query_json_body.additional_properties = d
        return multi_query_json_body

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

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

from typing import Union
from typing import cast
from typing import Dict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_json_body_params import QueryJsonBodyParams


T = TypeVar("T", bound="QueryJsonBody")


@attr.s(auto_attribs=True)
class QueryJsonBody:
    """The SQL query to be executed

    ### Attributes:
    * `query (str)`: None
    * `params (Union[Unset, QueryJsonBodyParams])`:
    """

    query: str
    params: Union[Unset, "QueryJsonBodyParams"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.query_json_body_params import QueryJsonBodyParams

        query = self.query
        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.query_json_body_params import QueryJsonBodyParams

        d = src_dict.copy()
        query = d.pop("query")

        _params = d.pop("params", UNSET)
        params: Union[Unset, QueryJsonBodyParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = QueryJsonBodyParams.from_dict(_params)

        query_json_body = cls(
            query=query,
            params=params,
        )

        query_json_body.additional_properties = d
        return query_json_body

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

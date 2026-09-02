from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_data_metrics_response_200_metrics_item_kind import ListDataMetricsResponse200MetricsItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListDataMetricsResponse200MetricsItem")


@_attrs_define
class ListDataMetricsResponse200MetricsItem:
    """One `// measure` or `// dimension` declaration, as catalogued from the
    script that materializes the table. `expr` and `filter` are the author's
    own SQL: a reader renders a measure as `expr` plus, when `filter` is set,
    a trailing `FILTER (WHERE filter)`.

        Attributes:
            script_path (str): The declaring script, and the path reads are authorized against
            table_path (str): Canonical scheme-less DuckLake path, `<lake>/<schema>.<table>` (schema defaults to `main`)
            kind (ListDataMetricsResponse200MetricsItemKind):
            name (str):
            expr (str):
            filter_ (Union[Unset, str]): Row predicate from a measure's trailing `where`
    """

    script_path: str
    table_path: str
    kind: ListDataMetricsResponse200MetricsItemKind
    name: str
    expr: str
    filter_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        script_path = self.script_path
        table_path = self.table_path
        kind = self.kind.value

        name = self.name
        expr = self.expr
        filter_ = self.filter_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "script_path": script_path,
                "table_path": table_path,
                "kind": kind,
                "name": name,
                "expr": expr,
            }
        )
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        script_path = d.pop("script_path")

        table_path = d.pop("table_path")

        kind = ListDataMetricsResponse200MetricsItemKind(d.pop("kind"))

        name = d.pop("name")

        expr = d.pop("expr")

        filter_ = d.pop("filter", UNSET)

        list_data_metrics_response_200_metrics_item = cls(
            script_path=script_path,
            table_path=table_path,
            kind=kind,
            name=name,
            expr=expr,
            filter_=filter_,
        )

        list_data_metrics_response_200_metrics_item.additional_properties = d
        return list_data_metrics_response_200_metrics_item

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

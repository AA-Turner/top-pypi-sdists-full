from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_data_metrics_response_200_metrics_item import ListDataMetricsResponse200MetricsItem
    from ..models.list_data_metrics_response_200_next_cursor import ListDataMetricsResponse200NextCursor


T = TypeVar("T", bound="ListDataMetricsResponse200")


@_attrs_define
class ListDataMetricsResponse200:
    """
    Attributes:
        metrics (List['ListDataMetricsResponse200MetricsItem']):
        next_cursor (Union[Unset, ListDataMetricsResponse200NextCursor]): Present when more rows may follow: pass its
            fields back as the `cursor_*` params. Absent means the catalog is exhausted.
    """

    metrics: List["ListDataMetricsResponse200MetricsItem"]
    next_cursor: Union[Unset, "ListDataMetricsResponse200NextCursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.to_dict()

            metrics.append(metrics_item)

        next_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.next_cursor, Unset):
            next_cursor = self.next_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metrics": metrics,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_data_metrics_response_200_metrics_item import ListDataMetricsResponse200MetricsItem
        from ..models.list_data_metrics_response_200_next_cursor import ListDataMetricsResponse200NextCursor

        d = src_dict.copy()
        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in _metrics:
            metrics_item = ListDataMetricsResponse200MetricsItem.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        _next_cursor = d.pop("next_cursor", UNSET)
        next_cursor: Union[Unset, ListDataMetricsResponse200NextCursor]
        if isinstance(_next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = ListDataMetricsResponse200NextCursor.from_dict(_next_cursor)

        list_data_metrics_response_200 = cls(
            metrics=metrics,
            next_cursor=next_cursor,
        )

        list_data_metrics_response_200.additional_properties = d
        return list_data_metrics_response_200

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

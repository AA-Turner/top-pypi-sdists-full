from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_dbt_run_graph_response_200_test_edges_item_asset_kind import (
    GetDbtRunGraphResponse200TestEdgesItemAssetKind,
)
from ..models.get_dbt_run_graph_response_200_test_edges_item_producer_kind import (
    GetDbtRunGraphResponse200TestEdgesItemProducerKind,
)
from ..models.get_dbt_run_graph_response_200_test_edges_item_runnable_kind import (
    GetDbtRunGraphResponse200TestEdgesItemRunnableKind,
)

T = TypeVar("T", bound="GetDbtRunGraphResponse200TestEdgesItem")


@_attrs_define
class GetDbtRunGraphResponse200TestEdgesItem:
    """
    Attributes:
        producer_kind (GetDbtRunGraphResponse200TestEdgesItemProducerKind):
        producer_path (str):
        runnable_kind (GetDbtRunGraphResponse200TestEdgesItemRunnableKind):
        runnable_path (str):
        asset_kind (GetDbtRunGraphResponse200TestEdgesItemAssetKind):
        asset_path (str):
    """

    producer_kind: GetDbtRunGraphResponse200TestEdgesItemProducerKind
    producer_path: str
    runnable_kind: GetDbtRunGraphResponse200TestEdgesItemRunnableKind
    runnable_path: str
    asset_kind: GetDbtRunGraphResponse200TestEdgesItemAssetKind
    asset_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        producer_kind = self.producer_kind.value

        producer_path = self.producer_path
        runnable_kind = self.runnable_kind.value

        runnable_path = self.runnable_path
        asset_kind = self.asset_kind.value

        asset_path = self.asset_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "producer_kind": producer_kind,
                "producer_path": producer_path,
                "runnable_kind": runnable_kind,
                "runnable_path": runnable_path,
                "asset_kind": asset_kind,
                "asset_path": asset_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        producer_kind = GetDbtRunGraphResponse200TestEdgesItemProducerKind(d.pop("producer_kind"))

        producer_path = d.pop("producer_path")

        runnable_kind = GetDbtRunGraphResponse200TestEdgesItemRunnableKind(d.pop("runnable_kind"))

        runnable_path = d.pop("runnable_path")

        asset_kind = GetDbtRunGraphResponse200TestEdgesItemAssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        get_dbt_run_graph_response_200_test_edges_item = cls(
            producer_kind=producer_kind,
            producer_path=producer_path,
            runnable_kind=runnable_kind,
            runnable_path=runnable_path,
            asset_kind=asset_kind,
            asset_path=asset_path,
        )

        get_dbt_run_graph_response_200_test_edges_item.additional_properties = d
        return get_dbt_run_graph_response_200_test_edges_item

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

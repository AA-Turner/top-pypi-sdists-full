from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_dbt_run_graph_response_200_edges_item_access_type import GetDbtRunGraphResponse200EdgesItemAccessType
from ..models.get_dbt_run_graph_response_200_edges_item_asset_kind import GetDbtRunGraphResponse200EdgesItemAssetKind
from ..models.get_dbt_run_graph_response_200_edges_item_runnable_kind import (
    GetDbtRunGraphResponse200EdgesItemRunnableKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDbtRunGraphResponse200EdgesItem")


@_attrs_define
class GetDbtRunGraphResponse200EdgesItem:
    """
    Attributes:
        runnable_path (str):
        runnable_kind (GetDbtRunGraphResponse200EdgesItemRunnableKind):
        asset_kind (GetDbtRunGraphResponse200EdgesItemAssetKind):
        asset_path (str):
        access_type (Union[Unset, None, GetDbtRunGraphResponse200EdgesItemAccessType]):
    """

    runnable_path: str
    runnable_kind: GetDbtRunGraphResponse200EdgesItemRunnableKind
    asset_kind: GetDbtRunGraphResponse200EdgesItemAssetKind
    asset_path: str
    access_type: Union[Unset, None, GetDbtRunGraphResponse200EdgesItemAccessType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        runnable_path = self.runnable_path
        runnable_kind = self.runnable_kind.value

        asset_kind = self.asset_kind.value

        asset_path = self.asset_path
        access_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.access_type, Unset):
            access_type = self.access_type.value if self.access_type else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runnable_path": runnable_path,
                "runnable_kind": runnable_kind,
                "asset_kind": asset_kind,
                "asset_path": asset_path,
            }
        )
        if access_type is not UNSET:
            field_dict["access_type"] = access_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        runnable_path = d.pop("runnable_path")

        runnable_kind = GetDbtRunGraphResponse200EdgesItemRunnableKind(d.pop("runnable_kind"))

        asset_kind = GetDbtRunGraphResponse200EdgesItemAssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        _access_type = d.pop("access_type", UNSET)
        access_type: Union[Unset, None, GetDbtRunGraphResponse200EdgesItemAccessType]
        if _access_type is None:
            access_type = None
        elif isinstance(_access_type, Unset):
            access_type = UNSET
        else:
            access_type = GetDbtRunGraphResponse200EdgesItemAccessType(_access_type)

        get_dbt_run_graph_response_200_edges_item = cls(
            runnable_path=runnable_path,
            runnable_kind=runnable_kind,
            asset_kind=asset_kind,
            asset_path=asset_path,
            access_type=access_type,
        )

        get_dbt_run_graph_response_200_edges_item.additional_properties = d
        return get_dbt_run_graph_response_200_edges_item

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

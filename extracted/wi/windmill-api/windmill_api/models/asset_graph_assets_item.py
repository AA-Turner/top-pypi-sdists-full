from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_graph_assets_item_fork_materialization import AssetGraphAssetsItemForkMaterialization
from ..models.asset_graph_assets_item_kind import AssetGraphAssetsItemKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_graph_assets_item_dbt import AssetGraphAssetsItemDbt


T = TypeVar("T", bound="AssetGraphAssetsItem")


@_attrs_define
class AssetGraphAssetsItem:
    """
    Attributes:
        kind (AssetGraphAssetsItemKind):
        path (str):
        fork_materialization (Union[Unset, AssetGraphAssetsItemForkMaterialization]): Fork workspaces only — 'fork' when
            this ducklake asset was materialized in the fork itself, 'deferred' when reads fall back to the parent
            workspace's current table via a defer view. Omitted otherwise.
        dbt (Union[Unset, AssetGraphAssetsItemDbt]): What dbt says about the model, snapshot, seed or source that
            produces (or, for a source, is read at) this relation. A dbt project is one runnable node with many model
            assets, so per-model metadata belongs here rather than on the script.
    """

    kind: AssetGraphAssetsItemKind
    path: str
    fork_materialization: Union[Unset, AssetGraphAssetsItemForkMaterialization] = UNSET
    dbt: Union[Unset, "AssetGraphAssetsItemDbt"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        fork_materialization: Union[Unset, str] = UNSET
        if not isinstance(self.fork_materialization, Unset):
            fork_materialization = self.fork_materialization.value

        dbt: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dbt, Unset):
            dbt = self.dbt.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
            }
        )
        if fork_materialization is not UNSET:
            field_dict["fork_materialization"] = fork_materialization
        if dbt is not UNSET:
            field_dict["dbt"] = dbt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.asset_graph_assets_item_dbt import AssetGraphAssetsItemDbt

        d = src_dict.copy()
        kind = AssetGraphAssetsItemKind(d.pop("kind"))

        path = d.pop("path")

        _fork_materialization = d.pop("fork_materialization", UNSET)
        fork_materialization: Union[Unset, AssetGraphAssetsItemForkMaterialization]
        if isinstance(_fork_materialization, Unset):
            fork_materialization = UNSET
        else:
            fork_materialization = AssetGraphAssetsItemForkMaterialization(_fork_materialization)

        _dbt = d.pop("dbt", UNSET)
        dbt: Union[Unset, AssetGraphAssetsItemDbt]
        if isinstance(_dbt, Unset):
            dbt = UNSET
        else:
            dbt = AssetGraphAssetsItemDbt.from_dict(_dbt)

        asset_graph_assets_item = cls(
            kind=kind,
            path=path,
            fork_materialization=fork_materialization,
            dbt=dbt,
        )

        asset_graph_assets_item.additional_properties = d
        return asset_graph_assets_item

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

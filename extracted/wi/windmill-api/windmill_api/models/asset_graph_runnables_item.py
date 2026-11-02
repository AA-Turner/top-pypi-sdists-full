from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_graph_runnables_item_usage_kind import AssetGraphRunnablesItemUsageKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_graph_runnables_item_dbt import AssetGraphRunnablesItemDbt
    from ..models.asset_graph_runnables_item_macros_item import AssetGraphRunnablesItemMacrosItem


T = TypeVar("T", bound="AssetGraphRunnablesItem")


@_attrs_define
class AssetGraphRunnablesItem:
    """
    Attributes:
        path (str):
        usage_kind (AssetGraphRunnablesItemUsageKind):
        in_pipeline (Union[Unset, bool]): True iff the script is a pipeline member (deployed with `// pipeline`).
            Omitted when false.
        macros (Union[Unset, List['AssetGraphRunnablesItemMacrosItem']]): Macros this script provides to the workspace
            registry (deployed `// macros` library). Omitted when empty.
        dbt (Union[Unset, AssetGraphRunnablesItemDbt]): Set on a `dbt` script, which owns a whole project rather than a
            single output. Omitted otherwise.
    """

    path: str
    usage_kind: AssetGraphRunnablesItemUsageKind
    in_pipeline: Union[Unset, bool] = UNSET
    macros: Union[Unset, List["AssetGraphRunnablesItemMacrosItem"]] = UNSET
    dbt: Union[Unset, "AssetGraphRunnablesItemDbt"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        usage_kind = self.usage_kind.value

        in_pipeline = self.in_pipeline
        macros: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.macros, Unset):
            macros = []
            for macros_item_data in self.macros:
                macros_item = macros_item_data.to_dict()

                macros.append(macros_item)

        dbt: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dbt, Unset):
            dbt = self.dbt.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "usage_kind": usage_kind,
            }
        )
        if in_pipeline is not UNSET:
            field_dict["in_pipeline"] = in_pipeline
        if macros is not UNSET:
            field_dict["macros"] = macros
        if dbt is not UNSET:
            field_dict["dbt"] = dbt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.asset_graph_runnables_item_dbt import AssetGraphRunnablesItemDbt
        from ..models.asset_graph_runnables_item_macros_item import AssetGraphRunnablesItemMacrosItem

        d = src_dict.copy()
        path = d.pop("path")

        usage_kind = AssetGraphRunnablesItemUsageKind(d.pop("usage_kind"))

        in_pipeline = d.pop("in_pipeline", UNSET)

        macros = []
        _macros = d.pop("macros", UNSET)
        for macros_item_data in _macros or []:
            macros_item = AssetGraphRunnablesItemMacrosItem.from_dict(macros_item_data)

            macros.append(macros_item)

        _dbt = d.pop("dbt", UNSET)
        dbt: Union[Unset, AssetGraphRunnablesItemDbt]
        if isinstance(_dbt, Unset):
            dbt = UNSET
        else:
            dbt = AssetGraphRunnablesItemDbt.from_dict(_dbt)

        asset_graph_runnables_item = cls(
            path=path,
            usage_kind=usage_kind,
            in_pipeline=in_pipeline,
            macros=macros,
            dbt=dbt,
        )

        asset_graph_runnables_item.additional_properties = d
        return asset_graph_runnables_item

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

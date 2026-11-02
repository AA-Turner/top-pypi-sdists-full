import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_graph_assets_item import AssetGraphAssetsItem
    from ..models.asset_graph_dbt_edges_item import AssetGraphDbtEdgesItem
    from ..models.asset_graph_edges_item import AssetGraphEdgesItem
    from ..models.asset_graph_macro_edges_item import AssetGraphMacroEdgesItem
    from ..models.asset_graph_runnables_item import AssetGraphRunnablesItem
    from ..models.asset_graph_test_edges_item import AssetGraphTestEdgesItem
    from ..models.asset_graph_triggers_item_type_0 import AssetGraphTriggersItemType0
    from ..models.asset_graph_triggers_item_type_1 import AssetGraphTriggersItemType1


T = TypeVar("T", bound="AssetGraph")


@_attrs_define
class AssetGraph:
    """
    Attributes:
        assets (List['AssetGraphAssetsItem']):
        runnables (List['AssetGraphRunnablesItem']):
        edges (List['AssetGraphEdgesItem']):
        triggers (List[Union['AssetGraphTriggersItemType0', 'AssetGraphTriggersItemType1']]):
        macro_edges (Union[Unset, List['AssetGraphMacroEdgesItem']]): Macro-library → consumer edges (deploy-recorded
            call detection plus `// use`). Omitted when empty.
        test_edges (Union[Unset, List['AssetGraphTestEdgesItem']]): Ordering-only "must-run-after" edges — a `//
            data_test relationships` (or custom test reading a pipeline asset) requires the referenced asset's producer to
            run before the tested script. Not a data-consumption edge; fed into the cascade topo-sort so cold runs order
            correctly. Omitted when empty.
        dbt_edges (Union[Unset, List['AssetGraphDbtEdgesItem']]): `ref()` lineage BETWEEN two dbt models, in the terms
            the canvas draws — the relations, not dbt's node ids. Without it every model hangs off the one dbt runnable and
            the project reads as a flat fan-out. Omitted when empty.
        dbt_snapshot_job (Union[Unset, str]): The job whose own snapshot the dbt half was resolved from, when one was
            asked for and found. A run page polls the graph while its job runs, because a dynamic descriptor's snapshot is
            written mid-run, and this is what tells it to stop. Omitted when the answer came from the version's deployed
            graph.
        dbt_graph_ingested_at (Union[Unset, datetime.datetime]): When the dbt half on screen was parsed, for a graph
            pinned to a job. What the dbt editor labels its provenance with — "parsed from the editor at 14:32" against "as
            of last deploy" — since the two are drawn identically and the ambiguity would otherwise just move into the
            editor. Omitted for the unpinned workspace graph, which spans every project and so has no one time.
    """

    assets: List["AssetGraphAssetsItem"]
    runnables: List["AssetGraphRunnablesItem"]
    edges: List["AssetGraphEdgesItem"]
    triggers: List[Union["AssetGraphTriggersItemType0", "AssetGraphTriggersItemType1"]]
    macro_edges: Union[Unset, List["AssetGraphMacroEdgesItem"]] = UNSET
    test_edges: Union[Unset, List["AssetGraphTestEdgesItem"]] = UNSET
    dbt_edges: Union[Unset, List["AssetGraphDbtEdgesItem"]] = UNSET
    dbt_snapshot_job: Union[Unset, str] = UNSET
    dbt_graph_ingested_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.asset_graph_triggers_item_type_0 import AssetGraphTriggersItemType0

        assets = []
        for assets_item_data in self.assets:
            assets_item = assets_item_data.to_dict()

            assets.append(assets_item)

        runnables = []
        for runnables_item_data in self.runnables:
            runnables_item = runnables_item_data.to_dict()

            runnables.append(runnables_item)

        edges = []
        for edges_item_data in self.edges:
            edges_item = edges_item_data.to_dict()

            edges.append(edges_item)

        triggers = []
        for triggers_item_data in self.triggers:
            triggers_item: Dict[str, Any]

            if isinstance(triggers_item_data, AssetGraphTriggersItemType0):
                triggers_item = triggers_item_data.to_dict()

            else:
                triggers_item = triggers_item_data.to_dict()

            triggers.append(triggers_item)

        macro_edges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.macro_edges, Unset):
            macro_edges = []
            for macro_edges_item_data in self.macro_edges:
                macro_edges_item = macro_edges_item_data.to_dict()

                macro_edges.append(macro_edges_item)

        test_edges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.test_edges, Unset):
            test_edges = []
            for test_edges_item_data in self.test_edges:
                test_edges_item = test_edges_item_data.to_dict()

                test_edges.append(test_edges_item)

        dbt_edges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dbt_edges, Unset):
            dbt_edges = []
            for dbt_edges_item_data in self.dbt_edges:
                dbt_edges_item = dbt_edges_item_data.to_dict()

                dbt_edges.append(dbt_edges_item)

        dbt_snapshot_job = self.dbt_snapshot_job
        dbt_graph_ingested_at: Union[Unset, str] = UNSET
        if not isinstance(self.dbt_graph_ingested_at, Unset):
            dbt_graph_ingested_at = self.dbt_graph_ingested_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assets": assets,
                "runnables": runnables,
                "edges": edges,
                "triggers": triggers,
            }
        )
        if macro_edges is not UNSET:
            field_dict["macro_edges"] = macro_edges
        if test_edges is not UNSET:
            field_dict["test_edges"] = test_edges
        if dbt_edges is not UNSET:
            field_dict["dbt_edges"] = dbt_edges
        if dbt_snapshot_job is not UNSET:
            field_dict["dbt_snapshot_job"] = dbt_snapshot_job
        if dbt_graph_ingested_at is not UNSET:
            field_dict["dbt_graph_ingested_at"] = dbt_graph_ingested_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.asset_graph_assets_item import AssetGraphAssetsItem
        from ..models.asset_graph_dbt_edges_item import AssetGraphDbtEdgesItem
        from ..models.asset_graph_edges_item import AssetGraphEdgesItem
        from ..models.asset_graph_macro_edges_item import AssetGraphMacroEdgesItem
        from ..models.asset_graph_runnables_item import AssetGraphRunnablesItem
        from ..models.asset_graph_test_edges_item import AssetGraphTestEdgesItem
        from ..models.asset_graph_triggers_item_type_0 import AssetGraphTriggersItemType0
        from ..models.asset_graph_triggers_item_type_1 import AssetGraphTriggersItemType1

        d = src_dict.copy()
        assets = []
        _assets = d.pop("assets")
        for assets_item_data in _assets:
            assets_item = AssetGraphAssetsItem.from_dict(assets_item_data)

            assets.append(assets_item)

        runnables = []
        _runnables = d.pop("runnables")
        for runnables_item_data in _runnables:
            runnables_item = AssetGraphRunnablesItem.from_dict(runnables_item_data)

            runnables.append(runnables_item)

        edges = []
        _edges = d.pop("edges")
        for edges_item_data in _edges:
            edges_item = AssetGraphEdgesItem.from_dict(edges_item_data)

            edges.append(edges_item)

        triggers = []
        _triggers = d.pop("triggers")
        for triggers_item_data in _triggers:

            def _parse_triggers_item(
                data: object,
            ) -> Union["AssetGraphTriggersItemType0", "AssetGraphTriggersItemType1"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    triggers_item_type_0 = AssetGraphTriggersItemType0.from_dict(data)

                    return triggers_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                triggers_item_type_1 = AssetGraphTriggersItemType1.from_dict(data)

                return triggers_item_type_1

            triggers_item = _parse_triggers_item(triggers_item_data)

            triggers.append(triggers_item)

        macro_edges = []
        _macro_edges = d.pop("macro_edges", UNSET)
        for macro_edges_item_data in _macro_edges or []:
            macro_edges_item = AssetGraphMacroEdgesItem.from_dict(macro_edges_item_data)

            macro_edges.append(macro_edges_item)

        test_edges = []
        _test_edges = d.pop("test_edges", UNSET)
        for test_edges_item_data in _test_edges or []:
            test_edges_item = AssetGraphTestEdgesItem.from_dict(test_edges_item_data)

            test_edges.append(test_edges_item)

        dbt_edges = []
        _dbt_edges = d.pop("dbt_edges", UNSET)
        for dbt_edges_item_data in _dbt_edges or []:
            dbt_edges_item = AssetGraphDbtEdgesItem.from_dict(dbt_edges_item_data)

            dbt_edges.append(dbt_edges_item)

        dbt_snapshot_job = d.pop("dbt_snapshot_job", UNSET)

        _dbt_graph_ingested_at = d.pop("dbt_graph_ingested_at", UNSET)
        dbt_graph_ingested_at: Union[Unset, datetime.datetime]
        if isinstance(_dbt_graph_ingested_at, Unset):
            dbt_graph_ingested_at = UNSET
        else:
            dbt_graph_ingested_at = isoparse(_dbt_graph_ingested_at)

        asset_graph = cls(
            assets=assets,
            runnables=runnables,
            edges=edges,
            triggers=triggers,
            macro_edges=macro_edges,
            test_edges=test_edges,
            dbt_edges=dbt_edges,
            dbt_snapshot_job=dbt_snapshot_job,
            dbt_graph_ingested_at=dbt_graph_ingested_at,
        )

        asset_graph.additional_properties = d
        return asset_graph

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

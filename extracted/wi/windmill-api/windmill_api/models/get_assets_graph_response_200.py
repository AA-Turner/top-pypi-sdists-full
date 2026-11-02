import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_assets_graph_response_200_assets_item import GetAssetsGraphResponse200AssetsItem
    from ..models.get_assets_graph_response_200_dbt_edges_item import GetAssetsGraphResponse200DbtEdgesItem
    from ..models.get_assets_graph_response_200_edges_item import GetAssetsGraphResponse200EdgesItem
    from ..models.get_assets_graph_response_200_macro_edges_item import GetAssetsGraphResponse200MacroEdgesItem
    from ..models.get_assets_graph_response_200_runnables_item import GetAssetsGraphResponse200RunnablesItem
    from ..models.get_assets_graph_response_200_test_edges_item import GetAssetsGraphResponse200TestEdgesItem
    from ..models.get_assets_graph_response_200_triggers_item_type_0 import GetAssetsGraphResponse200TriggersItemType0
    from ..models.get_assets_graph_response_200_triggers_item_type_1 import GetAssetsGraphResponse200TriggersItemType1


T = TypeVar("T", bound="GetAssetsGraphResponse200")


@_attrs_define
class GetAssetsGraphResponse200:
    """
    Attributes:
        assets (List['GetAssetsGraphResponse200AssetsItem']):
        runnables (List['GetAssetsGraphResponse200RunnablesItem']):
        edges (List['GetAssetsGraphResponse200EdgesItem']):
        triggers (List[Union['GetAssetsGraphResponse200TriggersItemType0',
            'GetAssetsGraphResponse200TriggersItemType1']]):
        macro_edges (Union[Unset, List['GetAssetsGraphResponse200MacroEdgesItem']]): Macro-library → consumer edges
            (deploy-recorded call detection plus `// use`). Omitted when empty.
        test_edges (Union[Unset, List['GetAssetsGraphResponse200TestEdgesItem']]): Ordering-only "must-run-after" edges
            — a `// data_test relationships` (or custom test reading a pipeline asset) requires the referenced asset's
            producer to run before the tested script. Not a data-consumption edge; fed into the cascade topo-sort so cold
            runs order correctly. Omitted when empty.
        dbt_edges (Union[Unset, List['GetAssetsGraphResponse200DbtEdgesItem']]): `ref()` lineage BETWEEN two dbt models,
            in the terms the canvas draws — the relations, not dbt's node ids. Without it every model hangs off the one dbt
            runnable and the project reads as a flat fan-out. Omitted when empty.
        dbt_snapshot_job (Union[Unset, str]): The job whose own snapshot the dbt half was resolved from, when one was
            asked for and found. A run page polls the graph while its job runs, because a dynamic descriptor's snapshot is
            written mid-run, and this is what tells it to stop. Omitted when the answer came from the version's deployed
            graph.
        dbt_graph_ingested_at (Union[Unset, datetime.datetime]): When the dbt half on screen was parsed, for a graph
            pinned to a job. What the dbt editor labels its provenance with — "parsed from the editor at 14:32" against "as
            of last deploy" — since the two are drawn identically and the ambiguity would otherwise just move into the
            editor. Omitted for the unpinned workspace graph, which spans every project and so has no one time.
    """

    assets: List["GetAssetsGraphResponse200AssetsItem"]
    runnables: List["GetAssetsGraphResponse200RunnablesItem"]
    edges: List["GetAssetsGraphResponse200EdgesItem"]
    triggers: List[Union["GetAssetsGraphResponse200TriggersItemType0", "GetAssetsGraphResponse200TriggersItemType1"]]
    macro_edges: Union[Unset, List["GetAssetsGraphResponse200MacroEdgesItem"]] = UNSET
    test_edges: Union[Unset, List["GetAssetsGraphResponse200TestEdgesItem"]] = UNSET
    dbt_edges: Union[Unset, List["GetAssetsGraphResponse200DbtEdgesItem"]] = UNSET
    dbt_snapshot_job: Union[Unset, str] = UNSET
    dbt_graph_ingested_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_assets_graph_response_200_triggers_item_type_0 import (
            GetAssetsGraphResponse200TriggersItemType0,
        )

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

            if isinstance(triggers_item_data, GetAssetsGraphResponse200TriggersItemType0):
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
        from ..models.get_assets_graph_response_200_assets_item import GetAssetsGraphResponse200AssetsItem
        from ..models.get_assets_graph_response_200_dbt_edges_item import GetAssetsGraphResponse200DbtEdgesItem
        from ..models.get_assets_graph_response_200_edges_item import GetAssetsGraphResponse200EdgesItem
        from ..models.get_assets_graph_response_200_macro_edges_item import GetAssetsGraphResponse200MacroEdgesItem
        from ..models.get_assets_graph_response_200_runnables_item import GetAssetsGraphResponse200RunnablesItem
        from ..models.get_assets_graph_response_200_test_edges_item import GetAssetsGraphResponse200TestEdgesItem
        from ..models.get_assets_graph_response_200_triggers_item_type_0 import (
            GetAssetsGraphResponse200TriggersItemType0,
        )
        from ..models.get_assets_graph_response_200_triggers_item_type_1 import (
            GetAssetsGraphResponse200TriggersItemType1,
        )

        d = src_dict.copy()
        assets = []
        _assets = d.pop("assets")
        for assets_item_data in _assets:
            assets_item = GetAssetsGraphResponse200AssetsItem.from_dict(assets_item_data)

            assets.append(assets_item)

        runnables = []
        _runnables = d.pop("runnables")
        for runnables_item_data in _runnables:
            runnables_item = GetAssetsGraphResponse200RunnablesItem.from_dict(runnables_item_data)

            runnables.append(runnables_item)

        edges = []
        _edges = d.pop("edges")
        for edges_item_data in _edges:
            edges_item = GetAssetsGraphResponse200EdgesItem.from_dict(edges_item_data)

            edges.append(edges_item)

        triggers = []
        _triggers = d.pop("triggers")
        for triggers_item_data in _triggers:

            def _parse_triggers_item(
                data: object,
            ) -> Union["GetAssetsGraphResponse200TriggersItemType0", "GetAssetsGraphResponse200TriggersItemType1"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    triggers_item_type_0 = GetAssetsGraphResponse200TriggersItemType0.from_dict(data)

                    return triggers_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                triggers_item_type_1 = GetAssetsGraphResponse200TriggersItemType1.from_dict(data)

                return triggers_item_type_1

            triggers_item = _parse_triggers_item(triggers_item_data)

            triggers.append(triggers_item)

        macro_edges = []
        _macro_edges = d.pop("macro_edges", UNSET)
        for macro_edges_item_data in _macro_edges or []:
            macro_edges_item = GetAssetsGraphResponse200MacroEdgesItem.from_dict(macro_edges_item_data)

            macro_edges.append(macro_edges_item)

        test_edges = []
        _test_edges = d.pop("test_edges", UNSET)
        for test_edges_item_data in _test_edges or []:
            test_edges_item = GetAssetsGraphResponse200TestEdgesItem.from_dict(test_edges_item_data)

            test_edges.append(test_edges_item)

        dbt_edges = []
        _dbt_edges = d.pop("dbt_edges", UNSET)
        for dbt_edges_item_data in _dbt_edges or []:
            dbt_edges_item = GetAssetsGraphResponse200DbtEdgesItem.from_dict(dbt_edges_item_data)

            dbt_edges.append(dbt_edges_item)

        dbt_snapshot_job = d.pop("dbt_snapshot_job", UNSET)

        _dbt_graph_ingested_at = d.pop("dbt_graph_ingested_at", UNSET)
        dbt_graph_ingested_at: Union[Unset, datetime.datetime]
        if isinstance(_dbt_graph_ingested_at, Unset):
            dbt_graph_ingested_at = UNSET
        else:
            dbt_graph_ingested_at = isoparse(_dbt_graph_ingested_at)

        get_assets_graph_response_200 = cls(
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

        get_assets_graph_response_200.additional_properties = d
        return get_assets_graph_response_200

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

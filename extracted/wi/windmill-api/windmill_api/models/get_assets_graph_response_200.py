from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_assets_graph_response_200_assets_item import GetAssetsGraphResponse200AssetsItem
    from ..models.get_assets_graph_response_200_edges_item import GetAssetsGraphResponse200EdgesItem
    from ..models.get_assets_graph_response_200_runnables_item import GetAssetsGraphResponse200RunnablesItem
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
    """

    assets: List["GetAssetsGraphResponse200AssetsItem"]
    runnables: List["GetAssetsGraphResponse200RunnablesItem"]
    edges: List["GetAssetsGraphResponse200EdgesItem"]
    triggers: List[Union["GetAssetsGraphResponse200TriggersItemType0", "GetAssetsGraphResponse200TriggersItemType1"]]
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_assets_graph_response_200_assets_item import GetAssetsGraphResponse200AssetsItem
        from ..models.get_assets_graph_response_200_edges_item import GetAssetsGraphResponse200EdgesItem
        from ..models.get_assets_graph_response_200_runnables_item import GetAssetsGraphResponse200RunnablesItem
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

        get_assets_graph_response_200 = cls(
            assets=assets,
            runnables=runnables,
            edges=edges,
            triggers=triggers,
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

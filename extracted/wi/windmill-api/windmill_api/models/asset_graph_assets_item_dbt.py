from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_graph_assets_item_dbt_resource_type import AssetGraphAssetsItemDbtResourceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_graph_assets_item_dbt_columns import AssetGraphAssetsItemDbtColumns
    from ..models.asset_graph_assets_item_dbt_data_tests_item import AssetGraphAssetsItemDbtDataTestsItem
    from ..models.asset_graph_assets_item_dbt_freshness import AssetGraphAssetsItemDbtFreshness


T = TypeVar("T", bound="AssetGraphAssetsItemDbt")


@_attrs_define
class AssetGraphAssetsItemDbt:
    """What dbt says about the model, snapshot, seed or source that produces (or, for a source, is read at) this relation.
    A dbt project is one runnable node with many model assets, so per-model metadata belongs here rather than on the
    script.

        Attributes:
            unique_id (str): dbt's own node id, e.g. `model.jaffle_shop.customers`.
            resource_type (AssetGraphAssetsItemDbtResourceType):
            materialized (Union[Unset, str]): dbt's own word (`table`, `view`, `incremental`, `snapshot`).
            materialize_strategy (Union[Unset, str]): The Windmill write strategy it maps to, absent for `view` and
                `ephemeral`, which have none.
            tags (Union[Unset, List[str]]):
            description (Union[Unset, str]):
            data_tests (Union[Unset, List['AssetGraphAssetsItemDbtDataTestsItem']]):
            columns (Union[Unset, AssetGraphAssetsItemDbtColumns]): Declared column metadata (name -> description). NOT
                column lineage — `manifest.json` carries none.
            freshness (Union[Unset, AssetGraphAssetsItemDbtFreshness]): A source's declared freshness policy, for the
                staleness chip.
            raw_code (Union[Unset, str]): The model's SQL as written, at the deploy this graph belongs to. Omitted when the
                caller cannot read the script.
            original_file_path (Union[Unset, str]): Its path inside the dbt project, e.g. `models/staging/stg_orders.sql`.
    """

    unique_id: str
    resource_type: AssetGraphAssetsItemDbtResourceType
    materialized: Union[Unset, str] = UNSET
    materialize_strategy: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    description: Union[Unset, str] = UNSET
    data_tests: Union[Unset, List["AssetGraphAssetsItemDbtDataTestsItem"]] = UNSET
    columns: Union[Unset, "AssetGraphAssetsItemDbtColumns"] = UNSET
    freshness: Union[Unset, "AssetGraphAssetsItemDbtFreshness"] = UNSET
    raw_code: Union[Unset, str] = UNSET
    original_file_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unique_id = self.unique_id
        resource_type = self.resource_type.value

        materialized = self.materialized
        materialize_strategy = self.materialize_strategy
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        description = self.description
        data_tests: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data_tests, Unset):
            data_tests = []
            for data_tests_item_data in self.data_tests:
                data_tests_item = data_tests_item_data.to_dict()

                data_tests.append(data_tests_item)

        columns: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = self.columns.to_dict()

        freshness: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.freshness, Unset):
            freshness = self.freshness.to_dict()

        raw_code = self.raw_code
        original_file_path = self.original_file_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unique_id": unique_id,
                "resource_type": resource_type,
            }
        )
        if materialized is not UNSET:
            field_dict["materialized"] = materialized
        if materialize_strategy is not UNSET:
            field_dict["materialize_strategy"] = materialize_strategy
        if tags is not UNSET:
            field_dict["tags"] = tags
        if description is not UNSET:
            field_dict["description"] = description
        if data_tests is not UNSET:
            field_dict["data_tests"] = data_tests
        if columns is not UNSET:
            field_dict["columns"] = columns
        if freshness is not UNSET:
            field_dict["freshness"] = freshness
        if raw_code is not UNSET:
            field_dict["raw_code"] = raw_code
        if original_file_path is not UNSET:
            field_dict["original_file_path"] = original_file_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.asset_graph_assets_item_dbt_columns import AssetGraphAssetsItemDbtColumns
        from ..models.asset_graph_assets_item_dbt_data_tests_item import AssetGraphAssetsItemDbtDataTestsItem
        from ..models.asset_graph_assets_item_dbt_freshness import AssetGraphAssetsItemDbtFreshness

        d = src_dict.copy()
        unique_id = d.pop("unique_id")

        resource_type = AssetGraphAssetsItemDbtResourceType(d.pop("resource_type"))

        materialized = d.pop("materialized", UNSET)

        materialize_strategy = d.pop("materialize_strategy", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        description = d.pop("description", UNSET)

        data_tests = []
        _data_tests = d.pop("data_tests", UNSET)
        for data_tests_item_data in _data_tests or []:
            data_tests_item = AssetGraphAssetsItemDbtDataTestsItem.from_dict(data_tests_item_data)

            data_tests.append(data_tests_item)

        _columns = d.pop("columns", UNSET)
        columns: Union[Unset, AssetGraphAssetsItemDbtColumns]
        if isinstance(_columns, Unset):
            columns = UNSET
        else:
            columns = AssetGraphAssetsItemDbtColumns.from_dict(_columns)

        _freshness = d.pop("freshness", UNSET)
        freshness: Union[Unset, AssetGraphAssetsItemDbtFreshness]
        if isinstance(_freshness, Unset):
            freshness = UNSET
        else:
            freshness = AssetGraphAssetsItemDbtFreshness.from_dict(_freshness)

        raw_code = d.pop("raw_code", UNSET)

        original_file_path = d.pop("original_file_path", UNSET)

        asset_graph_assets_item_dbt = cls(
            unique_id=unique_id,
            resource_type=resource_type,
            materialized=materialized,
            materialize_strategy=materialize_strategy,
            tags=tags,
            description=description,
            data_tests=data_tests,
            columns=columns,
            freshness=freshness,
            raw_code=raw_code,
            original_file_path=original_file_path,
        )

        asset_graph_assets_item_dbt.additional_properties = d
        return asset_graph_assets_item_dbt

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

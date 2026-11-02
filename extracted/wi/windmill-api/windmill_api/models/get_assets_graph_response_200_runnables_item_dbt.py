from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetAssetsGraphResponse200RunnablesItemDbt")


@_attrs_define
class GetAssetsGraphResponse200RunnablesItemDbt:
    """Set on a `dbt` script, which owns a whole project rather than a single output. Omitted otherwise.

    Attributes:
        model_count (int):
    """

    model_count: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        model_count = self.model_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_count": model_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_count = d.pop("model_count")

        get_assets_graph_response_200_runnables_item_dbt = cls(
            model_count=model_count,
        )

        get_assets_graph_response_200_runnables_item_dbt.additional_properties = d
        return get_assets_graph_response_200_runnables_item_dbt

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

from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_assets_graph_response_200_runnables_item_usage_kind import (
    GetAssetsGraphResponse200RunnablesItemUsageKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAssetsGraphResponse200RunnablesItem")


@_attrs_define
class GetAssetsGraphResponse200RunnablesItem:
    """
    Attributes:
        path (str):
        usage_kind (GetAssetsGraphResponse200RunnablesItemUsageKind):
        in_pipeline (Union[Unset, bool]): True iff the script is a pipeline member (deployed with `// pipeline`).
            Omitted when false.
    """

    path: str
    usage_kind: GetAssetsGraphResponse200RunnablesItemUsageKind
    in_pipeline: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        usage_kind = self.usage_kind.value

        in_pipeline = self.in_pipeline

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        usage_kind = GetAssetsGraphResponse200RunnablesItemUsageKind(d.pop("usage_kind"))

        in_pipeline = d.pop("in_pipeline", UNSET)

        get_assets_graph_response_200_runnables_item = cls(
            path=path,
            usage_kind=usage_kind,
            in_pipeline=in_pipeline,
        )

        get_assets_graph_response_200_runnables_item.additional_properties = d
        return get_assets_graph_response_200_runnables_item

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

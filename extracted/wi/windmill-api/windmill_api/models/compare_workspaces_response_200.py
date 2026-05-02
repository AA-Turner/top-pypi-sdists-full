from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.compare_workspaces_response_200_diffs_item import CompareWorkspacesResponse200DiffsItem
    from ..models.compare_workspaces_response_200_summary import CompareWorkspacesResponse200Summary


T = TypeVar("T", bound="CompareWorkspacesResponse200")


@_attrs_define
class CompareWorkspacesResponse200:
    """
    Attributes:
        all_ahead_items_visible (bool): All items with changes ahead are visible by the user of the request.
        all_behind_items_visible (bool): All items with changes behind are visible by the user of the request.
        skipped_comparison (bool): Whether the comparison was skipped. This happens with old forks that where not being
            kept track of
        diffs (List['CompareWorkspacesResponse200DiffsItem']): List of differences found between workspaces
        summary (CompareWorkspacesResponse200Summary): Summary statistics of the comparison
    """

    all_ahead_items_visible: bool
    all_behind_items_visible: bool
    skipped_comparison: bool
    diffs: List["CompareWorkspacesResponse200DiffsItem"]
    summary: "CompareWorkspacesResponse200Summary"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        all_ahead_items_visible = self.all_ahead_items_visible
        all_behind_items_visible = self.all_behind_items_visible
        skipped_comparison = self.skipped_comparison
        diffs = []
        for diffs_item_data in self.diffs:
            diffs_item = diffs_item_data.to_dict()

            diffs.append(diffs_item)

        summary = self.summary.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "all_ahead_items_visible": all_ahead_items_visible,
                "all_behind_items_visible": all_behind_items_visible,
                "skipped_comparison": skipped_comparison,
                "diffs": diffs,
                "summary": summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.compare_workspaces_response_200_diffs_item import CompareWorkspacesResponse200DiffsItem
        from ..models.compare_workspaces_response_200_summary import CompareWorkspacesResponse200Summary

        d = src_dict.copy()
        all_ahead_items_visible = d.pop("all_ahead_items_visible")

        all_behind_items_visible = d.pop("all_behind_items_visible")

        skipped_comparison = d.pop("skipped_comparison")

        diffs = []
        _diffs = d.pop("diffs")
        for diffs_item_data in _diffs:
            diffs_item = CompareWorkspacesResponse200DiffsItem.from_dict(diffs_item_data)

            diffs.append(diffs_item)

        summary = CompareWorkspacesResponse200Summary.from_dict(d.pop("summary"))

        compare_workspaces_response_200 = cls(
            all_ahead_items_visible=all_ahead_items_visible,
            all_behind_items_visible=all_behind_items_visible,
            skipped_comparison=skipped_comparison,
            diffs=diffs,
            summary=summary,
        )

        compare_workspaces_response_200.additional_properties = d
        return compare_workspaces_response_200

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

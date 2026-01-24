from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_item_diff_kind import WorkspaceItemDiffKind

T = TypeVar("T", bound="WorkspaceItemDiff")


@_attrs_define
class WorkspaceItemDiff:
    """
    Attributes:
        kind (WorkspaceItemDiffKind): Type of the item
        path (str): Path of the item in the workspace
        ahead (int): Number of versions source is ahead of target
        behind (int): Number of versions source is behind target
        has_changes (bool): Whether the item has any differences
        exists_in_source (bool): If the item exists in the source workspace
        exists_in_fork (bool): If the item exists in the fork workspace
    """

    kind: WorkspaceItemDiffKind
    path: str
    ahead: int
    behind: int
    has_changes: bool
    exists_in_source: bool
    exists_in_fork: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        ahead = self.ahead
        behind = self.behind
        has_changes = self.has_changes
        exists_in_source = self.exists_in_source
        exists_in_fork = self.exists_in_fork

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
                "ahead": ahead,
                "behind": behind,
                "has_changes": has_changes,
                "exists_in_source": exists_in_source,
                "exists_in_fork": exists_in_fork,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = WorkspaceItemDiffKind(d.pop("kind"))

        path = d.pop("path")

        ahead = d.pop("ahead")

        behind = d.pop("behind")

        has_changes = d.pop("has_changes")

        exists_in_source = d.pop("exists_in_source")

        exists_in_fork = d.pop("exists_in_fork")

        workspace_item_diff = cls(
            kind=kind,
            path=path,
            ahead=ahead,
            behind=behind,
            has_changes=has_changes,
            exists_in_source=exists_in_source,
            exists_in_fork=exists_in_fork,
        )

        workspace_item_diff.additional_properties = d
        return workspace_item_diff

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

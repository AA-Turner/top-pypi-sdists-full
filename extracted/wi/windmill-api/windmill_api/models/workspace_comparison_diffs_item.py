from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_comparison_diffs_item_fork_last_event_kind import WorkspaceComparisonDiffsItemForkLastEventKind
from ..models.workspace_comparison_diffs_item_fork_last_event_origin import (
    WorkspaceComparisonDiffsItemForkLastEventOrigin,
)
from ..models.workspace_comparison_diffs_item_kind import WorkspaceComparisonDiffsItemKind
from ..models.workspace_comparison_diffs_item_source_last_event_kind import (
    WorkspaceComparisonDiffsItemSourceLastEventKind,
)
from ..models.workspace_comparison_diffs_item_source_last_event_origin import (
    WorkspaceComparisonDiffsItemSourceLastEventOrigin,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceComparisonDiffsItem")


@_attrs_define
class WorkspaceComparisonDiffsItem:
    """
    Attributes:
        kind (WorkspaceComparisonDiffsItemKind): Type of the item
        path (str): Path of the item in the workspace
        ahead (int): Number of versions source is ahead of target
        behind (int): Number of versions source is behind target
        has_changes (bool): Whether the item has any differences
        exists_in_source (bool): If the item exists in the source workspace
        exists_in_fork (bool): If the item exists in the fork workspace
        fork_last_event_kind (Union[Unset, WorkspaceComparisonDiffsItemForkLastEventKind]): What a deploy event did to
            the path it is recorded against: `write` (the path holds an item
            after the event), `delete` (it does not), or `rename_from` (the path was vacated by a rename
            to another path). Create and update are not distinguished. Omitted when no such event has
            been recorded for that side, which counts as no evidence.
        fork_last_event_origin (Union[Unset, WorkspaceComparisonDiffsItemForkLastEventOrigin]): Who caused a deploy
            event: `authored` (written in that workspace by the requester) or `sync`
            (applied there by a git-sync pull or a workspace-to-workspace deploy). Only an authored
            removal is evidence that the workspace dropped the item on purpose. Omitted when no such
            event has been recorded for that side.
        source_last_event_kind (Union[Unset, WorkspaceComparisonDiffsItemSourceLastEventKind]): What a deploy event did
            to the path it is recorded against: `write` (the path holds an item
            after the event), `delete` (it does not), or `rename_from` (the path was vacated by a rename
            to another path). Create and update are not distinguished. Omitted when no such event has
            been recorded for that side, which counts as no evidence.
        source_last_event_origin (Union[Unset, WorkspaceComparisonDiffsItemSourceLastEventOrigin]): Who caused a deploy
            event: `authored` (written in that workspace by the requester) or `sync`
            (applied there by a git-sync pull or a workspace-to-workspace deploy). Only an authored
            removal is evidence that the workspace dropped the item on purpose. Omitted when no such
            event has been recorded for that side.
    """

    kind: WorkspaceComparisonDiffsItemKind
    path: str
    ahead: int
    behind: int
    has_changes: bool
    exists_in_source: bool
    exists_in_fork: bool
    fork_last_event_kind: Union[Unset, WorkspaceComparisonDiffsItemForkLastEventKind] = UNSET
    fork_last_event_origin: Union[Unset, WorkspaceComparisonDiffsItemForkLastEventOrigin] = UNSET
    source_last_event_kind: Union[Unset, WorkspaceComparisonDiffsItemSourceLastEventKind] = UNSET
    source_last_event_origin: Union[Unset, WorkspaceComparisonDiffsItemSourceLastEventOrigin] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        ahead = self.ahead
        behind = self.behind
        has_changes = self.has_changes
        exists_in_source = self.exists_in_source
        exists_in_fork = self.exists_in_fork
        fork_last_event_kind: Union[Unset, str] = UNSET
        if not isinstance(self.fork_last_event_kind, Unset):
            fork_last_event_kind = self.fork_last_event_kind.value

        fork_last_event_origin: Union[Unset, str] = UNSET
        if not isinstance(self.fork_last_event_origin, Unset):
            fork_last_event_origin = self.fork_last_event_origin.value

        source_last_event_kind: Union[Unset, str] = UNSET
        if not isinstance(self.source_last_event_kind, Unset):
            source_last_event_kind = self.source_last_event_kind.value

        source_last_event_origin: Union[Unset, str] = UNSET
        if not isinstance(self.source_last_event_origin, Unset):
            source_last_event_origin = self.source_last_event_origin.value

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
        if fork_last_event_kind is not UNSET:
            field_dict["fork_last_event_kind"] = fork_last_event_kind
        if fork_last_event_origin is not UNSET:
            field_dict["fork_last_event_origin"] = fork_last_event_origin
        if source_last_event_kind is not UNSET:
            field_dict["source_last_event_kind"] = source_last_event_kind
        if source_last_event_origin is not UNSET:
            field_dict["source_last_event_origin"] = source_last_event_origin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = WorkspaceComparisonDiffsItemKind(d.pop("kind"))

        path = d.pop("path")

        ahead = d.pop("ahead")

        behind = d.pop("behind")

        has_changes = d.pop("has_changes")

        exists_in_source = d.pop("exists_in_source")

        exists_in_fork = d.pop("exists_in_fork")

        _fork_last_event_kind = d.pop("fork_last_event_kind", UNSET)
        fork_last_event_kind: Union[Unset, WorkspaceComparisonDiffsItemForkLastEventKind]
        if isinstance(_fork_last_event_kind, Unset):
            fork_last_event_kind = UNSET
        else:
            fork_last_event_kind = WorkspaceComparisonDiffsItemForkLastEventKind(_fork_last_event_kind)

        _fork_last_event_origin = d.pop("fork_last_event_origin", UNSET)
        fork_last_event_origin: Union[Unset, WorkspaceComparisonDiffsItemForkLastEventOrigin]
        if isinstance(_fork_last_event_origin, Unset):
            fork_last_event_origin = UNSET
        else:
            fork_last_event_origin = WorkspaceComparisonDiffsItemForkLastEventOrigin(_fork_last_event_origin)

        _source_last_event_kind = d.pop("source_last_event_kind", UNSET)
        source_last_event_kind: Union[Unset, WorkspaceComparisonDiffsItemSourceLastEventKind]
        if isinstance(_source_last_event_kind, Unset):
            source_last_event_kind = UNSET
        else:
            source_last_event_kind = WorkspaceComparisonDiffsItemSourceLastEventKind(_source_last_event_kind)

        _source_last_event_origin = d.pop("source_last_event_origin", UNSET)
        source_last_event_origin: Union[Unset, WorkspaceComparisonDiffsItemSourceLastEventOrigin]
        if isinstance(_source_last_event_origin, Unset):
            source_last_event_origin = UNSET
        else:
            source_last_event_origin = WorkspaceComparisonDiffsItemSourceLastEventOrigin(_source_last_event_origin)

        workspace_comparison_diffs_item = cls(
            kind=kind,
            path=path,
            ahead=ahead,
            behind=behind,
            has_changes=has_changes,
            exists_in_source=exists_in_source,
            exists_in_fork=exists_in_fork,
            fork_last_event_kind=fork_last_event_kind,
            fork_last_event_origin=fork_last_event_origin,
            source_last_event_kind=source_last_event_kind,
            source_last_event_origin=source_last_event_origin,
        )

        workspace_comparison_diffs_item.additional_properties = d
        return workspace_comparison_diffs_item

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

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_drafts_response_200_item_kind import ListDraftsResponse200ItemKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_drafts_response_200_item_draft_users_item import ListDraftsResponse200ItemDraftUsersItem


T = TypeVar("T", bound="ListDraftsResponse200Item")


@_attrs_define
class ListDraftsResponse200Item:
    """
    Attributes:
        kind (ListDraftsResponse200ItemKind): Closed set of item kinds a user can autosave as a draft. Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        draft_only (bool): No deployed counterpart exists at this path — the draft is the whole item.
        legacy_draft (bool): The listed draft is a legacy workspace-level row (email NULL) predating the per-user drafts
            migration. Only true when no per-user draft exists at this path.
        created_at (datetime.datetime):
        can_write (bool): Whether the current user may deploy/discard this draft (same check the deploy/discard
            endpoints enforce).
        mine (bool): The row belongs to the current user (own draft or the legacy no-owner row) and is therefore
            actionable. Always true in the default listing; with `all_users=true`, other users' rows are false (view-only).
        summary (Union[Unset, str]): Best-effort, read from the draft JSON's `summary` field when the editor shape
            carries one.
        draft_path (Union[Unset, str]): User-typed friendly path from the draft JSON's `draft_path`, when set and
            different from the storage path (e.g. a never-deployed item parked at `u/{user}/draft_{uuid}`).
        draft_users (Union[Unset, List['ListDraftsResponse200ItemDraftUsersItem']]): Draft authors at this (path, kind)
            — the legacy NULL-email row surfaced as a null username.
            Populated only for the shared full-page-editor kinds (script/flow/app/raw_app); omitted for
            drawer kinds, which keep their drafts private. Feeds the Draft badge's owner-avatar circles.
    """

    kind: ListDraftsResponse200ItemKind
    path: str
    draft_only: bool
    legacy_draft: bool
    created_at: datetime.datetime
    can_write: bool
    mine: bool
    summary: Union[Unset, str] = UNSET
    draft_path: Union[Unset, str] = UNSET
    draft_users: Union[Unset, List["ListDraftsResponse200ItemDraftUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        draft_only = self.draft_only
        legacy_draft = self.legacy_draft
        created_at = self.created_at.isoformat()

        can_write = self.can_write
        mine = self.mine
        summary = self.summary
        draft_path = self.draft_path
        draft_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.draft_users, Unset):
            draft_users = []
            for draft_users_item_data in self.draft_users:
                draft_users_item = draft_users_item_data.to_dict()

                draft_users.append(draft_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
                "draft_only": draft_only,
                "legacy_draft": legacy_draft,
                "created_at": created_at,
                "can_write": can_write,
                "mine": mine,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if draft_path is not UNSET:
            field_dict["draft_path"] = draft_path
        if draft_users is not UNSET:
            field_dict["draft_users"] = draft_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_drafts_response_200_item_draft_users_item import ListDraftsResponse200ItemDraftUsersItem

        d = src_dict.copy()
        kind = ListDraftsResponse200ItemKind(d.pop("kind"))

        path = d.pop("path")

        draft_only = d.pop("draft_only")

        legacy_draft = d.pop("legacy_draft")

        created_at = isoparse(d.pop("created_at"))

        can_write = d.pop("can_write")

        mine = d.pop("mine")

        summary = d.pop("summary", UNSET)

        draft_path = d.pop("draft_path", UNSET)

        draft_users = []
        _draft_users = d.pop("draft_users", UNSET)
        for draft_users_item_data in _draft_users or []:
            draft_users_item = ListDraftsResponse200ItemDraftUsersItem.from_dict(draft_users_item_data)

            draft_users.append(draft_users_item)

        list_drafts_response_200_item = cls(
            kind=kind,
            path=path,
            draft_only=draft_only,
            legacy_draft=legacy_draft,
            created_at=created_at,
            can_write=can_write,
            mine=mine,
            summary=summary,
            draft_path=draft_path,
            draft_users=draft_users,
        )

        list_drafts_response_200_item.additional_properties = d
        return list_drafts_response_200_item

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

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_draft_overlay_draft import UserDraftOverlayDraft
    from ..models.user_draft_overlay_other_drafts_users_item import UserDraftOverlayOtherDraftsUsersItem


T = TypeVar("T", bound="UserDraftOverlay")


@_attrs_define
class UserDraftOverlay:
    """Overlay fields added to every "get by path" response that accepts
    the `get_draft` query parameter. The deployed payload is sent
    untouched in the response body; the authed user's saved draft
    for this path — whatever shape the editor wrote — is attached
    as the sibling `draft` field when `get_draft=true` and a draft
    exists. The frontend pairs the two to present diff / reset /
    discard UI; the server never merges them.

    When `no_deployed=true` there is no deployed row at this path —
    the response body is a best-effort stand-in synthesized from
    the draft, and only `draft` is canonical. Callers should disable
    "diff vs deployed" UI in that case.

        Attributes:
            is_draft (bool):
            draft_saved_at (Union[Unset, datetime.datetime]):
            no_deployed (Union[Unset, bool]):
            draft (Union[Unset, UserDraftOverlayDraft]):
            other_drafts_users (Union[Unset, List['UserDraftOverlayOtherDraftsUsersItem']]): Other workspace users (and the
                legacy NULL-email row, if any)
                with a saved draft at the same path. Populated only on the
                authed user's "get by path" responses for kinds the editor
                surfaces a fork banner for (script, flow, app, raw_app).
                Empty / omitted for kinds without that UI.
    """

    is_draft: bool
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "UserDraftOverlayDraft"] = UNSET
    other_drafts_users: Union[Unset, List["UserDraftOverlayOtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_draft = self.is_draft
        draft_saved_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_saved_at, Unset):
            draft_saved_at = self.draft_saved_at.isoformat()

        no_deployed = self.no_deployed
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        other_drafts_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.other_drafts_users, Unset):
            other_drafts_users = []
            for other_drafts_users_item_data in self.other_drafts_users:
                other_drafts_users_item = other_drafts_users_item_data.to_dict()

                other_drafts_users.append(other_drafts_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_draft": is_draft,
            }
        )
        if draft_saved_at is not UNSET:
            field_dict["draft_saved_at"] = draft_saved_at
        if no_deployed is not UNSET:
            field_dict["no_deployed"] = no_deployed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if other_drafts_users is not UNSET:
            field_dict["other_drafts_users"] = other_drafts_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_draft_overlay_draft import UserDraftOverlayDraft
        from ..models.user_draft_overlay_other_drafts_users_item import UserDraftOverlayOtherDraftsUsersItem

        d = src_dict.copy()
        is_draft = d.pop("is_draft")

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, UserDraftOverlayDraft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = UserDraftOverlayDraft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = UserDraftOverlayOtherDraftsUsersItem.from_dict(other_drafts_users_item_data)

            other_drafts_users.append(other_drafts_users_item)

        user_draft_overlay = cls(
            is_draft=is_draft,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        user_draft_overlay.additional_properties = d
        return user_draft_overlay

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

import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDraftOverlayOtherDraftsUsersItem")


@_attrs_define
class UserDraftOverlayOtherDraftsUsersItem:
    """
    Attributes:
        draft_saved_at (datetime.datetime): When this user's draft was last saved (`draft.created_at`),
            surfaced in the fork modal as "Last updated".
        username (Union[Unset, None, str]): Workspace username of the draft owner. `null` represents
            the legacy workspace-level (NULL-email) row. Emails never
            leave the server.
    """

    draft_saved_at: datetime.datetime
    username: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        draft_saved_at = self.draft_saved_at.isoformat()

        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "draft_saved_at": draft_saved_at,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        draft_saved_at = isoparse(d.pop("draft_saved_at"))

        username = d.pop("username", UNSET)

        user_draft_overlay_other_drafts_users_item = cls(
            draft_saved_at=draft_saved_at,
            username=username,
        )

        user_draft_overlay_other_drafts_users_item.additional_properties = d
        return user_draft_overlay_other_drafts_users_item

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

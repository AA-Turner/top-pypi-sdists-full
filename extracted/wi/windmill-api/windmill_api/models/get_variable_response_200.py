import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_variable_response_200_draft import GetVariableResponse200Draft
    from ..models.get_variable_response_200_extra_perms import GetVariableResponse200ExtraPerms
    from ..models.get_variable_response_200_other_drafts_users_item import GetVariableResponse200OtherDraftsUsersItem


T = TypeVar("T", bound="GetVariableResponse200")


@_attrs_define
class GetVariableResponse200:
    """
    Attributes:
        workspace_id (str):
        path (str):
        is_secret (bool):
        extra_perms (GetVariableResponse200ExtraPerms):
        is_draft (bool):
        value (Union[Unset, str]):
        description (Union[Unset, str]):
        account (Union[Unset, int]):
        is_oauth (Union[Unset, bool]):
        is_expired (Union[Unset, bool]):
        refresh_error (Union[Unset, str]):
        is_linked (Union[Unset, bool]):
        is_refreshed (Union[Unset, bool]):
        expires_at (Union[Unset, datetime.datetime]):
        labels (Union[Unset, List[str]]):
        inherited_labels (Union[Unset, List[str]]): Labels inherited from the parent folder, computed at read time.
            Read-only — edit them on the folder.
        ws_specific (Union[Unset, bool]):
        edited_at (Union[Unset, datetime.datetime]):
        edited_by (Union[Unset, str]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            variable at the same path. Frontend renders a "Draft" badge.
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetVariableResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetVariableResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    workspace_id: str
    path: str
    is_secret: bool
    extra_perms: "GetVariableResponse200ExtraPerms"
    is_draft: bool
    value: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    account: Union[Unset, int] = UNSET
    is_oauth: Union[Unset, bool] = UNSET
    is_expired: Union[Unset, bool] = UNSET
    refresh_error: Union[Unset, str] = UNSET
    is_linked: Union[Unset, bool] = UNSET
    is_refreshed: Union[Unset, bool] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    inherited_labels: Union[Unset, List[str]] = UNSET
    ws_specific: Union[Unset, bool] = UNSET
    edited_at: Union[Unset, datetime.datetime] = UNSET
    edited_by: Union[Unset, str] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetVariableResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetVariableResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        path = self.path
        is_secret = self.is_secret
        extra_perms = self.extra_perms.to_dict()

        is_draft = self.is_draft
        value = self.value
        description = self.description
        account = self.account
        is_oauth = self.is_oauth
        is_expired = self.is_expired
        refresh_error = self.refresh_error
        is_linked = self.is_linked
        is_refreshed = self.is_refreshed
        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        inherited_labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.inherited_labels, Unset):
            inherited_labels = self.inherited_labels

        ws_specific = self.ws_specific
        edited_at: Union[Unset, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat()

        edited_by = self.edited_by
        draft_only = self.draft_only
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
                "workspace_id": workspace_id,
                "path": path,
                "is_secret": is_secret,
                "extra_perms": extra_perms,
                "is_draft": is_draft,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if description is not UNSET:
            field_dict["description"] = description
        if account is not UNSET:
            field_dict["account"] = account
        if is_oauth is not UNSET:
            field_dict["is_oauth"] = is_oauth
        if is_expired is not UNSET:
            field_dict["is_expired"] = is_expired
        if refresh_error is not UNSET:
            field_dict["refresh_error"] = refresh_error
        if is_linked is not UNSET:
            field_dict["is_linked"] = is_linked
        if is_refreshed is not UNSET:
            field_dict["is_refreshed"] = is_refreshed
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if labels is not UNSET:
            field_dict["labels"] = labels
        if inherited_labels is not UNSET:
            field_dict["inherited_labels"] = inherited_labels
        if ws_specific is not UNSET:
            field_dict["ws_specific"] = ws_specific
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if edited_by is not UNSET:
            field_dict["edited_by"] = edited_by
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
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
        from ..models.get_variable_response_200_draft import GetVariableResponse200Draft
        from ..models.get_variable_response_200_extra_perms import GetVariableResponse200ExtraPerms
        from ..models.get_variable_response_200_other_drafts_users_item import (
            GetVariableResponse200OtherDraftsUsersItem,
        )

        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        is_secret = d.pop("is_secret")

        extra_perms = GetVariableResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        is_draft = d.pop("is_draft")

        value = d.pop("value", UNSET)

        description = d.pop("description", UNSET)

        account = d.pop("account", UNSET)

        is_oauth = d.pop("is_oauth", UNSET)

        is_expired = d.pop("is_expired", UNSET)

        refresh_error = d.pop("refresh_error", UNSET)

        is_linked = d.pop("is_linked", UNSET)

        is_refreshed = d.pop("is_refreshed", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        labels = cast(List[str], d.pop("labels", UNSET))

        inherited_labels = cast(List[str], d.pop("inherited_labels", UNSET))

        ws_specific = d.pop("ws_specific", UNSET)

        _edited_at = d.pop("edited_at", UNSET)
        edited_at: Union[Unset, datetime.datetime]
        if isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        edited_by = d.pop("edited_by", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetVariableResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetVariableResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetVariableResponse200OtherDraftsUsersItem.from_dict(other_drafts_users_item_data)

            other_drafts_users.append(other_drafts_users_item)

        get_variable_response_200 = cls(
            workspace_id=workspace_id,
            path=path,
            is_secret=is_secret,
            extra_perms=extra_perms,
            is_draft=is_draft,
            value=value,
            description=description,
            account=account,
            is_oauth=is_oauth,
            is_expired=is_expired,
            refresh_error=refresh_error,
            is_linked=is_linked,
            is_refreshed=is_refreshed,
            expires_at=expires_at,
            labels=labels,
            inherited_labels=inherited_labels,
            ws_specific=ws_specific,
            edited_at=edited_at,
            edited_by=edited_by,
            draft_only=draft_only,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_variable_response_200.additional_properties = d
        return get_variable_response_200

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

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_resource_response_200_draft import GetResourceResponse200Draft
    from ..models.get_resource_response_200_extra_perms import GetResourceResponse200ExtraPerms
    from ..models.get_resource_response_200_other_drafts_users_item import GetResourceResponse200OtherDraftsUsersItem


T = TypeVar("T", bound="GetResourceResponse200")


@_attrs_define
class GetResourceResponse200:
    """
    Attributes:
        path (str):
        resource_type (str):
        is_oauth (bool):
        is_linked (bool):
        is_refreshed (bool):
        is_draft (bool):
        workspace_id (Union[Unset, str]):
        description (Union[Unset, str]):
        value (Union[Unset, Any]):
        extra_perms (Union[Unset, GetResourceResponse200ExtraPerms]):
        is_expired (Union[Unset, bool]):
        refresh_error (Union[Unset, str]):
        account (Union[Unset, float]):
        created_by (Union[Unset, str]):
        edited_at (Union[Unset, datetime.datetime]):
        labels (Union[Unset, List[str]]):
        inherited_labels (Union[Unset, List[str]]): Labels inherited from the parent folder, computed at read time.
            Read-only — edit them on the folder.
        ws_specific (Union[Unset, bool]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            resource at the same path. Frontend renders a "Draft" badge.
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetResourceResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetResourceResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    path: str
    resource_type: str
    is_oauth: bool
    is_linked: bool
    is_refreshed: bool
    is_draft: bool
    workspace_id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    value: Union[Unset, Any] = UNSET
    extra_perms: Union[Unset, "GetResourceResponse200ExtraPerms"] = UNSET
    is_expired: Union[Unset, bool] = UNSET
    refresh_error: Union[Unset, str] = UNSET
    account: Union[Unset, float] = UNSET
    created_by: Union[Unset, str] = UNSET
    edited_at: Union[Unset, datetime.datetime] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    inherited_labels: Union[Unset, List[str]] = UNSET
    ws_specific: Union[Unset, bool] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetResourceResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetResourceResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        resource_type = self.resource_type
        is_oauth = self.is_oauth
        is_linked = self.is_linked
        is_refreshed = self.is_refreshed
        is_draft = self.is_draft
        workspace_id = self.workspace_id
        description = self.description
        value = self.value
        extra_perms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_perms, Unset):
            extra_perms = self.extra_perms.to_dict()

        is_expired = self.is_expired
        refresh_error = self.refresh_error
        account = self.account
        created_by = self.created_by
        edited_at: Union[Unset, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat()

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        inherited_labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.inherited_labels, Unset):
            inherited_labels = self.inherited_labels

        ws_specific = self.ws_specific
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
                "path": path,
                "resource_type": resource_type,
                "is_oauth": is_oauth,
                "is_linked": is_linked,
                "is_refreshed": is_refreshed,
                "is_draft": is_draft,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if description is not UNSET:
            field_dict["description"] = description
        if value is not UNSET:
            field_dict["value"] = value
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms
        if is_expired is not UNSET:
            field_dict["is_expired"] = is_expired
        if refresh_error is not UNSET:
            field_dict["refresh_error"] = refresh_error
        if account is not UNSET:
            field_dict["account"] = account
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if labels is not UNSET:
            field_dict["labels"] = labels
        if inherited_labels is not UNSET:
            field_dict["inherited_labels"] = inherited_labels
        if ws_specific is not UNSET:
            field_dict["ws_specific"] = ws_specific
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
        from ..models.get_resource_response_200_draft import GetResourceResponse200Draft
        from ..models.get_resource_response_200_extra_perms import GetResourceResponse200ExtraPerms
        from ..models.get_resource_response_200_other_drafts_users_item import (
            GetResourceResponse200OtherDraftsUsersItem,
        )

        d = src_dict.copy()
        path = d.pop("path")

        resource_type = d.pop("resource_type")

        is_oauth = d.pop("is_oauth")

        is_linked = d.pop("is_linked")

        is_refreshed = d.pop("is_refreshed")

        is_draft = d.pop("is_draft")

        workspace_id = d.pop("workspace_id", UNSET)

        description = d.pop("description", UNSET)

        value = d.pop("value", UNSET)

        _extra_perms = d.pop("extra_perms", UNSET)
        extra_perms: Union[Unset, GetResourceResponse200ExtraPerms]
        if isinstance(_extra_perms, Unset):
            extra_perms = UNSET
        else:
            extra_perms = GetResourceResponse200ExtraPerms.from_dict(_extra_perms)

        is_expired = d.pop("is_expired", UNSET)

        refresh_error = d.pop("refresh_error", UNSET)

        account = d.pop("account", UNSET)

        created_by = d.pop("created_by", UNSET)

        _edited_at = d.pop("edited_at", UNSET)
        edited_at: Union[Unset, datetime.datetime]
        if isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        labels = cast(List[str], d.pop("labels", UNSET))

        inherited_labels = cast(List[str], d.pop("inherited_labels", UNSET))

        ws_specific = d.pop("ws_specific", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetResourceResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetResourceResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetResourceResponse200OtherDraftsUsersItem.from_dict(other_drafts_users_item_data)

            other_drafts_users.append(other_drafts_users_item)

        get_resource_response_200 = cls(
            path=path,
            resource_type=resource_type,
            is_oauth=is_oauth,
            is_linked=is_linked,
            is_refreshed=is_refreshed,
            is_draft=is_draft,
            workspace_id=workspace_id,
            description=description,
            value=value,
            extra_perms=extra_perms,
            is_expired=is_expired,
            refresh_error=refresh_error,
            account=account,
            created_by=created_by,
            edited_at=edited_at,
            labels=labels,
            inherited_labels=inherited_labels,
            ws_specific=ws_specific,
            draft_only=draft_only,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_resource_response_200.additional_properties = d
        return get_resource_response_200

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

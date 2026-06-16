import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_app_by_path_response_200_execution_mode import GetAppByPathResponse200ExecutionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_app_by_path_response_200_draft import GetAppByPathResponse200Draft
    from ..models.get_app_by_path_response_200_extra_perms import GetAppByPathResponse200ExtraPerms
    from ..models.get_app_by_path_response_200_other_drafts_users_item import (
        GetAppByPathResponse200OtherDraftsUsersItem,
    )
    from ..models.get_app_by_path_response_200_policy import GetAppByPathResponse200Policy


T = TypeVar("T", bound="GetAppByPathResponse200")


@_attrs_define
class GetAppByPathResponse200:
    """
    Attributes:
        id (int):
        workspace_id (str):
        path (str):
        summary (str):
        versions (List[int]):
        created_by (str):
        created_at (datetime.datetime):
        value (Any):
        policy (GetAppByPathResponse200Policy):
        execution_mode (GetAppByPathResponse200ExecutionMode):
        extra_perms (GetAppByPathResponse200ExtraPerms):
        raw_app (bool):
        is_draft (bool):
        custom_path (Union[Unset, str]):
        bundle_secret (Union[Unset, str]):
        labels (Union[Unset, List[str]]):
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetAppByPathResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetAppByPathResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    id: int
    workspace_id: str
    path: str
    summary: str
    versions: List[int]
    created_by: str
    created_at: datetime.datetime
    value: Any
    policy: "GetAppByPathResponse200Policy"
    execution_mode: GetAppByPathResponse200ExecutionMode
    extra_perms: "GetAppByPathResponse200ExtraPerms"
    raw_app: bool
    is_draft: bool
    custom_path: Union[Unset, str] = UNSET
    bundle_secret: Union[Unset, str] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetAppByPathResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetAppByPathResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        path = self.path
        summary = self.summary
        versions = self.versions

        created_by = self.created_by
        created_at = self.created_at.isoformat()

        value = self.value
        policy = self.policy.to_dict()

        execution_mode = self.execution_mode.value

        extra_perms = self.extra_perms.to_dict()

        raw_app = self.raw_app
        is_draft = self.is_draft
        custom_path = self.custom_path
        bundle_secret = self.bundle_secret
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

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
                "id": id,
                "workspace_id": workspace_id,
                "path": path,
                "summary": summary,
                "versions": versions,
                "created_by": created_by,
                "created_at": created_at,
                "value": value,
                "policy": policy,
                "execution_mode": execution_mode,
                "extra_perms": extra_perms,
                "raw_app": raw_app,
                "is_draft": is_draft,
            }
        )
        if custom_path is not UNSET:
            field_dict["custom_path"] = custom_path
        if bundle_secret is not UNSET:
            field_dict["bundle_secret"] = bundle_secret
        if labels is not UNSET:
            field_dict["labels"] = labels
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
        from ..models.get_app_by_path_response_200_draft import GetAppByPathResponse200Draft
        from ..models.get_app_by_path_response_200_extra_perms import GetAppByPathResponse200ExtraPerms
        from ..models.get_app_by_path_response_200_other_drafts_users_item import (
            GetAppByPathResponse200OtherDraftsUsersItem,
        )
        from ..models.get_app_by_path_response_200_policy import GetAppByPathResponse200Policy

        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        summary = d.pop("summary")

        versions = cast(List[int], d.pop("versions"))

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        value = d.pop("value")

        policy = GetAppByPathResponse200Policy.from_dict(d.pop("policy"))

        execution_mode = GetAppByPathResponse200ExecutionMode(d.pop("execution_mode"))

        extra_perms = GetAppByPathResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        raw_app = d.pop("raw_app")

        is_draft = d.pop("is_draft")

        custom_path = d.pop("custom_path", UNSET)

        bundle_secret = d.pop("bundle_secret", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetAppByPathResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetAppByPathResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetAppByPathResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_app_by_path_response_200 = cls(
            id=id,
            workspace_id=workspace_id,
            path=path,
            summary=summary,
            versions=versions,
            created_by=created_by,
            created_at=created_at,
            value=value,
            policy=policy,
            execution_mode=execution_mode,
            extra_perms=extra_perms,
            raw_app=raw_app,
            is_draft=is_draft,
            custom_path=custom_path,
            bundle_secret=bundle_secret,
            labels=labels,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_app_by_path_response_200.additional_properties = d
        return get_app_by_path_response_200

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

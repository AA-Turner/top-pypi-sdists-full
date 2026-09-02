import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_runnables_response_200_items_item_type import ListRunnablesResponse200ItemsItemType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_runnables_response_200_items_item_draft_users_item import (
        ListRunnablesResponse200ItemsItemDraftUsersItem,
    )
    from ..models.list_runnables_response_200_items_item_extra_perms import ListRunnablesResponse200ItemsItemExtraPerms


T = TypeVar("T", bound="ListRunnablesResponse200ItemsItem")


@_attrs_define
class ListRunnablesResponse200ItemsItem:
    """A row in the merged runnables listing. `type` is the discriminator;
    kind-specific fields (hash/language/kind for scripts, execution_mode/
    version for apps) are present only for that kind. `edited_at` is the
    unified last-updated time (a script's created_at, a flow/app's edit
    time).

        Attributes:
            type (ListRunnablesResponse200ItemsItemType):
            path (str):
            summary (Union[Unset, str]):
            workspace_id (Union[Unset, str]):
            extra_perms (Union[Unset, ListRunnablesResponse200ItemsItemExtraPerms]):
            starred (Union[Unset, bool]):
            archived (Union[Unset, bool]):
            is_draft (Union[Unset, bool]):
            draft_only (Union[Unset, None, bool]):
            draft_path (Union[Unset, str]):
            draft_users (Union[Unset, List['ListRunnablesResponse200ItemsItemDraftUsersItem']]):
            labels (Union[Unset, List[str]]):
            inherited_labels (Union[Unset, List[str]]):
            ws_error_handler_muted (Union[Unset, bool]):
            edited_at (Union[Unset, datetime.datetime]):
            hash_ (Union[Unset, str]): script version hash as a 16-char hex string
            language (Union[Unset, str]):
            kind (Union[Unset, str]):
            auto_kind (Union[Unset, str]):
            use_codebase (Union[Unset, bool]):
            has_deploy_errors (Union[Unset, bool]):
            raw_app (Union[Unset, bool]):
            execution_mode (Union[Unset, str]):
            id (Union[Unset, int]):
            version (Union[Unset, int]):
    """

    type: ListRunnablesResponse200ItemsItemType
    path: str
    summary: Union[Unset, str] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    extra_perms: Union[Unset, "ListRunnablesResponse200ItemsItemExtraPerms"] = UNSET
    starred: Union[Unset, bool] = UNSET
    archived: Union[Unset, bool] = UNSET
    is_draft: Union[Unset, bool] = UNSET
    draft_only: Union[Unset, None, bool] = UNSET
    draft_path: Union[Unset, str] = UNSET
    draft_users: Union[Unset, List["ListRunnablesResponse200ItemsItemDraftUsersItem"]] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    inherited_labels: Union[Unset, List[str]] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    edited_at: Union[Unset, datetime.datetime] = UNSET
    hash_: Union[Unset, str] = UNSET
    language: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    auto_kind: Union[Unset, str] = UNSET
    use_codebase: Union[Unset, bool] = UNSET
    has_deploy_errors: Union[Unset, bool] = UNSET
    raw_app: Union[Unset, bool] = UNSET
    execution_mode: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    version: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        path = self.path
        summary = self.summary
        workspace_id = self.workspace_id
        extra_perms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_perms, Unset):
            extra_perms = self.extra_perms.to_dict()

        starred = self.starred
        archived = self.archived
        is_draft = self.is_draft
        draft_only = self.draft_only
        draft_path = self.draft_path
        draft_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.draft_users, Unset):
            draft_users = []
            for draft_users_item_data in self.draft_users:
                draft_users_item = draft_users_item_data.to_dict()

                draft_users.append(draft_users_item)

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        inherited_labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.inherited_labels, Unset):
            inherited_labels = self.inherited_labels

        ws_error_handler_muted = self.ws_error_handler_muted
        edited_at: Union[Unset, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat()

        hash_ = self.hash_
        language = self.language
        kind = self.kind
        auto_kind = self.auto_kind
        use_codebase = self.use_codebase
        has_deploy_errors = self.has_deploy_errors
        raw_app = self.raw_app
        execution_mode = self.execution_mode
        id = self.id
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "path": path,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms
        if starred is not UNSET:
            field_dict["starred"] = starred
        if archived is not UNSET:
            field_dict["archived"] = archived
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if draft_path is not UNSET:
            field_dict["draft_path"] = draft_path
        if draft_users is not UNSET:
            field_dict["draft_users"] = draft_users
        if labels is not UNSET:
            field_dict["labels"] = labels
        if inherited_labels is not UNSET:
            field_dict["inherited_labels"] = inherited_labels
        if ws_error_handler_muted is not UNSET:
            field_dict["ws_error_handler_muted"] = ws_error_handler_muted
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if language is not UNSET:
            field_dict["language"] = language
        if kind is not UNSET:
            field_dict["kind"] = kind
        if auto_kind is not UNSET:
            field_dict["auto_kind"] = auto_kind
        if use_codebase is not UNSET:
            field_dict["use_codebase"] = use_codebase
        if has_deploy_errors is not UNSET:
            field_dict["has_deploy_errors"] = has_deploy_errors
        if raw_app is not UNSET:
            field_dict["raw_app"] = raw_app
        if execution_mode is not UNSET:
            field_dict["execution_mode"] = execution_mode
        if id is not UNSET:
            field_dict["id"] = id
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_runnables_response_200_items_item_draft_users_item import (
            ListRunnablesResponse200ItemsItemDraftUsersItem,
        )
        from ..models.list_runnables_response_200_items_item_extra_perms import (
            ListRunnablesResponse200ItemsItemExtraPerms,
        )

        d = src_dict.copy()
        type = ListRunnablesResponse200ItemsItemType(d.pop("type"))

        path = d.pop("path")

        summary = d.pop("summary", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        _extra_perms = d.pop("extra_perms", UNSET)
        extra_perms: Union[Unset, ListRunnablesResponse200ItemsItemExtraPerms]
        if isinstance(_extra_perms, Unset):
            extra_perms = UNSET
        else:
            extra_perms = ListRunnablesResponse200ItemsItemExtraPerms.from_dict(_extra_perms)

        starred = d.pop("starred", UNSET)

        archived = d.pop("archived", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        draft_path = d.pop("draft_path", UNSET)

        draft_users = []
        _draft_users = d.pop("draft_users", UNSET)
        for draft_users_item_data in _draft_users or []:
            draft_users_item = ListRunnablesResponse200ItemsItemDraftUsersItem.from_dict(draft_users_item_data)

            draft_users.append(draft_users_item)

        labels = cast(List[str], d.pop("labels", UNSET))

        inherited_labels = cast(List[str], d.pop("inherited_labels", UNSET))

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        _edited_at = d.pop("edited_at", UNSET)
        edited_at: Union[Unset, datetime.datetime]
        if isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        hash_ = d.pop("hash", UNSET)

        language = d.pop("language", UNSET)

        kind = d.pop("kind", UNSET)

        auto_kind = d.pop("auto_kind", UNSET)

        use_codebase = d.pop("use_codebase", UNSET)

        has_deploy_errors = d.pop("has_deploy_errors", UNSET)

        raw_app = d.pop("raw_app", UNSET)

        execution_mode = d.pop("execution_mode", UNSET)

        id = d.pop("id", UNSET)

        version = d.pop("version", UNSET)

        list_runnables_response_200_items_item = cls(
            type=type,
            path=path,
            summary=summary,
            workspace_id=workspace_id,
            extra_perms=extra_perms,
            starred=starred,
            archived=archived,
            is_draft=is_draft,
            draft_only=draft_only,
            draft_path=draft_path,
            draft_users=draft_users,
            labels=labels,
            inherited_labels=inherited_labels,
            ws_error_handler_muted=ws_error_handler_muted,
            edited_at=edited_at,
            hash_=hash_,
            language=language,
            kind=kind,
            auto_kind=auto_kind,
            use_codebase=use_codebase,
            has_deploy_errors=has_deploy_errors,
            raw_app=raw_app,
            execution_mode=execution_mode,
            id=id,
            version=version,
        )

        list_runnables_response_200_items_item.additional_properties = d
        return list_runnables_response_200_items_item

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

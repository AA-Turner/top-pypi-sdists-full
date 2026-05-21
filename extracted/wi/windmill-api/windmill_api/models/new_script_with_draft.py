import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.new_script_with_draft_kind import NewScriptWithDraftKind
from ..models.new_script_with_draft_language import NewScriptWithDraftLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_script_with_draft_assets_item import NewScriptWithDraftAssetsItem
    from ..models.new_script_with_draft_draft import NewScriptWithDraftDraft
    from ..models.new_script_with_draft_modules import NewScriptWithDraftModules
    from ..models.new_script_with_draft_schema import NewScriptWithDraftSchema


T = TypeVar("T", bound="NewScriptWithDraft")


@_attrs_define
class NewScriptWithDraft:
    """
    Attributes:
        path (str):
        summary (str):
        content (str):
        language (NewScriptWithDraftLanguage):
        hash_ (str):
        parent_hash (Union[Unset, str]):
        description (Union[Unset, str]):
        schema (Union[Unset, NewScriptWithDraftSchema]):
        is_template (Union[Unset, bool]):
        lock (Union[Unset, str]):
        kind (Union[Unset, NewScriptWithDraftKind]):
        tag (Union[Unset, str]):
        draft_only (Union[Unset, bool]):
        envs (Union[Unset, List[str]]):
        concurrent_limit (Union[Unset, int]):
        concurrency_time_window_s (Union[Unset, int]):
        cache_ttl (Union[Unset, float]):
        cache_ignore_s3_path (Union[Unset, bool]):
        dedicated_worker (Union[Unset, bool]):
        ws_error_handler_muted (Union[Unset, bool]):
        priority (Union[Unset, int]):
        restart_unless_cancelled (Union[Unset, bool]):
        timeout (Union[Unset, int]):
        delete_after_secs (Union[Unset, int]): If set, delete the job's args, result and logs after this many seconds
            following job completion
        deployment_message (Union[Unset, str]):
        concurrency_key (Union[Unset, str]):
        debounce_key (Union[Unset, str]):
        debounce_delay_s (Union[Unset, int]):
        debounce_args_to_accumulate (Union[Unset, List[str]]):
        max_total_debouncing_time (Union[Unset, int]):
        max_total_debounces_amount (Union[Unset, int]):
        visible_to_runner_only (Union[Unset, bool]):
        auto_kind (Union[Unset, str]):
        codebase (Union[Unset, str]):
        has_preprocessor (Union[Unset, bool]):
        on_behalf_of_email (Union[Unset, str]):
        preserve_on_behalf_of (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original on_behalf_of_email value instead of overwriting it.
        assets (Union[Unset, List['NewScriptWithDraftAssetsItem']]):
        modules (Union[Unset, None, NewScriptWithDraftModules]): Additional script modules keyed by relative file path
        labels (Union[Unset, List[str]]):
        draft (Union[Unset, NewScriptWithDraftDraft]):
        draft_created_at (Union[Unset, datetime.datetime]): Timestamp at which the most recent DB draft was created.
            Used by the frontend's UserDraft staleness check.
    """

    path: str
    summary: str
    content: str
    language: NewScriptWithDraftLanguage
    hash_: str
    parent_hash: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    schema: Union[Unset, "NewScriptWithDraftSchema"] = UNSET
    is_template: Union[Unset, bool] = UNSET
    lock: Union[Unset, str] = UNSET
    kind: Union[Unset, NewScriptWithDraftKind] = UNSET
    tag: Union[Unset, str] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    envs: Union[Unset, List[str]] = UNSET
    concurrent_limit: Union[Unset, int] = UNSET
    concurrency_time_window_s: Union[Unset, int] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    cache_ignore_s3_path: Union[Unset, bool] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    restart_unless_cancelled: Union[Unset, bool] = UNSET
    timeout: Union[Unset, int] = UNSET
    delete_after_secs: Union[Unset, int] = UNSET
    deployment_message: Union[Unset, str] = UNSET
    concurrency_key: Union[Unset, str] = UNSET
    debounce_key: Union[Unset, str] = UNSET
    debounce_delay_s: Union[Unset, int] = UNSET
    debounce_args_to_accumulate: Union[Unset, List[str]] = UNSET
    max_total_debouncing_time: Union[Unset, int] = UNSET
    max_total_debounces_amount: Union[Unset, int] = UNSET
    visible_to_runner_only: Union[Unset, bool] = UNSET
    auto_kind: Union[Unset, str] = UNSET
    codebase: Union[Unset, str] = UNSET
    has_preprocessor: Union[Unset, bool] = UNSET
    on_behalf_of_email: Union[Unset, str] = UNSET
    preserve_on_behalf_of: Union[Unset, bool] = UNSET
    assets: Union[Unset, List["NewScriptWithDraftAssetsItem"]] = UNSET
    modules: Union[Unset, None, "NewScriptWithDraftModules"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft: Union[Unset, "NewScriptWithDraftDraft"] = UNSET
    draft_created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        content = self.content
        language = self.language.value

        hash_ = self.hash_
        parent_hash = self.parent_hash
        description = self.description
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        is_template = self.is_template
        lock = self.lock
        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        tag = self.tag
        draft_only = self.draft_only
        envs: Union[Unset, List[str]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = self.envs

        concurrent_limit = self.concurrent_limit
        concurrency_time_window_s = self.concurrency_time_window_s
        cache_ttl = self.cache_ttl
        cache_ignore_s3_path = self.cache_ignore_s3_path
        dedicated_worker = self.dedicated_worker
        ws_error_handler_muted = self.ws_error_handler_muted
        priority = self.priority
        restart_unless_cancelled = self.restart_unless_cancelled
        timeout = self.timeout
        delete_after_secs = self.delete_after_secs
        deployment_message = self.deployment_message
        concurrency_key = self.concurrency_key
        debounce_key = self.debounce_key
        debounce_delay_s = self.debounce_delay_s
        debounce_args_to_accumulate: Union[Unset, List[str]] = UNSET
        if not isinstance(self.debounce_args_to_accumulate, Unset):
            debounce_args_to_accumulate = self.debounce_args_to_accumulate

        max_total_debouncing_time = self.max_total_debouncing_time
        max_total_debounces_amount = self.max_total_debounces_amount
        visible_to_runner_only = self.visible_to_runner_only
        auto_kind = self.auto_kind
        codebase = self.codebase
        has_preprocessor = self.has_preprocessor
        on_behalf_of_email = self.on_behalf_of_email
        preserve_on_behalf_of = self.preserve_on_behalf_of
        assets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.assets, Unset):
            assets = []
            for assets_item_data in self.assets:
                assets_item = assets_item_data.to_dict()

                assets.append(assets_item)

        modules: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.modules, Unset):
            modules = self.modules.to_dict() if self.modules else None

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        draft_created_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_created_at, Unset):
            draft_created_at = self.draft_created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "summary": summary,
                "content": content,
                "language": language,
                "hash": hash_,
            }
        )
        if parent_hash is not UNSET:
            field_dict["parent_hash"] = parent_hash
        if description is not UNSET:
            field_dict["description"] = description
        if schema is not UNSET:
            field_dict["schema"] = schema
        if is_template is not UNSET:
            field_dict["is_template"] = is_template
        if lock is not UNSET:
            field_dict["lock"] = lock
        if kind is not UNSET:
            field_dict["kind"] = kind
        if tag is not UNSET:
            field_dict["tag"] = tag
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if envs is not UNSET:
            field_dict["envs"] = envs
        if concurrent_limit is not UNSET:
            field_dict["concurrent_limit"] = concurrent_limit
        if concurrency_time_window_s is not UNSET:
            field_dict["concurrency_time_window_s"] = concurrency_time_window_s
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if cache_ignore_s3_path is not UNSET:
            field_dict["cache_ignore_s3_path"] = cache_ignore_s3_path
        if dedicated_worker is not UNSET:
            field_dict["dedicated_worker"] = dedicated_worker
        if ws_error_handler_muted is not UNSET:
            field_dict["ws_error_handler_muted"] = ws_error_handler_muted
        if priority is not UNSET:
            field_dict["priority"] = priority
        if restart_unless_cancelled is not UNSET:
            field_dict["restart_unless_cancelled"] = restart_unless_cancelled
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if delete_after_secs is not UNSET:
            field_dict["delete_after_secs"] = delete_after_secs
        if deployment_message is not UNSET:
            field_dict["deployment_message"] = deployment_message
        if concurrency_key is not UNSET:
            field_dict["concurrency_key"] = concurrency_key
        if debounce_key is not UNSET:
            field_dict["debounce_key"] = debounce_key
        if debounce_delay_s is not UNSET:
            field_dict["debounce_delay_s"] = debounce_delay_s
        if debounce_args_to_accumulate is not UNSET:
            field_dict["debounce_args_to_accumulate"] = debounce_args_to_accumulate
        if max_total_debouncing_time is not UNSET:
            field_dict["max_total_debouncing_time"] = max_total_debouncing_time
        if max_total_debounces_amount is not UNSET:
            field_dict["max_total_debounces_amount"] = max_total_debounces_amount
        if visible_to_runner_only is not UNSET:
            field_dict["visible_to_runner_only"] = visible_to_runner_only
        if auto_kind is not UNSET:
            field_dict["auto_kind"] = auto_kind
        if codebase is not UNSET:
            field_dict["codebase"] = codebase
        if has_preprocessor is not UNSET:
            field_dict["has_preprocessor"] = has_preprocessor
        if on_behalf_of_email is not UNSET:
            field_dict["on_behalf_of_email"] = on_behalf_of_email
        if preserve_on_behalf_of is not UNSET:
            field_dict["preserve_on_behalf_of"] = preserve_on_behalf_of
        if assets is not UNSET:
            field_dict["assets"] = assets
        if modules is not UNSET:
            field_dict["modules"] = modules
        if labels is not UNSET:
            field_dict["labels"] = labels
        if draft is not UNSET:
            field_dict["draft"] = draft
        if draft_created_at is not UNSET:
            field_dict["draft_created_at"] = draft_created_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_script_with_draft_assets_item import NewScriptWithDraftAssetsItem
        from ..models.new_script_with_draft_draft import NewScriptWithDraftDraft
        from ..models.new_script_with_draft_modules import NewScriptWithDraftModules
        from ..models.new_script_with_draft_schema import NewScriptWithDraftSchema

        d = src_dict.copy()
        path = d.pop("path")

        summary = d.pop("summary")

        content = d.pop("content")

        language = NewScriptWithDraftLanguage(d.pop("language"))

        hash_ = d.pop("hash")

        parent_hash = d.pop("parent_hash", UNSET)

        description = d.pop("description", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, NewScriptWithDraftSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = NewScriptWithDraftSchema.from_dict(_schema)

        is_template = d.pop("is_template", UNSET)

        lock = d.pop("lock", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, NewScriptWithDraftKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = NewScriptWithDraftKind(_kind)

        tag = d.pop("tag", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        envs = cast(List[str], d.pop("envs", UNSET))

        concurrent_limit = d.pop("concurrent_limit", UNSET)

        concurrency_time_window_s = d.pop("concurrency_time_window_s", UNSET)

        cache_ttl = d.pop("cache_ttl", UNSET)

        cache_ignore_s3_path = d.pop("cache_ignore_s3_path", UNSET)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        priority = d.pop("priority", UNSET)

        restart_unless_cancelled = d.pop("restart_unless_cancelled", UNSET)

        timeout = d.pop("timeout", UNSET)

        delete_after_secs = d.pop("delete_after_secs", UNSET)

        deployment_message = d.pop("deployment_message", UNSET)

        concurrency_key = d.pop("concurrency_key", UNSET)

        debounce_key = d.pop("debounce_key", UNSET)

        debounce_delay_s = d.pop("debounce_delay_s", UNSET)

        debounce_args_to_accumulate = cast(List[str], d.pop("debounce_args_to_accumulate", UNSET))

        max_total_debouncing_time = d.pop("max_total_debouncing_time", UNSET)

        max_total_debounces_amount = d.pop("max_total_debounces_amount", UNSET)

        visible_to_runner_only = d.pop("visible_to_runner_only", UNSET)

        auto_kind = d.pop("auto_kind", UNSET)

        codebase = d.pop("codebase", UNSET)

        has_preprocessor = d.pop("has_preprocessor", UNSET)

        on_behalf_of_email = d.pop("on_behalf_of_email", UNSET)

        preserve_on_behalf_of = d.pop("preserve_on_behalf_of", UNSET)

        assets = []
        _assets = d.pop("assets", UNSET)
        for assets_item_data in _assets or []:
            assets_item = NewScriptWithDraftAssetsItem.from_dict(assets_item_data)

            assets.append(assets_item)

        _modules = d.pop("modules", UNSET)
        modules: Union[Unset, None, NewScriptWithDraftModules]
        if _modules is None:
            modules = None
        elif isinstance(_modules, Unset):
            modules = UNSET
        else:
            modules = NewScriptWithDraftModules.from_dict(_modules)

        labels = cast(List[str], d.pop("labels", UNSET))

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, NewScriptWithDraftDraft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = NewScriptWithDraftDraft.from_dict(_draft)

        _draft_created_at = d.pop("draft_created_at", UNSET)
        draft_created_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_created_at, Unset):
            draft_created_at = UNSET
        else:
            draft_created_at = isoparse(_draft_created_at)

        new_script_with_draft = cls(
            path=path,
            summary=summary,
            content=content,
            language=language,
            hash_=hash_,
            parent_hash=parent_hash,
            description=description,
            schema=schema,
            is_template=is_template,
            lock=lock,
            kind=kind,
            tag=tag,
            draft_only=draft_only,
            envs=envs,
            concurrent_limit=concurrent_limit,
            concurrency_time_window_s=concurrency_time_window_s,
            cache_ttl=cache_ttl,
            cache_ignore_s3_path=cache_ignore_s3_path,
            dedicated_worker=dedicated_worker,
            ws_error_handler_muted=ws_error_handler_muted,
            priority=priority,
            restart_unless_cancelled=restart_unless_cancelled,
            timeout=timeout,
            delete_after_secs=delete_after_secs,
            deployment_message=deployment_message,
            concurrency_key=concurrency_key,
            debounce_key=debounce_key,
            debounce_delay_s=debounce_delay_s,
            debounce_args_to_accumulate=debounce_args_to_accumulate,
            max_total_debouncing_time=max_total_debouncing_time,
            max_total_debounces_amount=max_total_debounces_amount,
            visible_to_runner_only=visible_to_runner_only,
            auto_kind=auto_kind,
            codebase=codebase,
            has_preprocessor=has_preprocessor,
            on_behalf_of_email=on_behalf_of_email,
            preserve_on_behalf_of=preserve_on_behalf_of,
            assets=assets,
            modules=modules,
            labels=labels,
            draft=draft,
            draft_created_at=draft_created_at,
        )

        new_script_with_draft.additional_properties = d
        return new_script_with_draft

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

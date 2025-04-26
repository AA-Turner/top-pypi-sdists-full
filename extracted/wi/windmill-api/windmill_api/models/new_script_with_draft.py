from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_script_with_draft_kind import NewScriptWithDraftKind
from ..models.new_script_with_draft_language import NewScriptWithDraftLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_script_with_draft_draft import NewScriptWithDraftDraft
    from ..models.new_script_with_draft_schema import NewScriptWithDraftSchema


T = TypeVar("T", bound="NewScriptWithDraft")


@_attrs_define
class NewScriptWithDraft:
    """
    Attributes:
        path (str):
        summary (str):
        description (str):
        content (str):
        language (NewScriptWithDraftLanguage):
        hash_ (str):
        parent_hash (Union[Unset, str]):
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
        dedicated_worker (Union[Unset, bool]):
        ws_error_handler_muted (Union[Unset, bool]):
        priority (Union[Unset, int]):
        restart_unless_cancelled (Union[Unset, bool]):
        timeout (Union[Unset, int]):
        delete_after_use (Union[Unset, bool]):
        deployment_message (Union[Unset, str]):
        concurrency_key (Union[Unset, str]):
        visible_to_runner_only (Union[Unset, bool]):
        no_main_func (Union[Unset, bool]):
        codebase (Union[Unset, str]):
        has_preprocessor (Union[Unset, bool]):
        on_behalf_of_email (Union[Unset, str]):
        draft (Union[Unset, NewScriptWithDraftDraft]):
    """

    path: str
    summary: str
    description: str
    content: str
    language: NewScriptWithDraftLanguage
    hash_: str
    parent_hash: Union[Unset, str] = UNSET
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
    dedicated_worker: Union[Unset, bool] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    restart_unless_cancelled: Union[Unset, bool] = UNSET
    timeout: Union[Unset, int] = UNSET
    delete_after_use: Union[Unset, bool] = UNSET
    deployment_message: Union[Unset, str] = UNSET
    concurrency_key: Union[Unset, str] = UNSET
    visible_to_runner_only: Union[Unset, bool] = UNSET
    no_main_func: Union[Unset, bool] = UNSET
    codebase: Union[Unset, str] = UNSET
    has_preprocessor: Union[Unset, bool] = UNSET
    on_behalf_of_email: Union[Unset, str] = UNSET
    draft: Union[Unset, "NewScriptWithDraftDraft"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        description = self.description
        content = self.content
        language = self.language.value

        hash_ = self.hash_
        parent_hash = self.parent_hash
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
        dedicated_worker = self.dedicated_worker
        ws_error_handler_muted = self.ws_error_handler_muted
        priority = self.priority
        restart_unless_cancelled = self.restart_unless_cancelled
        timeout = self.timeout
        delete_after_use = self.delete_after_use
        deployment_message = self.deployment_message
        concurrency_key = self.concurrency_key
        visible_to_runner_only = self.visible_to_runner_only
        no_main_func = self.no_main_func
        codebase = self.codebase
        has_preprocessor = self.has_preprocessor
        on_behalf_of_email = self.on_behalf_of_email
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "summary": summary,
                "description": description,
                "content": content,
                "language": language,
                "hash": hash_,
            }
        )
        if parent_hash is not UNSET:
            field_dict["parent_hash"] = parent_hash
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
        if delete_after_use is not UNSET:
            field_dict["delete_after_use"] = delete_after_use
        if deployment_message is not UNSET:
            field_dict["deployment_message"] = deployment_message
        if concurrency_key is not UNSET:
            field_dict["concurrency_key"] = concurrency_key
        if visible_to_runner_only is not UNSET:
            field_dict["visible_to_runner_only"] = visible_to_runner_only
        if no_main_func is not UNSET:
            field_dict["no_main_func"] = no_main_func
        if codebase is not UNSET:
            field_dict["codebase"] = codebase
        if has_preprocessor is not UNSET:
            field_dict["has_preprocessor"] = has_preprocessor
        if on_behalf_of_email is not UNSET:
            field_dict["on_behalf_of_email"] = on_behalf_of_email
        if draft is not UNSET:
            field_dict["draft"] = draft

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_script_with_draft_draft import NewScriptWithDraftDraft
        from ..models.new_script_with_draft_schema import NewScriptWithDraftSchema

        d = src_dict.copy()
        path = d.pop("path")

        summary = d.pop("summary")

        description = d.pop("description")

        content = d.pop("content")

        language = NewScriptWithDraftLanguage(d.pop("language"))

        hash_ = d.pop("hash")

        parent_hash = d.pop("parent_hash", UNSET)

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

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        priority = d.pop("priority", UNSET)

        restart_unless_cancelled = d.pop("restart_unless_cancelled", UNSET)

        timeout = d.pop("timeout", UNSET)

        delete_after_use = d.pop("delete_after_use", UNSET)

        deployment_message = d.pop("deployment_message", UNSET)

        concurrency_key = d.pop("concurrency_key", UNSET)

        visible_to_runner_only = d.pop("visible_to_runner_only", UNSET)

        no_main_func = d.pop("no_main_func", UNSET)

        codebase = d.pop("codebase", UNSET)

        has_preprocessor = d.pop("has_preprocessor", UNSET)

        on_behalf_of_email = d.pop("on_behalf_of_email", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, NewScriptWithDraftDraft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = NewScriptWithDraftDraft.from_dict(_draft)

        new_script_with_draft = cls(
            path=path,
            summary=summary,
            description=description,
            content=content,
            language=language,
            hash_=hash_,
            parent_hash=parent_hash,
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
            dedicated_worker=dedicated_worker,
            ws_error_handler_muted=ws_error_handler_muted,
            priority=priority,
            restart_unless_cancelled=restart_unless_cancelled,
            timeout=timeout,
            delete_after_use=delete_after_use,
            deployment_message=deployment_message,
            concurrency_key=concurrency_key,
            visible_to_runner_only=visible_to_runner_only,
            no_main_func=no_main_func,
            codebase=codebase,
            has_preprocessor=has_preprocessor,
            on_behalf_of_email=on_behalf_of_email,
            draft=draft,
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

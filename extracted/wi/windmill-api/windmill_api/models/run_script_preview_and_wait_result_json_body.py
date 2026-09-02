from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_script_preview_and_wait_result_json_body_kind import RunScriptPreviewAndWaitResultJsonBodyKind
from ..models.run_script_preview_and_wait_result_json_body_language import RunScriptPreviewAndWaitResultJsonBodyLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_script_preview_and_wait_result_json_body_args import RunScriptPreviewAndWaitResultJsonBodyArgs
    from ..models.run_script_preview_and_wait_result_json_body_modules import (
        RunScriptPreviewAndWaitResultJsonBodyModules,
    )
    from ..models.run_script_preview_and_wait_result_json_body_temp_script_refs import (
        RunScriptPreviewAndWaitResultJsonBodyTempScriptRefs,
    )


T = TypeVar("T", bound="RunScriptPreviewAndWaitResultJsonBody")


@_attrs_define
class RunScriptPreviewAndWaitResultJsonBody:
    """
    Attributes:
        args (RunScriptPreviewAndWaitResultJsonBodyArgs): The arguments to pass to the script or flow
        content (Union[Unset, str]): The code to run
        path (Union[Unset, str]): The path to the script
        script_hash (Union[Unset, str]): The hash of the script
        language (Union[Unset, RunScriptPreviewAndWaitResultJsonBodyLanguage]):
        tag (Union[Unset, str]):
        kind (Union[Unset, RunScriptPreviewAndWaitResultJsonBodyKind]):
        dedicated_worker (Union[Unset, bool]):
        lock (Union[Unset, str]):
        flow_path (Union[Unset, str]):
        modules (Union[Unset, None, RunScriptPreviewAndWaitResultJsonBodyModules]): Additional script modules keyed by
            relative file path
        temp_script_refs (Union[Unset, None, RunScriptPreviewAndWaitResultJsonBodyTempScriptRefs]): Map of relative-
            import script path -> temp storage hash so the preview job resolves those imports from not-yet-deployed local
            content instead of the deployed script
    """

    args: "RunScriptPreviewAndWaitResultJsonBodyArgs"
    content: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    script_hash: Union[Unset, str] = UNSET
    language: Union[Unset, RunScriptPreviewAndWaitResultJsonBodyLanguage] = UNSET
    tag: Union[Unset, str] = UNSET
    kind: Union[Unset, RunScriptPreviewAndWaitResultJsonBodyKind] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    lock: Union[Unset, str] = UNSET
    flow_path: Union[Unset, str] = UNSET
    modules: Union[Unset, None, "RunScriptPreviewAndWaitResultJsonBodyModules"] = UNSET
    temp_script_refs: Union[Unset, None, "RunScriptPreviewAndWaitResultJsonBodyTempScriptRefs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        args = self.args.to_dict()

        content = self.content
        path = self.path
        script_hash = self.script_hash
        language: Union[Unset, str] = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        tag = self.tag
        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        dedicated_worker = self.dedicated_worker
        lock = self.lock
        flow_path = self.flow_path
        modules: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.modules, Unset):
            modules = self.modules.to_dict() if self.modules else None

        temp_script_refs: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.temp_script_refs, Unset):
            temp_script_refs = self.temp_script_refs.to_dict() if self.temp_script_refs else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "args": args,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if path is not UNSET:
            field_dict["path"] = path
        if script_hash is not UNSET:
            field_dict["script_hash"] = script_hash
        if language is not UNSET:
            field_dict["language"] = language
        if tag is not UNSET:
            field_dict["tag"] = tag
        if kind is not UNSET:
            field_dict["kind"] = kind
        if dedicated_worker is not UNSET:
            field_dict["dedicated_worker"] = dedicated_worker
        if lock is not UNSET:
            field_dict["lock"] = lock
        if flow_path is not UNSET:
            field_dict["flow_path"] = flow_path
        if modules is not UNSET:
            field_dict["modules"] = modules
        if temp_script_refs is not UNSET:
            field_dict["temp_script_refs"] = temp_script_refs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_script_preview_and_wait_result_json_body_args import RunScriptPreviewAndWaitResultJsonBodyArgs
        from ..models.run_script_preview_and_wait_result_json_body_modules import (
            RunScriptPreviewAndWaitResultJsonBodyModules,
        )
        from ..models.run_script_preview_and_wait_result_json_body_temp_script_refs import (
            RunScriptPreviewAndWaitResultJsonBodyTempScriptRefs,
        )

        d = src_dict.copy()
        args = RunScriptPreviewAndWaitResultJsonBodyArgs.from_dict(d.pop("args"))

        content = d.pop("content", UNSET)

        path = d.pop("path", UNSET)

        script_hash = d.pop("script_hash", UNSET)

        _language = d.pop("language", UNSET)
        language: Union[Unset, RunScriptPreviewAndWaitResultJsonBodyLanguage]
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = RunScriptPreviewAndWaitResultJsonBodyLanguage(_language)

        tag = d.pop("tag", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, RunScriptPreviewAndWaitResultJsonBodyKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = RunScriptPreviewAndWaitResultJsonBodyKind(_kind)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        lock = d.pop("lock", UNSET)

        flow_path = d.pop("flow_path", UNSET)

        _modules = d.pop("modules", UNSET)
        modules: Union[Unset, None, RunScriptPreviewAndWaitResultJsonBodyModules]
        if _modules is None:
            modules = None
        elif isinstance(_modules, Unset):
            modules = UNSET
        else:
            modules = RunScriptPreviewAndWaitResultJsonBodyModules.from_dict(_modules)

        _temp_script_refs = d.pop("temp_script_refs", UNSET)
        temp_script_refs: Union[Unset, None, RunScriptPreviewAndWaitResultJsonBodyTempScriptRefs]
        if _temp_script_refs is None:
            temp_script_refs = None
        elif isinstance(_temp_script_refs, Unset):
            temp_script_refs = UNSET
        else:
            temp_script_refs = RunScriptPreviewAndWaitResultJsonBodyTempScriptRefs.from_dict(_temp_script_refs)

        run_script_preview_and_wait_result_json_body = cls(
            args=args,
            content=content,
            path=path,
            script_hash=script_hash,
            language=language,
            tag=tag,
            kind=kind,
            dedicated_worker=dedicated_worker,
            lock=lock,
            flow_path=flow_path,
            modules=modules,
            temp_script_refs=temp_script_refs,
        )

        run_script_preview_and_wait_result_json_body.additional_properties = d
        return run_script_preview_and_wait_result_json_body

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

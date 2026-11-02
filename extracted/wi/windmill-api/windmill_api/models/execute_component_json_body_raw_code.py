from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execute_component_json_body_raw_code_modules import ExecuteComponentJsonBodyRawCodeModules


T = TypeVar("T", bound="ExecuteComponentJsonBodyRawCode")


@_attrs_define
class ExecuteComponentJsonBodyRawCode:
    """
    Attributes:
        content (str):
        language (str):
        path (Union[Unset, str]):
        lock (Union[Unset, str]):
        cache_ttl (Union[Unset, int]):
        tag (Union[Unset, str]):
        modules (Union[Unset, None, ExecuteComponentJsonBodyRawCodeModules]): Additional modules keyed by relative file
            path. Honored in preview only: a deployed app runs the modules stored with its runnable.
    """

    content: str
    language: str
    path: Union[Unset, str] = UNSET
    lock: Union[Unset, str] = UNSET
    cache_ttl: Union[Unset, int] = UNSET
    tag: Union[Unset, str] = UNSET
    modules: Union[Unset, None, "ExecuteComponentJsonBodyRawCodeModules"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content
        language = self.language
        path = self.path
        lock = self.lock
        cache_ttl = self.cache_ttl
        tag = self.tag
        modules: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.modules, Unset):
            modules = self.modules.to_dict() if self.modules else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "language": language,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if lock is not UNSET:
            field_dict["lock"] = lock
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if tag is not UNSET:
            field_dict["tag"] = tag
        if modules is not UNSET:
            field_dict["modules"] = modules

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.execute_component_json_body_raw_code_modules import ExecuteComponentJsonBodyRawCodeModules

        d = src_dict.copy()
        content = d.pop("content")

        language = d.pop("language")

        path = d.pop("path", UNSET)

        lock = d.pop("lock", UNSET)

        cache_ttl = d.pop("cache_ttl", UNSET)

        tag = d.pop("tag", UNSET)

        _modules = d.pop("modules", UNSET)
        modules: Union[Unset, None, ExecuteComponentJsonBodyRawCodeModules]
        if _modules is None:
            modules = None
        elif isinstance(_modules, Unset):
            modules = UNSET
        else:
            modules = ExecuteComponentJsonBodyRawCodeModules.from_dict(_modules)

        execute_component_json_body_raw_code = cls(
            content=content,
            language=language,
            path=path,
            lock=lock,
            cache_ttl=cache_ttl,
            tag=tag,
            modules=modules,
        )

        execute_component_json_body_raw_code.additional_properties = d
        return execute_component_json_body_raw_code

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

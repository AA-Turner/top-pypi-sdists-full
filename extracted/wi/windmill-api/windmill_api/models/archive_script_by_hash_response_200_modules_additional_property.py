from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.archive_script_by_hash_response_200_modules_additional_property_language import (
    ArchiveScriptByHashResponse200ModulesAdditionalPropertyLanguage,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArchiveScriptByHashResponse200ModulesAdditionalProperty")


@_attrs_define
class ArchiveScriptByHashResponse200ModulesAdditionalProperty:
    """An additional module file associated with a script

    Attributes:
        content (str): The source code content of this module
        language (ArchiveScriptByHashResponse200ModulesAdditionalPropertyLanguage):
        lock (Union[Unset, None, str]): Lock file content for this module's dependencies
    """

    content: str
    language: ArchiveScriptByHashResponse200ModulesAdditionalPropertyLanguage
    lock: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content
        language = self.language.value

        lock = self.lock

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "language": language,
            }
        )
        if lock is not UNSET:
            field_dict["lock"] = lock

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        language = ArchiveScriptByHashResponse200ModulesAdditionalPropertyLanguage(d.pop("language"))

        lock = d.pop("lock", UNSET)

        archive_script_by_hash_response_200_modules_additional_property = cls(
            content=content,
            language=language,
            lock=lock,
        )

        archive_script_by_hash_response_200_modules_additional_property.additional_properties = d
        return archive_script_by_hash_response_200_modules_additional_property

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

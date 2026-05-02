from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dynamic_input_data_runnable_ref_type_1_language import DynamicInputDataRunnableRefType1Language
from ..models.dynamic_input_data_runnable_ref_type_1_source import DynamicInputDataRunnableRefType1Source
from ..types import UNSET, Unset

T = TypeVar("T", bound="DynamicInputDataRunnableRefType1")


@_attrs_define
class DynamicInputDataRunnableRefType1:
    """
    Attributes:
        source (DynamicInputDataRunnableRefType1Source):
        code (str): Code content for inline execution
        language (Union[Unset, DynamicInputDataRunnableRefType1Language]):
    """

    source: DynamicInputDataRunnableRefType1Source
    code: str
    language: Union[Unset, DynamicInputDataRunnableRefType1Language] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source.value

        code = self.code
        language: Union[Unset, str] = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "code": code,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = DynamicInputDataRunnableRefType1Source(d.pop("source"))

        code = d.pop("code")

        _language = d.pop("language", UNSET)
        language: Union[Unset, DynamicInputDataRunnableRefType1Language]
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = DynamicInputDataRunnableRefType1Language(_language)

        dynamic_input_data_runnable_ref_type_1 = cls(
            source=source,
            code=code,
            language=language,
        )

        dynamic_input_data_runnable_ref_type_1.additional_properties = d
        return dynamic_input_data_runnable_ref_type_1

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

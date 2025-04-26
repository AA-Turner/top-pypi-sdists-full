from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.template_script_language import TemplateScriptLanguage

if TYPE_CHECKING:
    from ..models.template_script_relations_item import TemplateScriptRelationsItem


T = TypeVar("T", bound="TemplateScript")


@_attrs_define
class TemplateScript:
    """
    Attributes:
        postgres_resource_path (str):
        relations (List['TemplateScriptRelationsItem']):
        language (TemplateScriptLanguage):
    """

    postgres_resource_path: str
    relations: List["TemplateScriptRelationsItem"]
    language: TemplateScriptLanguage
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        postgres_resource_path = self.postgres_resource_path
        relations = []
        for relations_item_data in self.relations:
            relations_item = relations_item_data.to_dict()

            relations.append(relations_item)

        language = self.language.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "postgres_resource_path": postgres_resource_path,
                "relations": relations,
                "language": language,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.template_script_relations_item import TemplateScriptRelationsItem

        d = src_dict.copy()
        postgres_resource_path = d.pop("postgres_resource_path")

        relations = []
        _relations = d.pop("relations")
        for relations_item_data in _relations:
            relations_item = TemplateScriptRelationsItem.from_dict(relations_item_data)

            relations.append(relations_item)

        language = TemplateScriptLanguage(d.pop("language"))

        template_script = cls(
            postgres_resource_path=postgres_resource_path,
            relations=relations,
            language=language,
        )

        template_script.additional_properties = d
        return template_script

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

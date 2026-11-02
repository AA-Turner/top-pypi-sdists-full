from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_template_script_json_body_language import CreateTemplateScriptJsonBodyLanguage

if TYPE_CHECKING:
    from ..models.create_template_script_json_body_relations_item import CreateTemplateScriptJsonBodyRelationsItem


T = TypeVar("T", bound="CreateTemplateScriptJsonBody")


@_attrs_define
class CreateTemplateScriptJsonBody:
    """
    Attributes:
        postgres_resource_path (str):
        relations (List['CreateTemplateScriptJsonBodyRelationsItem']):
        language (CreateTemplateScriptJsonBodyLanguage):
    """

    postgres_resource_path: str
    relations: List["CreateTemplateScriptJsonBodyRelationsItem"]
    language: CreateTemplateScriptJsonBodyLanguage
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
        from ..models.create_template_script_json_body_relations_item import CreateTemplateScriptJsonBodyRelationsItem

        d = src_dict.copy()
        postgres_resource_path = d.pop("postgres_resource_path")

        relations = []
        _relations = d.pop("relations")
        for relations_item_data in _relations:
            relations_item = CreateTemplateScriptJsonBodyRelationsItem.from_dict(relations_item_data)

            relations.append(relations_item)

        language = CreateTemplateScriptJsonBodyLanguage(d.pop("language"))

        create_template_script_json_body = cls(
            postgres_resource_path=postgres_resource_path,
            relations=relations,
            language=language,
        )

        create_template_script_json_body.additional_properties = d
        return create_template_script_json_body

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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.upload_ai_skills_json_body_skills_item import UploadAiSkillsJsonBodySkillsItem


T = TypeVar("T", bound="UploadAiSkillsJsonBody")


@_attrs_define
class UploadAiSkillsJsonBody:
    """
    Attributes:
        skills (List['UploadAiSkillsJsonBodySkillsItem']):
    """

    skills: List["UploadAiSkillsJsonBodySkillsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        skills = []
        for skills_item_data in self.skills:
            skills_item = skills_item_data.to_dict()

            skills.append(skills_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "skills": skills,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.upload_ai_skills_json_body_skills_item import UploadAiSkillsJsonBodySkillsItem

        d = src_dict.copy()
        skills = []
        _skills = d.pop("skills")
        for skills_item_data in _skills:
            skills_item = UploadAiSkillsJsonBodySkillsItem.from_dict(skills_item_data)

            skills.append(skills_item)

        upload_ai_skills_json_body = cls(
            skills=skills,
        )

        upload_ai_skills_json_body.additional_properties = d
        return upload_ai_skills_json_body

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

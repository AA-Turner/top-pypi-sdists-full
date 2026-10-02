from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rancher_template_question import RancherTemplateQuestion


T = TypeVar("T", bound="TemplateVersion")


@_attrs_define
class TemplateVersion:
    """
    Attributes:
        readme (str):
        app_readme (str):
        questions (list['RancherTemplateQuestion']):
    """

    readme: str
    app_readme: str
    questions: list["RancherTemplateQuestion"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        readme = self.readme

        app_readme = self.app_readme

        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "readme": readme,
                "app_readme": app_readme,
                "questions": questions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_template_question import RancherTemplateQuestion

        d = dict(src_dict)
        readme = d.pop("readme")

        app_readme = d.pop("app_readme")

        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = RancherTemplateQuestion.from_dict(questions_item_data)

            questions.append(questions_item)

        template_version = cls(
            readme=readme,
            app_readme=app_readme,
            questions=questions,
        )

        template_version.additional_properties = d
        return template_version

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

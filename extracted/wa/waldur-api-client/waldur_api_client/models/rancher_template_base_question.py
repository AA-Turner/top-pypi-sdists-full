from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rancher_template_question_type import RancherTemplateQuestionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherTemplateBaseQuestion")


@_attrs_define
class RancherTemplateBaseQuestion:
    """
    Attributes:
        label (str):
        variable (str):
        type_ (RancherTemplateQuestionType):
        description (Union[Unset, str]):
        required (Union[Unset, bool]):
        validate (Union[Unset, Any]):
        default (Union[None, Unset, str]):
        group (Union[Unset, str]):
        show_if (Union[Unset, str]):
    """

    label: str
    variable: str
    type_: RancherTemplateQuestionType
    description: Union[Unset, str] = UNSET
    required: Union[Unset, bool] = UNSET
    validate: Union[Unset, Any] = UNSET
    default: Union[None, Unset, str] = UNSET
    group: Union[Unset, str] = UNSET
    show_if: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        variable = self.variable

        type_ = self.type_.value

        description = self.description

        required = self.required

        validate = self.validate

        default: Union[None, Unset, str]
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        group = self.group

        show_if = self.show_if

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "variable": variable,
                "type": type_,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if required is not UNSET:
            field_dict["required"] = required
        if validate is not UNSET:
            field_dict["validate_"] = validate
        if default is not UNSET:
            field_dict["default"] = default
        if group is not UNSET:
            field_dict["group"] = group
        if show_if is not UNSET:
            field_dict["showIf"] = show_if

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        variable = d.pop("variable")

        type_ = RancherTemplateQuestionType(d.pop("type"))

        description = d.pop("description", UNSET)

        required = d.pop("required", UNSET)

        validate = d.pop("validate_", UNSET)

        def _parse_default(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default = _parse_default(d.pop("default", UNSET))

        group = d.pop("group", UNSET)

        show_if = d.pop("showIf", UNSET)

        rancher_template_base_question = cls(
            label=label,
            variable=variable,
            type_=type_,
            description=description,
            required=required,
            validate=validate,
            default=default,
            group=group,
            show_if=show_if,
        )

        rancher_template_base_question.additional_properties = d
        return rancher_template_base_question

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

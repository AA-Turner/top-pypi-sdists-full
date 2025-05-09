from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_copilot_config_json_body_code_completion_model import (
        EditCopilotConfigJsonBodyCodeCompletionModel,
    )
    from ..models.edit_copilot_config_json_body_default_model import EditCopilotConfigJsonBodyDefaultModel
    from ..models.edit_copilot_config_json_body_providers import EditCopilotConfigJsonBodyProviders


T = TypeVar("T", bound="EditCopilotConfigJsonBody")


@_attrs_define
class EditCopilotConfigJsonBody:
    """
    Attributes:
        providers (Union[Unset, EditCopilotConfigJsonBodyProviders]):
        default_model (Union[Unset, EditCopilotConfigJsonBodyDefaultModel]):
        code_completion_model (Union[Unset, EditCopilotConfigJsonBodyCodeCompletionModel]):
    """

    providers: Union[Unset, "EditCopilotConfigJsonBodyProviders"] = UNSET
    default_model: Union[Unset, "EditCopilotConfigJsonBodyDefaultModel"] = UNSET
    code_completion_model: Union[Unset, "EditCopilotConfigJsonBodyCodeCompletionModel"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        providers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers.to_dict()

        default_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_model, Unset):
            default_model = self.default_model.to_dict()

        code_completion_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_completion_model, Unset):
            code_completion_model = self.code_completion_model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if providers is not UNSET:
            field_dict["providers"] = providers
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if code_completion_model is not UNSET:
            field_dict["code_completion_model"] = code_completion_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_copilot_config_json_body_code_completion_model import (
            EditCopilotConfigJsonBodyCodeCompletionModel,
        )
        from ..models.edit_copilot_config_json_body_default_model import EditCopilotConfigJsonBodyDefaultModel
        from ..models.edit_copilot_config_json_body_providers import EditCopilotConfigJsonBodyProviders

        d = src_dict.copy()
        _providers = d.pop("providers", UNSET)
        providers: Union[Unset, EditCopilotConfigJsonBodyProviders]
        if isinstance(_providers, Unset):
            providers = UNSET
        else:
            providers = EditCopilotConfigJsonBodyProviders.from_dict(_providers)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, EditCopilotConfigJsonBodyDefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = EditCopilotConfigJsonBodyDefaultModel.from_dict(_default_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, EditCopilotConfigJsonBodyCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = EditCopilotConfigJsonBodyCodeCompletionModel.from_dict(_code_completion_model)

        edit_copilot_config_json_body = cls(
            providers=providers,
            default_model=default_model,
            code_completion_model=code_completion_model,
        )

        edit_copilot_config_json_body.additional_properties = d
        return edit_copilot_config_json_body

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

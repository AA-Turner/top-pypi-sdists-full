from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instance_ai_summary_code_completion_model import InstanceAISummaryCodeCompletionModel
    from ..models.instance_ai_summary_default_model import InstanceAISummaryDefaultModel
    from ..models.instance_ai_summary_providers_item import InstanceAISummaryProvidersItem


T = TypeVar("T", bound="InstanceAISummary")


@_attrs_define
class InstanceAISummary:
    """
    Attributes:
        providers (List['InstanceAISummaryProvidersItem']):
        default_model (Union[Unset, InstanceAISummaryDefaultModel]):
        code_completion_model (Union[Unset, InstanceAISummaryCodeCompletionModel]):
    """

    providers: List["InstanceAISummaryProvidersItem"]
    default_model: Union[Unset, "InstanceAISummaryDefaultModel"] = UNSET
    code_completion_model: Union[Unset, "InstanceAISummaryCodeCompletionModel"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()

            providers.append(providers_item)

        default_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_model, Unset):
            default_model = self.default_model.to_dict()

        code_completion_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_completion_model, Unset):
            code_completion_model = self.code_completion_model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "providers": providers,
            }
        )
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if code_completion_model is not UNSET:
            field_dict["code_completion_model"] = code_completion_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instance_ai_summary_code_completion_model import InstanceAISummaryCodeCompletionModel
        from ..models.instance_ai_summary_default_model import InstanceAISummaryDefaultModel
        from ..models.instance_ai_summary_providers_item import InstanceAISummaryProvidersItem

        d = src_dict.copy()
        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = InstanceAISummaryProvidersItem.from_dict(providers_item_data)

            providers.append(providers_item)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, InstanceAISummaryDefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = InstanceAISummaryDefaultModel.from_dict(_default_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, InstanceAISummaryCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = InstanceAISummaryCodeCompletionModel.from_dict(_code_completion_model)

        instance_ai_summary = cls(
            providers=providers,
            default_model=default_model,
            code_completion_model=code_completion_model,
        )

        instance_ai_summary.additional_properties = d
        return instance_ai_summary

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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.complete_ai_json_body_model import CompleteAiJsonBodyModel


T = TypeVar("T", bound="CompleteAiJsonBody")


@_attrs_define
class CompleteAiJsonBody:
    """
    Attributes:
        system (str):
        user (str):
        model (Union[Unset, CompleteAiJsonBodyModel]): defaults to the AI config's default model
        max_tokens (Union[Unset, int]):
    """

    system: str
    user: str
    model: Union[Unset, "CompleteAiJsonBodyModel"] = UNSET
    max_tokens: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        system = self.system
        user = self.user
        model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        max_tokens = self.max_tokens

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "system": system,
                "user": user,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.complete_ai_json_body_model import CompleteAiJsonBodyModel

        d = src_dict.copy()
        system = d.pop("system")

        user = d.pop("user")

        _model = d.pop("model", UNSET)
        model: Union[Unset, CompleteAiJsonBodyModel]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = CompleteAiJsonBodyModel.from_dict(_model)

        max_tokens = d.pop("max_tokens", UNSET)

        complete_ai_json_body = cls(
            system=system,
            user=user,
            model=model,
            max_tokens=max_tokens,
        )

        complete_ai_json_body.additional_properties = d
        return complete_ai_json_body

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

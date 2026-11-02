from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.complete_ai_response_200_model import CompleteAiResponse200Model


T = TypeVar("T", bound="CompleteAiResponse200")


@_attrs_define
class CompleteAiResponse200:
    """
    Attributes:
        text (str):
        model (CompleteAiResponse200Model):
    """

    text: str
    model: "CompleteAiResponse200Model"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        model = self.model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "model": model,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.complete_ai_response_200_model import CompleteAiResponse200Model

        d = src_dict.copy()
        text = d.pop("text")

        model = CompleteAiResponse200Model.from_dict(d.pop("model"))

        complete_ai_response_200 = cls(
            text=text,
            model=model,
        )

        complete_ai_response_200.additional_properties = d
        return complete_ai_response_200

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

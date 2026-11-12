from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_decision_type import AiDecisionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_decision_input_transforms import AiDecisionInputTransforms


T = TypeVar("T", bound="AiDecision")


@_attrs_define
class AiDecision:
    """AI decision step: one call to a decision model (TypeSafe's Jev, Cloudflare's
    Jev-compatible Clef, or OpenAI's or Gemini's Decisions API) that answers typed questions about a
    state with calibrated probabilities, instead of generating text.
    Prefer it over an AI agent to classify, route, score or check something: it is fast,
    cheap and its answers are structured. Its result is { output: { <question name>: answer },
    model, usage }, so a later step reads e.g. results.<id>.output.intent.choice. To route on
    the answers, follow it with a branchone whose branch exprs read
    results.<id>.output.<question>.choice. Usable as an AI agent tool, where the calling agent
    supplies the state.

        Attributes:
            input_transforms (AiDecisionInputTransforms): Input parameters for the decision mapped to their values
            type (AiDecisionType):
            tag (Union[Unset, str]): Worker group tag for execution routing. If not set, the step runs on the flow's tag
                (default `flow`)
    """

    input_transforms: "AiDecisionInputTransforms"
    type: AiDecisionType
    tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        type = self.type.value

        tag = self.tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "type": type,
            }
        )
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_decision_input_transforms import AiDecisionInputTransforms

        d = src_dict.copy()
        input_transforms = AiDecisionInputTransforms.from_dict(d.pop("input_transforms"))

        type = AiDecisionType(d.pop("type"))

        tag = d.pop("tag", UNSET)

        ai_decision = cls(
            input_transforms=input_transforms,
            type=type,
            tag=tag,
        )

        ai_decision.additional_properties = d
        return ai_decision

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

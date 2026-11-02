from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_decision_input_transforms_provider_type_0 import AiDecisionInputTransformsProviderType0
    from ..models.ai_decision_input_transforms_provider_type_1 import AiDecisionInputTransformsProviderType1
    from ..models.ai_decision_input_transforms_provider_type_2 import AiDecisionInputTransformsProviderType2
    from ..models.ai_decision_input_transforms_questions import AiDecisionInputTransformsQuestions
    from ..models.ai_decision_input_transforms_state import AiDecisionInputTransformsState


T = TypeVar("T", bound="AiDecisionInputTransforms")


@_attrs_define
class AiDecisionInputTransforms:
    """Input parameters for the decision mapped to their values

    Attributes:
        provider (Union['AiDecisionInputTransformsProviderType0', 'AiDecisionInputTransformsProviderType1',
            'AiDecisionInputTransformsProviderType2']): Provider configuration - can be static (ProviderConfig), JavaScript
            expression, or AI-determined
        state (AiDecisionInputTransformsState): What the questions are asked about: a string, an object or an array of
            strings.
            An object with descriptive keys holding only what the questions need works best.
            Example: { message: flow_input.message, plan: results.a.plan }
        questions (AiDecisionInputTransformsQuestions): Object mapping each question name to { type, instructions,
            criteria }, where type is:
            - 'choice': criteria maps each option to its description (up to 255); the answer
              has choice, probabilities and confidence
            - 'score': criteria is an ordered array of 2 to 10 level descriptions; the answer
              has score, legend, probabilities and confidence
            - 'noul': yes/no, criteria optionally { true, false } descriptions; the answer has
              noul, the probability of yes (0 to 1)
            Example: { intent: { type: 'choice', instructions: 'What does the customer want?',
            criteria: { refund: 'Money back', bug: 'Something is broken' } } }
    """

    provider: Union[
        "AiDecisionInputTransformsProviderType0",
        "AiDecisionInputTransformsProviderType1",
        "AiDecisionInputTransformsProviderType2",
    ]
    state: "AiDecisionInputTransformsState"
    questions: "AiDecisionInputTransformsQuestions"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_decision_input_transforms_provider_type_0 import AiDecisionInputTransformsProviderType0
        from ..models.ai_decision_input_transforms_provider_type_1 import AiDecisionInputTransformsProviderType1

        provider: Dict[str, Any]

        if isinstance(self.provider, AiDecisionInputTransformsProviderType0):
            provider = self.provider.to_dict()

        elif isinstance(self.provider, AiDecisionInputTransformsProviderType1):
            provider = self.provider.to_dict()

        else:
            provider = self.provider.to_dict()

        state = self.state.to_dict()

        questions = self.questions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "state": state,
                "questions": questions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_decision_input_transforms_provider_type_0 import AiDecisionInputTransformsProviderType0
        from ..models.ai_decision_input_transforms_provider_type_1 import AiDecisionInputTransformsProviderType1
        from ..models.ai_decision_input_transforms_provider_type_2 import AiDecisionInputTransformsProviderType2
        from ..models.ai_decision_input_transforms_questions import AiDecisionInputTransformsQuestions
        from ..models.ai_decision_input_transforms_state import AiDecisionInputTransformsState

        d = src_dict.copy()

        def _parse_provider(
            data: object,
        ) -> Union[
            "AiDecisionInputTransformsProviderType0",
            "AiDecisionInputTransformsProviderType1",
            "AiDecisionInputTransformsProviderType2",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                provider_type_0 = AiDecisionInputTransformsProviderType0.from_dict(data)

                return provider_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                provider_type_1 = AiDecisionInputTransformsProviderType1.from_dict(data)

                return provider_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            provider_type_2 = AiDecisionInputTransformsProviderType2.from_dict(data)

            return provider_type_2

        provider = _parse_provider(d.pop("provider"))

        state = AiDecisionInputTransformsState.from_dict(d.pop("state"))

        questions = AiDecisionInputTransformsQuestions.from_dict(d.pop("questions"))

        ai_decision_input_transforms = cls(
            provider=provider,
            state=state,
            questions=questions,
        )

        ai_decision_input_transforms.additional_properties = d
        return ai_decision_input_transforms

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

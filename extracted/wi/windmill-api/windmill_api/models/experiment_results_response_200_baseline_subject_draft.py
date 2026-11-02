from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_results_response_200_baseline_subject_draft_input_transforms import (
        ExperimentResultsResponse200BaselineSubjectDraftInputTransforms,
    )
    from ..models.experiment_results_response_200_baseline_subject_draft_tools_item import (
        ExperimentResultsResponse200BaselineSubjectDraftToolsItem,
    )


T = TypeVar("T", bound="ExperimentResultsResponse200BaselineSubjectDraft")


@_attrs_define
class ExperimentResultsResponse200BaselineSubjectDraft:
    """The brain and tools of an agent, as the flow editor holds them. Carried by the request and present exactly when the
    subject kind is `agent_draft` — the edits exist only in the editor — where it is the whole definition of what ran:
    the run goes through the same unlinked branch of the agent executor the editor's own test uses.

        Attributes:
            input_transforms (Union[Unset, ExperimentResultsResponse200BaselineSubjectDraftInputTransforms]): The agent's
                input transforms: provider, system prompt, output type and the rest. The message and attachments come from the
                case and override anything named here.
            tools (Union[Unset, List['ExperimentResultsResponse200BaselineSubjectDraftToolsItem']]):
    """

    input_transforms: Union[Unset, "ExperimentResultsResponse200BaselineSubjectDraftInputTransforms"] = UNSET
    tools: Union[Unset, List["ExperimentResultsResponse200BaselineSubjectDraftToolsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_transforms, Unset):
            input_transforms = self.input_transforms.to_dict()

        tools: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()

                tools.append(tools_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_transforms is not UNSET:
            field_dict["input_transforms"] = input_transforms
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.experiment_results_response_200_baseline_subject_draft_input_transforms import (
            ExperimentResultsResponse200BaselineSubjectDraftInputTransforms,
        )
        from ..models.experiment_results_response_200_baseline_subject_draft_tools_item import (
            ExperimentResultsResponse200BaselineSubjectDraftToolsItem,
        )

        d = src_dict.copy()
        _input_transforms = d.pop("input_transforms", UNSET)
        input_transforms: Union[Unset, ExperimentResultsResponse200BaselineSubjectDraftInputTransforms]
        if isinstance(_input_transforms, Unset):
            input_transforms = UNSET
        else:
            input_transforms = ExperimentResultsResponse200BaselineSubjectDraftInputTransforms.from_dict(
                _input_transforms
            )

        tools = []
        _tools = d.pop("tools", UNSET)
        for tools_item_data in _tools or []:
            tools_item = ExperimentResultsResponse200BaselineSubjectDraftToolsItem.from_dict(tools_item_data)

            tools.append(tools_item)

        experiment_results_response_200_baseline_subject_draft = cls(
            input_transforms=input_transforms,
            tools=tools,
        )

        experiment_results_response_200_baseline_subject_draft.additional_properties = d
        return experiment_results_response_200_baseline_subject_draft

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

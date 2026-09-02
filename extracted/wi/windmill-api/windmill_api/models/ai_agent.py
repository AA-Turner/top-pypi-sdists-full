from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_agent_type import AiAgentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms import AiAgentInputTransforms
    from ..models.ai_agent_tool_inputs import AiAgentToolInputs
    from ..models.ai_agent_tools_item import AiAgentToolsItem


T = TypeVar("T", bound="AiAgent")


@_attrs_define
class AiAgent:
    """AI agent step that can use tools to accomplish tasks. The agent receives inputs and can call any of its configured
    tools to complete the task

        Attributes:
            input_transforms (AiAgentInputTransforms): Input parameters for the AI agent mapped to their values
            type (AiAgentType):
            tools (Union[Unset, List['AiAgentToolsItem']]): Array of tools the agent can use. The agent decides which tools
                to call based on the task
            tag (Union[Unset, str]): Worker group tag for execution routing. If not set, the AI agent step runs on the
                flow's tag (default `flow`)
            omit_output_from_conversation (Union[Unset, bool]): If true, this AI agent step does not persist its assistant
                or tool messages to the flow conversation when chat mode is enabled.
            agent (Union[Unset, str]): Path of a reusable `ai_agent` resource (hybrid linking). When set, the agent brain
                config (provider/model/system prompt/etc.) and tool set are resolved at runtime from
                that resource; the module's input_transforms then only carry the flow-local inputs
                (user_message/user_attachments).
            tool_inputs (Union[Unset, AiAgentToolInputs]): Host-local wiring for an agent's tool inputs, keyed by tool id
                then input key. Binds the
                referenced agent's tools to this flow's context (flow_input/results) without mutating the
                shared resource; overlaid onto the tools' input_transforms at runtime — including when
                `agent` is unset, since a step forked for editing keeps these overrides until it is saved
                back or unlinked.
            parallel (Union[Unset, bool]): If true, the agent can execute multiple tool calls in parallel
    """

    input_transforms: "AiAgentInputTransforms"
    type: AiAgentType
    tools: Union[Unset, List["AiAgentToolsItem"]] = UNSET
    tag: Union[Unset, str] = UNSET
    omit_output_from_conversation: Union[Unset, bool] = False
    agent: Union[Unset, str] = UNSET
    tool_inputs: Union[Unset, "AiAgentToolInputs"] = UNSET
    parallel: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        type = self.type.value

        tools: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()

                tools.append(tools_item)

        tag = self.tag
        omit_output_from_conversation = self.omit_output_from_conversation
        agent = self.agent
        tool_inputs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tool_inputs, Unset):
            tool_inputs = self.tool_inputs.to_dict()

        parallel = self.parallel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "type": type,
            }
        )
        if tools is not UNSET:
            field_dict["tools"] = tools
        if tag is not UNSET:
            field_dict["tag"] = tag
        if omit_output_from_conversation is not UNSET:
            field_dict["omit_output_from_conversation"] = omit_output_from_conversation
        if agent is not UNSET:
            field_dict["agent"] = agent
        if tool_inputs is not UNSET:
            field_dict["tool_inputs"] = tool_inputs
        if parallel is not UNSET:
            field_dict["parallel"] = parallel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms import AiAgentInputTransforms
        from ..models.ai_agent_tool_inputs import AiAgentToolInputs
        from ..models.ai_agent_tools_item import AiAgentToolsItem

        d = src_dict.copy()
        input_transforms = AiAgentInputTransforms.from_dict(d.pop("input_transforms"))

        type = AiAgentType(d.pop("type"))

        tools = []
        _tools = d.pop("tools", UNSET)
        for tools_item_data in _tools or []:
            tools_item = AiAgentToolsItem.from_dict(tools_item_data)

            tools.append(tools_item)

        tag = d.pop("tag", UNSET)

        omit_output_from_conversation = d.pop("omit_output_from_conversation", UNSET)

        agent = d.pop("agent", UNSET)

        _tool_inputs = d.pop("tool_inputs", UNSET)
        tool_inputs: Union[Unset, AiAgentToolInputs]
        if isinstance(_tool_inputs, Unset):
            tool_inputs = UNSET
        else:
            tool_inputs = AiAgentToolInputs.from_dict(_tool_inputs)

        parallel = d.pop("parallel", UNSET)

        ai_agent = cls(
            input_transforms=input_transforms,
            type=type,
            tools=tools,
            tag=tag,
            omit_output_from_conversation=omit_output_from_conversation,
            agent=agent,
            tool_inputs=tool_inputs,
            parallel=parallel,
        )

        ai_agent.additional_properties = d
        return ai_agent

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

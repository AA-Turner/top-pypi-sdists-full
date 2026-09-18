from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms_enabled_tools import AiAgentInputTransformsEnabledTools
    from ..models.ai_agent_input_transforms_max_completion_tokens import AiAgentInputTransformsMaxCompletionTokens
    from ..models.ai_agent_input_transforms_max_iterations import AiAgentInputTransformsMaxIterations
    from ..models.ai_agent_input_transforms_memory_id import AiAgentInputTransformsMemoryId
    from ..models.ai_agent_input_transforms_memory_type_0 import AiAgentInputTransformsMemoryType0
    from ..models.ai_agent_input_transforms_memory_type_1 import AiAgentInputTransformsMemoryType1
    from ..models.ai_agent_input_transforms_memory_type_2 import AiAgentInputTransformsMemoryType2
    from ..models.ai_agent_input_transforms_output_schema import AiAgentInputTransformsOutputSchema
    from ..models.ai_agent_input_transforms_output_type import AiAgentInputTransformsOutputType
    from ..models.ai_agent_input_transforms_previous_messages import AiAgentInputTransformsPreviousMessages
    from ..models.ai_agent_input_transforms_provider_type_0 import AiAgentInputTransformsProviderType0
    from ..models.ai_agent_input_transforms_provider_type_1 import AiAgentInputTransformsProviderType1
    from ..models.ai_agent_input_transforms_provider_type_2 import AiAgentInputTransformsProviderType2
    from ..models.ai_agent_input_transforms_streaming import AiAgentInputTransformsStreaming
    from ..models.ai_agent_input_transforms_system_prompt import AiAgentInputTransformsSystemPrompt
    from ..models.ai_agent_input_transforms_temperature import AiAgentInputTransformsTemperature
    from ..models.ai_agent_input_transforms_user_attachments import AiAgentInputTransformsUserAttachments
    from ..models.ai_agent_input_transforms_user_message import AiAgentInputTransformsUserMessage


T = TypeVar("T", bound="AiAgentInputTransforms")


@_attrs_define
class AiAgentInputTransforms:
    """Input parameters for the AI agent mapped to their values

    Attributes:
        provider (Union['AiAgentInputTransformsProviderType0', 'AiAgentInputTransformsProviderType1',
            'AiAgentInputTransformsProviderType2', Unset]): Provider configuration - can be static (ProviderConfig),
            JavaScript expression, or AI-determined
        output_type (Union[Unset, AiAgentInputTransformsOutputType]): Output format type.
            Valid values: 'text' (default) - plain text response, 'image' - image generation
        user_message (Union[Unset, AiAgentInputTransformsUserMessage]): The user's prompt/message to the AI agent.
            Supports variable interpolation with
            flow.input syntax. Required unless memory is off and `previous_messages` supplies
            the prompt; image output always needs it.
        system_prompt (Union[Unset, AiAgentInputTransformsSystemPrompt]): System instructions that guide the AI's
            behavior, persona, and response style. Optional.
        streaming (Union[Unset, AiAgentInputTransformsStreaming]): Boolean. If true, stream the AI response
            incrementally.
            Streaming events include: token_delta, reasoning_token_delta, tool_call, tool_call_arguments, tool_execution,
            tool_result
        memory (Union['AiAgentInputTransformsMemoryType0', 'AiAgentInputTransformsMemoryType1',
            'AiAgentInputTransformsMemoryType2', Unset]): Memory configuration - can be static (MemoryConfig), JavaScript
            expression, or AI-determined
        memory_id (Union[Unset, AiAgentInputTransformsMemoryId]): String. Names the memory this step reads and writes,
            overriding the memory id the run
            was started with (the chat conversation, an app chat session or the `memory_id` run
            parameter). Leave unset to use the run's memory id. A fixed value shares one memory
            across every run; an expression such as `flow_input.customer_id` keeps one memory per
            key. When it evaluates to an empty value the agent runs without memory. Read only
            while `memory` is `window`: it is ignored when memory is off, and an older `auto` or
            `manual` memory reads neither history input.
        previous_messages (Union[Unset, AiAgentInputTransformsPreviousMessages]): Array of MemoryMessage. History
            supplied by the flow, sent between the system prompt
            and the user message. Read only while `memory` is off or absent: managed memory
            ignores it, and an older `auto` or `manual` memory reads neither history input.
        output_schema (Union[Unset, AiAgentInputTransformsOutputSchema]): JSON Schema object defining structured output
            format. Used when you need the AI to return data in a specific shape.
            Supports standard JSON Schema properties: type, properties, required, items, enum, pattern, minLength,
            maxLength, minimum, maximum, etc.
            Example: { type: 'object', properties: { name: { type: 'string' }, age: { type: 'integer' } }, required:
            ['name'] }
        user_attachments (Union[Unset, AiAgentInputTransformsUserAttachments]): Array of file references (images or
            PDFs) for the AI agent.
            Format: Array<{ bucket: string, key: string }> - S3 object references
            Example: [{ bucket: 'my-bucket', key: 'documents/report.pdf' }]
        enabled_tools (Union[Unset, AiAgentInputTransformsEnabledTools]): Array of strings naming which of the tools
            configured in `tools` the agent may call
            this run. Leaving it unset carries every one of them; an empty array carries none.
            A tool is named as the model is shown it. An entry the model is shown nothing of is
            named by what identifies it instead: an MCP server by its resource path, carrying
            every tool it exposes (which of them stays that entry's include_tools/exclude_tools),
            and a websearch entry by the reserved name '__wm_web_search', whatever summary it carries
            (no tool may take that name).
            Example: ['get_user', 'u/admin/github_mcp', '__wm_web_search']
        max_completion_tokens (Union[Unset, AiAgentInputTransformsMaxCompletionTokens]): Integer. Maximum number of
            tokens the AI will generate in its response.
            Range: 1 to 4,294,967,295. Typical values: 256-4096 for most use cases.
        temperature (Union[Unset, AiAgentInputTransformsTemperature]): Float. Controls randomness/creativity of
            responses.
            Range: 0.0 to 2.0 (provider-dependent)
            - 0.0 = deterministic, focused responses
            - 0.7 = balanced (common default)
            - 1.0+ = more creative/random
        max_iterations (Union[Unset, AiAgentInputTransformsMaxIterations]): Number. Limits how many times the agent can
            loop through reasoning and tool use.
            Range: 1-1000.
    """

    provider: Union[
        "AiAgentInputTransformsProviderType0",
        "AiAgentInputTransformsProviderType1",
        "AiAgentInputTransformsProviderType2",
        Unset,
    ] = UNSET
    output_type: Union[Unset, "AiAgentInputTransformsOutputType"] = UNSET
    user_message: Union[Unset, "AiAgentInputTransformsUserMessage"] = UNSET
    system_prompt: Union[Unset, "AiAgentInputTransformsSystemPrompt"] = UNSET
    streaming: Union[Unset, "AiAgentInputTransformsStreaming"] = UNSET
    memory: Union[
        "AiAgentInputTransformsMemoryType0",
        "AiAgentInputTransformsMemoryType1",
        "AiAgentInputTransformsMemoryType2",
        Unset,
    ] = UNSET
    memory_id: Union[Unset, "AiAgentInputTransformsMemoryId"] = UNSET
    previous_messages: Union[Unset, "AiAgentInputTransformsPreviousMessages"] = UNSET
    output_schema: Union[Unset, "AiAgentInputTransformsOutputSchema"] = UNSET
    user_attachments: Union[Unset, "AiAgentInputTransformsUserAttachments"] = UNSET
    enabled_tools: Union[Unset, "AiAgentInputTransformsEnabledTools"] = UNSET
    max_completion_tokens: Union[Unset, "AiAgentInputTransformsMaxCompletionTokens"] = UNSET
    temperature: Union[Unset, "AiAgentInputTransformsTemperature"] = UNSET
    max_iterations: Union[Unset, "AiAgentInputTransformsMaxIterations"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_agent_input_transforms_memory_type_0 import AiAgentInputTransformsMemoryType0
        from ..models.ai_agent_input_transforms_memory_type_1 import AiAgentInputTransformsMemoryType1
        from ..models.ai_agent_input_transforms_provider_type_0 import AiAgentInputTransformsProviderType0
        from ..models.ai_agent_input_transforms_provider_type_1 import AiAgentInputTransformsProviderType1

        provider: Union[Dict[str, Any], Unset]
        if isinstance(self.provider, Unset):
            provider = UNSET

        elif isinstance(self.provider, AiAgentInputTransformsProviderType0):
            provider = UNSET
            if not isinstance(self.provider, Unset):
                provider = self.provider.to_dict()

        elif isinstance(self.provider, AiAgentInputTransformsProviderType1):
            provider = UNSET
            if not isinstance(self.provider, Unset):
                provider = self.provider.to_dict()

        else:
            provider = UNSET
            if not isinstance(self.provider, Unset):
                provider = self.provider.to_dict()

        output_type: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.output_type, Unset):
            output_type = self.output_type.to_dict()

        user_message: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_message, Unset):
            user_message = self.user_message.to_dict()

        system_prompt: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.system_prompt, Unset):
            system_prompt = self.system_prompt.to_dict()

        streaming: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.streaming, Unset):
            streaming = self.streaming.to_dict()

        memory: Union[Dict[str, Any], Unset]
        if isinstance(self.memory, Unset):
            memory = UNSET

        elif isinstance(self.memory, AiAgentInputTransformsMemoryType0):
            memory = UNSET
            if not isinstance(self.memory, Unset):
                memory = self.memory.to_dict()

        elif isinstance(self.memory, AiAgentInputTransformsMemoryType1):
            memory = UNSET
            if not isinstance(self.memory, Unset):
                memory = self.memory.to_dict()

        else:
            memory = UNSET
            if not isinstance(self.memory, Unset):
                memory = self.memory.to_dict()

        memory_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory_id, Unset):
            memory_id = self.memory_id.to_dict()

        previous_messages: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.previous_messages, Unset):
            previous_messages = self.previous_messages.to_dict()

        output_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.output_schema, Unset):
            output_schema = self.output_schema.to_dict()

        user_attachments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_attachments, Unset):
            user_attachments = self.user_attachments.to_dict()

        enabled_tools: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.enabled_tools, Unset):
            enabled_tools = self.enabled_tools.to_dict()

        max_completion_tokens: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.max_completion_tokens, Unset):
            max_completion_tokens = self.max_completion_tokens.to_dict()

        temperature: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.temperature, Unset):
            temperature = self.temperature.to_dict()

        max_iterations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.max_iterations, Unset):
            max_iterations = self.max_iterations.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider is not UNSET:
            field_dict["provider"] = provider
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if user_message is not UNSET:
            field_dict["user_message"] = user_message
        if system_prompt is not UNSET:
            field_dict["system_prompt"] = system_prompt
        if streaming is not UNSET:
            field_dict["streaming"] = streaming
        if memory is not UNSET:
            field_dict["memory"] = memory
        if memory_id is not UNSET:
            field_dict["memory_id"] = memory_id
        if previous_messages is not UNSET:
            field_dict["previous_messages"] = previous_messages
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema
        if user_attachments is not UNSET:
            field_dict["user_attachments"] = user_attachments
        if enabled_tools is not UNSET:
            field_dict["enabled_tools"] = enabled_tools
        if max_completion_tokens is not UNSET:
            field_dict["max_completion_tokens"] = max_completion_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if max_iterations is not UNSET:
            field_dict["max_iterations"] = max_iterations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms_enabled_tools import AiAgentInputTransformsEnabledTools
        from ..models.ai_agent_input_transforms_max_completion_tokens import AiAgentInputTransformsMaxCompletionTokens
        from ..models.ai_agent_input_transforms_max_iterations import AiAgentInputTransformsMaxIterations
        from ..models.ai_agent_input_transforms_memory_id import AiAgentInputTransformsMemoryId
        from ..models.ai_agent_input_transforms_memory_type_0 import AiAgentInputTransformsMemoryType0
        from ..models.ai_agent_input_transforms_memory_type_1 import AiAgentInputTransformsMemoryType1
        from ..models.ai_agent_input_transforms_memory_type_2 import AiAgentInputTransformsMemoryType2
        from ..models.ai_agent_input_transforms_output_schema import AiAgentInputTransformsOutputSchema
        from ..models.ai_agent_input_transforms_output_type import AiAgentInputTransformsOutputType
        from ..models.ai_agent_input_transforms_previous_messages import AiAgentInputTransformsPreviousMessages
        from ..models.ai_agent_input_transforms_provider_type_0 import AiAgentInputTransformsProviderType0
        from ..models.ai_agent_input_transforms_provider_type_1 import AiAgentInputTransformsProviderType1
        from ..models.ai_agent_input_transforms_provider_type_2 import AiAgentInputTransformsProviderType2
        from ..models.ai_agent_input_transforms_streaming import AiAgentInputTransformsStreaming
        from ..models.ai_agent_input_transforms_system_prompt import AiAgentInputTransformsSystemPrompt
        from ..models.ai_agent_input_transforms_temperature import AiAgentInputTransformsTemperature
        from ..models.ai_agent_input_transforms_user_attachments import AiAgentInputTransformsUserAttachments
        from ..models.ai_agent_input_transforms_user_message import AiAgentInputTransformsUserMessage

        d = src_dict.copy()

        def _parse_provider(
            data: object,
        ) -> Union[
            "AiAgentInputTransformsProviderType0",
            "AiAgentInputTransformsProviderType1",
            "AiAgentInputTransformsProviderType2",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _provider_type_0 = data
                provider_type_0: Union[Unset, AiAgentInputTransformsProviderType0]
                if isinstance(_provider_type_0, Unset):
                    provider_type_0 = UNSET
                else:
                    provider_type_0 = AiAgentInputTransformsProviderType0.from_dict(_provider_type_0)

                return provider_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _provider_type_1 = data
                provider_type_1: Union[Unset, AiAgentInputTransformsProviderType1]
                if isinstance(_provider_type_1, Unset):
                    provider_type_1 = UNSET
                else:
                    provider_type_1 = AiAgentInputTransformsProviderType1.from_dict(_provider_type_1)

                return provider_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _provider_type_2 = data
            provider_type_2: Union[Unset, AiAgentInputTransformsProviderType2]
            if isinstance(_provider_type_2, Unset):
                provider_type_2 = UNSET
            else:
                provider_type_2 = AiAgentInputTransformsProviderType2.from_dict(_provider_type_2)

            return provider_type_2

        provider = _parse_provider(d.pop("provider", UNSET))

        _output_type = d.pop("output_type", UNSET)
        output_type: Union[Unset, AiAgentInputTransformsOutputType]
        if isinstance(_output_type, Unset):
            output_type = UNSET
        else:
            output_type = AiAgentInputTransformsOutputType.from_dict(_output_type)

        _user_message = d.pop("user_message", UNSET)
        user_message: Union[Unset, AiAgentInputTransformsUserMessage]
        if isinstance(_user_message, Unset):
            user_message = UNSET
        else:
            user_message = AiAgentInputTransformsUserMessage.from_dict(_user_message)

        _system_prompt = d.pop("system_prompt", UNSET)
        system_prompt: Union[Unset, AiAgentInputTransformsSystemPrompt]
        if isinstance(_system_prompt, Unset):
            system_prompt = UNSET
        else:
            system_prompt = AiAgentInputTransformsSystemPrompt.from_dict(_system_prompt)

        _streaming = d.pop("streaming", UNSET)
        streaming: Union[Unset, AiAgentInputTransformsStreaming]
        if isinstance(_streaming, Unset):
            streaming = UNSET
        else:
            streaming = AiAgentInputTransformsStreaming.from_dict(_streaming)

        def _parse_memory(
            data: object,
        ) -> Union[
            "AiAgentInputTransformsMemoryType0",
            "AiAgentInputTransformsMemoryType1",
            "AiAgentInputTransformsMemoryType2",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _memory_type_0 = data
                memory_type_0: Union[Unset, AiAgentInputTransformsMemoryType0]
                if isinstance(_memory_type_0, Unset):
                    memory_type_0 = UNSET
                else:
                    memory_type_0 = AiAgentInputTransformsMemoryType0.from_dict(_memory_type_0)

                return memory_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _memory_type_1 = data
                memory_type_1: Union[Unset, AiAgentInputTransformsMemoryType1]
                if isinstance(_memory_type_1, Unset):
                    memory_type_1 = UNSET
                else:
                    memory_type_1 = AiAgentInputTransformsMemoryType1.from_dict(_memory_type_1)

                return memory_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _memory_type_2 = data
            memory_type_2: Union[Unset, AiAgentInputTransformsMemoryType2]
            if isinstance(_memory_type_2, Unset):
                memory_type_2 = UNSET
            else:
                memory_type_2 = AiAgentInputTransformsMemoryType2.from_dict(_memory_type_2)

            return memory_type_2

        memory = _parse_memory(d.pop("memory", UNSET))

        _memory_id = d.pop("memory_id", UNSET)
        memory_id: Union[Unset, AiAgentInputTransformsMemoryId]
        if isinstance(_memory_id, Unset):
            memory_id = UNSET
        else:
            memory_id = AiAgentInputTransformsMemoryId.from_dict(_memory_id)

        _previous_messages = d.pop("previous_messages", UNSET)
        previous_messages: Union[Unset, AiAgentInputTransformsPreviousMessages]
        if isinstance(_previous_messages, Unset):
            previous_messages = UNSET
        else:
            previous_messages = AiAgentInputTransformsPreviousMessages.from_dict(_previous_messages)

        _output_schema = d.pop("output_schema", UNSET)
        output_schema: Union[Unset, AiAgentInputTransformsOutputSchema]
        if isinstance(_output_schema, Unset):
            output_schema = UNSET
        else:
            output_schema = AiAgentInputTransformsOutputSchema.from_dict(_output_schema)

        _user_attachments = d.pop("user_attachments", UNSET)
        user_attachments: Union[Unset, AiAgentInputTransformsUserAttachments]
        if isinstance(_user_attachments, Unset):
            user_attachments = UNSET
        else:
            user_attachments = AiAgentInputTransformsUserAttachments.from_dict(_user_attachments)

        _enabled_tools = d.pop("enabled_tools", UNSET)
        enabled_tools: Union[Unset, AiAgentInputTransformsEnabledTools]
        if isinstance(_enabled_tools, Unset):
            enabled_tools = UNSET
        else:
            enabled_tools = AiAgentInputTransformsEnabledTools.from_dict(_enabled_tools)

        _max_completion_tokens = d.pop("max_completion_tokens", UNSET)
        max_completion_tokens: Union[Unset, AiAgentInputTransformsMaxCompletionTokens]
        if isinstance(_max_completion_tokens, Unset):
            max_completion_tokens = UNSET
        else:
            max_completion_tokens = AiAgentInputTransformsMaxCompletionTokens.from_dict(_max_completion_tokens)

        _temperature = d.pop("temperature", UNSET)
        temperature: Union[Unset, AiAgentInputTransformsTemperature]
        if isinstance(_temperature, Unset):
            temperature = UNSET
        else:
            temperature = AiAgentInputTransformsTemperature.from_dict(_temperature)

        _max_iterations = d.pop("max_iterations", UNSET)
        max_iterations: Union[Unset, AiAgentInputTransformsMaxIterations]
        if isinstance(_max_iterations, Unset):
            max_iterations = UNSET
        else:
            max_iterations = AiAgentInputTransformsMaxIterations.from_dict(_max_iterations)

        ai_agent_input_transforms = cls(
            provider=provider,
            output_type=output_type,
            user_message=user_message,
            system_prompt=system_prompt,
            streaming=streaming,
            memory=memory,
            memory_id=memory_id,
            previous_messages=previous_messages,
            output_schema=output_schema,
            user_attachments=user_attachments,
            enabled_tools=enabled_tools,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            max_iterations=max_iterations,
        )

        ai_agent_input_transforms.additional_properties = d
        return ai_agent_input_transforms

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

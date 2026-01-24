from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms_max_completion_tokens_type_0 import (
        AiAgentInputTransformsMaxCompletionTokensType0,
    )
    from ..models.ai_agent_input_transforms_max_completion_tokens_type_1 import (
        AiAgentInputTransformsMaxCompletionTokensType1,
    )
    from ..models.ai_agent_input_transforms_memory_type_0 import AiAgentInputTransformsMemoryType0
    from ..models.ai_agent_input_transforms_memory_type_1 import AiAgentInputTransformsMemoryType1
    from ..models.ai_agent_input_transforms_output_schema_type_0 import AiAgentInputTransformsOutputSchemaType0
    from ..models.ai_agent_input_transforms_output_schema_type_1 import AiAgentInputTransformsOutputSchemaType1
    from ..models.ai_agent_input_transforms_output_type_type_0 import AiAgentInputTransformsOutputTypeType0
    from ..models.ai_agent_input_transforms_output_type_type_1 import AiAgentInputTransformsOutputTypeType1
    from ..models.ai_agent_input_transforms_provider_type_0 import AiAgentInputTransformsProviderType0
    from ..models.ai_agent_input_transforms_provider_type_1 import AiAgentInputTransformsProviderType1
    from ..models.ai_agent_input_transforms_streaming_type_0 import AiAgentInputTransformsStreamingType0
    from ..models.ai_agent_input_transforms_streaming_type_1 import AiAgentInputTransformsStreamingType1
    from ..models.ai_agent_input_transforms_system_prompt_type_0 import AiAgentInputTransformsSystemPromptType0
    from ..models.ai_agent_input_transforms_system_prompt_type_1 import AiAgentInputTransformsSystemPromptType1
    from ..models.ai_agent_input_transforms_temperature_type_0 import AiAgentInputTransformsTemperatureType0
    from ..models.ai_agent_input_transforms_temperature_type_1 import AiAgentInputTransformsTemperatureType1
    from ..models.ai_agent_input_transforms_user_images_type_0 import AiAgentInputTransformsUserImagesType0
    from ..models.ai_agent_input_transforms_user_images_type_1 import AiAgentInputTransformsUserImagesType1
    from ..models.ai_agent_input_transforms_user_message_type_0 import AiAgentInputTransformsUserMessageType0
    from ..models.ai_agent_input_transforms_user_message_type_1 import AiAgentInputTransformsUserMessageType1


T = TypeVar("T", bound="AiAgentInputTransforms")


@_attrs_define
class AiAgentInputTransforms:
    """Input parameters for the AI agent mapped to their values

    Attributes:
        provider (Union['AiAgentInputTransformsProviderType0', 'AiAgentInputTransformsProviderType1']): Maps input
            parameters for a step. Can be a static value or a JavaScript expression that references previous results or flow
            inputs
        output_type (Union['AiAgentInputTransformsOutputTypeType0', 'AiAgentInputTransformsOutputTypeType1']): Maps
            input parameters for a step. Can be a static value or a JavaScript expression that references previous results
            or flow inputs
        user_message (Union['AiAgentInputTransformsUserMessageType0', 'AiAgentInputTransformsUserMessageType1']): Maps
            input parameters for a step. Can be a static value or a JavaScript expression that references previous results
            or flow inputs
        system_prompt (Union['AiAgentInputTransformsSystemPromptType0', 'AiAgentInputTransformsSystemPromptType1',
            Unset]): Maps input parameters for a step. Can be a static value or a JavaScript expression that references
            previous results or flow inputs
        streaming (Union['AiAgentInputTransformsStreamingType0', 'AiAgentInputTransformsStreamingType1', Unset]): Maps
            input parameters for a step. Can be a static value or a JavaScript expression that references previous results
            or flow inputs
        memory (Union['AiAgentInputTransformsMemoryType0', 'AiAgentInputTransformsMemoryType1', Unset]): Maps input
            parameters for a step. Can be a static value or a JavaScript expression that references previous results or flow
            inputs
        output_schema (Union['AiAgentInputTransformsOutputSchemaType0', 'AiAgentInputTransformsOutputSchemaType1',
            Unset]): Maps input parameters for a step. Can be a static value or a JavaScript expression that references
            previous results or flow inputs
        user_images (Union['AiAgentInputTransformsUserImagesType0', 'AiAgentInputTransformsUserImagesType1', Unset]):
            Maps input parameters for a step. Can be a static value or a JavaScript expression that references previous
            results or flow inputs
        max_completion_tokens (Union['AiAgentInputTransformsMaxCompletionTokensType0',
            'AiAgentInputTransformsMaxCompletionTokensType1', Unset]): Maps input parameters for a step. Can be a static
            value or a JavaScript expression that references previous results or flow inputs
        temperature (Union['AiAgentInputTransformsTemperatureType0', 'AiAgentInputTransformsTemperatureType1', Unset]):
            Maps input parameters for a step. Can be a static value or a JavaScript expression that references previous
            results or flow inputs
    """

    provider: Union["AiAgentInputTransformsProviderType0", "AiAgentInputTransformsProviderType1"]
    output_type: Union["AiAgentInputTransformsOutputTypeType0", "AiAgentInputTransformsOutputTypeType1"]
    user_message: Union["AiAgentInputTransformsUserMessageType0", "AiAgentInputTransformsUserMessageType1"]
    system_prompt: Union[
        "AiAgentInputTransformsSystemPromptType0", "AiAgentInputTransformsSystemPromptType1", Unset
    ] = UNSET
    streaming: Union["AiAgentInputTransformsStreamingType0", "AiAgentInputTransformsStreamingType1", Unset] = UNSET
    memory: Union["AiAgentInputTransformsMemoryType0", "AiAgentInputTransformsMemoryType1", Unset] = UNSET
    output_schema: Union[
        "AiAgentInputTransformsOutputSchemaType0", "AiAgentInputTransformsOutputSchemaType1", Unset
    ] = UNSET
    user_images: Union["AiAgentInputTransformsUserImagesType0", "AiAgentInputTransformsUserImagesType1", Unset] = UNSET
    max_completion_tokens: Union[
        "AiAgentInputTransformsMaxCompletionTokensType0", "AiAgentInputTransformsMaxCompletionTokensType1", Unset
    ] = UNSET
    temperature: Union[
        "AiAgentInputTransformsTemperatureType0", "AiAgentInputTransformsTemperatureType1", Unset
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_agent_input_transforms_max_completion_tokens_type_0 import (
            AiAgentInputTransformsMaxCompletionTokensType0,
        )
        from ..models.ai_agent_input_transforms_memory_type_0 import AiAgentInputTransformsMemoryType0
        from ..models.ai_agent_input_transforms_output_schema_type_0 import AiAgentInputTransformsOutputSchemaType0
        from ..models.ai_agent_input_transforms_output_type_type_0 import AiAgentInputTransformsOutputTypeType0
        from ..models.ai_agent_input_transforms_provider_type_0 import AiAgentInputTransformsProviderType0
        from ..models.ai_agent_input_transforms_streaming_type_0 import AiAgentInputTransformsStreamingType0
        from ..models.ai_agent_input_transforms_system_prompt_type_0 import AiAgentInputTransformsSystemPromptType0
        from ..models.ai_agent_input_transforms_temperature_type_0 import AiAgentInputTransformsTemperatureType0
        from ..models.ai_agent_input_transforms_user_images_type_0 import AiAgentInputTransformsUserImagesType0
        from ..models.ai_agent_input_transforms_user_message_type_0 import AiAgentInputTransformsUserMessageType0

        provider: Dict[str, Any]

        if isinstance(self.provider, AiAgentInputTransformsProviderType0):
            provider = self.provider.to_dict()

        else:
            provider = self.provider.to_dict()

        output_type: Dict[str, Any]

        if isinstance(self.output_type, AiAgentInputTransformsOutputTypeType0):
            output_type = self.output_type.to_dict()

        else:
            output_type = self.output_type.to_dict()

        user_message: Dict[str, Any]

        if isinstance(self.user_message, AiAgentInputTransformsUserMessageType0):
            user_message = self.user_message.to_dict()

        else:
            user_message = self.user_message.to_dict()

        system_prompt: Union[Dict[str, Any], Unset]
        if isinstance(self.system_prompt, Unset):
            system_prompt = UNSET

        elif isinstance(self.system_prompt, AiAgentInputTransformsSystemPromptType0):
            system_prompt = UNSET
            if not isinstance(self.system_prompt, Unset):
                system_prompt = self.system_prompt.to_dict()

        else:
            system_prompt = UNSET
            if not isinstance(self.system_prompt, Unset):
                system_prompt = self.system_prompt.to_dict()

        streaming: Union[Dict[str, Any], Unset]
        if isinstance(self.streaming, Unset):
            streaming = UNSET

        elif isinstance(self.streaming, AiAgentInputTransformsStreamingType0):
            streaming = UNSET
            if not isinstance(self.streaming, Unset):
                streaming = self.streaming.to_dict()

        else:
            streaming = UNSET
            if not isinstance(self.streaming, Unset):
                streaming = self.streaming.to_dict()

        memory: Union[Dict[str, Any], Unset]
        if isinstance(self.memory, Unset):
            memory = UNSET

        elif isinstance(self.memory, AiAgentInputTransformsMemoryType0):
            memory = UNSET
            if not isinstance(self.memory, Unset):
                memory = self.memory.to_dict()

        else:
            memory = UNSET
            if not isinstance(self.memory, Unset):
                memory = self.memory.to_dict()

        output_schema: Union[Dict[str, Any], Unset]
        if isinstance(self.output_schema, Unset):
            output_schema = UNSET

        elif isinstance(self.output_schema, AiAgentInputTransformsOutputSchemaType0):
            output_schema = UNSET
            if not isinstance(self.output_schema, Unset):
                output_schema = self.output_schema.to_dict()

        else:
            output_schema = UNSET
            if not isinstance(self.output_schema, Unset):
                output_schema = self.output_schema.to_dict()

        user_images: Union[Dict[str, Any], Unset]
        if isinstance(self.user_images, Unset):
            user_images = UNSET

        elif isinstance(self.user_images, AiAgentInputTransformsUserImagesType0):
            user_images = UNSET
            if not isinstance(self.user_images, Unset):
                user_images = self.user_images.to_dict()

        else:
            user_images = UNSET
            if not isinstance(self.user_images, Unset):
                user_images = self.user_images.to_dict()

        max_completion_tokens: Union[Dict[str, Any], Unset]
        if isinstance(self.max_completion_tokens, Unset):
            max_completion_tokens = UNSET

        elif isinstance(self.max_completion_tokens, AiAgentInputTransformsMaxCompletionTokensType0):
            max_completion_tokens = UNSET
            if not isinstance(self.max_completion_tokens, Unset):
                max_completion_tokens = self.max_completion_tokens.to_dict()

        else:
            max_completion_tokens = UNSET
            if not isinstance(self.max_completion_tokens, Unset):
                max_completion_tokens = self.max_completion_tokens.to_dict()

        temperature: Union[Dict[str, Any], Unset]
        if isinstance(self.temperature, Unset):
            temperature = UNSET

        elif isinstance(self.temperature, AiAgentInputTransformsTemperatureType0):
            temperature = UNSET
            if not isinstance(self.temperature, Unset):
                temperature = self.temperature.to_dict()

        else:
            temperature = UNSET
            if not isinstance(self.temperature, Unset):
                temperature = self.temperature.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "output_type": output_type,
                "user_message": user_message,
            }
        )
        if system_prompt is not UNSET:
            field_dict["system_prompt"] = system_prompt
        if streaming is not UNSET:
            field_dict["streaming"] = streaming
        if memory is not UNSET:
            field_dict["memory"] = memory
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema
        if user_images is not UNSET:
            field_dict["user_images"] = user_images
        if max_completion_tokens is not UNSET:
            field_dict["max_completion_tokens"] = max_completion_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms_max_completion_tokens_type_0 import (
            AiAgentInputTransformsMaxCompletionTokensType0,
        )
        from ..models.ai_agent_input_transforms_max_completion_tokens_type_1 import (
            AiAgentInputTransformsMaxCompletionTokensType1,
        )
        from ..models.ai_agent_input_transforms_memory_type_0 import AiAgentInputTransformsMemoryType0
        from ..models.ai_agent_input_transforms_memory_type_1 import AiAgentInputTransformsMemoryType1
        from ..models.ai_agent_input_transforms_output_schema_type_0 import AiAgentInputTransformsOutputSchemaType0
        from ..models.ai_agent_input_transforms_output_schema_type_1 import AiAgentInputTransformsOutputSchemaType1
        from ..models.ai_agent_input_transforms_output_type_type_0 import AiAgentInputTransformsOutputTypeType0
        from ..models.ai_agent_input_transforms_output_type_type_1 import AiAgentInputTransformsOutputTypeType1
        from ..models.ai_agent_input_transforms_provider_type_0 import AiAgentInputTransformsProviderType0
        from ..models.ai_agent_input_transforms_provider_type_1 import AiAgentInputTransformsProviderType1
        from ..models.ai_agent_input_transforms_streaming_type_0 import AiAgentInputTransformsStreamingType0
        from ..models.ai_agent_input_transforms_streaming_type_1 import AiAgentInputTransformsStreamingType1
        from ..models.ai_agent_input_transforms_system_prompt_type_0 import AiAgentInputTransformsSystemPromptType0
        from ..models.ai_agent_input_transforms_system_prompt_type_1 import AiAgentInputTransformsSystemPromptType1
        from ..models.ai_agent_input_transforms_temperature_type_0 import AiAgentInputTransformsTemperatureType0
        from ..models.ai_agent_input_transforms_temperature_type_1 import AiAgentInputTransformsTemperatureType1
        from ..models.ai_agent_input_transforms_user_images_type_0 import AiAgentInputTransformsUserImagesType0
        from ..models.ai_agent_input_transforms_user_images_type_1 import AiAgentInputTransformsUserImagesType1
        from ..models.ai_agent_input_transforms_user_message_type_0 import AiAgentInputTransformsUserMessageType0
        from ..models.ai_agent_input_transforms_user_message_type_1 import AiAgentInputTransformsUserMessageType1

        d = src_dict.copy()

        def _parse_provider(
            data: object,
        ) -> Union["AiAgentInputTransformsProviderType0", "AiAgentInputTransformsProviderType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                provider_type_0 = AiAgentInputTransformsProviderType0.from_dict(data)

                return provider_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            provider_type_1 = AiAgentInputTransformsProviderType1.from_dict(data)

            return provider_type_1

        provider = _parse_provider(d.pop("provider"))

        def _parse_output_type(
            data: object,
        ) -> Union["AiAgentInputTransformsOutputTypeType0", "AiAgentInputTransformsOutputTypeType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_type_0 = AiAgentInputTransformsOutputTypeType0.from_dict(data)

                return output_type_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            output_type_type_1 = AiAgentInputTransformsOutputTypeType1.from_dict(data)

            return output_type_type_1

        output_type = _parse_output_type(d.pop("output_type"))

        def _parse_user_message(
            data: object,
        ) -> Union["AiAgentInputTransformsUserMessageType0", "AiAgentInputTransformsUserMessageType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_message_type_0 = AiAgentInputTransformsUserMessageType0.from_dict(data)

                return user_message_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            user_message_type_1 = AiAgentInputTransformsUserMessageType1.from_dict(data)

            return user_message_type_1

        user_message = _parse_user_message(d.pop("user_message"))

        def _parse_system_prompt(
            data: object,
        ) -> Union["AiAgentInputTransformsSystemPromptType0", "AiAgentInputTransformsSystemPromptType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _system_prompt_type_0 = data
                system_prompt_type_0: Union[Unset, AiAgentInputTransformsSystemPromptType0]
                if isinstance(_system_prompt_type_0, Unset):
                    system_prompt_type_0 = UNSET
                else:
                    system_prompt_type_0 = AiAgentInputTransformsSystemPromptType0.from_dict(_system_prompt_type_0)

                return system_prompt_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _system_prompt_type_1 = data
            system_prompt_type_1: Union[Unset, AiAgentInputTransformsSystemPromptType1]
            if isinstance(_system_prompt_type_1, Unset):
                system_prompt_type_1 = UNSET
            else:
                system_prompt_type_1 = AiAgentInputTransformsSystemPromptType1.from_dict(_system_prompt_type_1)

            return system_prompt_type_1

        system_prompt = _parse_system_prompt(d.pop("system_prompt", UNSET))

        def _parse_streaming(
            data: object,
        ) -> Union["AiAgentInputTransformsStreamingType0", "AiAgentInputTransformsStreamingType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _streaming_type_0 = data
                streaming_type_0: Union[Unset, AiAgentInputTransformsStreamingType0]
                if isinstance(_streaming_type_0, Unset):
                    streaming_type_0 = UNSET
                else:
                    streaming_type_0 = AiAgentInputTransformsStreamingType0.from_dict(_streaming_type_0)

                return streaming_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _streaming_type_1 = data
            streaming_type_1: Union[Unset, AiAgentInputTransformsStreamingType1]
            if isinstance(_streaming_type_1, Unset):
                streaming_type_1 = UNSET
            else:
                streaming_type_1 = AiAgentInputTransformsStreamingType1.from_dict(_streaming_type_1)

            return streaming_type_1

        streaming = _parse_streaming(d.pop("streaming", UNSET))

        def _parse_memory(
            data: object,
        ) -> Union["AiAgentInputTransformsMemoryType0", "AiAgentInputTransformsMemoryType1", Unset]:
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
            if not isinstance(data, dict):
                raise TypeError()
            _memory_type_1 = data
            memory_type_1: Union[Unset, AiAgentInputTransformsMemoryType1]
            if isinstance(_memory_type_1, Unset):
                memory_type_1 = UNSET
            else:
                memory_type_1 = AiAgentInputTransformsMemoryType1.from_dict(_memory_type_1)

            return memory_type_1

        memory = _parse_memory(d.pop("memory", UNSET))

        def _parse_output_schema(
            data: object,
        ) -> Union["AiAgentInputTransformsOutputSchemaType0", "AiAgentInputTransformsOutputSchemaType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _output_schema_type_0 = data
                output_schema_type_0: Union[Unset, AiAgentInputTransformsOutputSchemaType0]
                if isinstance(_output_schema_type_0, Unset):
                    output_schema_type_0 = UNSET
                else:
                    output_schema_type_0 = AiAgentInputTransformsOutputSchemaType0.from_dict(_output_schema_type_0)

                return output_schema_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _output_schema_type_1 = data
            output_schema_type_1: Union[Unset, AiAgentInputTransformsOutputSchemaType1]
            if isinstance(_output_schema_type_1, Unset):
                output_schema_type_1 = UNSET
            else:
                output_schema_type_1 = AiAgentInputTransformsOutputSchemaType1.from_dict(_output_schema_type_1)

            return output_schema_type_1

        output_schema = _parse_output_schema(d.pop("output_schema", UNSET))

        def _parse_user_images(
            data: object,
        ) -> Union["AiAgentInputTransformsUserImagesType0", "AiAgentInputTransformsUserImagesType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _user_images_type_0 = data
                user_images_type_0: Union[Unset, AiAgentInputTransformsUserImagesType0]
                if isinstance(_user_images_type_0, Unset):
                    user_images_type_0 = UNSET
                else:
                    user_images_type_0 = AiAgentInputTransformsUserImagesType0.from_dict(_user_images_type_0)

                return user_images_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _user_images_type_1 = data
            user_images_type_1: Union[Unset, AiAgentInputTransformsUserImagesType1]
            if isinstance(_user_images_type_1, Unset):
                user_images_type_1 = UNSET
            else:
                user_images_type_1 = AiAgentInputTransformsUserImagesType1.from_dict(_user_images_type_1)

            return user_images_type_1

        user_images = _parse_user_images(d.pop("user_images", UNSET))

        def _parse_max_completion_tokens(
            data: object,
        ) -> Union[
            "AiAgentInputTransformsMaxCompletionTokensType0", "AiAgentInputTransformsMaxCompletionTokensType1", Unset
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _max_completion_tokens_type_0 = data
                max_completion_tokens_type_0: Union[Unset, AiAgentInputTransformsMaxCompletionTokensType0]
                if isinstance(_max_completion_tokens_type_0, Unset):
                    max_completion_tokens_type_0 = UNSET
                else:
                    max_completion_tokens_type_0 = AiAgentInputTransformsMaxCompletionTokensType0.from_dict(
                        _max_completion_tokens_type_0
                    )

                return max_completion_tokens_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _max_completion_tokens_type_1 = data
            max_completion_tokens_type_1: Union[Unset, AiAgentInputTransformsMaxCompletionTokensType1]
            if isinstance(_max_completion_tokens_type_1, Unset):
                max_completion_tokens_type_1 = UNSET
            else:
                max_completion_tokens_type_1 = AiAgentInputTransformsMaxCompletionTokensType1.from_dict(
                    _max_completion_tokens_type_1
                )

            return max_completion_tokens_type_1

        max_completion_tokens = _parse_max_completion_tokens(d.pop("max_completion_tokens", UNSET))

        def _parse_temperature(
            data: object,
        ) -> Union["AiAgentInputTransformsTemperatureType0", "AiAgentInputTransformsTemperatureType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _temperature_type_0 = data
                temperature_type_0: Union[Unset, AiAgentInputTransformsTemperatureType0]
                if isinstance(_temperature_type_0, Unset):
                    temperature_type_0 = UNSET
                else:
                    temperature_type_0 = AiAgentInputTransformsTemperatureType0.from_dict(_temperature_type_0)

                return temperature_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _temperature_type_1 = data
            temperature_type_1: Union[Unset, AiAgentInputTransformsTemperatureType1]
            if isinstance(_temperature_type_1, Unset):
                temperature_type_1 = UNSET
            else:
                temperature_type_1 = AiAgentInputTransformsTemperatureType1.from_dict(_temperature_type_1)

            return temperature_type_1

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        ai_agent_input_transforms = cls(
            provider=provider,
            output_type=output_type,
            user_message=user_message,
            system_prompt=system_prompt,
            streaming=streaming,
            memory=memory,
            output_schema=output_schema,
            user_images=user_images,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
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

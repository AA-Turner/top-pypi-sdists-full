from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_TYPE_UNSPECIFIED: _ClassVar[ModelType]
    MODEL_TYPE_GEMINI_1_5_PRO: _ClassVar[ModelType]
    MODEL_TYPE_GEMINI_1_5_PRO_PREVIEW: _ClassVar[ModelType]
    MODEL_TYPE_GEMINI_1_5_FLASH: _ClassVar[ModelType]
    MODEL_TYPE_GEMINI_1_5_FLASH_PREVIEW: _ClassVar[ModelType]
    MODEL_TYPE_GPT_4_O_MINI: _ClassVar[ModelType]
    MODEL_TYPE_GPT_4_O: _ClassVar[ModelType]
    MODEL_TYPE_GPT_3_5_TURBO: _ClassVar[ModelType]
MODEL_TYPE_UNSPECIFIED: ModelType
MODEL_TYPE_GEMINI_1_5_PRO: ModelType
MODEL_TYPE_GEMINI_1_5_PRO_PREVIEW: ModelType
MODEL_TYPE_GEMINI_1_5_FLASH: ModelType
MODEL_TYPE_GEMINI_1_5_FLASH_PREVIEW: ModelType
MODEL_TYPE_GPT_4_O_MINI: ModelType
MODEL_TYPE_GPT_4_O: ModelType
MODEL_TYPE_GPT_3_5_TURBO: ModelType

class ExecutorParameters(_message.Message):
    __slots__ = ("completion_model_type", "completion_system_instruction")
    COMPLETION_MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_SYSTEM_INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    completion_model_type: ModelType
    completion_system_instruction: str
    def __init__(self, completion_model_type: _Optional[_Union[ModelType, str]] = ..., completion_system_instruction: _Optional[str] = ...) -> None: ...

class SpaceInstruction(_message.Message):
    __slots__ = ("instruction",)
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    instruction: str
    def __init__(self, instruction: _Optional[str] = ...) -> None: ...

class OrchestratorParameters(_message.Message):
    __slots__ = ("space_ids", "space_instructions")
    class SpaceInstructionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SpaceInstruction
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SpaceInstruction, _Mapping]] = ...) -> None: ...
    SPACE_IDS_FIELD_NUMBER: _ClassVar[int]
    SPACE_INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    space_ids: _containers.RepeatedScalarFieldContainer[str]
    space_instructions: _containers.MessageMap[str, SpaceInstruction]
    def __init__(self, space_ids: _Optional[_Iterable[str]] = ..., space_instructions: _Optional[_Mapping[str, SpaceInstruction]] = ...) -> None: ...

class AgentParameters(_message.Message):
    __slots__ = ("executor_parameters", "orchestrator_parameters")
    EXECUTOR_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ORCHESTRATOR_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    executor_parameters: ExecutorParameters
    orchestrator_parameters: OrchestratorParameters
    def __init__(self, executor_parameters: _Optional[_Union[ExecutorParameters, _Mapping]] = ..., orchestrator_parameters: _Optional[_Union[OrchestratorParameters, _Mapping]] = ...) -> None: ...

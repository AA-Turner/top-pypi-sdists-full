import math
from datetime import datetime, timedelta, timezone
from json import dumps
from typing import Any, Dict, List, Literal, Optional, Sequence, Union, cast

from pydantic import ConfigDict, Field, PrivateAttr, TypeAdapter, field_validator
from pydantic.types import UUID4
from pydantic_core import ValidationError
from typing_extensions import Annotated

from galileo_core.schemas.logging.agent import AgentType
from galileo_core.schemas.logging.llm import Event, Message, MessageRole
from galileo_core.schemas.logging.step import BaseStep, Metrics, StepAllowedInputType, StepType
from galileo_core.schemas.shared.document import Document
from galileo_core.utils.json import PydanticJsonEncoder

LlmSpanAllowedInputType = Union[Sequence[Message], Message, str, Dict[str, Any], Sequence[Dict[str, Any]]]
LlmSpanAllowedOutputType = Union[Message, str, Dict[str, Any]]


class BaseSpan(BaseStep):
    input: StepAllowedInputType = Field(default="", description="Input to the trace or span.")
    redacted_input: Optional[StepAllowedInputType] = Field(
        default=None, description="Redacted input of the trace or span."
    )
    step_number: Optional[int] = Field(default=None, description="Topological step number of the span.")
    parent_id: Optional[UUID4] = Field(
        default=None,
        title="Parent ID",
        description="Galileo ID of the parent of this span",
    )


class StepWithChildSpans(BaseSpan):
    spans: List["Span"] = Field(default_factory=list, description="Child spans.")
    _last_child_created_at: Optional[datetime] = PrivateAttr(default=None)
    # Runtime back-pointer for cursor navigation in TracesLogger (not serialized).
    # This enables O(1) navigation up the trace hierarchy without maintaining a stack.
    _parent: Optional["StepWithChildSpans"] = PrivateAttr(default=None)

    def add_child_spans(self, spans: Sequence["Span"]) -> None:
        self.spans.extend(spans)

    def add_child_span(self, span: "Span") -> None:
        self.add_child_spans([span])

    def _generate_unique_timestamp(self) -> datetime:
        """
        Generate a unique timestamp for a new child step, ensuring it is always greater than the previous one.

        This is important for spans that are created in rapid succession, as it prevents them from having the same
        timestamp, which can cause ordering issues in the UI.
        """
        new_timestamp = datetime.now(timezone.utc)
        if self._last_child_created_at is not None and new_timestamp <= self._last_child_created_at:
            new_timestamp = self._last_child_created_at + timedelta(microseconds=1)

        self._last_child_created_at = new_timestamp
        return new_timestamp


class BaseWorkflowSpan(BaseSpan):
    type: Literal[StepType.workflow] = Field(
        default=StepType.workflow, description=BaseStep.model_fields["type"].description
    )


class WorkflowSpan(BaseWorkflowSpan, StepWithChildSpans):
    pass


class BaseAgentSpan(BaseSpan):
    type: Literal[StepType.agent] = Field(default=StepType.agent, description=BaseStep.model_fields["type"].description)
    agent_type: AgentType = Field(default=AgentType.default, description="Agent type.")


class AgentSpan(BaseAgentSpan, StepWithChildSpans):
    pass


class LlmMetrics(Metrics):
    num_input_tokens: Optional[int] = Field(default=None, description="Number of input tokens.")
    num_output_tokens: Optional[int] = Field(default=None, description="Number of output tokens.")
    num_total_tokens: Optional[int] = Field(default=None, description="Total number of tokens.")
    time_to_first_token_ns: Optional[int] = Field(
        default=None,
        description="Time until the first token was generated in nanoseconds.",
    )

    model_config = ConfigDict(extra="allow")


class LlmSpan(BaseSpan):
    type: Literal[StepType.llm] = Field(default=StepType.llm, description=BaseStep.model_fields["type"].description)
    input: Sequence[Message] = Field(
        default_factory=list, validate_default=True, description=BaseStep.model_fields["input"].description
    )
    redacted_input: Optional[Sequence[Message]] = Field(
        default=None, description=BaseStep.model_fields["redacted_input"].description
    )
    output: Message = Field(
        default_factory=lambda: Message(content="", role=MessageRole.assistant),
        validate_default=True,
        description=BaseStep.model_fields["output"].description,
    )
    redacted_output: Optional[Message] = Field(
        default=None, description=BaseStep.model_fields["redacted_output"].description
    )
    metrics: LlmMetrics = Field(default_factory=LlmMetrics, description=BaseStep.model_fields["metrics"].description)
    tools: Optional[Sequence[Dict[str, Any]]] = Field(
        default=None,
        description="List of available tools passed to the LLM on invocation.",
    )
    events: Optional[List[Event]] = Field(
        default=None,
        description="List of reasoning, internal tool call, or MCP events that occurred during the LLM span.",
    )
    model: Optional[str] = Field(default=None, description="Model used for this span.")
    temperature: Optional[float] = Field(default=None, description="Temperature used for generation.")
    finish_reason: Optional[str] = Field(default=None, description="Reason for finishing.")

    @classmethod
    def _convert_dict_to_message(cls, value: Dict[str, Any], default_role: MessageRole = MessageRole.user) -> Message:
        """
        Converts a dict into a Message object.
        Will dump the dict to a json string if it unable to be deserialized into a Message object.

        Args:
            value (Dict[str, Any]): The dict to convert.
            default_role (Optional[MessageRole], optional): The role to use if the dict does not contain a role. Defaults to MessageRole.user.

        Returns:
            Message: The converted Message object.
        """
        try:
            return Message.model_validate(value)
        except ValidationError:
            return Message(content=dumps(value), role=default_role)

    @field_validator("tools", mode="after")
    def validate_tools_serializable(cls, val: Optional[Sequence[Dict[str, Any]]]) -> Optional[Sequence[Dict[str, Any]]]:
        # Make sure we can dump input/output to json string.
        dumps(val, cls=PydanticJsonEncoder)
        return val

    @classmethod
    def _convert_input_to_messages(cls, value: LlmSpanAllowedInputType) -> Sequence[Message]:
        """Helper method to convert various input types into a standardized list of Message objects."""
        if isinstance(value, Sequence) and all(isinstance(item, Message) for item in value):
            return cast(Sequence[Message], value)
        if isinstance(value, Sequence) and all(isinstance(item, Dict) for item in value):
            return [
                cls._convert_dict_to_message(value=cast(Dict[str, Any], item), default_role=MessageRole.user)
                for item in value
            ]
        if isinstance(value, str):
            return [Message(role=MessageRole.user, content=value)]
        if isinstance(value, Message):
            return [value]
        if isinstance(value, Dict):
            return [cls._convert_dict_to_message(value=value, default_role=MessageRole.user)]
        raise ValueError("LLM span input must be a Message, a list of Messages, a dict, a list of dicts, or a string.")

    @classmethod
    def _convert_output_to_message(cls, value: LlmSpanAllowedOutputType) -> Message:
        """Helper method to convert various output types into a standardized Message object."""
        if isinstance(value, Message):
            return value
        if isinstance(value, str):
            return Message(role=MessageRole.assistant, content=value)
        if isinstance(value, Dict):
            return cls._convert_dict_to_message(value=value, default_role=MessageRole.assistant)
        raise ValueError("LLM span output must be a Message, a string, or a dict.")

    @field_validator("input", mode="before")
    def convert_input(cls, value: LlmSpanAllowedInputType) -> Sequence[Message]:
        """Converts various input types into a standardized list of Message objects."""
        return cls._convert_input_to_messages(value)

    @field_validator("redacted_input", mode="before")
    def convert_redacted_input(cls, value: Optional[LlmSpanAllowedInputType]) -> Optional[Sequence[Message]]:
        """Converts various redacted input types into a standardized list of Message objects."""
        if value is None:
            return None
        return cls._convert_input_to_messages(value)

    @field_validator("output", mode="before")
    def convert_output(cls, value: LlmSpanAllowedOutputType) -> Message:
        """Converts various output types into a standardized Message object."""
        return cls._convert_output_to_message(value)

    @field_validator("redacted_output", mode="before")
    def convert_redacted_output(cls, value: Optional[LlmSpanAllowedOutputType]) -> Optional[Message]:
        """Converts various redacted output types into a standardized Message object."""
        if value is None:
            return None
        return cls._convert_output_to_message(value)

    @field_validator("temperature", mode="before")
    def convert_temperature(cls, value: Optional[float]) -> Optional[float]:
        if value is None or math.isnan(value) or math.isinf(value):
            return None
        return value


class BaseRetrieverSpan(BaseSpan):
    type: Literal[StepType.retriever] = Field(
        default=StepType.retriever, description=BaseStep.model_fields["type"].description
    )
    input: str = Field(default="", validate_default=True, description=BaseStep.model_fields["input"].description)
    redacted_input: Optional[str] = Field(default=None, description=BaseStep.model_fields["redacted_input"].description)
    output: List[Document] = Field(
        default_factory=list, validate_default=True, description=BaseStep.model_fields["output"].description
    )
    redacted_output: Optional[List[Document]] = Field(
        default=None, description=BaseStep.model_fields["redacted_output"].description
    )

    @classmethod
    def _convert_to_documents(cls, value: Union[List[Dict[str, str]], List[Document]]) -> List[Document]:
        """Helper method to convert various output types into a standardized list of Document objects."""
        if not isinstance(value, list):
            raise ValueError("Retriever output must be a list of dicts or a list of Documents.")

        if all(isinstance(doc, Document) for doc in value):
            return cast(List[Document], value)

        if all(isinstance(doc, dict) for doc in value):
            allowed_fields = {"content", "page_content", "metadata"}
            filtered_docs = [
                {k: v for k, v in cast(Dict[str, Any], doc).items() if k in allowed_fields} for doc in value
            ]
            return [Document.model_validate(doc) for doc in filtered_docs]

        raise ValueError("Retriever output must be a list of dicts, or a list of Documents.")

    @field_validator("output", mode="before")
    def set_output(cls, value: Union[List[Dict[str, str]], List[Document]]) -> List[Document]:
        return cls._convert_to_documents(value)

    @field_validator("redacted_output", mode="before")
    def set_redacted_output(
        cls, value: Optional[Union[List[Dict[str, str]], List[Document]]]
    ) -> Optional[List[Document]]:
        if value is None:
            return None
        return cls._convert_to_documents(value)


class RetrieverSpan(BaseRetrieverSpan, StepWithChildSpans):
    pass


class BaseToolSpan(BaseSpan):
    type: Literal[StepType.tool] = Field(default=StepType.tool, description=BaseStep.model_fields["type"].description)
    input: str = Field(default="", description=BaseStep.model_fields["input"].description)
    redacted_input: Optional[str] = Field(default=None, description=BaseStep.model_fields["redacted_input"].description)
    output: Optional[str] = Field(default=None, description=BaseStep.model_fields["output"].description)
    redacted_output: Optional[str] = Field(
        default=None, description=BaseStep.model_fields["redacted_output"].description
    )
    tool_call_id: Optional[str] = Field(default=None, description="ID of the tool call.")


class ToolSpan(BaseToolSpan, StepWithChildSpans):
    pass


Span = Annotated[Union[AgentSpan, WorkflowSpan, LlmSpan, RetrieverSpan, ToolSpan], Field(discriminator="type")]

SpanAdapter: TypeAdapter[Span] = TypeAdapter(Span)

StepWithChildSpans.model_rebuild()

SpanStepTypes = [step_type.value for step_type in StepType if step_type != StepType.trace]

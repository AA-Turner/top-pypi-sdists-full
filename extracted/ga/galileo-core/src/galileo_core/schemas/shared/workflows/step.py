from json import dumps, loads
from time import time_ns
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, ValidationInfo, field_serializer, field_validator
from typing_extensions import Annotated

from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.shared.document import Document
from galileo_core.schemas.shared.message import Message
from galileo_core.schemas.shared.workflows.node_type import NodeType
from galileo_core.utils.json import PydanticJsonEncoder

StepIOType = Union[
    str,
    Document,
    Message,
    Dict[str, Any],
    Sequence[str],
    Sequence[Document],
    Sequence[Message],
    Sequence[Dict[str, str]],
    Sequence[Dict[str, Any]],
]
LlmStepAllowedIOType = Union[str, Dict[str, str], Message, Sequence[str], Sequence[Dict[str, str]], Sequence[Message]]
RetrieverStepAllowedOutputType = Union[Sequence[str], Sequence[Dict[str, str]], Sequence[Document]]


class BaseStep(BaseModel):
    type: NodeType = Field(
        default=NodeType.workflow, description="Type of the step. By default, it is set to workflow."
    )
    input: StepIOType = Field(description="Input to the step.", union_mode="left_to_right")
    # Redacted field only supported for Observe
    redacted_input: Optional[StepIOType] = Field(
        default=None,
        description="Redacted input of the step. This is used to redact sensitive information.",
        union_mode="left_to_right",
    )
    output: StepIOType = Field(default="", description="Output of the step.", union_mode="left_to_right")
    # Redacted field only supported for Observe
    redacted_output: Optional[StepIOType] = Field(
        default=None,
        description="Redacted output of the step. This is used to redact sensitive information.",
        union_mode="left_to_right",
    )
    name: str = Field(default="", description="Name of the step.", validate_default=True)
    created_at_ns: int = Field(
        default_factory=time_ns, description="Timestamp of the step's creation, as nanoseconds since epoch."
    )
    duration_ns: int = Field(default=0, description="Duration of the step in nanoseconds.")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Metadata associated with this step.")
    status_code: Optional[int] = Field(
        default=None, description="Status code of the step. Used for logging failed/errored steps."
    )
    ground_truth: Optional[str] = Field(default=None, description="Ground truth expected output for the step.")

    model_config = ConfigDict(validate_assignment=True)

    @field_validator("name", mode="before")
    def set_name(cls, value: Optional[str], info: ValidationInfo) -> str:
        return value or info.data["type"]

    @field_validator("created_at_ns", mode="before")
    def set_timestamp(cls, value: Optional[int]) -> int:
        if value is None:
            return time_ns()
        return value

    @field_validator("duration_ns", mode="before")
    def set_duration(cls, value: Optional[int]) -> int:
        if value is None:
            return 0
        return value

    @field_validator("metadata", mode="before")
    def set_metadata(cls, value: Optional[Dict[str, str]]) -> Dict[str, str]:
        if value is None:
            return dict()
        return value

    @field_validator("input", "output", "redacted_input", "redacted_output", mode="after")
    def validate_input_output_serializable(cls, val: StepIOType) -> StepIOType:
        # Make sure we can dump input/output to json string.
        if val is not None:
            dumps(val, cls=PydanticJsonEncoder)
        return val

    # We disable the check_fields for this serializer because we want to use the same method for `tools`, which is not
    # a field in the this model but only on the `LlmStep` which is a subclass.
    @field_serializer(
        "input",
        "output",
        "redacted_input",
        "redacted_output",
        "tools",
        when_used="json-unless-none",
        check_fields=False,
    )
    def serialize_to_str(self, input: StepIOType) -> str:
        return input if isinstance(input, str) else dumps(input, cls=PydanticJsonEncoder)


class BaseStepWithChildren(BaseStep):
    def children(self) -> Sequence[BaseStep]:
        raise NotImplementedError("Please Implement this method")


class StepWithChildren(BaseStepWithChildren):
    steps: List["AWorkflowStep"] = Field(default_factory=list, description="Steps in the workflow.")
    parent: Optional["StepWithChildren"] = Field(
        default=None, description="Parent node of the current node. For internal use only.", exclude=True
    )
    _last_child_created_at_ns: Optional[int] = PrivateAttr(default=None)

    def _generate_unique_timestamp_ns(self) -> int:
        """
        Generate a unique timestamp for a new child step, ensuring it is always greater than the previous one.

        This is important for steps that are created in rapid succession, as it prevents them from having the same
        timestamp, which can cause ordering issues in the UI.
        """
        new_timestamp = time_ns()
        if self._last_child_created_at_ns is not None and new_timestamp <= self._last_child_created_at_ns:
            # Increment by 1000ns (1 microsecond) to ensure the timestamp is unique after conversion to datetime,
            # which has microsecond precision.
            new_timestamp = self._last_child_created_at_ns + 1000

        self._last_child_created_at_ns = new_timestamp
        return new_timestamp

    def children(self) -> Sequence[BaseStep]:
        return self.steps

    def add_llm(
        self,
        input: LlmStepAllowedIOType,
        output: LlmStepAllowedIOType,
        model: str,
        redacted_input: Optional[LlmStepAllowedIOType] = None,
        redacted_output: Optional[LlmStepAllowedIOType] = None,
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        time_to_first_token_ms: Optional[float] = None,
        status_code: Optional[int] = None,
    ) -> "LlmStep":
        """
        Add a new llm step to the current workflow.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this step.
            redacted_input: Optional[LlmStepAllowedIOType]: Redacted input of the node.
            redacted_output: Optional[LlmStepAllowedIOType]: Redacted output of the node.
            tools: Optional[Sequence[Dict[str, Any]]]: List of available tools passed to LLM on invocation.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            input_tokens: Optional[int]: Number of input tokens.
            output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            time_to_first_token_ms: Optional[float]: Time to first token in milliseconds.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            LlmStep: The created step.
        """
        step = LlmStep(
            input=input,
            output=output,
            model=model,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            tools=tools,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=self._generate_unique_timestamp_ns() if created_at_ns is None else created_at_ns,
            metadata=metadata,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            time_to_first_token_ms=time_to_first_token_ms,
            status_code=status_code,
        )
        self.steps.append(step)
        return step

    def add_retriever(
        self,
        input: StepIOType,
        documents: RetrieverStepAllowedOutputType,
        redacted_input: Optional[StepIOType] = None,
        redacted_documents: Optional[RetrieverStepAllowedOutputType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
    ) -> "RetrieverStep":
        """
        Add a new retriever step to the current workflow.

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            documents: Union[List[str], List[Dict[str, str]], List[Document]]: Documents retrieved from the retriever.
            redacted_input: Optional[StepIOType]: Redacted input of the node.
            redacted_documents: Optional[RetrieverStepAllowedOutputType]: Redacted documents retrieved from the retriever.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            RetrieverStep: The created step.
        """
        step = RetrieverStep(
            input=input,
            output=documents,
            redacted_input=redacted_input,
            redacted_output=redacted_documents,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=self._generate_unique_timestamp_ns() if created_at_ns is None else created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        self.steps.append(step)
        return step

    def add_tool(
        self,
        input: StepIOType,
        output: StepIOType,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
    ) -> "ToolStep":
        """
        Add a new tool step to the current workflow.

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: StepIOType: Output of the node.
            redacted_input: Optional[StepIOType]: Redacted input of the node.
            redacted_output: Optional[StepIOType]: Redacted output of the node.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            ToolStep: The created step.
        """
        step = ToolStep(
            input=input,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=self._generate_unique_timestamp_ns() if created_at_ns is None else created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        self.steps.append(step)
        return step

    def add_protect(
        self,
        payload: Payload,
        response: Response,
        redacted_payload: Optional[Payload] = None,
        redacted_response: Optional[Response] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
    ) -> "ToolStep":
        """
        Add a new protect step to the current workflow.

        Parameters:
        ----------
            payload: Payload: Input to Protect `invoke`.
            response: Response: Output from Protect `invoke`.
            redacted_payload: Optional[Payload]: Redacted input of the node.
            redacted_response: Optional[Response]: Redacted output of the node.
            name: Optional[str]: Name of the step.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            ToolStep: The created step.
        """
        step = ToolStep(
            input=payload.model_dump(mode="json"),
            output=response.model_dump(mode="json"),
            redacted_input=redacted_payload.model_dump(mode="json") if redacted_payload else None,
            redacted_output=redacted_response.model_dump(mode="json") if redacted_response else None,
            name="GalileoProtect",
            duration_ns=response.trace_metadata.response_at - response.trace_metadata.received_at,
            created_at_ns=self._generate_unique_timestamp_ns() if created_at_ns is None else created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        self.steps.append(step)
        return step

    def add_sub_workflow(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "WorkflowStep":
        """
        Add a nested workflow step to the workflow. This is useful when you want to create a nested workflow within the
        current workflow. The next step you add will be a child of this workflow. To step out of the nested workflow,
        use conclude_workflow().

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[StepIOType]: Output of the node. This can also be set on conclude_workflow().
            redacted_input: Optional[StepIOType]: Redacted input of the node.
            redacted_output: Optional[StepIOType]: Redacted output of the node. This can also be set on conclude_workflow().
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
        Returns:
        -------
            WorkflowStep: The created step.
        """
        step = WorkflowStep(
            parent=self,
            input=input,
            output=output or "",
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=self._generate_unique_timestamp_ns() if created_at_ns is None else created_at_ns,
            metadata=metadata,
        )
        self.steps.append(step)
        return step

    def add_sub_agent(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "AgentStep":
        """
        Add a nested agent workflow step to the workflow. This is useful when you want to create a nested workflow
        within the current workflow. The next step you add will be a child of this workflow. To step out of the nested
        workflow, use conclude_workflow().

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[StepIOType]: Output of the node. This can also be set on conclude_workflow().
            redacted_input: Optional[StepIOType]: Redacted input of the node.
            redacted_output: Optional[StepIOType]: Redacted output of the node. This can also be set on conclude_workflow().
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
        Returns:
        -------
            AgentStep: The created step.
        """
        step = AgentStep(
            parent=self,
            input=input,
            output=output or "",
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=self._generate_unique_timestamp_ns() if created_at_ns is None else created_at_ns,
            metadata=metadata,
        )
        self.steps.append(step)
        return step

    def conclude(
        self,
        output: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        duration_ns: Optional[int] = None,
        status_code: Optional[int] = None,
    ) -> Optional["StepWithChildren"]:
        """
        Conclude the workflow by setting the output of the current node. In the case of nested workflows, this will
        point the workflow back to the parent of the current workflow.

        Parameters:
        ----------
            output: Optional[StepIOType]: Output of the node.
            redacted_output: Optional[StepIOType]: Redacted output of the node.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Optional[StepWithChildren]: The parent of the current workflow. None if no parent exists.
        """
        self.output = output or self.output
        self.redacted_output = redacted_output or self.redacted_output
        self.status_code = status_code
        if duration_ns is not None:
            self.duration_ns = duration_ns
        return self.parent


class WorkflowStep(StepWithChildren):
    type: Literal[NodeType.workflow] = Field(
        default=NodeType.workflow, description="Type of the step. By default, it is set to workflow."
    )


class ChainStep(StepWithChildren):
    type: Literal[NodeType.chain] = Field(
        default=NodeType.chain, description="Type of the step. By default, it is set to chain."
    )


class LlmStep(BaseStep):
    type: Literal[NodeType.llm] = Field(
        default=NodeType.llm, description="Type of the step. By default, it is set to llm."
    )
    input: LlmStepAllowedIOType = Field(description="Input to the LLM step.", union_mode="left_to_right")
    output: LlmStepAllowedIOType = Field(default="", description="Output of the LLM step.", union_mode="left_to_right")
    redacted_input: Optional[LlmStepAllowedIOType] = Field(
        default=None,
        description="Redacted input of the LLM step. This is used to redact sensitive information.",
        union_mode="left_to_right",
    )
    redacted_output: Optional[LlmStepAllowedIOType] = Field(
        default=None,
        description="Redacted output of the LLM step. This is used to redact sensitive information.",
        union_mode="left_to_right",
    )
    tools: Optional[Sequence[Dict[str, Any]]] = Field(
        default=None, description="List of available tools passed to the LLM on invocation."
    )
    model: Optional[str] = Field(default=None, description="Model used for this step.")
    input_tokens: Optional[int] = Field(default=None, description="Number of input tokens.")
    output_tokens: Optional[int] = Field(default=None, description="Number of output tokens.")
    total_tokens: Optional[int] = Field(default=None, description="Total number of tokens.")
    temperature: Optional[float] = Field(default=None, description="Temperature used for generation.")
    time_to_first_token_ms: Optional[float] = Field(default=None, description="Time to first token in milliseconds.")


class RetrieverStep(BaseStep):
    type: Literal[NodeType.retriever] = Field(
        default=NodeType.retriever, description="Type of the step. By default, it is set to retriever."
    )
    input: str = Field(description="Input query to the retriever.")
    output: List[Document] = Field(
        default_factory=list,
        description="Documents retrieved from the retriever. This can be a list of strings or `Document`s.",
    )
    redacted_input: Optional[str] = Field(
        default=None,
        description="Redacted input of the retriever step. This is used to redact sensitive information.",
    )
    redacted_output: Optional[List[Document]] = Field(
        default=None,
        description="Redacted output of the retriever step. This is used to redact sensitive information.",
    )

    @field_validator("output", mode="before")
    def set_output(cls, value: Union[List[str], List[Dict[str, str]], List[Document]]) -> List[Document]:
        # If the output is stored as a JSON-encoded string, try to parse it.
        if isinstance(value, str):
            try:
                value = loads(value)
            except Exception:
                pass
        if isinstance(value, list):
            if all(isinstance(doc, str) for doc in value):
                parsed = [Document.model_validate(dict(content=doc)) for doc in value]
            elif all(isinstance(doc, dict) for doc in value):
                parsed = [Document.model_validate(doc) for doc in value]
            elif all(isinstance(doc, Document) for doc in value):
                parsed = [Document.model_validate(doc) for doc in value]
            else:
                raise ValueError("Retriever output must be a list of strings, a list of dicts, or a list of Documents.")
            return parsed
        raise ValueError("Retriever output must be a list of strings, a list of dicts or a list of Documents.")

    @field_validator("redacted_output", mode="before")
    def set_redacted_output(
        cls, value: Optional[Union[List[str], List[Dict[str, str]], List[Document]]]
    ) -> Optional[List[Document]]:
        if value is None:
            return None
        return cls.set_output(value)


class ToolStep(BaseStep):
    type: Literal[NodeType.tool] = Field(
        default=NodeType.tool, description="Type of the step. By default, it is set to tool."
    )


class AgentStep(StepWithChildren):
    type: Literal[NodeType.agent] = Field(
        default=NodeType.agent, description="Type of the step. By default, it is set to agent."
    )


AWorkflowStep = Annotated[
    Union[WorkflowStep, ChainStep, LlmStep, RetrieverStep, ToolStep, AgentStep], Field(discriminator="type")
]

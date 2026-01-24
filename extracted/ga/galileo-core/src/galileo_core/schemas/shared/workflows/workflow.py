from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.shared.workflows.step import (
    AgentStep,
    AWorkflowStep,
    LlmStep,
    LlmStepAllowedIOType,
    RetrieverStep,
    RetrieverStepAllowedOutputType,
    StepIOType,
    StepWithChildren,
    ToolStep,
    WorkflowStep,
)


class Workflows(BaseModel):
    workflows: List[AWorkflowStep] = Field(default_factory=list, description="List of workflows.")
    current_workflow: Optional[StepWithChildren] = Field(default=None, description="Current workflow in the workflow.")

    def add_workflow(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        ground_truth: Optional[str] = None,
    ) -> WorkflowStep:
        """
        Create a new workflow and add it to the list of workflows.
        Simple usage:
        ```
        my_workflows.add_workflow("input")
        my_workflows.add_llm_step("input", "output", model="<my_model>")
        my_workflows.conclude_workflow("output")
        ```
        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[str]: Output of the node.
            redacted_input: Optional[StepIOType]: Redacted input to the node.
            redacted_output: Optional[str]: Redacted output of the node.
            name: Optional[str]: Name of the workflow.
            duration_ns: Optional[int]: Duration of the workflow in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the workflow's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this workflow.
            ground_truth: Optional[str]: Ground truth, expected output of the workflow.
        Returns:
        -------
            WorkflowStep: The created workflow.
        """
        workflow = WorkflowStep(
            input=input,
            output=output or "",
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            ground_truth=ground_truth,
        )
        self.workflows.append(workflow)
        self.current_workflow = workflow
        return workflow

    def add_agent_workflow(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        ground_truth: Optional[str] = None,
    ) -> AgentStep:
        """
        Create a new workflow and add it to the list of workflows.
        Simple usage:
        ```
        my_workflows.add_agent_workflow("input")
        my_workflows.add_tool_step("input", "output")
        my_workflows.conclude_workflow("output")
        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[str]: Output of the node.
            redacted_input: Optional[StepIOType]: Redacted input to the node.
            redacted_output: Optional[str]: Redacted output of the node.
            name: Optional[str]: Name of the workflow.
            duration_ns: Optional[int]: Duration of the workflow in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the workflow's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this workflow.
            ground_truth: Optional[str] = None, Ground truth, expected output of the workflow.
        Returns:
        -------
            AgentStep: The created agent workflow.
        """
        workflow = AgentStep(
            input=input,
            output=output or "",
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            ground_truth=ground_truth,
        )
        self.workflows.append(workflow)
        self.current_workflow = workflow
        return workflow

    def add_single_step_workflow(
        self,
        input: LlmStepAllowedIOType,
        output: LlmStepAllowedIOType,
        model: str,
        redacted_input: Optional[LlmStepAllowedIOType] = None,
        redacted_output: Optional[LlmStepAllowedIOType] = None,
        tools: Optional[List[Dict]] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        time_to_first_token_ms: Optional[float] = None,
        ground_truth: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> LlmStep:
        """
        Create a new single-step workflow and add it to the list of workflows. This is just if you need a plain llm
        workflow with no surrounding steps.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this step. Feedback from April: Good docs about what model names we use.
            redacted_input: Optional[LlmStepAllowedIOType]: Redacted input to the node.
            redacted_output: Optional[LlmStepAllowedIOType]: Redacted output of the node.
            tools: Optional[List[Dict]]: List of available tools passed to LLM on invocation.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            input_tokens: Optional[int]: Number of input tokens.
            output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            time_to_first_token_ms: Optional[float]: Time taken to generate the first token.
            ground_truth: Optional[str]: Ground truth, expected output of the workflow.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            LlmStep: The created step.
        """
        step = LlmStep(
            input=input,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            model=model,
            tools=tools,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            time_to_first_token_ms=time_to_first_token_ms,
            status_code=status_code,
            ground_truth=ground_truth,
        )
        self.workflows.append(step)
        # Single step workflows are automatically concluded so we reset the current step.
        self.current_workflow = None
        return step

    def add_llm_step(
        self,
        input: LlmStepAllowedIOType,
        output: LlmStepAllowedIOType,
        model: str,
        redacted_input: Optional[LlmStepAllowedIOType] = None,
        redacted_output: Optional[LlmStepAllowedIOType] = None,
        tools: Optional[List[Dict]] = None,
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
    ) -> LlmStep:
        """
        Add a new llm step to the current workflow.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this step.
            redacted_input: Optional[LlmStepAllowedIOType]: Redacted input to the node.
            redacted_output: Optional[LlmStepAllowedIOType]: Redacted output of the node.
            tools: Optional[List[Dict]]: List of available tools passed to LLM on invocation.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            input_tokens: Optional[int]: Number of input tokens.
            output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            time_to_first_token_ms: Optional[float]: Time taken to generate the first token.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            LlmStep: The created step.
        """
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        step = self.current_workflow.add_llm(
            input=input,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            model=model,
            tools=tools,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            time_to_first_token_ms=time_to_first_token_ms,
            status_code=status_code,
        )
        return step

    def add_retriever_step(
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
    ) -> RetrieverStep:
        """
        Add a new retriever step to the current workflow.

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            documents: Union[List[str], List[Dict[str, str]], List[Document]]: Documents retrieved from the retriever.
            redacted_input: Optional[StepIOType]: Redacted input to the node.
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
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        step = self.current_workflow.add_retriever(
            input=input,
            documents=documents,
            redacted_input=redacted_input,
            redacted_documents=redacted_documents,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        return step

    def add_tool_step(
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
    ) -> ToolStep:
        """
        Add a new tool step to the current workflow.

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: StepIOType: Output of the node.
            redacted_input: Optional[StepIOType]: Redacted input to the node.
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
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        step = self.current_workflow.add_tool(
            input=input,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        return step

    def add_protect_step(
        self,
        payload: Payload,
        response: Response,
        redacted_payload: Optional[Payload] = None,
        redacted_response: Optional[Response] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
    ) -> ToolStep:
        """
        Add a new protect step to the current workflow.

        Parameters:
        ----------
            payload: Payload: Input to Protect `invoke`.
            response: Response: Output from Protect `invoke`.
            redacted_payload: Optional[Payload]: Redacted input to Protect `invoke`.
            redacted_response: Optional[Response]: Redacted output from Protect `invoke`.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            ToolStep: The created step.
        """
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        step = self.current_workflow.add_protect(
            payload=payload,
            response=response,
            redacted_payload=redacted_payload,
            redacted_response=redacted_response,
            created_at_ns=created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        return step

    def add_workflow_step(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> WorkflowStep:
        """
        Add a nested workflow step to the workflow. This is useful when you want to create a nested workflow within the
        current workflow. The next step you add will be a child of this workflow. To step out of the nested workflow,
        use conclude_workflow().

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[StepIOType]: Output of the node. This can also be set on conclude_workflow().
            redacted_input: Optional[StepIOType]: Redacted input to the node.
            redacted_output: Optional[StepIOType]: Redacted output of the node.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
        Returns:
        -------
            WorkflowStep: The created step.
        """
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        step = self.current_workflow.add_sub_workflow(
            input=input,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
        )
        self.current_workflow = step
        return step

    def add_agent_step(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        redacted_input: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> AgentStep:
        """
        Add a nested agent workflow step to the workflow. This is useful when you want to create a nested workflow
        within the current workflow. The next step you add will be a child of this workflow. To step out of the nested
        workflow, use conclude_workflow().

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[StepIOType]: Output of the node. This can also be set on conclude_workflow().
            redacted_input: Optional[StepIOType]: Redacted input to the node.
            redacted_output: Optional[StepIOType]: Redacted output of the node.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
        Returns:
        -------
            AgentStep: The created step.
        """
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        step = self.current_workflow.add_sub_agent(
            input=input,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
        )
        self.current_workflow = step
        return step

    def conclude_workflow(
        self,
        output: Optional[StepIOType] = None,
        redacted_output: Optional[StepIOType] = None,
        duration_ns: Optional[int] = None,
        status_code: Optional[int] = None,
    ) -> Optional[StepWithChildren]:
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
        if self.current_workflow is None:
            raise ValueError("No existing workflow to conclude.")
        self.current_workflow = self.current_workflow.conclude(
            output=output, redacted_output=redacted_output, duration_ns=duration_ns, status_code=status_code
        )
        return self.current_workflow


"""Enhanced ToolNode that handles artifacts properly.

This module provides an enhanced version of langgraph's ToolNode that can handle
ToolMessage artifacts (such as images) by converting them to HumanMessage format,
which is required for proper LLM processing.
"""

from typing import Any, Callable, Literal, Optional, Sequence, Type, Union
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.store.base import BaseStore
from pydantic import BaseModel

from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.chat_agent_executor import (
    create_react_agent,
    StructuredResponseSchema,
    Prompt,
    StateSchemaType,
)
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer
from langgraph.utils.runnable import RunnableLike
from langchain_core.runnables import RunnableConfig


class ArtifactAwareToolNode(ToolNode):
    """Enhanced ToolNode that properly handles ToolMessage artifacts.

    This class extends langgraph's ToolNode to handle the case where tools return
    ToolMessage objects with artifacts (like images). Since most LLM providers
    don't support images in ToolMessage format, this node converts any artifacts
    to HumanMessage format for proper processing.
    """

    def _func(
        self,
        input: Union[list[AnyMessage], dict[str, Any], BaseModel],
        config: RunnableConfig,
        *,
        store: BaseStore | None,
    ) -> Any:
        """Execute tool calls and handle artifacts in the responses.

        This method processes all tool calls and converts any ToolMessage artifacts
        to HumanMessage format for proper LLM processing.
        """
        # First, get the normal results from the parent implementation
        outputs = super()._func(input, config, store=store)

        # If outputs is a single message or list, we need to process it
        return self._process_artifacts(outputs)

    async def _afunc(
        self,
        input: Union[list[AnyMessage], dict[str, Any], BaseModel],
        config: RunnableConfig,
        *,
        store: BaseStore | None,
    ) -> Any:
        """Async version of _func with artifact handling."""
        # First, get the normal results from the parent implementation
        outputs = await super()._afunc(input, config, store=store)

        # If outputs is a single message or list, we need to process it
        return self._process_artifacts(outputs)

    def _process_artifacts(self, outputs: Any) -> Any:
        """Process outputs to handle ToolMessage artifacts.

        Args:
            outputs: The outputs from the parent ToolNode

        Returns:
            Modified outputs with artifacts converted to HumanMessage
        """
        # Handle different output formats
        if isinstance(outputs, list):
            processed_outputs = []
            for output in outputs:
                if (
                    isinstance(output, ToolMessage)
                    and hasattr(output, "artifact")
                    and output.artifact
                ):
                    # Add the original ToolMessage (with text content)
                    if output.content:
                        processed_outputs.append(output)

                    # Add HumanMessage for artifacts
                    artifact_content = []
                    for artifact in output.artifact:
                        artifact_content.append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{artifact.mimeType};base64,{artifact.data}"
                                },
                            }
                        )

                    processed_outputs.append(HumanMessage(content=artifact_content))
                else:
                    processed_outputs.append(output)
            return processed_outputs

        elif isinstance(outputs, dict) and self.messages_key in outputs:
            # Handle dict format (state updates)
            messages = outputs[self.messages_key]
            processed_messages = []

            for message in messages:
                if (
                    isinstance(message, ToolMessage)
                    and hasattr(message, "artifact")
                    and message.artifact
                ):
                    # Add the original ToolMessage (with text content)
                    if message.content:
                        processed_messages.append(message)

                    # Add HumanMessage for artifacts
                    artifact_content = []
                    for artifact in message.artifact:
                        artifact_content.append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{artifact.mimeType};base64,{artifact.data}"
                                },
                            }
                        )

                    processed_messages.append(HumanMessage(content=artifact_content))
                else:
                    processed_messages.append(message)

            # Return updated dict
            return {**outputs, self.messages_key: processed_messages}

        elif (
            isinstance(outputs, ToolMessage)
            and hasattr(outputs, "artifact")
            and outputs.artifact
        ):
            # Handle single ToolMessage with artifacts
            processed_outputs = []

            # Add the original ToolMessage (with text content)
            if outputs.content:
                processed_outputs.append(outputs)

            # Add HumanMessage for artifacts
            artifact_content = []
            for artifact in outputs.artifact:
                artifact_content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{artifact.mimeType};base64,{artifact.data}"
                        },
                    }
                )

            processed_outputs.append(HumanMessage(content=artifact_content))
            return processed_outputs

        # For all other cases, return as-is
        return outputs


def create_artifact_aware_react_agent(
    model: Union[str, LanguageModelLike],
    tools: Union[Sequence[Union[BaseTool, Callable]], ToolNode],
    *,
    prompt: Optional[Prompt] = None,
    response_format: Optional[
        Union[StructuredResponseSchema, tuple[str, StructuredResponseSchema]]
    ] = None,
    pre_model_hook: Optional[RunnableLike] = None,
    state_schema: Optional[StateSchemaType] = None,
    config_schema: Optional[Type[Any]] = None,
    checkpointer: Optional[Checkpointer] = None,
    store: Optional[BaseStore] = None,
    interrupt_before: Optional[list[str]] = None,
    interrupt_after: Optional[list[str]] = None,
    debug: bool = False,
    version: Literal["v1", "v2"] = "v1",
    name: Optional[str] = None,
) -> CompiledStateGraph:
    """Create a react agent with enhanced artifact handling.

    This function is a wrapper around langgraph's create_react_agent that automatically
    uses an ArtifactAwareToolNode to handle ToolMessage artifacts properly and implements
    intelligent prompt caching to optimize API costs and latency. It accepts all the same
    parameters as the original create_react_agent plus additional caching parameters.

    Returns:
        A compiled LangChain runnable with enhanced artifact handling.
    """
    # If tools is already a ToolNode, wrap it with our enhanced version
    if isinstance(tools, ToolNode):
        # Create our enhanced version with the same tools
        enhanced_tools = ArtifactAwareToolNode(list(tools.tools_by_name.values()))
    else:
        # Create our enhanced ToolNode with the provided tools
        enhanced_tools = ArtifactAwareToolNode(tools)

    # Call the original create_react_agent with our enhanced ToolNode and caching
    return create_react_agent(
        model=model,
        tools=enhanced_tools,
        prompt=prompt,
        response_format=response_format,
        pre_model_hook=pre_model_hook,
        state_schema=state_schema,
        config_schema=config_schema,
        checkpointer=checkpointer,
        store=store,
        interrupt_before=interrupt_before,
        interrupt_after=interrupt_after,
        debug=debug,
        version=version,
        name=name,
    )
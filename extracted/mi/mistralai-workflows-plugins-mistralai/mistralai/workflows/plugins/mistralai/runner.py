import asyncio
from typing import Any, cast

from pydantic import BaseModel

from mistralai.client import models as mistralai_models
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.plugins.mistralai.agent import Agent
from mistralai.workflows.plugins.mistralai.session import FinalOutputs, Inputs, RemoteSession, Session


class RunResult(BaseModel):
    final_output: Any


class Runner:
    @classmethod
    async def run(
        cls,
        agent: Agent,
        inputs: str | mistralai_models.ContentChunk | list[str | mistralai_models.ContentChunk],
        max_turns: int = 10,
        session: Session | None = None,
    ) -> FinalOutputs:
        if session is None:
            session = RemoteSession()

        try:
            # TODO: try to fix type by removing cast
            inputs_ = cast(Inputs, [inputs] if not isinstance(inputs, list) else inputs)

            if not session.is_conversation_active():
                outputs = await session.initialize_conversation(agent, inputs_)
            else:
                outputs = await session.append_messages(inputs_)

            for _ in range(max_turns):
                custom_tool_responses_list = await asyncio.gather(
                    *[session.process_output(output) for output in outputs]
                )
                custom_tool_responses = [response for responses in custom_tool_responses_list for response in responses]

                if not custom_tool_responses:
                    return session.format_final_outputs(outputs)

                # TODO: try to fix type by removing cast
                outputs = await session.append_messages(cast(Inputs, custom_tool_responses))

            return session.format_final_outputs(outputs)
        except Exception as e:
            # Something went wrong, close the conversation if it was started
            if session.is_conversation_active():
                await session.close_conversation()

            raise WorkflowsException(
                message=f"Agent runner failed: {e}",
                code=ErrorCode.AGENT_EXECUTION_ERROR,
                type="agent_execution_error",
            ) from e
        finally:
            # Clean up session resources (e.g., MCP clients)
            if hasattr(session, "cleanup"):
                await session.cleanup()

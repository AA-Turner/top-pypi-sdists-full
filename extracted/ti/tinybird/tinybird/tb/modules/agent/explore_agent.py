from datetime import datetime

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage

from tinybird.tb.modules.agent.animations import ThinkingAnimation
from tinybird.tb.modules.agent.compactor import compact_messages
from tinybird.tb.modules.agent.models import create_model
from tinybird.tb.modules.agent.prompts import (
    explore_data_instructions,
    resources_prompt,
    service_datasources_prompt,
    tone_and_style_instructions,
)
from tinybird.tb.modules.agent.tools.diff_resource import diff_resource
from tinybird.tb.modules.agent.tools.execute_query import execute_query
from tinybird.tb.modules.agent.tools.request_endpoint import request_endpoint
from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.project import Project


class ExploreAgent:
    def __init__(
        self,
        token: str,
        user_token: str,
        host: str,
        workspace_id: str,
        project: Project,
        dangerously_skip_permissions: bool,
        prompt_mode: bool,
        thinking_animation: ThinkingAnimation,
    ):
        self.token = token
        self.user_token = user_token
        self.host = host
        self.workspace_id = workspace_id
        self.dangerously_skip_permissions = dangerously_skip_permissions or prompt_mode
        self.project = project
        self.thinking_animation = thinking_animation
        self.messages: list[ModelMessage] = []
        self.agent = Agent(
            model=create_model(user_token, host, workspace_id),
            deps_type=TinybirdAgentContext,
            instructions=[
                """
You are part of Tinybird Code, an agentic CLI that can help users to work with Tinybird.                 
You are a sub-agent of the main Tinybird Code agent. You are responsible for querying the data in the project.
You can do the following:
- Executing SQL queries against Tinybird Cloud or Tinybird Local.
- Requesting endpoints in Tinybird Cloud or Tinybird Local.
- Visualizing data as a chart using execute_query tool with the `script` parameter.

IMPORTANT: Use always the last environment used in previous queries or endpoint requests (cloud_or_local: str). If you don't have any information about the last environment, use None.
IMPORTANT: If some resource is not found in a environment, you can use the `diff_resource` tool to check the status across environments.

Once you finish the task, return a valid response for the task to complete.
""",
                tone_and_style_instructions,
                explore_data_instructions,
            ],
            tools=[
                Tool(execute_query, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(request_endpoint, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(diff_resource, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
            ],
            history_processors=[compact_messages],
        )

        @self.agent.instructions
        def get_today_date(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"

        @self.agent.instructions
        def get_project_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return resources_prompt(self.project)

        @self.agent.instructions
        def get_service_datasources(ctx: RunContext[TinybirdAgentContext]) -> str:
            return service_datasources_prompt()

    def run(self, task: str, deps: TinybirdAgentContext, usage: Usage):
        result = self.agent.run_sync(
            task,
            deps=deps,
            usage=usage,
            message_history=self.messages,
            model=create_model(self.user_token, self.host, self.workspace_id, run_id=deps.run_id),
        )
        new_messages = result.new_messages()
        self.messages.extend(new_messages)
        return result

    def clear_messages(self):
        self.messages = []

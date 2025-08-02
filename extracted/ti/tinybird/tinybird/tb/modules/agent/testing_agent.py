from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage

from tinybird.tb.modules.agent.animations import ThinkingAnimation
from tinybird.tb.modules.agent.models import create_model
from tinybird.tb.modules.agent.prompts import test_instructions, tests_files_prompt, tone_and_style_instructions
from tinybird.tb.modules.agent.tools.test import create_tests, remove_test, rename_test, run_tests
from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.project import Project


class TestingAgent:
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
You are a sub-agent of the main Tinybird Code agent. You are responsible for managing test files.
You can do the following:
- Create new test files.
- Update existing test files.
- Run tests.
- Rename test files.
- Remove test files.
""",
                tone_and_style_instructions,
                test_instructions,
            ],
            tools=[
                Tool(create_tests, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(run_tests, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(rename_test, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(remove_test, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
            ],
        )

        @self.agent.instructions
        def get_tests_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return tests_files_prompt(self.project)

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

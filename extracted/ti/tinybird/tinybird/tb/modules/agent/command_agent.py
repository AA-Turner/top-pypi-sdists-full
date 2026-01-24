from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage

from tinybird.tb.modules.agent.animations import ThinkingAnimation
from tinybird.tb.modules.agent.models import create_model
from tinybird.tb.modules.agent.prompts import available_commands, tests_files_prompt
from tinybird.tb.modules.agent.tools.run_command import run_command
from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.project import Project


class CommandAgent:
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
                f"""
You are part of Tinybird Code, an agentic CLI that can help users to work with Tinybird.                 
You are a sub-agent of the main Tinybird Code agent. You are responsible for running commands on the user's machine.
You will be given a task to perform and you will use `run_command` tool to complete it.
If you do not find a command that can solve the task, just say that there is no command that can solve the task.
You can run `-h` in every level of the command to get help. E.g. `tb -h`, `tb datasource -h`, `tb datasource ls -h`.
When you need to access Tinybird Cloud, add the `--cloud` flag. E.g. `tb --cloud datasource ls`.
Available commands:
{available_commands}
Token and host are not required to add to the commands.
Always run first help commands to be sure that the commands you are running is not interactive.
IMPORTANT: Do NOT use any command that is not in the list above. 
IMPORTANT: If you are asked to run a command that is not in the list above, return that you are not able to run that command and needs to use the Tinybird CLI manually and that user should run `tb --help` to get the list of available commands.
IMPORTANT: If you are not able to run a command, do not recommend any command to be run by the user. Just `tb --help` to get the list of available commands.
<example_command_not_found>
User: switch to another workspace
Assistant: I'm sorry, but I cannot switch to another workspace. You can use the Tinybird CLI to switch workspaces. Run `tb --help` to get the list of available commands.
</example_command_not_found>
""",
            ],
            tools=[
                Tool(run_command, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
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
        self.messages.extend(result.new_messages())
        return result

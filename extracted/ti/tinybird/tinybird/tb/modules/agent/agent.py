import asyncio
import hashlib
import shlex
import subprocess
import sys
import urllib.parse
import uuid
from functools import partial
from typing import Any, Callable, Optional

import click
import humanfriendly
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart
from requests import Response

from tinybird.tb.check_pypi import CheckPypi
from tinybird.tb.client import TinyB
from tinybird.tb.config import CURRENT_VERSION, get_clickhouse_host, get_display_cloud_host
from tinybird.tb.modules.agent.animations import ThinkingAnimation
from tinybird.tb.modules.agent.banner import display_banner
from tinybird.tb.modules.agent.command_agent import CommandAgent
from tinybird.tb.modules.agent.compactor import compact_messages
from tinybird.tb.modules.agent.explore_agent import ExploreAgent
from tinybird.tb.modules.agent.file_agent import FileAgent
from tinybird.tb.modules.agent.memory import (
    clear_history,
    clear_messages,
    save_messages,
)
from tinybird.tb.modules.agent.mock_agent import MockAgent
from tinybird.tb.modules.agent.models import create_model
from tinybird.tb.modules.agent.prompts import (
    agent_system_prompt,
    fixtures_prompt,
    load_custom_project_rules,
    resources_prompt,
    secrets_prompt,
    service_datasources_prompt,
    vendor_files_prompt,
)
from tinybird.tb.modules.agent.testing_agent import TestingAgent
from tinybird.tb.modules.agent.tools.analyze import analyze_file, analyze_url
from tinybird.tb.modules.agent.tools.append import append_file, append_url
from tinybird.tb.modules.agent.tools.build import build
from tinybird.tb.modules.agent.tools.datafile import (
    create_datafile,
    read_datafile,
    remove_file,
    rename_datafile_or_fixture,
    search_datafiles,
)
from tinybird.tb.modules.agent.tools.deploy import deploy
from tinybird.tb.modules.agent.tools.deploy_check import deploy_check
from tinybird.tb.modules.agent.tools.diff_resource import diff_resource
from tinybird.tb.modules.agent.tools.get_endpoint_stats import get_endpoint_stats
from tinybird.tb.modules.agent.tools.get_openapi_definition import get_openapi_definition
from tinybird.tb.modules.agent.tools.plan import complete_plan, plan
from tinybird.tb.modules.agent.tools.secret import create_or_update_secrets
from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    SubAgentRunCancelled,
    TinybirdAgentContext,
    show_confirmation,
    show_input,
)
from tinybird.tb.modules.build_common import process as build_process
from tinybird.tb.modules.common import (
    _analyze,
    _get_tb_client,
    echo_safe_humanfriendly_tables_format_pretty_table,
    get_region_from_host,
    get_regions,
    sys_exit,
    update_cli,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.deployment_common import create_deployment
from tinybird.tb.modules.exceptions import CLIBuildException, CLIDeploymentException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.login_common import login
from tinybird.tb.modules.mock_common import append_mock_data
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.test_common import run_tests as run_tests_common


class TinybirdAgent:
    def __init__(
        self,
        token: str,
        user_token: str,
        host: str,
        workspace_id: str,
        project: Project,
        dangerously_skip_permissions: bool,
        prompt_mode: bool,
        feature: Optional[str] = None,
    ):
        self.token = token
        self.user_token = user_token
        self.workspace_id = workspace_id
        self.host = host
        self.dangerously_skip_permissions = dangerously_skip_permissions or prompt_mode
        self.project = project
        self.thinking_animation = ThinkingAnimation()
        self.confirmed_plan_id: Optional[str] = None
        self.feature = feature
        self.messages: list[ModelMessage] = []
        cli_config = CLIConfig.get_project_config()
        regions = get_regions(cli_config)
        self.agent = Agent(
            model=create_model(user_token, host, workspace_id, feature=feature),
            deps_type=TinybirdAgentContext,
            instructions=[agent_system_prompt],
            tools=[
                Tool(create_datafile, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(read_datafile, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(search_datafiles, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(remove_file, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(
                    rename_datafile_or_fixture,
                    docstring_format="google",
                    require_parameter_descriptions=True,
                    takes_ctx=True,
                ),
                Tool(plan, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(complete_plan, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(build, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(deploy, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(deploy_check, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(analyze_file, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(analyze_url, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(append_file, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(append_url, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(
                    get_endpoint_stats, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True
                ),
                Tool(
                    get_openapi_definition,
                    docstring_format="google",
                    require_parameter_descriptions=True,
                    takes_ctx=True,
                ),
                Tool(diff_resource, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(
                    create_or_update_secrets,
                    docstring_format="google",
                    require_parameter_descriptions=True,
                    takes_ctx=True,
                ),
            ],
            history_processors=[compact_messages],
        )

        self.testing_agent = TestingAgent(
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            prompt_mode=prompt_mode,
            thinking_animation=self.thinking_animation,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            workspace_id=workspace_id,
            project=self.project,
        )
        self.command_agent = CommandAgent(
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            prompt_mode=prompt_mode,
            thinking_animation=self.thinking_animation,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            workspace_id=workspace_id,
            project=self.project,
        )
        self.explore_agent = ExploreAgent(
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            prompt_mode=prompt_mode,
            thinking_animation=self.thinking_animation,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            workspace_id=workspace_id,
            project=self.project,
        )
        self.mock_agent = MockAgent(
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            prompt_mode=prompt_mode,
            thinking_animation=self.thinking_animation,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            workspace_id=workspace_id,
            project=self.project,
        )
        self.file_agent = FileAgent(
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            prompt_mode=prompt_mode,
            thinking_animation=self.thinking_animation,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            workspace_id=workspace_id,
            project=self.project,
        )

        @self.agent.tool
        def manage_tests(ctx: RunContext[TinybirdAgentContext], task: str) -> str:
            """Delegate test management to the test agent:

            Args:
                task (str): The detailed task to perform. Required.

            Returns:
                str: The result of the query.
            """
            result = self.testing_agent.run(task, deps=ctx.deps, usage=ctx.usage)

            if not result:
                return "Could not solve the task using the test agent"

            return result.output

        @self.agent.tool
        def run_command(ctx: RunContext[TinybirdAgentContext], task: str) -> str:
            """Solve a task using directly Tinybird CLI commands.

            Args:
                task (str): The task to solve. Required.

            Returns:
                str: The result of the command.
            """
            try:
                result = self.command_agent.run(task, deps=ctx.deps, usage=ctx.usage)
                return f"Result: {result.output}\nDo not repeat in your response the result again, because it is already displayed in the terminal."
            except SubAgentRunCancelled as e:
                return f"User does not want to continue with the proposed solution. Reason: {e}"

        @self.agent.tool
        def explore_data(ctx: RunContext[TinybirdAgentContext], task: str) -> str:
            """Explore the data in the project by executing SQL queries or requesting endpoints or exporting data or visualizing data as a chart.

            Args:
                task (str): The task to solve. Required.

            Returns:
                str: The summary of the result.
            """
            result = self.explore_agent.run(task, deps=ctx.deps, usage=ctx.usage)
            return result.output or "No result returned"

        @self.agent.tool
        def mock(
            ctx: RunContext[TinybirdAgentContext], datasource_name: str, rows: int, data_format: str, task: str
        ) -> str:
            """Generate mock data for a datasource.

            Args:
                datasource_name (str): The datasource name to generate mock data for. Required.
                rows (int): Number of rows to create. If not provided, the default is 10. Required.
                data_format (str): Format of the mock data to create. Options: ndjson, csv. Required.
                task (str): Extra details about how to generate the mock data (nested json if any, sample row to help with the generation, etc). Required.

            Returns:
                str: The result of the mock data generation.
            """
            user_input = f"Datasource name: {datasource_name}\nRows: {rows}\nData format: {data_format}\nTask: {task}"
            result = self.mock_agent.run(user_input, deps=ctx.deps, usage=ctx.usage)
            return result.output or "No result returned"

        @self.agent.tool
        def manage_files(ctx: RunContext[TinybirdAgentContext], task: str) -> str:
            """List file/folders and read any type of file in the current directory. Use this tool when you need to list or read non Tinybird project files (e.g. .txt, .md).

            Args:
                task (str): The task to solve. Required.

            Returns:
                str: The result of the task.
            """
            result = self.file_agent.run(task, deps=ctx.deps, usage=ctx.usage)
            return result.output or "No result returned"

        @self.agent.instructions
        def get_local_host(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"""
# Tinybird Local info:
- API Host: {ctx.deps.local_host}
- Token: {ctx.deps.local_token}
- UI Dashboard URL: {get_display_cloud_host(ctx.deps.local_host)}/{ctx.deps.workspace_name}
- ClickHouse native HTTP interface:
    - Protocol: HTTP
    - Host: localhost
    - Port: 7182
    - Full URL: http://localhost:7182
    - Username: {ctx.deps.workspace_name}  # Optional, for identification purposes
    - Password: __TB_CLOUD_TOKEN__          # Your Tinybird auth token
"""

        @self.agent.instructions
        def get_cloud_host(ctx: RunContext[TinybirdAgentContext]) -> str:
            try:
                region = get_region_from_host(ctx.deps.host, regions) or {
                    "provider": "Unknown",
                    "name": "Unknown",
                }
            except Exception as e:
                click.echo(FeedbackManager.error(message=f"Error getting region info: {e}"))
                region = {
                    "provider": "Unknown",
                    "name": "Unknown",
                }

            region_provider = region["provider"]
            region_name = region["name"]
            ch_host = get_clickhouse_host(ctx.deps.host)
            return f"""
# Tinybird Cloud info (region details):
- API Host: {ctx.deps.host}
- Workspace ID: {ctx.deps.workspace_id}
- Workspace Name: {project.workspace_name} (in Tinybird Local the workspace name is the same because it is synced with Cloud)
- Region provider: {region_provider}
- Region name: {region_name}
- UI Dashboard URL: {get_display_cloud_host(ctx.deps.host)}/{ctx.deps.workspace_name}
- ClickHouse native HTTP interface:
    - Protocol: HTTPS
    - Host: {ch_host.replace("https://", "").replace(":443", "")}
    - Port: 443 (HTTPS)
    - SSL/TLS: Required (enabled)
    - Full URL: {ch_host}
    - Username: {ctx.deps.workspace_name}  # Optional, for identification purposes
    - Password: __TB_CLOUD_TOKEN__          # Your Tinybird auth token
"""

        @self.agent.instructions
        def get_local_token(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"Tinybird Local token: {ctx.deps.local_token}"

        @self.agent.instructions
        def get_cloud_token(ctx: RunContext[TinybirdAgentContext]) -> str:
            return "When using in the output the Tinybird Cloud token, use the placeholder __TB_CLOUD_TOKEN__. Do not mention that it is a placeholder, because it will be replaced by the actual token by code."

        @self.agent.instructions
        def get_project_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return resources_prompt(self.project, config=ctx.deps.config)

        @self.agent.instructions
        def get_vendor_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return vendor_files_prompt(self.project)

        @self.agent.instructions
        def get_fixture_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return fixtures_prompt(self.project)

        @self.agent.instructions
        def get_service_datasources(ctx: RunContext[TinybirdAgentContext]) -> str:
            return service_datasources_prompt()

        @self.agent.instructions
        def get_secrets(ctx: RunContext[TinybirdAgentContext]) -> str:
            return secrets_prompt(self.project)

    def add_message(self, message: ModelMessage) -> None:
        self.messages.append(message)

    def start_plan(self, plan) -> str:
        self.confirmed_plan_id = hashlib.sha256(plan.encode()).hexdigest()[:16]
        return self.confirmed_plan_id

    def cancel_plan(self) -> Optional[str]:
        plan_id = self.confirmed_plan_id
        self.confirmed_plan_id = None
        return plan_id

    def get_plan(self) -> Optional[str]:
        return self.confirmed_plan_id

    def _build_agent_deps(self, config: dict[str, Any], run_id: Optional[str] = None) -> TinybirdAgentContext:
        project = self.project
        folder = self.project.folder
        local_client = get_tinybird_local_client(config, test=False, silent=False)
        test_client = get_tinybird_local_client(config, test=True, silent=True)
        return TinybirdAgentContext(
            # context does not support the whole client, so we need to pass only the functions we need
            build_project=partial(build_project, project=project, config=config),
            deploy_project=partial(deploy_project, project=project, config=config),
            deploy_check_project=partial(deploy_check_project, project=project, config=config),
            append_data_local=partial(append_data_local, config=config),
            append_data_cloud=partial(append_data_cloud, config=config),
            analyze_fixture=partial(analyze_fixture, config=config),
            execute_query_cloud=partial(execute_query_cloud, config=config),
            execute_query_local=partial(execute_query_local, config=config),
            request_endpoint_cloud=partial(request_endpoint_cloud, config=config),
            request_endpoint_local=partial(request_endpoint_local, config=config),
            build_project_test=partial(build_project_test, project=project, client=test_client, config=config),
            get_pipe_data_test=partial(get_pipe_data_test, client=test_client),
            get_datasource_datafile_cloud=partial(get_datasource_datafile_cloud, config=config),
            get_datasource_datafile_local=partial(get_datasource_datafile_local, config=config),
            get_pipe_datafile_cloud=partial(get_pipe_datafile_cloud, config=config),
            get_pipe_datafile_local=partial(get_pipe_datafile_local, config=config),
            get_connection_datafile_cloud=partial(get_connection_datafile_cloud, config=config),
            get_connection_datafile_local=partial(get_connection_datafile_local, config=config),
            get_project_files=project.get_project_files,
            run_tests=partial(run_tests, project=project, client=test_client, config=config),
            folder=folder,
            thinking_animation=self.thinking_animation,
            workspace_id=self.workspace_id,
            workspace_name=self.project.workspace_name,
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            config=config,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            local_host=local_client.host,
            local_token=local_client.token,
            run_id=run_id,
            get_plan=self.get_plan,
            start_plan=self.start_plan,
            cancel_plan=self.cancel_plan,
        )

    def run(self, user_prompt: str, config: dict[str, Any]) -> None:
        user_prompt = f"{user_prompt}\n\n{load_custom_project_rules(self.project.folder)}"
        self.thinking_animation.start()
        result = self.agent.run_sync(
            user_prompt,
            deps=self._build_agent_deps(config),
            message_history=self.messages,
        )
        new_messages = result.new_messages()
        self.messages.extend(new_messages)
        save_messages(new_messages)
        self.thinking_animation.stop()
        click.echo(result.output)

    async def run_iter(self, user_prompt: str, config: dict[str, Any], run_id: Optional[str] = None) -> None:
        model = create_model(self.user_token, self.host, self.workspace_id, run_id=run_id)
        user_prompt = f"{user_prompt}\n\n{load_custom_project_rules(self.project.folder)}"
        self.thinking_animation.start()
        deps = self._build_agent_deps(config)

        async with self.agent.iter(user_prompt, deps=deps, message_history=self.messages, model=model) as agent_run:
            async for node in agent_run:
                if hasattr(node, "model_response"):
                    for _i, part in enumerate(node.model_response.parts):
                        if hasattr(part, "content") and not agent_run.result:
                            animation_running = self.thinking_animation.running
                            if animation_running:
                                self.thinking_animation.stop()
                            click.echo(
                                FeedbackManager.info(message=part.content.replace("__TB_CLOUD_TOKEN__", self.token))
                            )
                            if animation_running:
                                self.thinking_animation.start()

        if agent_run.result is not None:
            new_messages = agent_run.result.new_messages()
            self.messages.extend(new_messages)
            save_messages(new_messages)
            self.thinking_animation.stop()

    def echo_usage(self, config: dict[str, Any], show_credits: bool = False) -> None:
        try:
            client = _get_tb_client(config["user_token"], config["host"])
            workspace_id = config.get("id", "")
            workspace = client.workspace(workspace_id, with_organization=True, version="v1")
            is_free_plan = workspace["organization"]["plan"].get("billing") == "free_shared_infrastructure_usage"

            if not is_free_plan and not show_credits:
                return

            limits_data = client.organization_limits(workspace["organization"]["id"])
            llm_usage_limits = limits_data.get("limits", {}).get("llm_usage", {})
            current_llm_usage = llm_usage_limits.get("quantity") or 0
            llm_usage = llm_usage_limits.get("max") or 0
            remaining_credits = round(max(llm_usage - current_llm_usage, 0), 2)
            current_llm_usage = round(min(llm_usage, current_llm_usage), 2)

            if not llm_usage:
                return

            def get_message(current_llm_usage, llm_usage: int) -> tuple[Callable[..., str], str, bool]:
                warning_threshold = llm_usage * 0.8
                ui_host = get_display_cloud_host(config["host"])

                if is_free_plan:
                    upgrade_link = f"{ui_host}/organizations/{workspace['organization']['name']}/upgrade?from=agent"
                    if current_llm_usage >= llm_usage:
                        return (
                            FeedbackManager.error,
                            f" You have reached the maximum number of credits. Please upgrade to continue using Tinybird Code: {upgrade_link}",
                            True,
                        )
                    if current_llm_usage >= warning_threshold:
                        return (
                            FeedbackManager.warning,
                            f" You are reaching the maximum number of credits. Please upgrade to continue using Tinybird Code: {upgrade_link}",
                            False,
                        )
                return FeedbackManager.gray, "", False

            message_color, upgrade_message, should_exit = get_message(current_llm_usage, llm_usage)
            click.echo(
                message_color(
                    message=f"{remaining_credits} credits left ({current_llm_usage}/{llm_usage}).{upgrade_message}"
                )
            )

            if should_exit:
                sys_exit("tinybird_code_error", "Maximum number of credits reached")

        except Exception:
            pass


def run_agent(
    config: dict[str, Any],
    project: Project,
    dangerously_skip_permissions: bool,
    prompt: Optional[str] = None,
    feature: Optional[str] = None,
):
    if not prompt:
        latest_version = CheckPypi().get_latest_version()
        if latest_version and "x.y.z" not in CURRENT_VERSION and latest_version != CURRENT_VERSION:
            yes = click.confirm(
                FeedbackManager.warning(
                    message=f"New version available. {CURRENT_VERSION} -> {latest_version}. Do you want to update now? [Y/n]"
                ),
                show_default=False,
                default=True,
                prompt_suffix="",
            )
            if yes:
                update_cli()

    if not prompt:
        click.echo(FeedbackManager.highlight(message="» Initializing Tinybird Code..."))

    token = config.get("token", "")
    host = config.get("host", "")
    user_token = config.get("user_token", "")
    workspace_id = config.get("id", "")
    workspace_name = config.get("name", "")
    try:
        if not token or not host or not workspace_id or not user_token:
            yes = click.confirm(
                FeedbackManager.warning(
                    message="Tinybird Code requires authentication. Do you want to authenticate now? [Y/n]"
                ),
                prompt_suffix="",
                show_default=False,
                default=True,
            )
            if yes:
                login(host, auth_host="https://cloud.tinybird.co", workspace=None, interactive=False, method="browser")
                cli_config = CLIConfig.get_project_config()
                config = {**config, **cli_config.to_dict()}
                token = cli_config.get_token() or ""
                user_token = cli_config.get_user_token() or ""
                host = cli_config.get_host()
                workspace_id = cli_config.get("id", "")
                workspace_name = cli_config.get("name", "")

            if not token or not host or not user_token or not workspace_id:
                click.echo(
                    FeedbackManager.error(message="Tinybird Code requires authentication. Run 'tb login' first.")
                )
                return
        build_user_input: Optional[str] = None
        try:
            build_project(config, project, test=False, silent=True)
        except CLIBuildException as e:
            if prompt:
                raise e
            click.echo(FeedbackManager.error(message=e))
            try:
                show_confirmation(
                    title="Fix project errors?", skip_confirmation=dangerously_skip_permissions, show_review=False
                )
            except AgentRunCancelled:
                click.echo(FeedbackManager.info(message="User cancelled the operation"))
                return

            build_user_input = f"Error building project. Fix the errors before continuing. {e}"

        # In prompt mode, always skip permissions to avoid interactive prompts
        prompt_mode = prompt is not None

        agent = TinybirdAgent(
            token,
            user_token,
            host,
            workspace_id,
            project,
            dangerously_skip_permissions,
            prompt_mode,
            feature,
        )

        # Print mode: run once with the provided prompt and exit
        if prompt:
            if build_user_input:
                prompt = f"User input: {prompt}\n\n{build_user_input}"
            agent.run(prompt, config)
            return

        # Interactive mode: show banner and enter interactive loop
        display_banner()
        click.echo(
            FeedbackManager.info(
                message="""Tips for getting started:
- Describe what you want to build or ask for specific resources.
- Run tb commands directly without leaving interactive mode.
- Create a TINYBIRD.md file to customize your interactions.
"""
            )
        )
        agent.echo_usage(config)

    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Failed to initialize agent: {e}"))
        return

    # Interactive loop
    try:
        while True:
            try:
                user_input = build_user_input or show_input(workspace_name)
                build_user_input = None
                if user_input.startswith("tb "):
                    cmd_parts = shlex.split(user_input)
                    subprocess.run(cmd_parts)
                    continue
                if user_input.lower() in ["/exit", "/quit", "exit", "quit"]:
                    click.echo(FeedbackManager.info(message="Goodbye!"))
                    break
                elif user_input.lower() in ["/clear", "clear"]:
                    clear_history()
                    click.echo(FeedbackManager.info(message="Message history cleared!"))
                    clear_messages()
                    continue
                elif not is_natural_language(user_input, user_token, host):
                    query = f"SELECT * FROM ({user_input.strip()}) FORMAT JSON"
                    try:
                        result = execute_query_local(config, query=query)
                    except Exception as e:
                        click.echo(FeedbackManager.error(message=f"Error executing query: {e}"))
                        continue
                    stats = result["statistics"]
                    seconds = stats["elapsed"]
                    rows_read = humanfriendly.format_number(stats["rows_read"])
                    bytes_read = humanfriendly.format_size(stats["bytes_read"])

                    click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

                    if not result["data"]:
                        click.echo(FeedbackManager.info_no_rows())
                    else:
                        echo_safe_humanfriendly_tables_format_pretty_table(
                            data=[d.values() for d in result["data"][:10]], column_names=result["data"][0].keys()
                        )
                        click.echo("Showing first 10 results\n")
                    continue
                elif user_input.lower() == "/login":
                    subprocess.run(["tb", "login"], check=True)

                    continue
                elif user_input.lower() == "/help":
                    subprocess.run(["tb", "--help"], check=True)
                    continue
                elif user_input.lower() == "/usage":
                    agent.echo_usage(config, show_credits=True)
                    continue
                elif user_input.strip() == "":
                    continue
                else:
                    run_id = str(uuid.uuid4())
                    asyncio.run(agent.run_iter(user_input, config, run_id))
            except AgentRunCancelled:
                click.echo(FeedbackManager.info(message="User cancelled the operation"))
                agent.add_message(
                    ModelRequest(
                        parts=[
                            UserPromptPart(
                                content="User cancelled the operation",
                            )
                        ]
                    )
                )
                agent.cancel_plan()
                continue
            except KeyboardInterrupt:
                click.echo(FeedbackManager.info(message="Goodbye!"))
                break
            except EOFError:
                click.echo(FeedbackManager.info(message="Goodbye!"))
                break

    except Exception as e:
        agent.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=f"Error: {e}"))
        sys.exit(1)


def build_project(
    config: dict[str, Any], project: Project, silent: bool = False, test: bool = True, load_fixtures: bool = False
) -> None:
    client = get_tinybird_local_client(config, test=test, silent=silent)
    build_error = build_process(
        project=project,
        tb_client=client,
        config=config,
        watch=False,
        silent=silent,
        exit_on_error=False,
        load_fixtures=load_fixtures,
    )
    if build_error:
        raise CLIBuildException(build_error)


def build_project_test(
    client: TinyB,
    project: Project,
    config: dict[str, Any],
    silent: bool = False,
) -> None:
    build_error = build_process(
        project=project,
        tb_client=client,
        config=config,
        watch=False,
        silent=silent,
        exit_on_error=False,
        load_fixtures=True,
    )
    if build_error:
        raise CLIBuildException(build_error)


def deploy_project(config: dict[str, Any], project: Project, allow_destructive_operations: bool = False) -> None:
    client = _get_tb_client(config["token"], config["host"])
    try:
        create_deployment(
            project=project,
            client=client,
            config=config,
            wait=True,
            auto=True,
            allow_destructive_operations=allow_destructive_operations,
        )
    except SystemExit as e:
        raise CLIDeploymentException(e.args[0])


def deploy_check_project(config: dict[str, Any], project: Project) -> None:
    client = _get_tb_client(config["token"], config["host"])
    try:
        create_deployment(project=project, client=client, config=config, check=True, wait=True, auto=True)
    except SystemExit as e:
        if hasattr(e, "code") and e.code == 0:
            return
        raise CLIDeploymentException(e.args[0])


def append_data_local(config: dict[str, Any], datasource_name: str, path: str) -> None:
    client = get_tinybird_local_client(config, test=False, silent=False)
    append_mock_data(client, datasource_name, path)


def append_data_cloud(config: dict[str, Any], datasource_name: str, path: str) -> None:
    client = _get_tb_client(config["token"], config["host"])
    append_mock_data(client, datasource_name, path)


def analyze_fixture(config: dict[str, Any], fixture_path: str, format: str = "json") -> dict[str, Any]:
    local_client = get_tinybird_local_client(config, test=False, silent=True)
    meta, _data = _analyze(fixture_path, local_client, format)
    return meta


def execute_query_cloud(config: dict[str, Any], query: str, pipe_name: Optional[str] = None) -> dict[str, Any]:
    client = _get_tb_client(config["token"], config["host"])
    return client.query(sql=query, pipeline=pipe_name)


def execute_query_local(config: dict[str, Any], query: str, pipe_name: Optional[str] = None) -> dict[str, Any]:
    local_client = get_tinybird_local_client(config, test=False, silent=True)
    return local_client.query(sql=query, pipeline=pipe_name)


def request_endpoint_cloud(
    config: dict[str, Any], endpoint_name: str, params: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    client = _get_tb_client(config["token"], config["host"])
    return client.pipe_data(endpoint_name, format="json", params=params)


def request_endpoint_local(
    config: dict[str, Any], endpoint_name: str, params: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    local_client = get_tinybird_local_client(config, test=False, silent=True)
    return local_client.pipe_data(endpoint_name, format="json", params=params)


def get_datasource_datafile_cloud(config: dict[str, Any], datasource_name: str) -> str:
    try:
        client = _get_tb_client(config["token"], config["host"])
        return client.datasource_file(datasource_name)
    except Exception:
        return "Datasource not found"


def get_datasource_datafile_local(config: dict[str, Any], datasource_name: str) -> str:
    try:
        local_client = get_tinybird_local_client(config, test=False, silent=True)
        return local_client.datasource_file(datasource_name)
    except Exception:
        return "Datasource not found"


def get_pipe_datafile_cloud(config: dict[str, Any], pipe_name: str) -> str:
    try:
        client = _get_tb_client(config["token"], config["host"])
        return client.pipe_file(pipe_name)
    except Exception:
        return "Pipe not found"


def get_pipe_datafile_local(config: dict[str, Any], pipe_name: str) -> str:
    try:
        local_client = get_tinybird_local_client(config, test=False, silent=True)
        return local_client.pipe_file(pipe_name)
    except Exception:
        return "Pipe not found"


def get_connection_datafile_cloud(config: dict[str, Any], connection_name: str) -> str:
    try:
        client = _get_tb_client(config["token"], config["host"])
        return client.connection_file(connection_name)
    except Exception:
        return "Connection not found"


def get_connection_datafile_local(config: dict[str, Any], connection_name: str) -> str:
    try:
        local_client = get_tinybird_local_client(config, test=False, silent=True)
        return local_client.connection_file(connection_name)
    except Exception:
        return "Connection not found"


def run_tests(
    client: TinyB, project: Project, config: dict[str, Any], pipe_name: Optional[str] = None
) -> Optional[str]:
    try:
        return run_tests_common(name=(pipe_name,) if pipe_name else (), project=project, client=client, config=config)
    except SystemExit as e:
        raise Exception(e.args[0])


def get_pipe_data_test(client: TinyB, pipe_name: str, test_params: Optional[dict[str, str]] = None) -> Response:
    pipe = client._req(f"/v0/pipes/{pipe_name}")
    output_node = next(
        (node for node in pipe["nodes"] if node["node_type"] != "default" and node["node_type"] != "standard"),
        {"name": "not_found"},
    )
    if output_node["node_type"] == "endpoint":
        return client._req_raw(f"/v0/pipes/{pipe_name}.ndjson?{test_params}")

    params = {
        "q": output_node["sql"],
        "pipeline": pipe_name,
    }
    return client._req_raw(f"""/v0/sql?{urllib.parse.urlencode(params)}&{test_params}""")


def is_natural_language(user_input: str, user_token: str, host: str) -> bool:
    stripped_input = user_input.strip().lower()
    sql_keywords = ["select", "with"]
    if not any(stripped_input.startswith(keyword) for keyword in sql_keywords):
        return True

    prompt = """Analyze the following text and determine if it's natural language or a SQL query.

Respond with only "NATURAL" if it's natural language (like a question, request, or conversational text), or "SQL" if it's a SQL query starting with SELECT or WITH statements.

Examples:
- "show me all users" -> NATURAL
- "what are the top products?" -> NATURAL
- "SELECT * FROM users" -> SQL
- "WITH cte AS (SELECT...) SELECT..." -> SQL
- "select count(*) from orders" -> SQL
- "help me analyze the data" -> NATURAL
- "select some page hits from analytics_events that happened yesterday" -> NATURAL

IMPORTANT: If you're not sure, default to NATURAL.
"""
    try:
        thinking_animation = ThinkingAnimation()
        thinking_animation.start()
        llm = LLM(user_token=user_token, host=host)
        response_text = llm.ask(
            system_prompt=prompt,
            prompt=f"Text: '{user_input}'",
            feature="tb_agent_is_natural_language",
            model="vertex_ai/gemini-2.0-flash-001",
        )
        thinking_animation.stop()
        if "NATURAL" in response_text:
            return True
        # If unclear, default to natural language to be safe
        return "SQL" not in response_text

    except Exception:
        # If the LLM call fails, fall back to simple heuristics
        # Check if it starts with common SQL keywords
        return not any(stripped_input.startswith(keyword) for keyword in sql_keywords)

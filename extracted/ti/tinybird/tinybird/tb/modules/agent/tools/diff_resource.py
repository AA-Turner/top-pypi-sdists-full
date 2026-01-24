from pathlib import Path

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import Datafile, TinybirdAgentContext
from tinybird.tb.modules.feedback_manager import FeedbackManager


def diff_resource(ctx: RunContext[TinybirdAgentContext], resource: Datafile) -> str:
    """Diff the content of a resource in Tinybird Cloud vs Tinybird Local vs Project local file

    Args:
        resource (Datafile): The resource to diff. Required.

    Returns:
        Datafile: The diff of the resource.
    """
    try:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Comparing content of {resource.pathname} with Tinybird Cloud"))
        resource.pathname = resource.pathname.removeprefix("/")
        project_file_path = Path(ctx.deps.folder) / resource.pathname
        if not project_file_path.exists():
            raise Exception(f"Resource {resource.pathname} not found in project")

        project_file_content = project_file_path.read_text()
        if resource.type == "datasource":
            cloud_content = ctx.deps.get_datasource_datafile_cloud(datasource_name=resource.name)
            local_content = ctx.deps.get_datasource_datafile_local(datasource_name=resource.name)
        elif resource.type == "connection":
            cloud_content = ctx.deps.get_connection_datafile_cloud(connection_name=resource.name)
            local_content = ctx.deps.get_connection_datafile_local(connection_name=resource.name)
        elif resource.type in ["endpoint", "materialized", "sink", "copy"]:
            cloud_content = ctx.deps.get_pipe_datafile_cloud(pipe_name=resource.name)
            local_content = ctx.deps.get_pipe_datafile_local(pipe_name=resource.name)
        else:
            raise Exception(f"{resource.type} is not a valid extension")

        needs_to_build = project_file_content != local_content
        needs_to_deploy = project_file_content != cloud_content
        ctx.deps.thinking_animation.start()
        diff = f"# Diff of resource {resource.name}:\n"
        diff += f"## Tinybird Cloud: {'Deploy needed. Resource does not exist or needs to be updated. Run `deploy` tool to deploy the resource.' if needs_to_deploy else 'Nothing to deploy.'}\n"
        diff += f"## Tinybird Local: {'Build needed. Resource does not exist or needs to be updated. Run `build` tool to build the resource.' if needs_to_build else 'Nothing to build.'}\n"
        return diff
    except Exception as e:
        ctx.deps.thinking_animation.start()
        return f"Could not diff resource {resource.pathname}: {e}"

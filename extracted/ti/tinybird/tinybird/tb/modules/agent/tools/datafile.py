import os
import re
from pathlib import Path
from typing import Any

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    Datafile,
    TinybirdAgentContext,
    create_terminal_box,
    show_confirmation,
    show_input,
)
from tinybird.tb.modules.exceptions import CLIBuildException
from tinybird.tb.modules.feedback_manager import FeedbackManager


def create_datafile(
    ctx: RunContext[TinybirdAgentContext], name: str, type: str, description: str, content: str, pathname: str
) -> str:
    """Given a resource representation, create or update a datafile (.datasource, .connection, .pipe) in the project folder

    Args:
        name (str): The name of the datafile. Required.
        type (str): The type of the datafile. Options: datasource, endpoint, materialized, sink, copy, connection. Required.
        description (str): The description of the datafile. Required.
        content (str): The content of the datafile. Required.
        pathname (str): The pathname of the datafile where the file will be created or it is already located. If it is a new datafile, always include the parent folder depending on the type of the datafile. Required.

    Returns:
        str: If the resource was created or not.
    """
    try:
        ctx.deps.thinking_animation.stop()
        resource = Datafile(
            type=type.lower(),
            name=name,
            content=content,
            description=description,
            pathname=pathname,
        )
        resource.pathname = resource.pathname.removeprefix("/")
        path = Path(ctx.deps.folder) / resource.pathname
        content = resource.content
        exists = str(path) in ctx.deps.get_project_files()
        if exists:
            content = create_terminal_box(path.read_text(), resource.content, title=resource.pathname)
        else:
            content = create_terminal_box(resource.content, title=resource.pathname)
        click.echo(content)
        action = "Create" if not exists else "Update"
        active_plan = ctx.deps.get_plan() is not None
        confirmation = show_confirmation(
            title=f"{action} '{resource.pathname}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Building {resource.pathname}..."))
        folder_path = path.parent
        folder_path.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text(resource.content)
        ctx.deps.build_project(test=False, silent=True, load_fixtures=False)
        action_text = "created" if not exists else "updated"
        click.echo(FeedbackManager.success(message=f"✓ {resource.pathname} {action_text}"))
        ctx.deps.thinking_animation.start()
        return f"{action_text} {resource.pathname}. Project built successfully."
    except AgentRunCancelled as e:
        raise e
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}. If the error is related to another resource, fix it and try again."
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error creating {resource.pathname}: {e}"


def read_datafile(ctx: RunContext[TinybirdAgentContext], path: str, show_content: bool = False) -> str:
    """Reads the content of a datafile (datasource, pipe, endpoint, etc.) in the project.

    Use this tool to read the content of project resources when you need to understand their structure,
    schema, or SQL queries. The path should be relative to the project folder.

    Args:
        path (str): The relative path to the datafile to read (e.g., 'datasources/my_table.datasource', 'endpoints/my_api.pipe'). Required.
        show_content (bool): If True, display the file content to the user in the terminal. Defaults to False.

    Returns:
        str: The content of the datafile.
    """
    try:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Reading {path}..."))
        result = ""
        with open(os.path.join(ctx.deps.folder, path), "r") as f:
            result = f.read()
        if show_content:
            click.echo(create_terminal_box(result, title=path))
            result = f"[Content of {path} was displayed to the user. Do not reprint it.]\n\n{result}"
        ctx.deps.thinking_animation.start()
        return result
    except FileNotFoundError:
        ctx.deps.thinking_animation.start()
        return f"Error: File {path} not found (double check the file path)"
    except Exception as e:
        ctx.deps.thinking_animation.start()
        return f"Error reading file {path}: {e}"


def search_datafiles(
    ctx: RunContext[TinybirdAgentContext], pattern: str, case_sensitive: bool = False, show_results: bool = False
) -> str:
    """Searches for a text pattern across all datafiles in the project.

    Use this tool to find where specific patterns (table names, column names, SQL fragments, etc.)
    appear across multiple project files. Returns matching files with line numbers and content.

    Args:
        pattern (str): The text pattern to search for. Supports regex patterns. Required.
        case_sensitive (bool): If True, perform case-sensitive search. Defaults to False.
        show_results (bool): If True, display the search results to the user in the terminal. Defaults to False.

    Returns:
        str: Search results showing matching files, line numbers, and matching lines.
    """
    ctx.deps.thinking_animation.stop()
    click.echo(FeedbackManager.highlight(message=f"» Searching for '{pattern}' in datafiles..."))

    try:
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
    except re.error as e:
        ctx.deps.thinking_animation.start()
        return f"Error: Invalid regex pattern: {e}"

    project_folder = Path(ctx.deps.folder)
    extensions = [".datasource", ".pipe", ".incl", ".connection"]
    matches: list[dict[str, Any]] = []

    for ext in extensions:
        for file_path in project_folder.rglob(f"*{ext}"):
            # Skip vendor files
            if "vendor" in file_path.parts:
                continue

            try:
                content = file_path.read_text()
                file_matches: list[dict[str, Any]] = []

                for line_num, line in enumerate(content.splitlines(), start=1):
                    if regex.search(line):
                        file_matches.append({"line": line_num, "content": line.strip()})

                if file_matches:
                    matches.append(
                        {
                            "path": str(file_path.relative_to(project_folder)),
                            "matches": file_matches,
                        }
                    )
            except Exception:
                continue

    if not matches:
        result = f"No matches found for pattern '{pattern}'"
        ctx.deps.thinking_animation.start()
        return result

    # Format results
    result_lines = [f"Found {sum(len(m['matches']) for m in matches)} matches in {len(matches)} files:\n"]

    for file_match in matches:
        result_lines.append(f"\n{file_match['path']}:")
        for match in file_match["matches"]:
            result_lines.append(f"  L{match['line']}: {match['content']}")

    result = "\n".join(result_lines)

    if show_results:
        click.echo(FeedbackManager.highlight(message=result))
        result = f"[Search results for '{pattern}' were displayed to the user. Do not reprint them.]\n\n{result}"

    ctx.deps.thinking_animation.start()
    return result


def update_file(ctx: RunContext[TinybirdAgentContext], path: str, content: str):
    """Updates the content of a file.

    Args:
        path (str): The path to the file to update. Required.
        content (str): The full file content to write. Required.
    """
    try:
        with open(os.path.join(ctx.deps.folder, path), "w") as f:
            f.write(content)
    except FileNotFoundError:
        return f"Error: File {path} not found (double check the file path)"

    return "ok"


def create_file(ctx: RunContext[TinybirdAgentContext], path: str, content: str):
    """Creates a new file with the given content.

    Args:
        path (str): The path to the file to create. Required.
        content (str): The full file content to write. Required.
    """
    os.makedirs(os.path.dirname(os.path.join(ctx.deps.folder, path)), exist_ok=True)
    with open(os.path.join(ctx.deps.folder, path), "w") as f:
        f.write(content)

    return "ok"


def rename_datafile_or_fixture(ctx: RunContext[TinybirdAgentContext], path: str, new_path: str):
    """Renames a datafile or fixture.

    Args:
        path (str): The path to the file to rename. Required.
        new_path (str): The new path to the file. Required.
    """
    try:
        ctx.deps.thinking_animation.stop()
        active_plan = ctx.deps.get_plan() is not None
        confirmation = show_confirmation(
            title=f"Rename '{path}' to '{new_path}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Renaming file {path} to {new_path}..."))
        new_path_full = Path(ctx.deps.folder) / new_path.removeprefix("/")

        if new_path_full.exists():
            click.echo(FeedbackManager.error(message=f"Error: File {new_path} already exists"))
            ctx.deps.thinking_animation.start()
            return f"Error: File {new_path} already exists"

        parent_path = new_path_full.parent
        parent_path.mkdir(parents=True, exist_ok=True)
        os.rename(Path(ctx.deps.folder) / path.removeprefix("/"), new_path_full)
        is_datafile = (".connection", ".datasource", ".pipe")

        if new_path_full.suffix in is_datafile:
            ctx.deps.build_project(test=False, silent=True, load_fixtures=False)

        click.echo(FeedbackManager.success(message=f"✓ {new_path} created"))
        ctx.deps.thinking_animation.start()
        return f"Renamed file from {path} to {new_path}"
    except AgentRunCancelled as e:
        raise e
    except FileNotFoundError:
        ctx.deps.thinking_animation.start()
        click.echo(FeedbackManager.error(message=f"Error: File {path} not found"))
        return f"Error: File {path} not found (double check the file path)"
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}"
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error renaming {path} to {new_path}: {e}"


def remove_file(ctx: RunContext[TinybirdAgentContext], path: str) -> str:
    """Removes a datafile or fixture from the project folder and rebuilds the project if needed

    Args:
        path (str): The path to the file to remove. Required.

    Returns:
        str: If the resource was removed successfully.
    """
    try:
        ctx.deps.thinking_animation.stop()
        path = path.removeprefix("/")
        full_path = Path(ctx.deps.folder) / path

        if not full_path.exists():
            click.echo(FeedbackManager.error(message=f"Error: File {path} not found"))
            ctx.deps.thinking_animation.start()
            return f"Error: File {path} not found (double check the file path)"
        active_plan = ctx.deps.get_plan() is not None
        confirmation = show_confirmation(
            title=f"Delete '{path}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Removing {path}..."))

        # Check if it's a datafile that requires project rebuild
        is_datafile = full_path.suffix in (".connection", ".datasource", ".pipe")

        # Remove the file
        full_path.unlink()

        # Check for corresponding .sql file (for fixtures)
        sql_file_path = full_path.with_suffix(".sql")
        sql_file_removed = False
        if sql_file_path.exists():
            sql_file_path.unlink()
            sql_file_removed = True

        # Rebuild project if it's a datafile
        if is_datafile:
            ctx.deps.build_project(test=False, silent=True, load_fixtures=False)

        success_message = f"✓ {path} removed"
        if sql_file_removed:
            success_message += f" (and {sql_file_path.name})"

        click.echo(FeedbackManager.success(message=success_message))
        ctx.deps.thinking_animation.start()

        result_message = f"Removed {path}"
        if sql_file_removed:
            result_message += f" and {sql_file_path.name}"
        if is_datafile:
            result_message += ". Project built successfully."
        else:
            result_message += "."

        return result_message
    except AgentRunCancelled as e:
        raise e
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}. If the error is related to another resource, fix it and try again."
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error removing {path}: {e}"

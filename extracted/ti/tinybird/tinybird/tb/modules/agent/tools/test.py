import os
from pathlib import Path
from typing import Optional

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    TinybirdAgentContext,
    create_terminal_box,
    show_confirmation,
    show_input,
)
from tinybird.tb.modules.exceptions import CLIBuildException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.test_common import dump_tests, parse_tests


def create_tests(ctx: RunContext[TinybirdAgentContext], pipe_name: str, test_content: str) -> str:
    """Given a pipe name, create or update a test for it

    Args:
        pipe_name (str): The pipe name to create a test for. Required.
        test_content (str): The content of the test. Required.

    Returns:
        str: If the test was created or updated and the result of running the tests.
    """
    running_tests = False
    try:
        ctx.deps.thinking_animation.stop()
        ctx.deps.build_project_test(silent=True)
        path = Path(ctx.deps.folder) / "tests" / f"{pipe_name}.yaml"
        current_test_content: Optional[str] = None
        if path.exists():
            current_test_content = path.read_text()

        pipe_tests_content = parse_tests(test_content)
        for test in pipe_tests_content:
            test_params = test["parameters"].split("?")[1] if "?" in test["parameters"] else test["parameters"]
            response = None
            try:
                response = ctx.deps.get_pipe_data_test(pipe_name=pipe_name, test_params=test_params)
            except Exception:
                continue

            if response.status_code >= 400:
                test["expected_http_status"] = response.status_code
                test["expected_result"] = response.json()["error"]
            else:
                if "expected_http_status" in test:
                    del test["expected_http_status"]

                test["expected_result"] = response.text or ""

        test_content = dump_tests(pipe_tests_content)

        if current_test_content:
            content = create_terminal_box(current_test_content, new_content=test_content, title=path.name)
        else:
            content = create_terminal_box(test_content, title=path.name)

        click.echo(content)
        action_text = "Create" if not current_test_content else "Update"
        confirmation = show_confirmation(
            title=f"{action_text} '{path.name}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        folder_path = path.parent
        folder_path.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text(test_content)
        action_text = "created" if not current_test_content else "updated"
        click.echo(FeedbackManager.success(message=f"✓ {path.name} {action_text}"))
        running_tests = True
        test_output = ctx.deps.run_tests(pipe_name=pipe_name)
        click.echo(test_output)
        ctx.deps.thinking_animation.start()
        return f"Test {action_text} for '{pipe_name}' endpoint in {path} and ran successfully\n{test_output}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e).replace("test_error__error__", "")
        ctx.deps.thinking_animation.stop()
        if not running_tests:
            click.echo(FeedbackManager.error(message=error_message))
        ctx.deps.thinking_animation.start()
        if running_tests:
            return f"Test {action_text} for '{pipe_name}' endpoint in {path} but there were errors running the tests: {error_message}"
        return f"Error creating test for '{pipe_name}' endpoint: {error_message}"


def run_tests(ctx: RunContext[TinybirdAgentContext], pipe_name: Optional[str] = None) -> str:
    """Run tests for a given pipe name or all tests in the project

    Args:
        pipe_name (Optional[str]): The pipe name to run tests for. If not provided, all tests in the project will be run.

    Returns:
        str: The result of running the tests.
    """

    try:
        ctx.deps.thinking_animation.stop()
        path = Path(ctx.deps.folder) / "tests" / f"{pipe_name}.yaml"

        title = f"Run tests for '{pipe_name}'?" if pipe_name else "Run all tests in the project?"
        confirmation = show_confirmation(
            title=title,
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        test_output = ctx.deps.run_tests(pipe_name=pipe_name)
        ctx.deps.thinking_animation.start()
        if pipe_name:
            return f"Tests for '{pipe_name}' endpoint in {path} and ran successfully\n{test_output}"
        else:
            return f"All tests in the project ran successfully\n{test_output}"
    except AgentRunCancelled as e:
        raise e
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}"
    except Exception as e:
        error_message = str(e)
        test_exit_code = "test_error__error__"
        test_error = test_exit_code in error_message
        ctx.deps.thinking_animation.stop()
        if not test_error:
            click.echo(FeedbackManager.error(message=error_message))
        else:
            error_message = error_message.replace(test_exit_code, "")
        ctx.deps.thinking_animation.start()
        return f"Error running tests: {error_message}"


def rename_test(ctx: RunContext[TinybirdAgentContext], path: str, new_path: str) -> str:
    """Renames a test file.

    Args:
        path (str): The path to the test file to rename. Required.
        new_path (str): The new path to the test file. Required.

    Returns:
        str: Result of the rename operation.
    """
    try:
        ctx.deps.thinking_animation.stop()
        confirmation = show_confirmation(
            title=f"Rename '{path}' to '{new_path}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Renaming test file {path} to {new_path}..."))
        old_path_full = Path(ctx.deps.folder) / path.removeprefix("/")
        new_path_full = Path(ctx.deps.folder) / new_path.removeprefix("/")

        if not old_path_full.exists():
            click.echo(FeedbackManager.error(message=f"Error: Test file {path} not found"))
            ctx.deps.thinking_animation.start()
            return f"Error: Test file {path} not found (double check the file path)"

        if new_path_full.exists():
            click.echo(FeedbackManager.error(message=f"Error: Test file {new_path} already exists"))
            ctx.deps.thinking_animation.start()
            return f"Error: Test file {new_path} already exists"

        # Ensure new file has .yaml extension for test files
        if new_path_full.suffix != ".yaml":
            new_path_full = new_path_full.with_suffix(".yaml")
            new_path = str(new_path_full.relative_to(ctx.deps.folder))

        parent_path = new_path_full.parent
        parent_path.mkdir(parents=True, exist_ok=True)
        os.rename(old_path_full, new_path_full)

        click.echo(FeedbackManager.success(message=f"✓ {new_path} created"))
        ctx.deps.thinking_animation.start()
        return f"Renamed test file from {path} to {new_path}"
    except AgentRunCancelled as e:
        raise e
    except FileNotFoundError:
        ctx.deps.thinking_animation.start()
        click.echo(FeedbackManager.error(message=f"Error: Test file {path} not found"))
        return f"Error: Test file {path} not found (double check the file path)"
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error renaming test file {path} to {new_path}: {e}"


def remove_test(ctx: RunContext[TinybirdAgentContext], path: str) -> str:
    """Removes a test file from the project folder

    Args:
        path (str): The path to the test file to remove. Required.

    Returns:
        str: If the test file was removed successfully.
    """
    try:
        ctx.deps.thinking_animation.stop()
        path = path.removeprefix("/")
        full_path = Path(ctx.deps.folder) / path

        if not full_path.exists():
            click.echo(FeedbackManager.error(message=f"Error: Test file {path} not found"))
            ctx.deps.thinking_animation.start()
            return f"Error: Test file {path} not found (double check the file path)"

        confirmation = show_confirmation(
            title=f"Delete '{path}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Removing {path}..."))

        # Remove the test file
        full_path.unlink()

        click.echo(FeedbackManager.success(message=f"✓ {path} removed"))
        ctx.deps.thinking_animation.start()

        return f"Removed test file {path}."
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error removing test file {path}: {e}"

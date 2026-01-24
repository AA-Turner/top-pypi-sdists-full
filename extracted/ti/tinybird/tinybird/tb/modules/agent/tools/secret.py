from pathlib import Path

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


def create_or_update_secrets(ctx: RunContext[TinybirdAgentContext], secrets: dict[str, str]) -> str:
    """Creates or updates multiple secrets in the .env.local file in the project folder.

    This function will:
    1. Check if .env.local exists in the project folder, create it if it doesn't
    2. Create or update all specified secret keys with their given values
    3. Handle existing keys by updating their values
    4. Show a single confirmation for all secrets

    Args:
        secrets (dict[str, str]): Dictionary of environment variable keys and values. Required.

    Returns:
        str: Confirmation message about the secrets creation/update.
    """
    try:
        ctx.deps.thinking_animation.stop()

        env_file_path = Path(ctx.deps.folder) / ".env.local"

        # Read existing content if file exists
        existing_content = ""
        if env_file_path.exists():
            existing_content = env_file_path.read_text()

        # Parse existing environment variables
        env_vars = {}
        for line in existing_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()

        # Update or add the new secrets
        new_keys = []
        updated_keys = []
        for key, value in secrets.items():
            if key in env_vars:
                updated_keys.append(key)
            else:
                new_keys.append(key)
            env_vars[key] = value

        # Generate new content
        new_content = "\n".join([f"{k}={v}" for k, v in sorted(env_vars.items())])
        if new_content:
            new_content += "\n"

        # Show preview
        action = "Update" if env_file_path.exists() and updated_keys else "Create"
        if new_keys and updated_keys:
            action = "Create/Update"

        preview_content = create_terminal_box(new_content, title=".env.local")
        click.echo(preview_content)

        active_plan = ctx.deps.get_plan() is not None
        confirmation = show_confirmation(
            title=f"{action} {len(secrets)} secret(s) in .env.local?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the secret changes and gave the following feedback: {feedback}"

        # Write the file
        action = "Updating" if env_file_path.exists() and updated_keys else "Creating"
        click.echo(FeedbackManager.highlight(message=f"» {action} secrets in .env.local..."))
        env_file_path.write_text(new_content)
        ctx.deps.build_project(test=False, silent=True, load_fixtures=False)

        # Generate success message
        result_parts = []
        if new_keys:
            result_parts.append(f"created {len(new_keys)} new secret(s): {', '.join(new_keys)}")
        if updated_keys:
            result_parts.append(f"updated {len(updated_keys)} existing secret(s): {', '.join(updated_keys)}")

        result_msg = " and ".join(result_parts)
        ctx.deps.thinking_animation.start()

        return f"Successfully {result_msg} in .env.local. Project built successfully."

    except AgentRunCancelled as e:
        raise e
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}. If the error is related to another resource, fix it and try again."
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=f"Error managing secrets: {e}"))
        ctx.deps.thinking_animation.start()
        return f"Error creating/updating secrets: {e}"

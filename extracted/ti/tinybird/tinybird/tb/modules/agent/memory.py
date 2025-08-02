import json
from pathlib import Path
from typing import Optional

import click
from prompt_toolkit.history import FileHistory
from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter, ModelRequest
from pydantic_core import to_jsonable_python

from tinybird.tb.modules.feedback_manager import FeedbackManager


def get_history_file_path():
    """Get the history file path based on current working directory"""
    # Get current working directory
    cwd = Path.cwd()

    # Get user's home directory
    home = Path.home()

    # Calculate relative path from home to current directory
    try:
        relative_path = cwd.relative_to(home)
    except ValueError:
        # If current directory is not under home, use absolute path components
        relative_path = Path(*cwd.parts[1:]) if cwd.is_absolute() else cwd

    # Create history directory structure
    history_dir = home / ".tinybird" / "projects" / relative_path
    history_dir.mkdir(parents=True, exist_ok=True)

    # Return history file path
    return history_dir / "history.txt"


def load_history() -> Optional[FileHistory]:
    try:
        history_file = get_history_file_path()
        return FileHistory(str(history_file))
    except Exception:
        return None


def clear_history():
    """Clear the history file"""
    history_file = get_history_file_path()
    history_file.unlink(missing_ok=True)


def clear_messages():
    """Clear the messages file"""
    messages_file = get_messages_file_path()
    messages_file.unlink(missing_ok=True)


def get_messages_file_path():
    """Get the history file path based on current working directory"""
    # Get current working directory
    cwd = Path.cwd()

    # Get user's home directory
    home = Path.home()

    # Calculate relative path from home to current directory
    try:
        relative_path = cwd.relative_to(home)
    except ValueError:
        # If current directory is not under home, use absolute path components
        relative_path = Path(*cwd.parts[1:]) if cwd.is_absolute() else cwd

    # Create history directory structure
    history_dir = home / ".tinybird" / "projects" / relative_path
    history_dir.mkdir(parents=True, exist_ok=True)

    # Return history file path
    return history_dir / "messages.json"


def load_messages() -> list[ModelMessage]:
    try:
        messages_file = get_messages_file_path()
        messages_file.touch()
        if not messages_file.exists():
            messages_file.touch(exist_ok=True)
            messages_file.write_text("[]")
            return []
        with open(messages_file, "r") as f:
            messages_json = json.loads(f.read() or "[]")
            return ModelMessagesTypeAdapter.validate_python(messages_json)
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Could not load previous messages: {e}"))
        messages_file.unlink(missing_ok=True)
        return []


def get_last_messages_from_last_user_prompt() -> list[ModelMessage]:
    all_messages = load_messages()
    # look the last message message with a part_kind of type "user_prompt" inside "parts" field that is a list of objects.
    # once you find it, return that message and all the messages after it
    for msg in reversed(all_messages):
        if isinstance(msg, ModelRequest) and msg.parts and any(part.part_kind == "user-prompt" for part in msg.parts):
            return all_messages[all_messages.index(msg) :]
    return []


def save_messages(new_messages: list[ModelMessage]):
    messages_file = get_messages_file_path()
    messages_file.touch(exist_ok=True)
    messages = load_messages()
    messages.extend(new_messages)
    messages_json = to_jsonable_python(messages)
    with open(messages_file, "w") as f:
        f.write(json.dumps(messages_json))

from glob import glob
from pathlib import Path

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.feedback_manager import FeedbackManager


def list_files(
    ctx: RunContext[TinybirdAgentContext],
    folder_path: str = ".",
    search_pattern: str = "*",
) -> str:
    """Lists all files and folders in a directory.

    Args:
        folder_path (str): The path to the directory to list. If not provided, it will list the files in the current directory. Default: "."
        search_pattern (str): The pattern to search for in the files and folders. Default: "*"
    Returns:
        str: The list of files in the directory.
    """
    try:
        ctx.deps.thinking_animation.stop()
        if folder_path:
            path = Path(folder_path)
        else:
            path = Path.cwd()

        display_folder = "current directory" if (folder_path == "." or not folder_path) else folder_path

        click.echo(
            FeedbackManager.highlight(message=f"» Searching in {display_folder} with pattern '{search_pattern}'")
        )

        if not path.exists():
            ctx.deps.thinking_animation.start()
            return f"Folder {folder_path} does not exist"

        result = glob(f"{path}/**/{search_pattern}", recursive=True)
        folders = [f for f in result if Path(f).is_dir()]
        files = [f for f in result if Path(f).is_file()]

        ctx.deps.thinking_animation.start()
        return f"Folders: {folders}\nFiles: {files}"
    except Exception as e:
        ctx.deps.thinking_animation.start()
        return f"Error listing files: {e}"


def read_file(ctx: RunContext[TinybirdAgentContext], file_path: str) -> str:
    """Reads a file from the local filesystem. The file_path parameter must be an absolute path, not a relative path. Any lines longer than 2000 characters will be truncated.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file.
    """
    try:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Reading file {file_path}"))
        path = Path(file_path)

        if not path.exists():
            ctx.deps.thinking_animation.start()
            return f"File {file_path} does not exist"

        content = path.read_text()
        chunks = content.split("\n")

        if len(chunks) > 2000:
            first_2000 = "\n".join(chunks[0:2000])
            ctx.deps.thinking_animation.start()
            return f"This file is too large to be read by the agent. Showing first 2000 lines instead:\n\n{first_2000}"

        ctx.deps.thinking_animation.start()
        return content
    except Exception as e:
        ctx.deps.thinking_animation.start()
        return f"Error reading file: {e}"

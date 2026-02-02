import os

from anyio import Path as AsyncPath

from exponent.core.remote_execution.types import (
    FilePath,
)
from exponent.core.remote_execution.utils import (
    safe_write_file,
)


async def execute_full_file_rewrite(
    file_path: FilePath, content: str, working_directory: str
) -> str:
    try:
        # Construct the absolute path
        full_file_path = AsyncPath(os.path.join(working_directory, file_path))

        # Check if the directory exists, if not, create it
        await full_file_path.parent.mkdir(parents=True, exist_ok=True)
        exists = await full_file_path.exists()

        await safe_write_file(full_file_path, content)

        # Determine if the file exists and write the new content
        if exists:
            result = f"Modified file {file_path} successfully"
        else:
            result = f"Created file {file_path} successfully"

        return result

    except Exception as e:
        return f"An error occurred: {e!s}"

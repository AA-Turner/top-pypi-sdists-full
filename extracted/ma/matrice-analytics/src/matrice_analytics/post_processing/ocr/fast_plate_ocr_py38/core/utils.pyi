"""Auto-generated stub for module: utils."""
from typing import Any, Callable, Optional, Union

# Functions
def log_time_taken(process_name: str) -> Any[None]:
    """
    A concise context manager to time code snippets and log the result.
    
    Usage:
        ```python
        with log_time_taken("process_name"):
            # Code snippet to be timed
        ```
    
    Args:
        process_name: Name of the process being timed.
    """
    ...
def measure_time() -> Any[Callable[[], float]]:
    """
    A context manager for measuring execution time (in milliseconds) within its code block.
    
    Usage:
        ```python
        with measure_time() as timer:
            # Code snippet to be timed
        print(f"Code took: {timer()} ms")
        ```
    
    Returns:
        A function that returns the elapsed time in milliseconds.
    """
    ...
def safe_write(file: Union[str, Any.Any[str]], mode: str = 'wb', encoding: Optional[str] = None, **kwargs: Any) -> Any[Any]:
    """
    Context manager for safe file writing.
    
    Opens the specified file for writing and yields a file object.
    If an exception occurs during writing, the file is removed before raising the exception.
    
    Args:
        file: Path to the file to write.
        mode: File open mode (e.g. ``"wb"``, ``"w"``, etc.). Defaults to ``"wb"``.
        encoding: Encoding to use (for text modes). Ignored in binary mode.
        **kwargs: Additional arguments passed to ``open()``.
    
    Returns:
        A writable file object.
    """
    ...

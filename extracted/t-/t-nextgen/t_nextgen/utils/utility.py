from pathlib import Path
import time
import re


class Timer:
    """Timer object."""

    def __init__(self, duration: int | float = 10):
        """Timer class initializing function."""
        self.duration = float(duration)
        self.start = time.perf_counter()

    def reset(self) -> None:
        """Resets the elapsed time."""
        self.start = time.perf_counter()

    def increment(self, increment: int = 0) -> None:
        """Increments duration."""
        self.duration += increment

    @property
    def expired(self) -> bool:
        """Checks if timer is expired."""
        return time.perf_counter() - self.start > self.duration

    @property
    def not_expired(self) -> bool:
        """Checks if timer is not expired."""
        return not self.expired

    @property
    def at(self) -> float:
        """Returns elapsed time."""
        return time.perf_counter() - self.start


def wait_until_file_downloads(
    directory_path: Path,
    file_identifier: str,
    is_regex: bool = False,
    wait_time: int = 30,
) -> str:
    """Wait until a file with the specified name or matching the regex pattern is found in the given directory."""
    if isinstance(directory_path, str):
        directory_path = Path(directory_path)
    timer = Timer(wait_time)
    while timer.not_expired:
        for file_path in directory_path.iterdir():
            if (is_regex and re.match(file_identifier, file_path.name)) or file_path.name == file_identifier:
                return str(file_path)
        time.sleep(1)
    raise AssertionError(
        f"{'File matching the pattern' if is_regex else 'File'} not found: {file_identifier} after {wait_time} seconds."
    )

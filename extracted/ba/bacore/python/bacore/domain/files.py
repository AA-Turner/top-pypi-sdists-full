"""Module domain files for handling of files and directories."""

import toml
from dataclasses import dataclass
from pathlib import Path


def ensure_path(path: str | Path) -> Path:
    """Ensure the path is a Path object."""
    return Path(path) if isinstance(path, str) else path


@dataclass
class MarkdownFile:
    """Markdown file representation."""

    path: Path
    skip_title: bool

    def __post_init__(self):
        self.path = ensure_path(self.path)
        if self.path.suffix not in [".md", ".markdown"]:
            raise ValueError("File should be in markdown format")

    def read(self) -> str:
        """Read file and optionally strip the title line."""
        try:
            text = self.path.read_text()
        except OSError as e:
            raise OSError(f"Error reading file {self.path}: {e.strerror}") from e

        title, body = text.split("\n", 1)
        if self.skip_title and title.strip().startswith("#"):
            return body.lstrip()
        else:
            return text


@dataclass
class TOMLFile:
    """TOML file representation."""

    path: Path

    def __post_init__(self):
        """Initialize."""
        self.path = ensure_path(self.path)
        if self.path.suffix != ".toml":
            raise ValueError("File should be in TOML format")

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        try:
            content = toml.loads(self.path.read_text())
        except toml.TomlDecodeError as e:
            raise ValueError(f"Error decoding TOML file {self.path}: {e}")
        return content

"""Pin a project name in a directory's ``pyproject.toml`` without disturbing anything else in it."""

import re
import tomllib
from pathlib import Path
from typing import ClassVar

from labqoat.projects.atomic_project_file import AtomicProjectFile
from labqoat.projects.project_names import ProjectNames


class ProjectPin:
    """Edit only the ``project`` key of ``[tool.labqoat]``, creating the table or the file when missing."""

    header: ClassVar[re.Pattern[str]] = re.compile(r"\s*\[\s*tool\s*\.\s*labqoat\s*\]\s*(#.*)?")
    table: ClassVar[re.Pattern[str]] = re.compile(r"\s*\[")
    key: ClassVar[re.Pattern[str]] = re.compile(r"\s*project\s*=")

    @classmethod
    def write(cls, directory: Path, name: str) -> Path:
        """Pin the name and return the file; refuse an edit that would change any other setting."""
        ProjectNames.project(name, "the project to pin")
        path = directory / "pyproject.toml"
        current = path.read_bytes().decode("utf-8") if path.is_file() else ""
        updated = cls.edit(current, name)
        if cls.expected(current, name) != cls.parsed(updated):
            raise ValueError(f'Cannot pin the project in {path}; set project = "{name}" under [tool.labqoat] yourself')
        AtomicProjectFile.write(path, updated.encode("utf-8"))
        return path

    @classmethod
    def edit(cls, text: str, name: str) -> str:
        """Replace the key in its table, add it below the table header, or append a new table."""
        lines = text.splitlines(keepends=True)
        entry = f'project = "{name}"'
        start = next((index for index, line in enumerate(lines) if cls.header.fullmatch(line.rstrip("\r\n"))), None)
        if start is None:
            gap = "" if not text else "\n" if text.endswith("\n") else "\n\n"
            return f"{text}{gap}[tool.labqoat]\n{entry}\n"
        for index in range(start + 1, len(lines)):
            if cls.table.match(lines[index]):
                break
            if cls.key.match(lines[index]):
                lines[index] = entry + cls.ending(lines[index])
                return "".join(lines)
        ending = cls.ending(lines[start])
        lines[start] = lines[start].rstrip("\r\n") + ending
        lines.insert(start + 1, entry + ending)
        return "".join(lines)

    @staticmethod
    def ending(line: str) -> str:
        """Keep the file's own line terminator on a rewritten or inserted line."""
        return line[len(line.rstrip("\r\n")) :] or "\n"

    @classmethod
    def expected(cls, text: str, name: str) -> dict[str, object]:
        """The current settings with only the project name changed."""
        document = cls.parsed(text)
        tool = document.setdefault("tool", {})
        table = tool.setdefault("labqoat", {}) if isinstance(tool, dict) else None
        if isinstance(table, dict):
            table["project"] = name
        return document

    @staticmethod
    def parsed(text: str) -> dict[str, object]:
        """Decode settings; text that is not valid TOML compares unequal to every document."""
        try:
            return tomllib.loads(text)
        except ValueError:
            return {"invalid": text}

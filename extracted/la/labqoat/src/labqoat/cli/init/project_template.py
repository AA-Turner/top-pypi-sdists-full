"""The starter project shipped with the installed CLI."""

from importlib.resources import files
from typing import ClassVar


class ProjectTemplate:
    """Read the starter files, one module per part of a model's work, from source checkouts and wheels alike."""

    sources: ClassVar[tuple[str, ...]] = ("app.py", "config.py", "data.py", "evaluate.py", "model.py")

    @staticmethod
    def text(name: str) -> str:
        """One packaged template file."""
        return files("labqoat.cli.init").joinpath("template", f"{name}.txt").read_text(encoding="utf-8")

    @classmethod
    def documents(cls, project: str) -> dict[str, str]:
        """Every file of a new project by its path, named after the project."""
        sources = {name: cls.text(name).replace("__NAME__", project) for name in cls.sources}
        return sources | {".gitignore": cls.text("gitignore")}

    @classmethod
    def hook(cls) -> str:
        """The pre-commit script that runs the checks."""
        return cls.text("pre-commit")

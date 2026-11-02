"""Read end-user skills shipped with the installed CLI."""

from importlib.resources import files
from importlib.resources.abc import Traversable


class SkillBundle:
    """Load the same skill content from source checkouts and installed wheels."""

    names = (
        "labqoat-cli",
        "labqoat-runs",
        "labqoat-data",
        "labqoat-memory",
        "labqoat-research",
        "labqoat-examples",
        "labqoat-update",
    )

    @staticmethod
    def contents() -> dict[str, str]:
        """Read the packaged UTF-8 skill entrypoints without network access."""
        root = files("labqoat.cli.skills").joinpath("bundled")
        return {name: root.joinpath(name, "SKILL.md").read_text(encoding="utf-8") for name in SkillBundle.names}

    @staticmethod
    def references() -> dict[str, str]:
        """Read the files an entrypoint points at, keyed by their path under the skills directory.

        They sit one directory below the entrypoint (`reference/`, `examples/`) and are read only when needed.
        """
        root = files("labqoat.cli.skills").joinpath("bundled")
        return {
            f"{name}/{directory.name}/{entry.name}": entry.read_text(encoding="utf-8")
            for name in SkillBundle.names
            for directory in sorted(root.joinpath(name).iterdir(), key=SkillBundle._name)
            if directory.is_dir()
            for entry in sorted(directory.iterdir(), key=SkillBundle._name)
            if entry.name.endswith(".md")
        }

    @staticmethod
    def _name(entry: Traversable) -> str:
        """Order bundled files by name so installs are reproducible."""
        return entry.name

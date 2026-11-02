"""The authoring API as agents need it: exact signatures and one line each, rendered from the code itself.

``bun run generate`` writes it into the labqoat-runs skill; a test fails when the file and the code disagree, so the
reference is never stale.
"""

from __future__ import annotations

import inspect
import re
from importlib import import_module
from pathlib import Path
from typing import ClassVar


class SdkReference:
    """Render the public members of the classes an authored app touches."""

    SUBJECTS: ClassVar[tuple[tuple[str, str, str], ...]] = (
        ("labqoat.compute.app", "App", "compute.App"),
        ("labqoat.compute.image", "Image", "compute.Image"),
        ("labqoat.compute.volume", "Volume", "compute.Volume"),
        ("labqoat.compute.secret", "Secret", "Secret"),
        ("labqoat.run_context", "RunContext", "RunContext"),
        ("labqoat.training.training_metrics", "TrainingMetrics", "context.training()"),
        ("labqoat.compute.function", "Function", "a decorated function"),
        ("labqoat.runs.run_handle", "RunHandle", "RunHandle"),
        ("labqoat.coordination.dict", "Dict", "Dict"),
        ("labqoat.coordination.queue", "Queue", "Queue"),
        ("labqoat.sandbox.sandbox", "Sandbox", "Sandbox"),
    )
    PATH: ClassVar[Path] = Path(__file__).parent / "bundled" / "labqoat-runs" / "reference" / "sdk.md"
    HEADER: ClassVar[str] = (
        "# SDK reference\n\n"
        "Exact signatures of the authoring API, generated from the code by `bun run generate`; do not edit. Read\n"
        "this instead of the SDK source. Defaults shown are the real defaults.\n"
    )

    @classmethod
    def render(cls) -> str:
        """The whole reference as Markdown."""
        sections = [cls.section(module, name, title) for module, name, title in cls.SUBJECTS]
        return cls.HEADER + "".join(sections)

    @classmethod
    def section(cls, module: str, name: str, title: str) -> str:
        """One class: its own summary, then each public member with its signature and summary."""
        subject = getattr(import_module(module), name)
        lines = [f"\n## {title}\n\n{cls.summary(subject)}\n"]
        for member, value in sorted(vars(subject).items()):
            line = cls.member(member, value)
            if line is not None:
                lines.append(line)
        return "\n".join(lines) + "\n"

    @classmethod
    def member(cls, name: str, value: object) -> str | None:
        """`name(signature)`: summary, for a public method, class method, static method or property."""
        if name.startswith("_"):
            return None
        if isinstance(value, property):
            return f"- `{name}` (property): {cls.summary(value.fget)}"
        function = value.__func__ if isinstance(value, (classmethod, staticmethod)) else value
        if not inspect.isfunction(function):
            return None
        signature = str(inspect.signature(function)).replace("(self, ", "(").replace("(self)", "()")
        signature = signature.replace("(cls, ", "(").replace("(cls)", "()")
        return f"- `{name}{cls.plain(signature)}`: {cls.summary(function)}"

    @staticmethod
    def plain(signature: str) -> str:
        """Types by their bare names, the same on every Python version: `Image`, not `labqoat.compute.image.Image`."""
        stable = re.sub(r" at 0x[0-9a-f]+", "", signature)
        bare = re.sub(r"\b(?:[A-Za-z_][A-Za-z0-9_]*\.)+([A-Za-z_][A-Za-z0-9_]*)", r"\1", stable)
        return re.sub(r"'([A-Za-z_][A-Za-z0-9_\[\], |]*)'", r"\1", bare)

    @staticmethod
    def summary(value: object) -> str:
        """The first line of an object's docstring."""
        return (inspect.getdoc(value) or "").split("\n", 1)[0]

    @classmethod
    def write(cls) -> None:
        """Write the reference into the bundled skill."""
        cls.PATH.write_text(cls.render(), encoding="utf-8")

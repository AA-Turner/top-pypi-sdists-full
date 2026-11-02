"""Which `Checkpoint | None` parameter a function restores itself from when its run resumes."""

from dataclasses import dataclass

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class ResumeDeclaration:
    """Name the resume parameter and, optionally, the checkpoint key prefix a resume may pick from."""

    argument: str
    key_prefix: str | None = None

    def capture(self, parameters: tuple[str, ...]) -> dict[str, JsonValue]:
        """The declaration as published, after checking it names one of the function's checkpoint parameters."""
        if self.argument not in parameters:
            raise ValueError(
                f"with_resume({self.argument!r}) must name a parameter annotated `Checkpoint[...] | None`; "
                f"this function has {', '.join(parameters) or 'none'}"
            )
        if self.key_prefix is not None and not 1 <= len(self.key_prefix) <= 200:
            raise ValueError("with_resume key_prefix must be 1 to 200 characters")
        declaration: dict[str, JsonValue] = {"argument": self.argument}
        if self.key_prefix is not None:
            declaration["key_prefix"] = self.key_prefix
        return declaration

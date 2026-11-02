"""A generated field's structural Python annotation and schema-owned value decoder."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldType:
    """Keep static type declarations and numeric decoding derived from the same schema shape."""

    annotation: str
    shape: str
    records: tuple[str, ...] = ()

    def optional_annotation(self) -> str:
        """Place explicit absence before nullable suffixes for clear Python union declarations."""
        return (
            self.annotation.removesuffix(" | None")
            + " | Missing"
            + (" | None" if self.annotation.endswith(" | None") else "")
        )

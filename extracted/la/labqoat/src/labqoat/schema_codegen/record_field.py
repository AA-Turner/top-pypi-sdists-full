"""One schema property and its deterministically generated Python field declaration."""

from dataclasses import dataclass

from labqoat.schema_codegen.field_type import FieldType


@dataclass(frozen=True)
class RecordField:
    """Retain JSON names separately from Python names and explicit optional absence."""

    name: str
    python_name: str
    type: FieldType
    required: bool

    def declaration(self) -> str:
        """Declare a typed dataclass constructor field without applying schema defaults."""
        annotation = self.type.annotation if self.required else self.type.optional_annotation()
        suffix = "" if self.required else " = Missing.VALUE"
        return f"    {self.python_name}: {annotation}{suffix}"

    def decoder(self, index: int) -> str:
        """Decode validated structure with generated metadata instead of Python reflection."""
        value = f"cast({self.type.annotation!r}, cls._shapes[{index}].decode(values[{self.name!r}]))"
        if not self.required:
            value = f"{value} if {self.name!r} in values else Missing.VALUE"
        return f"            {self.python_name}={value},"

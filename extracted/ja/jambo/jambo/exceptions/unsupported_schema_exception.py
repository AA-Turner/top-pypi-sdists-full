from typing_extensions import Optional


class UnsupportedSchemaException(ValueError):
    """Exception raised for unsupported JSON schemas."""

    def __init__(
        self,
        message: str,
        unsupported_field: Optional[str] = None,
        cause: Optional[BaseException] = None,
    ) -> None:
        # Normalize message by stripping redundant prefix if present
        message = message.removeprefix("Unsupported JSON Schema: ")
        self.unsupported_field = unsupported_field
        self.cause = cause
        super().__init__(message)

    def __str__(self) -> str:
        base_msg = f"Unsupported JSON Schema: {super().__str__()}"
        if self.unsupported_field:
            return f"{base_msg} (unsupported field: {self.unsupported_field})"
        return base_msg

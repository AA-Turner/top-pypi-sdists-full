from typing_extensions import Optional


class InvalidSchemaException(ValueError):
    """Exception raised for invalid JSON schemas."""

    def __init__(
        self,
        message: str,
        invalid_field: Optional[str] = None,
        cause: Optional[BaseException] = None,
    ) -> None:
        # Normalize message by stripping redundant prefix if present
        message = message.removeprefix("Invalid JSON Schema: ")
        self.invalid_field = invalid_field
        self.cause = cause
        super().__init__(message)

    def __str__(self) -> str:
        base_msg = f"Invalid JSON Schema: {super().__str__()}"
        if self.invalid_field:
            return f"{base_msg} (invalid field: {self.invalid_field})"
        if self.cause:
            return (
                f"{base_msg} (caused by {self.cause.__class__.__name__}: {self.cause})"
            )
        return base_msg

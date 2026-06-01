class InternalAssertionException(RuntimeError):
    """Exception raised for internal assertions."""

    def __init__(
        self,
        message: str,
    ) -> None:
        # Normalize message by stripping redundant prefix if present
        message = message.removeprefix("Internal Assertion Failed: ")
        super().__init__(message)

    def __str__(self) -> str:
        return (
            f"Internal Assertion Failed: {super().__str__()}\n"
            "This is likely a bug in Jambo. Please report it at"
        )

"""Source-located authoritative dataset errors."""


class DataValidationError(ValueError):
    """Retain the logical source path, one-based row, and schema or physical diagnostic."""

    def __init__(self, source: str, row: int, detail: str) -> None:
        """Keep structured location information for both CLI and publication failures."""
        self.source = source
        self.row = row
        self.detail = detail
        super().__init__(f"{source}:{row}\n  {detail}")

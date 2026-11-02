"""Typed failure for captured-schema validation."""

from labqoat.schemas.schema_issue import SchemaIssue


class SchemaValidationError(ValueError):
    """Retain all path-based validation failures for CLI and runtime callers."""

    def __init__(self, issues: tuple[SchemaIssue, ...]) -> None:
        """Capture immutable diagnostics without coercing the rejected value."""
        self.issues = issues
        super().__init__("; ".join(f"{issue.pointer or '/'}: {issue.message}" for issue in issues))

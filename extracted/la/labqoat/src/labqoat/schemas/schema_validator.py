"""Draft 2020-12 validation with captured references and annotation-only formats."""

import json
from collections.abc import Mapping, Sequence

from jsonschema_rs import Draft202012Validator, FancyRegexOptions

from labqoat.json_document import JsonValue
from labqoat.schemas.captured_resolver import CapturedResolver
from labqoat.schemas.schema_issue import SchemaIssue
from labqoat.schemas.schema_validation_error import SchemaValidationError


class SchemaValidator:
    """Compile standards validation independently of Python or Parquet representation."""

    def __init__(self, validator: Draft202012Validator) -> None:
        """Keep a compiled validator ready for bounded-memory row iteration."""
        self._validator = validator

    @classmethod
    def compile(
        cls, schema: dict[str, JsonValue] | bool, resources: Mapping[str, dict[str, JsonValue]] | None = None
    ) -> "SchemaValidator":
        """Check the meta-schema and bind a closed, explicit resource resolver."""
        resolver = CapturedResolver(resources or {})
        return cls(
            Draft202012Validator(
                json.dumps(schema, allow_nan=False),
                retriever=resolver.retrieve,
                validate_formats=False,
                pattern_options=FancyRegexOptions(backtrack_limit=10_000),
            )
        )

    def issues(self, value: JsonValue) -> tuple[SchemaIssue, ...]:
        """Return deterministic JSON Pointer diagnostics without changing values."""
        errors = self._validator.iter_errors(value)
        issues = [
            SchemaIssue(self._pointer(error.instance_path), self._pointer(error.schema_path), error.message)
            for error in errors
        ]
        return tuple(sorted(issues, key=self._issue_key))

    def validate(self, value: JsonValue) -> None:
        """Reject invalid values; defaults and formats remain annotations."""
        issues = self.issues(value)
        if issues:
            raise SchemaValidationError(issues)

    @staticmethod
    def _pointer(path: Sequence[str | int]) -> str:
        """Escape decoded property names according to RFC 6901."""
        return "".join("/" + str(part).replace("~", "~0").replace("/", "~1") for part in path)

    @staticmethod
    def _issue_key(issue: SchemaIssue) -> tuple[str, str, str]:
        """Keep diagnostic ordering independent of schema member order."""
        return issue.pointer, issue.schema_pointer, issue.message

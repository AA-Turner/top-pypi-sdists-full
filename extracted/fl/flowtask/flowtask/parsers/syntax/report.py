"""Pydantic models for the syntax-check pipeline.

Defines :class:`SyntaxIssue` (one problem) and :class:`SyntaxReport`
(aggregated result of a ``--syntax`` invocation).
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field


Severity = Literal["error", "warning", "info"]
Format = Literal["json", "yaml", "toml"]

_SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


class SyntaxIssue(BaseModel):
    """A single problem found while checking a task.

    Attributes:
        severity: Severity level of the issue (``"error"``, ``"warning"``,
            or ``"info"``).
        code: Stable machine-readable code, e.g. ``"E_PARSE"``,
            ``"E_ROOT_SCHEMA"``, ``"E_UNKNOWN_COMPONENT"``,
            ``"W_UNDOCUMENTED"``, ``"E_MISSING_ATTR"``,
            ``"W_UNKNOWN_ATTR"``.
        message: Human-readable description of the problem.
        step_index: Zero-based index of the step in the ``steps`` array,
            or ``None`` for top-level issues.
        component: Name of the component class involved, if applicable.
        attribute: Name of the attribute involved, if applicable.
        location: JSON pointer or YAML line reference where available.
    """

    severity: Severity
    code: str = Field(
        description=(
            'Stable machine code, e.g. "E_PARSE", "E_ROOT_SCHEMA", '
            '"E_UNKNOWN_COMPONENT", "W_UNDOCUMENTED", "E_MISSING_ATTR", '
            '"W_UNKNOWN_ATTR".'
        )
    )
    message: str
    step_index: Optional[int] = None
    component: Optional[str] = None
    attribute: Optional[str] = None
    location: Optional[str] = None  # JSON pointer / YAML line where available


class SyntaxReport(BaseModel):
    """Aggregate result for a single ``--syntax`` invocation.

    Attributes:
        file: Path or label of the task file that was checked.
        fmt: Format detected (``"json"``, ``"yaml"``, or ``"toml"``).
        ok: ``True`` when no errors were found; ``False`` otherwise.
        issues: List of :class:`SyntaxIssue` instances, possibly empty.
    """

    file: str
    fmt: Format
    ok: bool
    issues: list[SyntaxIssue] = Field(default_factory=list)

    def has_errors(self) -> bool:
        """Return ``True`` iff at least one issue has severity ``"error"``.

        Returns:
            ``True`` if any issue is an error; ``False`` otherwise.
        """
        return any(i.severity == "error" for i in self.issues)

    def to_text(self) -> str:
        """Render a human-readable report grouped by step.

        Layout::

            <file> [<fmt>]
            <N> error(s), <M> warning(s)

            Step 0: <Component>
              [error] E_MISSING_ATTR — required attribute "dataset" missing
              [warning] W_UNKNOWN_ATTR — attribute "typo" not in schema

            <General>
              [error] E_PARSE — yaml.scanner.ScannerError ...

        Returns:
            Multi-line human-readable string.
        """
        lines: list[str] = []
        # Header
        lines.append(f"{self.file} [{self.fmt}]")

        # Summary counts
        n_errors = sum(1 for i in self.issues if i.severity == "error")
        n_warnings = sum(1 for i in self.issues if i.severity == "warning")
        status = "OK" if self.ok else "FAIL"
        lines.append(
            f"{status}: {n_errors} error(s), {n_warnings} warning(s)"
        )

        if not self.issues:
            return "\n".join(lines)

        # Group by step_index (None → general bucket)
        step_groups: dict[Optional[int], list[SyntaxIssue]] = {}
        for issue in self.issues:
            key = issue.step_index
            step_groups.setdefault(key, []).append(issue)

        # Collect step indices in ascending order, general (None) last
        indexed = sorted(
            (k for k in step_groups if k is not None)
        )
        ordered_keys: list[Optional[int]] = list(indexed)
        if None in step_groups:
            ordered_keys.append(None)

        for key in ordered_keys:
            bucket = step_groups[key]
            # Sort issues within group: errors first, then warnings, then info
            bucket_sorted = sorted(
                bucket, key=lambda i: _SEVERITY_ORDER.get(i.severity, 99)
            )
            if key is None:
                lines.append("\n<General>")
            else:
                # Pick the component name from the first issue with one
                comp = next(
                    (i.component for i in bucket_sorted if i.component), None
                )
                header = f"Step {key}"
                if comp:
                    header += f": {comp}"
                lines.append(f"\n{header}")

            for issue in bucket_sorted:
                attr_suffix = f' (attribute: "{issue.attribute}")' if issue.attribute else ""
                lines.append(
                    f"  [{issue.severity}] {issue.code} — {issue.message}{attr_suffix}"
                )

        return "\n".join(lines)

    def to_json(self) -> str:
        """Return the report serialised with Pydantic v2 ``model_dump_json``.

        Returns:
            JSON string with a trailing newline for clean shell output.
        """
        return self.model_dump_json() + "\n"

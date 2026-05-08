"""Static syntax checker for Flowtask task definitions.

The checker does NOT execute the task, does NOT touch the worker, scheduler,
or event subsystems. It is safe to invoke from editors and CI.
"""
import asyncio
import logging
from pathlib import Path
from typing import Iterator, Literal, Optional

from jsonschema import Draft7Validator

from ...exceptions import TaskParseError
from ..json import JSONParser
from .._yaml import YAMLParser
from ..toml import TOMLParser
from .detector import detect_format, sniff_format
from .registry import ComponentSchemaRegistry
from .report import SyntaxIssue, SyntaxReport
from .schema import ROOT_TASK_SCHEMA


_PARSER_FOR: dict[str, type] = {
    "json": JSONParser,
    "yaml": YAMLParser,
    "toml": TOMLParser,
}

# Pre-built validator for the root task schema — constant, never changes.
_ROOT_VALIDATOR = Draft7Validator(ROOT_TASK_SCHEMA)


class SyntaxChecker:
    """Static, side-effect-free task-definition checker.

    Does NOT execute the task, does NOT touch the worker, scheduler, or
    event subsystems. Safe to invoke from editors and CI.

    Args:
        registry: Optional :class:`~flowtask.parsers.syntax.registry.ComponentSchemaRegistry`
            instance.  When ``None``, a default one is instantiated (uses
            ``BASE_DIR/docs/``).
        strict: When ``True``, undocumented components are reported as errors
            instead of warnings.
    """

    def __init__(
        self,
        *,
        registry: Optional[ComponentSchemaRegistry] = None,
        strict: bool = False,
    ) -> None:
        self.registry = registry or ComponentSchemaRegistry()
        self.strict = strict
        self.logger = logging.getLogger("FlowTask.Syntax")

    async def check_file(self, path: str | Path) -> SyntaxReport:
        """Check a task definition file on disk.

        Args:
            path: Filesystem path to the task file.  Format is inferred from
                the file suffix.

        Returns:
            :class:`~flowtask.parsers.syntax.report.SyntaxReport` with all
            found issues.
        """
        path = Path(path)
        fmt = detect_format(path)
        content = await asyncio.to_thread(path.read_text, encoding="utf-8")
        return await self._run(content, fmt, str(path))

    async def check_content(
        self,
        content: str,
        fmt: Optional[Literal["json", "yaml", "toml"]] = None,
        source_label: str = "<inline>",
    ) -> SyntaxReport:
        """Check a task definition supplied as a string.

        Args:
            content: Raw task definition as a string.
            fmt: Explicit format (``"json"``, ``"yaml"``, or ``"toml"``).
                When ``None``, :func:`~flowtask.parsers.syntax.detector.sniff_format`
                is used to detect the format.
            source_label: Display name used in the report's ``file`` field.

        Returns:
            :class:`~flowtask.parsers.syntax.report.SyntaxReport` with all
            found issues.
        """
        fmt_resolved = fmt or sniff_format(content)
        return await self._run(content, fmt_resolved, source_label)

    # --- internals ---------------------------------------------------------

    async def _run(self, content: str, fmt: str, label: str) -> SyntaxReport:
        """Execute the four-phase pipeline and return the report.

        Phases:
            1. Parse the content with the appropriate parser.
            2. Validate against ROOT_TASK_SCHEMA.
            3. Walk the ``steps`` array and validate each step.
            4. Aggregate into a SyntaxReport.

        Args:
            content: Raw task definition string.
            fmt: Format string (``"json"``, ``"yaml"``, ``"toml"``).
            label: Source label for the report's ``file`` field.

        Returns:
            :class:`~flowtask.parsers.syntax.report.SyntaxReport`.
        """
        issues: list[SyntaxIssue] = []
        parser_cls = _PARSER_FOR[fmt]
        parser = parser_cls(content=content)

        # Phase 1: Parse
        try:
            parsed = await parser.parse(content)
        except TaskParseError as err:
            issues.append(SyntaxIssue(
                severity="error",
                code="E_PARSE",
                message=str(err),
            ))
            return SyntaxReport(file=label, fmt=fmt, ok=False, issues=issues)

        # Phase 2: Root schema validation — collect all errors at once.
        for err in _ROOT_VALIDATOR.iter_errors(parsed):
            issues.append(SyntaxIssue(
                severity="error",
                code="E_ROOT_SCHEMA",
                message=err.message,
                location="/" + "/".join(str(p) for p in err.absolute_path)
                if err.absolute_path else None,
            ))

        # Phase 3: Walk steps
        steps = parsed.get("steps", []) if isinstance(parsed, dict) else []
        for idx, step in enumerate(steps):
            issues.extend(self._check_step(idx, step))

        # Phase 4: Aggregate
        ok = not any(i.severity == "error" for i in issues)
        return SyntaxReport(file=label, fmt=fmt, ok=ok, issues=issues)

    def _check_step(self, idx: int, step: object) -> list[SyntaxIssue]:
        """Validate a single step entry.

        Args:
            idx: Zero-based index of the step in the ``steps`` array.
            step: The step value from the parsed task dict.

        Returns:
            List of :class:`~flowtask.parsers.syntax.report.SyntaxIssue`
            instances; empty when the step is valid.
        """
        if not isinstance(step, dict) or len(step) != 1:
            return [SyntaxIssue(
                severity="error",
                code="E_STEP_SHAPE",
                step_index=idx,
                message=(
                    "Each step must be a single-key dict whose key is the "
                    "component name."
                ),
            )]
        name, body = next(iter(step.items()))

        if not self.registry.has(name):
            severity = "error" if self.strict else "warning"
            code = "E_UNKNOWN_COMPONENT" if self.strict else "W_UNDOCUMENTED"
            return [SyntaxIssue(
                severity=severity,
                code=code,
                step_index=idx,
                component=name,
                message=f"Component {name!r} is not in the documentation index.",
            )]

        schema = self.registry.get(name)
        if not schema:
            return [SyntaxIssue(
                severity="warning",
                code="W_UNDOCUMENTED",
                step_index=idx,
                component=name,
                message=f"Schema file for {name!r} is missing on disk.",
            )]

        return list(self._validate_step_body(idx, name, body, schema))

    def _validate_step_body(
        self,
        idx: int,
        name: str,
        body: object,
        schema: dict,
    ) -> Iterator[SyntaxIssue]:
        """Validate the body of a step against its component schema.

        Args:
            idx: Zero-based step index.
            name: Component class name.
            body: Step body value (should be a dict).
            schema: Component JSON Schema dict.

        Yields:
            :class:`~flowtask.parsers.syntax.report.SyntaxIssue` instances.
        """
        if not isinstance(body, dict):
            yield SyntaxIssue(
                severity="error",
                code="E_STEP_BODY",
                step_index=idx,
                component=name,
                message="Step body must be an object/dict.",
            )
            return

        for err in Draft7Validator(schema).iter_errors(body):
            v = err.validator
            if v == "required":
                # Extract the missing attribute name from the error message.
                missing = err.message.split("'")[1] if "'" in err.message else "?"
                yield SyntaxIssue(
                    severity="error",
                    code="E_MISSING_ATTR",
                    step_index=idx,
                    component=name,
                    attribute=missing,
                    message=err.message,
                )
            elif v == "additionalProperties":
                # Names of unknown attributes appear in err.message; surface as warnings.
                yield SyntaxIssue(
                    severity="warning",
                    code="W_UNKNOWN_ATTR",
                    step_index=idx,
                    component=name,
                    message=err.message,
                )
            elif v == "type":
                # Per spec §1 Non-Goals: do not enforce attribute-value types.
                # The schema generator emits "type": "string" for every property
                # regardless of the true Python type; type errors would be false positives.
                continue
            else:
                yield SyntaxIssue(
                    severity="warning",
                    code="W_SCHEMA",
                    step_index=idx,
                    component=name,
                    message=err.message,
                )

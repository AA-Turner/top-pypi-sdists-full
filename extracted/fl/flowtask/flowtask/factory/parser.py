"""Pure YAML parser for Flowtask task definitions.

Produces a :class:`ParsedTask` from raw YAML text without touching component
schemas, the runtime, or variable resolution. Schema-level checks live in
:mod:`flowtask.factory.validator`; YAML-shape errors are raised here as
:class:`ParserError`.

Expected YAML shape (matches existing tasks under ``tasks/programs/*``)::

    name: My task
    description: optional one-liner
    steps:
      - DownloadFromSharepoint:
          credentials: ...
          site: contoso
          ...
      - CopyToPg:
          tablename: foo
          schema: bar
"""
from __future__ import annotations

from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class ParserError(ValueError):
    """Raised when the YAML does not match the Flowtask task shape.

    Carries the offending YAML location (1-based line, when available) so
    callers can surface it back to the user.
    """

    def __init__(self, message: str, *, line: Optional[int] = None) -> None:
        self.line = line
        super().__init__(f"{message} (line {line})" if line else message)


class ParsedStep(BaseModel):
    """A single step extracted from the YAML, before schema validation."""

    step_index: int = Field(..., description="0-based position within `steps`.")
    component: str = Field(..., description="Component class name (the single key of the step mapping).")
    attrs: dict[str, Any] = Field(default_factory=dict, description="Attribute block as-is.")
    line: Optional[int] = Field(None, description="1-based YAML line where this step starts, when known.")


class ParsedTask(BaseModel):
    """Top-level task description after parsing — never validated against schemas."""

    name: Optional[str] = None
    description: Optional[str] = None
    steps: list[ParsedStep] = Field(default_factory=list)


class YamlTaskParser:
    """Parse Flowtask YAML task definitions.

    Stateless — instantiate once and reuse, or call :meth:`parse` directly.
    """

    def parse(self, text: str) -> ParsedTask:
        """Parse a YAML string into a :class:`ParsedTask`.

        Args:
            text: Raw YAML text.

        Returns:
            ParsedTask. Empty ``steps`` is permitted (e.g. user-saved drafts).

        Raises:
            ParserError: On invalid YAML or task-shape violations.
        """
        try:
            loader = yaml.SafeLoader(text)
            try:
                node = loader.get_single_node()
            finally:
                loader.dispose()
        except yaml.YAMLError as exc:
            line = _line_from_yaml_error(exc)
            raise ParserError(f"Invalid YAML: {exc}", line=line) from exc

        if node is None:
            raise ParserError("Empty YAML document; expected a task mapping.")

        if not isinstance(node, yaml.MappingNode):
            raise ParserError(
                "Top-level YAML must be a mapping with `name`/`description`/`steps`.",
                line=_node_line(node),
            )

        data = _construct_mapping(node)

        if "steps" not in data:
            raise ParserError("Missing required key `steps`.", line=_node_line(node))

        steps_raw = data.get("steps")
        if steps_raw is None:
            steps_raw = []

        if not isinstance(steps_raw, list):
            raise ParserError(
                "`steps` must be a list of single-key mappings.",
                line=_find_key_line(node, "steps"),
            )

        # Line lookup table for each step entry, when available.
        step_lines = _step_lines(node)

        steps: list[ParsedStep] = []
        for idx, item in enumerate(steps_raw):
            line = step_lines[idx] if idx < len(step_lines) else None
            if not isinstance(item, dict):
                raise ParserError(
                    f"Step #{idx} must be a single-key mapping, got {type(item).__name__}.",
                    line=line,
                )
            if len(item) != 1:
                raise ParserError(
                    f"Step #{idx} must declare exactly one component, found {len(item)}.",
                    line=line,
                )
            (component, attrs), = item.items()
            if not isinstance(component, str):
                raise ParserError(
                    f"Step #{idx} component name must be a string, got {type(component).__name__}.",
                    line=line,
                )
            if attrs is None:
                attrs_dict: dict[str, Any] = {}
            elif isinstance(attrs, dict):
                attrs_dict = attrs
            else:
                raise ParserError(
                    f"Step #{idx} (`{component}`) attributes must be a mapping, got {type(attrs).__name__}.",
                    line=line,
                )
            steps.append(
                ParsedStep(
                    step_index=idx,
                    component=component,
                    attrs=attrs_dict,
                    line=line,
                )
            )

        return ParsedTask(
            name=_optional_string(data.get("name")),
            description=_optional_string(data.get("description")),
            steps=steps,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _construct_mapping(node: yaml.MappingNode) -> dict[str, Any]:
    """Construct a plain dict from a YAML MappingNode preserving order.

    We deliberately go through a fresh ``SafeLoader`` so we get the same
    value semantics as ``yaml.safe_load`` (no custom tags, no arbitrary
    Python objects), while keeping access to the node tree for line lookups.
    """
    loader = yaml.SafeLoader("")
    try:
        return loader.construct_mapping(node, deep=True)
    finally:
        loader.dispose()


def _node_line(node: yaml.Node) -> Optional[int]:
    """1-based line number for a YAML node, when available."""
    mark = getattr(node, "start_mark", None)
    return mark.line + 1 if mark is not None else None


def _find_key_line(mapping: yaml.MappingNode, key: str) -> Optional[int]:
    """Find the YAML line of a particular top-level key."""
    for key_node, _value_node in mapping.value:
        if isinstance(key_node, yaml.ScalarNode) and key_node.value == key:
            return _node_line(key_node)
    return _node_line(mapping)


def _step_lines(top_mapping: yaml.MappingNode) -> list[Optional[int]]:
    """Return per-step 1-based line numbers from the `steps` sequence."""
    for key_node, value_node in top_mapping.value:
        if not (isinstance(key_node, yaml.ScalarNode) and key_node.value == "steps"):
            continue
        if not isinstance(value_node, yaml.SequenceNode):
            return []
        return [_node_line(item) for item in value_node.value]
    return []


def _line_from_yaml_error(exc: yaml.YAMLError) -> Optional[int]:
    mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
    return mark.line + 1 if mark is not None else None


def _optional_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)

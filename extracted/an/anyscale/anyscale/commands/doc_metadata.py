"""Doc-spec metadata for CLI commands: the command_metadata decorator, its
vocabulary models, and the build-time example expander used by cli_docgen.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from anyscale.commands.output_format import OutputFormat, render_output

# Re-exported: commands annotate error_codes= with ErrorCode from this module.
from anyscale.errors import ErrorCode  # noqa: F401


class ReleaseStatus(str, Enum):
    """Release status of a command in the doc spec."""

    PRIVATE = "private"
    ALPHA = "alpha"
    BETA = "beta"
    GA = "ga"
    DEPRECATED = "deprecated"


@dataclass(frozen=True)
class CommandExample:
    """Used in command_metadata decorator while defining CLI usage examples."""

    description: str
    command: str
    output_raw: Optional[str] = None
    output_instance: Any = None
    labels: Optional[List[str]] = None


# Keys accepted by command_metadata.
ANNOTATABLE_COMMAND_KEYS = frozenset(
    {
        "description",
        "status",
        "since",
        "output_formats",
        "output_schema",
        "option_docs",
        "argument_docs",
        "examples",
        "error_codes",
        "related",
        "changed",
        "deprecation_info",
    }
)


def command_metadata(**kwargs):
    """Attach a command's document metadata to a Click command as a decorator."""
    unknown = set(kwargs) - ANNOTATABLE_COMMAND_KEYS
    if unknown:
        raise ValueError(
            f"command_metadata got unsupported key(s) {sorted(unknown)}; "
            f"allowed: {sorted(ANNOTATABLE_COMMAND_KEYS)}"
        )

    # deprecation_info only makes sense for a deprecated command.
    if (
        "deprecation_info" in kwargs
        and kwargs.get("status") != ReleaseStatus.DEPRECATED
    ):
        raise ValueError(
            "command_metadata: 'deprecation_info' is only valid when status is "
            f"{ReleaseStatus.DEPRECATED.value!r}; got status={kwargs.get('status')!r}"
        )

    def wrap(cmd):
        cmd.doc_metadata = kwargs
        return cmd

    return wrap


def build_doc_examples(
    example: CommandExample,
    output_formats: List[OutputFormat],
    table_columns: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Expand CommandExample into one docs Example per format.

    Format is selected with -o <format>; text is the default (no flag).
    """
    instance = (
        example.output_instance()
        if callable(example.output_instance)
        else example.output_instance
    )

    examples: List[Dict[str, Any]] = []
    for fmt in output_formats:
        if fmt == OutputFormat.TEXT:
            output = example.output_raw
        elif instance is None:
            # No output_instance to render a structured example from; skip this
            # format rather than emitting a null-rendered "output".
            continue
        else:
            output = render_output(instance, fmt, table_columns=table_columns)
        entry: Dict[str, Any] = {
            "description": example.description,
            "command": example.command,
            "format": fmt,
            "output": output,
        }
        if example.labels is not None:
            entry["labels"] = example.labels
        examples.append(entry)
    return examples

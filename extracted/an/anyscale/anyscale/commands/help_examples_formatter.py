"""Rendering of command examples for inline --help output."""
from typing import Any, Dict, Iterable, List, Optional

from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    render_output,
)


# Structured formats shown in --help, most agent-friendly first.
_HELP_FORMAT_PRIORITY = (OutputFormat.JSON, OutputFormat.YAML, OutputFormat.TABLE)


def render_examples_for_help(doc_metadata: Optional[Dict[str, Any]]) -> str:
    """Render the --help Examples block from a command's doc_metadata."""
    meta = doc_metadata or {}
    examples = meta.get("examples")
    if not examples:
        return ""
    formats = meta.get("output_formats") or []
    output_format = next(
        (fmt.value for fmt in _HELP_FORMAT_PRIORITY if fmt in formats),
        OutputFormat.TEXT.value,
    )
    return format_structured_examples_for_help(examples, output_format)


def format_structured_examples_for_help(
    examples: Iterable[Any], output_format: str = OutputFormat.TEXT.value
) -> str:
    """Render structured CommandExample entries for --help.

    1. Text output: output_raw is shown as-is to provide backward compatibility.
    2. Structured output (json, yaml or table): the command is shown with
        -o <format> followed by output_instance rendered in that format.
    """
    blocks: List[str] = []
    for example in examples:
        command = getattr(example, "command", None)
        if not command:
            continue
        lines: List[str] = []
        description = getattr(example, "description", None)
        if description:
            lines.append(f"# {description}")
        structured_output = (
            _structured_example_output(example, output_format)
            if output_format != OutputFormat.TEXT.value
            else None
        )
        if structured_output is not None:
            command = command.strip()
            if not _has_output_flag(command):
                command += f" {OUTPUT_FLAG} {output_format}"
            lines.append(f"$ {command}")
            lines.append(structured_output.rstrip("\n"))
        else:
            output_raw = getattr(example, "output_raw", None)
            lines.append(
                output_raw.rstrip("\n") if output_raw else f"$ {command.strip()}"
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _has_output_flag(command: str) -> bool:
    """True if the command already passes -o/--output as its own argument."""
    return any(
        token in (OUTPUT_FLAG, OUTPUT_FLAG_LONG)
        or token.startswith(f"{OUTPUT_FLAG_LONG}=")
        for token in command.split()
    )


def _structured_example_output(example: Any, output_format: str) -> Optional[str]:
    """Render an example's output_instance in output_format, or None if it cannot be rendered."""
    try:
        instance = getattr(example, "output_instance", None)
        if callable(instance):
            instance = instance()
        if instance is None:
            return None
        return render_output(instance, output_format)
    except Exception:  # noqa: BLE001
        return None

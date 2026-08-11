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


# The flag most commands use to select an output format (-o json).
_OUTPUT_FORMAT_FLAG = OUTPUT_FLAG
# Commands that reserve -o/--output for an output *file* expose this option to
# select the format instead; appending -o to their examples would write a file.
_OUTPUT_FORMAT_OPTION = "--output-format"


def format_flag_for_command(command: Any) -> str:
    """Return the flag that selects the output format for a Click command.

    Most commands use -o/--output; the few that reserve -o/--output for an
    output file expose a separate --output-format option, so structured
    examples for those must be shown with --output-format instead.
    """
    for param in getattr(command, "params", None) or []:
        opts = list(getattr(param, "opts", []) or [])
        opts += list(getattr(param, "secondary_opts", []) or [])
        if _OUTPUT_FORMAT_OPTION in opts:
            return _OUTPUT_FORMAT_OPTION
    return _OUTPUT_FORMAT_FLAG


def render_examples_for_help(
    doc_metadata: Optional[Dict[str, Any]], output_flag: str = _OUTPUT_FORMAT_FLAG,
) -> str:
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
    return format_structured_examples_for_help(examples, output_format, output_flag)


def format_structured_examples_for_help(
    examples: Iterable[Any],
    output_format: str = OutputFormat.TEXT.value,
    output_flag: str = _OUTPUT_FORMAT_FLAG,
) -> str:
    """Render structured CommandExample entries for --help.

    1. Text output: the command is shown as `$ <command>`, followed by
        output_raw (console output only) when present.
    2. Structured output (json, yaml or table): the command is shown with
        `<output_flag> <format>` followed by output_instance rendered in that
        format. output_flag is -o for most commands and --output-format for
        commands whose -o/--output selects an output file.
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
            if not _has_output_flag(command, output_flag):
                command += f" {output_flag} {output_format}"
            lines.append(f"$ {command}")
            lines.append(structured_output.rstrip("\n"))
        else:
            lines.append(f"$ {command.strip()}")
            output_raw = getattr(example, "output_raw", None)
            if output_raw:
                lines.append(output_raw.rstrip("\n"))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _has_output_flag(command: str, output_flag: str = _OUTPUT_FORMAT_FLAG) -> bool:
    """True if the command already passes its output-format flag as an argument."""
    aliases = {output_flag}
    if output_flag == OUTPUT_FLAG:
        aliases.add(OUTPUT_FLAG_LONG)
    tokens = command.split()
    return any(
        token == alias or token.startswith(f"{alias}=")
        for token in tokens
        for alias in aliases
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

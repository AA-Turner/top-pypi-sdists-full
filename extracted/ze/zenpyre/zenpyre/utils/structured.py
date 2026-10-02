r"""Utilities for inspecting what a structured-output Pydantic schema
actually sends to a language model.

When a Pydantic ``BaseModel`` is used as a structured-output schema (via
``chat_model.with_structured_output(...)`` or ``chat_model.bind_tools(...)``),
LangChain converts it into a JSON-schema tool spec: the class docstring
becomes the tool/function description, and each field's ``Field(description=...)``
becomes the description of the corresponding JSON schema property. That
converted spec is the literal text/structure included in the request sent to
the model.

These helpers expose that conversion directly, so a schema's docstring and
field descriptions can be inspected -- e.g. to debug a prompt that isn't
producing the expected structured output -- without needing to make a real
API call.

Typical usage:

    from zenpyre.utils.structured import ExampleEntity, format_structured_output_schema

    print(format_structured_output_schema(ExampleEntity))
"""

from __future__ import annotations

__all__ = [
    "ExampleEntity",
    "format_structured_output_schema",
    "get_structured_output_tool_spec",
    "print_structured_output_schema",
]

import json
from typing import TYPE_CHECKING, Any

from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import BaseModel, Field
from rich import get_console
from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from rich.console import Console


# Minimal, reusable schema for the doctest examples below -- so each example
# can just reference it instead of redefining a schema class inline (which
# would require an inner triple-quoted docstring nested inside this module's
# own docstrings).
class ExampleEntity(BaseModel):
    """Extract a single entity mentioned in the user's message."""

    name: str = Field(description="The full name of the entity.")


def get_structured_output_tool_spec(schema: type[BaseModel]) -> dict[str, Any]:
    """Convert a Pydantic schema into the tool spec LangChain sends to a
    chat model.

    This calls the same conversion function LangChain uses internally in
    ``bind_tools`` and ``with_structured_output``, so the returned dict
    reflects exactly what would be serialized into a real request: the class
    docstring as ``function.description`` and each field's
    ``Field(description=...)`` as ``function.parameters.properties.<name>.description``.

    Args:
        schema: The Pydantic model class used as a structured-output or
            tool-calling schema.

    Returns:
        The OpenAI-style tool spec dict, e.g.
        ``{"type": "function", "function": {"name": ..., "description": ...,
        "parameters": {...}}}``.

    Example:
        ```pycon
        >>> from zenpyre.utils.structured import ExampleEntity, get_structured_output_tool_spec
        >>> spec = get_structured_output_tool_spec(ExampleEntity)
        >>> spec["function"]["name"]
        'ExampleEntity'
        >>> spec["function"]["parameters"]["properties"]["name"]["description"]
        'The full name of the entity.'

        ```
    """
    return convert_to_openai_tool(schema)


def format_structured_output_schema(schema: type[BaseModel]) -> str:
    """Render a human-readable summary of a schema's docstring, JSON
    schema, and per-field descriptions.

    Args:
        schema: The Pydantic model class used as a structured-output or
            tool-calling schema.

    Returns:
        A multi-line string with the schema's name, docstring-derived
        description, full parameters JSON schema, and a per-field
        description/type/required breakdown -- intended for logging or
        printing during debugging.

    Example:
        ```pycon
        >>> from zenpyre.utils.structured import ExampleEntity, format_structured_output_schema
        >>> print(format_structured_output_schema(ExampleEntity))
        Class: ExampleEntity
        name: ExampleEntity
        description (from docstring): "Extract a single entity mentioned in the user's message."
        <BLANKLINE>
        parameters JSON schema (sent as the tool spec):
        {
          "properties": {
            "name": {
              "description": "The full name of the entity.",
              "type": "string"
            }
          },
          "required": [
            "name"
          ],
          "type": "object"
        }
        <BLANKLINE>
        Per-field breakdown:
          - name (string, required): 'The full name of the entity.'

        ```
    """
    tool_spec = get_structured_output_tool_spec(schema)
    fn = tool_spec["function"]
    parameters = fn.get("parameters", {})
    properties: dict[str, Any] = parameters.get("properties", {})
    required = set(parameters.get("required", []))

    lines = [
        f"Class: {schema.__name__}",
        f"name: {fn['name']}",
        f"description (from docstring): {fn.get('description') or '<none>'!r}",
        "",
        "parameters JSON schema (sent as the tool spec):",
        json.dumps(parameters, indent=2),
        "",
        "Per-field breakdown:",
    ]
    for name, spec in properties.items():
        desc = spec.get("description", "<no description set>")
        field_type = spec.get("type", spec.get("anyOf", "?"))
        status = "required" if name in required else "optional"
        lines.append(f"  - {name} ({field_type}, {status}): {desc!r}")

    return "\n".join(lines)


def print_structured_output_schema(schema: type[BaseModel], console: Console | None = None) -> None:
    """Pretty-print a schema's docstring, JSON schema, and per-field
    descriptions to the terminal using rich.

    Renders a bordered panel titled with the schema's class name,
    containing: the docstring-derived tool description, a
    syntax-highlighted JSON dump of the ``parameters`` schema exactly as
    it would be sent to a chat model, and a table of fields with their
    type, required/optional status, default, and description -- so a
    docstring or ``Field(description=...)`` that isn't coming through as
    expected is easy to spot at a glance.

    Args:
        schema: The Pydantic model class used as a structured-output or
            tool-calling schema.
        console: An optional rich :class:`~rich.console.Console` to
            print to. If ``None``, the current active console (as
            returned by :func:`rich.get_console`) is used.

    Example:
        ```pycon
        >>> from zenpyre.utils.structured import ExampleEntity, print_structured_output_schema
        >>> print_structured_output_schema(ExampleEntity)

        ```
    """
    console = console or get_console()

    tool_spec = get_structured_output_tool_spec(schema)
    fn = tool_spec["function"]
    parameters = fn.get("parameters", {})
    properties: dict[str, Any] = parameters.get("properties", {})
    required = set(parameters.get("required", []))

    description = fn.get("description")
    boxes: list[Any] = [
        (
            Text(description, style="italic")
            if description
            else Text("<no docstring>", style="dim italic")
        )
    ]

    json_panel = Panel(
        Syntax(
            json.dumps(parameters, indent=2),
            "json",
            theme="ansi_dark",
            background_color="default",
            word_wrap=True,
        ),
        title="parameters JSON schema",
        title_align="left",
        border_style="dim",
    )
    boxes.append(json_panel)

    table = Table(title="Fields", title_justify="left", border_style="dim", expand=True)
    table.add_column("Name", style="bold cyan", no_wrap=True)
    table.add_column("Type")
    table.add_column("Required")
    table.add_column("Default")
    table.add_column("Description")

    for name, spec in properties.items():
        field_type = str(spec.get("type", spec.get("anyOf", "?")))
        is_required = name in required
        default = "—" if is_required else str(spec.get("default", "—"))
        desc = spec.get("description")
        table.add_row(
            name,
            field_type,
            Text("required", style="bold red") if is_required else Text("optional", style="green"),
            default,
            desc or Text("<no description set>", style="dim italic"),
        )
    boxes.append(table)

    console.print(
        Panel(
            Group(*boxes),
            title=f"[bold]{schema.__name__}[/bold] [dim]({fn['name']})[/dim]",
            title_align="left",
            border_style="cyan",
        )
    )

"""Record references that accept the shortened identifiers lists display."""

from __future__ import annotations

import re
from typing import ClassVar

import click

from labqoat.cli.cli_context import CliContext
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument


class ReferenceArgument(click.ParamType[str]):
    """Expand a unique leading part of an identifier, as git does for commits; pass everything else through."""

    name = "reference"
    kinds: ClassVar[dict[str, str]] = {
        "run_ref": "run",
        "build_ref": "build",
        "checkpoint_ref": "checkpoint",
        "dashboard_ref": "dashboard",
        "repository_ref": "dataset_repository",
        "revision_ref": "dataset_revision",
        "node_ref": "node",
        "worker_ref": "worker",
    }

    def __init__(self, kind: str) -> None:
        """Bind the kind of record the argument names."""
        self.kind = kind

    def convert(self, value: object, param: click.Parameter | None, ctx: click.Context | None) -> str:
        """Ask the service only for values that can be the start of an identifier and are not a whole one."""
        text = str(value)
        digits = text.replace("-", "").lower()
        context = None if ctx is None else ctx.find_root().obj
        if re.fullmatch(r"[0-9a-f]{4,31}", digits) is None or not isinstance(context, CliContext):
            return text
        matches = self.matches(context, digits)
        if len(matches) > 1:
            self.fail(self.ambiguous(text, matches), param, ctx)
        return str(matches[0]["id"]) if matches else text

    def matches(self, context: CliContext, digits: str) -> list[JsonDocument]:
        """Records starting with the digits; none when the service cannot say, so the command reports as before."""
        client = context.management()
        try:
            found = client.get("/api/v1/references/resolve", {"kind": self.kind, "prefix": digits})
        except ApiError:
            return []
        finally:
            client.close()
        return [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(found["matches"])]

    def ambiguous(self, text: str, matches: list[JsonDocument]) -> str:
        """Name the candidates so the next attempt can be exact."""
        label = self.kind.replace("_", " ")
        listed = ", ".join(f"{item['id']}" + (f" ({item['label']})" if item.get("label") else "") for item in matches)
        return f"{text!r} is the start of more than one {label}: {listed}. Use more characters."

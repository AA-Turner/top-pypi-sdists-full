"""Shared execution for domain commands."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING

from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.cli.cli_context import CliContext


class CommandRunner:
    """Execute domain operations behind CLI commands."""

    @staticmethod
    def payload(kwargs: Mapping[str, object]) -> JsonDocument:
        """Load a JSON payload from file, stdin, or args."""
        file = kwargs.get("file")
        args = kwargs.get("args")
        if isinstance(file, str) and file and file != "-":
            return JsonDocument.expect_dict(json.loads(Path(file).read_text(encoding="utf-8")))
        if isinstance(file, str) and file == "-":
            import sys

            return JsonDocument.expect_dict(json.loads(sys.stdin.read() or "{}"))
        if isinstance(args, str) and args:
            return JsonDocument.expect_dict(json.loads(args))
        extra = {key: value for key, value in kwargs.items() if key not in {"as_json", "file", "args"}}
        return JsonDocument.expect_dict({key: value for key, value in extra.items() if value is not None})

    @staticmethod
    def assets_upload(context: CliContext, kwargs: Mapping[str, object]) -> JsonDocument:
        """Upload a file."""
        client = context.assets()
        try:
            from labqoat.cli.mutation_key import MutationKey

            media_type = str(kwargs.get("media_type") or "application/octet-stream")
            return client.upload_file(
                Path(str(kwargs.get("source") or "")), media_type, key=MutationKey.resolve(kwargs.get("key"))
            ).to_dict()
        finally:
            client.close()

    @staticmethod
    def assets_download(context: CliContext, kwargs: Mapping[str, object]) -> JsonDocument:
        """Download bytes and report size."""
        ref = str(kwargs.get("reference") or "")
        output_path = Path(str(kwargs.get("output") or ""))
        client = context.assets()
        try:
            byte_size = client.download_to(ref, output_path)
            return JsonDocument({"ref": ref, "bytes": byte_size, "output": str(output_path)})
        finally:
            client.close()

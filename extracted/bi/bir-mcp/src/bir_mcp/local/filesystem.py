import inspect
import tempfile
from typing import Annotated, override

import detect_secrets
import fastmcp
import pydantic

from bir_mcp.core import BaseMcp, build_readonly_tools


class Filesystem(BaseMcp):
    @override
    def get_tag(self):
        return "filesystem"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="MCP server with local filesystem tools",
            instructions=inspect.cleandoc("""
                Contains tools to work with local files.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            find_secrets,
            find_secrets_in_text,
        ]
        tools = build_readonly_tools(
            read_tools, max_output_length=max_output_length, tags={self.get_tag()}
        )
        return tools


def find_secrets(
    file_path: Annotated[
        str,
        pydantic.Field(description="The path to the file to scan for secrets."),
    ],
) -> dict:
    """
    Scans a file for secrets using the [detect-secrets](https://github.com/Yelp/detect-secrets) tool.
    """
    secrets = detect_secrets.SecretsCollection()
    with detect_secrets.settings.default_settings():
        secrets.scan_file(file_path)

    secrets = [
        {
            "secret_type": secret.type,
            "line_number": secret.line_number,
        }
        for file_secrets in secrets.data.values()
        for secret in file_secrets
    ]
    secrets = {"detected_secrets": secrets}
    return secrets


def find_secrets_in_text(text: str) -> dict:
    """Scan text content for secrets."""
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(text.encode())
        temp_file.flush()
        secrets = find_secrets(temp_file.name)

    return secrets

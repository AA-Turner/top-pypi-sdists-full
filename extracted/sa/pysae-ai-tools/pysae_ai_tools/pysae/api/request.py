"""``pysae-ai-tools pysae api request`` — call any Pysae API endpoint.

Endpoints are NOT hard-coded: discover the right path, method and parameters
with ``pysae api spec`` (which fetches the live OpenAPI document), then call
it here. Authentication is resolved automatically (Api-Key / env token /
stored OAuth token with silent refresh).

Examples:
    pysae-ai-tools pysae api request GET /api/v4/networks
    pysae-ai-tools pysae api request GET /api/v4/vehicles -q limit=10 -q offset=0
    pysae-ai-tools pysae api request POST /api/v4/foo --data '{"name": "x"}' --env dev
"""

import json
import sys
from typing import Annotated

import typer

from .common import client as api_client
from .common.config import get_env

app = typer.Typer()


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


def _split_pair(item: str, flag: str) -> tuple[str, str]:
    if "=" not in item:
        _err(f"FAILED: invalid {flag} '{item}', expected key=value")
        raise typer.Exit(1)
    key, value = item.split("=", 1)
    return key, value


@app.command()
def main(
    method: Annotated[str, typer.Argument(help="HTTP method (GET, POST, PUT, PATCH, DELETE).")],
    path: Annotated[str, typer.Argument(help="API path, e.g. /api/v4/networks (full URL also accepted).")],
    env: Annotated[str, typer.Option("--env", help="Target environment.")] = "dev",
    query: Annotated[
        list[str] | None,
        typer.Option("--query", "-q", help="Query param key=value (repeatable)."),
    ] = None,
    data: Annotated[
        str | None,
        typer.Option("--data", "-d", help="JSON request body (string), or @file to read from a file."),
    ] = None,
    header: Annotated[
        list[str] | None,
        typer.Option("--header", "-H", help="Extra header key=value (repeatable)."),
    ] = None,
    api_key: Annotated[
        str | None,
        typer.Option("--api-key", help="Use Authorization: Api-Key <key> instead of the stored OAuth token."),
    ] = None,
    client_id: Annotated[str | None, typer.Option("--client-id", help="Override the Auth0 client id.")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Print the raw response body instead of pretty JSON.")] = False,
    include_status: Annotated[
        bool,
        typer.Option("--status", help="Also print the HTTP status line to stderr."),
    ] = False,
) -> None:
    """Send an authenticated request to the Pysae API and print the response."""
    auth0 = get_env(env)

    params = [_split_pair(q, "--query") for q in (query or [])]
    extra_headers = dict(_split_pair(h, "--header") for h in (header or []))

    json_body: object | None = None
    if data is not None:
        body_text = data
        if data.startswith("@"):
            try:
                with open(data[1:], encoding="utf-8") as f:
                    body_text = f.read()
            except OSError as e:
                _err(f"FAILED: cannot read body file '{data[1:]}': {e}")
                raise typer.Exit(1) from None
        try:
            json_body = json.loads(body_text)
        except json.JSONDecodeError as e:
            _err(f"FAILED: --data is not valid JSON: {e}")
            raise typer.Exit(1) from None

    try:
        credential = api_client.resolve_credential(auth0, api_key=api_key, client_id=client_id)
    except api_client.NotAuthenticated as e:
        _err(f"FAILED: {e}")
        raise typer.Exit(1) from None

    try:
        resp = api_client.request(
            auth0,
            method,
            path,
            credential=credential,
            params=params,
            json_body=json_body,
            headers=extra_headers,
        )
    except Exception as e:  # network-level failure
        _err(f"FAILED: request error: {e}")
        raise typer.Exit(1) from None

    if include_status:
        _err(f"HTTP {resp.status_code} {resp.reason_phrase} [{method.upper()} {path}]")

    body = resp.text
    if not raw:
        try:
            body = json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            body = resp.text
    print(body)

    if resp.status_code >= 400:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

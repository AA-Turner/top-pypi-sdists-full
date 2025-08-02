# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode

import click
import humanfriendly
import pyperclip
import requests
from click import Context

from tinybird.datafile.common import get_name_version
from tinybird.tb.client import AuthNoTokenException, DoesNotExistException, TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_smart_table
from tinybird.tb.modules.exceptions import CLIPipeException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def endpoint(ctx):
    """Endpoint commands."""


@endpoint.command(name="ls")
@click.option("--match", default=None, help="Retrieve any resource matching the pattern. For example, --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
def endpoint_ls(ctx: Context, match: str, format_: str):
    """List endpoints"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    pipes = client.pipes(dependencies=False, node_attrs="name", attrs="name,updated_at,endpoint,url")
    endpoints = [p for p in pipes if p.get("endpoint")]
    endpoints = sorted(endpoints, key=lambda p: p["updated_at"])
    tokens = client.tokens()
    columns = ["name", "updated at", "nodes", "url"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in endpoints:
        tk = get_name_version(t["name"])
        if pattern and not pattern.search(tk["name"]):
            continue
        token = get_endpoint_token(tokens, tk["name"]) or client.token
        endpoint_url = build_endpoint_url(client, tk["name"], token, client.staging)
        table_human_readable.append((tk["name"], t["updated_at"][:-7], len(t["nodes"]), endpoint_url))
        table_machine_readable.append(
            {
                "name": tk["name"],
                "updated at": t["updated_at"][:-7],
                "nodes": len(t["nodes"]),
                "url": endpoint_url,
            }
        )

    if not format_:
        click.echo(FeedbackManager.info_pipes())
        echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)
        click.echo("\n")
    elif format_ == "json":
        click.echo(json.dumps({"pipes": table_machine_readable}, indent=2))
    else:
        raise CLIPipeException(FeedbackManager.error_pipe_ls_type())


@endpoint.command(name="token")
@click.argument("pipe_name")
@click.pass_context
def endpoint_token(ctx: click.Context, pipe_name: str):
    """Retrieve a token to read an endpoint"""
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        client.pipe_file(pipe_name)
    except DoesNotExistException:
        raise CLIPipeException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name))

    tokens = client.tokens()
    token = get_endpoint_token(tokens, pipe_name)
    if token:
        click.echo(token)
    else:
        click.echo(FeedbackManager.warning_token_pipe(pipe=pipe_name))


@endpoint.command(
    name="data",
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
    ),
)
@click.argument("pipe")
@click.option("--query", default=None, help="Run SQL over endpoint results")
@click.option(
    "--format", "format_", type=click.Choice(["json", "csv"], case_sensitive=False), help="Return format (CSV, JSON)"
)
@click.pass_context
def endpoint_data(ctx: Context, pipe: str, query: str, format_: str):
    """Print data returned by an endpoint

    Syntax: tb endpoint data <pipe_name> --param_name value --param2_name value2 ...
    """

    client: TinyB = ctx.ensure_object(dict)["client"]
    params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
    req_format = "json" if not format_ else format_.lower()
    try:
        res = client.pipe_data(pipe, format=req_format, sql=query, params=params)
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_exception(error=str(e)))

    if not format_:
        stats = res["statistics"]
        seconds = stats["elapsed"]
        rows_read = humanfriendly.format_number(stats["rows_read"])
        bytes_read = humanfriendly.format_size(stats["bytes_read"])

        click.echo(FeedbackManager.success_print_pipe(pipe=pipe))
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

        if not res["data"]:
            click.echo(FeedbackManager.info_no_rows())
        else:
            echo_safe_humanfriendly_tables_format_smart_table(
                data=[d.values() for d in res["data"]], column_names=res["data"][0].keys()
            )
        click.echo("\n")
    elif req_format == "json":
        click.echo(json.dumps(res))
    else:
        click.echo(res)


@endpoint.command(name="url")
@click.argument("pipe")
@click.option(
    "--language",
    default="http",
    help="Language used for sending the request. Options: http, python, curl, javascript, rust, go",
)
@click.pass_context
def endpoint_url(ctx: Context, pipe: str, language: str):
    """Print the URL of an endpoint"""
    if language != "http":
        click.echo(FeedbackManager.highlight(message=f"\n» Generating snippet for {language} language"))
    client: TinyB = ctx.ensure_object(dict)["client"]
    tokens = client.tokens()
    token = get_endpoint_token(tokens, pipe) or client.token
    click.echo(build_endpoint_snippet(client, pipe, token, language, client.staging))
    if language != "http":
        click.echo(FeedbackManager.success(message="\n✓ Code snippet copied to clipboard!\n"))


def get_endpoint_token(tokens: List[Dict[str, Any]], pipe_name: str) -> Optional[str]:
    token = None
    for t in tokens:
        for scope in t["scopes"]:
            if scope["type"] == "PIPES:READ" and scope["resource"] == pipe_name:
                token = t["token"]
                break

    return token


@endpoint.command(name="stats")
@click.argument("pipes", nargs=-1)
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output. To parse the output, keep in mind to use `tb --no-version-warning endpoint stats` option.",
)
@click.pass_context
def endpoint_stats(ctx: click.Context, pipes: Tuple[str, ...], format_: str):
    """
    Print endpoint stats for the last 7 days
    """
    client: TinyB = ctx.ensure_object(dict)["client"]
    all_pipes = client.pipes()
    pipes_to_get_stats = []
    pipes_ids: Dict = {}

    if pipes:
        # We filter by the pipes we want to look for
        all_pipes = [pipe for pipe in all_pipes if pipe["name"] in pipes]

    for pipe in all_pipes:
        name_version = get_name_version(pipe["name"])
        if name_version["name"] in pipe["name"]:
            pipes_to_get_stats.append(f"'{pipe['id']}'")
            pipes_ids[pipe["id"]] = name_version

    if not pipes_to_get_stats:
        if format_ == "json":
            click.echo(json.dumps({"pipes": []}, indent=2))
        else:
            click.echo(FeedbackManager.info_no_pipes_stats())
        return

    sql = f"""
        SELECT
            pipe_id id,
            sumIf(view_count, date > now() - interval 7 day) requests,
            sumIf(error_count, date > now() - interval 7 day) errors,
            avgMergeIf(avg_duration_state, date > now() - interval 7 day) latency
        FROM tinybird.pipe_stats
        WHERE pipe_id in ({",".join(pipes_to_get_stats)})
        GROUP BY pipe_id
        ORDER BY requests DESC
        FORMAT JSON
    """

    res = client.query(sql)

    if res and "error" in res:
        raise CLIPipeException(FeedbackManager.error_exception(error=str(res["error"])))

    columns = ["name", "request count", "error count", "avg latency"]
    table_human_readable: List[Tuple] = []
    table_machine_readable: List[Dict] = []
    if res and "data" in res:
        for x in res["data"]:
            tk = pipes_ids[x["id"]]
            table_human_readable.append(
                (
                    tk["name"],
                    x["requests"],
                    x["errors"],
                    x["latency"],
                )
            )
            table_machine_readable.append(
                {
                    "name": tk["name"],
                    "requests": x["requests"],
                    "errors": x["errors"],
                    "latency": x["latency"],
                }
            )

        table_human_readable.sort(key=lambda x: (x[1], x[0]))
        table_machine_readable.sort(key=lambda x: x["name"])

        if format_ == "json":
            click.echo(json.dumps({"pipes": table_machine_readable}, indent=2))
        else:
            echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)


def build_endpoint_snippet(
    tb_client: TinyB, pipe_name: str, token: str, language: str, staging: bool = False
) -> Optional[str]:
    endpoint_url = build_endpoint_url(tb_client, pipe_name, token, staging)
    if language == "http":
        return endpoint_url

    snippet = None
    if language == "python":
        snippet = build_python_snippet(endpoint_url, token)
    elif language == "curl":
        snippet = build_curl_snippet(endpoint_url)
    elif language == "javascript":
        snippet = build_javascript_snippet(endpoint_url, token)
    elif language == "rust":
        snippet = build_rust_snippet(endpoint_url)
    elif language == "go":
        snippet = build_go_snippet(endpoint_url)

    if not snippet:
        raise CLIPipeException(FeedbackManager.error(message=f"Language {language} not supported"))

    pyperclip.copy(snippet.strip())
    return snippet


def build_endpoint_url(tb_client: TinyB, pipe_name: str, token: str, staging: bool = False) -> str:
    example_params = {
        "format": "json",
        "pipe": pipe_name,
        "q": "",
        "token": token,
    }
    if staging:
        example_params["__tb__deployment"] = "staging"
    response = requests.get(f"{tb_client.host}/examples/query.http?{urlencode(example_params)}")
    return response.text.replace("http://localhost:8001", tb_client.host)


def build_python_snippet(endpoint_url: str, token: str) -> str:
    endpoint_url = endpoint_url.replace(f"token={token}", "token={{token}}")
    return f"""
import requests

token = "{token}"
url = "{endpoint_url}"
response = requests.get(url)
print(response.json())
    """


def build_curl_snippet(endpoint_url: str) -> str:
    return f"""
curl -X GET "{endpoint_url}"
    """


def build_javascript_snippet(endpoint_url: str, token: str) -> str:
    endpoint_url = endpoint_url.replace(f"token={token}", "token=${token}")
    return f"""
const token = "{token}";
fetch(`{endpoint_url}`)
.then(response => response.json())
.then(data => console.log(data));
    """


def build_rust_snippet(endpoint_url: str) -> str:
    return f"""
use reqwest::Client;

let client = Client::new();
let response = client.get("{endpoint_url}").send().await?;
    """


def build_go_snippet(endpoint_url: str) -> str:
    return f"""
package main

import (
    "fmt"
    "io"
    "log"
    "net/http"
)

func main() {{
    url := "{endpoint_url}"
    resp, err := http.Get(url)
    if err != nil {{
        log.Fatal(err)
    }}
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {{
        log.Fatal(err)
    }}

    fmt.Println(string(body))
}}
    """

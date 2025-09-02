import datetime
import functools
import inspect
import json
import logging
import os
import re
import socket
import ssl
import tempfile
import textwrap
import typing
import urllib.parse
import warnings
import zoneinfo
from typing import Callable, Iterable

import fastmcp.tools
import httpx
import langchain.tools
import langchain_core.utils.function_calling
import mcp
import pydantic
import sqlalchemy as sa
import urllib3


def truncate_text(text: str, max_length: int, placeholder: str = "[...]") -> str:
    text = text[:max_length] + placeholder if len(text) > max_length else text
    return text


def json_dumps_for_ai(
    value: str | list | dict | pydantic.BaseModel,
    max_length: int | None = None,
    truncation_placeholder: str = "\n[CONTENT END] The rest of the content was truncated to fit into LLM context window.",
    **kwargs,
) -> str:
    if isinstance(value, str):
        return value

    if isinstance(value, pydantic.BaseModel):
        value = value.model_dump()

    value = json.dumps(value, ensure_ascii=False, **kwargs)
    if max_length:
        value = truncate_text(value, max_length, placeholder=truncation_placeholder)

    return value


def format_datetime_for_ai(
    date: datetime.datetime | str,
    timespec: str = "seconds",
    timezone: zoneinfo.ZoneInfo = zoneinfo.ZoneInfo("UTC"),
) -> str:
    date = datetime.datetime.fromisoformat(date) if isinstance(date, str) else date
    date = date.astimezone(timezone)
    date = date.isoformat(timespec=timespec, sep=" ")
    return date


def to_formatted_markdown(text: str, kind: str = "json") -> str:
    text = f"```{kind}\n{text}\n```"
    return text


def format_json_for_ai(
    value: str | list | dict | pydantic.BaseModel, indent: int | None = 0
) -> str:
    text = json_dumps_for_ai(value, indent=indent)
    text = to_formatted_markdown(text)
    return text


def filter_dict_by_keys(dictionary: dict, keys: Iterable) -> dict:
    dictionary = {key: dictionary[key] for key in keys if key in dictionary}
    return dictionary


def recursively_collect_file_paths_in_directory(directory_path: str) -> list[str]:
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path):
                file_paths.append(full_path)

    return file_paths


def get_return_type_annotation(function):
    return function.__annotations__.get("return")


def isinstance_typing_annotation(annotation, type) -> bool:
    return annotation is type or typing.get_origin(annotation) is type


def to_fastmcp_tool(
    function,
    tags: set[str] | None,
    annotations: mcp.types.ToolAnnotations | None,
    max_output_length: int | None = None,
) -> fastmcp.tools.FunctionTool:
    """Adds a custom serializer to ensure consistent and token-efficient conversion of tool output to text."""
    return_type = get_return_type_annotation(function)
    if isinstance_typing_annotation(return_type, list):
        warnings.warn(
            "When tool returns a list, each of its elements will be serialized separately "
            "using fastmcp.tools.tool._convert_to_content into MCPContent."
        )

    tool = fastmcp.tools.FunctionTool.from_function(
        function,
        tags=tags,
        annotations=annotations,
        serializer=functools.partial(json_dumps_for_ai, max_length=max_output_length),
    )
    # Normalize tool parameters schema to match OpenAI's.
    # For example, it dereferences JSON schema $refs, which are not supported by many AI API providers.
    openai_tool_schema = langchain_core.utils.function_calling.convert_to_openai_tool(function)
    tool.parameters = openai_tool_schema["function"]["parameters"]
    return tool


def request_as_dict(*args, **kwargs) -> dict:
    response = httpx.get(*args, **kwargs)
    response.raise_for_status()
    response_dict = response.json()
    return response_dict


def to_datetime(
    date: datetime.date | datetime.timedelta | str | int | float | None = None,
) -> datetime.datetime:
    match date:
        case datetime.datetime():
            pass
        case datetime.date():
            date = datetime.datetime.combine(date, datetime.time())
        case None:
            date = datetime.datetime.now()
        case datetime.timedelta():
            date += datetime.datetime.now()
        case str():
            date = datetime.datetime.fromisoformat(date)
        case int() | float():
            date = datetime.datetime.fromtimestamp(date)
        case _:
            raise ValueError(f"Unexpected date type: {type(date)}")

    date = date if date.tzinfo else date.astimezone()
    # or date = date.astimezone(datetime.timezone.utc)
    return date


def join_url_components(*url_components: str) -> str:
    url = "/".join(str(i).strip("/") for i in url_components)
    return url


def try_format_json_with_indent(text: str, indent: int = 2) -> str:
    try:
        text = json.dumps(json.loads(text), indent=indent)
    except json.JSONDecodeError:
        pass

    return text


def raise_for_status(response: httpx.Response, max_text_length: int = 1000) -> None:
    if not response.is_error:
        return

    response_text = try_format_json_with_indent(response.text)
    request_text = try_format_json_with_indent(response.request.content.decode())
    if max_text_length:
        request_text = truncate_text(request_text, max_text_length)
        response_text = truncate_text(response_text, max_text_length)

    error_message = (
        f"Error in HTTP response while requesting {response.url}\n"
        f"Status code: {response.status_code}\n"
        f"Reason: {response.reason_phrase}\n"
        f"Request body: {request_text}\n"
        f"Response body: {response_text}\n"
    )
    error = httpx.HTTPStatusError(error_message, request=response.request, response=response)
    raise error


async def araise_for_status(response: httpx.Response, max_response_text_length: int = 1000) -> None:
    if not response.is_error:
        return

    await response.aread()
    raise_for_status(response, max_text_length=max_response_text_length)


def try_match_regex(pattern: str, string: str, **kwargs):
    match = re.match(pattern, string, **kwargs)
    if not match:
        raise ValueError(f"String '{string}' does not fit expected pattern '{pattern}'")

    return match


def value_to_key(items: list, key: str) -> dict:
    dictionary = {i.pop(key): i for i in items}
    return dictionary


def to_maybe_ssl_context(ssl_verify: bool | str) -> bool | ssl.SSLContext:
    if isinstance(ssl_verify, str):
        ssl_verify = ssl.create_default_context(cafile=ssl_verify)

    return ssl_verify


def add_mcp_server_components(
    server: fastmcp.FastMCP | None = None,
    tools: Iterable[fastmcp.tools.FunctionTool] = (),
    resources: Iterable[fastmcp.resources.Resource] = (),
    prompts: Iterable[fastmcp.prompts.Prompt] = (),
) -> fastmcp.FastMCP:
    server = server or fastmcp.FastMCP()
    for tool in tools:
        server.add_tool(tool)

    for resource in resources:
        server.add_resource(resource)

    for prompt in prompts:
        server.add_prompt(prompt)

    return server


def wrap_with_xml_tag(tag: str, value: str, with_new_lines: bool = False) -> str:
    value = f"\n{value}\n" if with_new_lines else value
    wrapped_value = f"<{tag}>{value}</{tag}>"
    wrapped_value += "\n" if with_new_lines else ""
    return wrapped_value


def assign_default_tool_annotation_hints(
    annotation: mcp.types.ToolAnnotations | None = None,
) -> mcp.types.ToolAnnotations:
    annotation = annotation or mcp.types.ToolAnnotations()
    if annotation.readOnlyHint and annotation.destructiveHint:
        raise ValueError("Tool cannot be both readonly and destructive.")

    if annotation.readOnlyHint and annotation.idempotentHint is False:
        raise ValueError("Tool cannot be both readonly and non-idempotent.")

    default = mcp.types.ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    )
    for hint, value in default.model_dump().items():
        if getattr(annotation, hint) is None:
            setattr(annotation, hint, value)

    return annotation


def disable_urllib_insecure_request_warning():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def set_ssl_cert_file_from_cadata(cadata: str, set_ssl_cert_file_env_var: bool = True) -> str:
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".pem") as temp_ca_file:
        temp_ca_file.write(cadata)
        ca_file_path = temp_ca_file.name

    if set_ssl_cert_file_env_var:
        os.environ["SSL_CERT_FILE"] = ca_file_path
        os.environ["REQUESTS_CA_BUNDLE"] = ca_file_path

    return ca_file_path


def split_schema_table(schema_table: str) -> tuple[str | None, str]:
    schema, table = schema_table.split(".") if "." in schema_table else (None, schema_table)
    return schema, table


def get_all_schema_tables(engine: sa.Engine, verify_select_permissions: bool = False) -> list[str]:
    inspector = sa.inspect(engine)
    schemas = inspector.get_schema_names()
    schema_tables = []
    with engine.connect() as connection:
        for schema in schemas:
            try:
                tables = inspector.get_table_names(schema)
            except sa.exc.DatabaseError as e:
                logging.warning(f"Failed to get table names for schema {schema}:\n{e}")
                continue

            if not verify_select_permissions:
                schema_tables.extend([f"{schema}.{table}" for table in tables])
                continue

            for table in tables:
                # Use text to avoid expensive reflection for each table.
                probe_sql = sa.text(f'SELECT 1 FROM "{schema}"."{table}" LIMIT 0')
                try:
                    connection.execute(probe_sql)
                except sa.exc.DatabaseError:
                    # Need to rollback failed connection state to continue executing commands.
                    connection.rollback()
                else:
                    schema_tables.append(f"{schema}.{table}")

    return schema_tables


class StringFilter(pydantic.BaseModel):
    allowed_values: set[str] = set()
    forbidden_values: set[str] = set()
    allowed_pattern: re.Pattern[str] | None = None
    forbidden_pattern: re.Pattern[str] | None = None

    @classmethod
    def from_lists_and_strings(
        cls,
        allowed_values: list[str] | None = None,
        forbidden_values: list[str] | None = None,
        allowed_pattern: str | None = None,
        forbidden_pattern: str | None = None,
    ):
        string_filter = cls(
            allowed_values=set(allowed_values or []),
            forbidden_values=set(forbidden_values or []),
            allowed_pattern=re.compile(allowed_pattern) if allowed_pattern else None,
            forbidden_pattern=re.compile(forbidden_pattern) if forbidden_pattern else None,
        )
        return string_filter

    def is_explicitly_allowed(self, value: str) -> bool:
        return (
            value in self.allowed_values
            or self.allowed_pattern
            and self.allowed_pattern.fullmatch(value)
        )

    def is_explicitly_forbidden(self, value: str) -> bool:
        return (
            value in self.forbidden_values
            or self.forbidden_pattern
            and self.forbidden_pattern.fullmatch(value)
        )

    def should_keep(self, value: str) -> bool:
        return self.is_explicitly_allowed(value) and not self.is_explicitly_forbidden(value)


def find_available_port(host: str = "127.0.0.1") -> int:
    """Return an OS-allocated *free* TCP port number for *host*.

    This helper opens a temporary socket bound to *(host, 0)*: passing
    ``0`` tells the kernel to choose any port that is currently unused.
    After binding we read the port number via ``sock.getsockname()`` and
    immediately close the socket by leaving the *with* block.  The port is
    therefore released back to the OS, ready for the caller to reuse.

    Parameters
    ----------
    host : str, default "127.0.0.1"
        Interface to bind to.  Normally ``"127.0.0.1"`` (IPv4 loopback) or
        ``"::1"`` (IPv6 loopback).  Using an explicit host avoids the risk of
        exposing the service on a public interface.

    Returns
    -------
    int
        A currently free TCP port number.

    Notes
    -----
    ``socket.AF_INET`` specifies the IPv4 address family, while
    ``socket.SOCK_STREAM`` selects the TCP protocol.  Together they create a
    TCP/IPv4 socket.

    This pattern is perfectly adequate for local development, but in highly
    concurrent environments there is still a small race window between
    releasing the port and rebinding to it.  If you need stronger guarantees
    consider opening the socket once and *passing the open file descriptor*
    (e.g., via ``sock.fileno()``) to the server process instead of closing it
    here.
    """
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        port = sock.getsockname()[1]

    return port


async def llm_friendly_http_request(
    client: httpx.AsyncClient,
    url: str,
    http_method: str = "GET",
    json_query_params: str | None = None,
    content: str | dict | None = None,
    ensure_dict_output: bool = False,
):
    json_query_params = json.loads(json_query_params) if json_query_params else None
    kwargs = dict(
        method=http_method,
        url=url,
        params=json_query_params,
    )
    match content:
        case str():
            try:
                kwargs["json"] = json.loads(content)
            except json.JSONDecodeError:
                kwargs["content"] = content
        case dict():
            kwargs["json"] = content

    response = await client.request(**kwargs)
    data = response.json()
    data = {"response": data} if ensure_dict_output and not isinstance(data, dict) else data
    return data


def prepend_url_path_prefix_if_not_present(prefix: str, path: str) -> str:
    path = path.strip("/")
    prefix = prefix.strip("/")
    path = path if path.startswith(prefix) else f"{prefix}/{path}"
    return path


def wrap_tool_with_str_serializer(
    tool: callable, max_output_length: int | None = None, **kwargs
) -> callable:
    def serialize_output(output) -> str:
        return json_dumps_for_ai(output, max_length=max_output_length, **kwargs)

    @functools.wraps(tool)
    async def awrapped(*args, **tool_kwargs):
        output = await tool(*args, **tool_kwargs)
        output = serialize_output(output)
        return output

    @functools.wraps(tool)
    def wrapped(*args, **tool_kwargs):
        output = tool(*args, **tool_kwargs)
        output = serialize_output(output)
        return output

    wrapped_tool = awrapped if inspect.iscoroutinefunction(tool) else wrapped
    wrapped_tool.__annotations__["return"] = str
    return wrapped_tool


def get_line_separated_text_overview(
    text: str,
    line_chunks_len: int = 5,
    separator: str = "[LINES TRUNCATED FOR BREVITY]",
) -> str:
    """Return head, tail and middle of the text"""
    text = textwrap.dedent(text)
    lines = [line.rstrip() for line in text.splitlines() if line.rstrip()]
    if len(lines) < (line_chunks_len * 3) + 10:
        text = "\n".join(lines)
        return text

    head = lines[:line_chunks_len]
    mid = lines[(len(lines) - line_chunks_len) // 2 : (len(lines) + line_chunks_len) // 2]
    tail = lines[-line_chunks_len:]

    overview = "\n".join(head + [separator] + mid + [separator] + tail)
    return overview


def to_langchain_tool(
    tool: Callable | fastmcp.tools.FunctionTool,
    prefix: str | None = None,
    max_output_length: int | None = None,
) -> langchain.tools.BaseTool:
    match tool:
        case fastmcp.tools.FunctionTool(fn=fn, annotations=annotations, tags=tags):
            tool = fn
            metadata = annotations.model_dump(exclude_none=True) if annotations else None
            tags = sorted(tags) if tags else None
        case _:
            metadata = None
            tags = None

    if isinstance_typing_annotation(get_return_type_annotation(tool), dict):
        # Serialize dict outputs to JSON.
        tool = wrap_tool_with_str_serializer(tool, max_output_length=max_output_length)

    tool = langchain.tools.tool(tool)
    tool.name = f"{prefix}_{tool.name}" if prefix else tool.name
    tool.tags = tags
    tool.metadata = metadata
    return tool


def build_url(*url_components: str, **kwargs: str) -> str:
    url = join_url_components(*url_components)
    url = f"{url}?{urllib.parse.urlencode(kwargs)}" if kwargs else url
    return url

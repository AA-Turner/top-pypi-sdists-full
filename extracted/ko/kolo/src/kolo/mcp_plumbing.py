"""
MCP server implementation that is compatible with Python 3.8+.
This module contains the core infrastructure for the Model Context Protocol server.
"""

import asyncio
import inspect
import json
import logging
import sys
import traceback
import types
from dataclasses import asdict, dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from .version import __version__

# PEP 604 unions (`str | None`) have origin `types.UnionType` instead of
# `typing.Union`. The attribute does not exist on Python 3.8/3.9, so fall
# back to a sentinel that no `get_origin` result will ever equal.
_UNION_ORIGINS = (Union, getattr(types, "UnionType", type(None)))

logger = logging.getLogger("kolo.mcp")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

PROTOCOL_VERSION = "2024-11-05"

T = TypeVar("T")
ToolFunc = Callable[..., Any]


@dataclass
class Tool:
    """Representation of a tool in the MCP protocol."""

    name: str
    func: ToolFunc
    description: str
    input_schema: Dict[str, Any]


@dataclass
class MCPServerInfo:
    """Server information for MCP protocol."""

    name: str
    version: str = ""

    def __post_init__(self):
        if not self.version:
            self.version = __version__


@dataclass
class MCPCapabilities:
    """Capabilities supported by the MCP server."""

    experimental: Dict[str, Any] = field(default_factory=dict)
    prompts: Dict[str, bool] = field(default_factory=lambda: {"listChanged": False})
    resources: Dict[str, bool] = field(
        default_factory=lambda: {"subscribe": False, "listChanged": False}
    )
    tools: Dict[str, bool] = field(default_factory=lambda: {"listChanged": False})
    roots: Dict[str, bool] = field(default_factory=lambda: {"listChanged": False})
    sampling: Dict[str, Any] = field(default_factory=dict)


def _schema_for_type(param_type: Any) -> Dict[str, Any]:
    """Map a Python type annotation to a JSON Schema fragment."""
    if param_type is inspect.Parameter.empty:
        return {"type": "string"}
    if isinstance(param_type, type):
        if issubclass(param_type, str):
            return {"type": "string"}
        # bool must be checked before int: issubclass(bool, int) is True,
        # so the int branch would otherwise swallow booleans.
        if issubclass(param_type, bool):
            return {"type": "boolean"}
        if issubclass(param_type, int):
            return {"type": "integer"}
        if issubclass(param_type, float):
            return {"type": "number"}
        return {}
    if get_origin(param_type) is list:
        return {"type": "array", "items": {"type": "string"}}
    return {"type": "object"}


class MCPServer:
    """A minimal implementation of the Model Context Protocol server compatible with Python 3.8+."""

    def __init__(self, name: str):
        self.server_info = MCPServerInfo(name=name)
        self.capabilities = MCPCapabilities()
        self.tools: Dict[str, Tool] = {}
        logger.info(f"Initialized MCP server with name: {name}")

    def tool(self) -> Callable[[ToolFunc], ToolFunc]:
        """Decorator to register a function as an MCP tool."""

        def decorator(func: ToolFunc) -> ToolFunc:
            tool_name = func.__name__
            type_hints = get_type_hints(func)
            description = func.__doc__ or ""

            sig = inspect.signature(func)
            properties = {}
            required = []

            for name, param in sig.parameters.items():
                if name == "self" or name == "cls":
                    continue

                param_type = type_hints.get(name, Any)

                # Unwrap Optional[T] first: typing aliases aren't `type` instances and would fall
                # through to the {"type": "object"} default, rejecting valid inputs.
                is_optional = False
                if get_origin(param_type) in _UNION_ORIGINS:
                    args = [a for a in get_args(param_type) if a is not type(None)]
                    if len(args) < len(get_args(param_type)):
                        is_optional = True
                    if len(args) == 1:
                        param_type = args[0]

                prop = _schema_for_type(param_type)
                if is_optional:
                    prop = {"anyOf": [prop, {"type": "null"}]}

                if param.default is inspect.Parameter.empty:
                    required.append(name)
                else:
                    if param.default is not None:
                        if isinstance(param.default, bool):
                            prop["default"] = param.default
                            if not is_optional:
                                prop["type"] = "boolean"
                        else:
                            prop["default"] = param.default

                properties[name] = prop

            input_schema = {
                "type": "object",
                "title": f"{tool_name}Arguments",
                "properties": properties,
            }

            if required:
                input_schema["required"] = required

            self.tools[tool_name] = Tool(
                name=tool_name,
                func=func,
                description=description,
                input_schema=input_schema,
            )

            logger.info(f"Registered tool: {tool_name}")
            return func

        return decorator

    async def handle_request(self, request_data: str) -> str:
        """Handle an incoming JSON-RPC request."""
        try:
            logger.debug(f"Handling request: {request_data.strip()}")

            try:
                request = json.loads(request_data)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return self._error_response(None, -32700, f"Parse error: {str(e)}")

            jsonrpc = request.get("jsonrpc")
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            logger.info(f"Processing method: {method} with id: {request_id}")

            if jsonrpc != "2.0":
                logger.warning(f"Invalid JSON-RPC version: {jsonrpc}")
                return self._error_response(
                    request_id, -32600, "Invalid Request: expected jsonrpc 2.0"
                )

            if method == "initialize":
                response = self._initialize_response(request_id)
                logger.debug(f"Initialize response JSON: {response}")
                return response
            elif method == "tools/list":
                response = self._tools_list_response(request_id)
                logger.debug(f"Tools list response JSON: {response}")
                return response
            elif method == "roots/list":
                response = self._roots_list_response(request_id)
                logger.debug(f"Roots list response JSON: {response}")
                return response
            elif method == "tools/call":
                logger.info("Processing tools/call method")
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})

                if not tool_name:
                    logger.warning("Tool name not provided in tools/call")
                    return self._error_response(
                        request_id, -32602, "Invalid params: tool name not provided"
                    )

                if tool_name not in self.tools:
                    logger.warning(f"Tool not found: {tool_name}")
                    return self._error_response(
                        request_id, -32601, f"Tool '{tool_name}' not found"
                    )

                logger.info(f"Executing tool via tools/call: {tool_name}")
                response = await self._execute_tool(request_id, tool_name, tool_params)
                logger.debug(f"Tool execution response JSON: {response}")
                return response
            elif method.startswith("notifications/"):
                notification_type = method.split("/")[1]
                logger.info(f"Received notification: {notification_type}")

                return json.dumps({"jsonrpc": "2.0", "id": request_id, "result": {}})
            elif method.startswith("tools/execute/"):
                tool_name = method.split("/")[-1]
                if tool_name not in self.tools:
                    logger.warning(f"Tool not found: {tool_name}")
                    return self._error_response(
                        request_id, -32601, f"Tool '{tool_name}' not found"
                    )

                logger.info(f"Executing tool: {tool_name}")
                response = await self._execute_tool(request_id, tool_name, params)
                logger.debug(f"Tool execution response JSON: {response}")
                return response
            else:
                logger.warning(f"Method not found: {method}")
                return self._error_response(
                    request_id, -32601, f"Method '{method}' not found"
                )

        except json.JSONDecodeError:
            logger.error("JSON parse error")
            return self._error_response(None, -32700, "Parse error")
        except Exception as e:
            logger.error(f"Internal error: {str(e)}")
            logger.error(traceback.format_exc())
            return self._error_response(None, -32603, f"Internal error: {str(e)}")

    def _initialize_response(self, request_id: Any) -> str:
        """Generate the initialize response with server info and capabilities."""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": asdict(self.capabilities),
                "serverInfo": asdict(self.server_info),
            },
        }
        logger.debug(f"Initialize response: {response}")
        logger.debug(f"Server info: {asdict(self.server_info)}")
        logger.debug(f"Capabilities: {asdict(self.capabilities)}")
        return json.dumps(response)

    def _tools_list_response(self, request_id: Any) -> str:
        """Generate the tools/list response."""
        tools_list = []

        for name, tool in self.tools.items():
            tools_list.append(
                {
                    "name": name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema,
                }
            )

        response = {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools_list}}
        logger.debug(f"Tools list response contains {len(tools_list)} tools")
        return json.dumps(response)

    def _roots_list_response(self, request_id: Any) -> str:
        """Generate the roots/list response."""
        roots_list = [
            {
                "id": "kolo",
                "name": "Kolo MCP Tools",
                "description": "Tools for deep Python tracing and debugging",
            }
        ]

        response = {"jsonrpc": "2.0", "id": request_id, "result": {"roots": roots_list}}
        logger.debug(f"Roots list response contains {len(roots_list)} roots")
        return json.dumps(response)

    async def _execute_tool(
        self, request_id: Any, tool_name: str, params: Dict[str, Any]
    ) -> str:
        """Execute a tool and return the response."""
        tool = self.tools.get(tool_name)
        if not tool:
            logger.warning(f"Tool not found for execution: {tool_name}")
            return self._error_response(
                request_id, -32601, f"Tool '{tool_name}' not found"
            )

        try:
            logger.info(f"Calling tool function: {tool_name}")
            logger.debug(f"Tool params: {params}")
            result = tool.func(**params)

            if inspect.iscoroutine(result):
                logger.debug(f"Awaiting coroutine result for tool: {tool_name}")
                result = await result

            logger.info(f"Tool {tool_name} result: {result}")

            if isinstance(result, List):
                content_items = []
                for item in result:
                    content_items.append({"type": "text", "text": str(item)})

                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": content_items},
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    str(result)
                                    if isinstance(result, (str, int, float, bool))
                                    else json.dumps(result)
                                ),
                            }
                        ]
                    },
                }

            logger.info(f"Tool {tool_name} executed successfully")
            return json.dumps(response)

        except Exception as e:
            error_msg = f"Error executing tool {tool_name}: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            return self._error_response(request_id, -32603, error_msg)

    def _error_response(self, request_id: Any, code: int, message: str) -> str:
        """Generate an error response."""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }
        logger.debug(f"Error response: {response}")
        return json.dumps(response)

    async def read_stdin_line(self) -> str:
        """Read a line from stdin in an asynchronous way."""
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        logger.debug(f"Read line from stdin: {line.strip()}")
        return line

    async def run_stdio(self):
        """Run the server reading from stdin and writing to stdout."""
        logger.info("Starting MCP server on stdio transport")
        try:
            while True:
                line = await self.read_stdin_line()
                if not line:
                    logger.info("Received empty line, exiting")
                    break

                if line.strip():
                    try:
                        if line.startswith("{"):
                            request_data = line
                        else:
                            if line.startswith("Content-Length:"):
                                content_length = int(line.strip().split(": ")[1])
                                await self.read_stdin_line()
                                request_data = (
                                    await asyncio.get_event_loop().run_in_executor(
                                        None,
                                        lambda: sys.stdin.buffer.read(
                                            content_length
                                        ).decode("utf-8"),
                                    )
                                )
                            else:
                                logger.warning(f"Invalid header: {line.strip()}")
                                continue

                        response = await self.handle_request(request_data)

                        logger.debug(f"Response: {response}")

                        sys.stdout.write(response)
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                    except Exception as e:
                        logger.error(f"Error handling request: {e}")
                        logger.error(traceback.format_exc())

                        error_response = json.dumps(
                            {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32603,
                                    "message": f"Internal error: {str(e)}",
                                },
                                "id": None,
                            }
                        )
                        sys.stdout.write(error_response)
                        sys.stdout.write("\n")
                        sys.stdout.flush()
        except Exception as e:
            logger.error(f"Fatal error in MCP server loop: {e}")
            logger.error(traceback.format_exc())

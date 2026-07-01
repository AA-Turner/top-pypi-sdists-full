"""Generate local MCP server repos from packaged templates."""

from __future__ import annotations

import json
import keyword
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import indent
from typing import Any, Dict, List, Optional

from jinja2 import Environment, PackageLoader


TOKEN_DEFAULTS = {
    "USDC": {
        "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "decimals": 6,
    },
    "USDT": {
        "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "decimals": 6,
    },
}


@dataclass
class LocalMCPEndpoint:
    endpoint_path: str
    endpoint_name: str
    method: str
    description: Optional[str] = None
    # Populated when loading from an endpoints.json file.
    input_schema: Optional[Dict[str, Any]] = None
    # Per-endpoint price override; falls back to LocalMCPServerConfig.price_usd.
    price_usd: Optional[float] = None


@dataclass
class LocalMCPServerConfig:
    api_name: str
    api_url: str
    price_usd: float
    requires_auth: bool
    api_key_env: Optional[str]
    api_key_header: str
    output_dir: Path
    docs_url: Optional[str]
    sdk_package: Optional[str]
    server_address: str
    operator_address: str
    operator_private_key: str
    description: str = ""
    network: str = "arbitrum_one"
    token_symbol: str = "USDC"
    facilitator_url: str = "https://facilitator.d402.net"
    testing_mode: bool = True
    port: int = 8000
    endpoints: list[LocalMCPEndpoint] = field(default_factory=list)
    boilerplate_only: bool = False


class MCPServerTemplateGenerator:
    """Render the MCP template set into a local repo."""

    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("traia_iatp.mcp", "templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    @staticmethod
    def slugify(text: str) -> str:
        value = text.lower()
        value = re.sub(r"[\s_]+", "-", value)
        value = re.sub(r"[^a-z0-9-]", "", value)
        value = re.sub(r"-+", "-", value)
        return value.strip("-")

    def create_local_repo(self, config: LocalMCPServerConfig) -> Path:
        repo_dir = config.output_dir / f"{self._base_slug(config.api_name)}-mcp-server"
        repo_dir.mkdir(parents=True, exist_ok=True)

        context = self._build_context(config)
        self._render_repo_files(repo_dir, context)
        self._inject_tools(repo_dir / "server.py", config)
        self._update_deployment_params(repo_dir / "deployment_params.json", config)
        self._update_health_check(repo_dir / "mcp_health_check.py", config)
        self._update_generated_readme(repo_dir / "README.md", config)
        self._write_env_files(repo_dir, config)
        self._configure_local_iatp_dependency(repo_dir / "pyproject.toml")
        return repo_dir

    def _build_context(self, config: LocalMCPServerConfig) -> dict:
        api_slug = self._base_slug(config.api_name)
        api_key_env = config.api_key_env or f"{api_slug.upper().replace('-', '_')}_API_KEY"

        return {
            "api_name": config.api_name,
            "api_slug": api_slug,
            "server_title": self._server_title(config.api_name),
            "api_url": config.api_url.rstrip("/"),
            "docs_url": (config.docs_url or config.api_url).rstrip("/"),
            "api_description": config.description,
            "logger_name": f"{api_slug}_mcp",
            "api_name_lower": config.api_name.lower(),
            "requires_auth": config.requires_auth,
            "sdk_package": config.sdk_package,
            "sdk_module": None,
            "endpoints": [],
            "has_endpoints": True,
            "api_key_env_var": api_key_env if config.requires_auth else None,
            "api_key_value": "YOUR_API_KEY_HERE" if config.requires_auth else None,
            "auth_description": " with Authentication" if config.requires_auth else "",
            "auth_details": " with authentication via API keys" if config.requires_auth else "",
            "auth_startup_msg": " with authentication" if config.requires_auth else "",
            "environment_variables": [],
        }

    def _render_repo_files(self, repo_dir: Path, context: dict) -> None:
        template_map = {
            "local_server.py.j2": "server.py",
            "local_Dockerfile.j2": "Dockerfile",
            "local_docker-compose.yml.j2": "docker-compose.yml",
            "pyproject.toml.j2": "pyproject.toml",
            "local_run_local_docker.sh.j2": "run_local_docker.sh",
            "mcp_health_check.py.j2": "mcp_health_check.py",
            "gitignore.j2": ".gitignore",
            "dockerignore.j2": ".dockerignore",
            "local_README.md.j2": "README.md",
            "deployment_params.json.j2": "deployment_params.json",
            "local_env.example.j2": ".env.example",
            "pyrightconfig.json.j2": "pyrightconfig.json",
        }

        cursor_dir = repo_dir / ".cursor"
        cursor_dir.mkdir(exist_ok=True)
        cursor_rules = self.env.get_template("cursor-rules.md.j2").render(**context)
        (cursor_dir / f"{context['api_slug']}-mcp-server-setup-rules.md").write_text(cursor_rules)

        for template_name, output_name in template_map.items():
            content = self.env.get_template(template_name).render(**context)
            output_path = repo_dir / output_name
            output_path.write_text(content)
            if output_name.endswith(".sh"):
                output_path.chmod(0o755)

    def _inject_tools(self, server_py_path: Path, config: LocalMCPServerConfig) -> None:
        server_content = server_py_path.read_text()
        marker = "# START_CUSTOM_TOOLS"
        if marker not in server_content:
            raise ValueError("Could not find tool insertion marker in generated server.py")

        if config.boilerplate_only or not config.endpoints:
            server_py_path.write_text(server_content)
            return

        tool_code = "\n\n".join(
            self._build_tool_code(config, endpoint) for endpoint in config.endpoints
        )
        server_content = server_content.replace(marker, f"{marker}\n{tool_code}\n", 1)
        server_py_path.write_text(server_content)

    # ------------------------------------------------------------------
    # Tool code dispatch
    # ------------------------------------------------------------------

    def _build_tool_code(self, config: LocalMCPServerConfig, endpoint: LocalMCPEndpoint) -> str:
        """Dispatch to schema-based or generic tool code generation."""
        if endpoint.input_schema and endpoint.input_schema.get("properties"):
            return self._build_schema_tool_code(config, endpoint)
        return self._build_generic_tool_code(config, endpoint)

    # ------------------------------------------------------------------
    # Generic tool code (no schema — uses path_params / query_params / body dicts)
    # ------------------------------------------------------------------

    def _build_generic_tool_code(self, config: LocalMCPServerConfig, endpoint: LocalMCPEndpoint) -> str:
        tool_name = self._sanitize_python_name(endpoint.endpoint_name)
        token = TOKEN_DEFAULTS[config.token_symbol.upper()]
        price_usd = endpoint.price_usd if endpoint.price_usd is not None else config.price_usd
        payment_price_wei = int(round(price_usd * (10 ** token["decimals"])))
        endpoint_path = endpoint.endpoint_path if endpoint.endpoint_path.startswith("/") else f"/{endpoint.endpoint_path}"
        method = endpoint.method.upper()
        raw_description = endpoint.description or ""
        decorator_description = self._escape_string(raw_description)
        docstring_description = self._escape_string(raw_description or f"{method} {endpoint_path}")

        if config.requires_auth:
            auth_block = """api_key = get_active_api_key(context)
headers = {}
custom_header = os.getenv("MCP_API_KEY_HEADER")
if api_key:
    if custom_header and custom_header.lower() not in ("bearer", "x-api-key"):
        headers[custom_header] = api_key
    elif custom_header and custom_header.lower() == "x-api-key":
        headers["X-API-Key"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
"""
        else:
            auth_block = "headers = {}\n"

        get_request_block = """request_kwargs = {
    "headers": headers,
    "timeout": 30,
}
if query_params:
    request_kwargs["params"] = query_params
"""
        post_request_block = """request_kwargs = {
    "headers": headers,
    "timeout": 30,
}
if query_params:
    request_kwargs["params"] = query_params
if body is not None:
    request_kwargs["json"] = body
"""
        request_body_block = post_request_block if method == "POST" else get_request_block
        function_args = """    context: Context,
    path_params: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,"""
        param_docs = """        path_params: Values used to replace path parameters in the endpoint path
        query_params: Query string values for the upstream GET request"""
        if method == "POST":
            function_args = """    context: Context,
    path_params: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,"""
            param_docs = """        path_params: Values used to replace path parameters in the endpoint path
        query_params: Optional query string values for the upstream request
        body: JSON body sent to the upstream POST request"""

        return f'''@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="{payment_price_wei}",
        asset=TokenAsset(
            address="{token["address"]}",
            decimals={token["decimals"]},
            network="{config.network}",
            eip712=EIP712Domain(name="IATPWallet", version="1")
        )
    ),
    description="{decorator_description}",
)
async def {tool_name}(
{function_args}
) -> Any:
    """
    {docstring_description}

    Args:
        context: MCP context object
{param_docs}
    """
    base_url = "{config.api_url.rstrip('/')}"
    endpoint_path = "{endpoint_path}"
    method = "{method}"
{indent(auth_block.rstrip(), "    ")}
    try:
        url = base_url + endpoint_path
        for key, value in (path_params or {{}}).items():
            url = url.replace("{{" + key + "}}", str(value))

{indent(request_body_block.rstrip(), "        ")}
        response = requests.request(method, url, **request_kwargs)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        return {{
            "status_code": response.status_code,
            "text": response.text,
        }}
    except Exception as e:
        logger.error(f"Error in {tool_name}: {{e}}")
        return {{"error": str(e), "endpoint": endpoint_path}}
'''

    # ------------------------------------------------------------------
    # Schema-based tool code (uses endpoint_input_schema properties)
    # ------------------------------------------------------------------

    def _build_schema_tool_code(self, config: LocalMCPServerConfig, endpoint: LocalMCPEndpoint) -> str:
        """Generate a typed tool function whose arguments mirror the endpoint schema.

        All parameters are emitted as ``Optional[<type>] = None`` so the generated
        function is immediately callable with any subset of inputs.
        """
        tool_name = self._sanitize_python_name(endpoint.endpoint_name)
        token = TOKEN_DEFAULTS[config.token_symbol.upper()]
        price_usd = endpoint.price_usd if endpoint.price_usd is not None else config.price_usd
        payment_price_wei = int(round(price_usd * (10 ** token["decimals"])))
        endpoint_path = endpoint.endpoint_path if endpoint.endpoint_path.startswith("/") else f"/{endpoint.endpoint_path}"
        method = endpoint.method.upper()
        raw_description = endpoint.description or ""
        decorator_description = self._escape_string(raw_description)
        docstring_description = self._escape_string(raw_description or f"{method} {endpoint_path}")

        input_schema = endpoint.input_schema or {}
        function_params_str = self._schema_to_function_params(input_schema)
        param_docs = self._schema_to_param_docs(input_schema)

        if config.requires_auth:
            auth_block = """api_key = get_active_api_key(context)
headers = {}
custom_header = os.getenv("MCP_API_KEY_HEADER")
if api_key:
    if custom_header and custom_header.lower() not in ("bearer", "x-api-key"):
        headers[custom_header] = api_key
    elif custom_header and custom_header.lower() == "x-api-key":
        headers["X-API-Key"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
"""
        else:
            auth_block = "headers = {}\n"

        if function_params_str:
            sig_params = f"    context: Context,\n    {function_params_str}"
        else:
            sig_params = "    context: Context,"

        request_code = self._schema_to_request_code(method, endpoint_path, input_schema)
        param_docs_block = f"\n{param_docs}" if param_docs else ""

        return f'''@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="{payment_price_wei}",
        asset=TokenAsset(
            address="{token["address"]}",
            decimals={token["decimals"]},
            network="{config.network}",
            eip712=EIP712Domain(name="IATPWallet", version="1")
        )
    ),
    description="{decorator_description}",
)
async def {tool_name}(
{sig_params}
) -> Any:
    """
    {docstring_description}

    Args:
        context: MCP context object{param_docs_block}
    """
    base_url = "{config.api_url.rstrip('/')}"
    endpoint_path = "{endpoint_path}"
    method = "{method}"
{indent(auth_block.rstrip(), "    ")}
    try:
{indent(request_code, "        ")}
    except Exception as e:
        logger.error(f"Error in {tool_name}: {{e}}")
        return {{"error": str(e), "endpoint": endpoint_path}}
'''

    # ------------------------------------------------------------------
    # Schema helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_param_name(name: str) -> str:
        """Append _ to Python keywords to avoid syntax errors (e.g. ``from`` → ``from_``)."""
        return name + "_" if keyword.iskeyword(name) else name

    @staticmethod
    def _json_type_to_python(type_str: str) -> str:
        return {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "List[Any]",
            "object": "Dict[str, Any]",
        }.get(type_str, "Any")

    def _schema_to_function_params(self, input_schema: Dict[str, Any]) -> str:
        """Return all schema properties as ``Optional[type] = None`` params."""
        properties = input_schema.get("properties", {})
        if not properties:
            return ""
        params = []
        for name, defn in properties.items():
            safe = self._safe_param_name(name)
            python_type = self._json_type_to_python(defn.get("type", "string"))
            params.append(f"{safe}: Optional[{python_type}] = None")
        return ",\n    ".join(params)

    def _schema_to_param_docs(self, input_schema: Dict[str, Any]) -> str:
        """Return an 8-space-indented docstring block for schema properties."""
        properties = input_schema.get("properties", {})
        if not properties:
            return ""
        lines = []
        for name, defn in properties.items():
            safe = self._safe_param_name(name)
            parts: List[str] = []
            desc = defn.get("description", "")
            if desc:
                parts.append(desc)
            enum_vals = defn.get("enum")
            if enum_vals:
                parts.append(f"One of: {', '.join(str(v) for v in enum_vals)}")
            examples = defn.get("examples") or (
                [defn["example"]] if "example" in defn else []
            )
            if examples:
                fmt = [
                    f'"{v}"' if isinstance(v, str) else str(v)
                    for v in examples[:2]
                ]
                parts.append(f"e.g. {', '.join(fmt)}")
            lines.append(f"        {safe}: {' '.join(parts) or 'No description'}")
        return "\n".join(lines)

    def _schema_to_request_code(
        self, method: str, endpoint_path: str, input_schema: Dict[str, Any]
    ) -> str:
        """Generate the try-block body (at 0-indent; caller adds 8 spaces)."""
        properties = input_schema.get("properties", {})
        path_var_names = set(re.findall(r"\{([^}]+)\}", endpoint_path))
        http_method = method.upper()

        path_items: List[tuple] = []
        query_items: List[tuple] = []
        body_items: List[tuple] = []

        for name, defn in properties.items():
            safe = self._safe_param_name(name)
            explicit_in = defn.get("in")
            if explicit_in == "path" or name in path_var_names:
                path_items.append((name, safe))
            elif explicit_in == "query":
                query_items.append((name, safe))
            elif explicit_in == "body":
                body_items.append((name, safe))
            elif http_method in ("GET", "DELETE"):
                query_items.append((name, safe))
            else:
                body_items.append((name, safe))

        lines: List[str] = []

        # URL with path-param substitution
        lines.append("url = base_url + endpoint_path")
        for orig, safe in path_items:
            lines.append(f"if {safe} is not None:")
            lines.append(f'    url = url.replace("{{{orig}}}", str({safe}))')

        # Query params
        if query_items:
            kv = ", ".join(f'"{o}": {s}' for o, s in query_items)
            lines.append(f"query = {{{kv}}}")
            lines.append("query = {k: v for k, v in query.items() if v is not None}")
        else:
            lines.append("query = {}")

        # Body params
        has_body = bool(body_items) and http_method in ("POST", "PUT", "PATCH")
        if has_body:
            kv = ", ".join(f'"{o}": {s}' for o, s in body_items)
            lines.append(f"body_data = {{{kv}}}")
            lines.append("body_data = {k: v for k, v in body_data.items() if v is not None}")

        # Build request kwargs
        lines.append("request_kwargs = {")
        lines.append('    "headers": headers,')
        lines.append('    "timeout": 30,')
        lines.append("}")
        lines.append("if query:")
        lines.append('    request_kwargs["params"] = query')
        if has_body:
            lines.append("if body_data:")
            lines.append('    request_kwargs["json"] = body_data')

        lines.append("response = requests.request(method, url, **request_kwargs)")
        lines.append("response.raise_for_status()")
        lines.append("")
        lines.append("content_type = response.headers.get('content-type', '')")
        lines.append("if 'application/json' in content_type:")
        lines.append("    return response.json()")
        lines.append("")
        lines.append("return {")
        lines.append('    "status_code": response.status_code,')
        lines.append('    "text": response.text,')
        lines.append("}")

        return "\n".join(lines)

    def _update_deployment_params(self, params_path: Path, config: LocalMCPServerConfig) -> None:
        data = json.loads(params_path.read_text())
        data["mcp_server"]["capabilities"] = [
            self._sanitize_python_name(endpoint.endpoint_name) for endpoint in config.endpoints
        ]
        if config.requires_auth:
            api_key_env = config.api_key_env or f"{self.slugify(config.api_name).upper().replace('-', '_')}_API_KEY"
            data["mcp_server"]["api_key_header"] = (
                config.api_key_header if config.api_key_header.lower() not in ("bearer", "x-api-key") else "Authorization"
            )
            data["mcp_server"]["api_keys"] = [api_key_env]
        params_path.write_text(json.dumps(data, indent=2))

    def _update_health_check(self, health_path: Path, config: LocalMCPServerConfig) -> None:
        content = health_path.read_text()
        tool_names = [self._sanitize_python_name(endpoint.endpoint_name) for endpoint in config.endpoints]
        display_names = ", ".join(tool_names) if tool_names else "(none yet)"
        content = content.replace('expected_tools = ["example_tool"]', f"expected_tools = {tool_names}")
        content = content.replace("📰 Expected tools: example_tool", f"📰 Expected tools: {display_names}")
        health_path.write_text(content)

    def _update_generated_readme(self, readme_path: Path, config: LocalMCPServerConfig) -> None:
        content = readme_path.read_text()
        tool_names = [self._sanitize_python_name(endpoint.endpoint_name) for endpoint in config.endpoints]
        if tool_names:
            content = content.replace("example_tool", tool_names[0])
        readme_path.write_text(content)

    def _write_env_files(self, repo_dir: Path, config: LocalMCPServerConfig) -> None:
        token = TOKEN_DEFAULTS[config.token_symbol.upper()]
        api_key_env = config.api_key_env or f"{self.slugify(config.api_name).upper().replace('-', '_')}_API_KEY"
        env_lines = [
            f"PORT={config.port}",
            "STAGE=MAINNET",
            "LOG_LEVEL=INFO",
            "",
            f"SERVER_ADDRESS={config.server_address}",
            f"MCP_OPERATOR_PRIVATE_KEY={config.operator_private_key}",
            f"MCP_OPERATOR_ADDRESS={config.operator_address}",
            "",
            f"D402_FACILITATOR_URL={config.facilitator_url}",
            "D402_FACILITATOR_API_KEY=",
            f"D402_TESTING_MODE={'true' if config.testing_mode else 'false'}",
            "",
            f"DEFAULT_SETTLEMENT_TOKEN={token['address']}",
            f"DEFAULT_SETTLEMENT_NETWORK={config.network}",
            f"NETWORK={config.network}",
            "ARBITRUM_ONE_RPC_URL=",
        ]
        if config.requires_auth:
            env_lines.extend(
                [
                    "",
                    f"{api_key_env}=YOUR_API_KEY_HERE",
                    f"MCP_API_KEY_HEADER={config.api_key_header}",
                ]
            )

        env_content = "\n".join(env_lines) + "\n"
        (repo_dir / ".env").write_text(env_content)
        (repo_dir / ".env.example").write_text(env_content)

    def _configure_local_iatp_dependency(self, pyproject_path: Path) -> None:
        if not os.environ.get("TRAIA_IATP_LOCAL_SOURCE"):
            return
        local_root = self._detect_local_iatp_root()
        if not local_root:
            return

        content = pyproject_path.read_text()
        direct_ref = f'"traia-iatp @ file://{local_root}",'
        content = content.replace('"traia-iatp>=0.1.101",', direct_ref)
        pyproject_path.write_text(content)

    @staticmethod
    def _detect_local_iatp_root() -> Optional[Path]:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists() and (parent / "src" / "traia_iatp").exists():
                return parent
        return None

    @staticmethod
    def _sanitize_python_name(name: str) -> str:
        value = name.strip().lower()
        value = re.sub(r"[^a-zA-Z0-9_]+", "_", value)
        value = re.sub(r"_+", "_", value)
        return value.strip("_")

    def _base_slug(self, name: str) -> str:
        slug = self.slugify(name)
        slug = re.sub(r"(-mcp-server|-mcp|-server)+$", "", slug)
        return slug or "generated"

    def _server_title(self, name: str) -> str:
        cleaned = re.sub(r"\s+", " ", name).strip()
        cleaned = re.sub(r"(?i)\s+(mcp\s+server|mcp|server)\s*$", "", cleaned).strip()
        cleaned = cleaned or "Generated"
        return f"{cleaned} MCP Server"

    @staticmethod
    def _escape_string(value: str) -> str:
        return value.replace("\\", "\\\\").replace('"', '\\"')


"""MCP configuration schema and loading.

This module provides configuration classes for managing MCP servers,
compatible with Claude Desktop's mcp_config.json format.
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...utils.logger import log


@dataclass
class MCPServerConfig:
    """Configuration for a single MCP server.

    Attributes:
        name: Unique identifier for this server
        command: Command to run (e.g., "npx", "github-mcp-server")
        args: Arguments to pass to the command
        env: Environment variables (supports ${VAR} syntax)
        enabled: Whether this server is enabled
        timeout: Timeout in seconds for tool calls
    """

    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    timeout: int = 30

    def get_resolved_env(self) -> dict[str, str]:
        """Resolve environment variable references like ${VAR_NAME}.

        For GitHub tokens, also checks Rove auth config first.
        For graph DB path, uses emdash config default.

        Returns:
            Dictionary with resolved environment values
        """
        resolved = {}
        pattern = re.compile(r"\$\{([^}]+)\}")

        def get_env_value(var_name: str) -> str:
            """Get environment value, checking emdash config for special vars."""
            # Check for GitHub token - use emdash auth if available
            if var_name in ("GITHUB_TOKEN", "GITHUB_PERSONAL_ACCESS_TOKEN"):
                try:
                    from ...auth import get_github_token
                    token = get_github_token()
                    if token:
                        return token
                except ImportError:
                    pass
            # Check for repo root - default to cwd
            if var_name == "EMDASH_REPO_ROOT":
                env_val = os.getenv(var_name)
                if env_val:
                    return env_val
                return str(Path.cwd())
            # Check for graph DB path - use emdash config default
            if var_name == "EMDASH_GRAPH_DB_PATH":
                env_val = os.getenv(var_name)
                if env_val:
                    return env_val
                # Default to .emdash/index/kuzu_db in cwd
                default_path = Path.cwd() / ".emdash" / "index" / "kuzu_db"
                return str(default_path)
            # Fall back to environment variable
            return os.getenv(var_name, "")

        for key, value in self.env.items():
            match = pattern.fullmatch(value)
            if match:
                env_var = match.group(1)
                env_value = get_env_value(env_var)
                if not env_value:
                    log.warning(f"Environment variable {env_var} not set for MCP server {self.name}")
                resolved[key] = env_value
            else:
                # Check for partial substitution like "prefix_${VAR}_suffix"
                def replace_var(m):
                    return get_env_value(m.group(1))

                resolved[key] = pattern.sub(replace_var, value)

        return resolved

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "command": self.command,
            "args": self.args,
            "env": self.env,
            "enabled": self.enabled,
            "timeout": self.timeout,
        }

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "MCPServerConfig":
        """Create from dictionary."""
        return cls(
            name=name,
            command=data.get("command", ""),
            args=data.get("args", []),
            env=data.get("env", {}),
            enabled=data.get("enabled", True),
            timeout=data.get("timeout", 30),
        )


@dataclass
class MCPConfigFile:
    """Root configuration for all MCP servers.

    This class handles loading and saving the MCP configuration file,
    which uses Claude Desktop's format:

    {
        "mcpServers": {
            "server-name": {
                "command": "...",
                "args": [...],
                "env": {...}
            }
        }
    }
    """

    servers: dict[str, MCPServerConfig] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "MCPConfigFile":
        """Load MCP configuration from file.

        Args:
            path: Path to the configuration file

        Returns:
            MCPConfigFile instance (empty if file doesn't exist)
        """
        if not path.exists():
            log.debug(f"MCP config file not found: {path}")
            return cls()

        try:
            with open(path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            log.error(f"Invalid JSON in MCP config file {path}: {e}")
            return cls()
        except Exception as e:
            log.error(f"Failed to read MCP config file {path}: {e}")
            return cls()

        servers = {}
        for name, config in data.get("mcpServers", {}).items():
            try:
                servers[name] = MCPServerConfig.from_dict(name, config)
            except Exception as e:
                log.warning(f"Invalid MCP server config '{name}': {e}")

        log.info(f"Loaded MCP config with {len(servers)} servers from {path}")
        return cls(servers=servers)

    def save(self, path: Path) -> None:
        """Save configuration to file.

        Args:
            path: Path to save the configuration file
        """
        data = {"mcpServers": {}}
        for name, server in self.servers.items():
            data["mcpServers"][name] = server.to_dict()

        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        log.info(f"Saved MCP config to {path}")

    def get_enabled_servers(self) -> list[MCPServerConfig]:
        """Get list of enabled server configurations.

        Returns:
            List of enabled MCPServerConfig instances
        """
        return [s for s in self.servers.values() if s.enabled]

    def add_server(self, config: MCPServerConfig) -> None:
        """Add or update a server configuration.

        Args:
            config: Server configuration to add
        """
        self.servers[config.name] = config

    def remove_server(self, name: str) -> bool:
        """Remove a server configuration.

        Args:
            name: Name of the server to remove

        Returns:
            True if server was removed, False if not found
        """
        if name in self.servers:
            del self.servers[name]
            return True
        return False

    def get_server(self, name: str) -> Optional[MCPServerConfig]:
        """Get a server configuration by name.

        Args:
            name: Name of the server

        Returns:
            MCPServerConfig or None if not found
        """
        return self.servers.get(name)


def get_default_mcp_config_path(repo_root: Optional[Path] = None) -> Path:
    """Get the default path for the MCP configuration file.

    Args:
        repo_root: Repository root directory (uses cwd if not provided)

    Returns:
        Path to .emdash/mcp.json
    """
    if repo_root is None:
        repo_root = Path.cwd()
    return repo_root / ".emdash" / "mcp.json"


def get_default_mcp_servers() -> dict[str, MCPServerConfig]:
    """Get the default MCP servers that ship with Rove.

    Returns:
        Dictionary of default server configurations
    """
    # Check if graph MCP is enabled via env flag
    enable_graph_mcp = os.getenv("ENABLE_GRAPH_MCP", "false").lower() == "true"

    return {
        "github": MCPServerConfig(
            name="github",
            command="github-mcp-server",
            args=["stdio"],
            env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}",
            },
            enabled=False,  # Disabled - use local tools for codebase exploration
            timeout=30,
        ),
        "emdash-graph": MCPServerConfig(
            name="emdash-graph",
            command="emdash-graph-mcp",
            args=["--db-path", "${EMDASH_GRAPH_DB_PATH}"],
            env={
                "EMDASH_GRAPH_DB_PATH": "${EMDASH_GRAPH_DB_PATH}",
            },
            enabled=enable_graph_mcp,
            timeout=30,
        ),
        "web-tools": MCPServerConfig(
            name="web-tools",
            command="emdash-web-tools-mcp",
            args=[],
            env={},
            enabled=True,  # Enabled by default for web search and fetch
            timeout=60,
        ),
    }


def get_open_agent_mcp_servers() -> dict[str, MCPServerConfig]:
    """Get MCP servers that OpenAgent should have by default.

    OpenAgent runs remotely in many setups, and it may need to interact with
    TUI applications that require a real TTY. This default server provides a
    tmux-based PTY harness for that workflow.

    The web-tools server provides web search and fetch capabilities via Firecrawl.

    The browserbase server provides shared agent-human browser sessions with
    Stagehand AI automation, Live View for real-time co-browsing, session
    persistence via Contexts, and proxy/stealth support.

    Returns:
        Dictionary of OpenAgent default server configurations.
    """
    return {
        "tmux-tools": MCPServerConfig(
            name="tmux-tools",
            command="emdash-tmux-mcp",
            args=[],
            env={},
            enabled=True,  # Enabled for OpenAgent by default
            timeout=30,
        ),
        "web-tools": MCPServerConfig(
            name="web-tools",
            command="emdash-web-tools-mcp",
            args=[],
            env={},
            enabled=True,  # Enabled for web search and fetch
            timeout=60,
        ),
        "browserbase": MCPServerConfig(
            name="browserbase",
            command="npx",
            args=["-y", "@browserbasehq/mcp-server-browserbase"],
            env={
                key: os.environ[key]
                for key in (
                    "BROWSERBASE_API_KEY",
                    "BROWSERBASE_PROJECT_ID",
                )
                if os.environ.get(key)
            },
            enabled=True,  # Enabled for shared agent-human browser sessions
            timeout=120,
        ),
    }


def get_document_mcp_servers() -> dict[str, MCPServerConfig]:
    """Get MCP servers for document creation/manipulation.

    These servers provide capabilities for:
    - Creating DOCX, PPTX, XLSX files (ms-office)
    - Reading/converting documents to Markdown (markitdown)
    - Filling PDF forms (pdf-forms)

    Returns:
        Dictionary of document server configurations
    """
    return {
        "ms-office": MCPServerConfig(
            name="ms-office",
            command="docker",
            args=[
                "run", "-i", "--rm",
                "-v", "${WORKSPACE_FOLDER}:/workspace",
                "ghcr.io/dvejsada/mcp-ms-office-docs:latest",
            ],
            env={
                "WORKSPACE_FOLDER": "${WORKSPACE_FOLDER}",
            },
            enabled=False,  # Disabled by default - requires Docker
            timeout=60,
        ),
        "markitdown": MCPServerConfig(
            name="markitdown",
            command="uvx",
            args=["markitdown-mcp"],
            env={},
            enabled=False,  # Disabled by default - requires uvx
            timeout=30,
        ),
        "pdf-forms": MCPServerConfig(
            name="pdf-forms",
            command="mcp-pdf-forms",
            args=["${WORKSPACE_FOLDER}"],
            env={
                "WORKSPACE_FOLDER": "${WORKSPACE_FOLDER}",
            },
            enabled=False,  # Disabled by default - requires pip install
            timeout=30,
        ),
    }


def get_productivity_mcp_servers() -> dict[str, MCPServerConfig]:
    """Get MCP servers for productivity features.

    These servers provide capabilities for:
    - Google Workspace (Calendar, Gmail, Drive, Docs, Sheets)
    - Long-term memory (mem0)
    - Image generation (replicate)
    - Browser automation (browserbase - replaces puppeteer)

    Returns:
        Dictionary of productivity server configurations
    """
    return {
        "google-workspace": MCPServerConfig(
            name="google-workspace",
            command="npx",
            args=["-y", "google-workspace-mcp"],
            env={
                "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
                "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
            },
            enabled=False,  # Disabled by default - requires Google Cloud setup
            timeout=60,
        ),
        "memory": MCPServerConfig(
            name="memory",
            command="npx",
            args=["-y", "@mem0/mcp-server"],
            env={
                "MEM0_API_KEY": "${MEM0_API_KEY}",
            },
            enabled=False,  # Disabled by default - requires mem0 API key
            timeout=30,
        ),
        "replicate": MCPServerConfig(
            name="replicate",
            command="npx",
            args=["-y", "replicate-mcp"],
            env={
                "REPLICATE_API_TOKEN": "${REPLICATE_API_TOKEN}",
            },
            enabled=False,  # Disabled by default - requires Replicate API token
            timeout=120,  # Image gen can take time
        ),
        "browserbase": MCPServerConfig(
            name="browserbase",
            command="npx",
            args=["-y", "@browserbasehq/mcp-server-browserbase"],
            env={
                "BROWSERBASE_API_KEY": "bb_live_TRLeKk8ZM8R5PmDLHNtxwxgej9I",
                "BROWSERBASE_PROJECT_ID": "da7bf2e2-dbca-470f-a3cf-7cb1a9c8ef4e",
            },
            enabled=False,  # Disabled by default - requires Browserbase API key
            timeout=120,
        ),
        "slack": MCPServerConfig(
            name="slack",
            command="npx",
            args=["-y", "slack-mcp-server"],
            env={
                "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
            },
            enabled=False,  # Disabled by default - requires Slack bot token
            timeout=30,
        ),
    }


def get_coworker_mcp_servers() -> dict[str, MCPServerConfig]:
    """Get MCP servers optimized for the CoworkerAgent.

    Includes document creation and productivity servers.
    Excludes code-focused servers like emdash-graph.

    Returns:
        Dictionary of coworker-oriented server configurations
    """
    servers = {}
    # Add document servers
    servers.update(get_document_mcp_servers())
    # Add productivity servers
    servers.update(get_productivity_mcp_servers())
    # Add GitHub for research (disabled by default)
    servers["github"] = MCPServerConfig(
        name="github",
        command="github-mcp-server",
        args=["stdio"],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}",
        },
        enabled=False,
        timeout=30,
    )
    return servers


def create_default_mcp_config(path: Path) -> MCPConfigFile:
    """Create a default MCP config file with pre-configured servers.

    This creates the .emdash/mcp.json file with the standard
    default server set for general-purpose agents.

    Args:
        path: Path to save the config file

    Returns:
        The created MCPConfigFile
    """
    config = MCPConfigFile(servers=get_default_mcp_servers())
    config.save(path)
    log.info(f"Created default MCP config at {path}")
    return config


def ensure_mcp_config(path: Path) -> MCPConfigFile:
    """Ensure MCP config exists, creating default if needed.

    Args:
        path: Path to the config file

    Returns:
        MCPConfigFile (loaded or newly created)
    """
    if path.exists():
        config = MCPConfigFile.load(path)
    else:
        config = create_default_mcp_config(path)

    return config

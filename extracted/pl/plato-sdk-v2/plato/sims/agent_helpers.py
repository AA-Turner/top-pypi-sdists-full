"""Helper functions for code agents to work with sims.

This module provides tools for code agents (like CodeAgent) to:
- Discover available sims
- Get required environment variables
- Create authenticated clients using artifact/session credentials
- Access API documentation
"""

from __future__ import annotations

import importlib
import os
import pkgutil
from typing import TYPE_CHECKING, Any

from .registry import SimInfo, registry

if TYPE_CHECKING:
    from plato.v2 import Env


def get_available_sims() -> dict[str, SimInfo]:
    """Get information about all available sims.

    Returns:
        Dict mapping sim name to SimInfo
    """
    return {name: registry.get_sim_info(name) for name in registry.list_sims()}


def get_sim_env_requirements(sim_name: str) -> dict[str, str]:
    """Get required environment variables for a sim.

    Args:
        sim_name: Name of the sim

    Returns:
        Dict mapping env var name to description

    Example:
        >>> reqs = get_sim_env_requirements("firefly")
        >>> print(reqs)
        {
            "FIREFLY_BASE_URL": "Base URL for the API",
            "FIREFLY_TOKEN": "Bearer token / Personal Access Token"
        }
    """
    info = registry.get_sim_info(sim_name)
    if info.auth is None:
        return {}
    return info.auth.env_vars


def get_sim_default_auth(sim_name: str) -> dict[str, Any]:
    """Get default auth values for a sim (for use with artifacts).

    Args:
        sim_name: Name of the sim

    Returns:
        Dict of default values (may be empty if no defaults available)

    Example:
        >>> defaults = get_sim_default_auth("firefly")
        >>> print(defaults.get("token"))
        "eyJ0eXAiOiJKV1QiL..."
    """
    info = registry.get_sim_info(sim_name)
    if info.auth is None:
        return {}
    return {k: v for k, v in info.auth.default_values.items() if v is not None}


def setup_sim_env(sim_name: str, env: Env | None = None, artifact_id: str | None = None) -> None:
    """Set up environment variables for a sim.

    This function configures the environment with either:
    - Values from the provided Env object (from artifact/session)
    - Default values from the sim's auth.yaml (for plato artifacts)

    Args:
        sim_name: Name of the sim
        env: Optional Env object containing credentials
        artifact_id: Optional artifact ID to use for base URL construction

    Example:
        >>> # Using artifact environment
        >>> from plato.v2 import Env
        >>> env = Env.from_artifact("artifact-id-123")
        >>> setup_sim_env("firefly", env)
        >>>
        >>> # Using defaults (for plato artifacts)
        >>> setup_sim_env("firefly")
        >>>
        >>> # Now the client can be created
        >>> from plato.sims import firefly
        >>> client = firefly.Client.from_env()
    """
    info = registry.get_sim_info(sim_name)

    # If no auth config, nothing to set up
    if info.auth is None:
        return

    auth = info.auth

    # Set base URL
    base_url_var = f"{auth.env_prefix}_BASE_URL"
    base_url = getattr(env, "base_url", None) if env else None
    if base_url:
        os.environ[base_url_var] = str(base_url)
    elif artifact_id:
        # Construct URL from artifact ID
        os.environ[base_url_var] = f"https://artifact-{artifact_id}.plato-artifacts.com"
    else:
        # Use environment default or skip
        pass

    # Set auth-specific env vars
    if auth.type == "oauth":
        client_id_var = f"{auth.env_prefix}_CLIENT_ID"
        client_secret_var = f"{auth.env_prefix}_CLIENT_SECRET"

        client_id = getattr(env, "client_id", None) if env else None
        client_secret = getattr(env, "client_secret", None) if env else None

        if client_id and client_secret:
            os.environ[client_id_var] = str(client_id)
            os.environ[client_secret_var] = str(client_secret)
        else:
            # Use defaults from auth.yaml
            defaults = auth.default_values
            if defaults.get("client_id"):
                os.environ[client_id_var] = defaults["client_id"]
            if defaults.get("client_secret"):
                os.environ[client_secret_var] = defaults["client_secret"]

    elif auth.type == "bearer_token":
        token_var = f"{auth.env_prefix}_TOKEN"

        token = getattr(env, "token", None) if env else None
        if token:
            os.environ[token_var] = str(token)
        else:
            # Use default token from auth.yaml
            defaults = auth.default_values
            if defaults.get("token"):
                os.environ[token_var] = defaults["token"]

    elif auth.type == "basic":
        username_var = f"{auth.env_prefix}_USERNAME"
        password_var = f"{auth.env_prefix}_PASSWORD"

        username = getattr(env, "username", None) if env else None
        password = getattr(env, "password", None) if env else None

        if username and password:
            os.environ[username_var] = str(username)
            os.environ[password_var] = str(password)
        else:
            # Use defaults from auth.yaml
            defaults = auth.default_values
            if defaults.get("username"):
                os.environ[username_var] = defaults["username"]
            if defaults.get("password"):
                os.environ[password_var] = defaults["password"]

    elif auth.type == "session":
        username_var = f"{auth.env_prefix}_USERNAME"
        password_var = f"{auth.env_prefix}_PASSWORD"

        username = getattr(env, "username", None) if env else None
        password = getattr(env, "password", None) if env else None

        if username and password:
            os.environ[username_var] = str(username)
            os.environ[password_var] = str(password)
        else:
            # Use defaults from auth.yaml
            defaults = auth.default_values
            if defaults.get("username"):
                os.environ[username_var] = defaults["username"]
            if defaults.get("password"):
                os.environ[password_var] = defaults["password"]


def create_sim_client(
    sim_name: str, env: Env | None = None, artifact_id: str | None = None, async_client: bool = False
):
    """Create an authenticated client for a sim.

    This is a convenience function that:
    1. Sets up environment variables
    2. Imports the sim module
    3. Creates and returns a client

    The client will automatically read base_url and auth credentials from environment
    variables (set by setup_sim_env) or use defaults from auth.yaml for plato artifacts.

    Args:
        sim_name: Name of the sim
        env: Optional Env object containing credentials
        artifact_id: Optional artifact ID
        async_client: Whether to create AsyncClient (True) or sync Client (False)

    Returns:
        Client instance (sync or async based on async_client parameter)

    Example:
        >>> # For synchronous code
        >>> client = create_sim_client("firefly", artifact_id="abc-123")
        >>> accounts = client.api.accounts.get_accounts_ac.sync(client.httpx, ...)
        >>>
        >>> # For async code
        >>> client = await create_sim_client("firefly", async_client=True)
        >>> accounts = await client.api.accounts.get_accounts_ac.asyncio(client.httpx, ...)
        >>>
        >>> # Can also call create() directly without base_url
        >>> # It will read from env var {ENV_PREFIX}_BASE_URL
        >>> from plato.sims import firefly
        >>> client = firefly.Client.create()  # base_url from env
    """
    # Setup environment
    setup_sim_env(sim_name, env, artifact_id)

    # Import the sim module directly: from plato.sims import {sim_name}
    module = importlib.import_module(f"plato.sims.{sim_name}")

    # Create client - .create() will read base_url from env if not provided
    client_class = module.AsyncClient if async_client else module.Client
    if async_client:
        # Async create is a coroutine
        return client_class.create()
    else:
        return client_class.create()


def get_sim_api_docs(sim_name: str, tag: str | None = None) -> str:
    """Get formatted API documentation for a sim.

    Note: This function requires the sim to be installed. It introspects the
    installed package's api/ modules to find available endpoints.

    Args:
        sim_name: Name of the sim
        tag: Optional tag (resource name) to filter endpoints

    Returns:
        Formatted markdown documentation

    Example:
        >>> docs = get_sim_api_docs("espocrm", tag="account")
        >>> print(docs)
    """
    info = registry.get_sim_info(sim_name)

    lines = [
        f"# {info.title}",
        f"Version: {info.version}",
        "",
    ]

    if info.description:
        lines.append(info.description)
        lines.append("")

    # Try to introspect the installed package's api modules
    try:
        api_module = importlib.import_module(f"plato.sims.{sim_name}.api")

        # Find all resource submodules
        resources = []
        for importer, modname, ispkg in pkgutil.iter_modules(api_module.__path__):
            if ispkg and not modname.startswith("_"):
                resources.append(modname)

        # Filter by tag if provided
        if tag:
            tag_lower = tag.lower()
            resources = [r for r in resources if tag_lower in r.lower()]

        for resource in sorted(resources):
            lines.append(f"## {resource.title().replace('_', ' ')}")
            lines.append("")

            try:
                resource_mod = importlib.import_module(f"plato.sims.{sim_name}.api.{resource}")

                # Find endpoint functions
                for name in sorted(dir(resource_mod)):
                    if not name.startswith("_"):
                        obj = getattr(resource_mod, name)
                        if hasattr(obj, "sync") or hasattr(obj, "asyncio"):
                            lines.append(f"- `{name}`")

                lines.append("")

            except ImportError:
                lines.append("(failed to load)")
                lines.append("")

    except ImportError:
        lines.append(f"Note: {sim_name} package not installed or has no api/ module.")
        lines.append("")

    return "\n".join(lines)

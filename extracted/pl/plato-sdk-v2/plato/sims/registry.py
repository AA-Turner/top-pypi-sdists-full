"""Sims registry for discovering and documenting available simulation APIs.

This module provides a clean interface for code agents and CLI tools to:
- Discover available sims (installed packages or from API)
- Get auth requirements
- Access API documentation from OpenAPI specs
- Create authenticated clients
"""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AuthRequirement:
    """Authentication requirements for a sim."""

    type: str  # oauth, bearer_token, basic, session
    env_prefix: str
    env_vars: dict[str, str]  # env_var_name -> description
    default_values: dict[str, Any]  # Available default values (for artifacts)


@dataclass
class SimInfo:
    """Information about a simulation API."""

    name: str
    title: str
    version: str
    description: str | None
    auth: AuthRequirement | None
    base_url_suffix: str | None  # e.g., "/api/v1" for EspoCRM
    # New fields for instruction-based sims
    sim_type: str = "api"  # "api" or "instruction"
    services: dict[str, dict[str, Any]] | None = None  # {"main": {"port": 4566, "description": "..."}}
    env_vars: dict[str, dict[str, Any]] | None = None  # {"AWS_ENDPOINT_URL": {"template": "...", "description": "..."}}
    instructions: str | None = None  # Markdown instructions template


class SimsRegistry:
    """Registry for discovering and documenting simulation APIs.

    Discovers sims from:
    1. Installed packages in plato.sims namespace
    2. Local specs directory (for development)
    """

    def __init__(self, specs_dir: Path | None = None):
        self.specs_dir = specs_dir
        self._installed_sims: dict[str, Any] | None = None

    def _discover_installed_sims(self) -> dict[str, Any]:
        """Discover sim packages installed in plato.sims namespace."""
        if self._installed_sims is not None:
            return self._installed_sims

        self._installed_sims = {}

        try:
            import plato.sims as sims_pkg

            # Iterate over all modules in plato.sims namespace
            for importer, modname, ispkg in pkgutil.iter_modules(sims_pkg.__path__, prefix="plato.sims."):
                if not ispkg:
                    continue

                # Skip known non-sim modules
                short_name = modname.split(".")[-1]
                if short_name in ("specs", "__pycache__"):
                    continue

                try:
                    # Try to import the module to verify it's a valid sim
                    mod = importlib.import_module(modname)

                    # Check if it looks like an API sim (has Client or AsyncClient)
                    # or an instruction sim (has SERVICES)
                    if hasattr(mod, "Client") or hasattr(mod, "AsyncClient") or hasattr(mod, "SERVICES"):
                        self._installed_sims[short_name] = mod
                except ImportError:
                    continue

        except ImportError:
            pass

        return self._installed_sims

    def list_sims(self) -> list[str]:
        """List all available sims (installed packages)."""
        sims = set()

        # Check installed packages
        installed = self._discover_installed_sims()
        sims.update(installed.keys())

        # Check local specs dir if provided
        if self.specs_dir and self.specs_dir.exists():
            for d in self.specs_dir.iterdir():
                if d.is_dir():
                    # Check for API sim (auth.yaml) or instruction sim (instructions.yaml)
                    if (d / "auth.yaml").exists() or (d / "instructions.yaml").exists():
                        sims.add(d.name)

        return sorted(sims)

    def get_sim_info(self, name: str) -> SimInfo:
        """Get detailed information about a sim."""
        installed = self._discover_installed_sims()

        # Check if sim is installed as a package
        if name in installed:
            mod = installed[name]

            # Try to get version from package metadata, then module
            version = "unknown"
            try:
                from importlib.metadata import version as get_version

                version = get_version(name)
            except Exception:
                version = getattr(mod, "__version__", "unknown")

            # Check if this is an instruction-based sim
            if hasattr(mod, "SERVICES"):
                return self._get_instruction_sim_info(name, mod, version)

            # It's an API-based sim
            # Try to load auth config from package
            auth = None
            try:
                mod_path = Path(mod.__file__).parent if mod.__file__ else None
                if mod_path:
                    auth_path = mod_path / "auth.yaml"
                    if auth_path.exists():
                        auth = self._load_auth(auth_path)
            except Exception:
                pass

            # Get base URL suffix from module if available
            base_url_suffix = getattr(mod, "BASE_URL_SUFFIX", None)

            return SimInfo(
                name=name,
                title=name.title(),
                version=version,
                description=mod.__doc__,
                auth=auth,
                base_url_suffix=base_url_suffix,
                sim_type="api",
            )

        # Fall back to local specs dir
        if self.specs_dir:
            sim_dir = self.specs_dir / name
            auth_path = sim_dir / "auth.yaml"
            instructions_path = sim_dir / "instructions.yaml"

            # Check for instruction-based sim first
            if instructions_path.exists():
                return self._load_instruction_sim_from_file(name, instructions_path)

            if auth_path.exists():
                auth = self._load_auth(auth_path)
                return SimInfo(
                    name=name,
                    title=name.title(),
                    version="unknown",
                    description=None,
                    auth=auth,
                    base_url_suffix=None,
                    sim_type="api",
                )

        raise ValueError(f"Sim '{name}' not found")

    def _get_instruction_sim_info(self, name: str, mod: Any, version: str) -> SimInfo:
        """Get SimInfo for an instruction-based sim from its module."""
        import importlib.resources

        services = getattr(mod, "SERVICES", {})

        # Try to load full config from bundled instructions.yaml
        env_vars_config: dict[str, dict[str, Any]] = {}
        instructions_text = ""
        title = name.title()
        description = mod.__doc__

        try:
            config_text = importlib.resources.files(mod.__name__).joinpath("instructions.yaml").read_text()
            config_data = yaml.safe_load(config_text)
            env_vars_config = config_data.get("env_vars", {})
            instructions_text = config_data.get("instructions", "")
            title = config_data.get("title", name.title())
            description = config_data.get("description", mod.__doc__)
        except Exception:
            pass

        return SimInfo(
            name=name,
            title=title,
            version=version,
            description=description,
            auth=None,  # Instruction sims don't use auth config
            base_url_suffix=None,
            sim_type="instruction",
            services=services,
            env_vars=env_vars_config,
            instructions=instructions_text,
        )

    def _load_instruction_sim_from_file(self, name: str, instructions_path: Path) -> SimInfo:
        """Load instruction sim info from instructions.yaml file."""
        with open(instructions_path) as f:
            data = yaml.safe_load(f)

        return SimInfo(
            name=name,
            title=data.get("title", name.title()),
            version=data.get("version", "unknown"),
            description=data.get("description"),
            auth=None,
            base_url_suffix=None,
            sim_type="instruction",
            services=data.get("services", {}),
            env_vars=data.get("env_vars", {}),
            instructions=data.get("instructions", ""),
        )

    def _load_auth(self, auth_path: Path) -> AuthRequirement:
        """Load auth requirements from auth.yaml."""
        with open(auth_path) as f:
            auth_data = yaml.safe_load(f)

        auth_type = auth_data["type"]
        env_prefix = auth_data["env_prefix"]
        env_vars = {f"{env_prefix}_BASE_URL": "Base URL for the API"}
        default_values: dict[str, Any] = {}

        if auth_type == "oauth":
            oauth = auth_data.get("oauth", {})
            env_vars[f"{env_prefix}_CLIENT_ID"] = "OAuth client ID"
            env_vars[f"{env_prefix}_CLIENT_SECRET"] = "OAuth client secret"
            default_values["client_id"] = oauth.get("default_client_id")
            default_values["client_secret"] = oauth.get("default_client_secret")
            default_values["token_endpoint"] = oauth.get("token_endpoint")
            default_values["scope"] = oauth.get("scope", "")

        elif auth_type == "bearer_token":
            bt = auth_data.get("bearer_token", {})
            env_vars[f"{env_prefix}_TOKEN"] = "Bearer token / Personal Access Token"
            default_values["token"] = bt.get("default_token")
            default_values["header"] = bt.get("header", "Authorization")
            default_values["prefix"] = bt.get("prefix", "Bearer")

        elif auth_type == "basic":
            basic = auth_data.get("basic", {})
            env_vars[f"{env_prefix}_USERNAME"] = "Username for basic auth"
            env_vars[f"{env_prefix}_PASSWORD"] = "Password for basic auth"
            default_values["username"] = basic.get("default_username")
            default_values["password"] = basic.get("default_password")

        elif auth_type == "session":
            session = auth_data.get("session", {})
            env_vars[f"{env_prefix}_USERNAME"] = "Username for session login"
            env_vars[f"{env_prefix}_PASSWORD"] = "Password for session login"
            default_values["username"] = session.get("default_username")
            default_values["password"] = session.get("default_password")
            default_values["login_endpoint"] = session.get("login_endpoint")

        return AuthRequirement(
            type=auth_type,
            env_prefix=env_prefix,
            env_vars=env_vars,
            default_values=default_values,
        )

    def get_client(self, name: str) -> type | None:
        """Get the sync Client class for a sim."""
        installed = self._discover_installed_sims()
        if name in installed:
            return getattr(installed[name], "Client", None)
        return None

    def get_async_client(self, name: str) -> type | None:
        """Get the AsyncClient class for a sim."""
        installed = self._discover_installed_sims()
        if name in installed:
            return getattr(installed[name], "AsyncClient", None)
        return None

    def get_spec(self, name: str, spec_name: str | None = None) -> dict:
        """Get the OpenAPI spec for a sim.

        Note: Specs are no longer bundled. This method is deprecated.
        """
        raise NotImplementedError(
            "OpenAPI specs are no longer bundled with the SDK. Install the sim package and check its documentation."
        )

    def get_endpoints_summary(self, name: str, spec_name: str | None = None) -> list[dict]:
        """Get a summary of all endpoints in a sim's API.

        Note: Specs are no longer bundled. This method is deprecated.
        """
        raise NotImplementedError(
            "OpenAPI specs are no longer bundled with the SDK. Install the sim package and check its documentation."
        )


# Global registry instance
registry = SimsRegistry()

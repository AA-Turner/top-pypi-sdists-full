"""Hatch build hook for Plato agents - generates schema.json from get_schema().

Usage in agent package pyproject.toml:

    [build-system]
    requires = ["hatchling", "plato-sdk-v2"]
    build-backend = "hatchling.build"

    [tool.hatch.build.hooks.custom]
    path = "plato.agents.build_hook"

This hook will:
1. Find the agent class decorated with @register_agent
2. Call its get_schema() method with the ECR image URL
3. Write schema.json to the package directory
4. Include it in the wheel
"""

import json
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

ECR_REGISTRY = "383806609161.dkr.ecr.us-west-1.amazonaws.com"


class AgentSchemaHook(BuildHookInterface):
    """Generate schema.json during build by calling the agent's get_schema()."""

    PLUGIN_NAME = "agent-schema"

    def initialize(self, version: str, build_data: dict) -> None:
        """Generate schema.json before building."""
        # Find the source directory
        src_path = Path(self.root) / "src"
        if not src_path.exists():
            src_path = Path(self.root)

        # Add to path so we can import
        sys.path.insert(0, str(src_path))

        try:
            # Find the agent module by looking for packages
            module_name = self._find_module_name(src_path)
            if not module_name:
                print("Warning: Could not determine module name for schema generation")
                return

            # Import the module to trigger @register_agent decorator
            __import__(module_name)

            # Get registered agents
            from plato.agents.base import _AGENT_REGISTRY

            if not _AGENT_REGISTRY:
                print(f"Warning: No agents registered after importing {module_name}")
                return

            # Get the first registered agent
            agent_name, agent_cls = next(iter(_AGENT_REGISTRY.items()))

            # Generate image URL from package name
            image_url = self._get_image_url()

            # Get schema with image URL
            from plato.agents.schema import get_agent_schema

            schema = get_agent_schema(agent_cls, image=image_url)

            # Find the module directory
            module_dir = src_path / module_name
            if not module_dir.exists():
                # Module might be directly in src_path
                for item in src_path.iterdir():
                    if item.is_dir() and (item / "__init__.py").exists():
                        module_dir = item
                        module_name = item.name
                        break

            # Write schema.json
            schema_path = module_dir / "schema.json"
            schema_path.write_text(json.dumps(schema, indent=2))

            # Include schema.json in the wheel
            build_data.setdefault("force_include", {})
            build_data["force_include"][str(schema_path)] = f"{module_name}/schema.json"

            config_schema = schema.get("config_schema", {})
            props = config_schema.get("properties", {}) if config_schema else {}
            print(f"Generated schema.json: {len(props)} config properties, image={schema.get('image', 'N/A')}")

        except Exception as e:
            raise RuntimeError(f"Failed to generate schema.json: {e}") from e
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def _find_module_name(self, src_path: Path) -> str | None:
        """Find the Python module name in the source directory."""
        # Look for directories with __init__.py
        for item in src_path.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                # Skip common non-module directories
                if item.name not in ("tests", "test", "__pycache__"):
                    return item.name

        return None

    def _get_image_url(self) -> str | None:
        """Get the ECR image URL for this agent."""
        pyproject_path = Path(self.root) / "pyproject.toml"
        if not pyproject_path.exists():
            return None

        try:
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)

            package_name = pyproject.get("project", {}).get("name", "")
            if not package_name:
                return None

            # Get the actual package version from metadata (not build target version)
            pkg_version = self.metadata.version

            # Generate ECR image URL (same pattern as agent publish)
            short_name = package_name
            for prefix in ("plato-agent-", "plato-"):
                if short_name.startswith(prefix):
                    short_name = short_name[len(prefix) :]
                    break

            return f"{ECR_REGISTRY}/vm/rootfs/plato-agents/{short_name}:{pkg_version}"
        except Exception:
            return None

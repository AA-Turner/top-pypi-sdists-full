"""Hatch build hook for Plato worlds - generates schema.json from get_schema().

Usage in world package pyproject.toml:

    [build-system]
    requires = ["hatchling", "plato-sdk-v2"]
    build-backend = "hatchling.build"

    [tool.hatch.build.hooks.custom]
    path = "plato.worlds.build_hook"

This hook will:
1. Find the .py file containing @register_world (without importing __init__.py)
2. Call its get_schema() method with the ECR image URL
3. Write schema.json to the package directory
4. Include it in the wheel

By importing only the specific file containing the world class (via
importlib.util.spec_from_file_location), we avoid triggering __init__.py
and its cascading imports. This means world packages only need their
config models and the @register_world decorator to be importable at build
time — heavy runtime deps are not required.
"""

import importlib.util
import json
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

ECR_REGISTRY = "383806609161.dkr.ecr.us-west-1.amazonaws.com"


class WorldSchemaHook(BuildHookInterface):
    """Generate schema.json during build by calling the world's get_schema()."""

    PLUGIN_NAME = "world-schema"

    def initialize(self, version: str, build_data: dict) -> None:
        """Generate schema.json before building."""
        # Find the source directory
        src_path = Path(self.root) / "src"
        if not src_path.exists():
            src_path = Path(self.root)

        # Add to path so we can import
        sys.path.insert(0, str(src_path))

        try:
            # Find the world module by looking for packages
            module_name = self._find_module_name(src_path)
            if not module_name:
                print("Warning: Could not determine module name for schema generation")
                return

            # Find and import only the specific .py file with @register_world,
            # bypassing __init__.py to avoid importing heavy runtime deps.
            world_file = self._find_world_file(src_path / module_name)
            if world_file:
                self._import_file(module_name, world_file)
            else:
                # Fallback: import the package (triggers __init__.py)
                __import__(module_name)

            # Get registered worlds
            from plato.worlds.base import _WORLD_REGISTRY

            if not _WORLD_REGISTRY:
                print(f"Warning: No worlds registered after importing {module_name}")
                return

            # Get the first registered world
            world_name, world_cls = next(iter(_WORLD_REGISTRY.items()))

            # Generate image URL from package name
            image_url = self._get_image_url()

            # Get schema with image URL
            from plato.worlds.schema import get_world_schema

            schema = get_world_schema(world_cls, image=image_url)

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
            print(f"Warning: Could not generate schema.json: {e}")
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

    @staticmethod
    def _find_world_file(package_dir: Path) -> Path | None:
        """Find the .py file containing @register_world in a package directory.

        Scans .py files (excluding __init__.py) for the decorator to avoid
        importing the entire package and its heavy dependencies.
        """
        if not package_dir.is_dir():
            return None

        for py_file in sorted(package_dir.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            try:
                content = py_file.read_text()
                if "@register_world" in content:
                    return py_file
            except Exception:
                continue

        return None

    @staticmethod
    def _import_file(package_name: str, file_path: Path) -> None:
        """Import a single .py file as a submodule without triggering __init__.py.

        Registers both the package and submodule in sys.modules so that
        intra-package imports (e.g. ``from mypackage.world import Foo``)
        resolve correctly.
        """
        import types

        # Register a minimal package stub so imports like
        # "from <package_name>.world import ..." work.
        if package_name not in sys.modules:
            pkg = types.ModuleType(package_name)
            pkg.__path__ = [str(file_path.parent)]
            pkg.__package__ = package_name
            sys.modules[package_name] = pkg

        module_name = f"{package_name}.{file_path.stem}"
        spec = importlib.util.spec_from_file_location(
            module_name,
            file_path,
            submodule_search_locations=[],
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create module spec for {file_path}")

        module = importlib.util.module_from_spec(spec)
        module.__package__ = package_name
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    def _get_image_url(self) -> str | None:
        """Get the ECR image URL for this world."""
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

            # Generate ECR image URL (same pattern as world publish)
            short_name = package_name
            for prefix in ("plato-world-", "plato-"):
                if short_name.startswith(prefix):
                    short_name = short_name[len(prefix) :]
                    break

            return f"{ECR_REGISTRY}/vm/rootfs/plato-worlds/{short_name}:{pkg_version}"
        except Exception:
            return None

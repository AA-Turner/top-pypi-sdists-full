"""Simplified tool registry for automatic tool discovery and registration."""

import importlib
import sys
import pkgutil
import os
import json
import glob
import logging
import re
from typing import Dict, Optional

# Initialize logger for this module
logger = logging.getLogger("ToolRegistry")

# Global registries
_tool_registry = {}
_config_registry = {}
_lazy_registry: Dict[str, str] = {}  # Maps tool names to module names
_discovery_completed = False
_lazy_cache = {}

# Global error tracking
_TOOL_ERRORS = {}


def _extract_missing_package(error_msg: str) -> Optional[str]:
    """Extract package name from ImportError."""
    match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_msg)
    if match:
        return match.group(1).split(".")[0]
    return None


def mark_tool_unavailable(tool_name: str, error: Exception, module: str = None):
    """Record tool failure."""
    _TOOL_ERRORS[tool_name] = {
        "error": str(error),
        "error_type": type(error).__name__,
        "module": module,
        "missing_package": _extract_missing_package(str(error)),
    }


def get_tool_errors() -> dict:
    """Get all tool errors."""
    return _TOOL_ERRORS.copy()


def register_tool(tool_type_name=None, config=None):
    """
    Decorator to automatically register tool classes and their configs.

    Usage:
        @register_tool('CustomToolName', config={...})
        class MyTool:
            pass
    """

    def decorator(cls):
        name = tool_type_name or cls.__name__
        _tool_registry[name] = cls

        if config:
            # Add MCP annotations to config if it's a dict
            if isinstance(config, dict):
                from .tool_defaults import add_annotations_to_tool_config

                # Ensure config has type field for annotation calculation
                if "type" not in config:
                    config["type"] = name
                add_annotations_to_tool_config(config)

            _config_registry[name] = config
            logger.info(f"Registered tool with config: {name}")
        else:
            logger.debug(f"Registered tool: {name} -> {cls.__name__}")

        return cls

    return decorator


def register_external_tool(tool_name, tool_class):
    """Allow external registration of tool classes."""
    _tool_registry[tool_name] = tool_class
    logger.info(f"Externally registered tool: {tool_name}")


def register_config(tool_type_name, config):
    """Register a config for a tool type."""
    # Add MCP annotations to config if it's a dict
    if isinstance(config, dict):
        from .tool_defaults import add_annotations_to_tool_config

        # Ensure config has type field for annotation calculation
        if "type" not in config:
            config["type"] = tool_type_name
        add_annotations_to_tool_config(config)

    _config_registry[tool_type_name] = config
    logger.info(f"Registered config for: {tool_type_name}")


def get_tool_registry():
    """Get a copy of the current tool registry."""
    return _tool_registry.copy()


def get_config_registry():
    """Get a copy of the current config registry."""
    return _config_registry.copy()


def lazy_import_tool(tool_name):
    """
    Lazily import a tool by name without importing all tool modules.
    Only imports the specific module containing the requested tool.
    """
    global _tool_registry, _lazy_registry, _lazy_cache  # noqa: PLW0603

    # If tool is already in registry, return it
    if tool_name in _tool_registry:
        return _tool_registry[tool_name]

    # If we have a lazy mapping for this tool, import its module
    if tool_name in _lazy_registry:
        module_name = _lazy_registry[tool_name]

        # Ensure we have the full module path
        if not module_name.startswith("tooluniverse."):
            full_module_name = f"tooluniverse.{module_name}"
        else:
            full_module_name = module_name

        # Only import if we haven't cached this module yet
        module = _lazy_cache.get(full_module_name)
        if module is None:
            try:
                logger.debug(
                    f"Lazy importing module: {full_module_name} for tool: {tool_name}"
                )
                module = importlib.import_module(full_module_name)
                _lazy_cache[full_module_name] = module
                logger.debug(f"Successfully imported module: {full_module_name}")

            except ImportError as e:
                logger.warning(f"Failed to lazy import {full_module_name}: {e}")
                mark_tool_unavailable(tool_name, e, full_module_name)
                # Remove this bad mapping so we don't try again
                del _lazy_registry[tool_name]
                return None
            except Exception as e:
                logger.warning(f"Failed to load {full_module_name}: {e}")
                mark_tool_unavailable(tool_name, e, full_module_name)
                del _lazy_registry[tool_name]
                return None

        # Check if the tool is in the registry
        if tool_name in _tool_registry:
            return _tool_registry[tool_name]

        # Fallback: Check if the tool class exists directly in the module
        # This handles cases where @register_tool("Alias") is used, but we are looking
        # for the class name itself (e.g. MonarchTool vs Monarch), which AST discovery found.
        if hasattr(module, tool_name):
            tool_class = getattr(module, tool_name)
            # Optionally cache it in registry for next time?
            # _tool_registry[tool_name] = tool_class
            return tool_class

        logger.warning(
            f"Tool {tool_name} not found in module {full_module_name} (registry or attribute)"
        )

    # If still not found after lazy loading attempt, return None
    # Don't fall back to full discovery as that defeats the purpose of lazy loading
    logger.debug(f"Tool {tool_name} not found in lazy registry")
    return None


def _discover_from_ast():
    """
    Discover tools by parsing AST of files in the package.
    Returns: Dict[tool_name, module_name]
    """
    import ast
    import tooluniverse

    mapping = {}
    try:
        package_path = tooluniverse.__path__[0]
    except (ImportError, AttributeError):
        logger.warning("Cannot import tooluniverse package for AST discovery")
        return {}

    logger.debug(f"AST scanning directory: {package_path}")

    # Directories to exclude from scanning
    EXCLUDED_DIRS = {
        "tools",
        "space",
        "data",
        "compose_scripts",
        "cache",
        "remote",
        "scripts",
        "__pycache__",
        "tests",
        "venv",
        "build",
        "dist",
        ".git",
        ".idea",
        ".vscode",
    }

    # Walk through the directory
    for root, dirs, files in os.walk(package_path):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if not file.endswith(".py"):
                continue

            # Skip known non-tool files
            if file in [
                "__init__.py",
                "main.py",
                "generate_tools.py",
                "conftest.py",
                "setup.py",
            ]:
                continue

            # Determine if this is an explicit tool file (legacy naming convention)
            is_explicit_tool_file = (
                file.endswith("_tool.py")
                or file.endswith("_tools.py")
                or file in ["compose_tool.py", "agentic_tool.py"]
            )

            file_path = os.path.join(root, file)

            # Determine module name relative to tooluniverse package
            rel_path = os.path.relpath(file_path, package_path)
            module_name = os.path.splitext(rel_path)[0].replace(os.sep, ".")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        node = ast.parse(f.read())
                        for n in node.body:
                            if isinstance(n, ast.ClassDef):
                                # Skip private classes
                                if n.name.startswith("_"):
                                    continue

                                has_registered_alias = False

                                # Check for @register_tool("Alias") decorators
                                for decorator in n.decorator_list:
                                    # We look for calls to 'register_tool'
                                    if isinstance(decorator, ast.Call):
                                        func = decorator.func
                                        # Handle @register_tool(...)
                                        is_register_tool = False
                                        if (
                                            isinstance(func, ast.Name)
                                            and func.id == "register_tool"
                                        ):
                                            is_register_tool = True
                                        elif (
                                            isinstance(func, ast.Attribute)
                                            and func.attr == "register_tool"
                                        ):
                                            is_register_tool = True

                                        if is_register_tool:
                                            # It is decorated, so we definitely want to register it
                                            has_registered_alias = True
                                            if decorator.args:
                                                # Extract the first argument as the alias
                                                arg = decorator.args[0]
                                                alias = None
                                                if isinstance(
                                                    arg, ast.Constant
                                                ):  # Python 3.8+
                                                    alias = arg.value
                                                elif isinstance(
                                                    arg, ast.Str
                                                ):  # Older Python
                                                    alias = arg.s

                                                if alias and isinstance(alias, str):
                                                    mapping[alias] = module_name

                                # Registration Logic:
                                # 1. If it has @register_tool, we register the class name.
                                # 2. If it is in an explicit tool file (*_tool.py), we register the class name (legacy behavior).
                                if has_registered_alias or is_explicit_tool_file:
                                    mapping[n.name] = module_name

                    except SyntaxError:
                        logger.warning(f"Syntax error parsing {file_path}")
            except Exception as e:
                logger.warning(f"Error reading {file_path}: {e}")

    return mapping


def build_lazy_registry(package_name=None):
    """
    Build a mapping of tool names to module names.
    Prioritizes pre-computed static registry (for bundles/frozen envs).
    Falls back to AST analysis if static registry is missing.
    """
    global _lazy_registry  # noqa: PLW0603

    if package_name is None:
        package_name = "tooluniverse"

    # 1. Try to load pre-computed static registry (for frozen environments)
    try:
        # Nuitka/PyInstaller needs to see this import to bundle it.
        # We import it here dynamically, but we should make sure the build handles it.
        # Adding explicit print for debugging in bundle.
        from tooluniverse._lazy_registry_static import STATIC_LAZY_REGISTRY

        print(
            f"DEBUG: Loaded static lazy registry with {len(STATIC_LAZY_REGISTRY)} classes.",
            file=sys.stderr,
        )
        _lazy_registry.update(STATIC_LAZY_REGISTRY)
        return _lazy_registry.copy()
    except ImportError:
        print(
            "DEBUG: No static lazy registry found. Proceeding with AST discovery.",
            file=sys.stderr,
        )

    logger.debug(f"Building lazy registry using AST for package: {package_name}")

    # 2. Use AST-based discovery as the primary source of truth (dev environment)
    ast_mappings = _discover_from_ast()

    for tool_name, module_name in ast_mappings.items():
        _lazy_registry[tool_name] = module_name

    logger.info(
        f"Built lazy registry: {len(_lazy_registry)} classes discovered via AST (no modules imported)"
    )
    return _lazy_registry.copy()


def auto_discover_tools(package_name=None, lazy=True):
    """
    Automatically discover and import all tool modules.
    If lazy=True, only builds the mapping without importing any modules.
    If lazy=False, imports all tool modules immediately.
    """
    global _discovery_completed

    if package_name is None:
        package_name = "tooluniverse"

    # In lazy mode, just build the registry without importing anything
    if lazy:
        if not _lazy_registry:
            build_lazy_registry(package_name)

            # CRITICAL FIX FOR FROZEN/BUNDLED ENVIRONMENTS:
            # If AST discovery yielded 0 results (e.g. no .py files found in Nuitka/PyInstaller bundle),
            # we MUST fallback to eager loading using pkgutil/importlib.
            # Otherwise, the server will start but have 0 tools, causing client timeouts/errors.
            if not _lazy_registry:
                logger.warning(
                    "Lazy discovery returned 0 tools (likely frozen/bundled environment). "
                    "Falling back to eager loading."
                )
                return auto_discover_tools(package_name, lazy=False)

            logger.debug(
                f"Lazy discovery complete. Registry contains {len(_lazy_registry)} tool mappings (no modules imported)"
            )
        return _lazy_registry.copy()

    # Return cached registry if full discovery already done
    if _discovery_completed:
        return _tool_registry.copy()

    try:
        package = importlib.import_module(package_name)
        package_path = package.__path__
    except (ImportError, AttributeError):
        logger.warning(f"Could not import package {package_name}")
        return _tool_registry.copy()

    logger.info(
        f"Auto-discovering tools in package: {package_name} (lazy={lazy}) - importing ALL modules"
    )

    # Import all tool modules (non-lazy mode)
    imported_count = 0
    # Use pkgutil to find modules, but rely on our AST mapping logic implicitly
    # or just iterate all modules found
    for _importer, modname, _ispkg in pkgutil.iter_modules(package_path):
        if "_tool" in modname or modname in ["compose_tool", "agentic_tool"]:
            if modname == "generate_tools":
                continue
            try:
                importlib.import_module(f"{package_name}.{modname}")
                logger.debug(f"Imported tool module: {modname}")
                imported_count += 1
            except ImportError as e:
                logger.warning(f"Could not import {modname}: {e}")

    # Also need to handle subpackages if we want full parity, but for now
    # pkgutil.iter_modules only does top level unless recursive.
    # But `auto_discover_tools` non-lazy mode was originally just iterating top-level modules.
    # The AST discovery covers subdirectories, so lazy mode is actually BETTER now.

    # Let's preserve the original behavior for non-lazy mode which seemed to utilize pkgutil
    # But wait, original code only iterated package_path, so it missed subdirectories?
    # Original code:
    # for _importer, modname, _ispkg in pkgutil.iter_modules(package_path):
    # This implies the original eager loading might have been missing tools in subdirs too!
    # But our AST discovery fixes that for lazy mode.

    _discovery_completed = True
    logger.info(
        f"Full discovery complete. Imported {imported_count} modules, registered {len(_tool_registry)} tools"
    )
    return _tool_registry.copy()


def get_tool_class_lazy(tool_name):
    """
    Get a tool class by name, using lazy loading if possible.
    Only imports the specific module needed, not all modules.
    """
    # First try lazy import
    tool_class = lazy_import_tool(tool_name)
    if tool_class:
        return tool_class

    # If lazy loading fails and we haven't done full discovery yet,
    # check if the tool exists in the current registry
    if tool_name in _tool_registry:
        return _tool_registry[tool_name]

    # As a last resort, if full discovery hasn't been done, do it
    # But this should be rare with a properly configured lazy registry
    if not _discovery_completed:
        logger.warning(
            f"Tool {tool_name} not found in lazy registry, falling back to full discovery"
        )
        auto_discover_tools(lazy=False)
        return _tool_registry.get(tool_name)

    return None

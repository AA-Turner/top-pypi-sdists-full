"""
Integration Registry - Unified interface for framework auto-instrumentation.

This module provides a clean registry pattern for enabling framework integrations,
inspired by LiteLLM's callback registry pattern.

Usage:
    import aigie

    # Enable a single integration
    aigie.patch("langchain")

    # Enable multiple integrations
    aigie.patch("langchain", "langgraph", "openai")

    # Check if an integration is available
    if aigie.is_integration_available("langgraph"):
        aigie.patch("langgraph")

    # List all available integrations
    print(aigie.list_integrations())
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class IntegrationStatus(Enum):
    """Status of an integration."""

    NOT_INSTALLED = "not_installed"  # Framework not installed
    AVAILABLE = "available"  # Ready to be patched
    PATCHED = "patched"  # Currently patched
    FAILED = "failed"  # Patch failed


@dataclass
class IntegrationInfo:
    """Information about an integration."""

    name: str
    display_name: str
    description: str
    package_name: str  # pip package name
    import_name: str | None = None  # Runtime import module name if different
    patch_function: str | None = None  # Module path to patch function
    handler_class: str | None = None  # Module path to handler class
    status: IntegrationStatus = IntegrationStatus.AVAILABLE
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    # Broad class of integration. "agent_framework" entries emit agent traces and
    # must satisfy the cross-framework span contract (single trace, root I/O,
    # priceable llm spans) — enforced by tests/unit/integrations/test_framework_contract.py.
    kind: str = "other"


# Registry of all available integrations
_INTEGRATION_REGISTRY: dict[str, IntegrationInfo] = {
    # LangChain / LangGraph
    "langchain": IntegrationInfo(
        name="langchain",
        display_name="LangChain",
        description="Trace LangChain chains, agents, and tool calls",
        package_name="langchain-core",
        patch_function="aigie.integrations.langchain.lifecycle.install_langchain_patches",
        kind="agent_framework",
        handler_class="aigie.integrations.langchain.native_callback.LangChainNativeCallback",
    ),
    "langgraph": IntegrationInfo(
        name="langgraph",
        display_name="LangGraph",
        description="Trace LangGraph stateful graph workflows",
        package_name="langgraph",
        patch_function="aigie.integrations.langgraph.lifecycle.install_langgraph_patches",
        kind="agent_framework",
        handler_class="aigie.integrations.langgraph.native_callback.LangGraphNativeCallback",
    ),
    # Agent SDKs
    "claude_agent_sdk": IntegrationInfo(
        name="claude_agent_sdk",
        display_name="Claude Agent SDK",
        description="Trace Anthropic Claude Agent SDK sessions",
        package_name="claude-agent-sdk",
        patch_function="aigie.integrations.claude_agent_sdk.lifecycle.install_claude_agent_sdk_patches",
        kind="agent_framework",
        handler_class="aigie.integrations.claude_agent_sdk.native_callback.ClaudeAgentSDKNativeCallback",
    ),
    "strands": IntegrationInfo(
        name="strands",
        display_name="Strands Agents",
        description="AWS Strands Agents SDK — agent, tool, and model tracing.",
        package_name="strands-agents",
        import_name="strands",
        patch_function="aigie.integrations.strands.lifecycle.install_strands_patches",
        kind="agent_framework",
        handler_class="aigie.integrations.strands.native_callback.StrandsHookProvider",
    ),
    # LLM Providers (direct patching)
    "openai": IntegrationInfo(
        name="openai",
        display_name="OpenAI",
        description="Auto-trace OpenAI API calls",
        package_name="openai",
        patch_function="aigie.auto_instrument.llm.patch_openai",
    ),
    "anthropic": IntegrationInfo(
        name="anthropic",
        display_name="Anthropic",
        description="Auto-trace Anthropic API calls",
        package_name="anthropic",
        patch_function="aigie.auto_instrument.llm.patch_anthropic",
    ),
    "gemini": IntegrationInfo(
        name="gemini",
        display_name="Google Gemini",
        description="Auto-trace Gemini API calls",
        package_name="google-generativeai",
        patch_function="aigie.auto_instrument.llm.patch_gemini",
    ),
    "bedrock": IntegrationInfo(
        name="bedrock",
        display_name="AWS Bedrock",
        description="Auto-trace AWS Bedrock calls",
        package_name="boto3",
        patch_function="aigie.auto_instrument.llm.patch_bedrock",
    ),
    "cohere": IntegrationInfo(
        name="cohere",
        display_name="Cohere",
        description="Auto-trace Cohere API calls",
        package_name="cohere",
        patch_function="aigie.auto_instrument.llm.patch_cohere",
    ),
}

# Track patched integrations
_patched_integrations: set[str] = set()


def _import_from_path(module_path: str) -> Any:
    """Import a function or class from a dotted path."""
    parts = module_path.rsplit(".", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid module path: {module_path}")

    module_name, attr_name = parts

    import importlib

    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


def _check_package_installed(package_name: str, import_name: str | None = None) -> bool:
    """Check if a package's runtime import is available."""
    try:
        import importlib.util

        module_name = import_name or package_name.replace("-", "_").split("[")[0]
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError):
        return False


def patch(  # noqa: PLR0915 — orchestration dispatcher over the integration registry; splitting hurts readability
    *integrations: str, ignore_errors: bool = True
) -> dict[str, bool]:
    """
    Enable auto-instrumentation for specified frameworks.

    This is the main entry point for enabling framework integrations.
    It follows the LiteLLM pattern of simple, declarative patching.

    Args:
        *integrations: Names of integrations to enable (e.g., "langchain", "openai")
        ignore_errors: If True, continue patching other integrations if one fails

    Returns:
        Dict mapping integration names to success status

    Raises:
        ValueError: If an unknown integration is specified and ignore_errors=False
        RuntimeError: If patching fails and ignore_errors=False

    Usage:
        import aigie

        # Patch single integration
        aigie.patch("langchain")

        # Patch multiple integrations
        aigie.patch("langchain", "langgraph", "openai")

        # Get results
        results = aigie.patch("langchain", "langgraph")
        if not results["langgraph"]:
            print("LangGraph not installed")
    """
    results = {}

    for name in integrations:
        # Normalize name (allow hyphens or underscores)
        normalized_name = name.lower().replace("-", "_")

        if normalized_name not in _INTEGRATION_REGISTRY:
            if ignore_errors:
                logger.warning(f"Unknown integration: {name}")
                results[name] = False
                continue
            raise ValueError(
                f"Unknown integration: {name}. Available: {', '.join(_INTEGRATION_REGISTRY.keys())}"
            )

        info = _INTEGRATION_REGISTRY[normalized_name]

        # Check if already patched
        if normalized_name in _patched_integrations:
            logger.debug(f"Integration {name} already patched")
            results[name] = True
            continue

        # Check if package is installed
        if not _check_package_installed(info.package_name, info.import_name):
            if ignore_errors:
                logger.debug(f"Package {info.package_name} not installed for {name}")
                info.status = IntegrationStatus.NOT_INSTALLED
                results[name] = False
                continue
            raise RuntimeError(
                f"Package {info.package_name} not installed. "
                f"Install with: pip install {info.package_name}"
            )

        # Patch the integration
        if info.patch_function:
            try:
                patch_fn = _import_from_path(info.patch_function)
                patch_fn()
                _patched_integrations.add(normalized_name)
                info.status = IntegrationStatus.PATCHED
                results[name] = True
                logger.info(f"Successfully patched {info.display_name}")
            except Exception as e:
                info.status = IntegrationStatus.FAILED
                info.error = str(e)
                if ignore_errors:
                    logger.warning(f"Failed to patch {name}: {e}")
                    results[name] = False
                else:
                    raise RuntimeError(f"Failed to patch {name}: {e}") from e
        else:
            logger.warning(f"No patch function for {name}")
            results[name] = False

    return results


def unpatch(*integrations: str) -> dict[str, bool]:
    """
    Disable auto-instrumentation for specified frameworks.

    Note: Not all integrations support unpatching. This will reset the
    internal state but may not fully restore original behavior.

    Args:
        *integrations: Names of integrations to disable

    Returns:
        Dict mapping integration names to success status
    """
    results = {}

    for name in integrations:
        normalized_name = name.lower().replace("-", "_")

        if normalized_name in _patched_integrations:
            _patched_integrations.discard(normalized_name)
            if normalized_name in _INTEGRATION_REGISTRY:
                _INTEGRATION_REGISTRY[normalized_name].status = IntegrationStatus.AVAILABLE
            results[name] = True
            logger.info(f"Unpatched {name}")
        else:
            results[name] = False

    return results


def is_patched(integration: str) -> bool:
    """Check if an integration is currently patched."""
    normalized_name = integration.lower().replace("-", "_")
    return normalized_name in _patched_integrations


def is_integration_available(integration: str) -> bool:
    """
    Check if an integration's package is installed and available.

    Args:
        integration: Name of the integration

    Returns:
        True if the package is installed
    """
    normalized_name = integration.lower().replace("-", "_")

    if normalized_name not in _INTEGRATION_REGISTRY:
        return False

    info = _INTEGRATION_REGISTRY[normalized_name]
    return _check_package_installed(info.package_name, info.import_name)


def get_integration_info(integration: str) -> IntegrationInfo | None:
    """Get information about an integration."""
    normalized_name = integration.lower().replace("-", "_")
    return _INTEGRATION_REGISTRY.get(normalized_name)


def list_integrations(installed_only: bool = False) -> list[IntegrationInfo]:
    """
    List all available integrations.

    Args:
        installed_only: If True, only return integrations with installed packages

    Returns:
        List of IntegrationInfo objects
    """
    integrations = list(_INTEGRATION_REGISTRY.values())

    if installed_only:
        integrations = [
            info
            for info in integrations
            if _check_package_installed(info.package_name, info.import_name)
        ]

    return integrations


def list_integration_names(installed_only: bool = False) -> list[str]:
    """
    List names of available integrations.

    Args:
        installed_only: If True, only return names of installed integrations

    Returns:
        List of integration names
    """
    return [info.name for info in list_integrations(installed_only=installed_only)]


def get_patched_integrations() -> list[str]:
    """Get list of currently patched integrations."""
    return list(_patched_integrations)


def get_handler(integration: str) -> Any:
    """
    Get the handler class for an integration.

    This is useful for manual integration or when you need direct access
    to the handler.

    Args:
        integration: Name of the integration

    Returns:
        Handler class for the integration

    Raises:
        ValueError: If integration not found or no handler defined
    """
    normalized_name = integration.lower().replace("-", "_")

    if normalized_name not in _INTEGRATION_REGISTRY:
        raise ValueError(f"Unknown integration: {integration}")

    info = _INTEGRATION_REGISTRY[normalized_name]

    if not info.handler_class:
        raise ValueError(f"No handler class defined for {integration}")

    return _import_from_path(info.handler_class)


def register_integration(
    name: str,
    display_name: str,
    description: str,
    package_name: str,
    patch_function: str | None = None,
    handler_class: str | None = None,
    metadata: dict[str, Any] | None = None,
    import_name: str | None = None,
) -> None:
    """
    Register a custom integration.

    This allows third-party packages to register their own integrations
    with the Aigie registry.

    Args:
        name: Internal name (lowercase, underscores)
        display_name: Human-readable name
        description: Description of what the integration does
        package_name: pip package name
        patch_function: Dotted path to patch function
        handler_class: Dotted path to handler class
        metadata: Additional metadata
        import_name: Runtime import module name if different from package_name

    Usage:
        aigie.register_integration(
            name="my_framework",
            display_name="My Framework",
            description="Trace My Framework workflows",
            package_name="my-framework",
            import_name="my_framework",
            patch_function="my_framework.aigie.patch_my_framework",
        )

        aigie.patch("my_framework")
    """
    _INTEGRATION_REGISTRY[name] = IntegrationInfo(
        name=name,
        display_name=display_name,
        description=description,
        package_name=package_name,
        import_name=import_name,
        patch_function=patch_function,
        handler_class=handler_class,
        metadata=metadata or {},
    )
    logger.info(f"Registered custom integration: {display_name}")


def patch_all(ignore_errors: bool = True) -> dict[str, bool]:
    """
    Patch all installed integrations.

    This is equivalent to calling patch() with all integration names
    that have their packages installed.

    Args:
        ignore_errors: If True, continue if individual patches fail

    Returns:
        Dict mapping integration names to success status
    """
    installed = list_integration_names(installed_only=True)
    return patch(*installed, ignore_errors=ignore_errors)


# Convenience aliases
enable = patch
disable = unpatch

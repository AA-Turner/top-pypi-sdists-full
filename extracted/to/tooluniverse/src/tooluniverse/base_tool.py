from .utils import extract_function_call_json, evaluate_function_call
from .exceptions import (
    ToolError,
    ToolValidationError,
    ToolAuthError,
    ToolRateLimitError,
    ToolUnavailableError,
    ToolConfigError,
    ToolDependencyError,
    ToolServerError,
)
import json
from pathlib import Path
from typing import no_type_check, Optional, Dict, Any
import hashlib
import inspect


class BaseTool:
    STATIC_CACHE_VERSION = "1"

    def __init__(self, tool_config):
        self.tool_config = self._apply_defaults(tool_config)
        self._cached_version_hash: Optional[str] = None

    @classmethod
    def get_default_config_file(cls):
        """
        Get the path to the default configuration file for this tool type.

        This method uses a robust path resolution strategy that works across
        different installation scenarios:

        1. Installed packages: Uses importlib.resources for proper package
           resource access
        2. Development mode: Falls back to file-based path resolution
        3. Legacy Python: Handles importlib.resources and importlib_resources

        Override this method in subclasses to specify a custom defaults file.

        Returns
            Path or resource object pointing to the defaults file
        """
        tool_type = cls.__name__

        # Use importlib.resources for robust path resolution across different
        # installation methods
        try:
            import importlib.resources as pkg_resources
        except ImportError:
            # Fallback for Python < 3.9
            import importlib_resources as pkg_resources

        try:
            # Try to use package resources first (works with installed
            # packages). Use the newer files() API
            data_files = pkg_resources.files("tooluniverse.data")
            defaults_file = data_files / f"{tool_type.lower()}_defaults.json"

            # For compatibility, convert to a regular Path if possible
            if hasattr(defaults_file, "resolve"):
                return defaults_file.resolve()
            else:
                # For older Python versions or special cases, return resource
                # path
                return defaults_file

        except (FileNotFoundError, ModuleNotFoundError, AttributeError):
            # Fallback to file-based path resolution for development/local use
            current_dir = Path(__file__).parent
            defaults_file = current_dir / "data" / f"{tool_type.lower()}_defaults.json"
            return defaults_file

    @classmethod
    def load_defaults_from_file(cls):
        """Load defaults from the configuration file"""
        defaults_file = cls.get_default_config_file()

        # Handle both regular Path objects and importlib resource objects
        try:
            # Check if it's a regular Path object
            if hasattr(defaults_file, "exists") and not defaults_file.exists():
                return {}

            # Try to read the file (works for both Path and resource objects)
            if hasattr(defaults_file, "read_text"):
                # Resource object with read_text method
                content = defaults_file.read_text(encoding="utf-8")
                data = json.loads(content)
            else:
                # Regular file path
                with open(defaults_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

            # Look for defaults under the tool type key
            tool_type = cls.__name__
            return data.get(f"{tool_type.lower()}_defaults", {})

        except (FileNotFoundError, json.JSONDecodeError):
            # File doesn't exist or invalid JSON, return empty defaults
            return {}
        except Exception as e:
            print(f"Warning: Could not load defaults for {cls.__name__}: {e}")
            return {}

    def _apply_defaults(self, tool_config):
        """Apply default configuration to the tool config"""
        # Load defaults from file
        defaults = self.load_defaults_from_file()

        if not defaults:
            # No defaults available, return original config
            return tool_config

        # Create merged configuration by starting with defaults
        merged_config = defaults.copy()

        # Override with tool-specific configuration
        merged_config.update(tool_config)

        return merged_config

    @no_type_check
    def run(self, arguments=None, stream_callback=None, use_cache=False, validate=True):
        """Execute the tool.

        The default BaseTool implementation accepts an optional arguments
        mapping to align with most concrete tool implementations which expect
        a dictionary of inputs.

        Args:
            arguments (dict, optional): Tool-specific arguments
            stream_callback (callable, optional): Callback for streaming responses
            use_cache (bool, optional): Whether result caching is enabled
            validate (bool, optional): Whether parameter validation was performed

        Note:
            These additional parameters (stream_callback, use_cache, validate) are
            passed from run_one_function() to provide context about the execution.
            Tools can use these for optimization or special handling.

            For backward compatibility, tools that don't accept these parameters
            will still work - they will only receive the arguments parameter.
        """

    def check_function_call(self, function_call_json):
        if isinstance(function_call_json, str):
            function_call_json = extract_function_call_json(function_call_json)
        if function_call_json is not None:
            return evaluate_function_call(self.tool_config, function_call_json)
        else:
            return False, "Invalid JSON string of function call"

    def get_required_parameters(self):
        """
        Retrieve required parameters from the endpoint definition.
        Returns
        list: List of required parameters for the given endpoint.
        """
        schema = self.tool_config.get("parameter", {})
        required_params = schema.get("required", [])
        return required_params

    def validate_parameters(self, arguments: Dict[str, Any]) -> Optional[ToolError]:
        """
        Validate parameters against tool schema.

        This method provides standard parameter validation using jsonschema.
        Subclasses can override this method to implement custom validation
        logic.

        Args:
            arguments: Dictionary of arguments to validate

        Returns
            ToolError if validation fails, None if validation passes
        """
        schema = self.tool_config.get("parameter", {})

        if not schema:
            return None  # No schema to validate against

        try:
            import jsonschema
        except ImportError:
            # jsonschema not available, skip validation
            return None

        try:
            # Filter out internal control parameters before validation
            # Only filter known internal parameters, not all underscore-prefixed params
            # to allow optional streaming parameter _tooluniverse_stream
            internal_params = {"ctx", "_tooluniverse_stream"}
            filtered_arguments = {
                k: v for k, v in arguments.items() if k not in internal_params
            }

            jsonschema.validate(filtered_arguments, schema)
            return None
        except jsonschema.ValidationError as e:
            # Create a more agent-friendly error message
            error_msg = f"Parameter validation failed for '{e.path[-1] if e.path else 'root'}': {e.message}"

            # Add type hint if it's a type error
            if e.validator == "type":
                error_msg += (
                    f". Expected {e.validator_value}, got {type(e.instance).__name__}."
                )

            # Add allowed values if it's an enum error
            if e.validator == "enum":
                error_msg += f". Allowed values: {e.validator_value}."

            return ToolValidationError(
                error_msg,
                details={
                    "validation_error": str(e),
                    "path": list(e.absolute_path) if e.absolute_path else [],
                    "schema": schema,
                    "parameter": str(e.path[-1]) if e.path else "root",
                    "expected": str(e.validator_value)
                    if hasattr(e, "validator_value")
                    else None,
                },
            )
        except Exception as e:
            return ToolValidationError(f"Validation error: {str(e)}")

    def handle_error(self, exception: Exception) -> ToolError:
        """
        Classify a raw exception into a structured ToolError.

        This method provides standard error classification. Subclasses can
        override this method to implement custom error handling logic.

        Args:
            exception: The raw exception to classify

        Returns
            Structured ToolError instance
        """
        error_str = str(exception).lower()

        if any(
            keyword in error_str
            for keyword in ["auth", "unauthorized", "401", "403", "api key", "token"]
        ):
            return ToolAuthError(f"Authentication failed: {exception}")
        elif any(
            keyword in error_str
            for keyword in ["rate limit", "429", "quota", "limit exceeded"]
        ):
            return ToolRateLimitError(f"Rate limit exceeded: {exception}")
        elif any(
            keyword in error_str
            for keyword in [
                "unavailable",
                "timeout",
                "connection",
                "network",
                "not found",
                "404",
            ]
        ):
            return ToolUnavailableError(f"Tool unavailable: {exception}")
        elif any(
            keyword in error_str
            for keyword in ["validation", "invalid", "schema", "parameter"]
        ):
            return ToolValidationError(f"Validation error: {exception}")
        elif any(
            keyword in error_str for keyword in ["config", "configuration", "setup"]
        ):
            return ToolConfigError(f"Configuration error: {exception}")
        elif any(
            keyword in error_str
            for keyword in ["import", "module", "dependency", "package"]
        ):
            return ToolDependencyError(f"Dependency error: {exception}")
        else:
            return ToolServerError(f"Unexpected error: {exception}")

    def get_cache_key(self, arguments: Dict[str, Any]) -> str:
        """
        Generate a cache key for this tool call.

        This method provides standard cache key generation. Subclasses can
        override this method to implement custom caching logic.

        Args:
            arguments: Dictionary of arguments for the tool call

        Returns
            String cache key
        """
        # Include tool name and arguments in cache key
        cache_data = {
            "tool_name": self.tool_config.get("name", self.__class__.__name__),
            "arguments": arguments,
        }
        serialized = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(serialized.encode()).hexdigest()

    def supports_streaming(self) -> bool:
        """
        Check if this tool supports streaming responses.

        Returns
            True if tool supports streaming, False otherwise
        """
        return self.tool_config.get("supports_streaming", False)

    def supports_caching(self) -> bool:
        """
        Check if this tool's results can be cached.

        Returns
            True if tool results can be cached, False otherwise
        """
        return self.tool_config.get("cacheable", True)

    def get_batch_concurrency_limit(self) -> int:
        """Return maximum concurrent executions allowed during batch runs (0 = unlimited)."""
        limit = self.tool_config.get("batch_max_concurrency")
        if limit is None:
            return 0
        try:
            parsed = int(limit)
        except (TypeError, ValueError):
            return 0
        return max(0, parsed)

    def get_cache_namespace(self) -> str:
        """Return cache namespace identifier for this tool."""
        return self.tool_config.get("name", self.__class__.__name__)

    def get_cache_version(self) -> str:
        """Return a stable cache version fingerprint for this tool."""
        if self._cached_version_hash:
            return self._cached_version_hash

        hasher = hashlib.sha256()
        hasher.update(self.STATIC_CACHE_VERSION.encode("utf-8"))

        try:
            source = inspect.getsource(self.__class__)
            hasher.update(source.encode("utf-8"))
        except (OSError, TypeError):
            pass

        try:
            schema = json.dumps(self.tool_config.get("parameter", {}), sort_keys=True)
            hasher.update(schema.encode("utf-8"))
        except (TypeError, ValueError):
            pass

        self._cached_version_hash = hasher.hexdigest()[:16]
        return self._cached_version_hash

    def get_cache_ttl(self, result: Any = None) -> Optional[int]:
        """Return TTL (seconds) for cached results; None means no expiration."""
        ttl = self.tool_config.get("cache_ttl")
        return int(ttl) if ttl is not None else None

    def get_tool_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about this tool.

        Returns
            Dictionary containing tool metadata
        """
        return {
            "name": self.tool_config.get("name", self.__class__.__name__),
            "description": self.tool_config.get("description", ""),
            "supports_streaming": self.supports_streaming(),
            "supports_caching": self.supports_caching(),
            "required_parameters": self.get_required_parameters(),
            "parameter_schema": self.tool_config.get("parameter", {}),
            "tool_type": self.__class__.__name__,
        }

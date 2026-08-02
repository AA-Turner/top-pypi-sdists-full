"""Type stubs for the json_tools_rs native extension module."""

from typing import Any, Optional, Sequence, Union

class JsonToolsError(Exception):
    """Exception raised by JSON Tools operations."""

    ...

class JsonOutput:
    """Wrapper for JSON processing results (single or multiple)."""

    @property
    def is_single(self) -> bool:
        """True if this contains a single result."""
        ...

    @property
    def is_multiple(self) -> bool:
        """True if this contains multiple results."""
        ...

    def get_single(self) -> str:
        """Get the single result string. Raises ValueError if multiple."""
        ...

    def get_multiple(self) -> list[str]:
        """Get the multiple result strings. Raises ValueError if single."""
        ...

    def to_python(self) -> Union[str, list[str]]:
        """Get the result as a native Python object."""
        ...

class JSONTools:
    """High-performance JSON flattening/unflattening with builder pattern API.

    Supports str, dict, list[str], list[dict], DataFrame, and Series inputs.
    Output type matches input type automatically.

    Example::

        import json_tools_rs
        result = json_tools_rs.JSONTools().flatten().execute({"a": {"b": 1}})
        # result == {"a.b": 1}
    """

    def __init__(self) -> None: ...
    def flatten(self) -> "JSONTools":
        """Set operation mode to flatten nested JSON into dot-separated keys."""
        ...

    def unflatten(self) -> "JSONTools":
        """Set operation mode to unflatten dot-separated keys back into nested JSON."""
        ...

    def normal(self) -> "JSONTools":
        """Set operation mode to normal (apply transformations without flatten/unflatten)."""
        ...

    def separator(self, separator: str) -> "JSONTools":
        """Set the separator for nested keys (default: '.')."""
        ...

    def lowercase_keys(self, value: bool) -> "JSONTools":
        """Enable or disable lowercase key conversion."""
        ...

    def remove_empty_strings(self, value: bool) -> "JSONTools":
        """Enable or disable removal of keys with empty string values."""
        ...

    def remove_nulls(self, value: bool) -> "JSONTools":
        """Enable or disable removal of keys with null values."""
        ...

    def remove_empty_objects(self, value: bool) -> "JSONTools":
        """Enable or disable removal of keys with empty object values ({})."""
        ...

    def remove_empty_arrays(self, value: bool) -> "JSONTools":
        """Enable or disable removal of keys with empty array values ([])."""
        ...

    def key_replacement(self, find: str, replace: str) -> "JSONTools":
        """Add a key replacement pattern. Literal (exact substring) by default; wrap in r'...' for regex."""
        ...

    def value_replacement(self, find: str, replace: str) -> "JSONTools":
        """Add a value replacement pattern. Literal (exact substring) by default; wrap in r'...' for regex."""
        ...

    def exclude_key(self, pattern: str) -> "JSONTools":
        """Exclude any key (and its entire subtree) whose name contains pattern. Literal by default; wrap in r'...' for regex. Additive."""
        ...

    def exclude_value(self, pattern: str) -> "JSONTools":
        """Drop a key-value pair whose value contains pattern. Literal by default; wrap in r'...' for regex. Additive. Scalar leaf values only."""
        ...

    def handle_key_collision(self, value: bool) -> "JSONTools":
        """Enable collision handling by collecting duplicate keys into arrays."""
        ...

    def always_array_keys(self, keys: Sequence[str]) -> "JSONTools":
        """Flattened key names that must always render as an array, even with only one value -- keeps a key's shape consistent across documents/rows regardless of handle_key_collision. Matched against the final flattened key name."""
        ...

    def auto_convert_types(self, enable: bool) -> "JSONTools":
        """Enable automatic type conversion from strings to numbers and booleans."""
        ...

    def parallel_threshold(self, threshold: int) -> "JSONTools":
        """Set the minimum batch size for parallel processing."""
        ...

    def num_threads(self, num_threads: Optional[int]) -> "JSONTools":
        """Configure the number of threads for parallel processing."""
        ...

    def nested_parallel_threshold(self, threshold: int) -> "JSONTools":
        """Configure the threshold for nested parallel processing."""
        ...

    def max_array_index(self, max: int) -> "JSONTools":
        """Set the maximum array index allowed during unflattening (DoS protection)."""
        ...

    def execute(
        self,
        json_input: Any,
        normalise: bool = False,
        target: Optional[str] = None,
    ) -> Any:
        """Execute the configured JSON operation.

        Args:
            json_input: JSON input as str, dict, list[str], list[dict],
                DataFrame (pandas/polars/pyarrow/pyspark), or
                Series (pandas/polars/pyarrow).
            normalise: If True, always return a wide/tabular DataFrame (one
                column per flattened key) regardless of input shape -- a bare
                str/dict becomes a 1-row DataFrame. Requires `.flatten()` mode.
                Default False leaves all existing behavior unchanged.
            target: DataFrame library to use when normalise=True: "pandas",
                "polars", "pyarrow", or "pyspark". If omitted: uses the
                input's own backend when input is itself a live
                DataFrame/Series, otherwise tries pandas -> polars -> pyarrow
                (first installed wins; pyspark is never auto-selected for
                bare JSON input -- pass target="pyspark" explicitly, which
                requires an active SparkSession). Only meaningful when
                normalise=True.

        Returns:
            Output type matches input type when normalise=False (unchanged).
            When normalise=True, always a DataFrame of the resolved target type.

        Raises:
            JsonToolsError: If operation mode is not set or processing fails;
                if normalise=True but mode is not `.flatten()`; if target is
                passed without normalise=True; if target names an unknown
                library or one that isn't installed; or (target="pyspark")
                if no active SparkSession is found.
        """
        ...

    def execute_to_output(self, json_input: Any) -> JsonOutput:
        """Execute and return a JsonOutput wrapper instead of auto-detecting type."""
        ...

    def to_config_json(self) -> str:
        """Serialize this instance's configuration to a JSON string.

        Pairs with `from_config_json` to rebuild an equivalent, independent
        instance elsewhere -- e.g. inside a PySpark `mapInPandas` partition
        function, which should close over this string (not the instance
        itself) and call `from_config_json` fresh per partition. Also the
        mechanism behind this class's pickle support.
        """
        ...

    @staticmethod
    def from_config_json(config_json: str) -> "JSONTools":
        """Reconstruct a JSONTools instance from a `to_config_json()` string."""
        ...

    def __reduce__(self) -> Any:
        """Pickle support (also enables cloudpickle-based closure capture,
        e.g. inside a PySpark UDF), via the to_config_json/from_config_json
        round trip."""
        ...

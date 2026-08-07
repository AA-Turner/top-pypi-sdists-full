"""
JSON Tools RS - High-performance JSON manipulation library

This package provides Python bindings for the JSON Tools RS library,
offering high-performance JSON flattening and unflattening with SIMD-accelerated
parsing and Rayon-based parallelism.

The main entry point is the JSONTools class, which provides a unified builder pattern API
for all JSON manipulation operations with advanced collision handling and filtering.

Perfect Type Matching - Input type = Output type:
    - str input → str output (JSON string)
    - dict input → dict output (Python dictionary)
    - list[str] input → list[str] output (list of JSON strings)
    - list[dict] input → list[dict] output (list of Python dictionaries)
    - DataFrame input → DataFrame output (Pandas, Polars, PyArrow, PySpark)
    - Series input → Series output (Pandas, Polars, PyArrow)
    - Mixed lists preserve original types

Basic Usage:
    >>> import json_tools_rs
    >>>
    >>> # Basic flattening
    >>> tools = json_tools_rs.JSONTools().flatten()
    >>> result = tools.execute({"user": {"name": "John", "age": 30}})
    >>> print(result)  # {'user.name': 'John', 'user.age': 30} (dict)
    >>>
    >>> # Basic unflattening
    >>> tools = json_tools_rs.JSONTools().unflatten()
    >>> result = tools.execute({"user.name": "John", "user.age": 30})
    >>> print(result)  # {'user': {'name': 'John', 'age': 30}} (dict)

Advanced Features:
    >>> # Collision handling with filtering
    >>> tools = (json_tools_rs.JSONTools()
    ...     .flatten()
    ...     .separator("::")
    ...     .remove_empty_strings(True)
    ...     .remove_nulls(True)
    ...     .key_replacement("r'(User|Admin)_'", "")  # Wrap in r'...' for regex
    ...     .handle_key_collision(True))
    >>>
    >>> data = {"User_name": "John", "Admin_name": "", "Guest_name": "Bob"}
    >>> result = tools.execute(data)
    >>> print(result)  # {"name": ["John", "Bob"], "guest_name": "Bob"}

Batch Processing:
    >>> # Perfect type preservation in batch processing
    >>> tools = json_tools_rs.JSONTools().flatten()
    >>> str_results = tools.execute(['{"a": 1}', '{"b": 2}'])
    >>> print(str_results)  # ['{"a": 1}', '{"b": 2}'] (list of strings)
    >>>
    >>> dict_results = tools.execute([{"a": {"b": 1}}, {"c": {"d": 2}}])
    >>> print(dict_results)  # [{'a.b': 1}, {'c.d': 2}] (list of dicts)

Automatic Type Conversion:
    >>> # Convert strings to numbers and booleans automatically
    >>> tools = json_tools_rs.JSONTools().flatten().auto_convert_types(True)
    >>> data = {"id": "123", "price": "$1,234.56", "active": "true"}
    >>> result = tools.execute(data)
    >>> print(result)  # {'id': 123, 'price': 1234.56, 'active': True}

DataFrame & Series Support:
    >>> # Pandas DataFrame input → Pandas DataFrame output
    >>> import pandas as pd
    >>> df = pd.DataFrame([{"user": {"name": "Alice"}}, {"user": {"name": "Bob"}}])
    >>> tools = json_tools_rs.JSONTools().flatten()
    >>> result = tools.execute(df)  # Returns a Pandas DataFrame
    >>>
    >>> # Also works with Polars, PyArrow Tables, and PySpark DataFrames
    >>> # Series input → Series output for Pandas, Polars, and PyArrow

Parallel Processing (Automatic):
    >>> # Automatic parallel processing for large batches (10+ items by default)
    >>> large_batch = [{"data": i} for i in range(2000)]
    >>> tools = json_tools_rs.JSONTools().flatten()
    >>> results = tools.execute(large_batch)  # Automatically uses parallel processing
    >>>
    >>> # Configure parallel processing thresholds
    >>> tools = (json_tools_rs.JSONTools()
    ...     .flatten()
    ...     .parallel_threshold(50)  # Only parallelize batches of 50+ items
    ...     .num_threads(4)  # Limit to 4 threads
    ...     .nested_parallel_threshold(200))  # Parallelize large nested structures
"""

from .json_tools_rs import JsonOutput, JSONTools, JsonToolsError

__version__ = "0.9.28"
__author__ = "JSON Tools RS Contributors"

__all__ = [
    "JSONTools",
    "JsonOutput",
    "JsonToolsError",
]

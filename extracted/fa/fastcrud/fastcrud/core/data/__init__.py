"""
Data processing module with clean dependency hierarchy.

This module contains all data transformation, nesting, and formatting utilities
organized by dependency level:

Level 2: transforms.py - Pure functions with no external dependencies
Level 3: nesting.py - Functions that depend on introspection utilities
Level 4: formatting.py - High-level response formatting with join processing

All functions are re-exported here for backward compatibility.
"""

from .transforms import (
    handle_one_to_one,
    handle_one_to_many,
    sort_nested_list,
    build_column_label,
    format_single_response,
    format_multi_response,
    create_paginated_response_data,
    convert_to_pydantic_models,
)

from .nesting import (
    nest_join_data,
    get_nested_key_for_join,
    process_joined_field,
    process_data_fields,
    cleanup_null_joins,
)

from .formatting import (
    process_joined_data,
    format_joined_response,
)

__all__ = [
    # Data transformation functions
    "handle_one_to_one",
    "handle_one_to_many",
    "sort_nested_list",
    "build_column_label",
    "format_single_response",
    "format_multi_response",
    "create_paginated_response_data",
    "convert_to_pydantic_models",
    # Data nesting functions
    "nest_join_data",
    "get_nested_key_for_join",
    "process_joined_field",
    "process_data_fields",
    "cleanup_null_joins",
    # Response formatting functions
    "process_joined_data",
    "format_joined_response",
]

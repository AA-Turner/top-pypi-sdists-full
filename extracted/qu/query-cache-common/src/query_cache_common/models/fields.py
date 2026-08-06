from __future__ import annotations

import typing as t
from dataclasses import field


def transformed_nodes_by_query_field() -> t.Any:
    """
    Create a field for transformed_nodes_by_query with proto converter metadata.

    This field represents a nested dictionary structure:
    - Outer key: query identifier (str)
    - Inner dict: mapping of node names to function names (str -> str)

    The field includes custom proto converters that handle the protobuf
    MessageMap[str, NodeFuncMapping] <-> Dict[str, Dict[str, str]] conversion.
    """
    from query_cache_common.models import converters

    return field(
        default_factory=dict,
        metadata={
            "proto_converter": {
                "from_proto": converters.transformed_nodes_by_query_from_proto,
                "to_proto": converters.transformed_nodes_by_query_to_proto,
            }
        },
    )

"""Trace data structures and processing.

This module provides a structured way to work with Kolo traces,
similar to the TypeScript implementation in vscode/src/trace.ts.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Generator, List, Optional

from .build_frame_tree import ExecutionTreeInfo, build_execution_tree
from .node import ProcessedNode, make_processed_node
from .utils import pretty_byte_size, relative_time


class ProcessedTree:
    """Represents a processed execution tree for a set of frames.

    Similar to TypeScript's ProcessedTree class, this wraps the basic
    execution tree with additional functionality like DFS traversal
    and node lookup.
    """

    def __init__(self, frames_of_interest: List[Dict[str, Any]], trace_id: str):
        """Build a processed tree from frames of interest.

        Args:
            frames_of_interest: List of frame dictionaries to process
            trace_id: The trace ID these frames belong to
        """
        self.trace_id = trace_id
        self.basic_execution_tree: ExecutionTreeInfo = build_execution_tree(
            frames_of_interest
        )
        self.root_nodes: List[ProcessedNode] = [
            make_processed_node(node, None, trace_id)
            for node in self.basic_execution_tree.execution_tree_nodes
        ]
        self.total_execution_tree_node_count = (
            self.basic_execution_tree.total_execution_tree_node_count
        )

    def dfs(self) -> Generator[ProcessedNode, None, None]:
        """Depth-first traversal of all nodes in the tree."""
        for root_node in self.root_nodes:
            yield from root_node.dfs()

    def find_node_by_index(self, index: int) -> Optional[ProcessedNode]:
        """Find a node by its index.

        Args:
            index: The node index to find

        Returns:
            The ProcessedNode with the given index, or None if not found
        """
        for node in self.dfs():
            if node.index == index:
                return node
        return None


class Trace:
    """Represents a processed Kolo trace.

    Similar to TypeScript's ProcessedTrace class, this wraps the raw
    trace data and provides convenient access to the execution tree
    and other trace metadata.
    """

    def __init__(self, unprocessed_data: Dict[str, Any], size: int):
        """Create a processed trace from raw trace data.

        Args:
            unprocessed_data: The raw deserialized trace data (msgpack)
        """
        self.unprocessed_data = unprocessed_data
        self.id: str = unprocessed_data["trace_id"]
        self.timestamp: float = unprocessed_data["timestamp"]
        self.dt_utc = datetime.fromtimestamp(self.timestamp, tz=timezone.utc)
        self.size = size

        # The "main" tree which for now is the tree of frames
        #  from the thread that was active when kolo was enabled
        main_frames = self.get_main_frames_of_interest(unprocessed_data)
        self.main_tree = ProcessedTree(main_frames, self.id)

        # TODO: Support and display multiple threads in output!
        self.threads: List[ProcessedTree] = []

    @property
    def name(self) -> str:
        """Get a human-readable name for this trace."""
        # Use explicit trace name if available
        trace_name = self.unprocessed_data.get("trace_name")
        if trace_name:
            return trace_name

        # Generate name from root node
        if self.main_tree.root_nodes:
            first_node = self.main_tree.root_nodes[0]
            other_calls = self.main_tree.total_execution_tree_node_count - 1
            if other_calls > 0:
                return f"{first_node.name} (+{other_calls} calls)"
            return first_node.name

        # Fallback for empty traces - use command_line_args if available
        command_line_args = self.unprocessed_data.get("command_line_args", [])
        if command_line_args:
            # Use the script name (first arg) as the name
            script_name = command_line_args[0]
            source = self.unprocessed_data.get("meta", {}).get("source", "")
            return f"{script_name} (empty, {source})"

        # Final fallback to trace ID
        return self.id

    @staticmethod
    def get_main_frames_of_interest(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract the main frames of interest from trace data.

        Handles both old and new trace formats:
        - Old format: frames_of_interest at top level
        - New format: frames in threads, using current_thread_id

        Returns:
            Flat list of frames from the main thread
        """
        # Check if this is an old trace without config/threads
        meta = data.get("meta", {})
        config = meta.get("config")

        if not config:
            # Old traces just have frames_of_interest at the top level
            return data.get("frames_of_interest", [])

        # New format with threads
        threads = data.get("threads", {})
        if threads and len(threads) > 0:
            current_thread_id = data.get("current_thread_id")
            if not current_thread_id:
                raise ValueError("threads present but no current_thread_id")

            thread = threads.get(current_thread_id)
            if thread:
                return thread.get("frames", [])
            else:
                # We have a current thread id, but no frames captured yet
                return []

        # Fallback to old format
        return data.get("frames_of_interest", [])

    @staticmethod
    def resolve_display_name(
        msgpack_data: bytes,
        auto_generated_name: Optional[str],
        db_path: Path,
        trace_id: str,
    ) -> Optional[str]:
        """Resolve the display name for a trace.

        Uses fast path when auto_generated_name is available, otherwise
        falls back to lazy migration with full deserialization.

        Args:
            msgpack_data: The raw msgpack trace data
            auto_generated_name: Precomputed auto-generated name (may be None)
            db_path: Database path for lazy migration (optional)
            trace_id: Trace ID for lazy migration (optional)

        Returns:
            The resolved display name, or None if it couldn't be determined
        """
        from .db import (
            extract_trace_name_fast,
            update_auto_generated_name,
        )
        from .serialize import load_msgpack

        if not msgpack_data:
            # legacy traces pre msgpack
            return None

        if auto_generated_name:
            # Fast path: use fast extraction to check for user-specified name
            user_name = extract_trace_name_fast(msgpack_data)
            return user_name if user_name else auto_generated_name
        else:
            # Lazy migration: full deserialization needed
            data = load_msgpack(msgpack_data)
            if isinstance(data, dict):
                user_name = data.get("trace_name")
                if user_name:
                    return user_name
                else:
                    # Build trace to get the name
                    trace = Trace(unprocessed_data=data, size=len(msgpack_data))
                    update_auto_generated_name(db_path, trace_id, trace.name)
                    return trace.name
        return None

    def compact(self, include_return_value: bool = False) -> str:
        """Generate compact text representation of the trace."""

        header = f"""=== Kolo Trace {self.id} ===
{self.name}
{relative_time(self.dt_utc)}, {pretty_byte_size(self.size)}
source: {self.unprocessed_data.get("meta", {}).get("source", "unknown")} (kolo v{self.unprocessed_data.get("meta", {}).get("version", "unknown")})
config: {self.unprocessed_data.get("meta", {}).get("config", {})}
Python: {self.unprocessed_data.get("meta", {}).get("environment", {}).get("py_version", "unknown")}

format: node_idx, type, qualname, start_to_end_loc, duration
"""

        # todo: on the config, keep just the stuff that is not default.

        if include_return_value:
            header += """  ↪ input value 
  ↩ return value
"""

        guidance = """\nguidance:
- `kolo run myprogram.py` - run with kolo enabled or capture in another way: docs.kolo.app/capture
- `kolo trace list` - list recent kolo traces
- `kolo cat TRACE_ID` - show trace output. run with `--returns` to include input and return values
- `kolo trace node TRACE_ID NODE_INDEX` - get the FULL details of a specific node, incl locals
"""

        header += guidance + "\n"
        lines = []
        for node in self.main_tree.dfs():
            lines.append(node.full_compact_tree_line(include_return_value))

        return header + "=== Trace ===\n" + "\n".join(lines)

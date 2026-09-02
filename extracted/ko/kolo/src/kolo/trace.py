"""Trace data structures and processing.

This module provides a structured way to work with Kolo traces,
similar to the TypeScript implementation in vscode/src/trace.ts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Generator, List, Optional

from .build_frame_tree import ExecutionTreeInfo, build_execution_tree
from .node import ProcessedNode, make_processed_node
from .utils import pretty_byte_size, relative_time


@dataclass
class ThreadSection:
    """A single thread's processed tree plus its identifying metadata.

    Used by ``Trace`` to carry all threads through the rendering pipeline
    so compact/emit output can show frames from every thread, not just the
    one that was active when profiling started.
    """

    thread_id: str
    name: str
    tree: "ProcessedTree"
    is_main: bool

    @property
    def label(self) -> str:
        parts = [f"Thread {self.name}" if self.name else f"Thread {self.thread_id}"]
        if self.name and self.name != self.thread_id:
            parts.append(f"(id={self.thread_id})")
        if self.is_main:
            parts.append("(main)")
        return " ".join(parts)


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

        # Build frame_id -> node index for O(1) lookups
        self._frame_id_index: Dict[str, ProcessedNode] = {}
        self._build_frame_id_index()

        # Set sibling metadata on root nodes
        for i, root in enumerate(self.root_nodes):
            root._sibling_index = i
            root._tree_root_nodes = self.root_nodes

    def _build_frame_id_index(self) -> None:
        """Build the frame_id to node index."""
        for node in self.dfs():
            self._frame_id_index[node.frame_id] = node

    def find_node_by_frame_id(self, frame_id: str) -> Optional[ProcessedNode]:
        """Find a node by its frame_id in O(1) time.

        Args:
            frame_id: The frame_id to search for

        Returns:
            The ProcessedNode with the given frame_id, or None if not found
        """
        return self._frame_id_index.get(frame_id)

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
        self.recovered = bool(unprocessed_data.get("recovered"))

        # The "main" tree is the tree of frames from the thread that was
        # active when kolo was enabled. It is kept as a separate attribute
        # for backwards-compat and because some callers (folder naming,
        # HTTP/test detection) specifically want the originating thread.
        main_frames = self.get_main_frames_of_interest(unprocessed_data)
        self.main_tree = ProcessedTree(main_frames, self.id)

        # Non-main-thread ``ProcessedTree`` construction is deferred until
        # first access. Metadata-only callers (trace listing, name
        # resolution) never look at ``self.threads`` so they should not
        # pay the cost of building every worker's tree. Rendering callers
        # share this cache instead of rebuilding the same worker trees.
        self._threads_cache: Optional[List[ThreadSection]] = None

    @property
    def threads(self) -> List[ThreadSection]:
        """Lazy-constructed list of thread sections, main first.

        Each non-main thread's ``ProcessedTree`` is built on first
        access and cached, so metadata-only consumers don't pay the
        multi-thread tree-building cost. Always returns at least the
        main section when the main tree has root nodes.
        """
        if self._threads_cache is None:
            self._threads_cache = self._build_thread_sections(self.unprocessed_data)
        return self._threads_cache

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

    def _build_thread_sections(self, data: Dict[str, Any]) -> List[ThreadSection]:
        """Build the ordered list of thread sections for this trace.

        The main thread (whichever thread was active when profiling
        started) always comes first and reuses ``self.main_tree`` so we
        don't rebuild the same tree twice. Other threads follow, sorted
        by their earliest frame timestamp so output order matches
        execution order.

        For old-format traces that only have ``frames_of_interest`` (no
        ``threads`` dict), only the main section is returned.
        """
        threads = data.get("threads", {}) or {}
        current_thread_id = data.get("current_thread_id")

        main_thread_name = ""
        if current_thread_id and current_thread_id in threads:
            main_thread_name = threads[current_thread_id].get("name", "") or ""

        sections: List[ThreadSection] = [
            ThreadSection(
                thread_id=current_thread_id or "main",
                name=main_thread_name or (current_thread_id or "main"),
                tree=self.main_tree,
                is_main=True,
            )
        ]

        if not threads:
            return sections

        other_sections: List[ThreadSection] = []
        for thread_id, thread_data in threads.items():
            if thread_id == current_thread_id:
                continue
            frames = thread_data.get("frames", []) if thread_data else []
            if not frames:
                continue
            tree = ProcessedTree(frames, self.id)
            name = (thread_data.get("name") if thread_data else "") or thread_id
            other_sections.append(
                ThreadSection(
                    thread_id=thread_id,
                    name=name,
                    tree=tree,
                    is_main=False,
                )
            )

        def earliest_timestamp(section: ThreadSection) -> float:
            timestamps = [
                n.start for n in section.tree.root_nodes if n.start is not None
            ]
            return min(timestamps) if timestamps else float("inf")

        other_sections.sort(key=earliest_timestamp)
        sections.extend(other_sections)
        return sections

    @staticmethod
    def get_main_frames_of_interest(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract the main frames of interest from trace data.

        Handles both old and new trace formats:
        - Old format: frames_of_interest at top level
        - New format: frames in threads, using current_thread_id

        Returns:
            Flat list of frames from the main thread
        """
        # The threads mapping, not config truthiness, distinguishes the new
        # format. Hand-built and older producers can emit thread-aware traces
        # with an empty or missing config.
        threads = data.get("threads", {})
        if threads and len(threads) > 0:
            current_thread_id = data.get("current_thread_id")
            if not current_thread_id:
                # Preserve the legacy fallback for loosely constructed traces
                # that happened to include a threads-shaped value. Producers
                # that explicitly declare a new-format config remain strict.
                if data.get("meta", {}).get("config"):
                    raise ValueError("threads present but no current_thread_id")
                return data.get("frames_of_interest", [])

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
        from .trace_container import load_trace

        if not msgpack_data:
            # legacy traces pre msgpack
            return None

        if auto_generated_name:
            # Fast path: use fast extraction to check for user-specified name
            user_name = extract_trace_name_fast(msgpack_data)
            return user_name if user_name else auto_generated_name
        else:
            # Lazy migration: full deserialization needed
            data = load_trace(msgpack_data)
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

    def compact(
        self,
        include_return_value: bool = False,
        include_guidance: bool = True,
        include_header: bool = True,
    ) -> str:
        """Generate compact text representation of the trace.

        Args:
            include_return_value: Include input/return values in output
            include_guidance: Include CLI guidance section
            include_header: Include the "=== Kolo Trace ===" header with metadata
        """

        parts = []

        if include_header:
            meta = self.unprocessed_data.get("meta", {})
            source = meta.get("source")
            version = meta.get("version")
            py_version = meta.get("environment", {}).get("py_version")
            config = meta.get("config", {})

            header_lines = [
                f"=== Kolo Trace {self.id} ===",
                self.name,
                f"{relative_time(self.dt_utc)}, {pretty_byte_size(self.size)}",
            ]
            if self.recovered:
                header_lines.append(
                    "WARNING: recovered partial trace; the end of execution "
                    "and final metadata may be missing."
                )
            if source and version:
                header_lines.append(f"source: {source} (kolo v{version})")
            elif source:
                header_lines.append(f"source: {source}")
            if config:
                header_lines.append(f"config: {config}")
            if py_version:
                header_lines.append(f"Python: {py_version}")
            root_trace_id = self.unprocessed_data.get("root_trace_id")
            if root_trace_id and root_trace_id != self.id:
                header_lines.append(f"flushed segment of root trace: {root_trace_id}")
            header_lines.extend(
                ["", "format: node_idx, type, qualname, start_to_end_loc, duration", ""]
            )
            header = "\n".join(header_lines)

            # todo: on the config, keep just the stuff that is not default.

            if include_return_value:
                header += """  ↪ input value
  ↩ return value
"""
            parts.append(header)

        if include_guidance:
            guidance = """guidance:
- `kolo run myprogram.py` - run with kolo enabled or capture in another way: docs.kolo.app/capture
- `kolo trace list` - list recent kolo traces
- `kolo cat TRACE_ID` - show trace output. run with `--returns` to include input and return values
- `kolo trace node TRACE_ID NODE_INDEX` - get the FULL details of a specific node, incl locals
"""
            parts.append(guidance)

        lines = list(self._compact_tree_lines(include_return_value))

        if include_header:
            parts.append("=== Trace ===\n" + "\n".join(lines))
        else:
            parts.append("\n".join(lines))

        return "\n".join(parts)

    def compact_tree_only(self, include_return_value: bool = False) -> str:
        """Return compact output without the top-level trace metadata header.

        Single-thread traces render as a bare tree. Multi-thread traces
        still include per-thread section headers and the ``kolo trace
        node ... --thread_id <id>`` access hints so consumers of this
        string know which thread a copied index belongs to.
        """
        return "\n".join(self._compact_tree_lines(include_return_value))

    def _compact_tree_lines(
        self, include_return_value: bool
    ) -> Generator[str, None, None]:
        """Yield compact tree lines for every thread in this trace.

        When the trace only has a single thread, the output is identical
        to iterating ``self.main_tree.dfs()`` directly — no thread header
        is emitted — so single-threaded traces are unchanged. With more
        than one thread, each thread's frames are preceded by a header
        line identifying the thread.
        """
        sections = [s for s in self.threads if s.tree.root_nodes]
        # Fast path only when the main thread is the only thing to show.
        # If the main tree is empty but a background thread has frames,
        # we must still render the header and ``--thread_id`` hint —
        # otherwise a user copying an index out of that section would
        # hit ``kolo trace node TRACE_ID <idx>`` which resolves against
        # the empty ``main_tree`` and silently returns the wrong node.
        only_main = len(sections) == 0 or (
            len(sections) == 1 and sections[0].tree is self.main_tree
        )
        if only_main:
            tree = sections[0].tree if sections else self.main_tree
            for node in tree.dfs():
                yield node.full_compact_tree_line(include_return_value)
            return

        for i, section in enumerate(sections):
            if i > 0:
                yield ""
            yield f"--- {section.label} ---"
            # Per-section hint so users know how to copy a node index out
            # of this thread — non-main threads need --thread_id because
            # indices restart at 0 in every ProcessedTree.
            if section.is_main:
                yield (
                    f"  (access: `kolo trace node {self.id} <idx>` — "
                    "omit --thread_id to target the main thread)"
                )
            else:
                yield (
                    f"  (access: `kolo trace node {self.id} <idx> "
                    f"--thread_id {section.thread_id}`)"
                )
            for node in section.tree.dfs():
                yield node.full_compact_tree_line(include_return_value)

    def compact_metadata(self) -> str:
        """Return just the metadata section (source, config, python version, format)."""
        meta = self.unprocessed_data.get("meta", {})
        source = meta.get("source")
        version = meta.get("version")
        py_version = meta.get("environment", {}).get("py_version")
        config = meta.get("config", {})

        lines = [
            self.name,
            f"{relative_time(self.dt_utc)}, {pretty_byte_size(self.size)}",
        ]
        if self.recovered:
            lines.append(
                "WARNING: recovered partial trace; the end of execution "
                "and final metadata may be missing."
            )
        if source and version:
            lines.append(f"source: {source} (kolo v{version})")
        elif source:
            lines.append(f"source: {source}")
        if config:
            lines.append(f"config: {config}")
        if py_version:
            lines.append(f"Python: {py_version}")
        lines.extend(
            ["", "format: node_idx, type, qualname, start_to_end_loc, duration"]
        )
        return "\n".join(lines)

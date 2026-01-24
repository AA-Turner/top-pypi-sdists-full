"""
Processed node hierarchy for generating compact representations.

These classes wrap ExecutionTreeNode and provide formatting and traversal
capabilities for generating compact trace output.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Optional

from .build_frame_tree import ExecutionTreeNode


def get_line_number_from_path(path: str) -> int:
    """
    Frame paths are formatted as "path:line" (e.g., "foo.py:42").
    """

    parts = path.split(":")
    return int(parts[-1])


class ProcessedNode(ABC):
    def __init__(
        self,
        tree_node: ExecutionTreeNode,
        parent: Optional[ProcessedNode],
        trace_id: str,
    ):
        self.trace_id = trace_id
        self.index = tree_node.index
        self.parent = parent
        self.ancestor_count: int = parent.ancestor_count + 1 if parent else 0
        self.type = tree_node.type
        self.name = tree_node.name
        self.frame_id = tree_node.frame_id
        self.all_children_count = tree_node.all_children_count
        self.data = tree_node.data
        self.subtype = tree_node.subtype

        # Extract timestamps - subclasses may override
        self.start, self.end = self._extract_timestamps(tree_node)
        if self.start and self.end:
            self.duration_ms = (self.end - self.start) * 1000
        else:
            self.duration_ms = 0

        # Create child nodes
        self.children = [
            make_processed_node(child, self, trace_id) for child in tree_node.children
        ]

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
        """
        Extract start and end timestamps from node data.

        Subclasses can override for type-specific logic.
        """
        # Default: try to find timestamps in data
        start = self.data.get("call_timestamp")
        end = self.data.get("return_timestamp")
        return start, end

    def dfs(self) -> Iterator[ProcessedNode]:
        """Depth-first search through the subtree."""
        yield self
        for child in self.children:
            yield from child.dfs()

    def ancestors(self) -> Iterator[ProcessedNode]:
        """Iterate up through the parent chain."""
        node = self.parent
        while node:
            yield node
            node = node.parent

    def find_ancestor_by_frame_id(self, frame_id: str) -> Optional[ProcessedNode]:
        """Find an ancestor node with the given frame_id."""
        for ancestor in self.ancestors():
            if ancestor.frame_id == frame_id:
                return ancestor
        return None

    def is_part_of_background_job(self) -> bool:
        """Check if this node is part of a background job subtree."""
        for ancestor in self.ancestors():
            if isinstance(ancestor, BackgroundJobNode):
                return True
        return False

    def is_part_of_template_rendering(self) -> bool:
        """Check if this node is part of a Django template rendering subtree."""
        for ancestor in self.ancestors():
            if isinstance(ancestor, DjangoTemplateNode):
                return True
        return False

    def formatted_duration(self) -> str:
        """Format duration as human-readable string (ns/μs/ms/s/min/h)."""
        ms = self.duration_ms

        if ms < 0.001:
            # nanoseconds
            ns = ms * 1000000
            return f"{round(ns)}ns"
        elif ms < 1:
            # microseconds
            μs = ms * 1000
            return f"{round(μs)}μs"
        elif ms < 1000:
            # milliseconds
            return f"{round(ms)}ms"
        elif ms < 60000:
            # seconds
            s = ms / 1000
            return f"{s:.1f}s".rstrip("0").rstrip(".")
        elif ms < 3600000:
            # minutes
            min_val = ms / 60000
            return f"{min_val:.1f}min".rstrip("0").rstrip(".")
        else:
            # hours
            h = ms / 3600000
            return f"{h:.1f}h".rstrip("0").rstrip(".")

    @abstractmethod
    def compact_type(self) -> str:
        """Return compact type abbreviation. Subclasses must override."""
        ...

    @abstractmethod
    def compact_tree_line(self) -> str:
        """Return compact tree line content. Subclasses must override."""
        ...

    def input_value(self) -> str:
        """Input into the node as a string. Subclasses can override."""
        return ""

    def return_value(self) -> str:
        """Return the return value as a string. Subclasses can override."""
        return ""

    def full_compact_tree_line(self, include_return_value: bool) -> str:
        """Generate the full compact representation line."""

        indent = "  " * self.ancestor_count
        # space based indentation is better for humans.
        # if we learn later that models can't handle spaces, we can go back to
        # "->" based indentation.
        idx = self.index
        core = self.compact_tree_line()
        formatted_dur = self.formatted_duration()
        dur = formatted_dur if formatted_dur != "0ns" else ""
        input_output_indent = " " * (self.ancestor_count * 2 + len(str(idx)))

        output = f"{indent}{idx} {core} {dur}"

        if include_return_value:
            output += f"""
{input_output_indent} ↪ {self.input_value()}
{input_output_indent} ↩ {self.return_value()}"""

        return output


class FrameSpanNode(ProcessedNode):
    """Node representing a function call/return pair."""

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
        call_frame = self.data["call_frame"]
        return_frame = self.data["return_frame"]
        start = call_frame["timestamp"]
        end = return_frame["timestamp"]
        return start, end

    def compact_type(self) -> str:
        return "f"

    def input_value(self) -> str:
        call_locals = self.data["call_frame"].get("locals", {})

        output = ""
        for key, value in call_locals.items():
            if output:
                output += "; "
            output += f"{key}: {repr(value)}"
        return output

    def return_value(self) -> str:
        return_frame = self.data["return_frame"]

        try:
            return_value = return_frame["arg"]
        except KeyError:
            # some frames (module frames for example) don't have arg set at all
            return ""

        return repr(return_value)

    def compact_tree_line(self) -> str:
        call_frame = self.data["call_frame"]
        return_frame = self.data["return_frame"]
        call_line = get_line_number_from_path(call_frame["path"])
        return_line = get_line_number_from_path(return_frame["path"])
        return f"{self.name} ({call_line}-{return_line})"


class SQLQueryNode(ProcessedNode):
    """Node representing a SQL query."""

    def compact_type(self) -> str:
        return "s"

    def return_value(self) -> str:
        query_data = self.data["query_data"]
        if query_data is None:
            return ""
        return query_data

    def compact_tree_line(self) -> str:
        query = self.data["query"]
        if not query:
            return "SQL query"

        return query


class BackgroundJobNode(ProcessedNode):
    """Node representing a background job."""

    def compact_type(self) -> str:
        return "bgj"

    def return_value(self) -> str:
        return ""  # We don't collect return values for background jobs

    def compact_tree_line(self) -> str:
        subtype = self.data["subtype"]
        name = self.data["name"]
        return f"{subtype} {name}"


class ServedRequestNode(ProcessedNode):
    """Node representing a served HTTP request."""

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
        # Served requests store duration directly, not timestamps
        response = self.data["response"]
        ms_duration = response["ms_duration"]
        self.duration_ms = ms_duration
        return None, None

    def compact_type(self) -> str:
        return "sr"

    def return_value(self) -> str:
        response = self.data["response"]
        content = response["content"]
        if content is None:
            return ""
        # TODO: Figure out how to format this for newlines..

        return content

    def compact_tree_line(self) -> str:
        request = self.data["request"]
        method = request["method"]
        path_info = request["path_info"]
        return f"{method} {path_info}"


class OutboundRequestNode(ProcessedNode):
    """Node representing an outbound HTTP request."""

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
        request = self.data["request"]
        response = self.data["response"]
        start = request["timestamp"]
        end = response["timestamp"] if response else None
        return start, end

    def compact_type(self) -> str:
        return "or"

    def return_value(self) -> str:
        response = self.data["response"]
        if not response:
            return ""
        body = response["body"]
        if body is None:
            return ""
        # TODO: Figure out how to format this for newlines..
        body_str = str(body)[:100].replace("\n", " ")
        return body_str

    def compact_tree_line(self) -> str:
        request = self.data["request"]
        method = request["method"]
        url = request["url"]
        return f"{method} {url}"


class TestNode(ProcessedNode):
    """Node representing a test execution."""

    def compact_type(self) -> str:
        return "t"

    def return_value(self) -> str:
        return ""  # TODO: could show test outcome

    def compact_tree_line(self) -> str:
        test_class = self.data["test_class"]
        test_name = self.data["test_name"]
        if test_class:
            return f"{test_class}.{test_name}"
        return test_name


class DjangoTemplateNode(ProcessedNode):
    """Node representing Django template rendering."""

    def compact_type(self) -> str:
        return "djt"

    def return_value(self) -> str:
        return ""

    def compact_tree_line(self) -> str:
        template = self.data["template"]
        return f"Template: {template}"


class LogMessageNode(ProcessedNode):
    """Node representing a log message."""

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
        # Log messages are leaf nodes with no duration
        return None, None

    def compact_type(self) -> str:
        return "l"

    def return_value(self) -> str:
        return ""

    def compact_tree_line(self) -> str:
        msg = self.data["msg"]
        msg_str = str(msg)[:50]
        return f"Log: {msg_str}"


def make_processed_node(
    tree_node: ExecutionTreeNode, parent: Optional[ProcessedNode], trace_id: str
) -> ProcessedNode:
    """Factory function to create the appropriate ProcessedNode subclass."""
    node_type = tree_node.type

    if node_type == "frame_span":
        return FrameSpanNode(tree_node, parent, trace_id)
    elif node_type == "sql_query":
        return SQLQueryNode(tree_node, parent, trace_id)
    elif node_type == "nested_background_job":
        return BackgroundJobNode(tree_node, parent, trace_id)
    elif node_type == "nested_served_http_request":
        return ServedRequestNode(tree_node, parent, trace_id)
    elif node_type == "outbound_http_request":
        return OutboundRequestNode(tree_node, parent, trace_id)
    elif node_type == "nested_test":
        return TestNode(tree_node, parent, trace_id)
    elif node_type == "django_template":
        return DjangoTemplateNode(tree_node, parent, trace_id)
    elif node_type == "log_message":
        return LogMessageNode(tree_node, parent, trace_id)
    else:
        raise ValueError(f"Unknown node type: {node_type}")

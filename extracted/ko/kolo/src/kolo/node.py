"""
Processed node hierarchy for generating compact representations.

These classes wrap ExecutionTreeNode and provide formatting and traversal
capabilities for generating compact trace output.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Optional

from .build_frame_tree import ExecutionTreeNode


def get_line_number_from_path(path: str) -> int | None:
    """
    Frame paths are formatted as "path:line" (e.g., "foo.py:42"), or
    "path:None" when the frame had no source line.
    """

    line = path.rsplit(":", 1)[-1]
    if line == "None":
        return None
    return int(line)


def _line(line: int | None) -> str:
    return "?" if line is None else str(line)


def assignment_line(frame: dict) -> str:
    """The source line of a ``line_events`` assignment frame, or ``?``."""
    path = frame.get("path")
    if not isinstance(path, str):
        return "?"
    try:
        return _line(get_line_number_from_path(path))
    except ValueError:
        return "?"


def unattached_assignment_label(frame: dict) -> str:
    """Where an assignment outside any recorded call happened:
    ``path:line qualname``."""
    name = frame.get("qualname") or frame.get("co_name") or "<unknown>"
    return f"{frame.get('path')} {name}"


def exception_type_name(exception: str) -> str:
    """``DataError`` from the ``DataError: message`` a SQL query's end event
    records when the query raised."""
    return exception.split(":", 1)[0]


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

        self.start, self.end = self._extract_timestamps(tree_node)
        if self.start and self.end:
            self.duration_ms = (self.end - self.start) * 1000
        else:
            self.duration_ms = 0

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
            ns = ms * 1000000
            return f"{round(ns)}ns"
        elif ms < 1:
            μs = ms * 1000
            return f"{round(μs)}μs"
        elif ms < 1000:
            return f"{round(ms)}ms"
        elif ms < 60000:
            s = ms / 1000
            return f"{s:.1f}s".rstrip("0").rstrip(".")
        elif ms < 3600000:
            min_val = ms / 60000
            return f"{min_val:.1f}min".rstrip("0").rstrip(".")
        else:
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

    def compact_line(self) -> str:
        """``compact_tree_line``, saying so if the call has no recorded exit."""
        core = self.compact_tree_line()
        if self.data.get("exit_not_recorded"):
            return f"{core} {EXIT_NOT_RECORDED_LABEL}"
        return core

    def input_value(self) -> str:
        """Input into the node as a string. Subclasses can override."""
        return ""

    def return_value(self) -> str:
        """Return the return value as a string. Subclasses can override."""
        return ""

    def assignment_values(self) -> Iterator[str]:
        """The node's recorded assignments (``line_events``), in order, as
        ``line N: name = value`` strings. Subclasses can override."""
        return iter(())

    def full_compact_tree_line(self, include_return_value: bool) -> str:
        """Generate the full compact representation line."""

        indent = "  " * self.ancestor_count
        idx = self.index
        core = self.compact_line()
        formatted_dur = self.formatted_duration()
        dur = formatted_dur if formatted_dur != "0ns" else ""
        input_output_indent = " " * (self.ancestor_count * 2 + len(str(idx)))

        output = f"{indent}{idx} {core} {dur}"

        if include_return_value:
            lines = [output, f"{input_output_indent} ↪ {self.input_value()}"]
            lines.extend(
                f"{input_output_indent} ≔ {assignment}"
                for assignment in self.assignment_values()
            )
            lines.append(f"{input_output_indent} ↩ {self.return_value()}")
            output = "\n".join(lines)

        return output


VALUES_OMITTED = "<not recorded: too close to the C stack limit>"
EXIT_NOT_RECORDED_LABEL = "[did not return: no exit recorded]"
EXIT_NOT_RECORDED = "<not recorded: the trace has no exit for this call>"


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
        call_frame = self.data["call_frame"]
        if call_frame.get("values_omitted"):
            return VALUES_OMITTED
        call_locals = call_frame.get("locals", {})

        output = ""
        for key, value in call_locals.items():
            if output:
                output += "; "
            output += f"{key}: {repr(value)}"
        return output

    def return_value(self) -> str:
        return_frame = self.data["return_frame"]
        if return_frame.get("exit_not_recorded"):
            return EXIT_NOT_RECORDED
        if return_frame.get("values_omitted"):
            return VALUES_OMITTED

        try:
            return_value = return_frame["arg"]
        except KeyError:
            return ""

        return repr(return_value)

    def assignment_values(self) -> Iterator[str]:
        for frame in self.data.get("assignments", ()):
            variable, value = frame["assign"]
            yield f"line {assignment_line(frame)}: {variable} = {value!r}"

    def compact_tree_line(self) -> str:
        call_frame = self.data["call_frame"]
        return_frame = self.data["return_frame"]
        call_line = get_line_number_from_path(call_frame["path"])
        return_line = get_line_number_from_path(return_frame["path"])
        return f"{self.name} ({_line(call_line)}-{_line(return_line)})"


class SQLQueryNode(ProcessedNode):
    """Node representing a SQL query."""

    def compact_type(self) -> str:
        return "s"

    def return_value(self) -> str:
        if self.data.get("exit_not_recorded"):
            return EXIT_NOT_RECORDED
        exception = self.data.get("exception")
        if exception:
            return f"raised {exception}"
        query_data = self.data["query_data"]
        if query_data is None:
            return ""
        return query_data

    def compact_tree_line(self) -> str:
        query = self.data["query"]
        if not query:
            return "SQL query"
        exception = self.data.get("exception")
        if exception:
            return f"{query} [raised {exception_type_name(exception)}]"

        return query


class BackgroundJobNode(ProcessedNode):
    """Node representing a background job."""

    def compact_type(self) -> str:
        return "bgj"

    def return_value(self) -> str:
        return ""

    def compact_tree_line(self) -> str:
        subtype = self.data["subtype"]
        name = self.data["name"]
        return f"{subtype} {name}"


class ServedRequestNode(ProcessedNode):
    """Node representing a served HTTP request."""

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
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
        end = response["timestamp"] if response else self.data.get("return_timestamp")
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
        body_str = str(body)[:100].replace("\n", " ")
        return body_str

    def compact_tree_line(self) -> str:
        request = self.data["request"]
        method = request["method"]
        url = request["url"]
        if self.data.get("incomplete_at_trace_boundary"):
            return f"{method} {url} [response not captured: trace boundary]"
        return f"{method} {url}"


class TestNode(ProcessedNode):
    """Node representing a test execution."""

    def compact_type(self) -> str:
        return "t"

    def return_value(self) -> str:
        return ""

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
        return None, None

    def compact_type(self) -> str:
        return "l"

    def return_value(self) -> str:
        return ""

    def compact_tree_line(self) -> str:
        msg = self.data["msg"]
        msg_str = str(msg)[:50]
        return f"Log: {msg_str}"


class SubtreeFlushedNode(ProcessedNode):
    """Node representing a flushed subtree placeholder."""

    def _extract_timestamps(
        self, tree_node: ExecutionTreeNode
    ) -> tuple[Optional[float], Optional[float]]:
        timestamp = self.data.get("timestamp")
        return timestamp, timestamp

    def compact_type(self) -> str:
        return "sf"

    def return_value(self) -> str:
        return ""

    def compact_tree_line(self) -> str:
        co_name = self.data.get("co_name", "<unknown>")
        flushed_trace_id = self.data.get("flushed_trace_id", "<unknown>")
        segment_count = self.data.get("flushed_segment_count")
        if segment_count is not None and segment_count > 1:
            detail = f"{co_name} +{segment_count - 1} more"
        else:
            detail = co_name
        return f"[flushed segment] {detail} -> {flushed_trace_id}"


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
    elif node_type == "subtree_flushed":
        return SubtreeFlushedNode(tree_node, parent, trace_id)
    else:
        raise ValueError(f"Unknown node type: {node_type}")

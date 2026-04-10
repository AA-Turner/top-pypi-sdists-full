"""
Navigation context for emit functions with O(1) lookups.

This module provides the TraceNavigator class which enables efficient
navigation through trace trees, removing the need for denormalized data
like the `path` field in UserCodeCallSite.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .node import ProcessedNode
    from .trace import ProcessedTree


class TraceNavigator:
    """Navigation context for emit functions with O(1) lookups.

    TraceNavigator wraps a ProcessedTree and provides convenient methods
    for navigating the trace, including resolving call sites to their
    source frames.
    """

    def __init__(
        self, tree: ProcessedTree, current_node: Optional[ProcessedNode] = None
    ):
        """Create a navigator for the given tree.

        Args:
            tree: The ProcessedTree to navigate
            current_node: Optional current node context
        """
        self._tree = tree
        self._current = current_node

    @property
    def tree(self) -> ProcessedTree:
        """Get the underlying ProcessedTree."""
        return self._tree

    @property
    def current(self) -> Optional[ProcessedNode]:
        """Get the current node context."""
        return self._current

    def find_by_frame_id(self, frame_id: str) -> Optional[ProcessedNode]:
        """Find a node by its frame_id in O(1) time.

        Args:
            frame_id: The frame_id to search for

        Returns:
            The ProcessedNode with the given frame_id, or None if not found
        """
        return self._tree.find_node_by_frame_id(frame_id)

    def resolve_call_site(self, call_site: Optional[dict]) -> Optional[ProcessedNode]:
        """Resolve a UserCodeCallSite to the calling frame.

        Args:
            call_site: A UserCodeCallSite dict (or None)

        Returns:
            The ProcessedNode for the calling frame, or None if not found
        """
        if not call_site:
            return None
        call_frame_id = call_site.get("call_frame_id", "")
        if not call_frame_id:
            return None
        return self.find_by_frame_id(call_frame_id)

    def get_path_from_call_site(self, call_site: Optional[dict]) -> Optional[str]:
        """Get file path by looking up the calling frame.

        This replaces the need for the denormalized `path` field in
        UserCodeCallSite. Instead of storing the path redundantly,
        we look it up from the calling frame.

        Args:
            call_site: A UserCodeCallSite dict (or None)

        Returns:
            The file path of the calling frame, or None if not found
        """
        caller = self.resolve_call_site(call_site)
        if caller and caller.type == "frame_span":
            call_frame = caller.data.get("call_frame", {})
            return call_frame.get("path")
        return None

    def for_node(self, node: ProcessedNode) -> TraceNavigator:
        """Create a new navigator focused on a specific node.

        Args:
            node: The node to focus on

        Returns:
            A new TraceNavigator with the same tree but different current node
        """
        return TraceNavigator(self._tree, node)

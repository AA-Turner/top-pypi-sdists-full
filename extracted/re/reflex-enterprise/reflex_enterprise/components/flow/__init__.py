"""This module provides a drag-and-drop component for Reflex applications."""

import reflex

from . import hooks as api
from . import util
from .flow import (
    Background,
    BaseEdge,
    ControlButton,
    Controls,
    EdgeLabelRenderer,
    EdgeText,
    Flow,
    FlowProvider,
    Handle,
    MiniMap,
    NodeResizeControl,
    NodeResizer,
    NodeToolbar,
    Panel,
    ViewportPortal,
)


class FlowNamespace(reflex.ComponentNamespace):
    """Namespace for all flow-related components."""

    __call__ = Flow.create
    provider = FlowProvider.create
    background = Background.create
    base_edge = BaseEdge.create
    control_button = ControlButton.create
    controls = Controls.create
    edge_label_renderer = EdgeLabelRenderer.create
    edge_text = EdgeText.create
    handle = Handle.create
    mini_map = MiniMap.create
    node_resize_control = NodeResizeControl.create
    node_resizer = NodeResizer.create
    node_toolbar = NodeToolbar.create
    panel = Panel.create
    viewport_portal = ViewportPortal.create
    util = util
    api = api


flow = FlowNamespace()

__all__ = ["flow"]

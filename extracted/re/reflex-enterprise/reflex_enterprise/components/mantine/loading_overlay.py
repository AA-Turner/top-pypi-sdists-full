"""LoadingOverlay component for Mantine."""

from typing import Any, Dict

import reflex as rx

from reflex_enterprise.components.mantine.base import MantineCoreBase


class LoadingOverlay(MantineCoreBase):
    """Display loading overlay over any element."""

    tag = "LoadingOverlay"

    # Indicates whether the overlay is visible.
    visible: rx.Var[bool]

    # Controls overlay z-index.
    z_index: rx.Var[str | int]

    # Props passed down to the Overlay component.
    overlay_props: rx.Var[Dict[str, Any]]

    # Props passed down to the Loader component.
    loader_props: rx.Var[Dict[str, Any]]

    # Props passed down to the Transition component that wraps the Loader, applied when overlay is mounted and unmounted.
    transition_props: rx.Var[Dict[str, Any]]

    @classmethod
    def create(cls, *children: Any, **props: Any) -> rx.Component:
        """Create a LoadingOverlay component."""
        return rx.el.Div.create(
            super().create(**props),
            *children,
            position="relative",
        )


loading_overlay = LoadingOverlay.create

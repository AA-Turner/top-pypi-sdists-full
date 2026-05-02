"""Spoiler component for Mantine UI in Reflex."""

from typing import Any

import reflex as rx
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import MantineCoreBase


class Spoiler(MantineCoreBase):
    """Reveal content when the user clicks on the trigger."""

    tag = "Spoiler"

    # Control Ref
    control_ref: Var[Any]

    # Controlled expanded state value
    expanded: Var[bool]

    # Label for close spoiler action
    hide_label: Var[str]

    # Initial spoiler state, true to wrap content in spoiler, false to show content without spoiler, opened state is updated on mount
    initial_state: Var[bool]

    # Maximum height of the visible content, when this point is reached spoiler appears, 100 by default
    max_height: Var[int | float]

    # Label for open spoiler action
    show_label: Var[str]

    # Spoiler reveal transition duration in ms, set 0 or null to turn off animation, 200 by default
    transition_duration: Var[int | float]

    # Called when spoiler state changes.
    on_expanded_change: rx.EventHandler[rx.event.passthrough_event_spec(bool)]


spoiler = Spoiler.create

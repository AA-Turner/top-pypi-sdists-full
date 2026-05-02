"""Collapse component for Mantine UI in Reflex."""

import reflex as rx
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import MantineCoreBase


class Collapse(MantineCoreBase):
    """Expand or collapse content with animation."""

    tag = "Collapse"

    # Determines whether opacity should be animated, defaults to true
    animate_opacity: Var[bool]

    # Controls collapse state
    in_: Var[bool]

    # Transition duration in ms
    transition_duration: Var[int]

    # Transition timing function, defaults to 'ease'
    transition_timing_function: Var[str]

    # Called when transition ends
    on_transition_end: rx.EventHandler[rx.event.no_args_event_spec]

    _rename_props = {
        "in_": "in",
    }


collapse = Collapse.create

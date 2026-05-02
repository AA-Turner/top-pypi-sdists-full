"""Combobox component for Mantine UI."""

from typing import Any, Literal

import reflex as rx
from reflex.components.component import Component
from reflex.components.props import PropsBase

from reflex_enterprise.components.mantine.base import BaseMantineInput, MantineCoreBase


class ComboboxBase(MantineCoreBase):
    """Base class for Combobox components."""


class MiddlewaresProps(PropsBase):
    """Props for dropdown positioning middlewares."""

    shift: rx.Var[bool]
    flip: rx.Var[bool]
    inline: rx.Var[bool]


class Combobox(
    BaseMantineInput,
    ComboboxBase,
):
    """Displays a customizable dropdown list."""

    tag = "Combobox"

    # Arrow offset in px, 5 by default
    arrow_offset: rx.Var[int]

    # Arrow position
    arrow_position: rx.Var[Literal["center", "side"]]

    # Arrow border-radius in px, 0 by default
    arrow_radius: rx.Var[int]

    # Arrow size in px, 7 by default
    arrow_size: rx.Var[int]

    # If set, popover dropdown will not be rendered
    disabled: rx.Var[bool]

    # Controls padding of the dropdown, 4 by default
    dropdown_padding: rx.Var[str | int]

    # Changes floating ui position strategy, 'absolute' by default
    floating_strategy: rx.Var[Literal["absolute", "fixed"]]

    # If set, the dropdown is hidden when the element is hidden with styles or not visible on the screen, true by default
    hide_detached: rx.Var[bool]

    # If set dropdown will not be unmounted from the DOM when it is hidden, display: none styles will be added instead
    keep_mounted: rx.Var[bool]

    # Floating ui middlewares to configure position handling, { flip: true, shift: true, inline: false } by default
    middlewares: rx.Var[MiddlewaresProps | dict[str, Any]]

    # Offset of the dropdown element, 8 by default
    offset: rx.Var[int]

    # Props passed down to Overlay component
    overlay_props: rx.Var[dict[str, Any]]

    # Props to pass down to the Portal when withinPortal is true
    portal_props: rx.Var[dict[str, Any]]

    # Dropdown position relative to the target element, 'bottom' by default
    position: rx.Var[Literal["top", "bottom", "left", "right"]]

    # useEffect dependencies to force update dropdown position, [] by default
    position_dependencies: rx.Var[list[Any]]

    # Key of theme.radius or any valid CSS value to set border-radius, theme.defaultRadius by default
    radius: rx.Var[str | int]

    # Determines whether selection should be reset when option is hovered, false by default
    reset_selection_on_option_hover: rx.Var[bool]

    # Determines whether focus should be automatically returned to control when dropdown closes, false by default
    return_focus: rx.Var[bool]

    # Key of theme.shadows or any other valid CSS box-shadow value
    shadow: rx.Var[str]

    # Combobox store, can be used to control combobox state
    store: rx.Var[Any] = rx.Var.create("combobox")

    # Props passed down to the Transition component that used to animate dropdown presence, use to configure duration and animation type, { duration: 150, transition: 'fade' } by default
    transition_props: rx.Var[dict[str, Any]]

    # Dropdown width, or 'target' to make dropdown width the same as target element, 'max-content' by default
    width: rx.Var[str | int | Literal["target"]]

    # Determines whether component should have an arrow, false by default
    with_arrow: rx.Var[bool]

    # Determines whether the overlay should be displayed when the dropdown is opened, false by default
    with_overlay: rx.Var[bool]

    # Determines whether dropdown should be rendered within the Portal, true by default
    with_portal: rx.Var[bool]

    # Dropdown z-index, 300 by default
    z_index: rx.Var[int]

    # Called when dropdown closes
    on_close: rx.EventHandler[rx.event.no_args_event_spec]

    # Called when the popover is dismissed by clicking outside or by pressing escape
    on_dismiss: rx.EventHandler[rx.event.no_args_event_spec]

    # Called when enter transition ends
    on_enter_transition_end: rx.EventHandler[rx.event.no_args_event_spec]

    # Called when exit transition ends
    on_exit_transition_end: rx.EventHandler[rx.event.no_args_event_spec]

    # Called when dropdown opens
    on_open: rx.EventHandler[rx.event.no_args_event_spec]

    # Called when item is selected with Enter key or by clicking it
    on_option_submit: rx.EventHandler[
        rx.event.passthrough_event_spec(tuple[str, dict[str, Any]])
    ]

    # Called when dropdown position changes
    on_position_change: rx.EventHandler[rx.event.passthrough_event_spec(float)]

    def add_hooks(self):
        """Add hooks to the component."""
        combobox_hook = rx.Var(
            "const combobox = useCombobox()",
            _var_data=rx.vars.VarData(
                imports={"@mantine/core": "useCombobox"},
                position=rx.constants.Hooks.HookPosition.PRE_TRIGGER,
            ),
        )
        return [combobox_hook]


class ComboboxOptions(ComboboxBase):
    """Combobox options element wrapper."""

    tag = "Combobox.Options"


class ComboboxOption(ComboboxBase):
    """Combobox option."""

    tag = "Combobox.Option"

    # If set, highlights the option as active
    active: rx.Var[bool]

    # If set, option cannot be selected
    disabled: rx.Var[bool]

    # Determines whether item is selected, useful for virtualized comboboxes
    selected: rx.Var[bool]

    # Option value
    value: rx.Var[str]


class ComboboxTarget(ComboboxBase):
    """Target element wrapper, wraps the element that opens dropdown."""

    tag = "Combobox.Target"

    _rename_props = {"target": "children"}

    # Input autocomplete attribute
    autocomplete: rx.Var[str]

    # Target element
    target: rx.Var[Any]

    # Key of the prop that should be used to access element ref
    ref_prop: rx.Var[str]

    # Determines which events should be handled by the target element. button target type handles Space and Enter keys to toggle dropdown opened state. input by default.
    target_type: rx.Var[Literal["button", "input"]]

    # Determines whether the target should have aria- attributes, true by default
    with_aria_attributes: rx.Var[bool]

    # Determines whether the target should have aria-expanded attribute, false by default
    with_expanded_attribute: rx.Var[bool]

    # Determines whether component should respond to keyboard events, true by default
    with_keyboard_navigation: rx.Var[bool]


class ComboboxDropdownTarget(ComboboxBase):
    """Dropdown target element wrapper, wraps the element that opens dropdown."""

    tag = "Combobox.DropdownTarget"

    _rename_props = {"target": "children"}

    # Dropdown target element
    target: rx.Var[Any]

    # Key of the prop that should be used to access element ref
    ref_prop: rx.Var[str]


class ComboboxEventsTarget(ComboboxTarget):
    """Events target element wrapper, wraps the element that opens dropdown."""

    tag = "Combobox.EventsTarget"


class ComboboxDropdown(ComboboxBase):
    """Dropdown element wrapper."""

    tag = "Combobox.Dropdown"

    # If set, dropdown will be hidden, useful for custom transitions
    hidden: rx.Var[bool]


class ComboboxGroup(ComboboxBase):
    """Combobox group element wrapper."""

    tag = "Combobox.Group"

    # Group label
    label: rx.Var[Component | str]


class ComboboxNamespace(rx.ComponentNamespace):
    """Namespace for Combobox components."""

    __call__ = staticmethod(Combobox.create)
    options = staticmethod(ComboboxOptions.create)
    option = staticmethod(ComboboxOption.create)
    target = staticmethod(ComboboxTarget.create)
    dropdown_target = staticmethod(ComboboxDropdownTarget.create)
    events_target = staticmethod(ComboboxEventsTarget.create)
    dropdown = staticmethod(ComboboxDropdown.create)
    group = staticmethod(ComboboxGroup.create)


combobox = ComboboxNamespace()

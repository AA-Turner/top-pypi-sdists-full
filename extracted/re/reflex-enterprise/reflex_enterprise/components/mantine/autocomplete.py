"""Autocompletes input with dropdown."""

import reflex as rx
from reflex.components.component import Component  # noqa: F401

from reflex_enterprise.components.mantine.base import (
    MantineDescriptionProps,
    MantineErrorProps,
    MantineLabelProps,
    MantineSize,
)
from reflex_enterprise.components.mantine.combobox import (
    Combobox,
    MiddlewaresProps,  # noqa: F401
)


class Autocomplete(
    MantineDescriptionProps, MantineErrorProps, MantineLabelProps, Combobox
):
    """Autocomplete input with dropdown."""

    tag = "Autocomplete"

    # Props passed down to the clear button
    clear_button_props: rx.Var[dict]

    # Determines whether the clear button should be displayed in the right section when the component has value, false by default
    clearable: rx.Var[bool]

    # Props passed down to Combobox component
    combobox_props: rx.Var[dict]

    # Data displayed in the dropdown. Values must be unique, otherwise an error will be thrown and component will not render.
    data: rx.Var[list[str]]

    # Uncontrolled dropdown initial opened state
    default_dropdown_opened: rx.Var[bool]

    # Uncontrolled component default value
    default_value: rx.Var[list[str]]

    # Sets disabled attribute on the input element
    disabled: rx.Var[bool]

    # Controlled dropdown opened state
    dropdown_opened: rx.Var[bool]

    # max-height of the dropdown, only applicable when withScrollArea prop is true, 250 by default
    dropdown_max_height: rx.Var[float | str]

    # Controls input height and horizontal padding, 'sm' by default
    size: rx.Var[MantineSize | str]

    # Value of the input
    value: rx.Var[str]

    # Event handler for dropdown close
    on_dropdown_close: rx.EventHandler[rx.event.no_args_event_spec]

    # Event handler for dropdown open
    on_dropdown_open: rx.EventHandler[rx.event.no_args_event_spec]

    # Event handler when an option is submitted, receives item value
    on_option_submit: rx.EventHandler[lambda item: [item]]


autocomplete = Autocomplete.create

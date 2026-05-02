"""MultiSelect component for Reflex Enterprise."""

from typing import Any, List, Literal

import reflex as rx
from reflex.components.component import Component

from reflex_enterprise.components.mantine.base import BaseMantineInput


class MultiSelect(BaseMantineInput):
    """Renders a multiselect component."""

    tag = "MultiSelect"

    # If set, value can be cleared by clicking the clear button located on the right side of the input, by default hidden
    clearable: rx.Var[bool]

    # Props passed down to the clear button
    clear_button_props: rx.Var[dict]

    # Props passed down to the underlying Combobox component
    combobox_props: rx.Var[dict]

    # Data used to render options. Can be an array of strings or objects with value and label properties.
    data: rx.Var[List[str | dict]]

    # Initial value for uncontrolled component
    default_value: rx.Var[List[str]]

    # Input description, displayed below the input
    description: rx.Var[str | Component]

    # Props passed down to the description element
    description_props: rx.Var[dict]

    # If true, the input is disabled
    disabled: rx.Var[bool]

    # Controlled dropdown opened state
    dropdown_opened: rx.Var[bool]

    # Input error message, displayed below the input
    error: rx.Var[str | Component]

    # Props passed down to the error message element
    error_props: rx.Var[dict]

    # Function based on which items are filtered and sorted
    filter: rx.Var[Any]

    # Determines whether picked options should be removed from the dropdown. False by default.
    hide_picked_options: rx.Var[bool]

    # Function to customize the input container element.
    input_container: rx.Var[Any]

    # Controls the order of elements within the input wrapper.
    input_wrapper_order: rx.Var[List[Literal["label", "description", "input", "error"]]]

    # Input label, displayed above the input
    label: rx.Var[str | Component]

    # Props passed down to the label element
    label_props: rx.Var[dict]

    # Maximum number of options displayed in the dropdown, Infinity by default
    limit: rx.Var[int]

    # Maximum dropdown height, defaults to `220`
    max_dropdown_height: rx.Var[str | float | int]

    # Maximum number of values that can be picked
    max_values: rx.Var[int]

    # Message displayed when no options match the search query
    nothing_found_message: rx.Var[str | Component]

    # Props passed down to the underlying PillsInput component
    pills_input_props: rx.Var[dict]

    # Placeholder displayed when the input is empty
    placeholder: rx.Var[str]

    # Determines whether the input should have `cursor: pointer` style, `false` by default
    pointer: rx.Var[bool]

    # Input border-radius, key of `theme.radius` or any valid CSS value. Defaults to `theme.defaultRadius`.
    radius: rx.Var[str | int | Literal["xs", "sm", "md", "lg", "xl"]]

    # Function to customize option rendering
    render_option: rx.Var[Any]

    # Determines whether the input is required, adds an asterisk `*` to the label if `withAsterisk` is not set
    required: rx.Var[bool]

    # Determines whether the options should be filtered based on the search query, `false` by default
    searchable: rx.Var[bool]

    # Controlled search value
    search_value: rx.Var[str]

    # Determines whether the first option should be selected when the search query changes, `false` by default
    select_first_option_on_search: rx.Var[bool]

    # Input size, key of `theme.spacing` or any valid CSS value. Defaults to `md`.
    size: rx.Var[str | Literal["xs", "sm", "md", "lg", "xl"]]

    # Controlled component value
    value: rx.Var[List[str]]

    # Input variant, defaults to `default`
    variant: rx.Var[str]

    # Determines whether the required asterisk `*` should be displayed next to the label. True by default.
    with_asterisk: rx.Var[bool]

    # Props passed down to the root element
    wrapper_props: rx.Var[dict]

    # Determines whether the error state styles should be applied. True by default.
    with_error_styles: rx.Var[bool]

    # Called when the value changes
    on_change: rx.EventHandler[lambda value: [value]]

    # Called when the dropdown is closed
    on_dropdown_close: rx.EventHandler

    # Called when the dropdown is opened
    on_dropdown_open: rx.EventHandler

    # Called when the search value changes
    on_search_value_change: rx.EventHandler[lambda value: [value]]

    # Called when an option is selected from the dropdown, not called when the value changes programmatically
    on_option_submit: rx.EventHandler[lambda value: [value]]


multi_select = MultiSelect.create

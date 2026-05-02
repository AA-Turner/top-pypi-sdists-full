"""TagsInput component for Mantine."""

from typing import Callable, Literal

import reflex as rx
from reflex.components.component import Component
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import BaseMantineInput


class TagsInput(BaseMantineInput):
    """Display tags for multi-value input."""

    tag = "TagsInput"

    # Props for TagsInput specific functionality
    # Accept values on blur
    accept_value_on_blur: Var[bool]

    # Allow duplicate tags
    allow_duplicates: Var[bool]

    # Props for the clear button
    clear_button_props: Var[dict]

    # Combobox props
    combobox_props: Var[dict]

    # Data displayed in the dropdown. Values must be unique, otherwise an error will be thrown and component will not render.
    data: Var[list[str]]

    # Uncontrolled dropdown initial opened state
    default_dropdown_opened: Var[bool]

    # Default search value
    default_search_value: Var[str]

    # Default value for uncontrolled component
    default_value: Var[list[str]]

    # Description displayed below the input. If not set, the description will not be rendered.
    description: Var[Component | str]

    # Props for the description
    description_props: Var[dict]

    # Sets disabled attribute on the input element
    disabled: Var[bool]

    # Controlled dropdown opened state
    dropdown_opened: Var[bool]

    # Contents of Input.Error component. If not set, error is not rendered.
    error: Var[Component | str | bool]

    # Props for the error message.
    error_props: Var[dict]

    # Function based on which items are filtered and sorted
    filter: Var[Callable]

    # Props passed down to the hidden input
    hidden_input_props: Var[dict]

    # Divider used to separate values in the hidden input value attribute, ',' by default
    hidden_input_values_divider: Var[str]

    # Input container component
    input_container: Var[Component]

    # size prop added to the input element
    input_size: Var[str]

    # Controls order of the elements, ['label', 'description', 'input', 'error'] by default
    input_wrapper_order: Var[list[Literal["label", "description", "input", "error"]]]

    # Label component
    label: Var[Component | str]

    # Label props
    label_props: Var[dict]

    # Maximum number of options displayed at a time, Infinity by default
    limit: Var[int]

    # max-height of the dropdown, only applicable when withScrollArea prop is true, 250 by default
    max_dropdown_height: Var[float | str]

    # Maximum number of tags, Infinity by default
    max_tags: Var[int]

    # Determines whether the input should have cursor: pointer style, false by default
    pointer: Var[bool]

    # Key of theme.radius or any valid CSS value to set border-radius, numbers are converted to rem, theme.defaultRadius by default
    radius: Var[Literal["xs", "sm", "md", "lg", "xl"] | int | str]

    # A function to render content of the option, replaces the default content of the option
    render_option: Var[Callable]

    # Adds required attribute to the input and a red asterisk on the right side of label, false by default
    required: Var[bool]

    # Props passed down to the underlying ScrollArea component in the dropdown
    scroll_area_props: Var[dict]

    # Controlled search value
    search_value: Var[str]

    # Determines whether the first option should be selected when value changes, false by default
    select_first_option_on_change: Var[bool]

    # Controls input height and horizontal padding, 'sm' by default
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # Characters that should trigger tags split, [','] by default
    split_chars: Var[list[str]]

    # Controlled component value
    value: Var[list[str]]

    # Determines whether the required asterisk should be displayed. Overrides required prop. Does not add required attribute to the input. false by default
    with_asterisk: Var[bool]

    # Determines whether the input should have red border and red text color when the error prop is set, true by default
    with_error_styles: Var[bool]

    # Determines whether the options should be wrapped with ScrollArea.AutoSize, true by default
    with_scroll_area: Var[bool]

    # Event Handlers
    # Called when value changes
    on_change: rx.EventHandler[rx.event.passthrough_event_spec(list[str])]

    # Called when the clear button is clicked
    on_clear: rx.EventHandler[lambda: []]

    # Called when the dropdown is opened
    on_dropdown_open: rx.EventHandler[lambda: []]

    # Called when the dropdown is closed
    on_dropdown_close: rx.EventHandler[lambda: []]

    # Called when user tries to submit a duplicated tag
    on_duplicate: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when option is submitted from dropdown with mouse click or Enter key
    on_option_submit: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when tag is removed
    on_remove: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when search changes
    on_search_change: rx.EventHandler[lambda value: [value]]


tags_input = TagsInput.create

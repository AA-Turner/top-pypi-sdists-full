"""Mantines Dates."""

from typing import Callable, Literal, TypedDict

import reflex as rx
from reflex.components.component import Component

from reflex_enterprise.components.component import ComponentEnterprise

from .base import (
    MantineDescriptionProps,
    MantineErrorProps,
    MantineLabelProps,
    MantineLeftSection,
    MantineRightSection,
    MemoizedMantineProvider,
)

MANTINE_DATES_PACKAGE = "@mantine/dates"
MANTINE_DATES_VERSION = "8.3.9"


class MantineDates(ComponentEnterprise):
    """Mantine Dates component."""

    library = f"{MANTINE_DATES_PACKAGE}@{MANTINE_DATES_VERSION}"

    lib_dependencies: list[str] = ["dayjs@1.11.19"]

    def add_imports(self):
        """Add import for Mantine Dates component."""
        return {
            "": [
                "@mantine/core/styles.css",
                "@mantine/dates/styles.css",
            ],
            "dayjs": [rx.ImportVar(tag="dayjs", is_default=True)],
        }

    @staticmethod
    def _get_app_wrap_components() -> dict[tuple[int, str], Component]:
        return {
            (44, "MantineProvider"): MemoizedMantineProvider.create(),
        }


class CalendarEvents(ComponentEnterprise):
    """Events for Calendar component."""

    on_change: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when date changes
    on_date_change: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when level changes
    on_level_change: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when user selects month
    on_month_select: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when the next decade button is clicked
    on_next_decade: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when the next month button is clicked
    on_next_month: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when the next year button is clicked
    on_next_year: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when the previous decade button is clicked
    on_previous_decade: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when the previous month button is clicked
    on_previous_month: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when the previous year button is clicked
    on_previous_year: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when mouse enters year control
    on_year_control_mouse_enter: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Called when user selects year
    on_year_select: rx.EventHandler[rx.event.passthrough_event_spec(str)]


class PresetEntry(TypedDict):
    """Preset entry for date picker."""

    value: str | tuple[str, str]
    label: str


class SharedCalendarProps(ComponentEnterprise):
    """Shared props for Calendar and DatePicker components."""

    # aria-label attributes for controls on different levels
    aria_labels: rx.Var[dict[str, str]]

    # Number of columns to scroll with next/prev buttons, same as numberOfColumns if not set explicitly
    columns_to_scroll: rx.Var[int]

    # Displayed date in controlled mode
    date: rx.Var[str]

    # dayjs format for decade label or a function that returns decade label based on the date value, "YYYY" by default
    decade_label_format: rx.Var[str]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]

    # Initial displayed level in uncontrolled mode
    default_level: rx.Var[Literal["decade", "year", "month"]]

    # Number 0-6, where 0 - Sunday and 6 - Saturday. 1 - Monday by default
    first_day_of_week: rx.Var[int]

    # Assigns aria-label to Day components based on date
    get_day_aria_label: rx.Var[Callable]

    # Passes props down to Day components
    get_day_props: rx.Var[Callable]

    # Passes props down month picker control
    get_month_control_props: rx.Var[Callable]

    # Passes props down to year picker control based on date
    get_year_control_props: rx.Var[Callable]

    # Determines whether outside dates should be hidden, false by default
    hide_outside_dates: rx.Var[bool]

    # Determines whether outside months should be hidden, false by default
    hide_weekdays: rx.Var[bool]

    # Determines whether today should be highlighted with a border, false by default
    highlight_today: rx.Var[bool]

    # Current displayed level displayed in controlled mode
    level: rx.Var[Literal["decade", "year", "month"]]

    # Dayjs locale, defaults to value defined in DatesProvider
    locale: rx.Var[str]

    # Maximum possible date in YYYY-MM-DD format or Date object
    max_date: rx.Var[str]

    # Max level that user can go up to (decade, year, month), defaults to decade
    max_level: rx.Var[Literal["decade", "year", "month"]]

    # Minimum possible date in YYYY-MM-DD format or Date object
    min_date: rx.Var[str]

    # Minimum level that user can go down to (decade, year, month), defaults to month
    min_level: rx.Var[Literal["decade", "year", "month"]]

    # dayjs label format to display month label or a function that returns month label based on month value, "MMMM YYYY"
    month_label_format: rx.Var[str]

    # dayjs format for months list
    month_format: rx.Var[str]

    # Change next icon
    next_icon: rx.Var[Component]

    # Next button aria-label
    next_label: rx.Var[str]

    # Number of columns displayed next to each other, 1 by default
    number_of_columns: rx.Var[int]

    # Presets for quick date selection
    presets: rx.Var[list[PresetEntry]]

    # Change previous icon
    previous_icon: rx.Var[Component]

    # Previous button aria-label
    previous_label: rx.Var[str]

    # Controls day value rendering
    render_day: rx.Var[Callable]

    # Component size
    size: rx.Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # dayjs format for weekdays names, 'dd' by default
    weekday_format: rx.Var[str]

    # Indices of weekend days, 0-6, where 0 is Sunday and 6 is Saturday. The default value is defined by DatesProvider
    weekend_days: rx.Var[list[int]]

    # Determines whether controls should be separated, true by default
    with_cell_spacing: rx.Var[bool]

    # Determines whether week numbers should be displayed, false by default
    with_week_numbers: rx.Var[bool]

    # dayjs label format to display year label or a function that returns year label based on year value, "YYYY" by default
    year_label_format: rx.Var[str]

    # dayjs format for years list
    year_list_format: rx.Var[str]


class BareCalendar(
    MantineDates,
    SharedCalendarProps,
    CalendarEvents,
):
    """BareCalendar component."""


class Calendar(BareCalendar):
    """Calendar component."""

    tag = "Calendar"

    alias = "MantineCalendar"

    # Determines whether next level button should be enabled, true by default
    has_next_level: rx.Var[bool]

    # Called when mouse enters month control
    on_month_control_mouse_enter: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Determines whether days should be static, static days can be used to display month if it is not expected that user will interact with the component in any way
    static: rx.Var[bool]


class BareCalendarPicker(
    BareCalendar,
    MantineLabelProps,
    MantineErrorProps,
    MantineDescriptionProps,
    MantineLeftSection,
    MantineRightSection,
):
    """BareCalendarPicker component."""

    placeholder: rx.Var[str]


class DateTimePicker(BareCalendarPicker):
    """DateTimePicker component."""

    tag = "DateTimePicker"

    alias = "MantineDateTimePicker"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Determines whether user can deselect the date by clicking on selected item, applicable only when type="default"
    allow_deselect: rx.Var[bool]

    # Determines whether a single day can be selected as range, applicable only when type="range"
    allow_single_day_range: rx.Var[bool]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]

    # dayjs format for decade label or a function that returns decade label based on the date value, "YYYY" by default
    decade_label_format: rx.Var[str]

    # Number 0-6, where 0 - Sunday and 6 - Saturday. 1 - Monday by default
    first_day_of_week: rx.Var[int]

    # Passes props down to Day components
    get_day_props: rx.Var[Callable]


class DatePicker(BareCalendarPicker):
    """DatePicker component."""

    tag = "DatePicker"

    alias = "MantineDatePicker"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Picker type: range, multiple or default
    type: rx.Var[Literal["range", "multiple", "default"]]

    # Determines whether a single day can be selected as range, applicable only when type="range"
    allow_single_day_range: rx.Var[bool]


class DatePickerInput(BareCalendarPicker):
    """DatePickerInput component."""

    tag = "DatePickerInput"

    alias = "MantineDatePickerInput"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Picker type: range, multiple or default
    type: rx.Var[Literal["range", "multiple", "default"]]

    # Determines whether the dropdown is closed when date is selected, not applicable with type="multiple", true by default
    close_on_change: rx.Var[bool]

    # Determines whether a single day can be selected as range, applicable only when type="range"
    allow_single_day_range: rx.Var[bool]


class DateInput(BareCalendarPicker):
    """DateInput component."""

    tag = "DateInput"

    alias = "MantineDateInput"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Determines whether the dropdown is closed when date is selected, not applicable with type="multiple", true by default
    close_on_change: rx.Var[bool]

    # Determines whether a single day can be selected as range, applicable only when type="range"
    allow_single_day_range: rx.Var[bool]


class MonthPicker(BareCalendarPicker):
    """MonthPicker component."""

    tag = "MonthPicker"

    alias = "MantineMonthPicker"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]


class MonthPickerInput(BareCalendarPicker):
    """MonthPickerInput component."""

    tag = "MonthPickerInput"

    alias = "MantineMonthPickerInput"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]


class YearPicker(BareCalendarPicker):
    """YearPicker component."""

    tag = "YearPicker"

    alias = "MantineYearPicker"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]


class YearPickerInput(BareCalendarPicker):
    """YearPickerInput component."""

    tag = "YearPickerInput"

    alias = "MantineYearPickerInput"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]


class TimeInput(BareCalendarPicker):
    """TimeInput component."""

    tag = "TimeInput"

    alias = "MantineTimeInput"

    on_change: rx.EventHandler[rx.event.input_event]


class TimePicker(BareCalendarPicker):
    """TimePicker component."""

    tag = "TimePicker"

    alias = "MantineTimePicker"

    # Displayed date in controlled mode
    date: rx.Var[str]

    # Initial displayed date in uncontrolled mode
    default_date: rx.Var[str]


class TimeGrid(BareCalendarPicker):
    """TimeGrid component."""

    tag = "TimeGrid"

    alias = "MantineTimeGrid"

    # Time data in 24h format to be displayed in the grid, for example ['10:00', '18:30', '22:00']. Time values must be unique.
    data: rx.Var[list[str]]


class TimeValue(MantineDates):
    """TimeValue component."""

    tag = "TimeValue"

    alias = "MantineTimeValue"

    # AM/PM labels, { am: 'AM', pm: 'PM' } by default
    am_pm_labels: rx.Var[dict[Literal["am", "pm"], str]]

    # Time format, '24h' by default
    format: rx.Var[Literal["12h", "24h"]]

    # Time to format
    value: rx.Var[str]

    # Determines whether seconds should be displayed, false by default
    with_seconds: rx.Var[bool]


class DatesNamespace(rx.ComponentNamespace):
    """Namespace for Mantine Dates components."""

    calendar = staticmethod(Calendar.create)
    date_time_picker = staticmethod(DateTimePicker.create)
    date_picker = staticmethod(DatePicker.create)
    date_picker_input = staticmethod(DatePickerInput.create)
    date_input = staticmethod(DateInput.create)
    month_picker = staticmethod(MonthPicker.create)
    month_picker_input = staticmethod(MonthPickerInput.create)
    year_picker = staticmethod(YearPicker.create)
    year_picker_input = staticmethod(YearPickerInput.create)
    time_input = staticmethod(TimeInput.create)
    time_picker = staticmethod(TimePicker.create)
    time_grid = staticmethod(TimeGrid.create)
    time_value = staticmethod(TimeValue.create)


dates = DatesNamespace()

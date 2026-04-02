"""
Widget type determination for parameter-to-UI mapping.

Determines the appropriate UI widget for a given Homematic parameter
based on its type, range, and metadata.

Public API of this module is defined by __all__.
"""

from enum import StrEnum, unique
import inspect

from aiohomematic.const import ParameterData, ParameterType

from aiohomematic_config.const import RADIO_GROUP_THRESHOLD, SLIDER_RANGE_THRESHOLD


@unique
class WidgetType(StrEnum):
    """UI widget types for parameter rendering."""

    TOGGLE = "toggle"
    SLIDER_WITH_INPUT = "slider_with_input"
    NUMBER_INPUT = "number_input"
    RADIO_GROUP = "radio_group"
    DROPDOWN = "dropdown"
    TEXT_INPUT = "text_input"
    BUTTON = "button"
    READ_ONLY = "read_only"


def determine_widget(*, parameter_data: ParameterData) -> WidgetType:
    """
    Determine the appropriate UI widget for a parameter.

    Mapping logic:
    - BOOL                           -> TOGGLE
    - INTEGER (range <= 20)          -> SLIDER_WITH_INPUT
    - INTEGER (range > 20)           -> NUMBER_INPUT
    - FLOAT (range <= 100)           -> SLIDER_WITH_INPUT
    - FLOAT (range > 100)            -> NUMBER_INPUT
    - ENUM (options <= 4)            -> RADIO_GROUP
    - ENUM (options > 4)             -> DROPDOWN
    - STRING                         -> TEXT_INPUT
    - ACTION                         -> BUTTON
    """
    param_type = parameter_data.get("TYPE", ParameterType.EMPTY)

    if param_type == ParameterType.BOOL:
        return WidgetType.TOGGLE

    if param_type == ParameterType.INTEGER:
        p_min = parameter_data.get("MIN", 0)
        p_max = parameter_data.get("MAX", 0)
        if (
            isinstance(p_min, (int, float))
            and isinstance(p_max, (int, float))
            and abs(p_max - p_min) <= SLIDER_RANGE_THRESHOLD
        ):
            return WidgetType.SLIDER_WITH_INPUT
        return WidgetType.NUMBER_INPUT

    if param_type == ParameterType.FLOAT:
        p_min = parameter_data.get("MIN", 0.0)
        p_max = parameter_data.get("MAX", 0.0)
        if (
            isinstance(p_min, (int, float))
            and isinstance(p_max, (int, float))
            and abs(float(p_max) - float(p_min)) <= 100.0
        ):
            return WidgetType.SLIDER_WITH_INPUT
        return WidgetType.NUMBER_INPUT

    if param_type == ParameterType.ENUM:
        value_list = parameter_data.get("VALUE_LIST", [])
        if len(tuple(value_list)) <= RADIO_GROUP_THRESHOLD:
            return WidgetType.RADIO_GROUP
        return WidgetType.DROPDOWN

    if param_type == ParameterType.STRING:
        return WidgetType.TEXT_INPUT

    if param_type == ParameterType.ACTION:
        return WidgetType.BUTTON

    return WidgetType.READ_ONLY


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)

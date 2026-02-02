"""
CSSL GUI Builder - Widget type registry and property definitions.
Single source of truth for all widget metadata.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Any, Tuple, Dict, Optional


class WidgetCategory(Enum):
    WINDOW = "Window"
    DISPLAY = "Display"
    INPUT = "Input"
    DATA = "Data"
    TIME = "Time & Date"
    CONTAINER = "Container"
    NAVIGATION = "Navigation"


class CsslWidgetType(Enum):
    WIDGET = "CsslWidget"
    LABEL = "CsslLabel"
    BUTTON = "CsslButton"
    PICTURE = "CsslPicture"
    INPUT_FIELD = "CsslInputField"
    TEXT_AREA = "CsslTextArea"
    CHECK_BOX = "CsslCheckBox"
    RADIO_BUTTON = "CsslRadioButton"
    COMBO_BOX = "CsslComboBox"
    SLIDER = "CsslSlider"
    PROGRESS_BAR = "CsslProgressBar"
    LIST_BOX = "CsslListBox"
    TABLE = "CsslTable"
    TIME_PICKER = "CsslTimePicker"
    DATE_PICKER = "CsslDatePicker"
    TAB_CONTROL = "CsslTabControl"
    SCROLL_PANEL = "CsslScrollPanel"
    SEPARATOR = "CsslSeparator"
    MENU_BAR = "CsslMenuBar"
    TOOLBAR = "CsslToolbar"


@dataclass
class PropertyDef:
    """Definition of a single widget property."""
    name: str
    display_name: str
    prop_type: str  # "string", "int", "float", "bool", "color", "list", "choice", "items"
    default: Any = None
    choices: List[str] = field(default_factory=list)
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    cssl_setter: str = ""  # e.g. "setText" -> this->Widget.setText(value)
    constructor_param: str = ""  # Parameter name in constructor if applicable
    constructor_index: int = -1  # Position in constructor args (-1 = not a constructor param)


@dataclass
class WidgetTypeDef:
    """Complete definition of a CSSL widget type."""
    widget_type: CsslWidgetType
    category: WidgetCategory
    display_name: str
    icon: str
    default_size: Tuple[int, int]
    properties: List[PropertyDef] = field(default_factory=list)
    has_parent: bool = True
    is_container: bool = False
    parent_is_first_arg: bool = True  # Most widgets take parent as first constructor arg


# ---------------------------------------------------------------------------
# Common property templates
# ---------------------------------------------------------------------------

def _text_prop(default: str = "", setter: str = "setText", constr_param: str = "text",
               constr_idx: int = -1) -> PropertyDef:
    return PropertyDef("text", "Text", "string", default, cssl_setter=setter,
                       constructor_param=constr_param, constructor_index=constr_idx)


def _checked_prop() -> PropertyDef:
    return PropertyDef("checked", "Checked", "bool", False, cssl_setter="setChecked",
                       constructor_param="checked", constructor_index=2)


def _items_prop() -> PropertyDef:
    return PropertyDef("items", "Items", "items", [], cssl_setter="setItems",
                       constructor_param="items", constructor_index=1)


def _orientation_prop(default: str = "horizontal") -> PropertyDef:
    return PropertyDef("orientation", "Orientation", "choice", default,
                       choices=["horizontal", "vertical"], cssl_setter="setOrientation",
                       constructor_param="orientation")


def _color_fg_prop() -> PropertyDef:
    return PropertyDef("fg_color", "Foreground", "color", "", cssl_setter="setColor")


def _color_bg_prop() -> PropertyDef:
    return PropertyDef("bg_color", "Background", "color", "", cssl_setter="")


def _font_family_prop() -> PropertyDef:
    return PropertyDef("font_family", "Font Family", "string", "", cssl_setter="setFont")


def _font_size_prop() -> PropertyDef:
    return PropertyDef("font_size", "Font Size", "int", 0, min_val=0, max_val=200,
                       cssl_setter="setFont")


def _readonly_prop() -> PropertyDef:
    return PropertyDef("readonly", "Read Only", "bool", False, cssl_setter="setReadOnly")


def _placeholder_prop() -> PropertyDef:
    return PropertyDef("placeholder", "Placeholder", "string", "",
                       cssl_setter="setPlaceholderText")


def _max_length_prop() -> PropertyDef:
    return PropertyDef("max_length", "Max Length", "int", 0, min_val=0, max_val=100000,
                       cssl_setter="setMaxLength")


def _enabled_prop() -> PropertyDef:
    return PropertyDef("enabled", "Enabled", "bool", True, cssl_setter="setEnabled")


def _tooltip_prop() -> PropertyDef:
    return PropertyDef("tooltip", "Tooltip", "string", "", cssl_setter="setTooltip")


def _alignment_prop() -> PropertyDef:
    return PropertyDef("alignment", "Alignment", "choice", "left",
                       choices=["left", "center", "right"], cssl_setter="setAlignment")


def _bold_prop() -> PropertyDef:
    return PropertyDef("bold", "Bold", "bool", False, cssl_setter="setFont")


def _thickness_prop() -> PropertyDef:
    return PropertyDef("thickness", "Thickness", "int", 2, min_val=1, max_val=20,
                       cssl_setter="setThickness")


# ---------------------------------------------------------------------------
# Widget Registry
# ---------------------------------------------------------------------------

WIDGET_REGISTRY: Dict[CsslWidgetType, WidgetTypeDef] = {
    CsslWidgetType.WIDGET: WidgetTypeDef(
        widget_type=CsslWidgetType.WIDGET,
        category=WidgetCategory.WINDOW,
        display_name="Window",
        icon="\u25a3",  # filled square
        default_size=(800, 600),
        has_parent=False,
        is_container=True,
        parent_is_first_arg=False,
        properties=[
            PropertyDef("title", "Title", "string", "CSSL Application",
                        constructor_param="title", constructor_index=0),
            PropertyDef("bg_color", "Background", "color", "",
                        constructor_param="bg_color", constructor_index=3),
        ],
    ),
    CsslWidgetType.LABEL: WidgetTypeDef(
        widget_type=CsslWidgetType.LABEL,
        category=WidgetCategory.DISPLAY,
        display_name="Label",
        icon="\u0041",  # A
        default_size=(120, 25),
        properties=[
            _text_prop("Label", constr_idx=1),
            _color_fg_prop(),
            _color_bg_prop(),
            _font_family_prop(),
            _font_size_prop(),
            _alignment_prop(),
            _bold_prop(),
        ],
    ),
    CsslWidgetType.BUTTON: WidgetTypeDef(
        widget_type=CsslWidgetType.BUTTON,
        category=WidgetCategory.INPUT,
        display_name="Button",
        icon="\u25a2",  # white square with rounded corners
        default_size=(100, 30),
        properties=[
            _text_prop("Button", constr_idx=1),
            _color_fg_prop(),
            _color_bg_prop(),
            _font_size_prop(),
            _enabled_prop(),
            _tooltip_prop(),
        ],
    ),
    CsslWidgetType.PICTURE: WidgetTypeDef(
        widget_type=CsslWidgetType.PICTURE,
        category=WidgetCategory.DISPLAY,
        display_name="Picture",
        icon="\u25a6",  # square with pattern
        default_size=(200, 150),
        properties=[
            PropertyDef("image_path", "Image Path", "string", "",
                        cssl_setter="loadImage", constructor_param="image_path",
                        constructor_index=1),
        ],
    ),
    CsslWidgetType.INPUT_FIELD: WidgetTypeDef(
        widget_type=CsslWidgetType.INPUT_FIELD,
        category=WidgetCategory.INPUT,
        display_name="Input Field",
        icon="\u2500",  # horizontal line
        default_size=(200, 28),
        properties=[
            _text_prop("", constr_idx=1),
            _placeholder_prop(),
            _max_length_prop(),
            _readonly_prop(),
            _color_fg_prop(),
            _color_bg_prop(),
        ],
    ),
    CsslWidgetType.TEXT_AREA: WidgetTypeDef(
        widget_type=CsslWidgetType.TEXT_AREA,
        category=WidgetCategory.INPUT,
        display_name="Text Area",
        icon="\u2261",  # identical to / triple bar
        default_size=(300, 200),
        properties=[
            _text_prop("", constr_idx=1),
            _readonly_prop(),
            PropertyDef("wrap", "Wrap Mode", "choice", "word",
                        choices=["word", "char", "none"], cssl_setter="setWrap"),
            _color_fg_prop(),
            _color_bg_prop(),
            _font_family_prop(),
            _font_size_prop(),
        ],
    ),
    CsslWidgetType.CHECK_BOX: WidgetTypeDef(
        widget_type=CsslWidgetType.CHECK_BOX,
        category=WidgetCategory.INPUT,
        display_name="Checkbox",
        icon="\u2611",  # ballot box with check
        default_size=(150, 25),
        properties=[
            _text_prop("Checkbox", constr_idx=1),
            _checked_prop(),
        ],
    ),
    CsslWidgetType.RADIO_BUTTON: WidgetTypeDef(
        widget_type=CsslWidgetType.RADIO_BUTTON,
        category=WidgetCategory.INPUT,
        display_name="Radio Button",
        icon="\u25c9",  # fisheye
        default_size=(150, 25),
        properties=[
            _text_prop("Option", constr_idx=1),
            PropertyDef("group", "Group", "string", "default",
                        constructor_param="group", constructor_index=2),
            PropertyDef("value", "Value", "string", "",
                        constructor_param="value", constructor_index=3),
        ],
    ),
    CsslWidgetType.COMBO_BOX: WidgetTypeDef(
        widget_type=CsslWidgetType.COMBO_BOX,
        category=WidgetCategory.INPUT,
        display_name="Combo Box",
        icon="\u25be",  # down triangle
        default_size=(180, 28),
        properties=[
            _items_prop(),
        ],
    ),
    CsslWidgetType.SLIDER: WidgetTypeDef(
        widget_type=CsslWidgetType.SLIDER,
        category=WidgetCategory.INPUT,
        display_name="Slider",
        icon="\u2194",  # left-right arrow
        default_size=(200, 40),
        properties=[
            PropertyDef("min_val", "Min", "int", 0, min_val=-100000, max_val=100000,
                        constructor_param="min_val", constructor_index=1),
            PropertyDef("max_val", "Max", "int", 100, min_val=-100000, max_val=100000,
                        constructor_param="max_val", constructor_index=2),
            PropertyDef("value", "Value", "int", 0, min_val=-100000, max_val=100000,
                        cssl_setter="setValue", constructor_param="value", constructor_index=3),
            _orientation_prop(),
        ],
    ),
    CsslWidgetType.PROGRESS_BAR: WidgetTypeDef(
        widget_type=CsslWidgetType.PROGRESS_BAR,
        category=WidgetCategory.DISPLAY,
        display_name="Progress Bar",
        icon="\u25ac",  # black rectangle
        default_size=(200, 25),
        properties=[
            PropertyDef("value", "Value", "int", 0, min_val=0, max_val=100000,
                        cssl_setter="setValue", constructor_param="value", constructor_index=1),
            PropertyDef("max_val", "Max", "int", 100, min_val=1, max_val=100000,
                        cssl_setter="setMax", constructor_param="max_val", constructor_index=2),
            PropertyDef("mode", "Mode", "choice", "determinate",
                        choices=["determinate", "indeterminate"],
                        cssl_setter="setMode", constructor_param="mode", constructor_index=3),
        ],
    ),
    CsslWidgetType.LIST_BOX: WidgetTypeDef(
        widget_type=CsslWidgetType.LIST_BOX,
        category=WidgetCategory.DATA,
        display_name="List Box",
        icon="\u2630",  # trigram
        default_size=(200, 200),
        properties=[
            _items_prop(),
            PropertyDef("multi_select", "Multi-Select", "bool", False,
                        cssl_setter="setMultiSelect"),
        ],
    ),
    CsslWidgetType.TABLE: WidgetTypeDef(
        widget_type=CsslWidgetType.TABLE,
        category=WidgetCategory.DATA,
        display_name="Table",
        icon="\u2637",  # trigram for earth
        default_size=(400, 250),
        properties=[
            PropertyDef("columns", "Columns", "items", [],
                        cssl_setter="setColumns", constructor_param="columns",
                        constructor_index=1),
        ],
    ),
    CsslWidgetType.TIME_PICKER: WidgetTypeDef(
        widget_type=CsslWidgetType.TIME_PICKER,
        category=WidgetCategory.TIME,
        display_name="Time Picker",
        icon="\u23f0",  # alarm clock
        default_size=(150, 30),
        properties=[
            PropertyDef("hour", "Hour", "int", 0, min_val=0, max_val=23,
                        constructor_param="hour", constructor_index=1),
            PropertyDef("minute", "Minute", "int", 0, min_val=0, max_val=59,
                        constructor_param="minute", constructor_index=2),
            PropertyDef("second", "Second", "int", 0, min_val=0, max_val=59,
                        constructor_param="second", constructor_index=3),
            PropertyDef("show_seconds", "Show Seconds", "bool", True,
                        constructor_param="show_seconds", constructor_index=4),
        ],
    ),
    CsslWidgetType.DATE_PICKER: WidgetTypeDef(
        widget_type=CsslWidgetType.DATE_PICKER,
        category=WidgetCategory.TIME,
        display_name="Date Picker",
        icon="\U0001f4c5",  # calendar
        default_size=(150, 30),
        properties=[
            PropertyDef("year", "Year", "int", 2025, min_val=1900, max_val=2100,
                        constructor_param="year", constructor_index=1),
            PropertyDef("month", "Month", "int", 1, min_val=1, max_val=12,
                        constructor_param="month", constructor_index=2),
            PropertyDef("day", "Day", "int", 1, min_val=1, max_val=31,
                        constructor_param="day", constructor_index=3),
        ],
    ),
    CsslWidgetType.TAB_CONTROL: WidgetTypeDef(
        widget_type=CsslWidgetType.TAB_CONTROL,
        category=WidgetCategory.CONTAINER,
        display_name="Tab Control",
        icon="\u2b12",  # square with top half black
        default_size=(400, 300),
        is_container=True,
        properties=[],
    ),
    CsslWidgetType.SCROLL_PANEL: WidgetTypeDef(
        widget_type=CsslWidgetType.SCROLL_PANEL,
        category=WidgetCategory.CONTAINER,
        display_name="Scroll Panel",
        icon="\u21f3",  # up down arrow with double stroke
        default_size=(300, 200),
        is_container=True,
        properties=[
            PropertyDef("scroll_x", "Scroll X", "bool", False,
                        constructor_param="scroll_x", constructor_index=1),
            PropertyDef("scroll_y", "Scroll Y", "bool", True,
                        constructor_param="scroll_y", constructor_index=2),
        ],
    ),
    CsslWidgetType.SEPARATOR: WidgetTypeDef(
        widget_type=CsslWidgetType.SEPARATOR,
        category=WidgetCategory.DISPLAY,
        display_name="Separator",
        icon="\u2500",
        default_size=(200, 4),
        properties=[
            _orientation_prop(),
            PropertyDef("color", "Color", "color", "", cssl_setter="setColor"),
            _thickness_prop(),
        ],
    ),
    CsslWidgetType.MENU_BAR: WidgetTypeDef(
        widget_type=CsslWidgetType.MENU_BAR,
        category=WidgetCategory.NAVIGATION,
        display_name="Menu Bar",
        icon="\u2630",
        default_size=(0, 25),  # Spans full width, auto-positioned
        properties=[
            PropertyDef("menus", "Menus", "menu_structure", [],
                         cssl_setter="addMenu"),
        ],
    ),
    CsslWidgetType.TOOLBAR: WidgetTypeDef(
        widget_type=CsslWidgetType.TOOLBAR,
        category=WidgetCategory.NAVIGATION,
        display_name="Toolbar",
        icon="\u2338",  # APL functional symbol
        default_size=(0, 40),  # Spans full width
        properties=[
            PropertyDef("slots", "Slots", "toolbar_slots", [],
                         cssl_setter="addSlot"),
        ],
    ),
}


def get_widget_def(widget_type: CsslWidgetType) -> WidgetTypeDef:
    """Get the widget type definition."""
    return WIDGET_REGISTRY[widget_type]


def get_widgets_by_category() -> Dict[WidgetCategory, List[WidgetTypeDef]]:
    """Get all widget types grouped by category. Excludes WINDOW category."""
    result: Dict[WidgetCategory, List[WidgetTypeDef]] = {}
    for typedef in WIDGET_REGISTRY.values():
        if typedef.category == WidgetCategory.WINDOW:
            continue
        cat = typedef.category
        if cat not in result:
            result[cat] = []
        result[cat].append(typedef)
    return result


def cssl_type_from_string(type_str: str) -> Optional[CsslWidgetType]:
    """Convert a CSSL type string like 'CsslButton' to CsslWidgetType enum."""
    for wt in CsslWidgetType:
        if wt.value == type_str:
            return wt
    return None

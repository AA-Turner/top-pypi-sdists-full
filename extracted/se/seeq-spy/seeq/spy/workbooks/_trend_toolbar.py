from __future__ import annotations

import textwrap
from typing import List, Dict

import pandas as pd

from seeq.spy import _common
from seeq.spy._common import docstring_parameter
from seeq.spy._errors import *
from seeq.spy.workbooks._context_switchable import ContextSwitchable


# Refer client/packages/webserver/app/src/trend/toolbar/TrendToolbar.organism.tsx
class TrendToolbar(ContextSwitchable):
    """
    The configuration options for the Trend Toolbar of a worksheet in an Analysis. It can be used to change trend
    options such as modify the trend view mode, show grid lines, hide uncertainty, enable dimming, pick labels,
    customize colors, and more.
    """

    class CONSTANTS:
        TREND_STORE_NAME = "sqTrendStore"
        SHOW_GRIDLINES = "showGridlines"
        HIDE_UNCERTAINTY = "hideUncertainty"
        HIDE_UNSELECTED_ITEMS = "hideUnselectedItems"

    def __init__(self, parent):
        self._parent = parent
        self._labels = Labels(parent)
        self._color = Color(parent)
        super().__init__(parent)

    @property
    def view(self) -> str:
        """
        The current view for the workstep. Valid values are

        ============ =========================================
        View         Result
        ============ =========================================
        Trend        Show the time-series trend view (default)
        Scatter Plot Show the scatter plot view
        Treemap      Show the treemap view
        Table        Show the table view
        ============ =========================================
        """
        return self._getter_workstep.view

    @view.setter
    def view(self, value: str):
        self._setter_workstep.view = value

    @property
    def show_grid_lines(self) -> bool:
        """
        The boolean value indicating grid line visibility. Can be either True or False.
        """
        return self._get_show_grid_lines()

    @show_grid_lines.setter
    def show_grid_lines(self, value: bool):
        self._set_show_grid_lines(value)

    @property
    def hide_uncertainty(self) -> bool:
        """
        The boolean value indicating whether uncertainty indicators are hidden.
        Can be either True or False.
        """
        return self._get_hide_uncertainty()

    @hide_uncertainty.setter
    def hide_uncertainty(self, value: bool):
        self._set_hide_uncertainty(value)

    @property
    def dimming(self) -> bool:
        """
        The boolean value indicating whether only items selected in the details
        pane should be displayed on the trend. Can be either True or False.
        """
        return self._get_dimming()

    @dimming.setter
    def dimming(self, value: bool):
        self._set_dimming(value)

    @property
    def labels(self) -> Labels:
        """
        Labels configuration of the TrendToolbar.
        """
        return self._get_labels()

    @property
    def color(self) -> Color:
        """
        Color configuration of the TrendToolbar.
        """
        return self._get_color()

    def _get_store(self, workstep, store_name):
        workstep_stores = workstep.get_workstep_stores()
        return _common.get(workstep_stores, store_name, default=dict(), assign_default=True)

    def _get_show_grid_lines(self) -> bool:
        """
        Get the grid line visibility of the current workstep.

        :return: boolean
        """
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        return _common.get(trend_store, self.CONSTANTS.SHOW_GRIDLINES, default=False, assign_default=True)

    def _set_show_grid_lines(self, value: bool):
        """
        Set the visibility of grid lines for the current workstep.
        """
        if isinstance(value, bool):
            trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)
            trend_store[self.CONSTANTS.SHOW_GRIDLINES] = value
        else:
            raise SPyTypeError("'show_grid_lines' must be a boolean")

    def _get_hide_uncertainty(self) -> bool:
        """
        Get a boolean indicating whether uncertainty indicators are hidden for the current workstep.

        :return: boolean
        """
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        return _common.get(trend_store, self.CONSTANTS.HIDE_UNCERTAINTY, default=False, assign_default=True)

    def _set_hide_uncertainty(self, value: bool):
        """
        Set the visibility of uncertainty indicators for the current workstep.
        """
        if isinstance(value, bool):
            trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)
            trend_store[self.CONSTANTS.HIDE_UNCERTAINTY] = value
        else:
            raise SPyTypeError("'hide_uncertainty' must be a boolean")

    def _get_dimming(self) -> bool:
        """
        Get the dimming status of the current workstep.

        :return: boolean
        """
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        return _common.get(trend_store, self.CONSTANTS.HIDE_UNSELECTED_ITEMS, default=False, assign_default=True)

    def _set_dimming(self, value: bool):
        """
        Set the dimming status of the current workstep.
        """
        if isinstance(value, bool):
            trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)
            trend_store[self.CONSTANTS.HIDE_UNSELECTED_ITEMS] = value
        else:
            raise SPyTypeError("'dimming' must be a boolean")

    def _get_labels(self) -> Labels:
        """
        Get the labels visibility configuration of the current workstep.
        :return: Labels
        """
        return self._labels

    def _get_color(self) -> Color:
        """
        Get the color configuration of the current workstep.
        :return: Color
        """
        return self._color

    def __repr__(self):
        return (
            f"Trend toolbar configurations:\n"
            f"  - View: {self.view}\n"
            f"  - Show Gridlines: {self.show_grid_lines}\n"
            f"  - Hide Uncertainty: {self.hide_uncertainty}\n"
            f"  - Dimming: {self.dimming}\n"
            f"{textwrap.indent(f'- {repr(self.labels)}', prefix='  ')}\n"
            f"{textwrap.indent(f'- {repr(self.color)}', prefix='  ')}\n"
        )


# Refer client/packages/webserver/app/src/trend/toolbar/LabelsPopover.organism.tsx
class Labels(ContextSwitchable):
    """
    The configuration options for labeling trends in the worksheet or current workstep of an Analysis.
    """

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self._signals = Signals(parent)
        self._conditions = Conditions(parent)
        self._cursors = Cursors(parent)

    @property
    def signals(self) -> Signals:
        """
        Labels configuration for Signals.
        """
        return self._signals

    @property
    def conditions(self) -> Conditions:
        """
        Labels configuration for Conditions.
        """
        return self._conditions

    @property
    def cursors(self) -> Cursors:
        """
        Labels configuration for Cursors.
        """
        return self._cursors

    def __repr__(self):
        return ("Labels:\n" +
                textwrap.indent(
                    f"- {repr(self.signals)}\n"
                    f"- {repr(self.conditions)}\n"
                    f"- {repr(self.cursors)}",
                    prefix="  "
                ))


# Refer LABEL_LOCATIONS in client/packages/webserver/app/src/trendData/trendData.constants.ts
# Refer LABEL_PROPERTIES in client/packages/webserver/app/src/trendData/trendData.constants.ts
# Refer client/packages/webserver/app/src/trend/toolbar/SignalLabelSelection.molecule.tsx
class Signals(ContextSwitchable):
    """
    The configuration options for labeling signals in the worksheet or current workstep of an Analysis.
    """

    class CONSTANTS:
        OFF = "off"
        LANE = "lane"
        AXIS = "axis"
        TREND_STORE_NAME = "sqTrendStore"
        LABEL_DISPLAY_CONFIGURATION = "labelDisplayConfiguration"
        NAME = "name"
        DESCRIPTION = "description"
        ASSET = "asset"
        ASSET_PATH_LEVELS = "assetPathLevels"
        LINE = "line"
        UNIT_OF_MEASURE = "unitOfMeasure"
        CUSTOM = "custom"
        CUSTOM_LABELS = "customLabels"

    _valid_labels = {CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS}

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS)
    def name(self) -> str:
        """
        The string value indication Signals Name visibility.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_name()

    @name.setter
    def name(self, value: str):
        self._set_name(value)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS)
    def description(self) -> str:
        """
        The string value indication Signals Description visibility.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_description()

    @description.setter
    def description(self, value: str):
        self._set_description(value)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS)
    def asset(self) -> str:
        """
        The string value indication Signals Asset visibility.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_asset()

    @asset.setter
    def asset(self, value: str):
        self._set_asset(value)

    @property
    def asset_path_levels(self) -> int:
        """
        The integer value indication Signals Asset Path Levels visibility.
        """
        return self._get_asset_path_levels()

    @asset_path_levels.setter
    def asset_path_levels(self, value: int):
        self._set_asset_path_levels(value)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS)
    def line_style(self) -> str:
        """
        The string value indication Signals Line Style visibility.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_line_style()

    @line_style.setter
    def line_style(self, value: str):
        self._set_line_style(value)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS)
    def unit_of_measure(self) -> str:
        """
        The string value indication Signals Unit Of Measure visibility.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_unit_of_measure()

    @unit_of_measure.setter
    def unit_of_measure(self, value: str):
        self._set_unit_of_measure(value)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE, CONSTANTS.AXIS)
    def custom(self) -> str:
        """
        The string value indication Signals Custom Labels visibility.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_custom()

    @custom.setter
    def custom(self, value: str):
        self._set_custom(value)

    @property
    @docstring_parameter(CONSTANTS.LANE, CONSTANTS.AXIS)
    def custom_labels(self) -> List[str]:
        """
        A list of strings representing custom labels for '{0}' or '{1}' based on the custom property.
        """
        return self._get_custom_labels()

    @custom_labels.setter
    def custom_labels(self, value: List[str]):
        self._set_custom_labels(value)

    def _get_store(self, workstep, store_name):
        workstep_stores = workstep.get_workstep_stores()
        return _common.get(workstep_stores, store_name, default=dict(), assign_default=True)

    def _get_trend_store_label_display_config(self, config_name, default=CONSTANTS.LANE):
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        label_display_configuration = _common.get(trend_store, self.CONSTANTS.LABEL_DISPLAY_CONFIGURATION,
                                                  default=dict())
        return _common.get(label_display_configuration, config_name, default=default)

    def _set_trend_store_label_display_config(self, config_name, value):
        trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        label_display_configuration = _common.get(trend_store, self.CONSTANTS.LABEL_DISPLAY_CONFIGURATION,
                                                  default=dict(),
                                                  assign_default=True)
        label_display_configuration[config_name] = value

    def _get_name(self) -> str:
        return self._get_trend_store_label_display_config(self.CONSTANTS.NAME, default=self.CONSTANTS.LANE)

    def _set_name(self, value: str):
        if value in self._valid_labels:
            self._set_trend_store_label_display_config(self.CONSTANTS.NAME, value)
        else:
            raise SPyValueError(f"'name' must be one of {self._valid_labels}")

    def _get_description(self) -> str:
        return self._get_trend_store_label_display_config(self.CONSTANTS.DESCRIPTION, default=self.CONSTANTS.OFF)

    def _set_description(self, value: str):
        if value in self._valid_labels:
            self._set_trend_store_label_display_config(self.CONSTANTS.DESCRIPTION, value)
        else:
            raise SPyValueError(f"'description' must be one of {self._valid_labels}")

    def _get_asset(self) -> str:
        return self._get_trend_store_label_display_config(self.CONSTANTS.ASSET, default=self.CONSTANTS.OFF)

    def _set_asset(self, value: str):
        if value in self._valid_labels:
            self._set_trend_store_label_display_config(self.CONSTANTS.ASSET, value)
        else:
            raise SPyValueError(f"'asset' must be one of {self._valid_labels}")

    def _get_asset_path_levels(self) -> int:
        return int(self._get_trend_store_label_display_config(self.CONSTANTS.ASSET_PATH_LEVELS, default=1))

    def _set_asset_path_levels(self, value: int):
        if not (isinstance(value, int) or (
                isinstance(value, str) and value.isdigit())):
            raise SPyValueError("'asset_path_levels' must be an Integer")
        self._set_trend_store_label_display_config(self.CONSTANTS.ASSET_PATH_LEVELS, int(value))

    def _get_line_style(self) -> str:
        return self._get_trend_store_label_display_config(self.CONSTANTS.LINE, default=self.CONSTANTS.OFF)

    def _set_line_style(self, value: str):
        if value in self._valid_labels:
            self._set_trend_store_label_display_config(self.CONSTANTS.LINE, value)
        else:
            raise SPyValueError(f"'line_style' must be one of {self._valid_labels}")

    def _get_unit_of_measure(self) -> str:
        return self._get_trend_store_label_display_config(self.CONSTANTS.UNIT_OF_MEASURE, default=self.CONSTANTS.AXIS)

    def _set_unit_of_measure(self, value: str):
        if value in self._valid_labels:
            self._set_trend_store_label_display_config(self.CONSTANTS.UNIT_OF_MEASURE, value)
        else:
            raise SPyValueError(f"'unit_of_measure' must be one of {self._valid_labels}")

    def _get_custom(self) -> str:
        return self._get_trend_store_label_display_config(self.CONSTANTS.CUSTOM, default=self.CONSTANTS.OFF)

    def _set_custom(self, value: str):
        if value in self._valid_labels:
            previous_value = self._get_custom()
            if value == self.CONSTANTS.OFF or previous_value != value:
                self._set_custom_labels([])  # Reset custom labels when custom visibility changes
            self._set_trend_store_label_display_config(self.CONSTANTS.CUSTOM, value)
        else:
            raise SPyValueError(f"'custom' must be one of {self._valid_labels}")

    def _get_custom_labels(self) -> List[str]:
        def labels_to_list(labels: List[str], location: str):
            if location == self.CONSTANTS.OFF or len(labels) == 0:
                return []

            def char_to_index(target: str):
                letter = target[0]
                letter_index = ord(letter) - ord('A')
                return (len(target) - 1) * 26 + letter_index

            max_index = max(
                char_to_index(label['target']) if location == self.CONSTANTS.AXIS else label['target'] - 1 for label in
                labels)
            result = [""] * (max_index + 1)

            for label in labels:
                result[char_to_index(label['target']) if location == self.CONSTANTS.AXIS else label['target'] - 1] = (
                    label)['text']
            return result

        custom_labels = self._get_trend_store_label_display_config(self.CONSTANTS.CUSTOM_LABELS, default=[])
        custom = self._get_custom()
        return labels_to_list(custom_labels, custom)

    def _set_custom_labels(self, value: List[str]):
        def list_to_labels(labels: List[str], location: str):
            if location == self.CONSTANTS.OFF:
                return []

            def index_to_target(index):
                repeats = index // 26 + 1
                letter = chr(ord('A') + index % 26)
                return letter * repeats

            return [{"location": location,
                     "target": index_to_target(i) if location == self.CONSTANTS.AXIS else i + 1,
                     "text": str(label)} for i, label in enumerate(labels) if label]

        if not isinstance(value, list):
            raise SPyTypeError("'custom_labels' must be a list of strings")

        custom = self._get_custom()
        self._set_trend_store_label_display_config(self.CONSTANTS.CUSTOM_LABELS, list_to_labels(value, custom))

    def __repr__(self):
        return f"Signals:\n" \
               f"  - Name: {self.name}\n" \
               f"  - Description: {self.description}\n" \
               f"  - Asset: {self.asset}\n" \
               f"  - Asset Path Levels: {self.asset_path_levels}\n" \
               f"  - Line Style: {self.line_style}\n" \
               f"  - Unit of Measure: {self.unit_of_measure}\n" \
               f"  - Custom: {self.custom}\n" \
               f"  - Custom Labels: {self.custom_labels}"


class Conditions(ContextSwitchable):
    """
    The configuration options for labeling conditions in the worksheet or current workstep of an Analysis.
    """

    class CONSTANTS:
        OFF = "off"
        LANE = "lane"
        TREND_STORE_NAME = "sqTrendStore"
        SHOW_CAPSULE_LANE_LABELS = "showCapsuleLaneLabels"
        ENABLED_COLUMNS = "enabledColumns"
        CAPSULES = "CAPSULES"
        CHART_CAPSULES = "CHART_CAPSULES"
        PROPERTY_COLUMNS = "propertyColumns"

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)

    @property
    @docstring_parameter(CONSTANTS.OFF, CONSTANTS.LANE)
    def name(self) -> str:
        """
        The string value indication Conditions Name visibility.
        Can be either '{0}' or '{1}'.
        """
        return self._get_name()

    @name.setter
    def name(self, value: str):
        self._set_name(value)

    @property
    def capsules(self) -> List[str]:
        """
        A list of strings representing the enabled properties of the capsules.
        List can include 'startTime', 'endTime', 'duration', 'asset', etc...
        """
        return self._get_capsules()

    @capsules.setter
    def capsules(self, value: List[str]):
        self._set_capsules(value)

    def _get_store(self, workstep, store_name):
        workstep_stores = workstep.get_workstep_stores()
        return _common.get(workstep_stores, store_name, default=dict(), assign_default=True)

    def _get_name(self) -> str:
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        return self.CONSTANTS.LANE if _common.get(trend_store, self.CONSTANTS.SHOW_CAPSULE_LANE_LABELS, default=True) \
            else self.CONSTANTS.OFF

    def _set_name(self, value: str):
        if value not in {self.CONSTANTS.OFF, self.CONSTANTS.LANE}:
            raise SPyValueError(f"'name' must be either '{self.CONSTANTS.OFF}' or '{self.CONSTANTS.LANE}'")
        trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        trend_store[self.CONSTANTS.SHOW_CAPSULE_LANE_LABELS] = value == self.CONSTANTS.LANE

    def _get_capsules(self) -> List[str]:
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        return list(
            _common.get(_common.get(trend_store, self.CONSTANTS.ENABLED_COLUMNS, default=dict()),
                        self.CONSTANTS.CAPSULES,
                        default=dict()).keys())

    def _set_capsules(self, value: List[str]):
        if not isinstance(value, list):
            raise SPyTypeError("'capsules' must be a list of strings")

        trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)

        property_columns = _common.get(trend_store, self.CONSTANTS.PROPERTY_COLUMNS, default=dict(),
                                       assign_default=True)
        property_columns_capsules = _common.get(property_columns, self.CONSTANTS.CAPSULES, default=dict(),
                                                assign_default=True)
        property_columns_chart_capsules = _common.get(property_columns, self.CONSTANTS.CHART_CAPSULES, default=dict(),
                                                      assign_default=True)

        enabled_columns = _common.get(trend_store, self.CONSTANTS.ENABLED_COLUMNS, default=dict(), assign_default=True)
        enabled_columns_capsules = dict()
        enabled_columns_chart_capsules = dict()

        for capsule in value:
            capsule = str(capsule)
            enabled_columns_capsules[capsule] = True
            enabled_columns_chart_capsules[capsule] = True
            if capsule.startswith('properties.'):
                name = capsule.split('properties.')[-1]
                value = (property_columns_capsules.get(capsule) or property_columns_chart_capsules.get(capsule) or
                         dict(key=capsule, uomKey=f"propertiesUOM.{name}", propertyName=name, style='string'))
                property_columns_capsules[capsule] = value
                property_columns_chart_capsules[capsule] = value
        enabled_columns[self.CONSTANTS.CAPSULES] = enabled_columns_capsules
        enabled_columns[self.CONSTANTS.CHART_CAPSULES] = enabled_columns_chart_capsules

    def __repr__(self):
        return f"Conditions:\n" \
               f"  - Name: {self.name}\n" \
               f"  - Capsules: {self.capsules}"


class Cursors(ContextSwitchable):
    """
    The configuration options for trend cursors in the worksheet or current workstep of an Analysis.
    """

    class CONSTANTS:
        SHOW = "show"
        HIDE = "hide"
        CURSOR_STORE_NAME = "sqCursorStore"
        SHOW_VALUES = "showValues"

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)

    @property
    @docstring_parameter(CONSTANTS.SHOW, CONSTANTS.HIDE)
    def values(self) -> str:
        """
        The string value indication Cursors Value visibility.
        Can be either '{0}' or '{1}'.
        """
        return self._get_values()

    @values.setter
    def values(self, value: str):
        self._set_values(value)

    def _get_store(self, workstep, store_name):
        workstep_stores = workstep.get_workstep_stores()
        return _common.get(workstep_stores, store_name, default=dict(), assign_default=True)

    def _get_values(self) -> str:
        cursor_store = self._get_store(self._getter_workstep, self.CONSTANTS.CURSOR_STORE_NAME)
        return self.CONSTANTS.SHOW if _common.get(cursor_store, self.CONSTANTS.SHOW_VALUES, default=True) else (
            self.CONSTANTS.HIDE)

    def _set_values(self, value: str):
        if value not in {self.CONSTANTS.SHOW, self.CONSTANTS.HIDE}:
            raise SPyValueError(f"'values' must be either '{self.CONSTANTS.SHOW}' or '{self.CONSTANTS.HIDE}'")
        cursor_store = self._get_store(self._setter_workstep, self.CONSTANTS.CURSOR_STORE_NAME)
        cursor_store[self.CONSTANTS.SHOW_VALUES] = value == self.CONSTANTS.SHOW

    def __repr__(self):
        return f"Cursors:\n" \
               f"  - Values: {self.values}"


class TrendItems(ContextSwitchable):
    """
    The configuration options for the trended items in the worksheet or current workstep of an Analysis.
    """

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)

    @property
    def items(self) -> pd.DataFrame:
        """
        A pandas DataFrame of the items present in the trend view.
        """
        return self._get_items()

    def set_item_color(self, item_id: str, color_code: str):
        """
        Set the color of a specific item on the trend view.

        Parameters
        ----------
        item_id : str
            The item identifier
        color_code: str
            The hex code of the color
        """

        _common.validate_hex_string(color_code)
        items = self._get_items()
        items.loc[items.ID == item_id, 'Color'] = color_code
        self._set_items(items)

    def _get_items(self) -> pd.DataFrame:
        return self._getter_workstep.display_items

    def _set_items(self, items: pd.DataFrame):
        if not isinstance(items, pd.DataFrame):
            raise SPyValueError(f'Items must of type {type(pd.DataFrame)}')
        self._getter_workstep.display_items = items

    def __repr__(self):
        repr_display = f"Trend Items Color:"
        for i, item in self.items.iterrows():
            color = _common.get(item, 'Color')
            repr_display += f"\n  - Name: {item['Name']}, Color: {color}"
        return repr_display


class Capsules(ContextSwitchable):
    """
    The configuration options for capsule colorization in the worksheet or current workstep of an Analysis.
    """

    class CONSTANTS:
        ITEM = "item"
        PROPERTY = "capsuleProperty"
        GRADIENT = "capsulePropertyGradient"
        GRADIENT_COLOR = "seeqColorGradient"
        CAPSULE_STORE_NAME = "sqTrendCapsuleStore"
        TREND_STORE_NAME = "sqTrendStore"
        TREND_COLOR_SETTINGS = "trendColorSettings"
        COLORMODE = "colorMode"
        CAPSULE_PROPERTY = "colorByCapsuleProperty"
        CAPSULE_PROPERTY_COLORS = "trendCapsulePropertyColors"

    _valid_color_modes = {CONSTANTS.ITEM, CONSTANTS.PROPERTY, CONSTANTS.GRADIENT}

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)

    @property
    @docstring_parameter(CONSTANTS.ITEM, CONSTANTS.PROPERTY, CONSTANTS.GRADIENT)
    def color_capsules_by(self) -> str:
        """
        The string value indication of the capsules color mode.
        Can be either '{0}', '{1}', or '{2}'.
        """
        return self._get_color_mode()

    @color_capsules_by.setter
    def color_capsules_by(self, value: str):
        self._set_color_mode(value)

    @property
    def capsule_property(self) -> str:
        """
        The name of the capsule property
        """
        return self._get_capsule_property()

    @capsule_property.setter
    def capsule_property(self, value: str):
        self._set_capsule_property(value)

    @property
    def capsule_property_color(self) -> Dict[str, str]:
        """
        Dict object mapping the capsule property values and their respective color codes.
        """
        return self._get_capsule_property_color()

    @capsule_property_color.setter
    def capsule_property_color(self, value: Dict[str, str]):
        self._set_capsule_property_color(value)

    @property
    def capsule_property_gradient(self) -> Dict[str, str]:
        """
        Dict object mapping the gradient from a color to another.
        """
        return self._get_capsule_property_gradient()

    @capsule_property_gradient.setter
    def capsule_property_gradient(self, value: Dict[str, str]):
        self._set_capsule_property_gradient(value)

    def _get_color_mode(self) -> str:
        return self._get_trend_store_color_settings(self.CONSTANTS.COLORMODE)

    def _set_color_mode(self, value: str):
        if value not in self._valid_color_modes:
            raise SPyValueError(f"'Value' must be one of {self._valid_color_modes}")
        self._set_trend_store_color_settings(self.CONSTANTS.COLORMODE, value)

    def _get_capsule_property(self) -> str:
        return self._get_trend_store_color_settings(self.CONSTANTS.CAPSULE_PROPERTY)

    def _set_capsule_property(self, value: str):
        self._set_trend_store_color_settings(self.CONSTANTS.CAPSULE_PROPERTY, value)

    def _get_capsule_property_color(self) -> Dict[str, str]:
        return self._get_trend_capsule_property_colors(self.capsule_property)

    def _set_capsule_property_color(self, value):
        if not isinstance(value, dict):
            raise SPyValueError(f"'value' must be a dictionary of capsule property value and color value pair")
        for color in value.values():
            _common.validate_hex_string(color)
        self._set_color_mode(self.CONSTANTS.PROPERTY)
        self._set_trend_capsule_property_colors(self.capsule_property, value)

    def _get_capsule_property_gradient(self) -> Dict[str, str]:
        gradient_from_to = self._get_trend_capsule_property_colors(self.CONSTANTS.GRADIENT_COLOR)
        return {'From': gradient_from_to['from'], 'To': gradient_from_to['to']}

    def _set_capsule_property_gradient(self, gradient_from_to: Dict[str, str]):
        if isinstance(gradient_from_to, dict) and {'From', 'To'}.issubset(gradient_from_to.keys()):
            _common.validate_hex_string(gradient_from_to['From'])
            _common.validate_hex_string(gradient_from_to['To'])
            gradient_from_to = {k.lower(): v for k, v in gradient_from_to.items()}
            self._set_color_mode(self.CONSTANTS.GRADIENT)
            self._set_trend_capsule_property_colors(self.CONSTANTS.GRADIENT_COLOR, gradient_from_to)
        else:
            raise SPyValueError(f"capsule property gradient must be a dictionary with 'From' and 'To' keys and "
                                f"hex color code values")

    def _get_store(self, workstep, store_name):
        workstep_stores = workstep.get_workstep_stores()
        return _common.get(workstep_stores, store_name, default=dict(), assign_default=True)

    def _get_trend_store_color_settings(self, config_name, default=CONSTANTS.ITEM):
        trend_store = self._get_store(self._getter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        trend_color_settings = _common.get(trend_store, self.CONSTANTS.TREND_COLOR_SETTINGS, default=dict())
        return _common.get(trend_color_settings, config_name, default=default)

    def _set_trend_store_color_settings(self, config_name, value):
        trend_store = self._get_store(self._setter_workstep, self.CONSTANTS.TREND_STORE_NAME)
        trend_color_settings = _common.get(trend_store, self.CONSTANTS.TREND_COLOR_SETTINGS, default=dict(),
                                           assign_default=True)
        trend_color_settings[config_name] = value

    def _get_trend_capsule_property_colors(self, capsule_property):
        capsule_store = self._get_store(self._getter_workstep, self.CONSTANTS.CAPSULE_STORE_NAME)
        capsule_property_colors = _common.get(capsule_store, self.CONSTANTS.CAPSULE_PROPERTY_COLORS, default=dict())
        return _common.get(capsule_property_colors, capsule_property, default=dict())

    def _set_trend_capsule_property_colors(self, capsule_property, value):
        capsule_store = self._get_store(self._setter_workstep, self.CONSTANTS.CAPSULE_STORE_NAME)
        capsule_property_colors = _common.get(capsule_store, self.CONSTANTS.CAPSULE_PROPERTY_COLORS, default=dict(),
                                              assign_default=True)
        capsule_property_colors[capsule_property] = value

    def __repr__(self):
        repr_display = f"Capsules:\n" \
                       f"  - Color capsules by: {self.color_capsules_by}\n"
        if self.color_capsules_by == self.CONSTANTS.PROPERTY:
            repr_display += f"  - Capsule property: {self.capsule_property}\n" \
                            f"  - Capsule property color: {self.capsule_property_color}"
        elif self.color_capsules_by == self.CONSTANTS.GRADIENT:
            repr_display += f"  - Capsule property gradient: {self.capsule_property_gradient}"
        return repr_display


class Color(ContextSwitchable):
    """
    The configuration options for item colorization in the worksheet or current workstep of an Analysis.
    """

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self._trend_items = TrendItems(parent)
        self._capsules = Capsules(parent)

    @property
    def trend_items(self) -> TrendItems:
        """
        Color configuration for items on the trend.
        """
        return self._trend_items

    @property
    def capsules(self) -> Capsules:
        """
        Color configuration for condition capsules on the trend.
        """
        return self._capsules

    def __repr__(self):
        return ("Color:\n" +
                textwrap.indent(
                    f"- {repr(self.trend_items)}\n"
                    f"- {repr(self.capsules)}",
                    prefix="  "
                ))

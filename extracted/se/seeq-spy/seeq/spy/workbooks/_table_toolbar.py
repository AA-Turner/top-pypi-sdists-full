from __future__ import annotations

import textwrap
from abc import ABC, abstractmethod
from collections.abc import MutableSequence
from typing import Union, List, Dict, Any, cast, TypeVar, Generic

import pandas as pd

from seeq.spy import _common
from seeq.spy._common import docstring_parameter
from seeq.spy._errors import *
from seeq.spy.workbooks._context_switchable import ContextSwitchable

ColsT = TypeVar('ColsT', bound='Columns')


# refer client/packages/webserver/app/src/tableBuilder
class TableToolbar(ContextSwitchable, Generic[ColsT]):
    class CONSTANTS:
        TABLE_STORE_NAME = 'sqTableBuilderStore'
        SIMPLE_TABLE_MODE = 'simple'
        CONDITION_TABLE_MODE = 'condition'

        TRANSPOSE = 'isTransposed'
        STRIPED = 'isTableStriped'
        AUTO_GROUP_COLUMN = 'autoGroupColumn'

        DEFAULT_TABLE_STATE = {
            'headers': {
                'condition': {
                    'type': 'startEnd',
                    'format': 'lll'
                },
                'simple': {
                    'type': 'startEnd',
                    'format': 'lll'
                }
            },
            'columns': {
                'condition': [],
                'simple': []
            }
        }

    TABLE_MODE = None

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self._columns = None

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
    @docstring_parameter(CONSTANTS.SIMPLE_TABLE_MODE, CONSTANTS.CONDITION_TABLE_MODE)
    def table_mode(self) -> str:
        """
        The current table mode for the workstep.
        Can either be `{0}` or `{1}`

        """
        return self._get_table_mode()

    @table_mode.setter
    def table_mode(self, value: str):
        self._set_table_mode(value)

    @property
    def transpose(self) -> bool:
        """
        Boolean value indicating if the table is transposed.
        In Condition Table mode, a value of `True` produces a table where rows correspond to capsules
        In Simple Table mode, a value of `True` produces a table where rows correspond to item statistics

        Can either be `True` or `False`
        """
        return self._get_transpose()

    @transpose.setter
    def transpose(self, value: bool):
        self._set_transpose(value)

    @property
    def striped(self) -> bool:
        """
        Boolean value indicating if every alternate row in the table is shaded.
        Can either be `True` or `False`
        """
        return self._get_striped()

    @striped.setter
    def striped(self, value: bool):
        self._set_striped(value)

    @property
    def group(self):
        """
        Boolean value indicating if grouping is enabled in the table.
        Can either be `True` or `False`
        """
        return self._get_group()

    @group.setter
    def group(self, value: bool):
        self._set_group(value)

    @property
    def columns(self) -> ColsT:
        """
        Column configuration for Condition Tables. Use methods on this object to add or remove columns from the table.
        """
        return self._columns

    @columns.setter
    def columns(self, value: list[TableColumn]):
        self.columns._set_columns(value)

    @staticmethod
    def _get_table_store(workstep):
        workstep_stores = workstep.get_workstep_stores()
        return _common.get(
            workstep_stores, TableToolbar.CONSTANTS.TABLE_STORE_NAME,
            default=TableToolbar.CONSTANTS.DEFAULT_TABLE_STATE,
            assign_default=True
        )

    @staticmethod
    def get_config_for_table_mode(workstep, attribute: str, table_mode: str, default=None):
        table_store = TableToolbar._get_table_store(workstep)
        table_config = _common.get(table_store, attribute, default=dict(), assign_default=False)
        return table_config.get(table_mode, default)

    @staticmethod
    def set_config_for_table_mode(workstep, attribute: str, table_mode: str, value):
        table_store = TableToolbar._get_table_store(workstep)
        table_config = _common.get(table_store, attribute, default=dict(), assign_default=True)
        table_config[table_mode] = value

    def _get_table_mode(self) -> str:
        return self._getter_workstep.table_mode

    def _set_table_mode(self, value: str):
        self._setter_workstep.table_mode = value

    def _get_transpose(self) -> bool:
        return TableToolbar.get_config_for_table_mode(self._getter_workstep, self.CONSTANTS.TRANSPOSE,
                                                      self.TABLE_MODE, False)

    def _set_transpose(self, value: bool):

        if isinstance(value, bool):
            TableToolbar.set_config_for_table_mode(self._setter_workstep, self.CONSTANTS.TRANSPOSE,
                                                   self.TABLE_MODE, value)
        else:
            raise SPyTypeError("'transpose' must be a boolean")

    def _get_striped(self) -> bool:
        return TableToolbar.get_config_for_table_mode(self._getter_workstep, self.CONSTANTS.STRIPED, self.TABLE_MODE,
                                                      False)

    def _set_striped(self, value: bool):
        if isinstance(value, bool):
            TableToolbar.set_config_for_table_mode(self._setter_workstep, self.CONSTANTS.STRIPED,
                                                   self.TABLE_MODE, value)
        else:
            raise SPyTypeError("'striped' must be a boolean")

    def _get_group(self) -> bool:
        # grouping is determined by whether there is any value for the table mode for autoGroupColumn
        auto_group_column = TableToolbar.get_config_for_table_mode(self._getter_workstep,
                                                                   self.CONSTANTS.AUTO_GROUP_COLUMN,
                                                                   self.TABLE_MODE,
                                                                   None)

        return auto_group_column is not None

    def _set_group(self, value: bool):
        # grouping is enabled by setting a value for the table mode for autoGroupColumn
        if isinstance(value, bool):
            if value:
                TableToolbar.set_config_for_table_mode(self._setter_workstep, self.CONSTANTS.AUTO_GROUP_COLUMN,
                                                       self.TABLE_MODE, {})
            else:
                TableToolbar.set_config_for_table_mode(self._setter_workstep, self.CONSTANTS.AUTO_GROUP_COLUMN,
                                                       self.TABLE_MODE, None)
        else:
            raise SPyTypeError("'group' must be a boolean")


class SimpleTableToolbar(TableToolbar['SimpleTableColumns']):
    """
    Exposes configuration options for Simple Tables in a workbench Analysis.

    Methods are named based on a table with Transpose set to `False`: rows are items, columns are statistics or
    properties.
    """
    TABLE_MODE = TableToolbar.CONSTANTS.SIMPLE_TABLE_MODE

    def __init__(self, parent):
        super().__init__(parent)
        self._columns = SimpleTableColumns(parent)


class ConditionTableToolbar(TableToolbar['ConditionTableColumns']):
    """
    Exposes configuration options for Condition Tables in a workbench Analysis.

    Methods are named based on a table with Transpose set to `True`: rows are capsules, columns are statistics or
    properties.
    """
    TABLE_MODE = TableToolbar.CONSTANTS.CONDITION_TABLE_MODE

    def __init__(self, parent):
        super().__init__(parent)
        self._columns = ConditionTableColumns(parent)

    def add_row_column_labels(self) -> ConditionTableRow:
        """
        Enable and return the row that displays column labels in the table.
        Once returned, the row can be manipulated to adjust the appearance of the column labels.
        """
        return self.columns.add_row_column_labels()

    def remove_row_column_labels(self):
        """
        Hide the row that displays column labels in the table.
        """
        self.columns.remove_row_column_labels()

    def add_row_unit_of_measure(self) -> ConditionTableRow:
        """
        Enable and return the row that displays units of measure in the table.
        When the row is present, units will be moved from within each cell to the row.
        Once returned, this row can be manipulated to adjust the appearance of the units of measure.
        """
        return self.columns.add_row_unit_of_measure()

    def remove_row_unit_of_measure(self):
        """
        Hide the row that displays units of measure in the table.
        """
        self.columns.remove_row_unit_of_measure()

    def add_row_custom_text(self, column_values: Union[List[str], Dict[str, str]]) -> ConditionTableRowCustomText:
        """
        Add and return a row that displays custom text in the table.
        Once returned, the row can be manipulated to adjust the appearance of the custom text.

        Parameters
        ----------
        column_values: Union[List[str], Dict[str, str]]
            List of string values to display in the row or a dictionary of column keys and values
        """
        return self.columns.add_row_custom_text(column_values)

    def remove_row_custom_text(self):
        """
        Remove all rows that displays custom text in the table.
        """
        self.columns.remove_row_custom_text()

    def _column_labels_enabled(self) -> bool:
        return ConditionTableRow.CONSTANTS.COLUMN_LABELS in self.columns._get_columns()

    def _unit_of_measure_enabled(self) -> bool:
        return ConditionTableRow.CONSTANTS.UNIT_OF_MEASURE in self.columns._get_columns()

    def __repr__(self):
        return (
            f"Condition Table Configuration:\n"
            f"  - Table Mode: {self.table_mode}\n"
            f"  - Transpose: {self.transpose}\n"
            f"  - Striped: {self.striped}\n"
            f"  - Group: {self.group}\n"
            f"  - Column Labels: {self._column_labels_enabled()}\n"
            f"  - Units of Measure Row: {self._unit_of_measure_enabled()}\n"
            f"{textwrap.indent(f'- {repr(self.columns)}', prefix='  ')}"
        )


class TableColumn(ABC, ContextSwitchable):
    class CONSTANTS:
        # refer client/packages/webserver/app/src/core/TextFormatterPopover.molecule.tsx
        TEXT_ALIGN_OPTIONS = {'left', 'center', 'right'}
        TEXT_STYLE_OPTIONS = {'bold', 'italic', 'underline', 'line-through', 'overline'}

        # refer AgGridAggregationFunctions in  client/packages/webserver/app/src/tableBuilder/tableBuilder.constants.ts
        GROUPING_AGGREGATION_FUNCTIONS = {
            'none',
            'sum',
            'min',
            'max',
            'count',
            'avg',
            'range',
            'stdDev',
            'first',
            'last',
        }

        SIGNAL_STATISTICS = _common.get_trend_signal_statistic_function_map()
        SIGNAL_STATISTICS_TO_NAME = {v: k for k, v in SIGNAL_STATISTICS.items()}

    @property
    @abstractmethod
    def is_row(self) -> bool:
        pass

    @abstractmethod
    def _get_column_definition(self) -> dict:
        pass


class ConditionTableColumn(TableColumn):
    """
    The SPy representation of a column in a condition table.
    """

    class CONSTANTS(TableColumn.CONSTANTS):
        pass

    def __init__(self, column, parent):
        super().__init__(parent)
        self._key = column.get('key')

    def __repr__(self):
        return (f"{self.key}:\n" +
                textwrap.indent("".join([
                    f"- Key: {self.key}\n",
                    f"- Type: Property\n",
                    f"- Header: {self.header}\n" if self.header else "",
                    f"- Grouped: {self.grouping}\n",
                    f"- Group Order: {self.group_order}\n" if self.grouping else "",
                    f"- Aggregation Function: {self.aggregation_function}\n" if self.aggregation_function else ""
                ]), prefix="    "))

    def __eq__(self, other: Union[ConditionTableColumn, str]):
        # allow comparisons against strings for convenience
        if isinstance(other, str):
            return self.key == other

        return self.key == other.key

    def validate(self):
        if self.key is None:
            raise SPyValueError('Key must be provided')

    def _get_column_definition(self) -> dict:
        condition_columns = ConditionTableColumns.get_column_store(self._getter_workstep)
        return next(column for column in condition_columns if column['key'] == self.key)

    def _get_column_attribute(self, key: str, default=None) -> Any:
        return _common.get(self._get_column_definition(), key, default=default)

    def _set_column_attribute(self, key: str, value: Any):
        condition_columns = ConditionTableColumns.get_column_store(self._setter_workstep)
        column = next(column for column in condition_columns if column['key'] == self.key)
        # column attributes never read False or empty lists, the key is just removed
        if value or value == 0:
            column[key] = value
        else:
            column.pop(key, None)

    @property
    def is_row(self) -> bool:
        """
        Whether the column is displayed as a row in the table.
        """
        return False

    @property
    def key(self) -> str:
        """
        Unique identifier for the column. Must be unique within the table. Cannot be changed.
        """
        return self._key

    @key.setter
    def key(self, value: str):
        raise SPyValueError("'key' is read-only")

    @property
    def type(self) -> str:
        """
        The type of the column. Cannot be changed.
        """
        return self._get_column_attribute('type')

    @type.setter
    def type(self, value: str):
        raise SPyValueError("'type' is read-only")

    @property
    def header(self) -> str:
        """
        A string value that is displayed in the header of the column.
        Changing this will override what is displayed in the header for this column.
        """
        return self._get_column_attribute('header')

    @header.setter
    def header(self, value: str):
        if value is None or isinstance(value, str):
            self._set_column_attribute('header', value)
        else:
            raise SPyTypeError("'header' must be a string")

    @property
    @docstring_parameter(CONSTANTS.TEXT_ALIGN_OPTIONS)
    def header_text_align(self) -> str:
        """
        A string value indicating how the header text will be aligned.
        Must be one of: `{0}`
        """
        return self._get_column_attribute('headerTextAlign')

    @header_text_align.setter
    def header_text_align(self, value: str):
        if value is None or value in self.CONSTANTS.TEXT_ALIGN_OPTIONS:
            self._set_column_attribute('headerTextAlign', value)
        else:
            raise SPyValueError(f"'header_text_align' must be one of {self.CONSTANTS.TEXT_ALIGN_OPTIONS}")

    @property
    @docstring_parameter(CONSTANTS.TEXT_STYLE_OPTIONS)
    def header_text_style(self) -> List[str]:
        """
        A list of string values indicating the style of the header text.
        Must be a subset of: `{0}`
        """
        return self._get_column_attribute('headerTextStyle')

    @header_text_style.setter
    @docstring_parameter(CONSTANTS.TEXT_STYLE_OPTIONS)
    def header_text_style(self, value: List[str]):
        """
        A list of string values indicating the style of the header text.
        Must be a subset of: `{0}`
        """
        if value is None or all(style in self.CONSTANTS.TEXT_STYLE_OPTIONS for style in value):
            self._set_column_attribute('headerTextStyle', value)
        else:
            raise SPyValueError(f"'header_text_style' must be in {self.CONSTANTS.TEXT_STYLE_OPTIONS}")

    @property
    @docstring_parameter(CONSTANTS.TEXT_ALIGN_OPTIONS)
    def text_align(self) -> str:
        """
        A string value indicating how the values in the column will be aligned.
        Must be one of: `{0}`
        """
        return self._get_column_attribute('textAlign')

    @text_align.setter
    def text_align(self, value: str):
        if value is None or value in self.CONSTANTS.TEXT_ALIGN_OPTIONS:
            self._set_column_attribute('textAlign', value)
        else:
            raise SPyTypeError(f"'text_align' must be one of {self.CONSTANTS.TEXT_ALIGN_OPTIONS}")

    @property
    @docstring_parameter(CONSTANTS.TEXT_STYLE_OPTIONS)
    def text_style(self) -> List[str]:
        """
        A list of string values indicating the style of the values in the column.
        Must be a subset of: `{0}`
        """
        return self._get_column_attribute('textStyle')

    @text_style.setter
    def text_style(self, value: List[str]):
        if value is None or all(style in self.CONSTANTS.TEXT_STYLE_OPTIONS for style in value):
            self._set_column_attribute('textStyle', value)
        else:
            raise SPyTypeError(f"'text_style' must be in {self.CONSTANTS.TEXT_STYLE_OPTIONS}")

    @property
    def width(self) -> int:
        """
        Integer value indicating the width of the column.
        """
        return self._get_column_attribute('width')

    @width.setter
    def width(self, value: int):
        if value is None or isinstance(value, int):
            self._set_column_attribute('width', value)
        else:
            raise SPyTypeError("'width' must be an integer")

    @property
    def group_order(self) -> int:
        """
        Integer value indicating the order that columns are grouped in.
        This needs to be consistent across all columns that are grouped.
        To ensure this, always manipulate grouping through the :py:attr:`ConditionTableColumns.grouped_columns`
        property.
        """
        return self._get_column_attribute('rowGroupOrder')

    @group_order.setter
    def group_order(self, value: int):
        if value is None or isinstance(value, int):
            self._set_column_attribute('rowGroupOrder', value)
        else:
            raise SPyTypeError("group_order must be an integer")

    @property
    def grouping(self) -> bool:
        """
        Boolean value indicating if the column is grouped in the table.
        If `True`, group_order must also be set. To ensure this, always manipulate grouping through the
        :py:attr:`ConditionTableColumns.grouped_columns`
        property.
        """
        # if grouping not enabled, key isn't in the stores, so return False
        return self._get_column_attribute('grouping', False)

    @grouping.setter
    def grouping(self, value: bool):
        if isinstance(value, bool):
            self._set_column_attribute('grouping', value if value else None)
        else:
            raise SPyTypeError("'grouping' must be a boolean")

    @property
    @docstring_parameter(CONSTANTS.GROUPING_AGGREGATION_FUNCTIONS)
    def aggregation_function(self) -> str:
        """
        String value indicating how to aggregate values in this column when grouping is enabled.
        Must be one of: `{0}`
        """
        return self._get_column_attribute('aggregationFunction')

    @aggregation_function.setter
    def aggregation_function(self, value: str):
        if value is None or value in self.CONSTANTS.GROUPING_AGGREGATION_FUNCTIONS:
            self._set_column_attribute('aggregationFunction', value)
        else:
            raise SPyValueError(
                f"'aggregation_function' must be one of {self.CONSTANTS.GROUPING_AGGREGATION_FUNCTIONS}")

    @staticmethod
    def validate_definition(column_definition: dict) -> bool:
        return True


class ConditionTableColumnScorecard(ConditionTableColumn):
    @staticmethod
    def validate_definition(column_definition: dict) -> bool:
        return column_definition.get('metricId', None) is not None

    @property
    def metric_id(self) -> str:
        """
        The ID of the metric that the column is displaying.
        """
        return self._get_column_definition()['metricId']

    @metric_id.setter
    def metric_id(self, value: str):
        raise SPyValueError("'metric_id' is read-only")

    def __repr__(self):
        # lookup the name of the scorecard metric to show to user
        scorecard_name = self._getter_workstep.display_items.loc[
            self._getter_workstep.display_items['ID'] == self.metric_id, 'Name'].values[0]
        return (f"{scorecard_name}:\n" +
                textwrap.indent("".join([
                    f"- Key: {self.key}\n",
                    f"- Type: Scorecard Metric\n",
                    f"- Item ID: {self.metric_id}\n"
                    f"- Grouped: {self.grouping}\n",
                    f"- Group Order: {self.group_order}\n" if self.grouping else "",
                    f"- Aggregation Function: {self.aggregation_function}\n" if self.aggregation_function else ""
                ]), prefix="    "))


class ConditionTableRow(ConditionTableColumn):
    class CONSTANTS(ConditionTableColumn.CONSTANTS):
        COLUMN_LABELS = 'name'
        UNIT_OF_MEASURE = 'valueUnitOfMeasure'

        KEYS = [
            COLUMN_LABELS,
            UNIT_OF_MEASURE
        ]

    # these are the columns that actually display as rows in the table
    # includes column labels, custom text rows, and unit of measure rows
    # they do not accept custom text, and cannot be used for grouping
    @property
    def is_row(self) -> bool:
        return True

    @property
    def grouping(self) -> bool:
        return False

    @grouping.setter
    def grouping(self, value: bool):
        pass

    @staticmethod
    def validate_definition(column_definition: dict) -> bool:
        key = column_definition.get('key', None)
        return key in ConditionTableRow.CONSTANTS.KEYS


class ConditionTableRowCustomText(ConditionTableRow):
    @staticmethod
    def validate_definition(column_definition: dict) -> bool:
        return column_definition.get('type', None) == 'text'


class ConditionTableColumnReservedProperty(ConditionTableColumn):
    # refer CONDITION_EXTRA_COLUMNS in client/packages/webserver/app/src/tableBuilder/tableBuilder.constants.ts
    class CONSTANTS(ConditionTableColumn.CONSTANTS):
        START_KEY = 'startTime'
        END_KEY = 'endTime'
        NAME_EXPRESSION_KEY = 'nameExpression'
        ASSET_KEY = 'asset'

        KEY_MAPPING = {
            'start': START_KEY,
            'end': END_KEY,
            'name': NAME_EXPRESSION_KEY,
            'asset': ASSET_KEY
        }

        KEYS_OR_VALUES = set(KEY_MAPPING) | set(KEY_MAPPING.values())

    @staticmethod
    def validate_definition(column_definition: dict) -> bool:
        key = column_definition.get('key', None)
        return key in ConditionTableColumnReservedProperty.CONSTANTS.KEY_MAPPING.values()


class ConditionTableColumnSignalStatistic(ConditionTableColumn):
    @staticmethod
    def validate_definition(column_definition: dict) -> bool:
        return column_definition.get('statisticKey', None) is not None

    @property
    def signal_id(self) -> str:
        return self._get_column_definition()['signalId']

    @signal_id.setter
    def signal_id(self, value: str):
        raise SPyValueError("'signal_id' is read-only")

    @property
    def statistic_key(self) -> str:
        return self._get_column_definition()['statisticKey']

    @statistic_key.setter
    def statistic_key(self, value: str):
        raise SPyValueError("'statistic_key' is read-only")

    @property
    def statistic_name(self) -> str:
        """
        The name of the statistic that the column is displaying.
        """
        return self.CONSTANTS.SIGNAL_STATISTICS_TO_NAME[self.statistic_key]

    @property
    def signal_name(self):
        return self._getter_workstep.display_items.loc[
            self._getter_workstep.display_items['ID'] == self.signal_id, 'Name'].values[0]

    def __repr__(self):
        # lookup the name of the scorecard metric to show to user
        return (f"{self.signal_name} {self.statistic_name}:\n" +
                textwrap.indent("".join([
                    f"- Key: {self.key}\n",
                    f"- Type: Signal Statistic\n",
                    f"- Header: {self.header}\n" if self.header else "",
                    f"- Item ID: {self.signal_id}\n",
                    f"- Statistic: {self.statistic_name}\n",
                    f"- Grouped: {self.grouping}\n",
                    f"- Group Order: {self.group_order}\n" if self.grouping else "",
                    f"- Aggregation Function: {self.aggregation_function}\n" if self.aggregation_function else ""
                ]), prefix="    "))


ColT = TypeVar('ColT', bound=TableColumn)


class TableColumns(ABC, ContextSwitchable, MutableSequence, Generic[ColT]):
    TABLE_MODE = None

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)

    def __repr__(self) -> str:
        columns_repr = "\n".join(f"  - {repr(column)}" for column in self)
        columns_repr = columns_repr if columns_repr else "  No columns"
        return ("Columns:\n" +
                textwrap.indent(columns_repr, prefix="  "))

    def __getitem__(self, key: Union[str, int]) -> ColT:
        # get item either by index or by key
        if isinstance(key, str):
            # if key is a string, get the column by key
            columns = self._get_interactable_columns()
            column = next((column for column in columns if column.key == key), None)
            if not column:
                raise IndexError(f"Column with key '{key}' not found")
        else:
            column = self._get_interactable_columns()[key]

        return column

    def __setitem__(self, index: int, val: TableColumn) -> None:
        raise TypeError("Adding columns should be done through the appropriate method")

    def __delitem__(self, index: int) -> None:
        column_key = self[index].key
        self._remove_column(column_key)

    def __len__(self) -> int:
        return len(self._get_interactable_columns())

    def insert(self, index: int, value: ColT):
        raise TypeError("Adding columns should be done through the appropriate method")

    @property
    def grouped_columns(self) -> List[ColT]:
        """
        Set the columns that are grouped in the table. The columns must already be present in the table.
        The order of the columns in the list will determine the order that the columns are grouped in.

        Examples
        --------
        Add column for capsule property Batch ID and group the table by this column:

        >>> workbook: spy.workbooks.Analysis
        >>> worksheet = workbook.worksheets['Worksheet Name']
        >>> batch_id_column = worksheet.condition_table_toolbar.columns.add_column_property('Batch ID')
        >>> worksheet.condition_table_toolbar.group = True # enable grouping
        >>> worksheet.condition_table_toolbar.columns.grouped_columns = [batch_id_column] # group table by asset
        """
        return self._get_grouped_columns()

    @grouped_columns.setter
    def grouped_columns(self, value: list[ColT]):

        self._set_grouped_columns(value)

    @classmethod
    def get_column_store(cls, workstep):
        return TableToolbar.get_config_for_table_mode(workstep, 'columns', cls.TABLE_MODE)

    def _add_column(self, column_definition: dict) -> TableColumn:
        column_store = self.get_column_store(self._setter_workstep)
        # if column already exists, just return the column
        if column_definition['key'] in [column['key'] for column in column_store]:
            return self._column_factory(column_definition)
        column_store.append(column_definition)
        # return column so it can be interacted with
        return self._column_factory(column_definition)

    def _remove_column(self, key: str):
        column_store = self.get_column_store(self._setter_workstep)
        column_to_remove = next(
            column for column in column_store if column['key'] == key)
        column_store.remove(column_to_remove)
        self._refresh_group_order()

    def _get_columns(self) -> List[ColT]:
        # this will get everything that is stored as a column in the table store
        # this includes columns that are actually displayed as rows
        column_definitions = self.get_column_store(self._getter_workstep)
        columns = []
        for column_definition in column_definitions:
            column = self._column_factory(column_definition)
            if column:
                columns.append(column)
        return columns

    def _set_columns(self, value: List[ColT]):
        # first check that all columns are present in the table
        # then loop through the whole column store and either rearrange the whole thing
        # ensure that all columns are present in the table
        if not all(column in self for column in value):
            raise SPyValueError('All columns must be in the table')

        new_column_store = [row._get_column_definition() for row in self._get_rows()]
        for column in value:
            new_column_store.append(column._get_column_definition())

        TableToolbar.set_config_for_table_mode(self._setter_workstep, 'columns', self.TABLE_MODE,
                                               new_column_store)
        self._refresh_group_order()

    def _get_interactable_columns(self) -> List[ColT]:
        # this will get only columns that are displayed as columns in the table
        return [column for column in self._get_columns() if not column.is_row]

    def _get_rows(self) -> List[ColT]:
        # this will get only columns that are displayed as rows in the table
        return [column for column in self._get_columns() if column.is_row]

    def _refresh_group_order(self):
        """
        Refresh the group order of all grouped columns in the table. Needs to be called when
        columns are removed to keep the group order consistent in the workstep.
        """
        self.grouped_columns = self.grouped_columns

    @abstractmethod
    def _get_grouped_columns(self) -> List[ColT]:
        pass

    @abstractmethod
    def _set_grouped_columns(self, value: List[ColT]):
        pass

    @abstractmethod
    def _column_factory(self, column_definition: dict):
        pass


class ConditionTableColumns(TableColumns[ConditionTableColumn]):
    """
    Column configuration for Condition Tables. Use methods on this object to add or remove columns from the table.
    """

    class CONSTANTS:
        DEFAULT_COLUMN_DEFINITION: Dict[str, Any] = {
            'headerTextStyle': ['bold'],
            'headerTextAlign': 'center'
        }

    TABLE_MODE = TableToolbar.CONSTANTS.CONDITION_TABLE_MODE

    def _add_column(self, *args, **kwargs) -> ConditionTableColumn:
        return cast(ConditionTableColumn, super()._add_column(*args, **kwargs))

    def _column_factory(self, column_definition: dict) -> Union[None, ConditionTableColumn]:
        # given from most to least specific
        column_type_classes = [
            ConditionTableRowCustomText,
            ConditionTableRow,
            ConditionTableColumnReservedProperty,
            ConditionTableColumnSignalStatistic,
            ConditionTableColumnScorecard,
            ConditionTableColumn
        ]
        for column_type_class in column_type_classes:
            if column_type_class.validate_definition(column_definition):
                return column_type_class(column_definition, self._parent)

    def add_column_property(self, property_name: str) -> ConditionTableColumn:
        """
        Add and return a capsule or condition property column to the table.

        Parameters
        ----------
        property_name: str
            The name of the property to add as a column

        """
        column_definition = self.CONSTANTS.DEFAULT_COLUMN_DEFINITION.copy()
        # There are four 'Condition Extra Columns' that are treated differently by the frontend
        # Start Time, End Time, Name, and Asset have special keys and do not have type 'capsuleProperty'
        # To prevent users from having to know that you have to put nameExpression to get the condition name
        # Do a lookup from the name in the frontend to the key used in the workstep.
        if property_name.lower() not in ConditionTableColumnReservedProperty.CONSTANTS.KEYS_OR_VALUES:
            column_definition['type'] = 'capsuleProperty'
        if property_name.lower() in ConditionTableColumnReservedProperty.CONSTANTS.KEY_MAPPING:
            property_name = ConditionTableColumnReservedProperty.CONSTANTS.KEY_MAPPING[property_name.lower()]
        column_definition['key'] = property_name
        return self._add_column(column_definition)

    def remove_column_property(self, property_name: str):
        """
        Remove a capsule or condition property column from the table.

        Parameters
        ----------
        property_name: str
            The name of the property to remove from the table
        """
        if property_name.lower() in ConditionTableColumnReservedProperty.CONSTANTS.KEY_MAPPING:
            property_name = ConditionTableColumnReservedProperty.CONSTANTS.KEY_MAPPING[property_name.lower()]
        self._remove_column(property_name)

    @docstring_parameter(list(TableColumn.CONSTANTS.SIGNAL_STATISTICS.keys()))
    def add_column_statistic(
            self, items, statistic: str
    ) -> Union[ConditionTableColumnSignalStatistic, List[ConditionTableColumnSignalStatistic]]:
        """
        Add and return one or multiple signal statistic columns to the table.
        All items must already be present in the details pane before they can be added as columns.
        Statistic columns can only be added for signals in condition tables.

        Parameters
        ----------
        items: Union[pd.DataFrame, pd.Series, List[Dict[str, str]], Dict[str, str], str]
            List of items to add as columns, or a single item. Can supply as:
                - pd.DataFrame or pd.Series containing 'ID' column
                - List of dictionaries with 'ID' key
                - Dictionary with 'ID' key
                - String of the item ID
        statistic: str
            Statistic to apply to each of the items. Must be one of: {0}
        """
        items: Union[pd.DataFrame, pd.Series, List[Dict[str, str]], Dict[str, str], str]
        if isinstance(items, pd.DataFrame):
            items = items.to_dict(orient='records')
        elif isinstance(items, pd.Series):
            items = [items.to_dict()]
        elif isinstance(items, list):
            items = items
        elif isinstance(items, str):
            items = [{'ID': items}]
        else:
            items = [items]
        if not items:
            raise SPyValueError("Items must be a non-empty list, DataFrame, Series, or string")

        columns_to_return = []
        for item in items:
            if not _common.present(item, 'ID'):
                raise SPyValueError(f'Item must have an ID')
            if _common.is_guid(item['ID']):
                columns_to_return.append(self._add_single_column_statistic(item['ID'], statistic))
            else:
                raise SPyValueError(f'Expecting input of ID, got {item["ID"]}')

        # if only a single column was added, return it directly to stay consistent with add_column_property
        if len(columns_to_return) == 1:
            return columns_to_return[0]
        else:
            return columns_to_return

    def _add_single_column_statistic(self, item_id: str, statistic: str) -> ConditionTableColumnSignalStatistic:
        if item_id not in self._parent.display_items['ID'].values:
            # item must exist in details pane before it can be added
            raise SPyValueError(f"Item with ID {item_id} must be added to the details pane before adding as a column")
        # make sure it's a signal!
        if self._parent.display_items.loc[self._parent.display_items['ID'] == item_id, 'Type'].values[0] != 'Signal':
            raise SPyValueError(f"Item with ID {item_id} is not a signal.")

        if statistic.lower() not in TableColumn.CONSTANTS.SIGNAL_STATISTICS:
            raise SPyValueError(f"'statistic' must be one of {list(TableColumn.CONSTANTS.SIGNAL_STATISTICS.keys())}")

        column_definition = self.CONSTANTS.DEFAULT_COLUMN_DEFINITION.copy()

        statistic_key = TableColumn.CONSTANTS.SIGNAL_STATISTICS[statistic.lower()]
        column_definition['key'] = f"{statistic_key}_{item_id}"
        column_definition['statisticKey'] = statistic_key
        column_definition['signalId'] = item_id
        return cast(ConditionTableColumnSignalStatistic, self._add_column(column_definition))

    def remove_column_statistic(self, item_id: str, statistic: str):
        """
        Remove a signal statistic column from the table.

        Parameters
        ----------
        item_id: str
            ID of the signal to remove from the table
        statistic: str
            Statistic to remove for the signal. Must be one of: {0}
        """
        if statistic.lower() not in TableColumn.CONSTANTS.SIGNAL_STATISTICS:
            raise SPyValueError(f"Statistic must be one of {TableColumn.CONSTANTS.SIGNAL_STATISTICS.keys()}")
        statistic_key = TableColumn.CONSTANTS.SIGNAL_STATISTICS[statistic.lower()]
        key = f"{statistic_key}_{item_id}"
        self._remove_column(key)

    @docstring_parameter(ConditionTableToolbar.add_row_custom_text.__doc__)
    def add_row_custom_text(self, column_values: Union[List[str], Dict[str, str]]) -> ConditionTableRowCustomText:
        """
        Add and return a row that displays custom text in the table.
        Once returned, the row can be manipulated to adjust the appearance of the custom text.

        Parameters
        ----------
        column_values: Union[List[str], Dict[str, str]]
            List of string values to display in the row or a dictionary of column keys and values

        """
        cells = {}
        if isinstance(column_values, list):
            # if given a list of strings, assign to columns in the order that they are currently arranged
            if len(column_values) > len(self):
                raise SPyValueError(f'{len(column_values)} column values provided, but only '
                                    f'{len(self)} '
                                    f'columns exist')
            for i, value in enumerate(column_values):
                cells[self[i].key] = value
        if isinstance(column_values, dict):
            cells = column_values
        column_definition = self.CONSTANTS.DEFAULT_COLUMN_DEFINITION.copy()
        column_definition['type'] = 'text'
        column_definition['key'] = _common.new_placeholder_guid()
        column_definition['cells'] = cells
        return cast(ConditionTableRowCustomText, self._add_column(column_definition))

    @docstring_parameter(ConditionTableToolbar.remove_row_custom_text.__doc__)
    def remove_row_custom_text(self):
        """
        Remove all rows that displays custom text in the table.
        """
        columns_to_remove = [column for column in self._get_columns() if
                             isinstance(column, ConditionTableRowCustomText)]
        for column in columns_to_remove:
            self._remove_column(column.key)

    @docstring_parameter(ConditionTableToolbar.add_row_column_labels.__doc__)
    def add_row_column_labels(self) -> ConditionTableRow:
        """
        Enable and return the row that displays column labels in the table.
        Once returned, the row can be manipulated to adjust the appearance of the column labels.
        """
        column_definition = self.CONSTANTS.DEFAULT_COLUMN_DEFINITION.copy()
        column_definition['key'] = ConditionTableRow.CONSTANTS.COLUMN_LABELS
        return cast(ConditionTableRow, self._add_column(column_definition))

    @docstring_parameter(ConditionTableToolbar.remove_row_column_labels.__doc__)
    def remove_row_column_labels(self):
        """
        Hide the row that displays column labels in the table.
        """
        if ConditionTableRow.CONSTANTS.COLUMN_LABELS in self._get_columns():
            self._remove_column(ConditionTableRow.CONSTANTS.COLUMN_LABELS)

    @docstring_parameter(ConditionTableToolbar.add_row_unit_of_measure.__doc__)
    def add_row_unit_of_measure(self) -> ConditionTableRow:
        """
        Enable and return the row that displays units of measure in the table.
        When the row is present, units will be moved from within each cell to the row.
        Once returned, this row can be manipulated to adjust the appearance of the units of measure.
        """
        column_definition = self.CONSTANTS.DEFAULT_COLUMN_DEFINITION.copy()
        column_definition['key'] = ConditionTableRow.CONSTANTS.UNIT_OF_MEASURE
        return cast(ConditionTableRow, self._add_column(column_definition))

    @docstring_parameter(ConditionTableToolbar.remove_row_unit_of_measure.__doc__)
    def remove_row_unit_of_measure(self):
        """
        Hide the row that displays units of measure in the table.
        """
        if ConditionTableRow.CONSTANTS.UNIT_OF_MEASURE in self._get_columns():
            self._remove_column(ConditionTableRow.CONSTANTS.UNIT_OF_MEASURE)

    def _get_grouped_columns(self) -> List[TableColumn]:
        return sorted([column for column in self if column.grouping], key=lambda column: column.group_order)

    def _set_grouped_columns(self, value: List[TableColumn]):
        if not (isinstance(value, list)) and not (isinstance(value, ConditionTableColumns)):
            raise SPyTypeError(f"'grouped_columns' must be a list of columns")

        # ensure all columns given are currently in the table
        if not all(column in self for column in value):
            raise SPyValueError('All columns provided must be in the table')

        # do this in two stages. first remove grouping from all columns
        # and then apply to the columns specified
        for column in self:
            column.grouping = False
            column.group_order = None

        if value:
            for row_group_order, column in enumerate(value):
                column.grouping = True
                column.group_order = row_group_order


class SimpleTableColumns(TableColumns):
    """
    Column configuration for Simple Tables. Use methods on this object to add or remove columns from the table.
    """
    TABLE_MODE = TableToolbar.CONSTANTS.SIMPLE_TABLE_MODE

    def _column_factory(self, column_definition: dict):
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def add_column_property(self, key: str):
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def remove_column_property(self, key: str):
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def add_column_custom_text(self, column_values: Union[List[str], Dict[str, str]]):
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def remove_column_custom_text(self):
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def _get_interactable_columns(self) -> List[TableColumn]:
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def _get_grouped_columns(self) -> List[TableColumn]:
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

    def _set_grouped_columns(self, value: List[TableColumn]):
        raise NotImplementedError('SPy does not currently support manipulating columns in simple table mode')

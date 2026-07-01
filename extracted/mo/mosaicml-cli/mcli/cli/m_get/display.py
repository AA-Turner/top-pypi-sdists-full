"""Helpers for `mcli get` displays"""
import datetime
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple

import yaml
from rich.table import Table

from mcli.utils.utils_logging import console, err_console
from mcli.utils.utils_rich import create_table

logger = logging.getLogger(__name__)


class OutputDisplay(Enum):
    TABLE = 'table'
    NAME = 'name'
    JSON = 'json'

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)


@dataclass
class MCLIDisplayItem():
    """Item for display in an `mcli get` list of items
    """

    def __init__(self, obj: Dict):
        """Initialize a display item from an object
        object: The dictionary to initialize from. Dict keys should correspond to column names.
        """
        for col_name, val in obj.items():
            setattr(self, col_name, val)

    def to_dict(self) -> Dict[str, Any]:
        """Get the current object as a dictionary

        Returns:
            Dict[str, Any]: Dictionary representation of the object
        """

        def process_field_value(field_value: Any) -> Optional[Any]:
            """ Function that processes a field value based on its type into serializable form
            If a field value is an enum, it'll unpack it back to its serializable json value
            If a field is a list, it'll recursively process all elements
            """

            if isinstance(field_value, Enum):
                return str(field_value.value)
            elif isinstance(field_value, datetime.datetime):
                return field_value.isoformat()
            elif isinstance(field_value, (dict, list)):
                return field_value
            elif field_value is not None:
                return str(field_value)

        data = {}
        for field, value in self.__dict__.items():
            value = process_field_value(value)
            data[field] = value

        return data


class MCLIGetDisplay(ABC):
    """ABC for all `mcli get` lists
    """

    @property
    def index_label(self) -> str:
        return "name"

    def create_custom_table(self, data: List[Any]) -> Optional[Table]:  # pylint: disable=unused-argument
        """Override for custom create display table formatting"""
        return None

    @property
    def custom_column_names(self) -> Optional[List[str]]:
        """Override column names for display"""
        return None

    def print(self, output: OutputDisplay, markup: bool = True):
        items = self.get_list()
        if output == OutputDisplay.TABLE:
            if not items:
                err_console.print('No items found.')
                return
            disp = self.to_table(items)
        elif output == OutputDisplay.NAME:
            names = self.to_name(items)
            disp = '\n'.join(names)
        elif output == OutputDisplay.JSON:
            json_list = self.to_json(items)
            disp = json.dumps(json_list)
        else:
            raise ValueError(f'output is not a known display type. It must be one of {list(OutputDisplay)}')
        console.print(disp, markup=markup)

    def get_list(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self]

    @classmethod
    def clean_label(cls, item: Dict[str, Any]) -> Dict[str, Any]:
        return {(k if k not in ["End Time", "ETA"] else "End Time / ETA"): v for k, v in item.items()}

    def clean_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Given a list of inputs for display items, this will correct any misconfigured keys that come
        from ETA and End Time logic.

        Only the `mcli util` and `mcli get runs` commands use this class. `mcli util` does not use the
        "End Time" label, since it only shows active runs.
        """
        has_eta = False
        has_end_time = False
        for item in items:
            if "End Time" in item:
                has_end_time = True
            if "ETA" in item:
                has_eta = True
            if has_eta and has_end_time:
                break

        # If the items use both the "End Time" and "ETA" labels, we need to use one shared label for
        # the display
        if has_end_time and has_eta:
            return [self.clean_label(item) for item in items]

        # If the "ETA" label is used, but not "End Time", we must sanitize the list to avoid errors
        # with `mcli util`.
        elif has_eta:
            for item in items:
                if "ETA" not in item:
                    item["ETA"] = '-'
        return items

    def to_table(self, items: List[Dict[str, Any]]) -> Table:

        def _to_str(obj: Any) -> str:
            return yaml.safe_dump(obj, default_flow_style=None).strip() if not isinstance(obj, str) else obj

        items = self.clean_items(items)
        column_names = [key for key, val in items[0].items() if val is not None and key != self.index_label]
        columns, names = [], []
        for item in items:
            if self.index_label:
                names.append(item[self.index_label])
            columns.append(tuple(_to_str(item[key]) for key in column_names))
            for col, val in item.items():
                item[col] = _to_str(val)

        column_names = self.custom_column_names or column_names

        # pylint: disable-next=assignment-from-none
        custom_table = self.create_custom_table(data=items)
        return custom_table if custom_table else create_display_table(names, columns, column_names,
                                                                      self.index_label.upper())

    def to_name(self, items: List[Dict[str, Any]]) -> List[str]:
        res = []
        for item in items:
            value = item[self.index_label]
            if value:
                # hack; we put a dog in the run display name
                res.append(value.replace('🐕', '').strip())
        return res

    def to_json(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return items

    @abstractmethod
    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        ...


def create_vertical_display_table(data: Dict[str, str], padding: Optional[Tuple[int, int]] = None) -> Table:
    final_padding = (0, 5) if not padding else padding
    grid = Table.grid(expand=False, padding=final_padding)
    # left column is header, right column is data
    grid.add_column(justify="left")
    grid.add_column(justify="left")
    for col, val in data.items():
        grid.add_row(col, val)
    return grid


def get_min_width(rows: List[Tuple[str]], index: int):
    return max(len(row[index]) for row in rows)


def create_display_table(names: List[str],
                         rows: List[Tuple[str]],
                         column_names: List[str],
                         index_label: str = 'NAME') -> Table:
    never_truncate = ["id", "ID"]
    return create_table(data=rows,
                        indices=names,
                        index_label=index_label,
                        columns=[ss.upper() for ss in column_names],
                        table_kwargs={
                            'box': None,
                            'pad_edge': False
                        },
                        index_kwargs={
                            'justify': 'left',
                            'no_wrap': True
                        },
                        col_kwargs_override={
                            column_name.upper(): {
                                'min_width': get_min_width(rows, i),
                            } if column_name in never_truncate else {} for i, column_name in enumerate(column_names)
                        })

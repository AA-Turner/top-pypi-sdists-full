from copy import deepcopy
from datetime import datetime
from datetime import timezone
from typing import Dict
from typing import List
from typing import Tuple

from google.protobuf import timestamp_pb2
from jinja2 import BaseLoader
from jinja2 import Environment
from texttable import Texttable

from tecton_proto.data.summary__client_pb2 import FcoSummary
from tecton_proto.data.summary__client_pb2 import SummaryItem


_TABLE_HTML_TEMPLATE = """
<table>
<thead>
    <tr>
    {% for heading in headings %}
    <th style='text-align: left;'>{{heading}}</th>
    {% endfor %}
    </tr>
</thead>
<tbody>
    {% for item in items %}
    <tr>
        {% for value in item %}
        {% if value is string and '\n' in value %}
        <td style='text-align: left;'><pre style='padding: 5px; border:1px solid #efefef'>{{value}}</pre></td>
        {% else %}
        <td style='text-align: left;'>{{value}}</td>
        {% endif %}
        {% endfor %}
    </tr>
    {% endfor %}
</tbody>
</table>
"""


def _fco_metadata_formatter(key, value):
    if isinstance(value, timestamp_pb2.Timestamp):
        t = datetime.fromtimestamp(value.ToSeconds())
        return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    if key == "featureStartTimeSeconds":
        t = datetime.fromtimestamp(int(value))
        return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    if key == "tags":
        return dict(value)
    return value


class Displayable(object):
    """Class that can display data in string, HTML, or dictionary format."""

    _table_template = Environment(loader=BaseLoader(), autoescape=True).from_string(_TABLE_HTML_TEMPLATE)

    def __init__(self, text_table: Texttable, html: str, data: Dict):
        self._text_table = text_table
        self._html = html
        self._data = data

    def __repr__(self):
        return self._text_table.draw()

    def __str__(self):
        return self.__repr__()

    def _repr_html_(self):
        return self._html

    def to_dict(self) -> Dict:
        return deepcopy(self._data)

    @classmethod
    def from_table(
        cls, headings: List[str], rows: List[Tuple], max_width=None, center_align: bool = False
    ) -> "Displayable":
        """
        Returns a Displayable based on tabular data containing an arbitrary number of rows.

        :param headings: N-element list of heading names.
        :param rows: List of N-element tuples containing each row's data.
        :max_width: Optional max-width for the table. Setting to zero creates an unlimited width table.
        """
        for row_index, row in enumerate(rows):
            if len(row) != len(headings):
                msg = f"malformed dimensions: headings has length {len(headings)}, but row {row_index} has length {len(row)}"
                raise ValueError(msg)

        text_table = Texttable()
        if max_width is not None:
            text_table.set_max_width(max_width)
        text_table.add_rows(rows, header=False)
        text_table.header(headings)
        text_table.set_deco(Texttable.HEADER)
        if center_align:
            # Align columns in the middle horizontally
            text_table.set_cols_align(["c" for _ in range(len(headings))])

        # Build HTML version.
        html = cls._table_template.render(headings=headings, items=rows)

        # Build dict version.
        data = {"data": []}
        for row in rows:
            data["data"].append({headings[i]: row[i] for i in range(len(headings))})

        return cls(text_table, html, data)

    @classmethod
    def from_properties(cls, items: List[Tuple]) -> "Displayable":
        """
        Returns a Displayable based on key-value properties.

        :param items: List of 2-element tuples.
        """
        for row_index, item in enumerate(items):
            if len(item) != 2:
                msg = f"row {row_index} has length {len(item)}, but should be 2"
                raise ValueError(msg)

        text_table = Texttable()
        text_table.add_rows(items, header=False)
        text_table.set_deco(Texttable.BORDER | Texttable.VLINES | Texttable.HLINES)

        # build HTML version
        html = cls._table_template.render(items=items)

        # Build dictionary version.
        # E.g. { "k1": "v1", "k2", "v2"}
        data = {item[0]: item[1] for item in items}
        return cls(text_table, html, data)

    @classmethod
    def from_fco_summary(
        cls,
        fco_summary: FcoSummary,
        additional_items: List[Tuple] = [],
    ) -> "Displayable":
        """
        Returns a Displayable based on an FcoSummary proto.

        :param fco_summary: FcoSummary proto.
        :param additional_items: Optional additional 2-element tuples to be displayed.
        """
        data = cls._fco_summary_to_dict(fco_summary)
        for key, value in additional_items:
            data[key] = _fco_metadata_formatter(key, value)

        table_items = []
        for display_name, v in data.items():
            value = None
            if isinstance(v, list):
                value = ", ".join(v)
                table_items.append((display_name, value))
            elif isinstance(v, dict):
                # Render nested tables
                value = cls._draw_nested_table_from_dict(v)
                table_items.append((display_name, value))
            elif isinstance(v, str):
                table_items.append((display_name, v))
            else:
                msg = f"Unsupported type {type(v)}"
                raise TypeError(msg)

        text_table = Texttable()
        text_table.add_rows(table_items, header=False)
        text_table.set_deco(Texttable.BORDER | Texttable.VLINES | Texttable.HLINES)
        text_table.set_cols_valign(["m", "m"])

        # build HTML version
        html = cls._table_template.render(items=table_items)

        return cls(text_table, html, data)

    @classmethod
    def _fco_summary_to_dict(cls, fco_summary: FcoSummary) -> Dict:
        fco_metadata_fields = [
            "name",
            "workspace",
            "description",
            "created_at",
            "owner",
            "last_modified_by",
            "source_filename",
            "tags",
        ]
        metadata = {
            _transform_field_name(field): _fco_metadata_formatter(field, getattr(fco_summary.fco_metadata, field))
            for field in fco_metadata_fields
        }
        summarydata = cls._get_nested_dict(list(fco_summary.summary_items))
        return {**metadata, **summarydata}

    @classmethod
    def _get_nested_dict(cls, nested_summary_items: List[SummaryItem]) -> Dict:
        data = {}
        for item in nested_summary_items:
            if not item.HasField("display_name"):
                continue
            if item.HasField("value"):
                data_value = _fco_metadata_formatter(item.key, item.value)
            elif len(item.multi_values) > 0:
                data_value = list(item.multi_values)
            elif len(item.nested_summary_items) > 0:
                data_value = cls._get_nested_dict(list(item.nested_summary_items))
            else:
                data_value = ""
            data[item.display_name] = data_value
        return data

    @classmethod
    def _draw_nested_table_from_dict(cls, data: Dict):
        table_items = []
        for display_name, v in data.items():
            value = None
            if isinstance(v, list):
                value = ", ".join(v)
                table_items.append((display_name, value))
            elif isinstance(v, dict):
                value = str(cls._draw_nested_table_from_dict(v))
                table_items.append((display_name, value))
            elif isinstance(v, str):
                table_items.append((display_name, v))
            else:
                msg = f"Unsupported type {type(v)}"
                raise TypeError(msg)

        text_table = Texttable()
        text_table.add_rows(table_items, header=False)
        text_table.set_deco(Texttable.HLINES)
        return text_table.draw()


def _transform_field_name(name):
    return name.replace("_", " ").title()

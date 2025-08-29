import operator
import json
from babel import numbers
from datetime import timezone, datetime

from agilicus import context
from agilicus.output.json import convert_to_json

from dataclasses import dataclass
from typing import Callable

from prettytable import PrettyTable, MARKDOWN
from . import column_builder


def format_date(date_input):
    return date_input.strftime("%Y-%m-%d %H:%M:%S.%f")


def format_date_only(date_input):
    return date_input.strftime("%Y-%m-%d")


def date_else_identity(input_obj, ctx=None):
    if isinstance(input_obj, datetime):
        return format_date(input_obj)
    if ctx and not context.output_console(ctx):
        return input_obj
    if isinstance(input_obj, list):
        list_as_str = ""
        for obj in input_obj:
            try_dict = None
            try:
                try_dict = obj.to_dict()
            except Exception:
                pass
            if isinstance(try_dict, dict):
                prefix = "-"
                for k, v in try_dict.items():
                    list_as_str += f"{prefix} {k}: {v}\n"
                    prefix = " "
            else:
                list_as_str += f"- {obj}\n"
        return list_as_str
    return input_obj


def format_timestamp(input_obj, ctx=None):
    return datetime.fromtimestamp(input_obj)


def format_currency_from_cents(cents, currency=None, ctx=None):
    currency_symbol = ""
    if currency:
        currency_symbol = numbers.get_currency_symbol(currency.upper(), locale="en")
    if cents >= 0:
        return currency_symbol + "{:,.2f}".format(cents / 100)
    else:
        return "(" + currency_symbol + "{:,.2f}".format(-cents / 100) + ")"


@dataclass
class OutputColumn:
    in_name: str
    out_name: str
    format_fn: Callable = date_else_identity
    getter: Callable = None
    optional: bool = False


def column(name, newname=None, optional=False, getter=None, format_fn=None):
    out_name = newname
    if not out_name:
        out_name = name
    if not format_fn:
        format_fn = date_else_identity
    return OutputColumn(
        in_name=name,
        out_name=out_name,
        optional=optional,
        getter=getter,
        format_fn=format_fn,
    )


def mapped_column(in_name, out_name):
    return OutputColumn(in_name=in_name, out_name=out_name)


def subtable(
    ctx,
    in_name,
    columns,
    out_name=None,
    subobject_name=None,
    table_getter=operator.attrgetter,
    optional=False,
):
    if not out_name:
        out_name = in_name

    outer_ctx = ctx

    def format_fn(records, ctx=None):
        return format_table(
            outer_ctx, records, columns, getter=table_getter, nested=True
        )

    def getter(record, base_getter):
        subobject = base_getter(subobject_name)(record)
        return base_getter(in_name)(subobject)

    col_getter = None
    if subobject_name:
        col_getter = getter

    return OutputColumn(
        in_name=in_name,
        out_name=out_name,
        format_fn=format_fn,
        getter=col_getter,
        optional=optional,
    )


def subobject_column(
    in_name,
    out_name,
    subobject_name,
    optional=False,
    max_size=None,
    json_dump=None,
    formatter=None,
    subobject_keys=None,
    **kwargs,
):
    if not out_name:
        out_name = in_name

    def output_val(val):
        if json_dump:
            return json.dumps(val, indent=4)
        return val

    def getter(record, base_getter):
        names = subobject_keys
        if not names:
            names = in_name
        if not isinstance(names, list):
            names = [names]

        caught_exc = None
        for name in names:
            val = None
            try:
                subobject = base_getter(subobject_name)(record)
                val = base_getter(name)(subobject)
                if max_size is not None and val:
                    return output_val(val[:max_size])
                if val is not None or len(names) == 1:
                    return output_val(val)
            except Exception as exc:
                caught_exc = exc

        if not optional and caught_exc:
            raise caught_exc
        return None

    result = OutputColumn(
        in_name=in_name, out_name=out_name, getter=getter, optional=optional
    )

    if formatter:
        result.format_fn = formatter
    return result


def metadata_column(in_name, out_name=None, **kwargs):
    return subobject_column(in_name, out_name, "metadata", **kwargs)


def spec_column(in_name, out_name=None, **kwargs):
    return subobject_column(in_name, out_name, "spec", **kwargs)


def status_column(in_name, out_name=None, **kwargs):
    return subobject_column(in_name, out_name, "status", **kwargs)


def constant_if_exists(column: OutputColumn, constant, default=None):
    orig = column.format_fn

    def check(val, ctx=None):
        if orig:
            val = orig(val, ctx=ctx)

        if val:
            return constant
        return default

    column.format_fn = check
    return column


def list_count(column: OutputColumn):
    orig = column.format_fn

    def formatter(val, ctx=None):
        if isinstance(val, list):
            return len(val)
        if orig:
            val = orig(val, ctx=ctx)
        return val

    column.format_fn = formatter
    return column


def list_map(column: OutputColumn, mapfn: Callable):
    orig = column.getter

    def getter(record, getter):
        if orig:
            val = orig(record, getter)
        else:
            val = getter(column.in_name)(record)
        if isinstance(val, list):
            val = [mapfn(v) for v in val]
        return val

    column.getter = getter
    return column


def expand_dict(column: OutputColumn):
    orig = column.getter

    def getter(record, getter):
        if orig:
            val = orig(record, getter)
        else:
            val = getter(column.in_name)(record)
        if val is None:
            return val
        if not isinstance(val, dict):
            val = val.to_dict()
        return list(val.items())

    column.getter = getter
    return column


def summarize(column: OutputColumn, max_length: int):
    orig = column.format_fn

    def format_list(val, ctx=None):
        if len(val) <= max_length:
            if orig:
                val = orig(val, ctx=ctx)
            return val

        val = val[:max_length]
        if orig:
            val = orig(val)
        return val + "[truncated]"

    def formatter(val, ctx=None):
        if isinstance(val, list):
            return format_list(val, ctx=ctx)

        if orig:
            val = orig(val)

        if isinstance(val, str) and len(val) > max_length:
            idx = int(max_length / 2)
            return val[:idx] + "..." + val[-idx:]
        return val

    column.format_fn = formatter
    return column


# An implementation of attrgetter that handles a None in the middle
def short_circuit_attrgetter(item):
    def func(obj):
        for name in item.split("."):
            if obj is None:
                return None
            obj = getattr(obj, name)
        return obj

    return func


def _dump_json(ctx, to_dump, indent=2):
    # Sometimes a compound table can be a dict at its root. When formatting as json
    # handle that case
    if not isinstance(to_dump, list):
        to_dump_as_dict = to_dump
        if not isinstance(to_dump, dict):
            to_dump_as_dict = to_dump.to_dict()
    else:
        to_dump_as_dict = [
            record.to_dict() if not isinstance(record, dict) else record
            for record in to_dump
        ]

    return convert_to_json(ctx, to_dump_as_dict, indent=indent)


def output_is_formatted(ctx):
    return context.get_value(ctx, "output_format") in ("console", "csv")


def get_table_style(ctx):
    table_style_str = context.get_value(ctx, "output_format")
    table_style = None
    if table_style_str and not output_is_formatted(ctx):
        from prettytable import (
            DEFAULT,
            MARKDOWN,
            PLAIN_COLUMNS,
            TableStyle,
        )

        if table_style_str == "default":
            table_style = DEFAULT
        elif table_style_str == "markdown":
            table_style = MARKDOWN
        elif table_style_str == "plain":
            table_style = PLAIN_COLUMNS
        elif table_style_str == "msword":
            table_style = TableStyle.MSWORD_FRIENDLY
        else:
            raise Exception(f"invalid table style {table_style_str}")
    return table_style


def format_table(
    ctx,
    records,
    columns,
    getter=short_circuit_attrgetter,
    row_filter=None,
    nested=False,
):
    if context.output_json(ctx):
        return _dump_json(ctx, records)
    table = PrettyTable([column.out_name for column in columns])

    table_style = get_table_style(ctx)
    if table_style:
        table.set_style(table_style)

    if not records:
        records = []

    if not isinstance(records, list):
        records = [records]

    for record in records:
        row = []

        if row_filter is not None:
            if not row_filter(record):
                continue
        for column in columns:
            in_value = None
            if column.getter:
                try:
                    in_value = column.getter(record, getter)
                except Exception as exc:
                    if not column.optional:
                        raise exc
            else:
                try:
                    in_value = getter(column.in_name)(record)
                except Exception as exc:
                    if not column.optional:
                        raise exc

            out_value = "---"
            if in_value is not None:
                out_value = column.format_fn(in_value, ctx=ctx)
            row.append(out_value)

        table.add_row(row)
    table.align = "l"

    return _table_to_console(ctx, table, nested)


def _table_to_console(ctx, table: PrettyTable, nested):
    if context.output_csv(ctx):
        if nested:
            return table.get_json_string(header=False, indent=None, default=str)
        return table.get_csv_string()
    if context.output_markdown(ctx):
        table.set_style(MARKDOWN)
    return table


def output_entry(ctx, entry, headers=None):
    if ctx.obj["output_format"] == "json":
        print(_dump_json(ctx, entry))
        if headers and ctx.obj["output_headers"]:
            print(_dump_json(ctx, headers.__dict__))
        return
    table = PrettyTable(["field", "value"])
    if entry:
        for k, v in list(entry.items()):
            if k == "nbf" or k == "exp" or k == "iat":
                _t = v
                if not isinstance(_t, str):
                    _t = datetime.fromtimestamp(v, timezone.utc).strftime(
                        "%Y-%m-%d %H:%M:%S %z"
                    )
                table.add_row([k, json.dumps(_t, indent=4)])
            elif k == "created" or k == "updated":
                table.add_row([k, v])
            elif isinstance(v, str):
                table.add_row([k, v])
            else:
                table.add_row([k, json.dumps(v, indent=4, default=str)])
        table.align = "l"
        print(table)
        if headers and ctx.obj["output_headers"]:
            table = PrettyTable(["header-key", "value"])
            for k, v in list(headers.items()):
                table.add_row([k, v])
            table.align = "l"
            print(table)


def make_columns(*args, **kwargs):
    return column_builder.make_columns(*args, **kwargs)


def _get_with_default(column, record):
    getter = column.getter
    if not getter:
        getter = short_circuit_attrgetter
    return getter(column.in_name)(record)


def object_subtable(
    ctx,
    in_name,
    columns,
    out_name=None,
    subobject_name=None,
    table_getter=operator.itemgetter,
    optional=False,
):
    """
    converts an object with columns defined by "columns" into a subtable.
    """
    if not out_name:
        out_name = in_name

    def scalar_name(column, idx):
        return column.out_name

    def list_name(column, idx):
        return f"{column.out_name}.{idx}"

    subtable_columns = [column("name"), column("value")]

    outer_ctx = ctx

    def format_fn(records, ctx=None):
        subtable_records = []
        namer = scalar_name
        if isinstance(records, list):
            namer = list_name
        else:
            records = [records]

        for idx, record in enumerate(records):
            subtable_records.extend(
                [
                    {
                        "name": namer(column, idx),
                        "value": _get_with_default(column, record),
                    }
                    for column in columns
                ]
            )

        return format_table(
            outer_ctx,
            subtable_records,
            subtable_columns,
            getter=table_getter,
            nested=True,
        )

    def getter(record, base_getter):
        subobject = base_getter(subobject_name)(record)
        return base_getter(in_name)(subobject)

    col_getter = None
    if subobject_name:
        col_getter = getter

    return OutputColumn(
        in_name=in_name,
        out_name=out_name,
        format_fn=format_fn,
        getter=col_getter,
        optional=optional,
    )

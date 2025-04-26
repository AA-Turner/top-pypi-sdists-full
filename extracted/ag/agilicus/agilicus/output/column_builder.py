import yaml
import re
from collections import OrderedDict
from . import table


class ColumnBuilder:
    def __init__(self, ctx, result_list):
        self.ctx = ctx
        self.result_list = result_list

    def _get_column_names(self, subtable_column_name):
        results = set()
        if not self.result_list:
            return results
        obj = self.result_list[0]
        if subtable_column_name:
            obj = getattr(obj, subtable_column_name)
            if not obj:
                # nothing available
                return results
            obj = obj[0]
        return set(obj.to_dict().keys())

    def _make_subtable(self, table_name, format_doc):
        m = re.search("(.*)\\((.+)\\).*", table_name)
        all_options = {}
        if m:
            found = m.group(2)
            for option in found.split(","):
                split_str = option.split("=")
                all_options[split_str[0]] = split_str[1]
            table_name = m.group(1)
        columns = self.build_columns(format_doc, subtable_column_name=table_name)
        return table.subtable(
            self.ctx,
            table_name,
            columns=columns,
            optional=True,
            **all_options,
        )

    def _get_output_column(self, column_name: str):
        m = re.search("(.*)\\((.+)\\).*", column_name)
        if m:
            found = m.group(2)
            all_options = {}
            for option in found.split(","):
                split_str = option.split("=")
                all_options[split_str[0]] = split_str[1]
            return table.column(m.group(1), optional=True, **all_options)
        return table.column(column_name, optional=True)

    def build_columns(
        self,
        format_doc,
        subtable_column_name=None,
        **kwargs,
    ):
        column_names = OrderedDict()
        for column_name in format_doc:
            if column_name == "all":
                for c in self._get_column_names(subtable_column_name):
                    column_names[c] = self._get_output_column(c)
            elif isinstance(column_name, dict):
                sub_table_col = list(column_name.keys())[0]
                sub_table_val = column_name[sub_table_col]
                column_names[sub_table_col] = self._make_subtable(
                    sub_table_col,
                    sub_table_val,
                )
            else:
                column_names[column_name] = self._get_output_column(column_name)

        return list(column_names.values())


def make_columns(
    ctx,
    result_list,
    base_columns,
    show=None,
    clear=False,
    **kwargs,
):
    """
    A generic build for making columns, configurable by user
    to choose specific columns or subtables.

    Add the following options to your command:
    @click.option("--show-columns", type=str, default=None)
    @click.option("--reset-columns", is_flag=True, default=False)

    Then call make_columns (for example)
    columns = make_columns(ctx, results, ["id", "email"], show=show, clear=clear)

    This make the 'default' show have columns 'id', 'email'.

    You may clear it, and start from scratch:

    show just email:
      --clear --show email

    show email and the id
      --clear --show id,email

    show all columns
      --clear --show all

    show a subtable:
      --clear --show "[id,email,upstream_user_identities: [all]]"

    show a specific column in the subtable:
      --clear --show "[id,email,upstream_user_identities: [spec.upstream_idp_id]]"

     rename the output column
      --clear --show "[id,email,upstream_user_identities: [spec.upstream_idp_id(newname=upstream_idp_id)]]"  # noqa

    Note that the show format is a valid yaml doc. Its a list of columns, when
    a mapping (dictionary) is found that is assumed to be a subtable, where the
    key name is the subtable name
    """
    format_doc = []
    if not clear and base_columns:
        format_doc = yaml.safe_load(base_columns)

    if show:
        if "[" not in show:
            # incase the user hasn't created a valid yaml list,
            # make it a list.
            show = "[" + show + "]"
        format_doc.extend(yaml.safe_load(show))

    return ColumnBuilder(ctx, result_list).build_columns(format_doc, **kwargs)

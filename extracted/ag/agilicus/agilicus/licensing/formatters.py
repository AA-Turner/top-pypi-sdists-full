from operator import attrgetter

from ..output.table import (
    column,
    list_map,
    expand_dict,
    summarize,
)


def constraint_columns(num_subtable_rows=10, column_func=column):
    return [
        summarize(
            list_map(
                column_func("license_constraints", "constraints"), attrgetter("name")
            ),
            num_subtable_rows,
        ),
        summarize(
            list_map(
                expand_dict(column_func("constraint_variables", "variables")),
                lambda item: item[0],
            ),
            num_subtable_rows,
        ),
    ]

"""Test for column definition in ag-grid."""

from reflex.vars import FunctionVar, Var
from reflex.vars.function import ArgsFunctionOperation

from reflex_enterprise.components.ag_grid.resources import ColumnDef


def test_column_def():
    """Test basic column definition."""
    col = ColumnDef(field="name", header_name="Name")
    assert col.dict() == {"field": "name", "headerName": "Name"}


def test_column_def_camel_case():
    """Test column definition with camel case."""
    dict = {
        "field": "name",
        "headerName": "Name",
    }
    col = ColumnDef(**dict)  # pyright: ignore[reportArgumentType]
    assert col.dict() == {"field": "name", "headerName": "Name"}


def test_column_def_value_formatter():
    """Test column definition with value formatter."""
    format_expr = "params.value + '?'"

    col = ColumnDef(
        field="name",
        header_name="Name",
        value_formatter=format_expr,
    ).dict()
    assert isinstance(col["valueFormatter"], FunctionVar)
    assert str(col["valueFormatter"]) == f"((params) => {format_expr})"

    col2 = ColumnDef(
        field="name",
        header_name="Name",
        value_formatter={
            "function": format_expr,
        },
    ).dict()
    assert isinstance(col2["valueFormatter"], FunctionVar)
    assert str(col2["valueFormatter"]) == f"((params) => {format_expr})"

    custom_format_expr = "foobar.value + '?'"
    col3 = ColumnDef(
        field="name",
        header_name="Name",
        value_formatter=ArgsFunctionOperation.create(
            args_names=["foobar"],
            return_expr=Var(custom_format_expr),
        ),
    ).dict()
    assert isinstance(col3["valueFormatter"], FunctionVar)
    assert str(col3["valueFormatter"]) == f"((foobar) => {custom_format_expr})"

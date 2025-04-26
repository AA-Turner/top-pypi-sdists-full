from typing import List, Mapping

import pyarrow as pa

from chalk.features._encoding.pyarrow import pyarrow_to_polars
from chalk.utils.df_utils import pa_cast, pa_table_to_pl_df


def convert_hex_to_binary(table: pa.Table, cols_to_convert: List[str]) -> pa.Table:
    """
    Redshift returns binary data as a hex string.
    Ideally we'd add SQLAlchemy compiler hooks to do this conversion, but I'm not sure how to add this in the Chalk client w/o potentially clobbering other Redshift clients the customer may have.
    :param table: Table of data
    :param cols_to_convert: Columns to convert
    :return: Same table, but each column in cols_to_convert have been converterd from a hex string to binary
    """
    import polars as pl

    if len(cols_to_convert) == 0:
        return table
    pl_df = pa_table_to_pl_df(table)
    new_cols = [pl.col(colname).str.decode("hex").alias(colname) for colname in cols_to_convert]
    pl_df.with_columns(new_cols).to_arrow()


def json_parse_and_cast(tbl: pa.Table, schema: Mapping[str, pa.DataType]) -> pa.Table:
    import polars as pl

    """Json-parse any array and struct columns, do a case-insensitive column name mapping, and cast the table schema"""
    name_mapping = {k.upper(): k for k in schema}
    if len(schema) != len(name_mapping):
        raise ValueError(f"Column names must be case-insensitive. Case-insensitive names are {list(schema.keys())}")
    new_col_names: list[str] = []
    if len(name_mapping) != len(tbl.column_names):
        raise ValueError(
            f"Expected {len(name_mapping)} columns, got {len(tbl.column_names)} columns. Expected {list(name_mapping.keys())}; got {tbl.column_names}"
        )
    for x in tbl.column_names:
        cased_name = name_mapping.get(x.upper())
        if cased_name is None:
            raise ValueError(
                f"Did not expect to find column {x} (uppercased to {x.upper()}). Expected uppercase names {list(name_mapping.keys())}"
            )
        new_col_names.append(cased_name)

    tbl = tbl.rename_columns(new_col_names)
    # Snowflake returns arrays and structs as json strings. Parse them into their structured types
    json_cols_to_polars_dtype = {
        col_name: pyarrow_to_polars(pa_dtype, col_name)
        for (col_name, pa_dtype) in schema.items()
        if pa.types.is_struct(pa_dtype)
        or pa.types.is_list(pa_dtype)
        or pa.types.is_large_list(pa_dtype)
        or pa.types.is_fixed_size_list(pa_dtype)
    }
    if len(json_cols_to_polars_dtype) > 0:
        pl_df = pa_table_to_pl_df(tbl)
        pl_exprs: list[pl.Expr] = []
        for col_name, pl_dtype in json_cols_to_polars_dtype.items():
            expr = pl.col(col_name)
            if pl_df.schema[col_name] == pl.Binary():
                expr = expr.cast(pl.Utf8())
            expr = expr.str.json_extract(pl_dtype).alias(col_name)
            pl_exprs.append(expr)

        pl_df = pl_df.with_columns(pl_exprs)
        tbl = pl_df.to_arrow()
    tbl = pa_cast(tbl, pa.schema(schema))
    return tbl

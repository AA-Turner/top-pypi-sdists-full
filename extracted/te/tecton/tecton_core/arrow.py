from typing import Union

import pandas
import pyarrow
import pyarrow.dataset


# These are kwargs for the pyarrow.dataset.ParquetFileFormat.make_write_options function. They are "unwrapped" like this
# because some other APIs (e.g. pyarrow.parquet.write_to_dataset, which is in turn called by
# pandas.DataFrame.to_parquet) also accept write options in kwargs format but not FileWriteOptions format.
PARQUET_WRITE_OPTIONS_KWARGS = {
    "version": "2.4",
    "data_page_version": "1.0",
    "compression": "snappy",
}

PARQUET_WRITE_OPTIONS = pyarrow.dataset.ParquetFileFormat().make_write_options(**PARQUET_WRITE_OPTIONS_KWARGS)


def arrow_to_pandas_dataframe(
    table: Union[pyarrow.Table, pyarrow.RecordBatchReader], use_arrow_types: bool = False
) -> pandas.DataFrame:
    if isinstance(table, pyarrow.RecordBatchReader):
        to_pandas = table.read_pandas
    else:
        to_pandas = table.to_pandas

    if use_arrow_types and hasattr(pandas, "ArrowDtype"):
        return to_pandas(types_mapper=pandas.ArrowDtype)

    df = to_pandas(
        types_mapper={
            # until we upgrade pandas (and move to arrow-based type system)
            # we need to handle int columns that might contain nulls
            pyarrow.int32(): pandas.Int32Dtype(),
            pyarrow.int64(): pandas.Int64Dtype(),
        }.get
    )
    for col in df:
        if pandas.notnull(df[col]).all():
            continue

        # If column contains nulls (ie, numpy.nan or pandas.NA)
        # convert this column type to object to replace these nulls with Python None.
        # This is needed to match transform server, which converts all nulls to Nones.
        df[col] = df[col].astype("object")
        df[col] = df[col].where(pandas.notnull(df[col]), None)

    return df

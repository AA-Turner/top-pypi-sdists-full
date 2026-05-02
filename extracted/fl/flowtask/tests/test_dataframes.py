import pytest
import pandas as pd
import polars as pl
import pyarrow as pa
import datatable as dt
import io

# Import your classes here
from flowtask.interfaces.dataframes import (
    PandasDataframe,
    PolarsDataframe,
    ArrowDataframe,
    DtDataframe
)

@pytest.mark.asyncio
async def test_basic():
    test_data = [{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]

    # Test PandasDataframe
    pandas_df = PandasDataframe()
    result_pd = await pandas_df.create_dataframe(test_data)
    assert isinstance(result_pd, pd.DataFrame)

    # Test PolarsDataframe
    polars_df = PolarsDataframe()
    result_pl = await polars_df.create_dataframe(test_data)
    assert isinstance(result_pl, pl.DataFrame)

    # Test ArrowDataframe
    arrow_df = ArrowDataframe()
    result_pa = await arrow_df.create_dataframe(test_data)
    assert isinstance(result_pa, pa.Table)

    # Test DtDataframe
    dt_df = DtDataframe()
    result_dt = await dt_df.create_dataframe(test_data)
    assert isinstance(result_dt, dt.Frame)

@pytest.mark.asyncio
async def test_bytes():
    # Creating a CSV string and converting it to BytesIO
    csv_data = "col1,col2\n1,a\n2,b"
    test_data = io.BytesIO(csv_data.encode())

    # Test PandasDataframe
    pandas_df = PandasDataframe()
    result_pd = await pandas_df.create_dataframe(test_data)
    assert isinstance(result_pd, pd.DataFrame)

    # Test PolarsDataframe
    polars_df = PolarsDataframe()
    result_pl = await polars_df.create_dataframe(test_data)
    assert isinstance(result_pl, pl.DataFrame)

    # Test ArrowDataframe
    arrow_df = ArrowDataframe()
    table = pa.Table.from_pandas(pd.DataFrame(test_data))
    buf = io.BytesIO()
    pa.parquet.write_table(table, buf)
    buf.seek(0)  # Reset buffer position to the beginning

    result_pa = await arrow_df.create_dataframe(buf)
    assert isinstance(result_pa, pa.Table)

    test_data.seek(0)  # Reset buffer position to the beginning
    result_pa = await arrow_df.create_dataframe(test_data)
    assert isinstance(result_pa, pa.Table)

    # Test DtDataframe
    dt_df = DtDataframe()
    result_dt = await dt_df.create_dataframe(test_data)
    assert isinstance(result_dt, dt.Frame)

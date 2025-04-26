"""This files contains utilities for running feature_table.ingest()."""

import io
import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from typing import Dict
from typing import Tuple

import pandas
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql.types import ArrayType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import FloatType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli.upload_utils import DEFAULT_MAX_WORKERS_THREADS
from tecton.cli.upload_utils import UploadPart
from tecton.cli.upload_utils import get_upload_parts
from tecton_core import errors
from tecton_core import http
from tecton_core import schema
from tecton_core.arrow import PARQUET_WRITE_OPTIONS_KWARGS
from tecton_core.pandas_compat import pandas_to_spark
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import UploadDataframePartRequest
from tecton_spark import schema_spark_utils


logger = logging.getLogger(__name__)


def upload_df_pandas(upload_url: str, df: pandas.DataFrame, parquet: bool = True):
    out_buffer = io.BytesIO()
    if parquet:
        df.to_parquet(out_buffer, index=False, engine="pyarrow", **PARQUET_WRITE_OPTIONS_KWARGS)
    else:
        df.to_csv(out_buffer, index=False, header=False)

    # Maximum 1GB per ingestion
    if out_buffer.__sizeof__() > 5_000_000_000:
        raise errors.FT_DF_TOO_LARGE

    out_buffer.seek(0)
    r = http.session().put(upload_url, data=out_buffer)
    if r.status_code != 200:
        raise errors.FT_UPLOAD_FAILED(r.reason)


def convert_pandas_to_spark_df(df: pandas.DataFrame, view_schema: schema.Schema) -> pyspark_dataframe.DataFrame:
    tc = tecton_context.TectonContext.get_instance()
    spark = tc._spark
    spark_df = pandas_to_spark(spark, df)

    converted_schema = _convert_ingest_schema(spark_df.schema, view_schema)

    if converted_schema != spark_df.schema:
        spark_df = pandas_to_spark(df, schema=converted_schema)

    return spark_df


def _convert_ingest_schema(ingest_schema: StructType, view_schema: schema.Schema) -> StructType:
    """Convert pandas-derived spark schema to Tecton-compatible schema for Feature Tables.

    The Pandas to Spark dataframe conversion implicitly derives the Spark schema.
    We handle converting/correcting for some type conversions where the derived schema and the feature table schema do not match.
    """
    ft_columns = schema_spark_utils.column_name_spark_data_types(view_schema)
    ingest_columns = schema_spark_utils.column_name_spark_data_types(
        schema_spark_utils.schema_from_spark(ingest_schema)
    )

    converted_ingest_schema = StructType()
    int_converted_columns = []

    for col_name, col_type in ingest_columns:
        if col_type == LongType() and (col_name, IntegerType()) in ft_columns:
            int_converted_columns.append(col_name)
            converted_ingest_schema.add(col_name, IntegerType())
        elif col_type == ArrayType(DoubleType()) and (col_name, ArrayType(FloatType())) in ft_columns:
            converted_ingest_schema.add(col_name, ArrayType(FloatType()))
        else:
            converted_ingest_schema.add(col_name, col_type)

    if int_converted_columns:
        logger.warning(
            f"Tecton is casting field(s) {', '.join(int_converted_columns)} to type Integer (was type Long). To remove this warning, use a Long type in the schema."
        )

    return converted_ingest_schema


def upload(workspace: str, key: str, upload_id: str, out_buffer: io.BytesIO, buffer_size: int) -> Dict[int, str]:
    part_data_list = get_upload_parts(file_size=buffer_size)
    with ThreadPoolExecutor(DEFAULT_MAX_WORKERS_THREADS) as executor:
        upload_futures = []
        for part_data in part_data_list:
            future = executor.submit(
                _upload_part,
                upload_part=part_data,
                workspace=workspace,
                parent_upload_id=upload_id,
                key=key,
                data=out_buffer.getbuffer()[part_data.offset : part_data.offset + part_data.part_size],
            )
            upload_futures.append(future)

        results = []
        for future in as_completed(upload_futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error occurred: {e}")
                raise e

        return dict(results)


def _upload_part(
    upload_part: UploadPart, workspace: str, parent_upload_id: str, key: str, data: memoryview
) -> Tuple[int, str]:
    request = UploadDataframePartRequest(
        workspace=workspace,
        key=key,
        parent_upload_id=parent_upload_id,
        part_number=upload_part.part_number,
    )
    response = metadata_service.instance().UploadDataframePart(request)
    signed_url = response.upload_url
    response = http.session().put(signed_url, data=data)
    if response.ok:
        e_tag = response.headers["ETag"]
        return upload_part.part_number, e_tag
    else:
        msg = f"Upload failed with status {response.status_code} and error {response.text}"
        raise ValueError(msg)

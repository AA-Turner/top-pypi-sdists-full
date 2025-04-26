import random
import string
from datetime import datetime
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
from pyspark.sql.types import StructType

import tecton_core.tecton_pendulum as pendulum
from tecton_core import specs
from tecton_core.errors import UDF_ERROR
from tecton_core.errors import UDF_TYPE_ERROR
from tecton_core.materialization_context import MaterializationContext
from tecton_core.pandas_compat import pandas_to_spark
from tecton_core.pipeline.feature_pipeline import FeaturePipeline
from tecton_core.pipeline.pipeline_common import CONSTANT_TYPE
from tecton_core.pipeline.pipeline_common import check_transformation_type
from tecton_core.pipeline.pipeline_common import constant_node_to_value
from tecton_core.pipeline.pipeline_common import get_keyword_inputs
from tecton_core.pipeline.pipeline_common import positional_inputs
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_core.spark_type_annotations import PySparkSession
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.args.transformation__client_pb2 import TransformationMode


class SparkFeaturePipeline(FeaturePipeline):
    # Each internal node in the Pipeline Tree evaluates to a single type of value which can
    # be one of the following:
    _SPARK_INPUT_VALUE_TYPE = Union[PySparkDataFrame, CONSTANT_TYPE, MaterializationContext]

    # note that pipeline is included since this is meant to be a user hint, and it's
    # theoretically possible that a pipeline mode node shows up deeper than expected
    _VALID_MODES = ["pyspark", "spark_sql", "pipeline", "python", "pandas"]

    def __init__(
        self,
        spark: PySparkSession,
        pipeline: PipelineNode,
        transformations: List[specs.TransformationSpec],
        materialization_context_limits: Optional[pendulum.Period] = None,
        schedule_interval: Optional[pendulum.Duration] = None,
        data_source_inputs: Optional[Dict[str, PySparkDataFrame]] = None,
        # output_schema is only used by python/pandas transformations during backfills.
        # Specifically, it applies for Stream feature views with push sources and batch config, during
        # the batch materialization jobs.
        output_schema: Optional[StructType] = None,
    ) -> None:
        self._spark = spark
        self._pipeline = pipeline
        self._output_schema = output_schema
        self._materialization_context_limits = materialization_context_limits
        self._id_to_transformation = {t.id: t for t in transformations}
        self._schedule_interval = schedule_interval
        self._data_source_inputs = data_source_inputs
        self._registered_temp_view_names: List[str] = []

    def get_dataframe(self) -> PySparkDataFrame:
        df = self._node_to_value(self._pipeline.root)
        self._cleanup_temp_tables()
        assert is_pyspark_df(df)
        return df

    def _node_to_value(self, pipeline_node: PipelineNode) -> _SPARK_INPUT_VALUE_TYPE:
        if pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_value(pipeline_node.transformation_node)
        elif pipeline_node.HasField("data_source_node"):
            data_source_node = pipeline_node.data_source_node
            if data_source_node.input_name not in self._data_source_inputs:
                msg = f"Expected inputs {self._data_source_inputs} to contain {data_source_node.input_name}"
                raise ValueError(msg)
            return self._data_source_inputs[data_source_node.input_name]
        elif pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("materialization_context_node") or pipeline_node.HasField("context_node"):
            if self._materialization_context_limits is not None:
                feature_start_time = self._materialization_context_limits.start
                feature_end_time = self._materialization_context_limits.end
                batch_schedule = self._schedule_interval
            else:
                feature_start_time = pendulum.from_timestamp(0, pendulum.tz.UTC)
                feature_end_time = pendulum.datetime(2100, 1, 1)
                batch_schedule = self._schedule_interval or pendulum.duration()
            return MaterializationContext._create_internal(feature_start_time, feature_end_time, batch_schedule)
        elif pipeline_node.HasField("request_data_source_node"):
            msg = "RequestDataSource is not supported in Spark pipelines"
            raise ValueError(msg)
        elif pipeline_node.HasField("feature_view_node"):
            msg = "Dependent FeatureViews are not supported in Spark pipelines"
            raise ValueError(msg)
        else:
            msg = f"Unknown PipelineNode type: {pipeline_node}"
            raise KeyError(msg)

    def _transformation_node_to_value(self, transformation_node: TransformationNode) -> PySparkDataFrame:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[PySparkDataFrame, str, int, float, bool, datetime]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return self._apply_transformation_function(transformation_node, args, kwargs)

    def _apply_transformation_function(
        self, transformation_node: TransformationNode, args: List[Any], kwargs: Dict[str, Any]
    ) -> Union[Dict[str, Any], pandas.DataFrame, PySparkDataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation.

        If needed, resulted function is wrapped with a function that translates mode-specific input/output types to DataFrames.

        Pandas and Python mode cases below run for IngestAPI. See `RealtimeFeaturePipeline` class
        for Realtime Feature Views.
        """
        transformation = self.get_transformation_by_id(transformation_node.transformation_id)
        mode = transformation.transformation_mode
        user_function = transformation.user_function

        if mode == TransformationMode.TRANSFORMATION_MODE_PYSPARK:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e, feature_definition_name=transformation.metadata.name)
            check_transformation_type(transformation.name, res, "pyspark", self._VALID_MODES)
            return res
        elif mode == TransformationMode.TRANSFORMATION_MODE_SPARK_SQL:
            return self._build_spark_sql_function(transformation_node, user_function)(*args, **kwargs)
        elif mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            try:
                return self._run_pandas_function(user_function, args, kwargs)
            except Exception as e:
                raise UDF_ERROR(e, feature_definition_name=transformation.metadata.name)
        elif mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            try:
                return self._create_and_run_python_udf(user_function, args, kwargs)
            except TypeError as e:
                raise UDF_TYPE_ERROR(e)
            except Exception as e:
                raise UDF_ERROR(e, feature_definition_name=transformation.metadata.name)
        else:
            msg = f"Unknown transformation mode({transformation.transformation_mode})"
            raise KeyError(msg)

    def _run_pandas_function(
        self,
        user_function: Callable,
        args: List[Any],
        kwargs: Dict[str, Any],
    ) -> PySparkDataFrame:
        # Assumes that we only have one argument that is a pyspark Dataframe built from the batch source
        # because this code path is for ingest api which should only read from one batch source.
        assert len(args) + len(kwargs) == 1, "Pandas transformations only support a single input"
        input_df = args[0] if len(args) == 1 else next(iter(kwargs.values()))

        output_pandas_df = user_function(input_df.toPandas())
        return pandas_to_spark(self._spark, output_pandas_df)

    def _create_and_run_python_udf(
        self, user_function: Callable, args: List[Any], kwargs: Dict[str, Any]
    ) -> pandas.DataFrame:
        from pyspark.sql.functions import struct
        from pyspark.sql.functions import udf

        # Assumes that we only have one argument that is a pyspark Dataframe built from the batch source
        # because this code path is for ingest api which should only read from one batch source.
        assert len(args) + len(kwargs) == 1, "Pandas transformations only support a single input"
        df = args[0] if len(args) == 1 else next(iter(kwargs.values()))

        @udf(self._output_schema)
        def transform_rows(row_as_struct):
            # Apply your desired transformation on the input group of Rows(this applies row by row)
            transformed_df_group = user_function(row_as_struct.asDict())

            # Return the transformed group of rows as a Pandas DataFrame
            return transformed_df_group

        df = df.select(struct("*").alias("data"))
        df = df.select(transform_rows("data").alias("result"))
        res = df.select(*[f"result.{field.name}" for field in self._output_schema])
        return res

    def _build_spark_sql_function(
        self, transformation_node: TransformationNode, user_function: Callable[..., str]
    ) -> Callable[..., PySparkDataFrame]:
        """
        Returns a function that takes args/kwargs and appropriately passes it as arguments
        to a formatted SQL string.
        """

        def wrapped(*args, **kwargs):
            wrapped_args = []
            for input_value, input_proto in zip(args, positional_inputs(transformation_node)):
                # Replace Dataframe arguments with temp table name
                if is_pyspark_df(input_value):
                    input_value = self._register_temp_table(input_proto.node, input_value)
                wrapped_args.append(input_value)

            keyword_inputs = get_keyword_inputs(transformation_node)
            wrapped_kwargs = {}
            for k, input_value in kwargs.items():
                input_proto = keyword_inputs[k]
                # Replace Dataframe arguments with temp table name
                if is_pyspark_df(input_value):
                    input_value = self._register_temp_table(input_proto.node, input_value)
                wrapped_kwargs[k] = input_value

            sql_string = user_function(*wrapped_args, **wrapped_kwargs)

            transformation_name = self.get_transformation_by_id(transformation_node.transformation_id).name
            check_transformation_type(transformation_name, sql_string, "spark_sql", self._VALID_MODES)
            return self._spark.sql(sql_string)

        return wrapped

    def _register_temp_table(self, node: PipelineNode, df: PySparkDataFrame) -> str:
        """
        Registers a Dataframe as a temp table and returns its generated name.
        Only applicable for Transformation and DataSource Nodes
        """
        if node.HasField("transformation_node"):
            transformation_name = self.get_transformation_by_id(node.transformation_node.transformation_id).name
            name = f"transformation_{transformation_name}_output"
        elif node.HasField("data_source_node"):
            name = node.data_source_node.input_name
        else:
            msg = f"Expected transformation or data source node: {node}"
            raise Exception(msg)

        random_suffix = "".join(random.choice(string.ascii_letters) for i in range(6))
        unique_name = name + random_suffix

        self._registered_temp_view_names.append(unique_name)
        df.createOrReplaceTempView(unique_name)

        return unique_name

    def _cleanup_temp_tables(self):
        # Cleanup any temporary tables created during the process
        for temp_name in self._registered_temp_view_names:
            # DROP VIEW/DROP TABLE sql syntax is invalidated when spark_catalog is set to DeltaCatalog on EMR clusters
            if (
                self._spark.conf.get("spark.sql.catalog.spark_catalog", "")
                == "org.apache.spark.sql.delta.catalog.DeltaCatalog"
            ):
                self._spark.catalog.dropTempView(temp_name)
            else:
                self._spark.sql(f"DROP VIEW IF EXISTS {temp_name}")

import re
import sys
import typing
from dataclasses import dataclass
from textwrap import dedent
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas

import tecton_core.tecton_pendulum as pendulum
from tecton_core import specs
from tecton_core.data_types import ArrayType
from tecton_core.data_types import BoolType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.errors import UDF_ERROR
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonSnowflakeNotImplementedError
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import MaterializationContext
from tecton_core.pipeline.pipeline_common import CONSTANT_TYPE
from tecton_core.pipeline.pipeline_common import CONSTANT_TYPE_OBJECTS
from tecton_core.pipeline.pipeline_common import check_transformation_type
from tecton_core.pipeline.pipeline_common import constant_node_to_value
from tecton_core.pipeline.pipeline_common import get_keyword_inputs
from tecton_core.pipeline.pipeline_common import get_time_window_from_data_source_node
from tecton_core.pipeline.pipeline_common import positional_inputs
from tecton_proto.args.pipeline__client_pb2 import DataSourceNode
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.args.transformation__client_pb2 import TransformationArgs
from tecton_proto.args.transformation__client_pb2 import TransformationMode
from tecton_proto.common.data_source_type__client_pb2 import DataSourceType
from tecton_proto.data.transformation__client_pb2 import Transformation
from tecton_snowflake.templates_utils import load_template
from tecton_snowflake.utils import format_sql
from tecton_snowflake.utils import generate_random_name


if typing.TYPE_CHECKING:
    import snowflake.snowpark


PIPELINE_TEMPLATE = load_template("transformation_pipeline.sql")
TIME_LIMIT_TEMPLATE = load_template("time_limit.sql")
DATA_SOURCE_TEMPLATE = load_template("data_source.sql")
TEMP_CTE_PREFIX = "_TT_CTE_"
TEMP_DS_PREFIX = "_TT_DS_"
SPINE_TABLE_NAME = "_TT_SPINE_TABLE"
UDF_OUTPUT_COLUMN_NAME = "_TT_UDF_OUTPUT"
TEMP_PIPELINE_VIEW_NAME = "_TEMP_PIPELINE_VIEW_FROM_DF"
TRANSFORMATION_INPUT_PARAMETER = "transformation_input"
TRANSFORMATION_COLUMN_PREFIX = "_UDF_INTERNAL_TRANSFORMATION__"

SEPERATOR = "__"

SPARK_TO_SNOWFLAKE_TYPES = {
    Int64Type(): "NUMBER",
    Float64Type(): "FLOAT",
    StringType(): "STRING",
    BoolType(): "BOOLEAN",
    ArrayType(Int64Type()): "ARRAY",
    ArrayType(Float32Type()): "ARRAY",
    ArrayType(Float64Type()): "ARRAY",
    ArrayType(StringType()): "ARRAY",
}


# TODO(deprecate_after=0.7): Snowpark mode transformations are not supported in versions <=0.8. We should switch to only using PipelineSqlBuilder in the future
def pipeline_to_sql_string(
    pipeline: Pipeline,
    data_sources: List[specs.DataSourceSpec],
    transformations: List[specs.TransformationSpec],
    materialization_context: MaterializationContext,
    mock_sql_inputs: Optional[Dict[str, str]] = None,
    session: "snowflake.snowpark.Session" = None,
) -> str:
    """This method is deprecated!

    Do not use if not necessary. Instead, use PipelineSqlBuilder."""
    return format_sql(
        _PipelineBuilder(
            pipeline=pipeline,
            data_sources=data_sources,
            transformations=transformations,
            mock_sql_inputs=mock_sql_inputs,
            materialization_context=materialization_context,
            session=session,
        ).get_sql_string()
    )


# Pandas Pipeline (ODFV)
# input_df (snowpark df) is the spine passed in by the user (including request context),
# and it has been augmented with dependent fv fields in of the form "_udf_internal_{input_name}.{feature_field_name}".
# The dataframe we return will be everything from the spine, with the on-demand features added
# TODO: Figure out a way to get the dependent fv fields on tecton apply, this way we can
#      register the udf on apply and avoid doing it adhoc on feature retrival.
def pipeline_to_df_with_input(
    session: "snowflake.snowpark.Session",
    # This should have data from all inputs
    input_df: "snowflake.snowpark.DataFrame",
    pipeline: Pipeline,
    transformations: List[specs.TransformationSpec],
    output_schema: Dict[str, DataType],
    name: str,
    fv_id: str,
    namespace: str,
    append_prefix: bool,
) -> "snowflake.snowpark.DataFrame":
    # TODO: Currently there's a bug in toPandas() call, types may not be casted to the correct type.
    # e.g. Long is currently being casted to object(decimal.Decimal) instead of int64.
    return _ODFVPipelineBuilder(
        session=session,
        input_df=input_df,
        output_schema=output_schema,
        name=name,
        namespace=namespace,
        pipeline=pipeline,
        transformations=transformations,
        fv_id=fv_id,
        append_prefix=append_prefix,
    ).get_df()


# Used for j2 template
@dataclass
class _NodeInput:
    name: str
    sql_str: str


def has_snowpark_transformation(transformations: List[specs.TransformationSpec]) -> bool:
    for transformation in transformations:
        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_SNOWPARK:
            return True
    return False


def has_push_source(data_sources: List[specs.DataSourceSpec]) -> bool:
    for data_source in data_sources:
        if data_source.type in (DataSourceType.PUSH_NO_BATCH, DataSourceType.PUSH_WITH_BATCH):
            return True
    return False


# TODO(deprecate_after=0.7): Snowpark mode transformations are not supported in versions <=0.8. We should switch to only using PipelineSqlBuilder in the future
class _PipelineBuilder:
    """
    This class is for Snowflake Pipelines with snowpark transformations.

    WARNING: This class is deprecated! PipelineSqlBuilder should be used instead.
    """

    # The value of internal nodes in the tree
    _VALUE_TYPE = Union[str, CONSTANT_TYPE, MaterializationContext, "snowflake.snowpark.DataFrame"]

    def __init__(
        self,
        pipeline: Pipeline,
        data_sources: List[specs.DataSourceSpec],
        # we only use mode and name from these
        transformations: Union[List[Transformation], List[TransformationArgs]],
        mock_sql_inputs: Optional[Dict[str, str]],
        materialization_context: MaterializationContext,
        session: Optional["snowflake.snowpark.Session"],
    ):
        self._pipeline = pipeline
        self._id_to_ds = {ds.id: ds for ds in data_sources}
        self._id_to_transformation = {t.id: t for t in transformations}
        self._mock_sql_inputs = mock_sql_inputs
        self._materialization_context = materialization_context
        self._has_snowpark = has_snowpark_transformation(transformations)
        self._session = session
        self._ds_to_sql_str = {}
        if self._has_snowpark:
            assert self._session is not None

    def get_sql_string(self) -> str:
        if self._has_snowpark:
            df = self._node_to_value(self._pipeline.root)
            temp_pipeline_view_name = generate_random_name()
            df.create_or_replace_temp_view(temp_pipeline_view_name)
            row = self._session.sql(f"SELECT GET_DDL('VIEW', '{temp_pipeline_view_name}') AS SQL").collect(
                statement_params={"SF_PARTNER": "tecton-ai"}
            )[0]
            generated_sql = row.as_dict()["SQL"]
            # The generated sql query will be something like:
            #
            # create or replace view TEST_VIEW(
            # 	USER_ID,
            # 	USER_HAS_GOOD_CREDIT,
            # 	TIMESTAMP
            # ) as  SELECT  *  FROM (
            #   xxx
            #   xxx
            #   xxx);
            # Remove the "create or replace view XXX as" part
            m = re.search(f"create or replace view {temp_pipeline_view_name}\([^()]*\) as ((?s:.)*);", generated_sql)
            if m:
                view_sql = m.group(1)
            else:
                msg = f"Couldn't extract from generated sql query: {generated_sql}"
                raise TectonInternalError(msg)
            self._session.sql(f"DROP VIEW IF EXISTS {temp_pipeline_view_name}")
            return view_sql
        else:
            sql_str = self._node_to_value(self._pipeline.root)
            assert isinstance(sql_str, str)
            sql_str = DATA_SOURCE_TEMPLATE.render(data_sources=self._ds_to_sql_str, source=sql_str)
            return sql_str

    def _node_to_value(self, pipeline_node: PipelineNode) -> _VALUE_TYPE:
        if pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_value(pipeline_node.transformation_node)
        elif pipeline_node.HasField("data_source_node"):
            return self._data_source_node_to_value(pipeline_node.data_source_node)
        elif pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("materialization_context_node"):
            return self._materialization_context
        elif pipeline_node.HasField("request_data_source_node"):
            msg = "RequestDataSource is not supported in Snowflake SQL pipelines"
            raise TectonSnowflakeNotImplementedError(msg)
        elif pipeline_node.HasField("feature_view_node"):
            msg = "Dependent FeatureViews are not supported in Snowflake SQL pipelines"
            raise TectonSnowflakeNotImplementedError(msg)
        else:
            msg = f"Unknown PipelineNode type: {pipeline_node}"
            raise KeyError(msg)

    def _data_source_node_to_value(
        self, data_source_node: DataSourceNode
    ) -> Union[str, "snowflake.snowpark.DataFrame"]:
        """Creates a sql string from a ds and time parameters."""
        sql_str = ""
        if self._mock_sql_inputs is not None and data_source_node.input_name in self._mock_sql_inputs:
            sql_str = self._mock_sql_inputs[data_source_node.input_name]
        else:
            time_window = get_time_window_from_data_source_node(
                feature_time_limits=pendulum.Period(
                    self._materialization_context.start_time, self._materialization_context.end_time
                ),
                schedule_interval=self._materialization_context.batch_schedule,
                data_source_node=data_source_node,
            )
            ds = self._id_to_ds[IdHelper.to_string(data_source_node.virtual_data_source_id)]
            sql_str = self._get_ds_sql_str(ds, time_window)

        cte_name = f"{TEMP_DS_PREFIX}_{generate_random_name()}"
        self._ds_to_sql_str[cte_name] = sql_str
        if self._has_snowpark:
            return self._session.sql(sql_str)
        else:
            return cte_name

    def _get_ds_sql_str(self, ds: specs.DataSourceSpec, time_window: Optional[pendulum.Period]) -> str:
        if not ds.batch_source:
            msg = "Snowflake SQL pipeline only supports batch data source"
            raise TectonSnowflakeNotImplementedError(msg)
        if not isinstance(ds.batch_source, specs.SnowflakeSourceSpec):
            msg = f"Snowflake SQL pipeline does not support batch data source: {ds.batch_source}"
            raise TectonSnowflakeNotImplementedError(msg)

        snowflake_source = ds.batch_source

        if snowflake_source.table:
            if snowflake_source.query:
                msg = "Only one of table and query can be specified"
                raise TectonInternalError(msg)
            # Makes sure we have all the info for the table
            assert snowflake_source.database
            assert snowflake_source.schema
            sql_str = f"{snowflake_source.database}.{snowflake_source.schema}.{snowflake_source.table}"
        elif snowflake_source.query:
            sql_str = snowflake_source.query
        else:
            msg = "Either table or query must be specified for Snowflake data source"
            raise TectonInternalError(msg)

        if time_window is None:
            return f"SELECT * FROM ({sql_str})"

        # If we have a time window, we need to filter the source based on it
        if not snowflake_source.timestamp_field:
            msg = f"timestamp_field must be set within Snowflake data source '{ds.name}' to use time filtering in this feature view."
            raise TectonInternalError(msg)
        return TIME_LIMIT_TEMPLATE.render(
            source=sql_str,
            timestamp_key=snowflake_source.timestamp_field,
            start_time=time_window.start,
            end_time=time_window.end,
        )

    def _transformation_node_to_value(
        self, transformation_node: TransformationNode
    ) -> Union[str, "snowflake.snowpark.DataFrame"]:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args = []
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
        self, transformation_node, args, kwargs
    ) -> Union[str, "snowflake.snowpark.DataFrame"]:
        """For the given transformation node, returns the corresponding sql string or dataframe."""
        transformation = self._id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL:
            return self._wrap_sql_function(transformation_node, user_function)(*args, **kwargs)
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_SNOWPARK:
            res = user_function(*args, **kwargs)
            check_transformation_type(transformation.name, res, "snowpark", self._possible_modes())
            return res
        else:
            msg = f"Invalid transformation mode: {TransformationMode.Name(transformation.transformation_mode)} for a Snowflake SQL pipeline"
            raise KeyError(msg)

    def _wrap_sql_function(
        self, transformation_node: TransformationNode, user_function: Callable[..., str]
    ) -> Callable[..., str]:
        def wrapped(*args, **kwargs):
            transformationInputs = []
            wrapped_args = []
            for arg, node_input in zip(args, positional_inputs(transformation_node)):
                input_str, is_sql = self._wrap_node_inputvalue(node_input, arg)
                cte_name = TEMP_CTE_PREFIX + generate_random_name()
                if is_sql:
                    wrapped_args.append(cte_name)
                    transformationInputs.append(_NodeInput(name=cte_name, sql_str=input_str))
                else:
                    wrapped_args.append(input_str)
            keyword_inputs = get_keyword_inputs(transformation_node)
            wrapped_kwargs = {}
            for k, v in kwargs.items():
                node_input = keyword_inputs[k]
                input_str, is_sql = self._wrap_node_inputvalue(node_input, v)
                if is_sql:
                    cte_name = TEMP_CTE_PREFIX + k
                    wrapped_kwargs[k] = cte_name
                    transformationInputs.append(_NodeInput(name=cte_name, sql_str=input_str))
                else:
                    wrapped_kwargs[k] = input_str
            user_function_sql = dedent(user_function(*wrapped_args, **wrapped_kwargs))
            sql_str = PIPELINE_TEMPLATE.render(inputs=transformationInputs, user_function=user_function_sql)
            transformation_name = self._id_to_transformation[
                IdHelper.to_string(transformation_node.transformation_id)
            ].name
            check_transformation_type(transformation_name, sql_str, "snowflake_sql", self._possible_modes())
            return sql_str

        return wrapped

    def _wrap_node_inputvalue(self, node_input, value: _VALUE_TYPE) -> Tuple[Union[CONSTANT_TYPE], bool]:
        """Returns the node value, along with a boolean indicating whether the input is a sql str."""
        if node_input.node.HasField("constant_node"):
            assert value is None or isinstance(value, CONSTANT_TYPE_OBJECTS)
            return value, False
        elif node_input.node.HasField("data_source_node"):
            # For data source we don't want a bracket around it
            assert isinstance(value, str)
            return value, False
        elif node_input.node.HasField("materialization_context_node"):
            assert isinstance(value, MaterializationContext)
            return value, False
        else:
            # This should be a sql string already, we need to return this with a bracket wrapping it
            # The current implementation will add a round bracket () to all subquery
            assert isinstance(value, str)
            return f"({value})", True

    def _possible_modes(self):
        return ["snowflake_sql", "pipeline", "snowpark"]


# This class is for Pandas pipelines
class _ODFVPipelineBuilder:
    def __init__(
        self,
        session: "snowflake.snowpark.Session",
        name: str,
        namespace: str,
        transformations: List[specs.TransformationSpec],
        output_schema: Dict[str, DataType],
        pipeline: Pipeline,
        fv_id: str,
        input_df: "snowflake.snowpark.DataFrame" = None,
        append_prefix: bool = True,
    ):
        self._input_df = input_df
        self._session = session
        self._pipeline = pipeline
        self._name = name
        self._namespace = namespace
        self._fv_id = fv_id
        self._id_to_transformation = {t.id: t for t in transformations}
        self._output_schema = output_schema
        self._append_prefix = append_prefix

    def get_df(self) -> "snowflake.snowpark.DataFrame":
        if not self._pipeline.root.HasField("transformation_node"):
            msg = "Root pipeline has to be a transformation for pandas mode"
            raise ValueError(msg)
        output_df, _ = self._transformation_node_to_df(
            self._pipeline.root.transformation_node, is_top_level_transformation=True
        )
        return output_df

    def _transformation_node_to_df(
        self, transformation_node: TransformationNode, is_top_level_transformation: bool = False
    ) -> ("snowflake.snowpark.DataFrame", list):
        """
        Run pipeline on transformation node
        :param transformation_node: input transformation node
        :param is_top_level_transformation: whether the transformation node is the root node of the pipeline
        :return: 1. A snowpark DataFrame with the results from the transformation
                2. The list of the column names of this DataFrame.
                (We return them specifically since Snowflake will automatically capitalize them in a way the code does not expect.
        """
        # Columns in snowflake dataframe have double quotes around them.
        udf_args = [c.strip('"') for c in self._input_df.columns if ("_UDF_INTERNAL" in c)]

        # The following parameters are used to generate the UDF snowflake calls.
        input_columns = []  # Columns on the input dataframe that are used as inputs to the transformation.
        input_map = {}  # Maps parameter names to relevant featuere columns/keys.
        prefix_map = {}  # Maps parameter names to the prefix used on their dependent features.
        input_df = self._input_df  # The DataFrame to be passed to the UDF

        # Input for On-Demand can only be a feature view, request data source, or transformation
        for transformation_input in transformation_node.inputs:
            input_node = transformation_input.node
            if input_node.HasField("feature_view_node"):
                features = []
                feature_view_node = input_node.feature_view_node
                prefix = f"_UDF_INTERNAL_{feature_view_node.input_name}_{self._fv_id}__".upper()
                for feature in udf_args:
                    if not feature.startswith(prefix):
                        continue
                    input_columns.append(feature)
                    features.append(feature)
                input_map[feature_view_node.input_name] = features
                prefix_map[feature_view_node.input_name] = prefix
            elif input_node.HasField("request_data_source_node"):
                request_data_source_node = input_node.request_data_source_node
                field_names = [field.name for field in request_data_source_node.request_context.tecton_schema.columns]
                for input_col in field_names:
                    input_columns.append(input_col)
                input_map[request_data_source_node.input_name] = field_names
                prefix_map[request_data_source_node.input_name] = ""
                # Request context should be in the input_df already
            elif input_node.HasField("transformation_node"):
                # TODO: https://tecton.atlassian.net/browse/TEC-11231
                assert (
                    len(transformation_node.inputs) == 1
                ), "Snowflake currently only supports a single transformation as the input to another transformation"
                # overwrite the input df to be the output of the nested transformation
                input_df, result_columns = self._transformation_node_to_df(input_node.transformation_node)
                prefix = TRANSFORMATION_COLUMN_PREFIX
                features = []
                for feature in result_columns:
                    if not feature.startswith(prefix):
                        continue
                    input_columns.append(feature)
                    features.append(feature)
                # We don't know the param name for nested transformations so we set a placeholder name.
                input_map[TRANSFORMATION_INPUT_PARAMETER] = features
                prefix_map[TRANSFORMATION_INPUT_PARAMETER] = prefix
            else:
                msg = "Snowflake only supports feature view and request data source as input."
                raise TectonSnowflakeNotImplementedError(msg)
        # Get back the name of the UDF
        ondemand_udf = self._generate_on_demand_udf(transformation_node, input_map, prefix_map, input_columns)
        # Call the udf and return the output dataframe and columns for this dataframe.
        # We return the columns explicitly since snowflake will auto capitalize them which causes some issues.
        return self._call_udf(ondemand_udf, input_columns, input_df, is_top_level_transformation)

    def _get_dict_keys_from_udf_output(self, output_df: "snowflake.snowpark.DataFrame"):
        from snowflake.snowpark.functions import object_keys

        # Compute the keys from the udf output dict, since we do not know the output schema of the nested transformation.
        # When converting snowpark -> pandas there's some weird formatting we strip out.
        udf_column_names_df = output_df.withColumn(
            "COLUMN_NAMES", object_keys(UDF_OUTPUT_COLUMN_NAME).cast("ARRAY")
        ).limit(1)
        udf_column_names_str = str(udf_column_names_df.to_pandas()["COLUMN_NAMES"].iloc[0])[1:-1]
        udf_column_names_list = []
        for i in udf_column_names_str.split(","):
            value = i.strip()
            udf_column_names_list.append(value.strip('"'))
        return udf_column_names_list

    def _call_udf(
        self,
        ondemand_udf: "snowflake.snowpark.udf.UserDefinedFunction",
        input_columns: List[str],
        input_df: "snowflake.snowpark.DataFrame",
        is_top_level_transformation: bool,
    ) -> ("snowflake.snowpark.DataFrame", list):
        from snowflake.snowpark.functions import array_construct
        from snowflake.snowpark.functions import col

        # Call the udf and append the result to the input dataframe.
        try:
            output_df = input_df.withColumn(UDF_OUTPUT_COLUMN_NAME, ondemand_udf(array_construct(*input_columns)))
        except Exception as e:
            raise UDF_ERROR(e)

        # Rename the feature columns to match the output schema.
        # Only do this for the top level transformation in the pipeline.
        if is_top_level_transformation:
            for column in self._output_schema.keys():
                output_df = output_df.withColumn(
                    self._namespace + SEPERATOR + column if self._append_prefix else column,
                    col(UDF_OUTPUT_COLUMN_NAME)[column].cast(SPARK_TO_SNOWFLAKE_TYPES[self._output_schema[column]]),
                )
            columns_to_select = list(input_df.columns) + [
                self._namespace + SEPERATOR + column if self._append_prefix else column
                for column in self._output_schema.keys()
            ]
            return output_df.select(*columns_to_select), columns_to_select

        udf_column_names_list = self._get_dict_keys_from_udf_output(output_df)
        # Rename the output columns with the transformation prefix since this df will be the input to another transformation.
        feature_columns = []
        for feature in udf_column_names_list:
            feature_name = TRANSFORMATION_COLUMN_PREFIX + feature
            feature_columns.append(feature_name)
            output_df = output_df.withColumn(feature_name, col(UDF_OUTPUT_COLUMN_NAME)[feature])
        columns_to_select = input_df.columns + feature_columns
        return output_df.select(*columns_to_select), columns_to_select

    def _generate_on_demand_udf(
        self,
        transformation_node: TransformationNode,
        input_map: Dict[str, List[str]],
        prefix_map: Dict[str, str],
        input_columns: List[str],
    ) -> "snowflake.snowpark.udf.UserDefinedFunction":
        """Returns the name of the registered udf"""
        transformation = self._id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function

        use_pandas = transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS

        def _consume_prefix(s: str, prefix: str) -> str:
            assert s.startswith(prefix), f"{prefix} is not a prefix of {s}"
            return s[len(prefix) :]

        if use_pandas:

            def udf(params: List) -> Dict:
                # This is a requirement from snowflake to track udf
                sys._xoptions["snowflake_partner_attribution"].append("tecton-ai")
                # For udfs that have a data source or feature view as an input, use kwargs.
                # For udfs that have a transformation result as an input, use args.
                kwargs = {}
                args = None
                all_inputs_df = pandas.DataFrame([params], columns=input_columns)
                for input_name, columns in input_map.items():
                    if input_name == TRANSFORMATION_INPUT_PARAMETER:
                        assert args is None, "Only one transformation can be the input to another transformation"
                        df = all_inputs_df[columns]
                        df.columns = df.columns.str[len(prefix_map[input_name]) :]
                        args = df
                    else:
                        df = all_inputs_df[columns]
                        df.columns = df.columns.str[len(prefix_map[input_name]) :]
                        kwargs[input_name] = df

                # Pandas will complain if you use args != None due to how they implement the truth value of a dataframe.
                if not isinstance(args, type(None)):
                    result = user_function(args)
                else:
                    result = user_function(**kwargs)

                result_df = result.astype("object")
                return {col: result_df[col][0] for col in result_df.columns}

        else:

            def udf(params: List) -> Dict:
                sys._xoptions["snowflake_partner_attribution"].append("tecton-ai")
                # For udfs that have a data source or feature view as an input, use kwargs.
                # For udfs that have a transformation result as an input, use args.
                kwargs = {}
                args = None
                all_inputs = dict(zip(input_columns, params))
                for input_name, columns in input_map.items():
                    if input_name == TRANSFORMATION_INPUT_PARAMETER:
                        assert args is None, "Only one transformation can be the input to another transformation"
                        args = {
                            _consume_prefix(column, prefix_map[input_name]): all_inputs[column] for column in columns
                        }
                    else:
                        kwargs[input_name] = {
                            _consume_prefix(column, prefix_map[input_name]): all_inputs[column] for column in columns
                        }
                if args is not None:
                    return user_function(args)

                return user_function(**kwargs)

        if use_pandas:
            # Make sure to update the pandas version in python/requirements.in as well to keep it in sync.
            self._session.add_packages("pandas==1.3.5")
        return self._session.udf.register(udf, replace=True)

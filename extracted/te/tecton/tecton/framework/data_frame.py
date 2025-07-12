import contextlib
import logging
import time
import typing
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import numpy
import pandas
import pyarrow
import pyspark
import pytz
from packaging import version
from pandas.core.dtypes.common import is_datetime64_any_dtype
from pandas.core.dtypes.common import is_datetime64tz_dtype

import tecton_core.query.dialect
import tecton_core.tecton_pendulum as pendulum
from tecton._internals import errors
from tecton._internals import materialization_api
from tecton._internals.model_artifact_provider import MDSModelArtifactProvider
from tecton._internals.offline_store_credentials import INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS
from tecton._internals.sdk_decorators import sdk_public_method
from tecton._internals.secret_resolver import LocalDevSecretResolver
from tecton.framework import configs
from tecton.snowflake_context import SnowflakeContext
from tecton_athena import athena_session
from tecton_athena.data_catalog_helper import register_feature_view_as_athena_table_if_necessary
from tecton_athena.query.translate import AthenaSqlExecutor
from tecton_athena.query.translate import athena_convert
from tecton_core import conf
from tecton_core import data_types
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import offline_retrieval_compute_mode
from tecton_core.data_processing_utils import merge_validity_periods
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.pandas_compat import pandas_to_spark
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import recurse_query_tree
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_staging_nodes
from tecton_core.query.node_utils import tree_contains
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.query.rewrite import rewrite_tree_for_spine
from tecton_core.schema import Schema
from tecton_core.schema_validation import arrow_schema_to_tecton_schema
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_core.spark_type_annotations import PySparkSession
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_core.time_utils import convert_pandas_df_for_snowflake_upload
from tecton_spark import schema_spark_utils
from tecton_spark.query import translate


logger = logging.getLogger(__name__)

_internal_index_column = "_tecton_internal_index_col"


def convert_pandas_timestamps_from_spark(pandas_df) -> pandas.DataFrame:
    """Match pandas timezone to that of Spark, s.t. the timestamps are correctly displayed."""
    from tecton.tecton_context import TectonContext

    tz = TectonContext.get_instance()._spark.conf.get("spark.sql.session.timeZone")
    for col in pandas_df.columns:
        if pandas.core.dtypes.common.is_datetime64_dtype(pandas_df[col]):
            pandas_df[col] = pandas_df[col].dt.tz_localize(pytz.timezone(tz))
            pandas_df[col] = pandas_df[col].dt.tz_convert(pytz.timezone("UTC"))
            if conf.TECTON_STRIP_TIMEZONE_FROM_FEATURE_VALUES_FF.enabled():
                pandas_df[col] = pandas_df[col].dt.tz_localize(None)
    # TODO: We're editing the df in place, but returning the same object. This would be less confusing if we picked
    #  one or the other
    return pandas_df


def _remove_timezones(df: pandas.DataFrame) -> pandas.DataFrame:
    for col in df.columns:
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    return df


@attrs.define(auto_attribs=True)
class FeatureVector(object):
    """
    A FeatureVector is a representation of a single feature vector. Usage of a FeatureVector typically involves
    extracting the feature vector using ``to_pandas()``, ``to_dict()``, or ``to_numpy()``.
    """

    _names: List[str]
    _values: List[Union[int, str, bytes, float, list]]
    _effective_times: List[Optional[datetime]]
    slo_info: Optional[Dict[str, str]] = None

    @sdk_public_method
    def to_dict(
        self, return_effective_times: bool = False
    ) -> Dict[str, Union[int, str, bytes, float, list, dict, None]]:
        """Turns vector into a Python dict.

        :param return_effective_times: Whether to return the effective time of the feature.

        :return: A Python dict.
        """
        if return_effective_times:
            return {
                name: {"value": self._values[i], "effective_time": self._effective_times[i]}
                for i, name in enumerate(self._names)
            }

        return dict(zip(self._names, self._values))

    @sdk_public_method
    def to_pandas(self, return_effective_times: bool = False) -> pandas.DataFrame:
        """Turns vector into a Pandas DataFrame.

        :param return_effective_times: Whether to return the effective time of the feature as part of the DataFrame.

        :return: A Pandas DataFrame.
        """
        if return_effective_times:
            return pandas.DataFrame(
                list(zip(self._names, self._values, self._effective_times)), columns=["name", "value", "effective_time"]
            )

        return pandas.DataFrame([self._values], columns=self._names)

    @sdk_public_method
    def to_numpy(self, return_effective_times: bool = False) -> numpy.array:
        """Turns vector into a numpy array.

        :param return_effective_times: Whether to return the effective time of the feature as part of the list.

        :return: A numpy array.
        """
        if return_effective_times:
            return numpy.array([self._values, self._effective_times])

        return numpy.array(self._values)

    def _update(self, other: "FeatureVector"):
        self._names.extend(other._names)
        self._values.extend(other._values)
        self._effective_times.extend(other._effective_times)


@attrs.define(repr=False)
class TectonDataFrame(DataframeWrapper):
    """
    A thin wrapper around Pandas, Spark dataframes.
    """

    _spark_df: Optional[PySparkDataFrame] = None
    _pandas_df: Optional[pandas.DataFrame] = None
    _arrow_table: Optional[pyarrow.Table] = None
    # This should not be accessed directly. use _querytree instead.
    _querytree_do_not_use: Optional[NodeRef] = attrs.field(default=None, repr=lambda x: "TectonQueryTree")

    _need_rewrite_tree: bool = False

    # _schema is the schema of TectonDataFrame. It is present only if the TectonDataFrame is built from a pandas
    # dataframe as a spine and it is used when converting a pandas datafarme to a spark dataframe. Note the _schema only
    # contains the name and data type for those columns Tecton manages. If the spine contains extra columns like `label`
    # etc, those columns are converted to their default spark data types.
    _schema: Optional[Schema] = None

    # This is the params that are passed to get_features_for_events or get_features_in_range.
    _request_params: Optional[Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams]] = None

    _children_dfs: Optional[List["TectonDataFrame"]] = None

    @property
    def _querytree(self):
        if self._need_rewrite_tree:
            rewrite_tree_for_spine(self._querytree_do_not_use)
            self._need_rewrite_tree = False
        return self._querytree_do_not_use

    @sdk_public_method
    def start_dataset_job(
        self,
        dataset_name: str,
        cluster_config: Optional[configs.ComputeConfigTypes] = None,
        tecton_materialization_runtime: Optional[str] = None,
        environment: Optional[str] = None,
        extra_config: Optional[Dict[str, Any]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        job_retry_times: Optional[int] = None,
    ) -> "materialization_api.DatasetJob":
        """
        Start a job to materialize a dataset from this TectonDataFrame.

        :param dataset_name: Dataset object will be created with this name.
                Dataset can be later retrieved by this name,
                hence it must be unique within the workspace.
        :param cluster_config: Configuration for Spark/Rift cluster
        :param tecton_materialization_runtime: Version of `tecton` package used by the job cluster
        :param environment: The custom environment in which jobs will be run
        :param extra_config: Additional parameters (the list may vary depending on
                the tecton runtime) which may be used to tune remote execution heuristics
                (ie, what number to use when chunking the events dataframe)
        :param compute_mode: Override compute mode used in `get_features` call
        :param job_retry_times: Max retry times of the job. If not specified, use the default Remote
                Dateset Job retry times.
        :return: DatasetJob object
        """
        if conf.DUCKDB_ENABLE_SPINE_SPLIT_FF.enabled():
            msg = (
                "Spine splitting can't be used together with remote dataset generation. "
                "Set DUCKDB_ENABLE_SPINE_SPLIT to 'False'"
            )
            raise TectonValidationError(msg)

        assert self._request_params, (
            "TectonDataFrame must be created by calling get_features_in_range or get_features_for_events "
            "on MaterializedFeatureView or FeatureService object to use this method"
        )

        fco: Union[specs.FeatureViewSpec, specs.FeatureServiceSpec] = (
            self._request_params.fco.fv_spec
            if isinstance(self._request_params.fco, FeatureDefinitionWrapper)
            else self._request_params.fco
        )

        if self._request_params.mock_data_sources:
            msg = "Mocking data sources is currently unsupported in remote dataset generation"
            raise TectonValidationError(msg)

        input_ = materialization_api.retrieval_params_to_job_input(self._request_params, fco)
        compute_mode = (
            offline_retrieval_compute_mode(compute_mode) if compute_mode else self._request_params.compute_mode
        )
        if isinstance(fco, specs.FeatureServiceSpec) and compute_mode == ComputeMode.RIFT and not environment:
            msg = "`environment` parameter must be provided when dataset job is run for a feature service"
            raise TectonValidationError(msg)

        # using querytree before rewrite to avoid triggering Spark
        # (we assume that users are calling this API because that don't want to run Spark locally)
        output_schema = self._querytree_do_not_use.output_schema

        return materialization_api.start_dataset_job(
            fco=fco,
            input_=input_,
            dataset=dataset_name,
            output_schema=output_schema,
            compute_mode=compute_mode.to_batch_compute(),
            from_source=self._request_params.from_source,
            cluster_config=cluster_config._to_cluster_proto() if cluster_config else None,
            tecton_materialization_runtime=tecton_materialization_runtime,
            environment=environment,
            extra_config=extra_config,
            job_retry_times=job_retry_times,
        )

    @sdk_public_method
    def explain(
        self,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
        columns: bool = False,
    ):
        """Prints the query tree. Should only be used when this TectonDataFrame is backed by a query tree.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
            columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        if self._querytree:
            if not name and not description:
                msg = "At least one of 'name' or 'description' must be True."
                raise RuntimeError(msg)
            if columns and not node_id:
                msg = "Can only show columns if 'node_id' is True."
                raise RuntimeError(msg)
            print(self._querytree.pretty_str(node_id=node_id, name=name, description=description, columns=columns))
        else:
            print("Explain is only available for TectonDataFrames backed by a query tree.")

    @sdk_public_method
    def to_spark(self) -> PySparkDataFrame:
        """Returns data as a Spark DataFrame.

        :return: A Spark DataFrame.
        """
        if self._spark_df is not None:
            return self._spark_df
        else:
            from tecton.tecton_context import TectonContext

            tc = TectonContext.get_instance()
            if self._querytree is not None:
                return self._to_spark(tc._spark)
            elif self._pandas_df is not None:
                if self._schema is not None:
                    extra_columns = list(set(self._pandas_df.columns) - set(self._schema.column_names()))
                    if len(extra_columns) == 0:
                        pdf = self._pandas_df[self._schema.column_names()]
                        return pandas_to_spark(tc._spark, pdf, schema=schema_spark_utils.schema_to_spark(self._schema))
                    else:
                        # If there are extra columns beyond Tecton's management sopce, it splits the spine into two
                        # parts:
                        #   1. sub_df_1, which contains Tecton managed columns, is built with explicit schema.
                        #   2. sub_df_2, which contains those extra columns, is built with spark default schema(no
                        #      explicit schema passed in.
                        # Eventually these two parts are joined together using an internal index column, which is
                        # dropped afterwards. Note the join operation isn't expensive here given it is backed by a
                        # pandas dataframe that is already loaded into memory.
                        pdf = self._pandas_df.rename_axis(_internal_index_column).reset_index()
                        pdf_schema = self._schema + Schema.from_dict({_internal_index_column: data_types.Int64Type()})
                        sub_df_1 = pandas_to_spark(
                            tc._spark,
                            pdf[pdf_schema.column_names()],
                            schema=schema_spark_utils.schema_to_spark(pdf_schema),
                        )
                        sub_df_2 = pandas_to_spark(tc._spark, pdf[[_internal_index_column, *extra_columns]])
                        return sub_df_1.join(sub_df_2, on=_internal_index_column).drop(_internal_index_column)
                else:
                    return pandas_to_spark(tc._spark, self._pandas_df)
            else:
                raise NotImplementedError

    @staticmethod
    def _spark_to_pandas_wrapped(spark_df: PySparkDataFrame) -> pandas.DataFrame:
        try:
            return spark_df.toPandas()
        except TypeError as e:
            if "Casting to unit-less dtype 'datetime64' is not supported" in str(e):
                pyspark_version = version.parse(pyspark.__version__)
                pandas_version = version.parse(pandas.__version__)

                if pyspark_version < version.parse("3.5.0") and pandas_version >= version.parse("2.0.0"):
                    msg = (
                        f"Caught PySpark error converting dataframe toPandas: `{str(e)}`. "
                        f"This error is known to occur with PySpark versions below 3.5 and Pandas 2.0 or higher. "
                        f"Current versions - PySpark: {pyspark.__version__}, Pandas: {pandas.__version__}. "
                        f"To resolve, set Spark config `spark.sql.execution.arrow.pyspark.enabled=true` "
                        f"or see more information here: https://docs.tecton.ai/docs/beta/tips-and-tricks/troubleshooting/conversion-from-pyspark-dataframe-to-pandas-dataframe-with-pandas-2-0"
                    )
                    raise TypeError(msg)
                else:
                    # If versions don't match the known issue, re-raise the original error
                    raise e
            else:
                raise e

    @sdk_public_method
    def to_pandas(self, pretty_sql: bool = False) -> pandas.DataFrame:
        """
        Convert TectonDataFrame to Pandas DataFrame

        :param pretty_sql: Not applicable when using spark. For Snowflake and Athena, to_pandas() will generate a SQL string, execute it, and then return the resulting data in a pandas DataFrame.
            If True, the sql will be reformatted and executed as a more readable,
            multiline string. If False, the SQL will be executed as a one line string. Use pretty_sql=False for better performance.
        :return: A Pandas DataFrame.
        """
        if self._children_dfs is not None:
            if isinstance(self._request_params, GetFeaturesInRangeParams):
                from tecton_core.query import query_tree_executor

                qt = merge_validity_periods(
                    [df.to_pandas() for df in self._children_dfs],
                    pendulum.Period(self._request_params.start_time, self._request_params.end_time),
                    self._request_params.fco,
                )
                executor = query_tree_executor.QueryTreeExecutor(
                    secret_resolver=LocalDevSecretResolver(),
                    offline_store_options_providers=INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS,
                    model_artifact_provider=MDSModelArtifactProvider(),
                )
                qt_output_df = executor.exec_qt(qt).result_df
                if not conf.TECTON_STRIP_TIMEZONE_FROM_FEATURE_VALUES_FF.enabled():
                    qt_output_df = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(qt_output_df)
                return qt_output_df
            else:
                return pandas.concat([df.to_pandas() for df in self._children_dfs], axis=0)

        if self._pandas_df is not None:
            return self._pandas_df

        assert self._spark_df is not None or self._querytree is not None

        if self._spark_df is not None:
            return convert_pandas_timestamps_from_spark(self._spark_to_pandas_wrapped(self._spark_df))

        if self._arrow_table is not None:
            return self._arrow_table.to_pandas()

        if self._querytree is not None:
            if self._compute_mode == ComputeMode.ATHENA:
                output = self._to_pandas_from_athena(pretty_sql)
            elif self._compute_mode == ComputeMode.RIFT:
                output = self._to_pandas_from_duckdb(pretty_sql)
                if conf.TECTON_STRIP_TIMEZONE_FROM_FEATURE_VALUES_FF.enabled():
                    output = _remove_timezones(output)
            elif self._compute_mode == ComputeMode.SPARK:
                output = convert_pandas_timestamps_from_spark(self._spark_to_pandas_wrapped(self.to_spark()))
            else:
                raise ValueError(self._compute_mode)
            # Cache this since it's important to keep this around. We call this method repeatedly e.g. to do spine
            # validation, infer timestamps, etc. We also generate a unique id based on this object and rely on that
            # to be stable.
            self._pandas_df = output
            return output

    @property
    def _compute_mode(self):
        assert self._querytree is not None, "Must be called on a QueryTree DataFrame"
        return self._querytree.node.compute_mode

    def _to_spark(self, spark: PySparkSession) -> PySparkDataFrame:
        return translate.spark_convert(self._querytree, spark).to_dataframe(spark)

    # Converts all datetime columns within the DF to UTC datetimes at microsecond precision
    @staticmethod
    def _cast_timestamps_to_utc_aware_pandas(df: pandas.DataFrame) -> pandas.DataFrame:
        def is_datetime_col(column):
            return is_datetime64_any_dtype(column) or is_datetime64tz_dtype(column)

        # TODO: It is inefficient to check each of these explicitly, but the alternative does not
        # correctly filter non TS values (see test_to_utc_aware_pandas_with_incorrect_input)
        #
        # `df.select_dtypes(include=[pandas.DatetimeTZDtype, "datetime", "datetime64"]).columns`
        for col in df.columns:
            if is_datetime_col(df[col]):
                # Localize where necessary, because pandas refuses to cast from a tz naive object
                if df[col].dt.tz is None:
                    df[col] = df[col].dt.tz_localize("UTC", ambiguous="NaT", nonexistent="NaT")
                # Convert to UTC
                df[col] = df[col].dt.tz_convert("UTC").astype("datetime64[ns, UTC]")

        return df

    def _to_arrow_reader(self) -> "pyarrow.RecordBatchReader":
        if self._arrow_table is not None:
            return self._arrow_table.to_reader()
        elif self._pandas_df is not None:
            return pyarrow.Table.from_pandas(self._pandas_df).to_reader()
        elif self._querytree:
            from tecton_core.query import query_tree_executor

            assert self._compute_mode == ComputeMode.RIFT, "Query tree must be in Rift mode to convert to Arrow"
            fv_dialect = get_pipeline_dialect(self._querytree)
            if fv_dialect is not None and fv_dialect not in (
                Dialect.SNOWFLAKE,
                Dialect.PANDAS,
                Dialect.BIGQUERY,
            ):
                msg = f"Rift does not support feature views of {fv_dialect.value} dialect."
                raise ValueError(msg)

            executor = query_tree_executor.QueryTreeExecutor(
                secret_resolver=LocalDevSecretResolver(),
                offline_store_options_providers=INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS,
                model_artifact_provider=MDSModelArtifactProvider(),
            )
            return executor.exec_qt(self._querytree).result_table
        else:
            raise NotImplementedError

    def _to_pandas_from_duckdb(self, pretty_sql: bool) -> pandas.DataFrame:
        from tecton_core.query import query_tree_executor

        # TODO(danny): support pretty_sql
        fv_dialect = get_pipeline_dialect(self._querytree)
        if fv_dialect is not None and fv_dialect not in (
            Dialect.SNOWFLAKE,
            Dialect.PANDAS,
            Dialect.BIGQUERY,
        ):
            msg = f"Rift does not support feature views of {fv_dialect.value} dialect."
            raise Exception(msg)

        executor = query_tree_executor.QueryTreeExecutor(
            secret_resolver=LocalDevSecretResolver(),
            offline_store_options_providers=INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS,
            model_artifact_provider=MDSModelArtifactProvider(),
        )

        qt_output_df = executor.exec_qt(self._querytree).result_df
        if not conf.TECTON_STRIP_TIMEZONE_FROM_FEATURE_VALUES_FF.enabled():
            qt_output_df = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(qt_output_df)

        return qt_output_df

    def _to_pandas_from_athena(self, pretty_sql: bool) -> pandas.DataFrame:
        with self._register_tables(tecton_core.query.dialect.Dialect.ATHENA):
            session = athena_session.get_session()
            recurse_query_tree(
                self._querytree,
                lambda node: register_feature_view_as_athena_table_if_necessary(
                    node.feature_definition_wrapper, session
                )
                if isinstance(node, OfflineStoreScanNode)
                else None,
            )
            views = self._register_querytree_views_or_tables(pretty_sql=pretty_sql)
            try:
                athena_sql_executor = AthenaSqlExecutor(session)
                df = athena_convert(self._querytree, athena_sql_executor, pretty_sql).to_dataframe()
            finally:
                # A tree and its subtree can share the same temp tables. If to_pandas() is called
                # concurrently, tables can be deleted when they are still being used by the other tree.
                for view_name, _ in views:
                    session.delete_view_if_exists(view_name)
            return df

    def _to_sql(self, pretty_sql: bool = False):
        if self._querytree is not None:
            if tree_contains(self._querytree, MultiOdfvPipelineNode):
                # SQL is not available for ODFVs. Showing SQL only for the subtree below the ODFV pipeline
                subtree = self.get_sql_node(self._querytree)
                return subtree.to_sql(pretty_sql=pretty_sql)
            else:
                return self._querytree.to_sql(pretty_sql=pretty_sql)
        else:
            raise NotImplementedError

    def get_sql_node(self, tree: NodeRef):
        """
        Returns the first node from which SQL can be generated from the TectonDataFrame's query tree.

        :param tree: Subtree for which to generate SQL
        """
        can_be_pushed = (
            MultiOdfvPipelineNode,
            RenameColsNode,
        )
        if isinstance(tree.node, can_be_pushed):
            return self.get_sql_node(tree.node.input_node)
        return tree

    @contextlib.contextmanager
    def _register_tables(self, dialect: tecton_core.query.dialect.Dialect):
        tables = set()

        def maybe_register_temp_table(node):
            if isinstance(node, UserSpecifiedDataNode):
                assert isinstance(node.data, TectonDataFrame), "Must be called with a TectonDataFrame"
                # Don't register the same table twice
                if node.data._temp_table_name not in tables:
                    tmp_table_name = node.data._register_temp_table(dialect)
                    tables.add(tmp_table_name)

        recurse_query_tree(
            self._querytree,
            maybe_register_temp_table,
        )

        try:
            yield
        finally:
            self._drop_temp_tables(dialect, tables)

    def _get_querytree_sql_views(self, pretty_sql=False):
        qt_views = []
        recurse_query_tree(self._querytree, lambda node: qt_views.extend(node.get_sql_views(pretty_sql=pretty_sql)))
        return qt_views

    def _register_querytree_views_or_tables(self, pretty_sql=False) -> typing.Sequence[Tuple[str, str]]:
        views = self._get_querytree_sql_views(pretty_sql=pretty_sql)
        if self._compute_mode == ComputeMode.ATHENA:
            session = athena_session.get_session()
            for view_name, view_sql in views:
                session.create_view(view_sql, view_name)
        else:
            raise ValueError(self._compute_mode)
        return views

    @classmethod
    def _create(
        cls,
        df: Union[PySparkDataFrame, pandas.DataFrame, NodeRef, pyarrow.Table],
        rewrite: bool = True,
    ):
        """Creates a Tecton DataFrame from a Spark or Pandas DataFrame."""
        if isinstance(df, pandas.DataFrame):
            return cls(spark_df=None, pandas_df=df)
        elif is_pyspark_df(df):
            return cls(spark_df=df, pandas_df=None)
        elif isinstance(df, NodeRef):
            return cls(spark_df=None, pandas_df=None, querytree_do_not_use=df, need_rewrite_tree=rewrite)
        elif isinstance(df, pyarrow.Table):
            return cls(spark_df=None, pandas_df=None, arrow_table=df)

        msg = f"Input must be of type pandas.DataFrame, pyspark.sql.Dataframe, pyarrow.Table, NodeRef, not {type(df)}"
        raise TypeError(msg)

    @classmethod
    def _create_from_dataframes(
        cls,
        dfs: List["TectonDataFrame"],
    ):
        return cls(children_dfs=dfs)

    @classmethod
    def _create_from_pandas_with_schema(cls, df: pandas.DataFrame, schema: Schema):
        if isinstance(df, pandas.DataFrame):
            missing = list(set(schema.column_names()) - set(df.columns))
            if missing:
                raise errors.MISSING_SPINE_COLUMN(missing[0], missing[0], df.columns)
            return cls(spark_df=None, pandas_df=df, schema=schema)
        msg = f"DataFrame must be pandas.DataFrame when using _create_from_pandas, not {type(df)}"
        raise TypeError(msg)

    def subtree(self, node_id: int) -> "TectonDataFrame":
        """
        Creates a TectonDataFrame from a subtree of prior querytree labeled by a node id in .explain().

        :param node_id: identifier of node from .explain()
        :return:
        """
        if not self._querytree:
            msg = "Cannot construct a TectonDataFrame from a node id."
            raise RuntimeError(msg)

        tree = self._querytree.create_tree()
        qt_root = NodeRef(tree.get_node(node_id).data)

        if self._compute_mode == ComputeMode.RIFT:
            # Rift requires StagingNodes to properly execute a querytree with a DataSourceScanNode or a
            # FeatureViewPipelineNode. If a StagingNode is not present, we add one.
            data_source_staging_nodes = get_staging_nodes(qt_root, QueryTreeStep.DATA_SOURCE)
            data_source_scan_node = get_first_input_node_of_class(qt_root, node_class=DataSourceScanNode)
            pipeline_staging_nodes = get_staging_nodes(qt_root, QueryTreeStep.PIPELINE)
            feature_view_pipeline_node = get_first_input_node_of_class(qt_root, node_class=FeatureViewPipelineNode)
            if len(data_source_staging_nodes) == 0 and data_source_scan_node is not None:
                staging_node = StagingNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    input_node=qt_root.deepcopy(),
                    staging_table_name=data_source_scan_node.ds.name,
                    query_tree_step=QueryTreeStep.DATA_SOURCE,
                )
                qt_root.node = staging_node
            elif len(pipeline_staging_nodes) == 0 and feature_view_pipeline_node is not None:
                staging_node = StagingNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    input_node=qt_root.deepcopy(),
                    staging_table_name=feature_view_pipeline_node.feature_definition_wrapper.name,
                    query_tree_step=QueryTreeStep.PIPELINE,
                )
                qt_root.node = staging_node

        # Do not apply rewrites again as they should have already been applied when generating the query tree for this
        # TectonDataFrame.
        return TectonDataFrame._create(qt_root, rewrite=False)

    def _timed_to_pandas(self):
        """Convenience method for measuring performance."""
        start = time.time()
        ret = self.to_spark().toPandas()
        end = time.time()
        print(f"took {end - start} seconds")
        return ret

    # The methods below implement the DataframeWrapper interface
    def _register_temp_table(self, dialect: tecton_core.query.dialect.Dialect):
        if dialect == tecton_core.query.dialect.Dialect.SPARK:
            self.to_spark().createOrReplaceTempView(self._temp_table_name)
            return
        if dialect == tecton_core.query.dialect.Dialect.ATHENA:
            session = athena_session.get_session()
            session.write_pandas(self.to_pandas(), self._temp_table_name)
        elif dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
            session = SnowflakeContext.get_instance().get_session()
            df_to_write = self.to_pandas()
            convert_pandas_df_for_snowflake_upload(df_to_write)
            session.write_pandas(
                df_to_write,
                table_name=self._temp_table_name,
                auto_create_table=True,
                table_type="temporary",
                quote_identifiers=False,
                overwrite=True,
                parallel=64,
                chunk_size=1000000,
                use_logical_type=True,
            )
        elif dialect == tecton_core.query.dialect.Dialect.DUCKDB:
            from tecton_core import duckdb_factory

            pandas_df = self.to_pandas()
            connection = duckdb_factory.create_connection()
            connection.sql(f"CREATE OR REPLACE TABLE {self._temp_table_name} AS SELECT * FROM pandas_df")
            connection.close()
        else:
            msg = f"Unexpected dialect {dialect}"
            raise Exception(msg)

        return self._temp_table_name

    def _drop_temp_tables(self, dialect: tecton_core.query.dialect.Dialect, tables: typing.Collection[str]):
        if dialect == tecton_core.query.dialect.Dialect.ATHENA:
            session = athena_session.get_session()
            for temp_table in tables:
                session.delete_table_if_exists(session.get_database(), temp_table)
        elif dialect == tecton_core.query.dialect.Dialect.SPARK:
            from tecton.tecton_context import TectonContext

            spark = TectonContext.get_instance()._spark
            for temp_table in tables:
                # DROP VIEW/DROP TABLE sql syntax is invalidated when spark_catalog is set to DeltaCatalog on EMR clusters
                if (
                    spark.conf.get("spark.sql.catalog.spark_catalog", "")
                    == "org.apache.spark.sql.delta.catalog.DeltaCatalog"
                ):
                    spark.catalog.dropTempView(temp_table)
                else:
                    spark.sql(f"DROP VIEW IF EXISTS {temp_table}")
        elif dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
            # Snowpark automatically drops temp views when the session ends
            # All other temp views/tables are created with 'overwrite' mode
            pass

    def _select_distinct(self, columns: List[str]) -> DataframeWrapper:
        if self._pandas_df is not None:
            return TectonDataFrame._create(self._pandas_df[columns].drop_duplicates())
        elif self._spark_df is not None:
            return TectonDataFrame._create(self._spark_df.select(columns).distinct())
        else:
            raise NotImplementedError

    @property
    def _dataframe(self) -> Union[pyspark.sql.DataFrame, pandas.DataFrame]:
        if self._spark_df is not None:
            return self._spark_df
        elif self._pandas_df is not None:
            return self._pandas_df
        elif self._querytree:
            if self._compute_mode == ComputeMode.SPARK:
                return self.to_spark()
            else:
                return self.to_pandas()
        elif self._arrow_table is not None:
            return self._arrow_table.to_pandas()
        else:
            raise NotImplementedError

    @property
    def columns(self) -> Sequence[str]:
        """The columns of the dataframe"""
        if self._querytree:
            return self._querytree.columns
        elif self._spark_df is not None:
            return self._spark_df.columns
        elif self._pandas_df is not None:
            return list(self._pandas_df.columns)
        else:
            raise NotImplementedError

    @property
    def schema(self) -> Schema:
        """The schema of the dataframe"""
        if self._querytree:
            return self._querytree.output_schema
        elif self._pandas_df is not None:
            if not self._pandas_df.shape[0] and self._schema:
                return self._schema

            arrow_schema = pyarrow.Schema.from_pandas(self._pandas_df, preserve_index=False)
            return arrow_schema_to_tecton_schema(arrow_schema)
        elif self._spark_df is not None:
            from tecton_spark.vendor.pyspark.sql.pandas.types import to_arrow_schema

            arrow_schema = to_arrow_schema(self._spark_df.schema)
            return arrow_schema_to_tecton_schema(arrow_schema, ignore_unsupported_types=True)
        elif self._arrow_table is not None:
            return arrow_schema_to_tecton_schema(self._arrow_table.schema)

        # TODO(oleksii): implement schema conversion for other sources
        return Schema.from_dict({})


# for legacy compat
DataFrame = TectonDataFrame

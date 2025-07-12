from __future__ import annotations

import dataclasses
import datetime
import enum
import inspect
import logging
import os
import re
import shutil
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union
from typing import overload

import attrs
import numpy
import pandas
from google.protobuf import duration_pb2
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming
from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton import Attribute
from tecton import Calculation
from tecton import run_api_consts
from tecton import tecton_context
from tecton import types
from tecton import vnext
from tecton._internals import athena_api
from tecton._internals import delete_keys_api
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import materialization_api
from tecton._internals import metadata_service
from tecton._internals import mock_source_utils
from tecton._internals import query_helper
from tecton._internals import querytree_api
from tecton._internals import run_api
from tecton._internals import sdk_decorators
from tecton._internals import spark_api
from tecton._internals import type_utils
from tecton._internals import utils as internal_utils
from tecton._internals import validations_api
from tecton._internals.model_utils import model_type_string_to_enum
from tecton._internals.sdk_decorators import deprecated
from tecton._internals.secret_resolver import LocalDevSecretResolver
from tecton._internals.tecton_typeguard import batch_feature_view_typechecked
from tecton._internals.tecton_typeguard import realtime_feature_view_typechecked
from tecton._internals.tecton_typeguard import stream_feature_view_typechecked
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton.framework import data_source as framework_data_source
from tecton.framework import entity as framework_entity
from tecton.framework import feature
from tecton.framework import model_config
from tecton.framework import repo_config
from tecton.framework import resource_provider
from tecton.framework import transformation as framework_transformation
from tecton.framework import utils
from tecton.framework.configs import RECOMMENDED_PYTHON_VERSION_EMR
from tecton.framework.configs import Secret
from tecton.framework.configs import convert_secret_to_sanitized_reference
from tecton.framework.data_frame import FeatureVector
from tecton.framework.data_frame import GetFeaturesForEventsParams
from tecton.framework.data_frame import GetFeaturesInRangeParams
from tecton.framework.data_frame import TectonDataFrame
from tecton.framework.data_source import FilteredSource
from tecton.framework.feature import Aggregate
from tecton.framework.feature import Feature
from tecton.framework.feature import FeatureMetadata
from tecton.framework.transformation import PipelineNodeWrapper
from tecton.types import SdkDataType
from tecton.types import Timestamp
from tecton_core import aggregation_utils
from tecton_core import conf
from tecton_core import data_types
from tecton_core import errors as core_errors
from tecton_core import fco_container
from tecton_core import feature_definition_wrapper
from tecton_core import feature_set_config
from tecton_core import id_helper
from tecton_core import request_context
from tecton_core import schema
from tecton_core import schema_derivation_utils
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import default_batch_compute_mode
from tecton_core.compute_mode import offline_retrieval_compute_mode
from tecton_core.embeddings.artifacts_provider import _initialize_model_cache_dir
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.filter_utils import FilterDateTime
from tecton_core.filter_utils import TectonTimeConstant
from tecton_core.materialization_context import MaterializationContext
from tecton_core.materialization_context import materialization_context
from tecton_core.mock_context import MockContext
from tecton_core.pandas_compat import pandas_to_spark
from tecton_core.pipeline import pipeline_common
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.realtime_context import REQUEST_TIMESTAMP_FIELD_NAME
from tecton_core.realtime_context import RealtimeContext
from tecton_core.repo_file_handler import construct_fco_source_info
from tecton_core.schema import Schema
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_core.specs import MaterializedFeatureViewSpec
from tecton_core.specs.time_window_spec import LifetimeWindowSpec
from tecton_core.specs.time_window_spec import RelativeTimeWindowSpec
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.time_window_spec import create_time_window_spec_from_data_proto
from tecton_core.specs.utils import get_field_or_none
from tecton_core.tecton_pendulum import Duration
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import fco_args__client_pb2 as fco_args_pb2
from tecton_proto.args import feature_service__client_pb2 as feature_service_pb2
from tecton_proto.args import feature_view__client_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2
from tecton_proto.args import transformation__client_pb2 as transformation_pb2
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.common import data_source_type__client_pb2 as data_source_type_pb2
from tecton_proto.common import fco_locator__client_pb2 as fco_locator_pb2
from tecton_proto.common import id__client_pb2 as id_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.common.data_source_type__client_pb2 import DataSourceType
from tecton_proto.data import materialization_status__client_pb2 as materialization_status_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.modelartifactservice import model_artifact_data__client_pb2 as model_artifact_data_pb2
from tecton_proto.modelartifactservice import model_artifact_service__client_pb2 as model_artifact_service_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


CONSTRAINTS_ERROR_MESSAGE = "environments and required_packages cannot be set together"

# FilteredSource start offsets smaller (more negative) than this offset will be considered UNBOUNDED_PRECEEDING.
MIN_START_OFFSET = datetime.timedelta(days=-365 * 100)  # 100 years

# This is the mode used when the feature view decorator is used on a pipeline function, i.e. one that only contains
# references to transformations and constants.
PIPELINE_MODE = "pipeline"

# Mode used when feature view is instantiated directly without a decorator and thereby without a transformation.
# The user should never have to set this manually - it will be inferred when they call RealtimeFeatureView constructor
# directly (without the decorator) and leave off the "mode" argument.
NO_TRANSFORMATION_MODE_STR = "no_transformation"

# Default name for realtime context
# If a Realtime Feature View is defined without a transformation, the realtime context can be accessed using DEFAULT_CONTEXT_PARAMETER_NAME.
# Mirrored in FeatureServer (engine.go).
DEFAULT_CONTEXT_PARAMETER_NAME = "context"

# Delimiter for column references in calculation and attribute features in no-transformation rtfvs
CALCULATION_COLUMN_REFERENCE_DELIMITER = "."
ATTRIBUTE_COLUMN_REFERENCE_DELIMITER = "__"

MOCK_INPUT_TYPES = Union[pandas.DataFrame, pyspark_dataframe.DataFrame, MockContext, RealtimeContext]

logger = logging.getLogger(__name__)


# Create a parallel enum class since Python proto extensions do not use an enum class.
# Keep up-to-date with StreamProcessingMode from tecton_proto/args/feature_view.proto.
class StreamProcessingMode(enum.Enum):
    TIME_INTERVAL = feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_TIME_INTERVAL
    CONTINUOUS = feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS


# Keep up-to-date with BatchTriggerType from tecton_proto/args/feature_view.proto.
class BatchTriggerType(enum.Enum):
    SCHEDULED = feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_SCHEDULED
    MANUAL = feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_MANUAL
    NO_BATCH_MATERIALIZATION = feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_NO_BATCH_MATERIALIZATION


class FeatureStoreFormatVersion(enum.Enum):
    NANOSECONDS = feature_view__args_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS
    TTL = (
        feature_view__args_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_ONLINE_STORE_TTL_DELETION_ENABLED
    )


class AggregationLeadingEdge(enum.Enum):
    """Defines the leading edge timestamp for aggregation windows in stream feature views during online retrieval.

    WALL_CLOCK_TIME: Stream aggregation windows are fetched relative to the wall clock time at the time of online retrieval.
    LATEST_EVENT_TIME: Stream aggregation windows are fetched relative the latest materialized event timestamp for the stream feature view. This timestamp is also known as the stream high watermark.

    Example:
        For a stream that is 30-seconds delayed and a 10-minute aggregation window:
        - WALL_CLOCK_TIME at 12:00:00 uses the window [11:50:00, 12:00:00]
        - LATEST_EVENT_TIME at 12:00:00 uses the window [11:49:30, 11:59:30]

    Refer to documentation for detailed implications of each option.
    """

    UNSPECIFIED = feature_view__args_pb2.AggregationLeadingEdge.AGGREGATION_MODE_UNSPECIFIED
    WALL_CLOCK_TIME = feature_view__args_pb2.AggregationLeadingEdge.AGGREGATION_MODE_WALL_CLOCK_TIME
    LATEST_EVENT_TIME = feature_view__args_pb2.AggregationLeadingEdge.AGGREGATION_MODE_LATEST_EVENT_TIME


@attrs.define(auto_attribs=True)
class QuerySources:
    from_source_count: int = 0
    offline_store_count: int = 0
    realtime_count: int = 0
    feature_table_count: int = 0

    def __add__(self, other: "QuerySources"):
        return QuerySources(
            from_source_count=self.from_source_count + other.from_source_count,
            offline_store_count=self.offline_store_count + other.offline_store_count,
            realtime_count=self.realtime_count + other.realtime_count,
            feature_table_count=self.feature_table_count + other.feature_table_count,
        )

    def _print_from_source_message(self, count: int, single: str, message: str):
        if count > 0:
            feature_view_text = internal_utils.plural(count, f"{single} is", f"{single}s are")
            logger.info(f"{count} {feature_view_text} {message}")

    def display(self):
        self._print_from_source_message(
            self.offline_store_count, "Feature View", "being read from data in the offline store."
        )
        self._print_from_source_message(
            self.from_source_count, "Feature View", "being computed directly from raw data sources."
        )
        self._print_from_source_message(
            self.feature_table_count, "Feature Table", "being loaded from the offline store."
        )
        self._print_from_source_message(self.realtime_count, "Realtime Feature View", "being computed ad hoc.")


def _to_pyspark_mocks(
    mock_inputs: Dict[str, MOCK_INPUT_TYPES],
) -> Dict[str, pyspark_dataframe.DataFrame]:
    pyspark_mock_inputs = {}
    for input_name, mock_data in mock_inputs.items():
        if is_pyspark_df(mock_data):
            pyspark_mock_inputs[input_name] = mock_data
        elif isinstance(mock_data, pandas.DataFrame):
            spark = tecton_context.TectonContext.get_instance()._spark
            pyspark_mock_inputs[input_name] = pandas_to_spark(spark, mock_data)
        else:
            msg = f"Unexpected mock source type for kwarg {input_name}: {type(mock_data)}"
            raise TypeError(msg)
    return pyspark_mock_inputs


@dataclasses.dataclass
class _Schemas:
    view_schema: Optional[schema_pb2.Schema]
    materialization_schema: Optional[schema_pb2.Schema]
    online_batch_table_format: Optional[schema_pb2.OnlineBatchTableFormat]


@attrs.define(eq=False)
class FeatureView(base_tecton_object.BaseTectonObject):
    """Base class for Feature View classes (including Feature Tables)."""

    # A FeatureDefinitionWrapper instance, which contains the Feature View spec for this Feature View and dependent
    # FCO specs (e.g. Data Source specs).
    _feature_definition: Optional[feature_definition_wrapper.FeatureDefinitionWrapper] = attrs.field(repr=False)

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and fetched
    # from the Tecton backend.
    _args: Optional[feature_view__args_pb2.FeatureViewArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    # A supplement to the _args proto that is needed to create the Feature View spec.
    _args_supplement: Optional[specs.FeatureViewSpecArgsSupplement] = attrs.field(repr=False)

    @property
    def _spec(self) -> Optional[specs.FeatureViewSpec]:
        return self._feature_definition.fv_spec if self._feature_definition is not None else None

    @property
    def _supported_modes(self) -> List[str]:
        raise NotImplementedError

    @sdk_decorators.assert_local_object
    def _build_and_resolve_args(self, objects) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(feature_view=self._args)

    def _build_fco_validation_args(
        self, local_models: Optional[List[model_artifact_data_pb2.ModelArtifactInfo]] = None
    ) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            assert self._args_supplement is not None
            return validator_pb2.FcoValidationArgs(
                feature_view=validator_pb2.FeatureViewValidationArgs(
                    args=self._args,
                    view_schema=self._args_supplement.view_schema,
                    materialization_schema=self._args_supplement.materialization_schema,
                    local_model_artifacts=local_models,
                )
            )
        else:
            return self._spec.validation_args

    @staticmethod
    def _get_or_create_pipeline_function(
        name: str,
        mode: str,
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Dict[str, str]],
        feature_view_function,
    ):
        """Helper method for creating the pipeline function from args"""
        if mode == PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = framework_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        return pipeline_function

    @typechecked
    def _build_pipeline(
        self,
        fv_name: str,
        feature_view_function: Callable,
        pipeline_function: Callable[..., framework_transformation.PipelineNodeWrapper],
        sources: Sequence[
            Union[
                framework_data_source.DataSource,
                FilteredSource,
                configs.RequestSource,
                FeatureView,
                FeatureReference,
            ]
        ],
        context_parameter_name: Optional[str],
    ) -> framework_transformation.PipelineNodeWrapper:
        pipeline_kwargs = self._build_transformation_kwargs(feature_view_function, sources, context_parameter_name)
        pipeline_root = pipeline_function(**pipeline_kwargs)
        # we bind to user_function since pipeline_function may be artificially created and just accept **kwargs
        _test_binding_user_function(feature_view_function, pipeline_kwargs)

        pipeline_common.check_transformation_type(
            fv_name, pipeline_root.node_proto, "pipeline", supported_modes=self._supported_modes
        )

        return pipeline_root

    def _build_transformation_kwargs(
        self,
        user_function: Callable,
        sources: Sequence[
            Union[
                framework_data_source.DataSource,
                FilteredSource,
                configs.RequestSource,
                FeatureView,
                FeatureReference,
            ]
        ],
        context_parameter_name: Optional[str],
    ) -> Dict[str, Any]:
        non_context_params = [
            param.name
            for param in inspect.signature(user_function).parameters.values()
            if not _is_context_param(param, context_parameter_name)
        ]
        kwargs = dict(zip(non_context_params, sources))

        for param_name, source in kwargs.items():
            pipeline_node = _source_to_pipeline_node(source=source, input_name=param_name)
            kwargs[param_name] = pipeline_node

        context_exists = False
        for param in inspect.signature(user_function).parameters.values():
            if _is_context_param(param, context_parameter_name):
                if context_exists:
                    raise errors.TOO_MANY_TRANSFORMATION_CONTEXTS(user_function.__name__)

                context_exists = True
                # TODO(lilly/ajeya): Remove is_legacy_context_param bifurcation once `context=materialization_context()` is removed in 1.2
                # https://linear.app/tecton/issue/FE-2228/remove-is-legacy-context-param-bifurcation-logic-when
                if _is_legacy_context_param(param):
                    logger.warning(
                        "`context=materialization_context()` is deprecated in versions >=1.0. Use `context` directly instead. For example, instead of `my_func(source, context=materialization_context()`, use `my_func(source, context)`."
                    )
                    kwargs[param.name] = materialization_context()
                else:
                    if isinstance(self, MaterializedFeatureView):
                        kwargs[param.name] = pipeline_pb2.ContextNode(
                            context_type=pipeline_pb2.ContextType.CONTEXT_TYPE_MATERIALIZATION,
                            input_name=param.name,
                        )
                    elif isinstance(self, RealtimeFeatureView):
                        kwargs[param.name] = pipeline_pb2.ContextNode(
                            context_type=pipeline_pb2.ContextType.CONTEXT_TYPE_REALTIME,
                            input_name=param.name,
                        )
                    else:
                        raise errors.TRANSFORMATION_CONTEXT_NOT_SUPPORTED

        if not context_exists and context_parameter_name is not None:
            raise errors.TRANSFORMATION_CONTEXT_NAME_NOT_FOUND(context_parameter_name, user_function.__name__)

        return kwargs

    def _get_schemas(self) -> _Schemas:
        """Get schemas from the user-supplied schema or features argument."""
        raise NotImplementedError

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        raise NotImplementedError

    def _get_dependent_specs(self) -> List[specs.TectonObjectSpec]:
        """Returns all of the specs dependend on by this Feature View."""
        dependent_objects = self._get_dependent_objects(include_indirect_dependencies=True)
        return [obj._spec for obj in dependent_objects]

    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        raise NotImplementedError

    @property
    @sdk_decorators.sdk_public_method
    def join_keys(self) -> List[str]:
        """The join key column names."""
        return list(self._spec.join_keys)

    @property
    @sdk_decorators.sdk_public_method
    def online_serving_index(self) -> List[str]:
        """The set of join keys that will be indexed and queryable during online serving.

        defaults to the complete set of join keys.
        """
        return list(self._spec.online_serving_keys)

    @property
    @sdk_decorators.sdk_public_method
    def wildcard_join_key(self) -> Optional[set]:
        """Returns a wildcard join key column name if it exists; Otherwise returns None."""
        wildcard_keys = set(self.join_keys) - set(self.online_serving_index)
        if len(wildcard_keys) == 0:
            return None
        elif len(wildcard_keys) == 1:
            return next(iter(wildcard_keys))
        else:
            msg = "The online serving index must either be equal to join_keys or only be missing a single key."
            raise ValueError(msg)

    @property
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def url(self) -> str:
        """Returns a link to the Tecton Web UI."""
        return self._spec.url

    @sdk_decorators.sdk_public_method
    def get_feature_columns(self) -> List[str]:
        """
        Retrieves the list of feature columns produced by this FeatureView.

        :return: The features produced by this FeatureView.
        """
        return self._feature_definition.features

    @sdk_decorators.sdk_public_method
    def print_transformation_schema(self) -> None:
        """Prints the schema of the output of the transformation."""
        transformation_schema = self.transformation_schema()
        print(
            "If copy/pasting the schema below, import the specified datatypes from tecton.types\n"
            + type_utils.schema_pretty_str(transformation_schema)
        )

    @sdk_decorators.sdk_public_method
    def transformation_schema(self) -> List[types.Field]:
        """Returns the schema of the output of the transformation."""
        view_schema = self._feature_definition.view_schema.to_proto()
        return querytree_api.get_fields_list_from_tecton_schema(view_schema)

    @property
    def prevent_destroy(self) -> bool:
        """If set to True, Tecton will block destructive actions taken on this Feature View or Feature Table."""
        return self._spec.prevent_destroy

    @property
    def feature_metadata(self) -> List[FeatureMetadata]:
        metadata = []
        for feature_metadata_spec in self._spec.feature_metadata:
            metadata.append(FeatureMetadata._from_spec(feature_metadata_spec))

        return metadata

    def _validate(self, local_models: Optional[List[model_artifact_data_pb2.ModelArtifactInfo]] = None) -> None:
        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(
                validation_args=[
                    dependent_obj._build_fco_validation_args()
                    for dependent_obj in self._get_dependent_objects(include_indirect_dependencies=True)
                ]
                + [self._build_fco_validation_args(local_models=local_models)],
            ),
        )

    def _get_args_supplement(
        self, schemas, model_artifacts: Optional[Dict[str, model_artifact_data_pb2.ModelArtifactInfo]] = None
    ):
        return specs.FeatureViewSpecArgsSupplement(
            view_schema=schemas.view_schema,
            materialization_schema=schemas.materialization_schema,
            online_batch_table_format=schemas.online_batch_table_format,
            model_artifacts=model_artifacts,
        )

    def _populate_spec(self) -> None:
        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, self._args_supplement)
        fco_container_specs = [*self._get_dependent_specs(), fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])
        self._feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human-readable summary."""
        request = metadata_service_pb2.GetFeatureViewSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self.info.workspace)
        )
        response = metadata_service.instance().GetFeatureViewSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> feature_set_config.FeatureSetConfig:
        return feature_set_config.FeatureSetConfig.from_feature_definition(self._feature_definition)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.cancel_job)
    @sdk_decorators.assert_remote_object
    def cancel_materialization_job(self, job_id: str) -> materialization_api.MaterializationJob:
        logger.warning("FeatureView.`cancel_materialization_job` function is deprecated. Use job.cancel() instead.")
        job = self.get_materialization_job(job_id)
        return job.cancel()

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_materialization_job(self, job_id: str) -> materialization_api.MaterializationJob:
        """
        Retrieves data about the specified materialization job.
        :param job_id: ID string of the materialization job.
        :return: `MaterializationJobData` object for the job.
        """
        job = materialization_api.get_job(self.workspace, job_id, feature_view=self.name)
        if not isinstance(job, materialization_api.MaterializationJob):
            msg = f"Job {job_id} is not a materialization job"
            raise TypeError(msg)

        return job

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def list_materialization_jobs(self) -> List[materialization_api.MaterializationJob]:
        """
        Retrieves the list of all materialization jobs for this feature view.

        :return: List of `MaterializationJobData` objects.
        """
        return [
            job
            for job in materialization_api.list_jobs(workspace=self.workspace, feature_view=self.name)
            if isinstance(job, materialization_api.MaterializationJob)
        ]

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_job(self, job_id: str) -> materialization_api.TectonJob:
        """
        Retrieves data about the specified job (materialization or dataset generation).
        :param job_id: ID string of the job.
        :return: `JobData` object for the job.
        """
        return materialization_api.get_job(workspace=self.workspace, job_id=job_id, feature_view=self.name)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def list_jobs(self) -> List[materialization_api.TectonJob]:
        """
        Retrieves the list of all jobs (materialization and dataset generation) for this Feature View or Feature Table.

        :return: List of `JobData` objects.
        """
        return materialization_api.list_jobs(workspace=self.workspace, feature_view=self.name)

    @sdk_decorators.assert_remote_object
    def _get_materialization_status(self) -> materialization_status_pb2.MaterializationStatus:
        # TODO(TEC-13080): delete this private method when integration tests no longer use it.
        return materialization_api.get_materialization_status_response(self._spec.id_proto, self.workspace)

    @sdk_decorators.assert_remote_object
    def _get_serving_status(self):
        request = metadata_service_pb2.GetServingStatusRequest(
            feature_package_id=id_helper.IdHelper.from_string(self._feature_definition.id), workspace=self.workspace
        )
        return metadata_service.instance().GetServingStatus(request)

    def __getitem__(self, features: List[str]) -> FeatureReference:
        """
        Used to select a subset of features from a Feature View for use within a Feature Service.

        ```python
        from tecton import FeatureService

        # `my_feature_view` is a feature view that contains three features: `my_feature_1/2/3`. The Feature Service
        # can be configured to include only two of those features like this:
        feature_service = FeatureService(
            name="feature_service",
            features=[
                my_feature_view[["my_feature_1", "my_feature_2"]]
            ],
        )
        ```
        """
        if not isinstance(features, list):
            msg = "The `features` field must be a list"
            raise TypeError(msg)

        return FeatureReference(feature_definition=self, features=features)

    def with_name(self, namespace: str) -> FeatureReference:
        """Rename a Feature View or Feature Table used in a Feature Service.

        ```python
        from tecton import FeatureService

        # The feature view in this feature service will be named "new_named_feature_view" in training data dataframe
        # columns and other metadata.

        feature_service = FeatureService(
            name="feature_service",
            features=[
                my_feature_view.with_name("new_named_feature_view")
            ],
        )
        ```

        ```python
        # Here is a more sophisticated example. The join keys for this feature service will be "transaction_id",
        # "sender_id", and "recipient_id" and will contain three feature views named "transaction_features",
        # "sender_features", and "recipient_features".
        transaction_fraud_service = FeatureService(
            name="transaction_fraud_service",
            features=[
                # Select a subset of features from a feature view.
                transaction_features[["amount"]],

                # Rename a feature view and/or rebind its join keys. In this example, we want user features for both the
                # transaction sender and recipient, so include the feature view twice and bind it to two different feature
                # service join keys.
                user_features.with_name("sender_features").with_join_key_map({"user_id" : "sender_id"}),
                user_features.with_name("recipient_features").with_join_key_map({"user_id" : "recipient_id"}),
            ],
        )
        ```

        :param namespace: The namespace used to prefix the features joined from this FeatureView. By default, namespace
            is set to the FeatureView name.

        """
        return FeatureReference(feature_definition=self, namespace=namespace)

    def with_join_key_map(self, join_key_map: Dict[str, str]) -> FeatureReference:
        """Rebind join keys for a Feature View or Feature Table used in a Feature Service.

        The keys in join_key_map should be the join keys, and the values should be the feature service overrides.

        ```python
        from tecton import FeatureService

        # The join key for this feature service will be "feature_service_user_id".
        feature_service = FeatureService(
            name="feature_service",
            features=[
                my_feature_view.with_join_key_map({"user_id" : "feature_service_user_id"}),
            ],
        )

        # Here is a more sophisticated example. The join keys for this feature service will be "transaction_id",
        # "sender_id", and "recipient_id" and will contain three feature views named "transaction_features",
        # "sender_features", and "recipient_features".
        transaction_fraud_service = FeatureService(
            name="transaction_fraud_service",
            features=[
                # Select a subset of features from a feature view.
                transaction_features[["amount"]],

                # Rename a feature view and/or rebind its join keys. In this example, we want user features for both the
                # transaction sender and recipient, so include the feature view twice and bind it to two different feature
                # service join keys.
                user_features.with_name("sender_features").with_join_key_map({"user_id" : "sender_id"}),
                user_features.with_name("recipient_features").with_join_key_map({"user_id" : "recipient_id"}),
            ],
        )
        ```
        :param join_key_map: Dictionary remapping the join key names. Dictionary keys are join keys,
            values are the feature service override values.
        """
        return FeatureReference(feature_definition=self, override_join_keys=join_key_map.copy())


def _warn_if_emr_compute_uses_cluster_default_python(compute: configs.ComputeConfigTypes):
    emr_warning = f'Tecton recommends overriding the Python version of your EMR cluster to {RECOMMENDED_PYTHON_VERSION_EMR}. This can be done by setting `python_version="{RECOMMENDED_PYTHON_VERSION_EMR}"` on `EMRClusterConfig`.'
    if isinstance(compute, configs.EMRClusterConfig):
        if compute.python_version == "default":
            logger.warning(
                f"{emr_warning} For details, see https://docs.tecton.ai/docs/materializing-features/configure-spark-materialization/using-pinned-emr-and-databricks-runtime-releases#overriding-emr-default-python-version."
            )
    elif isinstance(compute, configs.EMRJsonClusterConfig):
        configurations = compute.json.get("Configurations")
        warning = f"{emr_warning} For details, see https://docs.tecton.ai/docs/materializing-features/configure-spark-materialization/configuring-job-clusters-via-json#configuring-emr-job-clusters."

        if configurations is None:
            logger.warning(warning)
            return

        spark_defaults = next(
            configuration for configuration in configurations if configuration["Classification"] == "spark-defaults"
        )

        # if the Python path for spark is not overridden, customer is most likely not using custom Python installation
        if spark_defaults is None:
            logger.warning(warning)
        elif spark_defaults.get("Properties", {}).get("spark.pyspark.python") is None:
            logger.warning(warning)


@attrs.define(eq=False)
class MaterializedFeatureView(FeatureView):
    """Class for BatchFeatureView and StreamFeatureView to inherit common methods from.

    Attributes:
        sources: The Data Sources for this Feature View.
        transformations: The Transformations for this Feature View.
        entities: The Entities for this Feature View.
    """

    sources: Tuple[framework_data_source.DataSource, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    transformations: Tuple[framework_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    entities: Tuple[framework_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    # Note providers are stored here so there are fetched in `_get_dependent_objects`
    # and put in the fco container. The key used in the map is not needed here.
    resource_providers: Tuple[resource_provider.ResourceProvider, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @property
    def _supported_modes(self) -> List[str]:
        return ["pipeline", "spark_sql", "pyspark", "snowflake_sql", "athena"]

    @property
    def _batch_compute_mode(self) -> BatchComputeMode:
        spec = self._spec
        assert isinstance(spec, MaterializedFeatureViewSpec), spec
        return spec.batch_compute_mode

    @classmethod
    @typechecked
    def _from_spec(
        cls, spec: specs.MaterializedFeatureViewSpec, fco_container_: fco_container.FcoContainer
    ) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        sources = []
        for data_source_spec in feature_definition.data_sources:
            sources.append(framework_data_source.data_source_from_spec(data_source_spec))

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(framework_entity.Entity._from_spec(entity_spec))

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(framework_transformation.Transformation._from_spec(transformation_spec))

        resource_providers = []
        for resource_provider_spec in feature_definition.resource_providers.values():
            resource_providers.append(resource_provider.ResourceProvider._from_spec(resource_provider_spec))

        # override the framework version class attribute to be the framework version set by the spec
        class MaterializedFeatureViewFromSpec(cls):
            _framework_version = spec.metadata.framework_version

        obj = MaterializedFeatureViewFromSpec.__new__(MaterializedFeatureViewFromSpec)  # pylint: disable=no-value-for-parameter
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=tuple(sources),
            entities=tuple(entities),
            transformations=tuple(transformations),
            resource_providers=resource_providers,
            args_supplement=None,
        )
        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        return list(self.sources) + list(self.entities) + list(self.transformations) + list(self.resource_providers)

    def _get_schemas(
        self, model_artifacts: Optional[Dict[str, model_artifact_data_pb2.ModelArtifactInfo]] = None
    ) -> _Schemas:
        """Get schemas from the user-supplied schema or features argument."""
        entity_specs = [entity._spec for entity in self.entities]
        view_schema = self._build_feature_view_schema(entity_specs).to_proto()

        materialization_schema = schema_derivation_utils.compute_aggregate_materialization_schema_from_view_schema(
            view_schema, self._args, model_artifacts
        )

        online_batch_table_format = None
        if self._args.materialized_feature_view_args.compaction_enabled:
            online_batch_table_format = schema_derivation_utils.compute_batch_table_format_for_compaction(
                self._args, view_schema
            )

        return _Schemas(
            view_schema=view_schema,
            materialization_schema=materialization_schema,
            online_batch_table_format=online_batch_table_format,
        )

    # Note this function assumes valid column types defined in features. The actual validation of column data types happened in MDS.
    def _build_feature_view_schema(self, entity_specs: List[specs.EntitySpec]):
        schema_dict = {
            join_key.name: join_key.dtype for entity_spec in entity_specs for join_key in entity_spec.join_keys
        }

        attributes = self._args.materialized_feature_view_args.attributes
        embeddings = self._args.materialized_feature_view_args.embeddings
        inferences = self._args.materialized_feature_view_args.inferences
        aggregates = self._args.materialized_feature_view_args.aggregations

        if attributes or embeddings or inferences:
            schema_dict.update(
                {attribute.name: data_types.data_type_from_proto(attribute.column_dtype) for attribute in attributes}
            )
            schema_dict.update(
                {embedding.column: data_types.data_type_from_proto(embedding.column_dtype) for embedding in embeddings}
            )
            if inferences:
                for inference in inferences:
                    schema_dict.update(
                        {
                            input_column.name: data_types.data_type_from_proto(input_column.dtype)
                            for input_column in inference.input_columns
                        }
                    )
        else:  # aggregates case
            schema_dict.update(
                {aggregate.column: data_types.data_type_from_proto(aggregate.column_dtype) for aggregate in aggregates}
            )

            if self._args.materialized_feature_view_args.aggregation_secondary_key:
                schema_dict[self._args.materialized_feature_view_args.aggregation_secondary_key] = (
                    data_types.StringType()
                )

        # when timestamp_field is deprecated
        if self._args.materialized_feature_view_args.timestamp_field:
            schema_dict[self._args.materialized_feature_view_args.timestamp_field] = data_types.TimestampType()
        else:
            msg = "No timestamp field specified for the Materialized Feature View"
            raise TectonValidationError(msg)

        if self._args.materialized_feature_view_args.batch_publish_timestamp:
            schema_dict[self._args.materialized_feature_view_args.batch_publish_timestamp] = data_types.TimestampType()

        return schema.Schema.from_dict(schema_dict)

    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        fd = self._feature_definition

        if fd.is_incremental_backfill:
            if self.info._is_local_object:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES(fv_name=self.name, workspace_name=None)
            if not fd.materialization_enabled:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES(
                    fv_name=self.name, workspace_name=self.info.workspace
                )

            if from_source:
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE

            # from_source=None + offline=False computes from source which is not supported for incremental
            if from_source is None and (not fd.materialization_enabled or not fd.writes_to_offline_store):
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE
        elif from_source is False:
            if self._is_local_object:
                raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(self.name, "Feature View")
            elif not fd.writes_to_offline_store:
                raise errors.FD_GET_FEATURES_MATERIALIZATION_DISABLED(self.name)
            elif not fd.materialization_enabled:
                raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD(self.name, self.workspace)

        if from_source is None:
            from_source = not fd.materialization_enabled or not fd.writes_to_offline_store

        if from_source:
            return QuerySources(from_source_count=1)
        else:
            return QuerySources(offline_store_count=1)

    def _convert_data_sources_to_explicitly_filtered_objects(
        self,
        sources: Sequence[
            Union[
                framework_data_source.DataSource,
                FilteredSource,
                configs.RequestSource,
                FeatureView,
                FeatureReference,
            ]
        ],
    ) -> Sequence[Union[FilteredSource]]:
        new_sources = []
        for source in sources:
            # Invalid data sources for a materialized FV
            if isinstance(source, (FeatureReference, FeatureView, configs.RequestSource)):
                err = f"Unexpected source type {source.__class__} for Materialized Feature View"
                raise RuntimeError(err)
            elif isinstance(source, framework_data_source.DataSource):
                # FilteredSource is only supported for batch sources or sources with batch_configs.
                if source.data_source_type is DataSourceType.PUSH_NO_BATCH:
                    new_sources.append(source.unfiltered())
                else:
                    new_sources.append(
                        source.select_range(
                            start_time=TectonTimeConstant.MATERIALIZATION_START_TIME,
                            end_time=TectonTimeConstant.MATERIALIZATION_END_TIME,
                        )
                    )
            else:
                new_sources.append(source)
        return new_sources

    def _validate_start_and_end_times(self, start_time: datetime.datetime, end_time: datetime.datetime):
        if start_time is not None and end_time is not None:
            if start_time >= end_time:
                raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

            # feature_start_time should have a tz but end_time may not. Drop the info to allow a comparison
            # since a few hours either way shouldn't matter here
            if self.feature_start_time is not None and end_time.replace(tzinfo=None) < self.feature_start_time.replace(
                tzinfo=None
            ):
                raise core_errors.TIME_RANGE_NOT_BEFORE_FEATURE_START(start_time, end_time, self.feature_start_time)

    @sdk_decorators.sdk_public_method
    def get_features_in_range(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        max_lookback: Optional[datetime.timedelta] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **kwargs,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature view which were valid within the input time range.

        A feature value is considered to be valid at a specific point in time if the Online Store
        would have returned that value if queried at that moment in time.

        The DataFrame returned by this method contains the following:
        - Entity Join Key Columns
        - Feature Value Columns
        - The columns `_valid_from` and `_valid_to` that specify the time range for which the row of features values is
        valid. The time range defined by [`_valid_from`, `_valid_to`) will never intersect with any other rows for the same
        join keys.
        - `_valid_from` (Inclusive) is the timestamp from which feature values were valid and returned from the Online Feature
        Store for the corresponding set of join keys. `_valid_from` will never be less than `end_time`.
        Values for which `_valid_from` is equal to `start_time` may have been valid prior to `start_time`.
        - `_valid_to` (Exclusive) is the timestamp from which feature values are invalid and no longer returned from the
        Online Feature Store for the corresponding set of join keys. `_valid_to` will never be greater than `end_time`.
        Values for which `_valid_to` is equal to `end_time` may be valid beyond `end_time`.
        - By default, (i.e. `from_source=None`), this method fetches feature values from the Offline Store for
        Feature Views that have offline materialization enabled. Otherwise, this method computes feature values directly
        from the original data source.

        :param start_time: The inclusive start time of the time range to compute features for.
        :param end_time:  The exclusive end time of the time range to compute features for.
        :param max_lookback: [Non-Aggregate Feature Views Only] A performance optimization that configures how far back
        before start_time to look for events in the raw data. If set, `get_features_in_range()` may not include all
        entities with valid feature values in the specified time range, but `get_features_in_range()` will never
        return invalid values.
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :param from_source: Whether feature values should be recomputed from the original data source. If None,
        feature values will be fetched from the Offline Store for Feature Views that have offline materialization enabled
        and otherwise computes feature values on the fly from raw data. Use `from_source=True` to force computing from raw
        data and `from_source=False` to error if any Feature Views are not materialized.
        :param compute_mode: Compute mode to use to produce the data frame. Examples include `spark` and `rift`.
        :param mock_inputs: Mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the Feature View's function parameters. For Feature Views with multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.
        :return: A TectonDataFrame with Feature Values for the requested time range in the format specified above.
        """
        compute_mode = offline_retrieval_compute_mode(compute_mode)
        if compute_mode != ComputeMode.SPARK and compute_mode != ComputeMode.RIFT:
            raise errors.GET_FEATURES_IN_RANGE_UNSUPPORTED

        self._validate_start_and_end_times(start_time, end_time)

        sources = self._check_can_query_from_source(from_source)
        sources.display()

        feature_definition = self._feature_definition

        dialect = compute_mode.default_dialect()

        mock_data_sources = {}
        mock_context = None
        if mock_inputs:
            mock_context, mock_data_sources = _get_mock_context_and_sources(
                mock_inputs, dialect, compute_mode, feature_definition
            )

        return querytree_api.get_features_from_params(
            GetFeaturesInRangeParams(
                fco=feature_definition,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                max_lookback=max_lookback,
                from_source=from_source,
                compute_mode=compute_mode,
                mock_data_sources=mock_data_sources,
                mock_context=mock_context,
                skew_config=kwargs.get("skew_config"),
            )
        )

    @sdk_decorators.sdk_public_method
    def get_features_for_events(
        self,
        events: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **kwargs,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature view.

        By default (i.e. `from_source=None`), this method fetches feature values from the Offline Store for Feature
        Views that have offline materialization enabled and otherwise computes feature values on the fly from raw data.

        :param events: A `DataFrame` containing all possible join key combinations and timestamps specifying which feature values to fetch. The returned DataFrame includes rollups for all (join key, timestamp) combinations necessary to compute a complete dataset. To differentiate between event columns and feature columns, feature columns are labeled as feature_view_name.feature_name in the returned `DataFrame`.
        :param timestamp_key: Name of the time column in the `events` `DataFrame`. This method will fetch the latest features computed before the specified timestamps in this column. If unspecified, will default to the time column of the `events` `DataFrame` if there is only one present. If more than one time column is present in the `events` `DataFrame`, you must specify which column you would like to use.
        :param from_source: Whether feature values should be recomputed from the original data source. If `None`,
            feature values will be fetched from the Offline Store for Feature Views that have offline materialization
            enabled and otherwise computes feature values on the fly from raw data. Use `from_source=True` to force
            computing from raw data and `from_source=False` to error if any Feature Views are not materialized.
            Defaults to None.
        :param mock_inputs: Mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the Feature View's function parameters. For Feature Views with multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.
        :param compute_mode: Compute mode to use to produce the data frame. Valid examples include `spark` and `rift`.

        :return: A `TectonDataFrame`.
        """
        compute_mode = offline_retrieval_compute_mode(compute_mode)
        dialect = compute_mode.default_dialect()
        if compute_mode == ComputeMode.ATHENA:
            raise errors.GET_FEATURES_FOR_EVENTS_UNSUPPORTED

        sources = self._check_can_query_from_source(from_source)
        sources.display()

        feature_definition = self._feature_definition

        mock_data_sources = {}
        mock_context = None
        if mock_inputs:
            mock_context, mock_data_sources = _get_mock_context_and_sources(
                mock_inputs, dialect, compute_mode, feature_definition
            )

        return querytree_api.get_features_from_params(
            GetFeaturesForEventsParams(
                fco=self._feature_definition,
                events=events,
                timestamp_key=timestamp_key,
                from_source=from_source,
                compute_mode=compute_mode,
                mock_data_sources=mock_data_sources,
                mock_context=mock_context,
                skew_config=kwargs.get("skew_config"),
            )
        )

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message is split conditionally depending on whether a spine is provided.
    )
    # if spine is provided, then timestamp_key is optional, but start_time, end_time, and entities cannot be used
    @overload
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message is split conditionally depending on whether a spine is provided.
    )
    # if spine not provided, then timestamp_key should also not be provided.
    # start_time, end_time, and entities can be used instead.
    @overload
    def get_historical_features(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message is split conditionally depending on whether a spine is provided.
    )
    @sdk_decorators.sdk_public_method
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str]] = None,
        timestamp_key: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature view.

        By default (i.e. `from_source=None`), this method fetches feature values from the Offline Store for Feature
        Views that have offline materialization enabled and otherwise computes feature values on the fly from raw data.

        If no arguments are passed in, all feature values for this feature view will be returned in a Tecton DataFrame.

        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in the spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
            If more than one time column is present in the spine, you must specify which column you'd like to use.
        :type timestamp_key: str
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: datetime.datetime
        :param end_time: The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: datetime.datetime
        :param entities: Filter feature data returned to a set of entity IDs.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param from_source: Whether feature values should be recomputed from the original data source. If `None`,
            feature values will be fetched from the Offline Store for Feature Views that have offline materialization
            enabled and otherwise computes feature values on the fly from raw data. Use `from_source=True` to force
            computing from raw data and `from_source=False` to error if any Feature Views are not materialized.
            Defaults to None.
        :type from_source: bool
        :param mock_inputs: Mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the Feature View's function parameters. For Feature Views with multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]]
        :param compute_mode: Compute mode to use to produce the data frame. Valid examples include `spark` and `rift`.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A `TectonDataFrame`.
        """
        sources = self._check_can_query_from_source(from_source)
        sources.display()

        # We need a validated feature definition to check that it has an offset window
        if self._feature_definition.has_offset_window and spine is None:
            logger.warning(
                "Calling get_historical_features() with a specified time range on a feature view that has an offset "
                "aggregation will not return all features. Please use get_features_in_range() to return all features in"
                "a specified time range."
            )

        # if spine is not provided, timestamp_key cannot be set
        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        # start_time, end_time, and entities are incompatible with spine
        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        # late-arriving data functionality is not supported for get_historical_features
        if self._feature_definition.batch_publish_timestamp is not None:
            msg = "`get_historical_features()` method does not support late-arriving data. Please use `get_features_for_events()` or `get_features_in_range` instead."
            raise TectonValidationError(msg)

        self._validate_start_and_end_times(start_time, end_time)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
            if self.info.workspace is None or not self._feature_definition.materialization_enabled:
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE
            if mock_inputs:
                raise errors.ATHENA_COMPUTE_MOCK_SOURCES_UNSUPPORTED
            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                feature_set_config=self._construct_feature_set_config(),
            )

        dialect = compute_mode.default_dialect()
        mock_data_sources = {}

        feature_definition = self._feature_definition

        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.get_historical_features_for_feature_definition(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition=feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
            mock_data_sources=mock_data_sources,
        )

    @sdk_decorators.sdk_public_method
    def get_partial_aggregates(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """
        Returns the partially aggregated tiles in between `start_time` and `end_time` for a Feature View that uses the Tecton Aggregation Engine.

        :param start_time: The start time of the time window to fetch partial aggregates for. The start_time will fall
        in the time interval of the first tile that is returned.
        :type start_time: datetime.datetime
        :param end_time: The end time of the time window to fetch partial aggregates for. The end_time will fall in the
        time interval of the last tile that is returned.
        :param mock_inputs: Mock sources that should be used instead of fetching directly from raw data
        sources. The keys of the dictionary should match the Feature View's function parameters. For feature views with
        multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame, MockContext]]]
        :param entities: A DataFrame that is used to filter down feature values. If specified, this DataFrame should only
        contain join key columns.
        :type entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]]
        :param from_source: Whether feature values should be recomputed from the original data source. If ``None``,
            input feature values will be fetched from the Offline Store for Feature Views that have offline
            materialization enabled and otherwise computes feature values on the fly from raw data. Use
            ``from_source=True`` to force computing from raw data and ``from_source=False`` to error if any input
            Feature Views are not materialized. Defaults to None.
        :type from_source: bool
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A Tecton DataFrame with partially aggregated feature values and the _interval_start_time and
        _interval_end_time columns for each partial aggregation.
        """
        sources = self._check_can_query_from_source(from_source)
        sources.display()

        if start_time is None or end_time is None:
            msg = "get_partial_aggregates() requires start_time and end_time to be set."
            raise TectonValidationError(msg)

        self._validate_start_and_end_times(start_time, end_time)

        feature_definition = self._feature_definition

        if not feature_definition.is_temporal_aggregate:
            raise errors.GET_PARTIAL_AGGREGATES_UNSUPPORTED_NON_AGGREGATE

        if feature_definition.compaction_enabled:
            raise errors.GET_PARTIAL_AGGREGATES_UNSUPPORTED_COMPACTED

        if feature_definition.is_continuous:
            raise errors.GET_PARTIAL_AGGREGATES_UNSUPPORTED_CONTINUOUS()

        if any(ds.data_source_type == DataSourceType.PUSH_NO_BATCH for ds in self.sources):
            msg = "The `get_partial_aggregates()` method is currently unsupported for Feature Views that are backed by a PushSource without a batch_config."
            raise TectonValidationError(msg)

        if entities is not None:
            if not isinstance(entities, TectonDataFrame):
                entities = TectonDataFrame._create(entities)
            if not set(entities._dataframe.columns).issubset(set(feature_definition.join_keys)):
                msg = f"Entities should only contain columns that can be used as Join Keys: {feature_definition.join_keys}"
                raise TectonValidationError(msg)

        compute_mode = offline_retrieval_compute_mode(compute_mode)
        dialect = compute_mode.default_dialect()

        mock_data_sources = {}
        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.get_partial_aggregates(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition=feature_definition,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            mock_data_sources=mock_data_sources,
            from_source=from_source,
        )

    @sdk_decorators.sdk_public_method
    def run_transformation(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Run the FeatureView Transformation as is without any aggregations or joins. Supports transforming data directly from raw data sources or using mock data.

        To run the feature view transformation with data from raw data sources, the environment must have access to the data sources.

        :param start_time: The start time of the time window to materialize.
        :type start_time: datetime.datetime
        :param end_time: The end time of the time window to materialize.
        :type end_time: datetime.datetime
        :param mock_inputs: Mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the Feature View's function parameters. For Feature Views with multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]]
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A tecton DataFrame of the results.
        """
        feature_definition = self._feature_definition

        if any(ds.data_source_type == DataSourceType.PUSH_NO_BATCH for ds in self.sources) and len(mock_inputs) == 0:
            msg = "The `run_transformation()` method is currently unsupported for Feature Views backed by a StreamSource without a batch_config unless mock_inputs are provided."
            raise TectonValidationError(msg)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode != ComputeMode.SPARK and compute_mode != ComputeMode.RIFT:
            raise errors.RUN_TRANSFORMATION_UNSUPPORTED

        if start_time is None or end_time is None:
            msg = "run_transformation() requires start_time and end_time to be set."
            raise TypeError(msg)

        self._validate_start_and_end_times(start_time, end_time)

        time_range = end_time - start_time
        if (
            feature_definition.is_incremental_backfill
            and time_range != feature_definition.batch_materialization_schedule
        ):
            logger.warning(
                f"run_transformation() time range ({start_time}, {end_time}) is not equivalent to the batch_schedule: {feature_definition.batch_materialization_schedule}. This may lead to incorrect feature values since feature views with incremental_backfills typically implicitly rely on the materialization range being equivalent to the batch_schedule."
            )

        dialect = compute_mode.default_dialect()

        mock_data_sources = {}
        mock_context = None
        if mock_inputs:
            mock_context, mock_data_sources = _get_mock_context_and_sources(
                mock_inputs, dialect, compute_mode, feature_definition
            )

        return querytree_api.run_transformation_batch(
            dialect,
            compute_mode,
            feature_definition,
            start_time,
            end_time,
            mock_data_sources,
            mock_context=mock_context,
        )

    @deprecated(
        version="0.9",
        reason="`run()` is replaced by `run_transformation()`, `get_partial_aggregates()`, and `get_features_in_range()`.",
        warning_message=None,  # warning message is split conditionally depending on what aggregation_level is provided
    )
    @sdk_decorators.sdk_public_method
    def run(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        aggregation_level: Optional[str] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **mock_inputs_kwargs: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> TectonDataFrame:
        r"""Run the FeatureView. Supports transforming data directly from raw data sources or using mock data.

        To run the feature view with data from raw data sources, the environment must have access to the data sources.

        :param start_time: The start time of the time window to materialize.
        :param end_time: The end time of the time window to materialize.
        :param aggregation_level: For feature views with aggregations, `aggregation_level` configures which stage of
            the aggregation to run up to. The query for Aggregate Feature Views operates in three steps:

            1) The feature view query is run over the provided time range. The user defined transformations are applied over the data source.

            2) The result of #1 is aggregated into tiles the size of the aggregation_interval.

            3) The tiles from #2 are combined to form the final feature values. The number of tiles that are combined is based off of the time_window of the aggregation.

            For testing and debugging purposes, to see the output of #1, use `aggregation_level="disabled"`.
            For #2, use `aggregation_level="partial"`.
            For #3, use `aggregation_level="full"`.
            `aggregation_level="full"` is the default behavior if `aggregation_level` is not explicitly specified.


        :param mock_inputs: Mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the Feature View's function parameters. For Feature Views with multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame, MockContext]]]

        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :param mock_inputs_kwargs: Keyword arguments for mock sources that should be used instead of fetching directly from raw data
            sources. The keys should match the Feature View's function parameters. For Feature Views with multiple sources, mocking some data sources and using raw data for others is supported. Using `mock_inputs` is incompatible with `from_source=False`.

        :return: A tecton DataFrame of the results.
        """
        if mock_inputs:
            resolved_mock_inputs = mock_inputs
            if len(mock_inputs_kwargs) > 0:
                msg = "Mock sources cannot be configured using both the mock_inputs dictionary and using the kwargs to the `run` call."
                raise TectonValidationError(msg)
        else:
            resolved_mock_inputs = mock_inputs_kwargs

        if (
            any(ds.data_source_type == DataSourceType.PUSH_NO_BATCH for ds in self.sources)
            and len(resolved_mock_inputs) == 0
        ):
            msg = "The `run()` method is currently unsupported for Feature Views backed by a StreamSource without a batch_config unless mock_inputs are provided."
            raise TectonValidationError(msg)

        if start_time is None or end_time is None:
            msg = "run() requires start_time and end_time to be set."
            raise TypeError(msg)

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        feature_definition = self._feature_definition

        if feature_definition.is_temporal and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        if feature_definition.compaction_enabled and aggregation_level == run_api_consts.AGGREGATION_LEVEL_PARTIAL:
            raise errors.RUN_API_PARTIAL_LEVEL_UNSUPPORTED_FOR_COMPACTION

        aggregation_level = run_api.validate_and_get_aggregation_level(feature_definition, aggregation_level)

        run_api.maybe_warn_incorrect_time_range_size(feature_definition, start_time, end_time, aggregation_level)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        dialect = compute_mode.default_dialect()

        mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
            dialect, compute_mode, feature_definition, resolved_mock_inputs
        )

        return run_api.run_batch(
            dialect,
            compute_mode,
            feature_definition,
            start_time,
            end_time,
            mock_data_sources,
            aggregation_level=aggregation_level,
        )

    @deprecated(
        version="0.9",
        reason="`test_run()` is replaced by `run_transformation()`, `get_partial_aggregates()`, and `get_features_in_range()`.",
        warning_message=None,  # warning message is split conditionally depending on what aggregation_level is provided
    )
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_local_object(error_message=errors.CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT)
    def test_run(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        aggregation_level: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **mock_inputs: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> TectonDataFrame:
        r"""Run the FeatureView using mock data sources. This requires a local spark session.

        Unlike `run`, `test_run` is intended for unit testing. It will not make calls to your
        connected Tecton cluster or attempt to read real data.

        :param start_time: The start time of the time window to materialize.
        :param end_time: The end time of the time window to materialize.
        :param aggregation_level: For feature views with aggregations, `aggregation_level` configures what stage of the aggregation to run up to.

            The query for Aggregate Feature Views operates in three logical steps:
            1) The feature view query is run over the provided time range. The user defined transformations are applied over the data source.

            2) The result of #1 is aggregated into tiles the size of the aggregation_interval.

            3) The tiles from #2 are combined to form the final feature values. The number of tiles that are combined is based off of the time_window of the aggregation.

            For testing and debugging purposes, to see the output of #1, use `aggregation_level="disabled"`. For #2, use

            `aggregation_level="partial"`. For #3, use `aggregation_level="full"`.

        :param compute_mode: Compute mode to use to produce the data frame.

        :param mock_inputs: Keyword arguments with expected same keys as the FeatureView's inputs parameter. Each input name
            maps to a Spark DataFrame that should be evaluated for that node in the pipeline.

        :return: A `tecton.TectonDataFrame` object.
        """
        with conf._temporary_set("TECTON_SKIP_OBJECT_VALIDATION", True):
            return self.run(
                start_time=start_time,
                end_time=end_time,
                aggregation_level=aggregation_level,
                compute_mode=compute_mode,
                mock_inputs=mock_inputs,
            )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, numpy.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """Returns a single Tecton `tecton.FeatureVector` from the Online Store.

        :param join_keys: The join keys to fetch from the online store.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.

        :return: A `tecton.FeatureVector` of the results.
        """
        if not self._feature_definition.writes_to_online_store:
            msg = "get_online_features"
            raise errors.UNSUPPORTED_OPERATION(msg, "online=True is not set for this FeatureView.")

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @property
    @sdk_decorators.sdk_public_method
    def feature_start_time(self) -> Optional[datetime.datetime]:
        return self._spec.feature_start_time

    @property
    @sdk_decorators.sdk_public_method
    def batch_trigger(self) -> BatchTriggerType:
        """The `BatchTriggerType` for this FeatureView."""
        batch_trigger = self._spec.batch_trigger

        return BatchTriggerType(batch_trigger)

    @property
    def is_batch_trigger_manual(self) -> bool:
        """Whether this Feature View's batch trigger is `BatchTriggerType.Manual`."""
        return self.batch_trigger == BatchTriggerType.MANUAL

    @sdk_decorators.sdk_public_method
    def get_timestamp_field(self) -> str:
        """Returns the name of the timestamp field for this Feature View."""
        return self._spec.timestamp_field

    @property
    def batch_publish_timestamp(self) -> Optional[str]:
        """Returns the batch publish timestamp for this Feature View."""
        if not isinstance(self._spec, MaterializedFeatureViewSpec):
            msg = "Cannot access batch_publish_timestamp for non-MaterializedFeatureView"
            raise TectonValidationError(msg)
        return self._spec.batch_publish_timestamp

    @property
    @sdk_decorators.sdk_public_method
    def batch_schedule(self) -> Optional[datetime.timedelta]:
        """The batch schedule of this Feature View."""
        return self._spec.batch_schedule

    @property
    @sdk_decorators.sdk_public_method
    def aggregations(self) -> List[configs.Aggregation]:
        """List of `Aggregation` configs used by this Feature View."""
        aggregate_features = self._spec.aggregate_features

        # Note that this isn't exactly what the user provided, functions like last(3) are returned as 'lastn'.
        aggregation_list = []
        for agg in aggregate_features:
            time_window_spec = create_time_window_spec_from_data_proto(agg.time_window)
            if isinstance(time_window_spec, TimeWindowSeriesSpec):
                time_window = configs.TimeWindowSeries(
                    series_start=time_window_spec.window_series_start,
                    series_end=time_window_spec.window_series_end,
                    step_size=time_window_spec.step_size,
                    window_size=time_window_spec.window_duration,
                )
            elif isinstance(time_window_spec, RelativeTimeWindowSpec):
                time_window = configs.TimeWindow(
                    window_size=time_window_spec.window_duration, offset=time_window_spec.offset
                )
            elif isinstance(time_window_spec, LifetimeWindowSpec):
                time_window = configs.LifetimeWindow()
            else:
                msg = f"Unexpected time window type: {type(time_window_spec)}"
                raise ValueError(msg)

            aggregation_list.append(
                configs.Aggregation(
                    column=agg.input_feature_name,
                    function=aggregation_utils.get_aggregation_function_name(agg.function),
                    time_window=time_window,
                    name=agg.output_feature_name,
                    description=get_field_or_none(agg, "description"),
                    tags=dict(agg.tags) if agg.tags else None,
                )
            )

        return aggregation_list

    @property
    @sdk_decorators.sdk_public_method
    def max_source_data_delay(self) -> datetime.timedelta:
        """Returns the maximum data delay of input sources for this feature view."""
        return max([source.data_delay for source in self.sources]) or datetime.timedelta(0)

    @property
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def published_features_path(self) -> Optional[str]:
        """The location of published features in the offline store."""
        return self._feature_definition.published_features_path

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def delete_keys(
        self,
        keys: Union[pyspark_dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> List[str]:
        """Deletes any materialized data that matches the specified join keys from the FeatureView.

        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureView has multiple entities, the full set of join keys must be specified.
        Only supports Delta or Iceberg as the offline store (`offline_store=DeltaConfig()`).
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureView join keys.
        :param online: Whether or not to delete from the online store.
        :param offline: Whether or not to delete from the offline store.
        :return: List of job ids for jobs created for entity deletion.
        """
        is_live_workspace = internal_utils.is_live_workspace(self.info.workspace)
        if not is_live_workspace:
            msg = "delete_keys"
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(msg)

        return delete_keys_api.delete_keys(online, offline, keys, self._feature_definition)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def materialization_status(
        self, verbose: bool = False, limit: int = 1000, sort_columns: Optional[str] = None, errors_only: bool = False
    ) -> display.Displayable:
        """Displays materialization information for the FeatureView, which may include past jobs, scheduled jobs, and job failures.

        This method returns different information depending on the type of FeatureView.
        :param verbose: If set to true, method will display additional low level materialization information,
        useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return materialization_api.get_materialization_status_for_display(
            self._spec.id_proto, self.workspace, verbose, limit, sort_columns, errors_only
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.trigger_materialization_job)
    @sdk_decorators.assert_remote_object
    def trigger_materialization_job(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        online: bool,
        offline: bool,
        use_tecton_managed_retries: bool = True,
        overwrite: bool = False,
    ) -> str:
        return materialization_api.trigger_materialization_job(
            self.name, self.workspace, start_time, end_time, online, offline, use_tecton_managed_retries, overwrite
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.wait_for_materialization_job)
    @sdk_decorators.assert_remote_object
    def wait_for_materialization_job(
        self,
        job_id: str,
        timeout: Optional[datetime.timedelta] = None,
    ) -> materialization_api.MaterializationJob:
        return materialization_api.wait_for_materialization_job(
            workspace=self.workspace, job_id=job_id, feature_view=self.name, timeout=timeout
        )

    @property
    def aggregation_interval(self) -> Optional[datetime.timedelta]:
        """How frequently the feature values are updated"""
        return self._spec.slide_interval

    @property
    def aggregation_secondary_key(self) -> Optional[str]:
        """Configures secondary key aggregates using the set column."""
        return self._spec.aggregation_secondary_key

    @property
    def compaction_enabled(self) -> bool:
        """(Private preview) Runs compaction job post-materialization; requires Dynamo and ImportTable API."""
        return self._spec.compaction_enabled

    @property
    def online(self) -> bool:
        """Whether the Feature View is materialized to the online feature store."""
        return self._spec.online

    @property
    def offline(self) -> bool:
        """Whether the Feature View is materialized to the offline feature store."""
        return self._spec.offline

    @property
    def ttl(self) -> Duration:
        """The TTL (or look back window) for features defined by this Feature View. This parameter determines how
        long features will live in the online store and how far to look back relative to a training example's
        timestamp when generating offline training sets.
        """
        return self._spec.ttl

    @property
    def manual_trigger_backfill_end_time(self) -> Optional[pendulum.datetime]:
        """If set, Tecton will schedule backfill materialization jobs for this Feature
        View up to this time.
        """
        return self._spec.manual_trigger_backfill_end_time

    @property
    def timestamp_field(self) -> Optional[str]:
        return self._spec.timestamp_field

    @property
    def _options(self) -> Mapping[str, str]:
        """
        Additional options to configure the Feature View. Used for advanced use cases and beta features.
        """
        return self._spec.options

    @property
    def context_parameter_name(self) -> Optional[str]:
        """
        Name of the function parameter that Tecton injects MaterializationContext object to.
        """
        return self._spec.context_parameter_name

    @property
    def incremental_backfills(self) -> bool:
        """
        Backfills incrementally from feature_start_time to current time, one interval at a time
        """
        return self._spec.incremental_backfills

    @property
    def offline_store(
        self,
    ) -> Optional[Union[configs.DeltaConfig, configs.ParquetConfig, vnext.IcebergConfig]]:
        """Configuration for the Offline Store of this Feature View."""
        offline_feature_store = self._spec.offline_store
        if offline_feature_store.HasField("delta"):
            staging_config = configs.DeltaConfig
        elif offline_feature_store.HasField("parquet"):
            staging_config = configs.ParquetConfig
        elif offline_feature_store.HasField("iceberg"):
            staging_config = vnext.IcebergConfig
        else:
            return None

        return staging_config.from_proto(offline_feature_store)

    @property
    def monitor_freshness(self) -> bool:
        """
        If true, enables monitoring when feature data is materialized to the online feature store.
        """
        return self._spec.monitor_freshness

    @property
    def expected_feature_freshness(self) -> Optional[pendulum.Duration]:
        """
        Threshold used to determine if recently materialized feature data is stale.
        """
        return self._spec.expected_feature_freshness

    @property
    def alert_email(self) -> Optional[str]:
        """
        Email that alerts for this FeatureView will be sent to.
        """
        return self._spec.alert_email

    @property
    def max_backfill_interval(self) -> Optional[pendulum.Duration]:
        """
        (Advanced) The time interval for which each backfill job will run to materialize feature data. This affects the number of backfill jobs that will run,
        which is (`<feature registration time>` - `feature_start_time`) / `max_backfill_interval`. Configuring the `max_backfill_interval` parameter appropriately
        will help to optimize large backfill jobs. If this parameter is not specified, then 10 backfill jobs will run (the default).
        """
        return self._spec.max_backfill_interval

    @property
    def tecton_materialization_runtime(self) -> Optional[str]:
        """
        Version of `tecton` package used by your job cluster.
        """
        return self._spec.tecton_materialization_runtime

    @property
    def cache_config(self) -> Optional[configs.CacheConfig]:
        """
        Uses cache for Feature View if online caching is enabled.
        """
        cache_config_proto = self._spec.cache_config
        if cache_config_proto:
            return configs.CacheConfig.from_proto(cache_config_proto)
        return None

    @property
    def environment(self) -> Optional[str]:
        """
        The custom environment in which materialization jobs will be run. Defaults to `None`, which means jobs will execute in the default Tecton environment.
        """
        return self._spec.environment


def resolve_local_remote_model_artifact(
    inferences: List[feature_view__args_pb2.Inference],
) -> Tuple[Dict[str, model_artifact_data_pb2.ModelArtifactInfo], List[model_artifact_data_pb2.ModelArtifactInfo]]:
    model_artifact_map = {}
    # Local model artifacts that will be used (some local models may not be used if a model of that name exists remotely).
    # This list will be passed to the validation endpoint in MDS.
    local_models_used = []
    all_local_models = model_config._LOCAL_CUSTOM_MODELS

    for inference in inferences:
        remote_model_artifact = _fetch_model(inference.model)
        if inference.model not in all_local_models and not remote_model_artifact:
            msg = f"Model with name {inference.model} is not found remotely or locally."
            raise TectonValidationError(msg)
        elif inference.model not in all_local_models:
            model_artifact_map[inference.model] = remote_model_artifact
        else:
            if remote_model_artifact:
                print(
                    f"There is both a remote and local model with name {inference.model}, The local model will be used."
                )

            local_model_config = all_local_models[inference.model]
            local_model_artifact = model_artifact_data_pb2.ModelArtifactInfo(
                name=local_model_config.name,
                model_file_path=local_model_config.model_file,
                type=model_type_string_to_enum(local_model_config.model_type),
                description=local_model_config.description,
                tags=local_model_config.tags,
                input_schema=type_utils.to_tecton_schema(local_model_config.input_schema),
                output_schema=type_utils.to_tecton_schema([local_model_config.output_schema]),
                environments=local_model_config.environments,
            )
            model_artifact_map[local_model_config.name] = local_model_artifact
            local_models_used.append(local_model_artifact)
            # Load model into cache, overwrite old model in cache if needed.
            model_cache_dir, _ = _initialize_model_cache_dir(
                inference.model, local_model_config.model_file, force_overwrite=True
            )

            artifact_files = local_model_config.artifact_files or []
            all_files = [local_model_config.model_file, *artifact_files]
            for item in all_files:
                real_path = item
                if os.path.islink(item):
                    real_path = os.readlink(item)
                os.makedirs(os.path.join(model_cache_dir, os.path.dirname(item)), exist_ok=True)
                shutil.copy(real_path, os.path.join(model_cache_dir, item))

    return model_artifact_map, local_models_used


@attrs.define(eq=False)
class BatchFeatureView(MaterializedFeatureView):
    """A Tecton Batch Feature View, used for materializing features on a batch schedule from a BatchSource.

    The BatchFeatureView should not be instantiated directly, the `@batch_feature_view`
    decorator is recommended instead.

    Attributes:
        entities: The Entities for this Feature View.
        info: A dataclass containing basic info about this Tecton Object.
        sources: The Data Source inputs for this Feature View.
        transformations: The Transformations used by this Feature View.
    """

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Callable,
        sources: Sequence[Union[framework_data_source.BatchSource, FilteredSource]],
        entities: Sequence[framework_entity.Entity],
        mode: str,
        features: Sequence[feature.Feature],
        timestamp_field: str,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregation_secondary_key: Optional[str] = None,
        online: bool = False,
        offline: bool = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        lifetime_start_time: Optional[datetime.datetime] = None,
        manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
        batch_trigger: BatchTriggerType = BatchTriggerType.SCHEDULED,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[configs.ComputeConfigTypes] = None,
        offline_store: Optional[
            Union[
                configs.OfflineStoreConfig,
                configs.ParquetConfig,
                configs.DeltaConfig,
                vnext.IcebergConfig,
            ]
        ] = None,
        publish_features_config: Optional[vnext.PublishFeaturesConfig] = None,
        online_store: Optional[configs.OnlineStoreTypes] = None,
        monitor_freshness: bool = False,
        data_quality_enabled: Optional[bool] = None,
        skip_default_expectations: Optional[bool] = None,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        max_backfill_interval: Optional[datetime.timedelta] = None,
        incremental_backfills: bool = False,
        run_transformation_validation: Optional[bool] = None,
        options: Optional[Dict[str, str]] = None,
        tecton_materialization_runtime: Optional[str] = None,
        cache_config: Optional[configs.CacheConfig] = None,
        compaction_enabled: bool = False,
        environment: Optional[str] = None,
        context_parameter_name: Optional[str] = None,
        secrets: Optional[Dict[str, Union[Secret, str]]] = None,
        resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
    ):
        _validate_fv_function_inputs(sources, feature_view_function, context_parameter_name)
        _validate_features(features, name)

        if online_store is None:
            online_store = repo_config.get_batch_feature_view_defaults().online_store

        if offline_store is None:
            offline_store = repo_config.get_batch_feature_view_defaults().offline_store_config
        elif isinstance(offline_store, (configs.DeltaConfig, configs.ParquetConfig, vnext.IcebergConfig)):
            offline_store = configs.OfflineStoreConfig(staging_table_format=offline_store)

        if batch_compute is None:
            batch_compute = repo_config.get_batch_feature_view_defaults().batch_compute
        _warn_if_emr_compute_uses_cluster_default_python(batch_compute)

        if tecton_materialization_runtime is None:
            tecton_materialization_runtime = (
                repo_config.get_batch_feature_view_defaults().tecton_materialization_runtime
            )

        pipeline_function = self._get_or_create_pipeline_function(
            name=name,
            mode=mode,
            description=description,
            owner=owner,
            tags=tags,
            feature_view_function=feature_view_function,
        )

        wrapped_sources = self._convert_data_sources_to_explicitly_filtered_objects(sources)
        pipeline_root = self._build_pipeline(
            name,
            feature_view_function,
            pipeline_function,
            wrapped_sources,
            context_parameter_name,
        )

        has_aggregates = any(isinstance(item, feature.Aggregate) for item in features)

        # TODO(deprecate_after=0.6): Batch Feature Views requiring a stream_processing_mode is a legacy of when
        # stream_processing_mode was called aggregation_mode (which existed in 0.6 and prior). Changing this would break
        # `tecton plan` for customers without some backend handling.
        stream_processing_mode = StreamProcessingMode.TIME_INTERVAL if has_aggregates else None
        if (
            environment is None
            and infer_batch_compute_mode(
                pipeline_root=pipeline_root, batch_compute_config=batch_compute, stream_compute_config=None
            )
            == BatchComputeMode.RIFT
        ):
            environment = repo_config.get_batch_feature_view_defaults().environment

        if isinstance(offline_store, configs.OfflineStoreConfig):
            assert not (offline_store.publish_full_features and publish_features_config), (
                "Publish Features cannot be enabled via `OfflineStoreConfig` and `PublishFeaturesConfig` at once, please use `PublishFeaturesConfig`."
            )

        args = _build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            prevent_destroy=prevent_destroy,
            pipeline_root=pipeline_root,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            publish_features_config=publish_features_config,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode,
            aggregation_secondary_key=aggregation_secondary_key,
            features=features,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            data_source_type=data_source_type_pb2.DataSourceType.BATCH,
            max_backfill_interval=max_backfill_interval,
            output_stream=None,
            incremental_backfills=incremental_backfills,
            run_transformation_validation=run_transformation_validation,
            options=options,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            compaction_enabled=compaction_enabled,
            environment=environment,
            context_parameter_name=context_parameter_name,
            framework_version=self._framework_version,
            secrets=secrets,
            resource_providers=resource_providers,
            timestamp_field=timestamp_field,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = tuple(source.source if isinstance(source, FilteredSource) else source for source in sources)

        source_info = construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
            resource_providers=tuple(resource_providers.values() if resource_providers else []),
            args_supplement=None,
        )

        inferences = list(args.materialized_feature_view_args.inferences)
        # Note: Creating the materialization schema for feature views with `Inference`
        # requires MDS access (because we need to fetch the output data type). If user
        # is using NDD we will fetch this. This also means that unit tests are not
        # supported.
        model_artifact_map = None
        local_models = None
        if len(inferences) > 0:
            model_artifact_map, local_models = resolve_local_remote_model_artifact(inferences)

        schemas = self._get_schemas(model_artifacts=model_artifact_map)
        self._args_supplement = self._get_args_supplement(schemas, model_artifact_map)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate(local_models=local_models)
        self._populate_spec()
        base_tecton_object._register_local_object(self)


@batch_feature_view_typechecked
def batch_feature_view(
    *,
    mode: str,
    sources: Sequence[Union[framework_data_source.BatchSource, FilteredSource]],
    entities: Sequence[framework_entity.Entity],
    features: Union[
        Sequence[feature.Aggregate], Sequence[Union[feature.Attribute, feature.Embedding, feature.Inference]]
    ],
    timestamp_field: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregation_secondary_key: Optional[str] = None,
    online: bool = False,
    offline: bool = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    lifetime_start_time: Optional[datetime.datetime] = None,
    manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
    batch_trigger: BatchTriggerType = BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[configs.ComputeConfigTypes] = None,
    offline_store: Optional[
        Union[
            configs.OfflineStoreConfig,
            configs.ParquetConfig,
            configs.DeltaConfig,
            vnext.IcebergConfig,
        ]
    ] = None,
    online_store: Optional[configs.OnlineStoreTypes] = None,
    publish_features_config: Optional[vnext.PublishFeaturesConfig] = None,
    monitor_freshness: bool = False,
    data_quality_enabled: Optional[bool] = None,
    skip_default_expectations: Optional[bool] = None,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    max_backfill_interval: Optional[datetime.timedelta] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    incremental_backfills: bool = False,
    run_transformation_validation: Optional[bool] = None,
    options: Optional[Dict[str, str]] = None,
    tecton_materialization_runtime: Optional[str] = None,
    cache_config: Optional[configs.CacheConfig] = None,
    batch_compaction_enabled: Optional[bool] = None,
    compaction_enabled: Optional[bool] = None,
    environment: Optional[str] = None,
    context_parameter_name: Optional[str] = None,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
):
    """Declare a Batch Feature View.

    :param mode: (Required) Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation mode ("spark_sql", "pyspark", "python", or "pandas").
    :param sources: (Required) The Data Source inputs to the Feature View.
    :param entities: (Required) The entities this Feature View is associated with.
    :param timestamp_field: (Required) The column name that refers to the timestamp for records that are produced by the
        feature view. This parameter is optional if exactly one column is a Timestamp type.
    :param features: (Required) A list of Attribute, Aggregate, and Embedding feature values managed by this Feature View.
    :param aggregation_interval: The size of the tiles for a particular feature view (for example, `"1h"` or `"6h"`). Only valid when using aggregations.
    :param aggregation_secondary_key: Configures secondary key aggregates using the set column. Only valid when using aggregations.
    :param online: Whether the feature view should be materialized to the online feature store.
    :param offline: Whether the feature view should be materialized to the offline feature store.
    :param ttl: The TTL (or "look back window") for features defined by this feature view. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
    :param feature_start_time: When materialization for this feature view should start from. (Required if `offline=True` or `online=True`)
    :param lifetime_start_time: The start time for what data should be included in a lifetime aggregate. (Required if using lifetime windows)
    :param batch_schedule: The interval at which batch materialization should be scheduled.
    :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
    :param batch_trigger: Defines the mechanism for initiating batch materialization jobs.
        One of `BatchTriggerType.SCHEDULED` or `BatchTriggerType.MANUAL`.
        The default value is `BatchTriggerType.SCHEDULED`, where Tecton will run materialization jobs based on the
        schedule defined by the `batch_schedule` parameter. If set to `BatchTriggerType.MANUAL`, then batch
        materialization jobs must be explicitly initiated by the user through either the Tecton SDK or Airflow operator.
    :param batch_compute: Configuration for the batch materialization cluster.
    :param offline_store: Configuration for how data is written to the offline feature store.
    :param publish_features_config: Configuration for how full features are published post-offline materialization.
    :param online_store: Configuration for how data is written to the online feature store.
    :param monitor_freshness: If true, enables monitoring when feature data is materialized to the online feature store.
    :param data_quality_enabled: If false, disables data quality metric computation and data quality dashboard.
    :param skip_default_expectations: If true, skips validating default expectations on the feature data.
    :param expected_feature_freshness: Threshold used to determine if recently materialized feature data is stale. Data is stale if `now - most_recent_feature_value_timestamp > expected_feature_freshness`. For feature views using Tecton aggregations, data is stale if `now - round_up_to_aggregation_interval(most_recent_feature_value_timestamp) > expected_feature_freshness`. Where `round_up_to_aggregation_interval()` rounds up the feature timestamp to the end of the `aggregation_interval`. Value must be at least 2 times `aggregation_interval`. If not specified, a value determined by the Tecton backend is used.
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :param description: A human readable description.
    :param owner: Typically the name or email of the Feature View's primary maintainer.
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be set to
        False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
        such as inadvertently deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
        that would trigger a recreation of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
        only enforced in live (i.e. non-dev) workspaces.
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param max_batch_aggregation_interval: Deprecated. Use max_backfill_interval instead, which has the exact same usage.
    :param max_backfill_interval: (Advanced) The time interval for which each backfill job will run to materialize
        feature data. This affects the number of backfill jobs that will run, which is
        (`<feature registration time>` - `feature_start_time`) / `max_backfill_interval`.
        Configuring the `max_backfill_interval` parameter appropriately will help to optimize large backfill jobs.
        If this parameter is not specified, then 10 backfill jobs will run (the default).
    :param incremental_backfills: If set to `True`, the feature view will be backfilled one interval at a time as
        if it had been updated "incrementally" since its feature_start_time. For example, if `batch_schedule` is 1 day
        and `feature_start_time` is 1 year prior to the current time, then the backfill will run 365 separate
        backfill queries to fill the historical feature data.
    :param manual_trigger_backfill_end_time: If set, Tecton will schedule backfill materialization jobs for this feature
        view up to this time. Materialization jobs after this point must be triggered manually. (This param is only valid
        to set if batch_trigger is MANUAL.)
    :param options: Additional options to configure the Feature View. Used for advanced use cases and beta features.
    :param run_transformation_validation: If `True`, Tecton will execute the Feature View transformations during tecton plan/apply
        validation. If `False`, then Tecton will not execute the transformations during validation. Skipping query validation can be useful to speed up tecton plan/apply or for Feature Views that have issues
        with Tecton's validation (e.g. some pip dependencies). defaults to `True` for Spark and Snowflake Feature Views and
        `False` for Python and Pandas Feature Views.
    :param tecton_materialization_runtime: Version of `tecton` package used by your job cluster.
    :param cache_config: Cache config for the Feature View. Including this option enables the feature server to use the cache
        when retrieving features for this feature view. Will only be respected if the feature service containing this feature
        view has `enable_online_caching` set to `True`.
    :param batch_compaction_enabled: Deprecated: Please use `compaction_enabled` instead which has the exact same usage.
    :param compaction_enabled: (Private preview) If `True`, Tecton will run a compaction job after each batch
        materialization job to write to the online store. This requires the use of Dynamo and uses the ImportTable API.
        Because each batch job overwrites the online store, a larger compute cluster may be required.
    :param environment: The custom environment in which materialization jobs will be run. Defaults to `None`, which means
        jobs will execute in the default Tecton environment.
    :param context_parameter_name: Name of the function parameter that Tecton injects MaterializationContext object to.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the transformation function at runtime. During local development and testing, strings may be used instead Secret references.
    :param resource_providers: A dictionary of Resource providers that will be evaluated and resources will be provided to transformation function at runtime.

    :return: An object of type `BatchFeatureView`
    """
    # TODO(deprecate_after=0.8): This warning can be completely removed in 0.9, so it can be deleted once the 0.8 branch is cut.
    if max_batch_aggregation_interval is not None:
        msg = "FeatureView.max_batch_aggregation_interval is deprecated and is no longer supported in 0.8. Please use max_backfill_interval instead. max_backfill_interval has the same semantics and is just a new name."
        raise ValueError(msg)

    if batch_compaction_enabled is not None and compaction_enabled is not None:
        msg = "FeatureView.batch_compaction_enabled is deprecated. Please use compaction_enabled instead. compaction_enabled has the same semantics and is just a new name."
        raise TectonValidationError(msg)
    compaction_enabled = compaction_enabled or batch_compaction_enabled or False

    def decorator(feature_view_function):
        return BatchFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            feature_view_function=feature_view_function,
            mode=mode,
            sources=sources,
            entities=entities,
            aggregation_interval=aggregation_interval,
            aggregation_secondary_key=aggregation_secondary_key,
            features=features,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            offline_store=offline_store,
            publish_features_config=publish_features_config,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            timestamp_field=timestamp_field,
            max_backfill_interval=max_backfill_interval,
            incremental_backfills=incremental_backfills,
            run_transformation_validation=run_transformation_validation,
            options=options,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            compaction_enabled=compaction_enabled,
            environment=environment,
            context_parameter_name=context_parameter_name,
            secrets=secrets,
            resource_providers=resource_providers,
        )

    return decorator


@attrs.define(eq=False)
class StreamFeatureView(MaterializedFeatureView):
    """A Tecton Stream Feature View, used for transforming and materializing features from a StreamSource.

    If a Stream Feature View must change or transform the input source data, then a function decorated with
    `@stream_feature_view` is recommended. If the source data does not need to be transformed, then
    using the StreamFeatureView class directly is recommended and considered idiomatic.

    Attributes:
        entities: The Entities for this Feature View.
        info: A dataclass containing basic info about this Tecton Object.
        sources: The Source inputs for this Feature View.
        transformations: The Transformations used by this Feature View.
    """

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Optional[Callable] = None,
        source: Union[framework_data_source.StreamSource, FilteredSource],
        entities: Sequence[framework_entity.Entity],
        # TODO(FE-2368): Default mode to NO_TRANSFORMATION_MODE in constructor
        mode: Optional[str] = None,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregation_secondary_key: Optional[str] = None,
        aggregation_leading_edge: AggregationLeadingEdge = AggregationLeadingEdge.UNSPECIFIED,
        features: Sequence[feature.Feature],
        timestamp_field: str,
        stream_processing_mode: Optional[StreamProcessingMode] = None,
        online: bool = False,
        offline: bool = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        lifetime_start_time: Optional[datetime.datetime] = None,
        manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
        batch_trigger: BatchTriggerType = None,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[configs.ComputeConfigTypes] = None,
        stream_compute: Optional[configs.ComputeConfigTypes] = None,
        offline_store: Optional[
            Union[
                configs.OfflineStoreConfig,
                configs.ParquetConfig,
                configs.DeltaConfig,
                vnext.IcebergConfig,
            ]
        ] = None,
        publish_features_config: Optional[vnext.PublishFeaturesConfig] = None,
        online_store: Optional[configs.OnlineStoreTypes] = None,
        monitor_freshness: bool = False,
        data_quality_enabled: Optional[bool] = None,
        skip_default_expectations: Optional[bool] = None,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        max_backfill_interval: Optional[datetime.timedelta] = None,
        output_stream: Optional[configs.OutputStream] = None,
        run_transformation_validation: Optional[bool] = None,
        options: Optional[Dict[str, str]] = None,
        tecton_materialization_runtime: Optional[str] = None,
        cache_config: Optional[configs.CacheConfig] = None,
        compaction_enabled: bool = False,
        stream_tiling_enabled: bool = False,
        environment: Optional[str] = None,
        transform_server_group: Optional[str] = None,
        context_parameter_name: Optional[str] = None,
        secrets: Optional[Dict[str, Union[Secret, str]]] = None,
        resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
    ):
        """Construct a StreamFeatureView.

        `init` should not be used directly, and instead `@stream_feature_view` decorator is recommended.

        :param transform_server_group: The server group to use for running the transformation function.
        :param resource_providers: A dictionary mapping string names to ResourceProviders that will be available during feature transformation.
        """
        _validate_features(features, name)

        if online_store is None:
            online_store = repo_config.get_stream_feature_view_defaults().online_store

        if offline_store is None:
            offline_store = repo_config.get_stream_feature_view_defaults().offline_store_config
        elif isinstance(offline_store, (configs.DeltaConfig, configs.ParquetConfig, vnext.IcebergConfig)):
            offline_store = configs.OfflineStoreConfig(staging_table_format=offline_store)
            assert not (offline_store.publish_full_features and publish_features_config), (
                "Publish Features cannot be enabled via `OfflineStoreConfig` and `PublishFeaturesConfig` at once, please use `PublishFeaturesConfig`."
            )

        if batch_compute is None:
            batch_compute = repo_config.get_stream_feature_view_defaults().batch_compute
        _warn_if_emr_compute_uses_cluster_default_python(batch_compute)

        if tecton_materialization_runtime is None:
            tecton_materialization_runtime = (
                repo_config.get_stream_feature_view_defaults().tecton_materialization_runtime
            )

        data_source = source.source if isinstance(source, FilteredSource) else source
        if aggregation_leading_edge == AggregationLeadingEdge.UNSPECIFIED:
            # Default for all newly created stream feature views in sdk version >= 1.0.0.
            # If the feature view is a stream feature view updated from any sdk version < 1.0.0, the server side
            # validation will fail because it will not allow the feature view to be upgraded to use `WALL_CLOCK_TIME`
            # immediately.
            aggregation_leading_edge_default = repo_config.get_stream_feature_view_defaults().aggregation_leading_edge
            if aggregation_leading_edge_default == configs.LatestEventTime:
                aggregation_leading_edge = AggregationLeadingEdge.LATEST_EVENT_TIME
            else:
                aggregation_leading_edge = AggregationLeadingEdge.WALL_CLOCK_TIME

        data_source_type = data_source.data_source_type

        has_push_source = data_source_type in {
            data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        }

        if stream_compute is None and not has_push_source:
            # The stream compute default should not be applied for Stream Feature Views with Push Sources, since they
            # don't have any stream compute.
            stream_compute = repo_config.get_stream_feature_view_defaults().stream_compute

        _validate_fv_function_inputs([source], feature_view_function, context_parameter_name)

        if stream_processing_mode is None:
            stream_processing_mode_ = _compute_default_stream_processing_mode(
                has_push_source,
                features,
                compaction_enabled,
                stream_tiling_enabled,
            )
        else:
            stream_processing_mode_ = stream_processing_mode

        wrapped_sources = self._convert_data_sources_to_explicitly_filtered_objects([source])
        if feature_view_function:
            pipeline_function = self._get_or_create_pipeline_function(
                name=name,
                mode=mode,
                description=description,
                owner=owner,
                tags=tags,
                feature_view_function=feature_view_function,
            )
            pipeline_root = self._build_pipeline(
                name, feature_view_function, pipeline_function, wrapped_sources, context_parameter_name
            )
        else:
            pipeline_root = _source_to_pipeline_node(source=wrapped_sources[0], input_name=data_source.name)

        if data_source_type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            default_batch_trigger = BatchTriggerType.NO_BATCH_MATERIALIZATION
        else:
            default_batch_trigger = BatchTriggerType.SCHEDULED

        batch_trigger_ = batch_trigger or default_batch_trigger

        # Use stream source's transform_server_group as default if not specified
        if transform_server_group is None:
            stream_source = source.source if isinstance(source, FilteredSource) else source
            if (
                hasattr(stream_source, "_args")
                and hasattr(stream_source._args, "push_config")
                and hasattr(stream_source._args.push_config, "transform_server_group")
                and stream_source._args.push_config.transform_server_group
            ):
                # For push sources, transform_server_group is in PushSourceArgs
                transform_server_group = stream_source._args.push_config.transform_server_group

        if (
            infer_batch_compute_mode(
                pipeline_root=pipeline_root, batch_compute_config=batch_compute, stream_compute_config=stream_compute
            )
            == BatchComputeMode.RIFT
        ):
            # TODO(Rt-Data): Remove support for top-level `environment` parameter for Stream Feature Views once TSGs are GA
            msg = "The `environment` parameter is deprecated for Stream Feature Views. Please use the `transform_server_group` parameter instead to configure the Transform Server Group from which the environment will be inferred."
            if environment is not None:
                raise TectonValidationError(msg)
            environment = repo_config.get_stream_feature_view_defaults().environment

        args = _build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            prevent_destroy=prevent_destroy,
            pipeline_root=pipeline_root,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            publish_features_config=publish_features_config,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode_,
            aggregation_secondary_key=aggregation_secondary_key,
            features=features,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger_,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            data_source_type=data_source_type,
            max_backfill_interval=max_backfill_interval,
            output_stream=output_stream,
            incremental_backfills=False,
            run_transformation_validation=run_transformation_validation,
            options=options,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            stream_tiling_enabled=stream_tiling_enabled,
            compaction_enabled=compaction_enabled,
            environment=environment,
            transform_server_group=transform_server_group,
            context_parameter_name=context_parameter_name,
            aggregation_leading_edge=aggregation_leading_edge,
            framework_version=self._framework_version,
            secrets=secrets,
            resource_providers=resource_providers,
            timestamp_field=timestamp_field,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = (source.source if isinstance(source, FilteredSource) else source,)

        source_info = construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
            resource_providers=tuple(resource_providers.values() if resource_providers else []),
            args_supplement=None,
        )
        schemas = self._get_schemas()
        self._args_supplement = self._get_args_supplement(schemas)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._populate_spec()
        base_tecton_object._register_local_object(self)

    @sdk_decorators.sdk_public_method
    def run_stream(self, output_temp_table: str, checkpoint_dir: Optional[str] = None) -> streaming.StreamingQuery:
        """Starts a streaming job to keep writing the output records of this FeatureView to a temporary table.

        The job will be running until the execution is terminated.

        After records have been written to the table, they can be queried using `spark.sql()`.
        If ran in a Databricks notebook, Databricks will also automatically visualize the number of incoming records.

        :param output_temp_table: The name of the temporary table to write to.
        :param checkpoint_dir: A root directory that the streaming job will checkpoint to.
        """
        if self._spec.data_source_type != data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH:
            raise errors.FEATURE_VIEW_HAS_NO_STREAM_SOURCE(self.name)
        return run_api.run_stream(self._feature_definition, output_temp_table, checkpoint_dir)

    @property
    def stream_tiling_enabled(self) -> bool:
        """(Private preview) If `False`, Tecton transforms and writes all events from the stream to the online store (same as stream_processing_mode=`StreamProcessingMode.CONTINUOUS`) . If `True`, Tecton will store the partial aggregations of the events in the online store. defaults to `False`."""
        return self._spec.stream_tiling_enabled

    @property
    def output_stream(self):
        """Configuration for a stream to write feature outputs to, specified as a `tecton.framework.configs.KinesisOutputStream` or `tecton.framework.configs.KafkaOutputStream`."""
        proto = self._spec.output_stream
        if proto.HasField("kafka"):
            return configs.KafkaOutputStream.from_proto(proto)
        elif proto.HasField("kinesis"):
            return configs.KinesisOutputStream.from_proto(proto)
        else:
            msg = f"Unsupported proto for output_stream {proto}"
            raise TypeError(msg)


@stream_feature_view_typechecked
def stream_feature_view(
    *,
    mode: str,
    source: Union[framework_data_source.StreamSource, FilteredSource],
    entities: Sequence[framework_entity.Entity],
    features: Union[Sequence[feature.Aggregate], Sequence[feature.Attribute]],
    timestamp_field: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregation_secondary_key: Optional[str] = None,
    stream_processing_mode: Optional[StreamProcessingMode] = None,
    online: bool = False,
    offline: bool = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    lifetime_start_time: Optional[datetime.datetime] = None,
    manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
    batch_trigger: BatchTriggerType = None,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[configs.ComputeConfigTypes] = None,
    stream_compute: Optional[configs.ComputeConfigTypes] = None,
    offline_store: Optional[
        Union[
            configs.OfflineStoreConfig,
            configs.ParquetConfig,
            configs.DeltaConfig,
            vnext.IcebergConfig,
        ]
    ] = None,
    online_store: Optional[configs.OnlineStoreTypes] = None,
    publish_features_config: Optional[vnext.PublishFeaturesConfig] = None,
    monitor_freshness: bool = False,
    data_quality_enabled: Optional[bool] = None,
    skip_default_expectations: Optional[bool] = None,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    max_backfill_interval: Optional[datetime.timedelta] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[configs.OutputStream] = None,
    options: Optional[Dict[str, str]] = None,
    run_transformation_validation: Optional[bool] = None,
    tecton_materialization_runtime: Optional[str] = None,
    cache_config: Optional[configs.CacheConfig] = None,
    stream_compaction_enabled: Optional[bool] = None,
    batch_compaction_enabled: Optional[bool] = None,
    compaction_enabled: Optional[bool] = None,
    stream_tiling_enabled: Optional[bool] = None,
    environment: Optional[str] = None,
    transform_server_group: Optional[str] = None,
    context_parameter_name: Optional[str] = None,
    aggregation_leading_edge: Optional[AggregationLeadingEdge] = None,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
):
    """Declare a Stream Feature View.

    :param mode: (Required) Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation mode ("spark_sql", "pyspark", "python", or "pandas").
    :param source: (Required) The data source input to the feature view.
    :param entities: (Required) The entities this feature view is associated with.
    :param timestamp_field: (Required) The column name that refers to the timestamp for records that are produced by the
        feature view. This parameter is optional if exactly one column is a Timestamp type.
    :param features: (Required) A list of features this feature view manages.
    :param aggregation_interval: The size of the tiles for a particular feature view (for example, `"1h"` or `"6h"`)
    :param stream_processing_mode: Whether aggregations should be "batched" in time intervals or be updated continuously.
        Continuously aggregated features are fresher but more expensive. One of `StreamProcessingMode.TIME_INTERVAL` or
        `StreamProcessingMode.CONTINUOUS`. defaults to `StreamProcessingMode.TIME_INTERVAL`.
    :param aggregation_secondary_key: Configures secondary key aggregates using the set column. Only valid when using aggregations.
    :param online: Whether the feature view should be materialized to the online feature store.
    :param offline: Whether the feature view should be materialized to the offline feature store.
    :param ttl: The TTL (or "look back window") for features defined by this feature view. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
    :param feature_start_time: When materialization for this feature view should start from. (Required if `offline=True` or `online=True`)
    :param lifetime_start_time: The start time for what data should be included in a lifetime aggregate. (Required if using lifetime windows)
    :param batch_trigger: Defines the mechanism for initiating batch materialization jobs.
        One of `BatchTriggerType.SCHEDULED` or `BatchTriggerType.MANUAL`.
        The default value is `BatchTriggerType.SCHEDULED`, where Tecton will run materialization jobs based on the
        schedule defined by the `batch_schedule` parameter. If set to `BatchTriggerType.MANUAL`, then batch
        materialization jobs must be explicitly initiated by the user through either the Tecton SDK or Airflow operator.
    :param batch_schedule: The interval at which batch materialization should be scheduled.
    :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
    :param batch_compute: Batch materialization cluster configuration.
    :param stream_compute: Streaming materialization cluster configuration.
    :param offline_store: Configuration for how data is written to the offline feature store.
    :param publish_features_config: Configuration for how full features are published post-offline materialization.
    :param online_store: Configuration for how data is written to the online feature store.
    :param monitor_freshness: If true, enables monitoring when feature data is materialized to the online feature store.
    :param data_quality_enabled: If false, disables data quality metric computation and data quality dashboard.
    :param skip_default_expectations: If true, skips validating default expectations on the feature data.
    :param expected_feature_freshness: Threshold used to determine if recently materialized feature data is stale. Data is stale if `now - most_recent_feature_value_timestamp > expected_feature_freshness`. For feature views using Tecton aggregations, data is stale if `now - round_up_to_aggregation_interval(most_recent_feature_value_timestamp) > expected_feature_freshness`. Where `round_up_to_aggregation_interval()` rounds up the feature timestamp to the end of the `aggregation_interval`. Value must be at least 2 times `aggregation_interval`. If not specified, a value determined by the Tecton backend is used.
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be set
        to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
        such as inadvertently deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
        that would trigger a recreation of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
        only enforced in live (i.e. non-dev) workspaces.
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param max_batch_aggregation_interval: Deprecated. Use max_backfill_interval instead, which has the exact same usage.
    :param max_backfill_interval: (Advanced) The time interval for which each backfill job will run to materialize
        feature data. This affects the number of backfill jobs that will run, which is
        (`<feature registration time>` - `feature_start_time`) / `max_backfill_interval`.
        Configuring the `max_backfill_interval` parameter appropriately will help to optimize large backfill jobs.
        If this parameter is not specified, then 10 backfill jobs will run (the default).
    :param output_stream: Configuration for a stream to write feature outputs to, specified as a `tecton.framework.configs.KinesisOutputStream` or `tecton.framework.configs.KafkaOutputStream`.
    :param manual_trigger_backfill_end_time: If set, Tecton will schedule backfill materialization jobs for this feature view up to this time. Materialization jobs after this point must be triggered manually. (This param is only valid to set if batch_trigger is MANUAL.)
    :param options: Additional options to configure the Feature View. Used for advanced use cases and beta features.
    :param run_transformation_validation: If `True`, Tecton will execute the Feature View transformations during tecton plan/apply
        validation. If `False`, then Tecton will not execute the transformations during validation. Skipping query validation can be useful to speed up tecton plan/apply or for Feature Views that have issues
        with Tecton's validation (e.g. some pip dependencies). defaults to `True` for Spark and Snowflake Feature Views and
        `False` for Python and Pandas Feature Views.
    :param tecton_materialization_runtime: Version of `tecton` package used by your job cluster.
    :param cache_config: Cache config for the Feature View. Including this option enables the feature server to use the cache
        when retrieving features for this feature view. Will only be respected if the feature service containing this feature
        view has `enable_online_caching` set to `True`.
    :param stream_compaction_enabled: Deprecated: Please use `stream_tiling_enabled` instead which has the exact same usage.
    :param batch_compaction_enabled: Deprecated: Please use `compaction_enabled` instead which has the exact same usage.
    :param stream_tiling_enabled: (Private preview) If `False`, Tecton transforms and writes all events from the stream to the online store (same as stream_processing_mode=`StreamProcessingMode.CONTINUOUS`) . If `True`, Tecton will store the partial aggregations of the events in the online store. defaults to `False`.
    :param compaction_enabled: (Private preview) If `True`, Tecton will run a compaction job after each batch
        materialization job to write to the online store. This requires the use of Dynamo and uses the ImportTable API.
        Because each batch job overwrites the online store, a larger compute cluster may be required. This is required to be True if `stream_compaction_enabled` is True. defaults to `False`
    :param environment: The custom environment in which materialization jobs will be run. Only one of `environment` and `transform_server_group` can be specified. Defaults to `None`, which means
        jobs will execute in the default Tecton environment.
    :param transform_server_group: The server group to use for running the transformation job. Only one of `environment` and `transform_server_group` can be specified. If not specified, the default Tecton Environment will be used. This is only applicable for stream feature views with push config.
        Defaults to `None`.
    :param context_parameter_name: Name of the function parameter that Tecton injects MaterializationContext object to.
    :param aggregation_leading_edge: (Advanced) Specifies the timestamp used for the leading edge of aggregation time windows. This parameter only affects online serving. See the AggregationLeadingEdge class documentation or the Tecton docs for more information. defaults to AggregationLeadingEdge.WALL_CLOCK_TIME.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the transformation function at runtime. During local development and testing, strings may be used instead Secret references.
    :param resource_providers: A dictionary mapping string names to ResourceProviders that will be available during feature transformation.
    :return: An object of type `StreamFeatureView`.
    """
    # TODO(deprecate_after=0.8): This warning can be completely removed in 0.9, so it can be deleted once the 0.8 branch is cut.
    if max_batch_aggregation_interval is not None:
        msg = "FeatureView.max_batch_aggregation_interval is deprecated and is no longer supported in 0.8. Please use max_backfill_interval instead. max_backfill_interval has the same semantics and is just a new name."
        raise ValueError(msg)

    if batch_compaction_enabled is not None and compaction_enabled is not None:
        msg = "FeatureView.batch_compaction_enabled is deprecated. Please use compaction_enabled instead. compaction_enabled has the same semantics and is just a new name."
        raise TectonValidationError(msg)

    compaction_enabled = compaction_enabled or batch_compaction_enabled or False

    if stream_compaction_enabled is not None and stream_tiling_enabled is not None:
        msg = "FeatureView.stream_compaction_enabled is deprecated. Please use stream_tiling_enabled instead. stream_tiling_enabled has the same semantics and is just a new name."
        raise TectonValidationError(msg)

    stream_tiling_enabled = stream_tiling_enabled or stream_compaction_enabled or False

    def decorator(feature_view_function):
        return StreamFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            feature_view_function=feature_view_function,
            source=source,
            entities=entities,
            mode=mode,
            aggregation_interval=aggregation_interval,
            aggregation_secondary_key=aggregation_secondary_key,
            features=features,
            stream_processing_mode=stream_processing_mode,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            offline_store=offline_store,
            publish_features_config=publish_features_config,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            timestamp_field=timestamp_field,
            max_backfill_interval=max_backfill_interval,
            output_stream=output_stream,
            options=options,
            run_transformation_validation=run_transformation_validation,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            compaction_enabled=compaction_enabled,
            stream_tiling_enabled=stream_tiling_enabled,
            environment=environment,
            transform_server_group=transform_server_group,
            context_parameter_name=context_parameter_name,
            aggregation_leading_edge=aggregation_leading_edge or AggregationLeadingEdge.WALL_CLOCK_TIME,
            secrets=secrets,
            resource_providers=resource_providers,
        )

    return decorator


@attrs.define(eq=False)
class FeatureTable(FeatureView):
    """A Tecton Feature Table.

    Feature Tables are used to batch push features into Tecton from external feature computation systems.

    ```python
    from tecton import Entity, FeatureTable
    from tecton.types import Field, String, Timestamp, Int64
    import datetime

    # Declare your user Entity instance here or import it if defined elsewhere in
    # your Tecton repo.

    user = ...

    features = [
        Attribute('user_login_count_7d', Int64),
        Attribute('user_login_count_30d', Int64)
    ]

    user_login_counts = FeatureTable(
        name='user_login_counts',
        entities=[user],
        features=features,
        online=True,
        offline=True,
        ttl=datetime.timedelta(days=30),
        timestamp_key='timestamp'
    )
    ```
    Attributes:
        entities: The Entities for this Feature View.
        info: A dataclass containing basic info about this Tecton Object.
    """

    entities: Tuple[framework_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        entities: List[framework_entity.Entity],
        features: List[feature.Attribute],
        timestamp_field: str,
        ttl: Optional[datetime.timedelta] = None,
        online: bool = False,
        offline: bool = False,
        offline_store: Optional[Union[configs.OfflineStoreConfig, configs.DeltaConfig, vnext.IcebergConfig]] = None,
        online_store: Optional[configs.OnlineStoreTypes] = None,
        batch_compute: Optional[configs.ComputeConfigTypes] = None,
        online_serving_index: Optional[List[str]] = None,
        alert_email: Optional[str] = None,
        tecton_materialization_runtime: Optional[str] = None,
        cache_config: Optional[configs.CacheConfig] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Instantiate a new Feature Table.

        :param name: Unique, human friendly name that identifies the Feature Table.
        :param description: A human-readable description.
        :param owner: Owner name (typically the email of the primary maintainer).
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must
            be set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to
            prevent accidental changes such as inadvertently deleting a Feature Service used in production or recreating
            a Feature Table that triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to
            dependent Tecton objects that would trigger a recreation of the tagged object, e.g. if `prevent_destroy` is
            set on a Feature Service, that will also prevent deletions or re-creates of Feature Tables used in that
            service. `prevent_destroy` is only enforced in live (i.e. non-dev) workspaces.
        :param entities: A list of Entity objects, used to organize features.
        :param ttl: The TTL (or "look back window") for features defined by this feature table. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
        :param online: Enable writing to online feature store.
        :param offline: Enable writing to offline feature store.
        :param offline_store: Configuration for how data is written to the offline feature store.
        :param online_store: Configuration for how data is written to the online feature store.
        :param batch_compute: Configuration for batch materialization clusters. Should be one of:
            [`EMRClusterConfig`, `DatabricksClusterConfig`, `EMRJsonClusterConfig`, `DatabricksJsonClusterConfig`]
        :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during
            online serving. Defaults to the complete set of join keys. Up to one join key may be omitted. If one key is
            omitted, online requests to a Feature Service will return all feature vectors that match the specified join
            keys.
        :param alert_email: Email that alerts for this Feature Table will be sent to.
        :param tecton_materialization_runtime: Version of `tecton` package used by your job cluster.
        :param features: A list of features this Feature Table manages.
        :param timestamp_field: The column name that refers to the timestamp for records that are produced by the
            Feature Table.
        :param cache_config: Cache config for the Feature Table. Including this option enables the feature server to use
            the cache when retrieving features for this feature table. Will only be respected if the feature service
            containing this feature table has `enable_online_caching` set to `True`.
        :param options: Additional options to configure the Feature Table. Used for advanced use cases and beta features.
        """
        _validate_features(features, name)

        if online_store is None:
            online_store = repo_config.get_feature_table_defaults().online_store

        if offline_store is None:
            offline_store = repo_config.get_feature_table_defaults().offline_store_config
        elif isinstance(offline_store, (configs.DeltaConfig, vnext.IcebergConfig)):
            offline_store = configs.OfflineStoreConfig(staging_table_format=offline_store)

        if batch_compute is None:
            batch_compute = repo_config.get_feature_table_defaults().batch_compute
        _warn_if_emr_compute_uses_cluster_default_python(batch_compute)

        if tecton_materialization_runtime is None:
            tecton_materialization_runtime = repo_config.get_feature_table_defaults().tecton_materialization_runtime

        feature_table_args = feature_view__args_pb2.FeatureTableArgs(
            tecton_materialization_runtime=tecton_materialization_runtime,
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            batch_compute=batch_compute._to_cluster_proto(),
            online_store=online_store._to_proto() if online_store else None,
            monitoring=configs.MonitoringConfig(monitor_freshness=False, alert_email=alert_email)._to_proto(),
            offline_store=offline_store._to_proto(),
            timestamp_field=timestamp_field,
        )

        if features:
            feature_table_args.attributes.extend([feature._to_proto() for feature in features])
        else:
            msg = f"Feature Table'{name}' needs to set `features`. "
            raise TectonValidationError(msg)

        # If unspecified, online_serving_index defaults to the join_keys of the Feature Table.
        join_keys = []
        for entity in entities:
            join_keys.extend(entity.join_keys)

        args = feature_view__args_pb2.FeatureViewArgs(
            feature_table_args=feature_table_args,
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FEATURE_TABLE,
            version=self._framework_version.value,
            entities=[
                feature_view__args_pb2.EntityKeyOverride(entity_id=entity.info._id_proto, join_keys=entity.join_keys)
                for entity in entities
            ],
            online_enabled=online,
            offline_enabled=offline,
            online_serving_index=online_serving_index,
            batch_compute_mode=BatchComputeMode(
                infer_batch_compute_mode(
                    pipeline_root=None, batch_compute_config=batch_compute, stream_compute_config=None
                )
            ).value,
            cache_config=cache_config._to_proto() if cache_config else None,
            options=options,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            entities=tuple(entities),
            args_supplement=None,
        )
        schemas = self._get_schemas()
        self._args_supplement = self._get_args_supplement(schemas)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._populate_spec()
        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.FeatureTableSpec, fco_container_: fco_container.FcoContainer) -> "FeatureTable":
        """Create a FeatureTable from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(framework_entity.Entity._from_spec(entity_spec))

        # override the framework version class attribute to be the framework version set by the spec
        class FeatureTableFromSpec(cls):
            _framework_version = spec.metadata.framework_version

        obj = FeatureTableFromSpec.__new__(FeatureTableFromSpec)  # pylint: disable=no-value-for-parameter
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            entities=tuple(entities),
            args_supplement=None,
        )

        return obj

    @property
    def _supported_modes(self) -> List[str]:
        return []

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        return list(self.entities)

    def _get_schemas(self) -> _Schemas:
        entity_specs = [entity._spec for entity in self.entities]

        schema_dict = {
            join_key.name: join_key.dtype for entity_spec in entity_specs for join_key in entity_spec.join_keys
        }
        schema_dict.update(
            {
                attribute.name: data_types.data_type_from_proto(attribute.column_dtype)
                for attribute in self._args.feature_table_args.attributes
            }
        )
        schema_dict[self._args.feature_table_args.timestamp_field] = data_types.TimestampType()

        view_schema = Schema.from_dict(schema_dict).to_proto()

        # For feature tables, materialization and view schema are the same.
        return _Schemas(
            view_schema=view_schema,
            materialization_schema=view_schema,
            online_batch_table_format=None,
        )

    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        fd = self._feature_definition

        if self._is_local_object:
            raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(self.name, "Feature Table")

        if not fd.materialization_enabled:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if from_source:
            raise errors.FROM_SOURCE_WITH_FT

        if not fd.writes_to_offline_store:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(self.info.name)

        return QuerySources(feature_table_count=1)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_features_for_events(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame],
        timestamp_key: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature table.

        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.

        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        Examples:
        A FeatureView `fv` with join key `user_id`.
        1. `fv.get_features_for_events(spine)` where `spine=pandas.Dataframe({'user_id': [1,2,3],
        'date': [datetime(...), datetime(...), datetime(...)]})`
        Fetch features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.
        2) `fv.get_features_for_events(spine, timestamp_key='date_1')` where spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
        Fetch features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of  feature values in the specified time range.
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
        :param compute_mode: Compute mode to use to produce the data frame.

        :return: A TectonDataFrame with features values.
        """
        sources = self._check_can_query_from_source(from_source=False)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA:
            raise errors.GET_FEATURES_FOR_EVENTS_UNSUPPORTED

        return querytree_api.get_features_for_events(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            from_source=False,
            mock_data_sources={},
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_features_in_range(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        max_lookback: Optional[datetime.timedelta] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature table.

        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.

        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: Union[pendulum.DateTime, datetime.datetime]
        :param end_time:  The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: Union[pendulum.DateTime, datetime.datetime]
        :param max_lookback: [Non-Aggregate Feature Tables Only] A performance optimization that configures how far back
        before start_time to look for events in the raw data. If set, get_features_in_range() may not include all
        entities with valid feature values in the specified time range, but get_features_in_range() will never
        return invalid values.
        :type max_lookback: datetime.timedelta
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A TectonDataFrame with features values.
        """
        sources = self._check_can_query_from_source(from_source=False)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode != ComputeMode.SPARK and compute_mode != ComputeMode.RIFT:
            raise errors.GET_FEATURES_IN_RANGE_UNSUPPORTED

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        return querytree_api.get_features_in_range(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            start_time=start_time,
            end_time=end_time,
            max_lookback=max_lookback,
            entities=entities,
            from_source=False,
            mock_data_sources={},
        )

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message is split conditionally on whether a spine is provided
    )
    # if spine is provided, then timestamp_key is optional, but start_time, end_time, and entities cannot be used
    @overload
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, MOCK_INPUT_TYPES]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message
    )
    # if spine not provided, then timestamp_key should also not be provided.
    # start_time, end_time, and entities can be used instead.
    @overload
    def get_historical_features(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message is split conditionally depending on whether a spine is provided.
    )
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        timestamp_key: Optional[str] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature table.

        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.

        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of  feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: Union[pendulum.DateTime, datetime.datetime]
        :param end_time:  The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: Union[pendulum.DateTime, datetime.datetime]
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A TectonDataFrame with features values.
        """
        sources = self._check_can_query_from_source(from_source=False)
        sources.display()

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if start_time is not None and end_time is not None and start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=False,
                feature_set_config=self._construct_feature_set_config(),
            )

        return querytree_api.get_historical_features_for_feature_definition(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=False,
            mock_data_sources={},
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, numpy.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """Returns a single Tecton FeatureVector from the Online Store.

        :param join_keys: Join keys of the enclosed Feature Table.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.

        :return: A FeatureVector of the results.
        """
        if not self._feature_definition.materialization_enabled:
            raise errors.FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if not self._feature_definition.writes_to_online_store:
            msg = "get_online_features"
            raise errors.UNSUPPORTED_OPERATION(msg, "online=True was not set for this Feature Table.")

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def ingest(self, df: Union[pyspark_dataframe.DataFrame, pandas.DataFrame]):
        """Ingests a Dataframe into the Feature Table.

        This method kicks off a materialization job to write the data into the offline and online store, depending on
        the Feature Table configuration.

        :param df: The Dataframe to be ingested. Has to conform to the Feature Table schema.
        """
        if not self._feature_definition.materialization_enabled:
            msg = "ingest"
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(msg)

        get_upload_info_request = metadata_service_pb2.GetNewIngestDataframeInfoRequest(
            feature_definition_id=self._spec.id_proto
        )
        upload_info_response = metadata_service.instance().GetNewIngestDataframeInfo(get_upload_info_request)

        df_path = upload_info_response.df_path
        upload_url = upload_info_response.signed_url_for_df_upload
        spark_api.write_dataframe_to_path_or_url(
            df, df_path, upload_url, self._feature_definition.view_schema, enable_schema_validation=True
        )

        ingest_request = metadata_service_pb2.IngestDataframeRequest(
            workspace=self.info.workspace, feature_definition_id=self._spec.id_proto, df_path=df_path
        )
        response = metadata_service.instance().IngestDataframe(ingest_request)

    @sdk_decorators.sdk_public_method
    def get_timestamp_field(self) -> str:
        """Returns the name of the timestamp field of this Feature Table."""
        return self._spec.timestamp_field

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def delete_keys(
        self,
        keys: Union[pyspark_dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> List[str]:
        """Deletes any materialized data that matches the specified join keys from the Feature Table.

        This method kicks off a job to delete the data in the offline and online stores.
        If a Feature Table has multiple entities, the full set of join keys must be specified.
        Only supports Dynamo online store.
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the Feature Table join keys.
        :param online: Whether or not to delete from the online store.
        :param offline: Whether or not to delete from the offline store.
        :return: List of job ids for jobs created for entity deletion.
        """
        is_live_workspace = internal_utils.is_live_workspace(self.info.workspace)
        if not is_live_workspace:
            msg = "delete_keys"
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(msg)

        return delete_keys_api.delete_keys(online, offline, keys, self._feature_definition)

    @sdk_decorators.documented_by(MaterializedFeatureView.materialization_status)
    @sdk_decorators.assert_remote_object
    def materialization_status(
        self, verbose: bool = False, limit: int = 1000, sort_columns: Optional[str] = None, errors_only: bool = False
    ) -> display.Displayable:
        return materialization_api.get_materialization_status_for_display(
            self._spec.id_proto, self.workspace, verbose, limit, sort_columns, errors_only
        )

    @property
    def ttl(self) -> Duration:
        """TTL defines feature lifespan and look-back window for training sets."""
        return self._spec.ttl

    @property
    def online(self) -> bool:
        """Whether the Feature Table is materialized to the online feature store."""
        return self._spec.online

    @property
    def offline(self) -> bool:
        """Whether the Feature Table is materialized to the offline feature store."""
        return self._spec.offline

    @property
    def offline_store(
        self,
    ) -> Optional[Union[configs.DeltaConfig, configs.ParquetConfig, vnext.IcebergConfig]]:
        """Configuration for the Offline Store of this Feature Table."""
        offline_feature_store = self._spec.offline_store
        if offline_feature_store.HasField("delta"):
            staging_config = configs.DeltaConfig
        elif offline_feature_store.HasField("parquet"):
            staging_config = configs.ParquetConfig
        elif offline_feature_store.HasField("iceberg"):
            staging_config = vnext.IcebergConfig
        else:
            return None

        return staging_config.from_proto(offline_feature_store)

    @property
    def alert_email(self) -> Optional[str]:
        """
        Email that alerts for this Feature Table will be sent to.
        """
        return self._spec.alert_email

    @property
    def tecton_materialization_runtime(self) -> Optional[str]:
        """
        Version of `tecton` package used by your job cluster.
        """
        return self._spec.tecton_materialization_runtime

    @property
    def timestamp_field(self) -> Optional[str]:
        """
        The column name that refers to the timestamp for records that are produced by the Feature Table. This parameter
        is optional if exactly one column is a Timestamp type.
        """
        return self._spec.timestamp_field


@attrs.define(eq=False)
class _RealtimeBase(FeatureView):
    """Class for RealtimeFeatureView and potential similar classes to inherit common methods from.

    Attributes:
        sources: The Data Sources for this Feature View.
        transformations: The Transformations for this Feature View.
    """

    sources: Tuple[Union["FeatureReference", configs.RequestSource], ...] = attrs.field(on_setattr=attrs.setters.frozen)
    transformations: Tuple[framework_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    # Note providers are stored here so there are fetched in `_get_dependent_objects`
    # and put in the fco container. The key used in the map is not needed here.
    resource_providers: Tuple[resource_provider.ResourceProvider, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    def _supported_modes(self) -> List[str]:
        raise NotImplementedError

    @staticmethod
    def _extract_sources(sources):
        """Helper function to extract from arguments"""
        references_and_request_sources = []
        for source in sources:
            if isinstance(source, FeatureView):
                references_and_request_sources.append(FeatureReference(feature_definition=source))
            else:
                references_and_request_sources.append(source)
        return tuple(references_and_request_sources)

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        dependent_objects = list(self.transformations) + list(self.resource_providers)
        for fv in self._get_dependent_feature_views():
            if include_indirect_dependencies:
                dependent_objects.extend([*fv._get_dependent_objects(include_indirect_dependencies=True), fv])
            else:
                dependent_objects.append(fv)

        # Dedupe by ID.
        return list({fco_obj.id: fco_obj for fco_obj in dependent_objects}.values())

    def _get_dependent_feature_views(self) -> List[FeatureView]:
        return [source.feature_definition for source in self.sources if isinstance(source, FeatureReference)]

    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        all_sources = QuerySources(realtime_count=1)
        for fv in self._get_dependent_feature_views():
            all_sources += fv._check_can_query_from_source(from_source)
        return all_sources

    @property
    def _request_context(self) -> request_context.RequestContext:
        rc = pipeline_common.find_request_context(self._feature_definition.pipeline.root)
        return request_context.RequestContext({}) if rc is None else request_context.RequestContext.from_proto(rc)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_online_features(
        self,
        join_keys: Optional[Mapping[str, Union[int, numpy.int_, str, bytes]]] = None,
        include_join_keys_in_response: bool = False,
        request_data: Optional[Mapping[str, Union[int, numpy.int_, str, bytes, float]]] = None,
    ) -> FeatureVector:
        """Returns a single Tecton `tecton.FeatureVector` from the Online Store.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.
        :param request_data: Dictionary of request context values used for RealtimeFeatureViews.

        :return: A `tecton.FeatureVector` of the results.
        """
        # Default to empty dicts.
        join_keys = join_keys or {}
        request_data = request_data or {}

        if not join_keys and self._get_dependent_feature_views():
            raise errors.GET_ONLINE_FEATURES_ODFV_JOIN_KEYS

        request_context = self._request_context
        required_request_context_keys = list(request_context.schema.keys())
        if len(required_request_context_keys) > 0 and request_data is None:
            raise errors.GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(required_request_context_keys)
        internal_utils.validate_request_data(request_data, required_request_context_keys)

        return query_helper._QueryHelper(self.workspace, feature_view_name=self.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_data,
            request_context,
        )


@attrs.define(eq=False)
class RealtimeFeatureView(_RealtimeBase):
    """A Tecton Realtime Feature View.

    :param mode: (Required) Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("python" or "pandas" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: (Required) The data source inputs to the feature view. An input can be a RequestSource, a BatchFeatureView, or a StreamFeatureView
    :param features: (Required) A list of features this feature view manages.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
        set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
        only enforced in live (i.e. non-dev) workspaces.
    :param environments: The environments in which this feature view can run. Defaults to `None`, which means
        the feature view can run in any environment. If specified, the feature view will only run in the specified
        environments. Learn more about environments at
        [Realtime Feature View Environments](https://docs.tecton.ai/docs/defining-features/feature-views/realtime-feature-view/realtime-feature-view-environments).
    :param required_packages: A list of Python packages constraints required to run the transformation function. These list of constraints will be validated against the environment used by a transformn server group at apply time.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the Realtime transformation at runtime. During local development and testing, strings may be used instead Secret references.
    :param resource_providers: A dictionary of Resource providers that will be evaluated and resources will be provided to transformation function at runtime.


    The RealtimeFeatureView should only be instantiated directly if you're using Calculation features. Otherwise the
    `@realtime_feature_view` decorator is recommended.

    Attributes:
        sources: The Request Sources and dependent Feature Views for this Realtime Feature View.
        transformations: The Transformations for this Feature View.
    """

    sources: Tuple[Union["FeatureReference", configs.RequestSource], ...] = attrs.field(on_setattr=attrs.setters.frozen)
    transformations: Tuple[framework_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @realtime_feature_view_typechecked
    def __init__(
        self,
        *,
        name: str,
        sources: List[Union[configs.RequestSource, FeatureView, "FeatureReference"]],
        features: List[Union[feature.Attribute, feature.Calculation]],
        mode: Optional[str] = NO_TRANSFORMATION_MODE_STR,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Optional[Callable] = None,
        environments: Optional[List[str]] = None,
        required_packages: Optional[List[str]] = None,
        secrets: Optional[Dict[str, Union[Secret, str]]] = None,
        resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
        _context_parameter_name: Optional[
            str
        ] = DEFAULT_CONTEXT_PARAMETER_NAME,  # should not be set directly here, only by the decorator
    ):
        self._validate_parameters(name, features, mode, feature_view_function, sources, _context_parameter_name)

        if feature_view_function:
            pipeline_function = self._get_or_create_pipeline_function(
                name=name,
                mode=mode,
                description=description,
                owner=owner,
                tags=tags,
                feature_view_function=feature_view_function,
            )
            pipeline_root = self._build_pipeline(
                name, feature_view_function, pipeline_function, sources, _context_parameter_name
            )
        else:
            pipeline_root = _build_join_inputs_pipeline(
                sources=sources,
                context_parameter_name=_context_parameter_name,
                features=features,
            )

        if environments and required_packages:
            raise TectonValidationError(CONSTRAINTS_ERROR_MESSAGE)

        realtime_args = feature_view__args_pb2.RealtimeArgs(
            environments=environments if environments else [],
            required_packages=(required_packages if required_packages else []) if feature_view_function else [],
        )
        references_and_request_sources = self._extract_sources(sources)

        for _feature in features:
            if isinstance(_feature, Attribute):
                realtime_args.attributes.append(_feature._to_proto())
            elif isinstance(_feature, Calculation):
                input_schema = self._build_input_schema(references_and_request_sources)
                realtime_args.calculations.append(_feature._to_proto(input_schema))
            else:
                # @realtime_realtime_feature_view_typechecked on __init__ should prevent this branch.
                msg = f"Feature '{_feature.name}' is {_feature.__class__}, which is not compatible with Realtime Feature View. "
                raise TectonValidationError(msg)

        secret_references = {}
        if secrets:
            for secret_name, secret in secrets.items():
                secret_references[secret_name] = convert_secret_to_sanitized_reference(secret)

        args = feature_view__args_pb2.FeatureViewArgs(
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            version=self._framework_version.value,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_REALTIME,
            realtime_args=realtime_args,
            context_parameter_name=_context_parameter_name,
            secrets=secret_references,
            resource_providers={
                name_override: resource_provider._id_proto
                for name_override, resource_provider in resource_providers.items()
            }
            if resource_providers
            else {},
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = construct_fco_source_info(args.feature_view_id)

        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=references_and_request_sources,
            transformations=tuple(pipeline_root.transformations),
            resource_providers=tuple(resource_providers.values() if resource_providers else []),
            args_supplement=None,
        )

        schemas = self._get_schemas()
        self._args_supplement = self._get_args_supplement(schemas)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._populate_spec()

        base_tecton_object._register_local_object(self)

    def _validate_parameters(self, name, features, mode, feature_view_function, sources, context_parameter_name):
        # TODO (lee): remove _validate_rtfv_no_transform_with_calculations after we allow calculations with
        #  transformations
        _validate_rtfv_no_transform_with_calculations(feature_view_function, features, name)

        # TODO(FE-2701): Allow Attributes and Calculation once the column reference declaration between Attributes and Calculations
        #  are consistent
        has_attributes_and_calculations = any(isinstance(feature, Calculation) for feature in features) and any(
            isinstance(feature, Attribute) for feature in features
        )
        if has_attributes_and_calculations:
            msg = "Currently `Attribute` and `Calculation` cannot be defined on the same Feature View. Please separate them into different Feature Views."
            raise TectonValidationError(msg)

        # this error gets caught in the Transformation code and returns a confusing stack trace, so catch it here instead
        if mode == NO_TRANSFORMATION_MODE_STR and feature_view_function:
            raise errors.ModeUnsupportedForFeatureView(mode=mode, has_transformation=True)

        if feature_view_function is None and mode != NO_TRANSFORMATION_MODE_STR:
            raise errors.ModeUnsupportedForFeatureView(mode=mode, has_transformation=feature_view_function is not None)

        if mode == NO_TRANSFORMATION_MODE_STR and context_parameter_name != DEFAULT_CONTEXT_PARAMETER_NAME:
            raise errors.CONTEXT_PARAMETER_NAME_UNSUPPORTED_FOR_NO_TRANSFORMATION_MODE(context_parameter_name)

        _validate_fv_function_inputs(sources, feature_view_function, context_parameter_name)
        _validate_features(features, name)

    def _build_input_schema(
        self, references_and_request_source: Tuple[Union[FeatureReference, configs.RequestSource]]
    ) -> Dict[str, SdkDataType]:
        schema = {f"{DEFAULT_CONTEXT_PARAMETER_NAME}.{REQUEST_TIMESTAMP_FIELD_NAME}": Timestamp}
        for source in references_and_request_source:
            if isinstance(source, FeatureReference):
                schema.update(self._build_input_schema_from_feature_reference(source))
            else:
                schema.update(self._build_input_schema_from_request_source(source))
        return schema

    def _build_input_schema_from_feature_reference(self, feature_reference: FeatureReference):
        all_metadata = feature_reference.feature_definition.feature_metadata
        if feature_reference.features:
            all_metadata = filter(lambda metadata: metadata.name in feature_reference.features, all_metadata)
        return {f"{feature_reference.namespace}.{metadata.name}": metadata.dtype for metadata in all_metadata}

    def _build_input_schema_from_request_source(self, request_source: configs.RequestSource):
        if request_source.name:
            prefix = request_source.name + "."
        else:
            prefix = ""
        return {prefix + field.name: field.dtype for field in request_source.schema}

    def _get_schemas(self) -> _Schemas:
        attributes = self._args.realtime_args.attributes
        calculations = self._args.realtime_args.calculations
        attribute_schema = {
            attribute.name: data_types.data_type_from_proto(attribute.column_dtype) for attribute in attributes
        }
        calculation_schema = {
            calculation.name: data_types.data_type_from_proto(calculation.column_dtype) for calculation in calculations
        }
        view_schema = Schema.from_dict({**attribute_schema, **calculation_schema}).to_proto()

        return _Schemas(
            view_schema=view_schema,
            materialization_schema=view_schema,
            online_batch_table_format=None,
        )

    @classmethod
    @typechecked
    def _from_spec(
        cls, spec: specs.RealtimeFeatureViewSpec, fco_container_: fco_container.FcoContainer
    ) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(framework_transformation.Transformation._from_spec(transformation_spec))

        resource_providers = []
        for resource_provider_spec in feature_definition.resource_providers.values():
            resource_providers.append(resource_provider.ResourceProvider._from_spec(resource_provider_spec))

        # override the framework version class attribute to be the framework version set by the spec
        class RealtimeFeatureViewFromSpec(cls):
            _framework_version = spec.metadata.framework_version

        obj = RealtimeFeatureViewFromSpec.__new__(RealtimeFeatureViewFromSpec)  # pylint: disable=no-value-for-parameter
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=tuple(_build_realtime_sources_from_spec(spec, fco_container_)),
            transformations=tuple(transformations),
            resource_providers=resource_providers,
            args_supplement=None,
        )

        return obj

    @property
    def _supported_modes(self) -> List[str]:
        return ["pipeline", "pandas", "python"]

    @property
    def environments(self) -> Tuple[str, ...]:
        """The environment in which this feature view runs."""
        return self._spec.environments

    @property
    def context_parameter_name(self) -> Optional[str]:
        """Name of the function parameter that Tecton injects Realtime Context to."""
        return self._spec.context_parameter_name

    @sdk_decorators.sdk_public_method
    def run_transformation(
        self,
        input_data: Dict[str, Any],
        request_timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
    ) -> Union[Dict[str, Any], TectonDataFrame]:
        """Run the RealtimeFeatureView using mock inputs.

        ```python
        # Given a Python Realtime Feature View defined in your workspace:
        @realtime_feature_view(
            sources=[transaction_request, user_transaction_amount_metrics],
            mode="python",
            features=features,
            description="The transaction amount is higher than the 1 day average.",
        )
        def transaction_amount_is_higher_than_average(request, user_metrics):
            return {"higher_than_average": request["amt"] > user_metrics["daily_average"]}
        ```

        ```python
        # Retrieve and run the Feature View in a notebook using mock data:
        import tecton

        fv = tecton.get_workspace("prod").get_feature_view("transaction_amount_is_higher_than_average")

        input_data = {"request": {"amt": 100}, "user_metrics": {"daily_average": 1000}}

        result = fv.run_transformation(input_data=input_data)

        print(result)
        # {'higher_than_average': False}
        ```

        :param input_data: Required. Dict with the same expected keys as the RealtimeFeatureView's inputs parameters.
            For the "python" mode, each value must be a Dictionary representing a single row.
            For the "pandas" mode, each value must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        :param request_timestamp: The timestamp of the request made to the Tecton Feature Server. Used to populate the
            `request_timestamp` field in the RealtimeContext. defaults to datetime.now().

        :return: A `Dict` object for the "python" mode and a tecton DataFrame of the results for the "pandas" mode.
        """
        if (
            self._feature_definition.transformation_mode
            == transformation_pb2.TransformationMode.TRANSFORMATION_MODE_NO_TRANSFORMATION
        ):
            raise errors.RUN_TRANSFORMATION_UNSUPPORTED_FOR_NO_TRANSFORMATION_MODE

        # Snowflake compute uses the same code for run_realtime as Spark.
        return run_api.run_realtime(
            self._feature_definition,
            self.info.name,
            input_data,
            self._feature_definition.transformation_mode,
            request_timestamp=request_timestamp,
        )

    @deprecated(
        version="0.9",
        reason="`run()` is replaced by `run_transformation()`.",
        warning_message=errors.REALTIME_FEATURE_VIEW_RUN_DEPRECATED,
    )
    @sdk_decorators.sdk_public_method
    def run(
        self, **mock_inputs: Union[Dict[str, Any], pandas.DataFrame, pyspark_dataframe.DataFrame]
    ) -> Union[Dict[str, Any], TectonDataFrame]:
        r"""Run the RealtimeFeatureView using mock inputs.

        ```python
        # Given a Python Realtime Feature View defined in your workspace:
        @realtime_feature_view(
            sources=[transaction_request, user_transaction_amount_metrics],
            mode="python",
            features=features,
            description="The transaction amount is higher than the 1 day average.",
        )
        def transaction_amount_is_higher_than_average(request, user_metrics):
            return {"higher_than_average": request["amt"] > user_metrics["daily_average"]}
        ```

        ```python
        # Retrieve and run the Feature View in a notebook using mock data:
        import tecton

        fv = tecton.get_workspace("prod").get_feature_view("transaction_amount_is_higher_than_average")

        result = fv.run(request={"amt": 100}, user_metrics={"daily_average": 1000})

        print(result)
        # {'higher_than_average': False}
        ```

        :param mock_inputs: Required. Keyword args with the same expected keys
            as the RealtimeFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        :return: A `Dict` object for the "python" mode and a tecton DataFrame of the results for the "pandas" mode.
        """
        # Snowflake compute uses the same code for run_realtime as Spark.
        return run_api.run_realtime(
            self._feature_definition,
            self.info.name,
            mock_inputs,
            self._feature_definition.transformation_mode,
        )

    @deprecated(
        version="0.9",
        reason="`test_run()` is replaced by `run_transformation()`.",
        warning_message=None,  # warning message is split conditionally depending on what aggregation_level is provided
    )
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_local_object(error_message=errors.CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT)
    def test_run(
        self, **mock_inputs: Union[Dict[str, Any], pandas.DataFrame]
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Run the RealtimeFeatureView using mock sources.

        Unlike `run`, `test_run` is intended for unit testing. It will not make calls to your
        connected Tecton cluster to validate the RealtimeFeatureView.

        ```python
        from datetime import datetime, timedelta
        import pandas
        from fraud.features.batch_features.user_credit_card_issuer import user_credit_card_issuer

        # The `tecton_pytest_spark_session` is a PyTest fixture that provides a
        # Tecton-defined PySpark session for testing Spark transformations and feature
        # views.

        def test_user_distinct_merchant_transaction_count_30d(tecton_pytest_spark_session):
            input_pandas_df = pandas.DataFrame({
                "user_id": ["user_1", "user_2", "user_3", "user_4"],
                "signup_timestamp": [datetime(2022, 5, 1)] * 4,
                "cc_num": [1000000000000000, 4000000000000000, 5000000000000000, 6000000000000000],
            })
            input_spark_df = tecton_pytest_spark_session.createDataFrame(input_pandas_df)

            # Simulate materializing features for May 1st.
            output = user_credit_card_issuer.test_run(
                start_time=datetime(2022, 5, 1),
                end_time=datetime(2022, 5, 2),
                fraud_users_batch=input_spark_df)
            actual = output.to_pandas()
            expected = pandas.DataFrame({
                "user_id": ["user_1", "user_2", "user_3", "user_4"],
                "signup_timestamp":  [datetime(2022, 5, 1)] * 4,
                "credit_card_issuer": ["other", "Visa", "MasterCard", "Discover"],
            })

            pandas.testing.assert_frame_equal(actual, expected)
        ```

        :param mock_inputs: Required. Keyword args with the same expected keys
            as the RealtimeFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.
        :return: A `Dict` object for the "python" mode and a `pandas.DataFrame` object for the "pandas" mode".
        """
        # TODO(FE-2693): Validate batch feature inputs here against BFV schema
        run_api._validate_realtime_mock_inputs_match_expected_shape(
            mock_inputs, self._args.pipeline, self._feature_definition
        )

        transformation_specs = [transformation._spec for transformation in self.transformations]

        return run_api.run_mock_rtfv_pipeline(
            self._args.pipeline,
            transformation_specs,
            self.name,
            mock_inputs,
            context_parameter_name=self._feature_definition.context_parameter_name or DEFAULT_CONTEXT_PARAMETER_NAME,
            secret_resolver=LocalDevSecretResolver(),
            secret_references=self._feature_definition.secrets,
            resource_providers=self._feature_definition.resource_providers,
        )

    @sdk_decorators.sdk_public_method
    def get_features_for_events(
        self,
        events: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **kwargs,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature view.

        By default (i.e. `from_source=None`), this method fetches feature values from the Offline Store for input
        Feature Views that have offline materialization enabled and otherwise computes input feature values on the fly
        from raw data.

        :param events: A dataframe of possible join keys, request data keys, and timestamps that specify which feature values to fetch.
            The returned data frame will contain rollups for all (join key, request data key)
            combinations that are required to compute a full frame from the `events` dataframe.
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified and this feature view has feature view dependencies, `timestamp_key` will default to the time column of the spine if there is only one present.
        :param from_source: Whether feature values should be recomputed from the original data source. If `None`,
            input feature values will be fetched from the Offline Store for Feature Views that have offline
            materialization enabled and otherwise computes feature values on the fly from raw data. Use
            `from_source=True` to force computing from raw data and `from_source=False` to error if any input
            Feature Views are not materialized. Defaults to None.
        :param compute_mode: Compute mode to use to produce the data frame.


        :return: A `TectonDataFrame`.
        """
        sources = self._check_can_query_from_source(from_source)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA:
            raise errors.GET_FEATURES_FOR_EVENTS_UNSUPPORTED

        return querytree_api.get_features_from_params(
            GetFeaturesForEventsParams(
                fco=self._feature_definition,
                events=events,
                timestamp_key=timestamp_key,
                from_source=from_source,
                compute_mode=compute_mode,
                mock_data_sources={},
                skew_config=kwargs.get("skew_config"),
            )
        )

    @deprecated(
        version="0.9",
        reason=errors.GET_HISTORICAL_FEATURES_DEPRECATION_REASON,
        warning_message=None,  # warning message is split conditionally depending on whether a spine is provided.
    )
    @sdk_decorators.sdk_public_method
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a `TectonDataFrame` of historical values for this feature view.

        By default (i.e. `from_source=None`), this method fetches feature values from the Offline Store for input
        Feature Views that have offline materialization enabled and otherwise computes input feature values on the fly
        from raw data.

        :param spine: The spine to join against, as a dataframe.
            The returned data frame will contain rollups for all (join key, request data key)
            combinations that are required to compute a full frame from the spine.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified and this feature view has feature view dependencies, `timestamp_key` will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param from_source: Whether feature values should be recomputed from the original data source. If `None`,
            input feature values will be fetched from the Offline Store for Feature Views that have offline
            materialization enabled and otherwise computes feature values on the fly from raw data. Use
            `from_source=True` to force computing from raw data and `from_source=False` to error if any input
            Feature Views are not materialized. Defaults to None.
        :type from_source: bool
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A `TectonDataFrame`.
        """
        sources = self._check_can_query_from_source(from_source)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
            if not self._feature_definition.materialization_enabled:
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                feature_set_config=feature_set_config,
            )

        return querytree_api.get_historical_features_for_feature_definition(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=None,
            end_time=None,
            entities=None,
            from_source=from_source,
            mock_data_sources={},
        )


@realtime_feature_view_typechecked
def realtime_feature_view(
    *,
    mode: str,
    sources: List[Union[configs.RequestSource, FeatureView, "FeatureReference"]],
    features: List[feature.Attribute],
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    environments: Optional[List[str]] = None,
    context_parameter_name: Optional[str] = None,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
    required_packages: Optional[List[str]] = None,
):
    """
    Declare a Realtime Feature View.
    With Python mode, the function sources will be dictionaries, and the function is expected to return a dictionary matching the schema from `features`.
    Tecton recommends using Python mode for improved online serving performance.

    ```python
    from tecton import RequestSource, realtime_feature_view
    from tecton.types import Field, Float64, Int64

    # Define the request schema
    transaction_request = RequestSource(schema=[Field("amount", Float64)])

    # Define the output schema
    features = [Attribute("transaction_amount_is_high", Int64)]

    # This Realtime Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
    @realtime_feature_view(
        sources=[transaction_request],
        mode='python',
        features=features,
        owner='matt@tecton.ai',
        tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
        description='Whether the transaction amount is considered high (over $10000)'
    )

    def transaction_amount_is_high(transaction_request):
        result = {}
        result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
        return result
    ```

    ```python
    from tecton import RequestSource, realtime_feature_view
    from tecton.types import Field, Float64, Int64
    import pandas

    # Define the request schema
    transaction_request = RequestSource(schema=[Field("amount", Float64)])

    # Define the output schema
    features = [Attribute("transaction_amount_is_high", Int64)]

    # This Realtime Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
    @realtime_feature_view(
        sources=[transaction_request],
        mode='pandas',
        features=features,
        owner='matt@tecton.ai',
        tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
        description='Whether the transaction amount is considered high (over $10000)'
    )
    def transaction_amount_is_high(transaction_request):
        import pandas

        df = pandas.DataFrame()
        df['transaction_amount_is_high'] = (transaction_request['amount'] >= 10000).astype('int64')
        return df
    ```

    :param mode: (Required) Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("python" or "pandas" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: (Required) The data source inputs to the feature view. An input can be a RequestSource, a BatchFeatureView, or a StreamFeatureView
    :param features: (Required) A list of features this feature view manages.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
        set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
        only enforced in live (i.e. non-dev) workspaces.
    :param environments: The environments in which this feature view can run. Defaults to `None`, which means
        the feature view can run in any environment. If specified, the feature view will only run in the specified
        environments. Learn more about environments at
        [Realtime Feature View Environments](https://docs.tecton.ai/docs/defining-features/feature-views/realtime-feature-view/realtime-feature-view-environments).
    :param required_packages: A list of Python packages constraints required to run the transformation function. These list of constraints will be validated against the environment used by a transform server group at apply time.
    :param context_parameter_name: Name of the function parameter that Tecton injects Realtime Context to. This context
        is a RealtimeContext object for Python mode FVs and a pandas.DataFrame object for Pandas mode FVs.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the Realtime transformation at runtime. During local development and testing, strings may be used instead Secret references.
    :param resource_providers: A dictionary of Resource providers that will be evaluated and resources will be provided to transformation function at runtime.

    :return: An object of type `RealtimeFeatureView`.
    """

    def decorator(feature_view_function):
        if mode == NO_TRANSFORMATION_MODE_STR:
            raise errors.ModeUnsupportedForFeatureView(mode=mode, has_transformation=feature_view_function is not None)
        return RealtimeFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            mode=mode,
            sources=sources,
            features=features,
            feature_view_function=feature_view_function,
            environments=environments,
            _context_parameter_name=context_parameter_name,
            secrets=secrets,
            resource_providers=resource_providers,
            required_packages=required_packages,
        )

    return decorator


@attrs.define
class FeatureReference:
    """A reference to a Feature Definition used in Feature Service construction.

    By default, you can add all of the features in a Feature Definition (i.e. a Feature View or Feature Table) to a
    Feature Service by passing the Feature Definition into the `features` parameter of a Feature Service. However,
    if you want to specify a subset, you can use this class.

    You can use the double-bracket notation `my_feature_view[[<features>]]` as a short-hand for generating a
    FeatureReference from a Feature Defintion. This is the preferred way to select a subset of the features
    contained in a Feature Definition.

    ```python
    from tecton import FeatureService
    from feature_repo.features import my_feature_view_1, my_feature_view_2

    my_feature_service = FeatureService(
       name='my_feature_service',
       features=[
           # Add all features from my_feature_view_1 to this FeatureService
           my_feature_view_1,
           # Add a single feature from my_feature_view_2, 'my_feature'
           my_feature_view_2[['my_feature']]
       ]
    )
    ```

    :param feature_definition: The Feature View or Feature Table.
    :param namespace: A namespace used to prefix the features joined from this FeatureView. By default, namespace
        is set to the FeatureView name.
    :param features: The subset of features to select from the FeatureView. If empty, all features will be included.
    :param override_join_keys: A map from feature view join key to spine join key override.
    """

    feature_definition: FeatureView = attrs.field(on_setattr=attrs.setters.frozen, repr=utils.short_tecton_object_repr)
    namespace: str
    features: Optional[List[str]]
    override_join_keys: Optional[Dict[str, str]]

    def __init__(
        self,
        *,
        feature_definition: FeatureView,
        namespace: Optional[str] = None,
        features: Optional[List[str]] = None,
        override_join_keys: Optional[Dict[str, str]] = None,
    ):
        namespace = namespace if namespace is not None else feature_definition.name
        self.__attrs_init__(
            feature_definition=feature_definition,
            namespace=namespace,
            features=features,
            override_join_keys=override_join_keys,
        )

    @property
    def id(self) -> id_pb2.Id:
        return self.feature_definition._id_proto

    @sdk_decorators.documented_by(FeatureView.with_name)
    def with_name(self, namespace: str) -> "FeatureReference":
        self.namespace = namespace
        return self

    @sdk_decorators.documented_by(FeatureView.with_join_key_map)
    def with_join_key_map(self, join_key_map: Dict[str, str]) -> "FeatureReference":
        self.override_join_keys = join_key_map.copy()
        return self


def _validate_fv_function_inputs(
    sources: Sequence[
        Union[
            FilteredSource,
            framework_data_source.BatchSource,
            framework_data_source.StreamSource,
            configs.RequestSource,
            FeatureReference,
            FeatureView,
        ]
    ],
    feature_view_function: Optional[Callable],
    context_parameter_name: Optional[str] = None,
):
    if feature_view_function is None:
        return

    if context_parameter_name is not None:
        params = inspect.signature(feature_view_function).parameters.values()
        if not any(param.name == context_parameter_name for param in params):
            raise errors.TRANSFORMATION_CONTEXT_NAME_NOT_FOUND(context_parameter_name, feature_view_function.__name__)

    num_fn_params = _get_source_param_count(feature_view_function, context_parameter_name)
    num_sources = len(sources)
    if num_sources != num_fn_params:
        raise errors.INVALID_NUMBER_OF_FEATURE_VIEW_INPUTS(num_sources, num_fn_params)


def _validate_features(features: Sequence[Feature], fv_name: str):
    """Validates that there are no duplicate names in the list of features."""
    if features is None or len(features) == 0:
        raise errors.FeaturesRequired(fv_name)
    feature_names = [_feature.name for _feature in features if _feature.name is not None]
    seen_names = set()
    duplicate_names = []
    for name in feature_names:
        if name in seen_names:
            duplicate_names.append(name)
        seen_names.add(name)
    if duplicate_names:
        raise errors.FV_FEATURES_PARAM_HAS_DUPLICATE_NAMES(fv_name, duplicate_names)


def _get_mock_context_and_sources(
    mock_inputs: Dict[str, Any],
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: Union[feature_definition_wrapper.FeatureDefinitionWrapper],
) -> Tuple[Optional[MockContext], Dict[str, NodeRef]]:
    mock_context = None
    mock_data_sources = {}

    context_inputs = [
        v for v in mock_inputs.values() if isinstance(v, (MockContext, RealtimeContext, MaterializationContext))
    ]
    if len(context_inputs) > 1:
        msg = "Only one MockContext can be provided in mock_inputs."
        raise ValueError(msg)
    elif len(context_inputs) == 1:
        mock_context = context_inputs[0]

    source_inputs = {k: v for k, v in mock_inputs.items() if not isinstance(v, MockContext)}
    if source_inputs:
        mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
            dialect, compute_mode, feature_definition, source_inputs
        )
    return mock_context, mock_data_sources


def _validate_rtfv_no_transform_with_calculations(
    feature_view_function: Optional[Callable], features: List[feature.Feature], name: str
) -> None:
    """Disallows the edge case when a user initializes a rtfv with the __init__ method,
    provides a `feature_view_function` and a `mode`, and includes a Calculation feature. We raise an error because we
    currently do not allow Calculation features with transformations.
    """
    if feature_view_function and features and any(isinstance(feature, Calculation) for feature in features):
        msg = f"Realtime Feature View '{name}' cannot have a `feature_view_function` and a `Calculation` feature."
        raise TectonValidationError(msg)


def feature_view_from_spec(feature_view_spec: specs.FeatureViewSpec, fco_container_: fco_container.FcoContainer):
    if isinstance(feature_view_spec, specs.RealtimeFeatureViewSpec):
        return RealtimeFeatureView._from_spec(feature_view_spec, fco_container_)
    elif isinstance(feature_view_spec, specs.FeatureTableSpec):
        return FeatureTable._from_spec(feature_view_spec, fco_container_)
    elif isinstance(feature_view_spec, specs.MaterializedFeatureViewSpec):
        if feature_view_spec.data_source_type == data_source_type_pb2.DataSourceType.BATCH:
            return BatchFeatureView._from_spec(feature_view_spec, fco_container_)
        if feature_view_spec.data_source_type in (
            data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
        ):
            return StreamFeatureView._from_spec(feature_view_spec, fco_container_)
    msg = "Missing or unsupported FeatureView type."
    raise errors.INTERNAL_ERROR(msg)


def _build_realtime_sources_from_spec(
    spec: specs.RealtimeFeatureViewSpec, fco_container_: fco_container.FcoContainer
) -> List[Union[FeatureReference, configs.RequestSource]]:
    sources = []
    request_context_node = pipeline_common.get_request_context_node(spec.pipeline)
    if request_context_node is not None:
        request_schema = querytree_api.get_fields_list_from_tecton_schema(
            request_context_node.request_context.tecton_schema
        )
        sources.append(configs.RequestSource(schema=request_schema, name=request_context_node.input_name))

    feature_view_nodes = pipeline_common.get_all_feature_view_nodes(spec.pipeline)
    for node in feature_view_nodes:
        fv_spec = fco_container_.get_by_id_proto(node.feature_view_node.feature_view_id)
        fv = feature_view_from_spec(fv_spec, fco_container_)
        override_join_keys = {
            colpair.feature_column: colpair.spine_column
            for colpair in node.feature_view_node.feature_reference.override_join_keys
        }
        feature_reference = FeatureReference(
            feature_definition=fv,
            namespace=node.feature_view_node.feature_reference.namespace,
            features=node.feature_view_node.feature_reference.features,
            override_join_keys=override_join_keys,
        )
        sources.append(feature_reference)

    return sources


def _is_context_param(param: inspect.Parameter, context_parameter_name: Optional[str]) -> bool:
    if context_parameter_name is not None:
        return param.name == context_parameter_name

    return isinstance(param.default, MaterializationContext) or param.name == "context"


def _is_legacy_context_param(param: inspect.Parameter) -> bool:
    return isinstance(param.default, MaterializationContext)


def _get_source_param_count(user_function, context_parameter_name) -> int:
    params = [
        param.name
        for param in inspect.signature(user_function).parameters.values()
        if not _is_context_param(param, context_parameter_name)
    ]
    return len(params)


def _source_to_pipeline_node(
    source: Union[
        framework_data_source.DataSource,
        FilteredSource,
        configs.RequestSource,
        FeatureView,
        FeatureReference,
    ],
    input_name: str,
) -> framework_transformation.PipelineNodeWrapper:
    if isinstance(source, FeatureView):
        source = FeatureReference(feature_definition=source)

    pipeline_node = pipeline_pb2.PipelineNode()
    if isinstance(source, framework_data_source.DataSource):
        node = pipeline_pb2.DataSourceNode(
            virtual_data_source_id=source._id_proto,
            window_unbounded=True,
            schedule_offset=time_utils.timedelta_to_proto(source.data_delay),
            input_name=input_name,
        )
        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, FilteredSource):
        node = pipeline_pb2.DataSourceNode(
            virtual_data_source_id=source.source._id_proto,
            schedule_offset=time_utils.timedelta_to_proto(source.source.data_delay),
            input_name=input_name,
        )

        # Filter using select_range()
        if source.start_time is not None:
            node.filter_start_time.CopyFrom(source.start_time.to_args_proto())
            node.filter_end_time.CopyFrom(source.end_time.to_args_proto())
        # TODO(ajeya): Deprecate
        # Filter using v09_compat.FilteredSource(start_time_offset=...)
        else:
            start_time = FilterDateTime(
                time_reference=TectonTimeConstant.MATERIALIZATION_START_TIME,
            )
            end_time = FilterDateTime(
                time_reference=TectonTimeConstant.MATERIALIZATION_END_TIME,
            )
            if source.start_time_offset is not None:
                if source.start_time_offset <= MIN_START_OFFSET:
                    start_time = FilterDateTime(
                        time_reference=TectonTimeConstant.UNBOUNDED_PAST,
                    )
                else:
                    start_time = FilterDateTime(
                        time_reference=TectonTimeConstant.MATERIALIZATION_START_TIME,
                        offset=source.start_time_offset,
                    )
            node.filter_start_time.CopyFrom(start_time.to_args_proto())
            node.filter_end_time.CopyFrom(end_time.to_args_proto())

        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, configs.RequestSource):
        request_schema = source.schema
        schema_proto = type_utils.to_tecton_schema(request_schema)

        node = pipeline_pb2.RequestDataSourceNode(
            request_context=pipeline_pb2.RequestContext(tecton_schema=schema_proto),
            input_name=input_name,
        )
        pipeline_node.request_data_source_node.CopyFrom(node)
    elif isinstance(source, FeatureReference):
        override_join_keys = None
        if source.override_join_keys:
            override_join_keys = [
                feature_service_pb2.ColumnPair(spine_column=spine_key, feature_column=fv_key)
                for fv_key, spine_key in sorted(source.override_join_keys.items())
            ]
        node = pipeline_pb2.FeatureViewNode(
            feature_view_id=source.id,
            input_name=input_name,
            feature_reference=feature_service_pb2.FeatureReference(
                feature_view_id=source.id,
                override_join_keys=override_join_keys,
                namespace=source.namespace,
                features=source.features,
            ),
        )
        pipeline_node.feature_view_node.CopyFrom(node)
    else:
        msg = f"Invalid source type: {type(source)}"
        raise TypeError(msg)
    return framework_transformation.PipelineNodeWrapper(node_proto=pipeline_node)


SourceType = Union[
    framework_data_source.DataSource,
    FilteredSource,
    configs.RequestSource,
    FeatureView,
    FeatureReference,
]


def _build_join_inputs_pipeline(
    sources: List[SourceType], context_parameter_name: str, features: List[feature.Feature]
) -> PipelineNodeWrapper:
    input_nodes = [_source_to_pipeline_node(source, _get_name_for_source(source)).node_proto for source in sources]

    # include the context pipeline node for no-tranform rtfv if context_parameter_name is referenced in a feature
    if _context_referenced_in_features(context_parameter_name, features):
        context_node = _build_context_pipeline_node(context_parameter_name=context_parameter_name)
        input_nodes.append(context_node)

    pipeline_node = pipeline_pb2.PipelineNode()
    join_inputs_node = pipeline_pb2.JoinInputsNode(nodes=input_nodes)
    pipeline_node.join_inputs_node.CopyFrom(join_inputs_node)
    return framework_transformation.PipelineNodeWrapper(node_proto=pipeline_node)


def _context_referenced_in_features(context_parameter_name: str, features: List[feature.Feature]) -> bool:
    calculation_pattern = re.compile(re.escape(context_parameter_name + CALCULATION_COLUMN_REFERENCE_DELIMITER))
    attribute_pattern = re.compile(re.escape(context_parameter_name + ATTRIBUTE_COLUMN_REFERENCE_DELIMITER))

    for feature_ in features:
        if isinstance(feature_, Calculation):
            if calculation_pattern.search(feature_.expr):
                return True
        elif isinstance(feature_, Attribute):
            if attribute_pattern.search(feature_.name):
                return True
        else:
            msg = f"Unexpected feature type: {type(feature_)} in context_parameter_name search."
            raise ValueError(msg)
    return False


def _build_context_pipeline_node(context_parameter_name: str) -> PipelineNode:
    context_node = pipeline_pb2.ContextNode(
        context_type=pipeline_pb2.ContextType.CONTEXT_TYPE_REALTIME,
        input_name=context_parameter_name,
    )
    pipeline_node = pipeline_pb2.PipelineNode()
    pipeline_node.context_node.CopyFrom(context_node)
    return pipeline_node


def _get_name_for_source(source: SourceType) -> str:
    # we only want to use source.name if the name is set, not if the name is None.
    # cannot use walrus operator because we need to support Python 3.7.
    if hasattr(source, "name") and source.name:
        return source.name
    elif hasattr(source, "namespace"):
        return source.namespace
    errorMsg = f'Source of type {source.__class__.__name__} must have "name" or "namespace" set'
    raise ValueError(errorMsg)


def _test_binding_user_function(fn, inputs):
    # this function binds the top-level pipeline function only, for transformation binding, see transformation.__call__
    pipeline_signature = inspect.signature(fn)
    try:
        pipeline_signature.bind(**inputs)
    except TypeError as e:
        msg = f"while binding inputs to pipeline function, TypeError: {e}"
        raise TypeError(msg)


def _build_default_cluster_config():
    return feature_view__args_pb2.ClusterConfig(
        implicit_config=feature_view__args_pb2.DefaultClusterConfig(
            **{
                **configs.DEFAULT_SPARK_VERSIONS,
                **configs.TECTON_COMPUTE_DEFAULTS,
            }
        )
    )


_SPARK_MODES = {
    transformation_pb2.TRANSFORMATION_MODE_PYSPARK,
    transformation_pb2.TRANSFORMATION_MODE_SPARK_SQL,
}


def _is_spark_config(config: Optional[configs.ComputeConfigTypes]) -> bool:
    if config is None:
        return False
    # This looks silly right now because it's all the possible types, but soon there will be e.g. a TectonComputeConfig
    # for managed compute.
    return isinstance(
        config,
        (
            configs.DatabricksClusterConfig,
            configs.EMRClusterConfig,
            configs.DatabricksJsonClusterConfig,
            configs.EMRJsonClusterConfig,
        ),
    )


def infer_batch_compute_mode(
    pipeline_root: Optional[PipelineNodeWrapper],
    batch_compute_config: configs.ComputeConfigTypes,
    stream_compute_config: Optional[configs.ComputeConfigTypes],
) -> BatchComputeMode:
    has_spark_config = any(_is_spark_config(c) for c in (batch_compute_config, stream_compute_config))
    transformations = pipeline_root.transformations if pipeline_root is not None else []
    has_spark_transforms = any(t.transformation_mode in _SPARK_MODES for t in transformations)
    if has_spark_config or has_spark_transforms:
        return BatchComputeMode.SPARK
    else:
        return default_batch_compute_mode()


@typechecked
def _build_materialized_feature_view_args(
    name: str,
    pipeline_root: PipelineNodeWrapper,
    entities: Sequence[framework_entity.Entity],
    online: bool,
    offline: bool,
    offline_store: configs.OfflineStoreConfig,
    online_store: Optional[configs.OnlineStoreTypes],
    aggregation_interval: Optional[datetime.timedelta],
    aggregation_secondary_key: Optional[str],
    features: Sequence[feature.Feature],
    ttl: Optional[datetime.timedelta],
    feature_start_time: Optional[datetime.datetime],
    lifetime_start_time: Optional[datetime.datetime],
    manual_trigger_backfill_end_time: Optional[datetime.datetime],
    batch_schedule: Optional[datetime.timedelta],
    online_serving_index: Optional[Sequence[str]],
    batch_compute: configs.ComputeConfigTypes,
    stream_compute: Optional[configs.ComputeConfigTypes],
    monitor_freshness: bool,
    data_quality_enabled: Optional[bool],
    skip_default_expectations: Optional[bool],
    expected_feature_freshness: Optional[datetime.timedelta],
    alert_email: Optional[str],
    description: Optional[str],
    owner: Optional[str],
    tags: Optional[Dict[str, str]],
    feature_view_type: feature_view__args_pb2.FeatureViewType.ValueType,
    data_source_type: data_source_type_pb2.DataSourceType.ValueType,
    incremental_backfills: bool,
    prevent_destroy: bool,
    timestamp_field: str,
    publish_features_config: Optional[vnext.PublishFeaturesConfig] = None,
    run_transformation_validation: Optional[bool] = None,
    stream_processing_mode: Optional[StreamProcessingMode] = None,
    max_backfill_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[configs.OutputStream] = None,
    batch_trigger: Optional[BatchTriggerType] = None,
    options: Optional[Dict[str, str]] = None,
    tecton_materialization_runtime: Optional[str] = None,
    cache_config: Optional[configs.CacheConfig] = None,
    compaction_enabled: bool = False,
    stream_tiling_enabled: bool = False,
    environment: Optional[str] = None,
    transform_server_group: Optional[str] = None,
    context_parameter_name: Optional[str] = None,
    aggregation_leading_edge: Optional[AggregationLeadingEdge] = None,
    framework_version: Optional[FrameworkVersion] = None,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    resource_providers: Optional[Dict[str, resource_provider.ResourceProvider]] = None,
) -> feature_view__args_pb2.FeatureViewArgs:
    """Build feature view args proto for materialized feature views (i.e. batch and stream feature views)."""
    monitoring = configs.MonitoringConfig(
        monitor_freshness=monitor_freshness, expected_freshness=expected_feature_freshness, alert_email=alert_email
    )

    aggregation_protos = None
    attribute_protos = None
    embedding_protos = None
    inference_protos = None
    secondary_key_output_columns = None
    # push sources are not yet supported for stream compaction
    is_streaming_fv = data_source_type in {data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH}
    if all(isinstance(f, feature.Aggregate) for f in features):
        is_continuous = stream_processing_mode == StreamProcessingMode.CONTINUOUS
        if aggregation_interval is None:
            aggregation_interval = datetime.timedelta(seconds=0)

        aggregation_protos = [
            agg._to_proto(aggregation_interval, is_continuous, compaction_enabled, is_streaming_fv) for agg in features
        ]
        if aggregation_secondary_key:
            secondary_key_output_columns = _create_secondary_key_output_columns(features, aggregation_secondary_key)
    else:
        attribute_protos = [f._to_proto() for f in features if isinstance(f, feature.Attribute)]
        embedding_protos = [f._to_proto() for f in features if isinstance(f, feature.Embedding)]
        inference_protos = [f._to_proto() for f in features if isinstance(f, feature.Inference)]
        if any(isinstance(f, feature.Aggregate) for f in features):
            msg = "`features` param should be either List[Aggregate] or List[Union[Attribute, Embedding]]"
            raise TectonValidationError(msg)

    feature_store_format_version = FeatureStoreFormatVersion.NANOSECONDS  # NANOSECONDS
    if isinstance(online_store, (configs.DynamoConfig, configs.RedisConfig)) or not online_store:
        feature_store_format_version = FeatureStoreFormatVersion.TTL

    secret_references = {}
    if secrets:
        for secret_name, secret in secrets.items():
            secret_references[secret_name] = convert_secret_to_sanitized_reference(secret)

    # TODO(TEC-17296): populate default value for tecton_materialization_runtime from repo config
    return feature_view__args_pb2.FeatureViewArgs(
        feature_view_id=id_helper.IdHelper.generate_id(),
        version=framework_version.value,
        info=basic_info_pb2.BasicInfo(name=name, description=description, owner=owner, tags=tags),
        prevent_destroy=prevent_destroy,
        entities=[
            feature_view__args_pb2.EntityKeyOverride(entity_id=entity._id_proto, join_keys=entity.join_keys)
            for entity in entities
        ],
        pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
        feature_view_type=feature_view_type,
        online_serving_index=online_serving_index if online_serving_index else None,
        online_enabled=online,
        offline_enabled=offline,
        data_quality_config=feature_view__args_pb2.DataQualityConfig(
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
        ),
        batch_compute_mode=infer_batch_compute_mode(
            pipeline_root=pipeline_root, batch_compute_config=batch_compute, stream_compute_config=stream_compute
        ).value,
        materialized_feature_view_args=feature_view__args_pb2.MaterializedFeatureViewArgs(
            feature_start_time=time_utils.datetime_to_proto(feature_start_time),
            lifetime_start_time=time_utils.datetime_to_proto(lifetime_start_time),
            manual_trigger_backfill_end_time=time_utils.datetime_to_proto(manual_trigger_backfill_end_time),
            batch_schedule=time_utils.timedelta_to_proto(batch_schedule),
            online_store=online_store._to_proto() if online_store else None,
            max_backfill_interval=time_utils.timedelta_to_proto(max_backfill_interval),
            monitoring=monitoring._to_proto(),
            data_source_type=data_source_type,
            aggregation_secondary_key=aggregation_secondary_key,
            secondary_key_output_columns=secondary_key_output_columns,
            incremental_backfills=incremental_backfills,
            batch_trigger=batch_trigger.value,
            output_stream=output_stream._to_proto() if output_stream else None,
            batch_compute=batch_compute._to_cluster_proto(),
            stream_compute=stream_compute._to_cluster_proto() if stream_compute else None,
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            stream_processing_mode=stream_processing_mode.value if stream_processing_mode else None,
            aggregations=aggregation_protos,
            aggregation_interval=time_utils.timedelta_to_proto(aggregation_interval),
            schema=None,
            run_transformation_validation=run_transformation_validation,
            tecton_materialization_runtime=tecton_materialization_runtime,
            offline_store=offline_store._to_proto(),
            stream_tiling_enabled=stream_tiling_enabled,
            stream_tile_size=_compute_compacted_fv_stream_tile_size(features) if stream_tiling_enabled else None,
            compaction_enabled=compaction_enabled,
            environment=environment,
            transform_server_group=transform_server_group,
            attributes=attribute_protos,
            embeddings=embedding_protos,
            inferences=inference_protos,
            aggregation_leading_edge=aggregation_leading_edge.value if aggregation_leading_edge else None,
            feature_store_format_version=feature_store_format_version.value,
            publish_features_configs=publish_features_config._to_proto() if publish_features_config else None,
            batch_publish_timestamp=options.get("BATCH_PUBLISH_TIMESTAMP") if options else None,
            timestamp_field=timestamp_field,
        ),
        secrets=secret_references,
        resource_providers={
            name_override: resource_provider._id_proto
            for name_override, resource_provider in resource_providers.items()
        }
        if resource_providers
        else {},
        options=options,
        cache_config=cache_config._to_proto() if cache_config else None,
        context_parameter_name=context_parameter_name,
    )


def _create_secondary_key_output_columns(
    aggregations: Sequence[configs.Aggregation, feature.Aggregate], aggregation_secondary_key: str
) -> List[feature_view__args_pb2.SecondaryKeyOutputColumn]:
    secondary_time_windows: Sequence[specs.TimeWindowSpec] = sorted(
        # eliminates duplicates of time windows for secondary key output columns
        {agg.time_window._to_spec() for agg in aggregations},
        key=lambda tw: tw.to_sort_tuple(),
        reverse=True,
    )

    secondary_key_output_columns = []
    for window in secondary_time_windows:
        name = f"{aggregation_secondary_key}_keys_{window.to_string()}".replace(" ", "")
        if isinstance(window, LifetimeWindowSpec):
            output_col = feature_view__args_pb2.SecondaryKeyOutputColumn(
                lifetime_window=window.to_proto(),
                name=name,
            )
        elif isinstance(window, RelativeTimeWindowSpec):
            output_col = feature_view__args_pb2.SecondaryKeyOutputColumn(
                time_window=window.to_args_proto(),
                name=name,
            )
        elif isinstance(window, TimeWindowSeriesSpec):
            output_col = feature_view__args_pb2.SecondaryKeyOutputColumn(
                time_window_series=window.to_args_proto(),
                name=name,
            )
        else:
            msg = f"Unexpected time window type in agg args proto: {type(window)}"
            raise ValueError(msg)
        secondary_key_output_columns.append(output_col)
    return secondary_key_output_columns


def _compute_compacted_fv_stream_tile_size(
    features: Optional[Sequence[Feature]],
) -> Optional[duration_pb2.Duration]:
    """Calculate the compacted fv stream tile size.

    Only applicable for fvs with stream_tiling_enabled=True. This calculates the tile size used for the online stream table. Currently, this cannot be set by the user.
    """
    aggregates = [feature for feature in features if isinstance(feature, Aggregate)]
    if not aggregates:
        msg = "Only feature views with aggregates can set `stream_tiling_enabled`=True"
        raise ValueError(msg)

    relative_time_windows = []
    for agg in aggregates:
        if isinstance(agg.time_window, configs.TimeWindow):
            relative_time_windows.append(agg.time_window)
        elif isinstance(agg.time_window, configs.TimeWindowSeries):
            raise errors.COMPACTION_TIME_WINDOW_SERIES_UNSUPPORTED()

    if relative_time_windows:
        min_time_window = min([window.window_size for window in relative_time_windows])
        if min_time_window < timedelta(hours=1):
            return time_utils.timedelta_to_proto(timedelta(minutes=1))
        elif min_time_window < timedelta(hours=10):
            return time_utils.timedelta_to_proto(timedelta(minutes=5))

    return time_utils.timedelta_to_proto(timedelta(hours=1))


def _compute_default_stream_processing_mode(
    has_push_source: bool,
    features: Optional[Sequence[feature.Feature]],
    compaction_enabled: bool,
    stream_tiling_enabled: Optional[bool] = None,
):
    if has_push_source:
        # Stream Feature Views with Push Sources default to continuous-mode only.
        return StreamProcessingMode.CONTINUOUS
    elif compaction_enabled:
        # This is a Compacted stream feature view. We set defaults here for compacted feature views. The actual validations
        # will be in the validation server.
        return StreamProcessingMode.CONTINUOUS if not stream_tiling_enabled else None
    elif features:
        has_aggregate_features = bool([_feature for _feature in features if isinstance(_feature, Aggregate)])
        if has_aggregate_features:
            return StreamProcessingMode.TIME_INTERVAL
    return None


def _fetch_model(model_name: str) -> Optional[model_artifact_data_pb2.ModelArtifactInfo]:
    try:
        artifacts = (
            metadata_service.instance()
            .ListModelArtifacts(model_artifact_service_pb2.ListModelArtifactsRequest(name=model_name))
            .models
        )
        if len(artifacts) == 0:
            return None
        elif len(artifacts) > 1:
            msg = f"More than one model found with name: {model_name}"
            raise errors.TectonInternalError(msg)
        return artifacts[0]
    except Exception as e:
        msg = f"Failed to fetch model metadata for model {model_name} : {e}"
        raise errors.TectonValidationError(msg)

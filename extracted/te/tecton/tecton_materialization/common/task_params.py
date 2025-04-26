import datetime
import functools
import itertools
import re
import typing
from typing import List
from typing import Union

import tecton_core.tecton_pendulum as pendulum
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.fco_container import DataProto
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


SENSITIVE_FIELDS = ["authenticationToken", "secret_access_api_key"]


@functools.lru_cache(maxsize=0)
def feature_definition_from_task_params(params: MaterializationTaskParams) -> FeatureDefinitionWrapper:
    if not params.HasField("feature_view"):
        msg = "'feature_view' must be set in MaterializationTaskParams"
        raise ValueError(msg)

    fco_container = create_fco_container(
        itertools.chain(
            *(
                # The cast helps out various type inference implementations which otherwise would complain that
                # the different FCO lists are not the same type
                typing.cast(typing.Iterable[DataProto], p)
                for p in (
                    params.virtual_data_sources,
                    params.transformations,
                    params.entities,
                    params.resource_providers,
                )
            )
        ),
        include_main_variables_in_scope=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(params.feature_view)
    return FeatureDefinitionWrapper(fv_spec, fco_container)


# Return a list of FeatureDefinitionWrappers of the Feature Service.
@functools.lru_cache(maxsize=0)
def feature_definition_from_feature_service_task_params(
    params: MaterializationTaskParams,
) -> List[FeatureDefinitionWrapper]:
    if not params.feature_views:
        msg = "'feature_views' must be set in MaterializationTaskParams"
        raise ValueError(msg)

    fco_container = create_fco_container(
        itertools.chain(
            *(
                # The cast helps out various type inference implementations which otherwise would complain that
                # the different FCO lists are not the same type
                typing.cast(typing.Iterable[DataProto], p)
                for p in (
                    params.virtual_data_sources,
                    params.transformations,
                    params.entities,
                    params.resource_providers,
                )
            )
        ),
        include_main_variables_in_scope=True,
    )
    return [
        FeatureDefinitionWrapper(specs.create_feature_view_spec_from_data_proto(feature_view), fco_container)
        for feature_view in params.feature_views
    ]


@functools.lru_cache(maxsize=0)
def feature_service_from_task_params(params: MaterializationTaskParams) -> specs.FeatureServiceSpec:
    if not params.HasField("feature_service"):
        msg = "'feature_service' must be set in MaterializationTaskParams"
        raise ValueError(msg)

    return specs.FeatureServiceSpec.from_data_proto(params.feature_service)


@functools.lru_cache(maxsize=0)
def feature_set_config_from_task_params(params: MaterializationTaskParams) -> FeatureSetConfig:
    if not params.HasField("feature_service"):
        msg = "'feature_service' must be set in MaterializationTaskParams"
        raise ValueError(msg)

    fco_container = create_fco_container(
        itertools.chain(
            *(
                # The cast helps out various type inference implementations which otherwise would complain that
                # the different FCO lists are not the same type
                typing.cast(typing.Iterable[DataProto], p)
                for p in (
                    params.virtual_data_sources,
                    params.transformations,
                    params.entities,
                    params.feature_views,
                    params.resource_providers,
                )
            )
        ),
        include_main_variables_in_scope=True,
    )
    fs_spec = feature_service_from_task_params(params)
    return FeatureSetConfig.from_feature_service_spec(fs_spec, fco_container)


def get_features_params_from_task_params(
    params: MaterializationTaskParams,
    compute_mode: ComputeMode,
) -> Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams]:
    dataset_generation_params = params.dataset_generation_task_info.dataset_generation_parameters
    if dataset_generation_params.WhichOneof("input") == "spine":
        spine = dataset_generation_params.spine

        if params.HasField("feature_view"):
            fco = feature_definition_from_task_params(params)
            feature_set_config = None
        elif params.HasField("feature_service"):
            fco = feature_service_from_task_params(params)
            feature_set_config = feature_set_config_from_task_params(params)
        else:
            msg = "Either feature_view or feature_service must be set in MaterializationTaskParams"
            raise ValueError(msg)

        return GetFeaturesForEventsParams(
            fco=fco,
            events=spine.path,
            timestamp_key=spine.timestamp_key if spine.HasField("timestamp_key") else None,
            from_source=dataset_generation_params.from_source
            if dataset_generation_params.HasField("from_source") and dataset_generation_params.from_source == True
            else None,
            compute_mode=compute_mode,
            feature_set_config=feature_set_config,
        )
    elif dataset_generation_params.WhichOneof("input") == "datetime_range":
        datetime_range = dataset_generation_params.datetime_range
        start_time = datetime_range.start.ToDatetime()
        end_time = datetime_range.end.ToDatetime()
        max_lookback_time = (
            datetime_range.max_lookback.ToDatetime() if datetime_range.HasField("max_lookback") else None
        )
        entities = datetime_range.entities_path if datetime_range.HasField("entities_path") else None
        return GetFeaturesInRangeParams(
            fco=feature_definition_from_task_params(params),
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            max_lookback=(max_lookback_time - start_time) if max_lookback_time else None,
            from_source=dataset_generation_params.from_source
            if dataset_generation_params.HasField("from_source")
            else None,
            compute_mode=compute_mode,
        )
    else:
        error = "Invalid dataset_generation_params"
        raise ValueError(error)


class TimeInterval(typing.NamedTuple):
    start: datetime.datetime
    end: datetime.datetime

    def to_pendulum(self) -> pendulum.Period:
        return pendulum.instance(self.end) - pendulum.instance(self.start)


def _backfill_job_periods(
    start_time: datetime.datetime, end_time: datetime.datetime, interval: datetime.timedelta
) -> List[TimeInterval]:
    jobs = []
    while start_time < end_time:
        jobs.append(TimeInterval(start_time, start_time + interval))
        start_time = start_time + interval
    assert start_time == end_time, "Start and end times were not aligned to `interval`"
    return jobs


def job_query_intervals(task_params: MaterializationTaskParams) -> typing.List[TimeInterval]:
    """
    Return a list of start/end tuples of size batch_schedule.
    For use of breaking up a large backfill window into incremental sizes.
    """
    fd = feature_definition_from_task_params(task_params)
    assert task_params.batch_task_info.HasField("batch_parameters")
    task_feature_start_time = task_params.batch_task_info.batch_parameters.feature_start_time.ToDatetime()
    task_feature_end_time = task_params.batch_task_info.batch_parameters.feature_end_time.ToDatetime()
    # for incremental backfills, we split the job into each batch interval
    if fd.is_incremental_backfill:
        return _backfill_job_periods(task_feature_start_time, task_feature_end_time, fd.batch_materialization_schedule)
    else:
        return [TimeInterval(task_feature_start_time, task_feature_end_time)]


def redact_sensitive_fields_from_params(message_json: str):
    for field_name in SENSITIVE_FIELDS:
        message_json = re.sub(rf'"{field_name}": ".*?"', f'"{field_name}": "<REDACTED>"', message_json)
    return message_json

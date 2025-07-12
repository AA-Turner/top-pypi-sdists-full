import io
import time
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas

from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.display import Displayable
from tecton._internals.ingest_utils import upload
from tecton_core import specs
from tecton_core.arrow import PARQUET_WRITE_OPTIONS_KWARGS
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.data_processing_utils import infer_pandas_timestamp
from tecton_core.errors import TectonValidationError
from tecton_core.id_helper import IdHelper
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.schema import Schema
from tecton_proto.args.feature_view__client_pb2 import ClusterConfig
from tecton_proto.common import id__client_pb2 as id_pb2
from tecton_proto.data.materialization_status__client_pb2 import MaterializationStatus
from tecton_proto.materialization.spark_cluster__client_pb2 import TaskType
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import CancelDatasetJobRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import CancelJobRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import (
    CompleteDataframeUploadRequest,
)
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import GetDataframeUploadUrlRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import GetDatasetJobRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import GetJobRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import GetLatestReadyTimeRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import GetLatestReadyTimeResponse
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import JobAttempt
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import ListJobsRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import (
    MaterializationJob as MaterializationJobProto,
)
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import MaterializationJobRequest
from tecton_proto.materializationjobservice.materialization_job_service__client_pb2 import StartDatasetJobRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import GetJobStatusRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import GetMaterializationStatusRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import GetSavedFeatureDataFrameRequest


if TYPE_CHECKING:
    from tecton.framework.dataset import SavedDataset


class JobTimeoutException(Exception):
    pass


class JobFailedException(Exception):
    pass


WAIT_INTERVAL = timedelta(seconds=60)


@dataclass
class MaterializationAttempt:
    """
    Data representation of the materialization job attempt.

    Materialization job may have multiple attempts to materialize features.

    :param id: ID string of the materialization attempt.
    :param run_url: URL to track materialization attempt.
    :param state: State of the materialization attempt.
    :param created_at: Materialization attempt creation timestamp.
    :param updated_at: Materialization attempt update timestamp.
    """

    id: str
    run_url: str
    state: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def _from_proto(cls, proto: JobAttempt):
        created_at = datetime.utcfromtimestamp(proto.created_at.seconds)
        updated_at = datetime.utcfromtimestamp(proto.updated_at.seconds)
        return cls(id=proto.id, run_url=proto.run_url, state=proto.state, created_at=created_at, updated_at=updated_at)


@dataclass
class TectonJob:
    """
    Base class for Tecton jobs executed remotely by Tecton compute
    """

    id: str
    workspace: str
    feature_view: Optional[str]
    feature_service: Optional[str]
    state: str
    created_at: datetime
    updated_at: datetime
    attempts: List[MaterializationAttempt]
    next_attempt_at: Optional[datetime]
    job_type: str

    @classmethod
    def _from_proto(cls, proto: MaterializationJobProto):
        if proto.HasField("saved_feature_data_frame"):
            return DatasetJob._from_proto(proto)

        return MaterializationJob._from_proto(proto)

    def cancel(self) -> "TectonJob":
        """
        Cancels the scheduled or running job by the job identifier.
        Once cancelled, a job will not be retried further.

        Job run state will be set to MANUAL_CANCELLATION_REQUESTED.
        Note that cancellation is asynchronous, so it may take some time for the cancellation to complete.
        If job run is already in MANUAL_CANCELLATION_REQUESTED or in a terminal state then it'll return the job.

        :param job_id: ID string of the materialization job.
        :return: `JobData` object for the cancelled job.
        """
        return cancel_job(self.workspace, self.id, feature_view=self.feature_view, feature_service=self.feature_service)

    @abstractmethod
    def get_status_for_display(self) -> Displayable: ...


@dataclass
class MaterializationJob(TectonJob):
    """
    Representation of the materialization job

    :param id: ID string of the materialization job.
    :param workspace: Name of the project workspace.
    :param feature_view: Name of the Feature View (if job attached to a feature view).
    :param feature_service: Name of the Feature Service (if job attached to a feature service).
    :param state: State of the materialization job.
    :param online: Whether the job materializes features to the online store.
    :param offline: Whether the job materializes features to the offline store.
    :param start_time: Start timestamp of the batch materialization window.
    :param end_time: End timestamp of the batch materialization window.
    :param created_at: Job creation timestamp.
    :param updated_at: Job update timestamp.
    :param attempts: Materialization attempts. List of `MaterializationAttemptData`
    :param next_attempt_at: If job needs another attempt, Start timestamp the next materialization attempt.
    :param job_type: Type of materialization. One of 'BATCH' or 'STREAM'.
    """

    online: bool
    offline: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    @classmethod
    def _from_proto(cls, proto: MaterializationJobProto):
        start_time = datetime.utcfromtimestamp(proto.start_time.seconds) if proto.HasField("start_time") else None
        end_time = datetime.utcfromtimestamp(proto.end_time.seconds) if proto.HasField("end_time") else None
        created_at = datetime.utcfromtimestamp(proto.created_at.seconds)
        updated_at = datetime.utcfromtimestamp(proto.updated_at.seconds)
        attempts = [MaterializationAttempt._from_proto(attempt_proto) for attempt_proto in proto.attempts]
        next_attempt_at = (
            datetime.utcfromtimestamp(proto.next_attempt_at.seconds) if proto.HasField("next_attempt_at") else None
        )
        return cls(
            id=proto.id,
            workspace=proto.workspace,
            feature_view=proto.feature_view if proto.HasField("feature_view") else None,
            feature_service=proto.feature_service if proto.HasField("feature_service") else None,
            state=proto.state,
            online=proto.online,
            offline=proto.offline,
            start_time=start_time,
            end_time=end_time,
            created_at=created_at,
            updated_at=updated_at,
            attempts=attempts,
            next_attempt_at=next_attempt_at,
            job_type=proto.job_type,
        )

    def __repr__(self):
        return f"MaterializationJob {self.id}"

    def get_status_for_display(self) -> Displayable:
        """
        Returns a user-friendly representation of this job's status (with attempts).
        """
        status = get_job_status(IdHelper.from_string(self.id), self.workspace)
        column_names, materialization_status_rows = utils.format_materialization_attempts(
            status.materialization_attempts,
            verbose=True,
        )
        return _create_materialization_table(column_names, materialization_status_rows)


@dataclass
class DatasetJob(TectonJob):
    """
    Representation of dataset generation job

    :param id: ID string of the materialization job.
    :param workspace: Name of the project workspace.
    :param feature_view: Name of the Feature View (if job attached to a feature view).
    :param feature_service: Name of the Feature Service (if job attached to a feature service).
    :param state: State of the materialization job.
    :param created_at: Job creation timestamp.
    :param updated_at: Job update timestamp.
    :param attempts: Materialization attempts. List of `MaterializationAttemptData`
    :param next_attempt_at: If job needs another attempt, Start timestamp the next materialization attempt.
    :param job_type: Type of materialization. For now only one value is expected 'DATASET_GENERATION'.
    :param dataset: Name of the Dataset.
    """

    dataset: str

    def __repr__(self):
        return f"DatasetJob {self.id}"

    def _repr_html_(self):
        """Controls what is shown in a Jupyter or Databricks Notebook"""
        if self.feature_view:
            object_type = "FeatureView"
            object_name = self.feature_view
        else:
            object_type = "FeatureService"
            object_name = self.feature_service
        attempts_html = ""
        for attempt in self.attempts:
            attempts_html += f'<li><a href="{attempt.run_url}" target="_blank">{attempt.id}</a></li>'

        footer = (
            '<p style="margin-top:1em;"><em>Call <code>get_dataset()</code> to retrieve dataset.</em></p>'
            if self.state.upper() == "SUCCESS"
            else ""
        )

        html = f"""
        <div style="font-family: sans-serif; line-height: 1.4;">
            <strong>DatasetJob</strong> <code>{self.id}</code> </h3>
            <p>
            <strong>{object_type}:</strong> <code>{object_name}</code><br>
            <strong>Dataset:</strong> <code>{self.dataset}</code><br>
            <strong>State:</strong> {self.state}<br>
            <p><strong>Attempts:</strong></p>
            <ul>
                {attempts_html}
            </ul>
            {footer}
        </div>
        """
        return html

    @classmethod
    def _from_proto(cls, proto: MaterializationJobProto):
        created_at = datetime.utcfromtimestamp(proto.created_at.seconds)
        updated_at = datetime.utcfromtimestamp(proto.updated_at.seconds)
        attempts = [MaterializationAttempt._from_proto(attempt_proto) for attempt_proto in proto.attempts]
        next_attempt_at = (
            datetime.utcfromtimestamp(proto.next_attempt_at.seconds) if proto.HasField("next_attempt_at") else None
        )
        return cls(
            id=proto.id,
            workspace=proto.workspace,
            feature_view=proto.feature_view if proto.HasField("feature_view") else None,
            feature_service=proto.feature_service if proto.HasField("feature_service") else None,
            dataset=proto.saved_feature_data_frame,
            state=proto.state,
            created_at=created_at,
            updated_at=updated_at,
            attempts=attempts,
            next_attempt_at=next_attempt_at,
            job_type=proto.job_type,
        )

    def wait_for_completion(self, timeout: Optional[timedelta] = None):
        """
        Blocks until the job has been completed.

        :param timeout: (Optional) timeout for this function.
            An exception is raised if the job does not complete within the specified time.
        """
        self.state = wait_for_dataset_job(self.workspace, self.id, self.dataset, timeout=timeout).state

    def get_dataset(self) -> Optional["SavedDataset"]:
        """
        Retrieves the dataset instance after the job is completed.

        :return: `SavedDataset` object if the job has finished successfully. Otherwise, returns None.
        """
        from tecton.framework.dataset import SavedDataset

        self.state = get_dataset_job(self.workspace, self.id, self.dataset).state

        if self.state != "SUCCESS":
            return

        request = GetSavedFeatureDataFrameRequest(saved_feature_dataframe_name=self.dataset, workspace=self.workspace)
        response = metadata_service.instance().GetSavedFeatureDataFrame(request)
        return SavedDataset._from_proto(response.saved_feature_dataframe)

    def get_status_for_display(self) -> Displayable:
        """
        Returns a user-friendly representation of this job's status (with attempts).
        """
        status = get_job_status(IdHelper.from_string(self.id), self.workspace)
        column_names, materialization_status_rows = utils.format_materialization_attempts(
            status.materialization_attempts,
            override_columns=[
                "TYPE",
                "STATUS",
                "ATTEMPT",
                "ENV_VERSION",
                "TERMINATION_REASON",
                "STATE_MESSAGE",
                "TASK_SCHEDULED_AT",
                "JOB_LOGS",
            ],
        )
        return _create_materialization_table(column_names, materialization_status_rows)


def trigger_materialization_job(
    feature_view: str,
    workspace: str,
    start_time: datetime,
    end_time: datetime,
    online: bool,
    offline: bool,
    use_tecton_managed_retries: bool = True,
    overwrite: bool = False,
) -> str:
    """
    Starts a batch materialization job for this Feature View.

    :param start_time: The job will materialize feature values between the start_time and end_time.
    :param end_time: The job will materialize feature values between the start_time and end_time.
    :param online: Whether the job will materialize features to the online store.
        The Feature View must be configured with online=True in order to materialize features online.
    :param offline: Whether the job will materialize features to the offline store.
        The Feature View must be configured with offline=True in order to materialize features offline.
    :param use_tecton_managed_retries: If enabled, Tecton will automatically retry failed attempts.
        Disable to manage your own retry behavior.
    :param overwrite: If enabled, you will be able to run materialization jobs for periods that previously have materialized data.
        This operation can be sensitive for feature views with existing materialized online data.
        For the offline store, all previously materialized data between the start time and end time will be dropped.
        For the online store, all previous data will remain, but may be overwritten by this job.
    :return: ID string of the created materialization job.
    :raises TectonValidationError: If job params are not valid.
    """
    request = MaterializationJobRequest()
    request.feature_view = feature_view
    request.workspace = workspace
    request.start_time.FromDatetime(start_time)
    request.end_time.FromDatetime(end_time)
    request.online = online
    request.offline = offline
    request.use_tecton_managed_retries = use_tecton_managed_retries
    request.overwrite = overwrite

    mds_instance = metadata_service.instance()
    response = mds_instance.SubmitMaterializationJob(request)
    return response.job.id


def list_jobs(
    workspace: str, feature_view: Optional[str] = None, feature_service: Optional[str] = None
) -> List[TectonJob]:
    """
    Retrieves the list of all jobs for the provided feature view or feature service.
    :return: List of `JobData` objects.
    """
    assert (feature_view is not None) ^ (feature_service is not None), (
        "Either feature_view or feature_service must be provided. Not both."
    )

    request = ListJobsRequest()
    if feature_view:
        request.feature_view = feature_view
    if feature_service:
        request.feature_service = feature_service
    request.workspace = workspace

    mds_instance = metadata_service.instance()
    response = mds_instance.ListMaterializationJobs(request)
    return [TectonJob._from_proto(job) for job in response.jobs]


def get_job(
    workspace: str, job_id: str, feature_view: Optional[str] = None, feature_service: Optional[str] = None
) -> TectonJob:
    """
    Retrieves data about the specified job for the provided feature view or feature service.

    This data includes information about job attempts.

    :param job_id: ID string of the materialization job.
    :return: `JobData` object for the job.
    """
    assert (feature_view is not None) ^ (feature_service is not None), (
        "Either feature_view or feature_service must be provided. Not both."
    )

    request = GetJobRequest()
    if feature_view:
        request.feature_view = feature_view
    if feature_service:
        request.feature_service = feature_service
    request.workspace = workspace
    request.job_id = job_id

    mds_instance = metadata_service.instance()
    response = mds_instance.GetMaterializationJob(request)
    return TectonJob._from_proto(response.job)


def get_latest_ready_time(feature_view: str, workspace: str) -> GetLatestReadyTimeResponse:
    request = GetLatestReadyTimeRequest()
    request.feature_view = feature_view
    request.workspace = workspace

    mds_instance = metadata_service.instance()
    return mds_instance.GetLatestReadyTime(request)


def cancel_job(
    workspace: str, job_id: str, feature_view: Optional[str] = None, feature_service: Optional[str] = None
) -> TectonJob:
    """
    Cancels the scheduled or running job by the job identifier.
    Once cancelled, a job will not be retried further.

    Job run state will be set to `MANUAL_CANCELLATION_REQUESTED`.
    Note that cancellation is asynchronous, so it may take some time for the cancellation to complete.
    If job run is already in `MANUAL_CANCELLATION_REQUESTED` or in a terminal state then it'll return the job.

    :param job_id: ID string of the materialization job.
    :return: `JobData` object for the cancelled job.
    """
    assert (feature_view is not None) ^ (feature_service is not None), (
        "Either feature_view or feature_service must be provided. Not both."
    )

    request = CancelJobRequest()
    if feature_view:
        request.feature_view = feature_view
    if feature_service:
        request.feature_service = feature_service
    request.workspace = workspace
    request.job_id = job_id

    mds_instance = metadata_service.instance()
    response = mds_instance.CancelMaterializationJob(request)
    return TectonJob._from_proto(response.job)


def wait_for_materialization_job(
    workspace: str,
    job_id: str,
    feature_view: Optional[str] = None,
    feature_service: Optional[str] = None,
    timeout: Optional[timedelta] = None,
) -> TectonJob:
    """
    Blocks until the specified job has been completed.

    :param job_id: ID string of the materialization job.
    :param timeout: (Optional) timeout for this function.
        An exception is raised if the job does not complete within the specified time.
    :return: `JobData` object for the successful job.
    :raises JobTimeoutException:
        If timeout param is specified and job does not complete within the specified time.
    :raises MaterializationJobFailedException: If materialization job did not reach a successful state.
    """
    return _wait_for_job(
        lambda: get_job(workspace, job_id, feature_view, feature_service),
        job_id,
        timeout,
    )


def _wait_for_job(
    job_retriever: Callable[[], TectonJob],
    job_id: str,
    timeout: timedelta,
    max_retries: int = 10,
) -> TectonJob:
    wait_start_time = datetime.now()
    retries = 0
    while True:
        try:
            job_data = job_retriever()
        except IOError:
            retries += 1
            if retries > max_retries:
                raise

            continue
        else:
            # reset retries on successful retrieval
            retries = 0

        run_state = job_data.state

        if run_state == "SUCCESS":
            return job_data
        elif timeout and ((datetime.now() - wait_start_time) > timeout):
            msg = f"job {job_id} timed out, last job state {run_state}"
            raise JobTimeoutException(msg)
        elif run_state == "RUNNING":
            time.sleep(WAIT_INTERVAL.total_seconds())
        else:
            msg = f"job {job_id} failed, last job state {run_state}"
            raise JobFailedException(msg)


def get_materialization_status_response(id_proto: id_pb2.Id, workspace: str) -> MaterializationStatus:
    """Returns MaterializationStatus proto for the FeatureView."""
    request = GetMaterializationStatusRequest()
    request.feature_package_id.CopyFrom(id_proto)
    request.workspace = workspace

    response = metadata_service.instance().GetMaterializationStatus(request)
    return response.materialization_status


def get_job_status(task_id: id_pb2.Id, workspace: str) -> MaterializationStatus:
    request = GetJobStatusRequest()
    request.task_id.CopyFrom(task_id)
    request.workspace = workspace

    response = metadata_service.instance().GetJobStatus(request)
    return response.status


@dataclass
class SpineInput:
    path: str
    timestamp_key: str
    column_names: List[str]


@dataclass
class DateTimeRangeInput:
    start_time: datetime
    end_time: datetime
    max_loopback: Optional[timedelta] = None
    entities_path: Optional[str] = None


def _build_start_dataset_job_request(
    fco: Union[specs.FeatureServiceSpec, specs.FeatureViewSpec],
    input_: Union[SpineInput, DateTimeRangeInput],
    dataset: str,
    compute_mode: BatchComputeMode,
    output_schema: Schema,
    from_source: Optional[bool] = None,
    cluster_config: Optional[ClusterConfig] = None,
    tecton_materialization_runtime: Optional[str] = None,
    environment: Optional[str] = None,
    extra_config: Optional[Dict[str, Any]] = None,
    job_retry_times: Optional[int] = None,
) -> StartDatasetJobRequest:
    """This function shared between `start_dataset_job` and local integration tests"""
    request = StartDatasetJobRequest()
    request.workspace = fco.workspace
    request.compute_mode = compute_mode.value
    request.dataset_name = dataset
    request.expected_schema.CopyFrom(output_schema.to_proto())
    if from_source is not None:
        request.from_source = from_source

    if isinstance(fco, specs.FeatureViewSpec):
        request.feature_view_id.CopyFrom(fco.id_proto)
    elif isinstance(fco, specs.FeatureServiceSpec):
        request.feature_service_id.CopyFrom(fco.id_proto)
    else:
        msg = f"unexpected fco type {type(fco)} for start_dataset_job"
        raise RuntimeError(msg)

    if isinstance(input_, SpineInput):
        request.spine.path = input_.path

        request.spine.timestamp_key = input_.timestamp_key
        request.spine.column_names.extend(input_.column_names)
    elif isinstance(input_, DateTimeRangeInput):
        request.datetime_range.start.FromDatetime(input_.start_time)
        request.datetime_range.end.FromDatetime(input_.end_time)
        if input_.max_loopback:
            request.datetime_range.max_loopback.FromTimedelta(input_.max_loopback)
        if input_.entities_path:
            request.datetime_range.entities_path = input_.entities_path
    else:
        msg = f"unexpected input type {type(input_)} for start_dataset_jon"
        raise RuntimeError(msg)

    if cluster_config:
        request.cluster_config.CopyFrom(cluster_config)

    if tecton_materialization_runtime:
        request.tecton_runtime = tecton_materialization_runtime

    if environment:
        request.environment = environment

    if extra_config:
        request.extra_config.update({k: str(v) for k, v in extra_config.items()})

    if job_retry_times:
        request.job_retry_times.job_retry_times = job_retry_times

    return request


def start_dataset_job(
    fco: Union[specs.FeatureServiceSpec, specs.FeatureViewSpec],
    input_: Union[SpineInput, DateTimeRangeInput],
    dataset: str,
    compute_mode: BatchComputeMode,
    output_schema: Schema,
    from_source: Optional[bool] = None,
    cluster_config: Optional[ClusterConfig] = None,
    tecton_materialization_runtime: Optional[str] = None,
    environment: Optional[str] = None,
    extra_config: Optional[Dict[str, Any]] = None,
    job_retry_times: Optional[int] = None,
) -> DatasetJob:
    request = _build_start_dataset_job_request(
        fco,
        input_,
        dataset,
        compute_mode,
        output_schema,
        from_source,
        cluster_config,
        tecton_materialization_runtime,
        environment,
        extra_config,
        job_retry_times,
    )

    response = metadata_service.instance().StartDatasetJob(request)
    return DatasetJob._from_proto(response.job)


def get_dataset_job(workspace: str, job_id: str, dataset: str):
    request = GetDatasetJobRequest()
    request.workspace = workspace
    request.saved_feature_data_frame = dataset
    request.job_id = job_id

    response = metadata_service.instance().GetDatasetJob(request)
    return DatasetJob._from_proto(response.job)


def wait_for_dataset_job(workspace: str, job_id: str, dataset: str, timeout: Optional[timedelta] = None):
    return _wait_for_job(
        lambda: get_dataset_job(workspace, job_id, dataset),
        job_id,
        timeout,
    )


def cancel_dataset_job(workspace: str, job_id: str, dataset: str) -> DatasetJob:
    request = CancelDatasetJobRequest()
    request.workspace = workspace
    request.saved_feature_data_frame = dataset
    request.job_id = job_id

    response = metadata_service.instance().CancelDatasetJob(request)
    return DatasetJob._from_proto(response.job)


def upload_dataframe_for_dataset_job(
    df: Union["pandas.DataFrame", str], fco: Union[specs.FeatureServiceSpec, specs.FeatureViewSpec], param_name: str
) -> str:
    if isinstance(df, str):
        if not df.startswith("s3://"):
            msg = f"Provide a valid S3 URI for `{param_name}` parameter"
            raise TectonValidationError(msg)
        return df
    elif not isinstance(df, pandas.DataFrame):
        msg = f"`{param_name}` parameter must be a pandas.DataFrame or an S3 URI"
        raise TectonValidationError(msg)

    # Step 1 : Create the upload request
    start_upload_request = GetDataframeUploadUrlRequest()
    workspace = fco.workspace
    start_upload_request.workspace = workspace
    if isinstance(fco, specs.FeatureViewSpec):
        start_upload_request.feature_view = fco.name
    elif isinstance(fco, specs.FeatureServiceSpec):
        start_upload_request.feature_service = fco.name
    else:
        msg = f"unexpected fco type {type(fco)}"
        raise RuntimeError(msg)
    start_upload_request.task_type = TaskType.DATASET_GENERATION

    # Step 2 : Get the upload url response
    start_upload_response = metadata_service.instance().GetDataframeUploadUrl(start_upload_request)
    out_buffer = io.BytesIO()
    df.to_parquet(out_buffer, index=False, engine="pyarrow", **PARQUET_WRITE_OPTIONS_KWARGS)
    buffer_size = out_buffer.tell()
    out_buffer.seek(0)

    # Step 3: Upload (in chunks)
    upload_id = start_upload_response.upload_id
    key = start_upload_response.key
    upload_response_map = upload(
        workspace=workspace,
        key=key,
        upload_id=upload_id,
        out_buffer=out_buffer,
        buffer_size=buffer_size,
    )
    # Step 4: Complete the upload request
    complete_upload_request = CompleteDataframeUploadRequest(
        workspace=workspace,
        key=key,
        upload_id=upload_id,
        part_etags=upload_response_map,
    )
    complete_upload_response = metadata_service.instance().CompleteDataframeUpload(complete_upload_request)
    return str(complete_upload_response.key)


def _create_materialization_table(column_names: List[str], materialization_status_rows: List[List]) -> Displayable:
    # Setting `max_width=0` creates a table with an unlimited width.
    table = Displayable.from_table(headings=column_names, rows=materialization_status_rows, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(column_names))])

    return table


def get_materialization_status_for_display(
    id_proto: id_pb2.Id, workspace: str, verbose: bool, limit: int, sort_columns: Optional[str], errors_only: bool
) -> Displayable:
    materialization_attempts = get_materialization_status_response(id_proto, workspace).materialization_attempts
    column_names, materialization_status_rows = utils.format_materialization_attempts(
        materialization_attempts, verbose, limit, sort_columns, errors_only
    )

    return _create_materialization_table(column_names, materialization_status_rows)


def retrieval_params_to_job_input(
    params: Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams],
    fco: Union[specs.FeatureServiceSpec, specs.FeatureViewSpec],
):
    if isinstance(params, GetFeaturesInRangeParams):
        input_ = DateTimeRangeInput(
            start_time=params.start_time,
            end_time=params.end_time,
            max_loopback=params.max_lookback,
        )
        if params.entities is not None:
            input_.entities_path = upload_dataframe_for_dataset_job(params.entities, fco, param_name="entities")

        return input_
    if isinstance(params, GetFeaturesForEventsParams):
        return SpineInput(
            path=upload_dataframe_for_dataset_job(params.events, fco, param_name="events"),
            column_names=params.events.columns if isinstance(params.events, pandas.DataFrame) else [],
            timestamp_key=params.timestamp_key or infer_pandas_timestamp(params.events),
        )

    msg = f"Unsupported request context type: {type(params)}"
    raise RuntimeError(msg)

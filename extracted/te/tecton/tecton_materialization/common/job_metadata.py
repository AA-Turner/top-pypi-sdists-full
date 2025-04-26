# This is Spark-free module, which is used by both Spark and Ray materializations
import abc
import datetime
import logging
import threading
from typing import Callable
from typing import Optional
from typing import Tuple

from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadata
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadataTableType
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


logger = logging.getLogger(__name__)
# This section of constants should be used purely for ensuring idempotence of spark jobs.
IDEMPOTENCE_KEY_ATTRIBUTE = "idempotence_key"
VALUE_ATTRIBUTE = "value"
TTL_ATTRIBUTE = "ttl"
LAST_UPDATED_ATTRIBUTE = "last_updated"
RUN_ID_PREFIX = "id:"

TTL_DURATION_SECONDS = int(datetime.timedelta(days=60).total_seconds())

JOB_EXEC_PKEY_ATTRIBUTE = "id"
JOB_EXEC_LAST_UPDATED_ATTRIBUTE = "last_updated"
JOB_EXEC_DATA_ATTRIBUTE = "data"
JOB_EXEC_VERSION_ATTRIBUTE = "version"
CONSUMPTION_BUCKET_SIZE = datetime.timedelta(hours=1)  # see ConsumptionConstants.kt


class JobMetadataClient(abc.ABC):
    @staticmethod
    def for_params(materialization_task_params: MaterializationTaskParams) -> "JobMetadataClient":
        if materialization_task_params.job_metadata_table_type == JobMetadataTableType.JOB_METADATA_TABLE_TYPE_GCS:
            from tecton_materialization.common.job_metadata_gcp import GCSMetadataClient

            return GCSMetadataClient.for_params(materialization_task_params)
        elif materialization_task_params.job_metadata_table_type == JobMetadataTableType.JOB_METADATA_TABLE_TYPE_DYNAMO:
            from tecton_materialization.common.job_metadata_aws import DynamoMetadataClient

            return DynamoMetadataClient.for_params(materialization_task_params)
        else:
            msg = f"Unhandled JobMetadataTableType: {materialization_task_params.job_metadata_table_type}"
            raise Exception(msg)

    @abc.abstractmethod
    def get(self) -> Tuple[JobMetadata, int]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, updater: Callable[[JobMetadata], Optional[JobMetadata]]) -> JobMetadata:
        raise NotImplementedError


class LazyJobMetadataClient(JobMetadataClient):
    def __init__(self, params: MaterializationTaskParams):
        self._params = params
        self._delegate = None
        self._lock = threading.Lock()

    def _get_delegate(self):
        with self._lock:
            if self._delegate is None:
                self._delegate = JobMetadataClient.for_params(self._params)
            return self._delegate

    def get(self) -> Tuple[JobMetadata, int]:
        return self._get_delegate().get()

    def update(self, updater: Callable[[JobMetadata], Optional[JobMetadata]]) -> JobMetadata:
        return self._get_delegate().update(updater)

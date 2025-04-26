import re
from typing import Callable
from typing import Optional
from typing import Tuple

from google.api_core.exceptions import PreconditionFailed
from google.cloud import storage

from tecton_core.id_helper import IdHelper
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_proto.common.id__client_pb2 import Id
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadata
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


class GCSMetadataClient(JobMetadataClient):
    def __init__(self, table: str, attempt_id: Id):
        matches = re.match("gs://(.*?)/(.*)", f"{table}/{IdHelper.to_string(attempt_id)}")
        self._bucket_name, self._blob_name = matches.groups()
        self._storage_client = storage.Client()

    @staticmethod
    def for_params(materialization_task_params: MaterializationTaskParams) -> JobMetadataClient:
        return GCSMetadataClient(materialization_task_params.job_metadata_table, materialization_task_params.attempt_id)

    def get(self) -> Tuple[JobMetadata, int]:
        bucket = self._storage_client.bucket(self._bucket_name)
        blob = bucket.blob(self._blob_name)
        item = blob.download_as_string()
        data = JobMetadata()
        data.ParseFromString(item)
        assert blob.generation is not None, (self._bucket_name, self._blob_name, blob)
        return data, blob.generation

    def update(self, updater: Callable[[JobMetadata], Optional[JobMetadata]]) -> JobMetadata:
        num_retries = 100
        last_exception = None
        for i in range(num_retries):
            try:
                old_data, old_version = self.get()
                new_data = updater(old_data)
                if new_data is None:
                    return old_data
                bucket = self._storage_client.bucket(self._bucket_name)
                blob = bucket.blob(self._blob_name)
                blob.upload_from_string(new_data.SerializeToString(), if_generation_match=old_version)
                return new_data
            except PreconditionFailed as e:
                # We had a conflicting update
                last_exception = e
                continue
        raise last_exception

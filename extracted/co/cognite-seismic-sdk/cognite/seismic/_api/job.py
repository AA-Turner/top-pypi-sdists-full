# Copyright 2022 Cognite AS

import datetime
import os
from typing import Iterator, Optional

from cognite.seismic._api.api import API
from cognite.seismic.data_classes.api_types import JobStatus, StatusCode
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import StringValue

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import SearchJobStatusRequest


class JobAPI(API):
    def __init__(self, query):
        super().__init__(query=query)

    def status(
        self,
        job_id: Optional[str] = None,
        file_id: Optional[int] = None,
        file_uuid: Optional[str] = None,
        status: StatusCode = StatusCode.NONE,
        target_storage_tier_name: Optional[str] = None,
        started_before: Optional[datetime.datetime] = None,
        started_after: Optional[datetime.datetime] = None,
        updated_before: Optional[datetime.datetime] = None,
        updated_after: Optional[datetime.datetime] = None,
    ) -> Iterator[JobStatus]:
        """Retrieve all job statuses that are within the specified criteria.
        One of each criteria can be specified.
        No specified criteria will list all jobs.

        Args:
            job_id (str, optional): The id of the job
            file_id (int, optional): The id of the file being ingested
            file_uuid (str, optional): The uuid of the file being ingested
            status (int, optional): The status code of the jobs returned
            target_storage_tier_name (str, optional): The target storage tier of the jobs returned
            started_before (datetime, optional): The date jobs returned were started before
            started_after (datetime, optional): The date jobs returned were started after
            updated_before (datetime, optional): The date jobs returned were updated before
            updated_after (datetime, optional): The date jobs returned were updated after

        Returns:
            A stream of job statuses in order of most recently updated
        """

        def proto_timestamp(datetime: datetime.datetime):
            timestamp = datetime.timestamp()
            seconds = int(timestamp)
            nanos = int(timestamp % 1 * 1e9)
            proto_timestamp = Timestamp(seconds=seconds, nanos=nanos)
            return proto_timestamp

        if sum([job_id is not None, file_id is not None, file_uuid is not None]) > 1:
            raise ValueError("Only one of job_id, file_id or file_uuid can be specified.")

        req = SearchJobStatusRequest(
            status=status._to_proto(),
            target_storage_tier_name=StringValue(value=target_storage_tier_name)
            if target_storage_tier_name is not None
            else None,
            started_before=proto_timestamp(started_before) if started_before is not None else None,
            started_after=proto_timestamp(started_after) if started_after is not None else None,
            updated_before=proto_timestamp(updated_before) if updated_before is not None else None,
            updated_after=proto_timestamp(updated_after) if updated_after is not None else None,
        )

        if job_id is not None:
            req.job_id = job_id
        if file_id is not None:
            req.file_id = file_id
        if file_uuid is not None:
            req.file_uuid = file_uuid

        results = self.query.SearchJobStatus(req)
        for s in results:
            yield JobStatus._from_proto(s)

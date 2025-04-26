import base64
import datetime
import json
import os
import time
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple

import boto3
import botocore.credentials
import botocore.errorfactory

from tecton_core import aws_credentials
from tecton_core.id_helper import IdHelper
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_proto.common.aws_credentials__client_pb2 import AwsIamRole
from tecton_proto.common.id__client_pb2 import Id
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadata
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


JOB_EXEC_PKEY_ATTRIBUTE = "id"
JOB_EXEC_LAST_UPDATED_ATTRIBUTE = "last_updated"
JOB_EXEC_DATA_ATTRIBUTE = "data"
JOB_EXEC_VERSION_ATTRIBUTE = "version"


class DynamoMetadataClient(JobMetadataClient):
    def __init__(self, table: str, attempt_id: Id, dynamodb_client: Any):
        self._table = table
        self._attempt_id = attempt_id
        self._dynamodb_client = dynamodb_client

    @staticmethod
    def for_params(materialization_task_params: MaterializationTaskParams) -> JobMetadataClient:
        return DynamoMetadataClient(
            table=materialization_task_params.job_metadata_table,
            attempt_id=materialization_task_params.attempt_id,
            dynamodb_client=_dynamodb_client(materialization_task_params),
        )

    @property
    def _key(self):
        return {JOB_EXEC_PKEY_ATTRIBUTE: {"S": IdHelper.to_string(self._attempt_id)}}

    def get(self) -> Tuple[JobMetadata, int]:
        item = self._dynamodb_client.get_item(
            TableName=self._table,
            Key=self._key,
            ConsistentRead=True,
        )["Item"]
        version = item[JOB_EXEC_VERSION_ATTRIBUTE]["N"]
        data = JobMetadata()
        data.ParseFromString(item[JOB_EXEC_DATA_ATTRIBUTE]["B"])
        return data, version

    def update(self, updater: Callable[[JobMetadata], Optional[JobMetadata]]) -> JobMetadata:
        num_retries = 100
        for i in range(num_retries):
            try:
                old_data, old_version = self.get()
                new_data = updater(old_data)
                if new_data is None:
                    return old_data
                now_seconds = int(time.time())
                self._dynamodb_client.put_item(
                    TableName=self._table,
                    Item={
                        **self._key,
                        JOB_EXEC_LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
                        JOB_EXEC_DATA_ATTRIBUTE: {"B": new_data.SerializeToString()},
                        JOB_EXEC_VERSION_ATTRIBUTE: {"N": str(int(old_version) + 1)},
                    },
                    ConditionExpression="#version = :version",
                    ExpressionAttributeNames={"#version": JOB_EXEC_VERSION_ATTRIBUTE},
                    ExpressionAttributeValues={":version": {"N": str(old_version)}},
                )
                return new_data
            except botocore.errorfactory.ClientError as e:
                # Condition failed means we have a conflicting update
                if e.response["Error"]["Code"] == "ConditionalCheckFailedException" and i + 1 < num_retries:
                    continue
                else:
                    raise e


class DBFSCredentialFetcher(botocore.credentials.CachedCredentialFetcher):
    REFRESH_INTERVAL = datetime.timedelta(minutes=5)

    def __init__(self, path: str):
        # A fetch happens when expiration is expiry_window_seconds away, so this will cause us to re-fetch
        # credentials from DBFS every REFRESH_INTERVAL
        super().__init__(expiry_window_seconds=0)
        self._path = path

    def _create_cache_key(self) -> str:
        return "dbfs"

    def _get_credentials(self):
        with open(f"/dbfs{self._path}") as f:
            credentials = json.loads(base64.b64decode(f.read()))
            expiration = datetime.datetime.now(datetime.timezone.utc) + self.REFRESH_INTERVAL
            return {
                "Credentials": {
                    "AccessKeyId": credentials["accessKeyId"],
                    "SecretAccessKey": credentials["secretAccessKey"],
                    "SessionToken": credentials["sessionToken"],
                    "Expiration": expiration,
                },
            }


def _dynamo_session(params: MaterializationTaskParams) -> boto3.Session:
    if params.HasField("dynamodb_cross_account_role") or params.HasField("dynamodb_cross_account_role_arn"):
        assert not params.HasField("dbfs_credentials_path")
        role = AwsIamRole()
        if params.HasField("dynamodb_cross_account_role"):
            role = params.dynamodb_cross_account_role
        else:
            # TODO(meastham): Remove this fallback after dynamodb_cross_account_role support has been released in the
            #  backend for several releases
            role.role_arn = params.dynamodb_cross_account_role_arn
            if params.HasField("dynamodb_cross_account_external_id"):
                role.external_id = params.dynamodb_cross_account_external_id
        return aws_credentials.session_for_role(role, "tecton_materialization")
    elif params.HasField("dbfs_credentials_path"):
        return aws_credentials.session_for_fetcher(DBFSCredentialFetcher(params.dbfs_credentials_path), "dbfs")
    else:
        return boto3.Session()


def _dynamodb_client(params: MaterializationTaskParams):
    dynamo_params = {"region_name": params.dynamodb_table_region}
    if os.environ.get("TEST_ONLY_TECTON_DYNAMODB_ENDPOINT_OVERRIDE"):
        dynamo_params.update(endpoint_url=os.environ["TEST_ONLY_TECTON_DYNAMODB_ENDPOINT_OVERRIDE"])

    return _dynamo_session(params).client("dynamodb", **dynamo_params)

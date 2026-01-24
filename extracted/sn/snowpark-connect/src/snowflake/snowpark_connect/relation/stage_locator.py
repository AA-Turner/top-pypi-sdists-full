#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import os

from fsspec.core import url_to_fs
from pyspark.errors.exceptions.base import AnalysisException
from s3fs.core import S3FileSystem

from snowflake import snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark_connect.config import sessions_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    get_cloud_from_url,
    parse_azure_url,
)
from snowflake.snowpark_connect.relation.utils import random_string
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def get_paths_from_stage(
    paths: list[str],
    session: snowpark.Session,
) -> list[str]:
    """
    Create a Snowflake stage and get the paths to the staged files.
    """
    if paths[0].startswith("@"):  # This is a stage name
        return paths

    stage_name = StageLocator.get_instance(session).get_and_maybe_create_stage(paths[0])

    # TODO : What if GCP?
    # TODO: What if already stage path?
    match get_cloud_from_url(paths[0]):
        case "azure":
            rewrite_paths = []
            for p in paths:
                _, bucket_name, path = parse_azure_url(p)
                rewrite_paths.append(f"{stage_name}/{path}")
            paths = rewrite_paths
        case "gcp":
            exception = AnalysisException(
                "You must configure an integration for Google Cloud Storage to perform I/O operations rather than accessing the URL directly. Reference: https://docs.snowflake.com/en/user-guide/data-load-gcs-config"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        case _:
            filesystem, parsed_path = url_to_fs(paths[0])
            if isinstance(filesystem, S3FileSystem):  # aws
                # Remove bucket name from the path since the stage name will replace
                # the bucket name in the path.
                paths = [
                    f"{stage_name}/{'/'.join(url_to_fs(p)[1].split('/')[1:])}"
                    for p in paths
                ]
            else:  # local
                # For local files, we need to preserve directory structure for partitioned data
                # Instead of just using basename, we'll use the last few path components
                new_paths = []
                for p in paths:
                    # Split the path and take the last 2-3 components to preserve structure
                    # but avoid very long paths
                    path_parts = p.split(os.sep)
                    if len(path_parts) >= 2:
                        # Take last 2 components (e.g., "base_case/x=abc")
                        relative_path = "/".join(path_parts[-2:])
                    else:
                        # Single component, use basename
                        relative_path = os.path.basename(p)
                    new_paths.append(f"{stage_name}/{relative_path}")
                paths = new_paths

    return paths


def separate_stage_and_file_from_path(path: str) -> tuple[str, str]:
    # Remove matching quotes from both ends of the path to get the stage name, if present.
    # Not handle the quote inside the path for now.
    if path is None or len(path) < 2:
        return "", ""
    if path[0] == path[-1] and path[0] in ('"', "'"):
        path = path[1:-1]
    return path.split("/")[0], "/".join(path.split("/")[1:])


class StageLocator:
    _instance = None

    @classmethod
    def get_instance(cls, session: Session) -> "StageLocator":
        if cls._instance is None or cls._instance.session._conn._conn.expired:
            cls._instance = cls(session)
        return cls._instance

    def __init__(self, session: Session) -> None:
        self.stages_for_azure = {}
        self.stages_for_aws = {}
        self.stages_for_gcp = {}
        self.stages_for_local = None

        self.session = session

    def get_and_maybe_create_stage(
        self,
        url: str = "/",
    ) -> str:
        spark_session_id = get_spark_session_id()

        match get_cloud_from_url(url):
            case "azure":
                account, bucket_name, path = parse_azure_url(url)
                key = f"{account}/{bucket_name}"
                if key in self.stages_for_azure:
                    return self.stages_for_azure[key]

                stage_name = random_string(5, "@spark_connect_stage_azure_")
                sql_query = f"CREATE OR REPLACE TEMP STAGE {stage_name[1:]} URL='azure://{account}.blob.core.windows.net/{bucket_name}'"

                credential_session_key = (
                    f"fs.azure.sas.fixed.token.{account}.dfs.core.windows.net",
                    f"fs.azure.sas.{bucket_name}.{account}.blob.core.windows.net",
                )
                credential = sessions_config.get(spark_session_id, None)
                sas_token = None
                for session_key in credential_session_key:
                    if (
                        credential is not None
                        and credential.get(session_key) is not None
                        and credential.get(session_key).strip() != ""
                    ):
                        sas_token = credential.get(session_key)
                        break
                if sas_token is not None:
                    sql_query += f" CREDENTIALS = (AZURE_SAS_TOKEN = '{sas_token}')"

                logger.info(self.session.sql(sql_query).collect())
                self.stages_for_azure[bucket_name] = stage_name
                return stage_name

            case _:
                filesystem, parsed_path = url_to_fs(url)
                if isinstance(filesystem, S3FileSystem):
                    bucket_name = parsed_path.split("/")[0]
                    if bucket_name in self.stages_for_aws:
                        return self.stages_for_aws[bucket_name]

                    stage_name = random_string(5, "@spark_connect_stage_aws_")
                    # Stage name when created does not have "@" at the beginning
                    # but the rest of the time it's used, it does. We just drop it here.
                    sql_query = f"CREATE OR REPLACE TEMP STAGE {stage_name[1:]} URL='s3://{parsed_path.split('/')[0]}'"
                    credential = sessions_config.get(spark_session_id, None)
                    if credential is not None:
                        if (  # USE AWS KEYS to connect
                            credential.get("spark.hadoop.fs.s3a.access.key") is not None
                            and credential.get("spark.hadoop.fs.s3a.secret.key")
                            is not None
                            and credential.get("spark.hadoop.fs.s3a.access.key").strip()
                            != ""
                            and credential.get("spark.hadoop.fs.s3a.secret.key").strip()
                            != ""
                        ):
                            aws_keys = f" AWS_KEY_ID = '{credential.get('spark.hadoop.fs.s3a.access.key')}'"
                            aws_keys += f" AWS_SECRET_KEY = '{credential.get('spark.hadoop.fs.s3a.secret.key')}'"
                            if (
                                credential.get("spark.hadoop.fs.s3a.session.token")
                                is not None
                            ):
                                aws_keys += f" AWS_TOKEN = '{credential.get('spark.hadoop.fs.s3a.session.token')}'"
                            sql_query += f" CREDENTIALS = ({aws_keys})"
                            sql_query += " ENCRYPTION = ( TYPE = 'AWS_SSE_S3' )"
                        elif (  # USE AWS ROLE and KMS KEY to connect
                            credential.get(
                                "spark.hadoop.fs.s3a.server-side-encryption.key"
                            )
                            is not None
                            and credential.get(
                                "spark.hadoop.fs.s3a.server-side-encryption.key"
                            ).strip()
                            != ""
                            and credential.get("spark.hadoop.fs.s3a.assumed.role.arn")
                            is not None
                            and credential.get(
                                "spark.hadoop.fs.s3a.assumed.role.arn"
                            ).strip()
                            != ""
                        ):
                            aws_role = f" AWS_ROLE = '{credential.get('spark.hadoop.fs.s3a.assumed.role.arn')}'"
                            sql_query += f" CREDENTIALS = ({aws_role})"
                            sql_query += f" ENCRYPTION = ( TYPE='AWS_SSE_KMS' KMS_KEY_ID = '{credential.get('spark.hadoop.fs.s3a.server-side-encryption.key')}' )"

                    logger.info(self.session.sql(sql_query).collect())
                    self.stages_for_aws[bucket_name] = stage_name
                    return stage_name

                else:
                    if self.stages_for_local is None:
                        stage_name = random_string(5, "@spark_connect_stage_local_")
                        self.session.sql(
                            f"CREATE OR REPLACE TEMP STAGE {stage_name[1:]}"
                        ).collect()
                        self.stages_for_local = stage_name
                    return self.stages_for_local

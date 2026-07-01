#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from fsspec.core import url_to_fs
from pyspark.errors.exceptions.base import AnalysisException
from s3fs.core import S3FileSystem

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.session import Session
from snowflake.snowpark_connect.config import sessions_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    get_cloud_from_url,
    parse_azure_url,
)
from snowflake.snowpark_connect.relation.read.path_anchoring import (
    _local_path_stage_relative_suffix,
    classify_source_path,
    split_glob_scan_prefix,
)
from snowflake.snowpark_connect.relation.utils import random_string
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def _path_for_stage_mapping(path: str) -> str:
    """Return the path shape ``get_paths_from_stage`` should map for ``path``."""
    if classify_source_path(path).kind != "glob":
        return path
    scan_prefix, _ = split_glob_scan_prefix(path)
    return scan_prefix


def get_paths_from_stage(
    paths: list[str],
    session: snowpark.Session,
) -> list[str]:
    """
    Create a Snowflake stage and get the paths to the staged files.
    """
    if paths[0].startswith("@"):  # This is a stage name
        return [_path_for_stage_mapping(p) for p in paths]

    stage_name = StageLocator.get_instance(session).get_and_maybe_create_stage(
        _path_for_stage_mapping(paths[0])
    )

    # TODO : What if GCP?
    # TODO: What if already stage path?
    match get_cloud_from_url(paths[0]):
        case "azure":
            rewrite_paths = []
            for p in paths:
                mapped = _path_for_stage_mapping(p)
                _, bucket_name, path = parse_azure_url(mapped)
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
                    f"{stage_name}/{'/'.join(url_to_fs(_path_for_stage_mapping(p))[1].split('/')[1:])}"
                    for p in paths
                ]
            else:  # local
                new_paths = []
                for p in paths:
                    mapped = _path_for_stage_mapping(p)
                    new_paths.append(
                        f"{stage_name}/{_local_path_stage_relative_suffix(mapped)}"
                    )
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
        self.stage_for_local = None

        self.session = session

    def _fully_qualified_stage_name(self, unqualified_stage_name: str) -> str:
        db = unquote_if_quoted(self.session.get_current_database())
        schema = unquote_if_quoted(self.session.get_current_schema())
        bare_name = unqualified_stage_name.lstrip("@")
        return f"@{db}.{schema}.{bare_name}"

    def _stage_exists(self, stage_name: str) -> bool:
        try:
            self.session.sql(f"DESCRIBE STAGE {stage_name[1:]}").collect()
            return True
        except Exception as e:
            logger.debug(f"Stage liveness check failed for '{stage_name}': {e}")
            return False

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
                    cached = self.stages_for_azure[key]
                    return cached

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
                fq_stage_name = self._fully_qualified_stage_name(stage_name)
                self.stages_for_azure[key] = fq_stage_name
                return fq_stage_name

            case _:
                filesystem, parsed_path = url_to_fs(url)
                if isinstance(filesystem, S3FileSystem):
                    bucket_name = parsed_path.split("/")[0]
                    if bucket_name in self.stages_for_aws:
                        cached = self.stages_for_aws[bucket_name]
                        return cached

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
                    fq_stage_name = self._fully_qualified_stage_name(stage_name)
                    self.stages_for_aws[bucket_name] = fq_stage_name
                    return fq_stage_name

                else:
                    if self.stage_for_local is not None:
                        return self.stage_for_local

                    stage_name = random_string(5, "@spark_connect_stage_local_")
                    self.session.sql(
                        f"CREATE OR REPLACE TEMP STAGE {stage_name[1:]}"
                    ).collect()
                    # Keep local stages unqualified. The local download flow uses GET/LS
                    # against stage paths and currently expects @stage/path form.
                    self.stage_for_local = stage_name
                    return self.stage_for_local

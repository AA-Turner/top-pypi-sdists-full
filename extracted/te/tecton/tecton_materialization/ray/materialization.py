import base64
import logging.config
import os
import sys
from urllib.parse import urlparse

from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.materialization.params__client_pb2 import SecretMaterializationTaskParams
from tecton_proto.materialization.params__client_pb2 import SecretServiceParams


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)


def run_job(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
):
    # nested import so that we can publish any import errors out to the job status table
    from tecton_materialization.ray.materialization_jobs import _ray
    from tecton_materialization.ray.materialization_jobs import run_materialization

    with _ray():
        run_materialization(materialization_task_params, secret_materialization_task_params)


def main():
    try:
        task_params = MaterializationTaskParams()
        secret_params = SecretMaterializationTaskParams()

        # Extract secret m13n params from env vars. VM-based Rift passes secrets via this env var.
        if "SECRET_MATERIALIZATION_PARAMS" in os.environ:
            logger.info("Found secret materialization params, parsing...")
            secret_params.ParseFromString(base64.standard_b64decode(os.environ["SECRET_MATERIALIZATION_PARAMS"]))

        # Extract standard m13n params from the object store
        if "MATERIALIZATION_TASK_PARAMS_S3_URL" in os.environ:
            parsed = urlparse(os.environ["MATERIALIZATION_TASK_PARAMS_S3_URL"])
            logger.info(f"Found materialization task params at {parsed}, parsing...")

            bucket_name = parsed.netloc
            object_key = parsed.path.lstrip("/")

            import boto3

            s3_client = boto3.client("s3")
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            content = response["Body"].read()

            task_params.ParseFromString(content)
        elif "MATERIALIZATION_TASK_PARAMS_GCS_URL" in os.environ:
            parsed = urlparse(os.environ["MATERIALIZATION_TASK_PARAMS_GCS_URL"])
            logger.info(f"Found materialization task params at {parsed}, parsing...")

            bucket_name = parsed.netloc
            object_key = parsed.path.lstrip("/")

            from google.cloud import storage

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(object_key)
            content = blob.download_as_bytes()

            task_params.ParseFromString(content)
        # Legacy way of passing standard m13n params via env vars. Required for compatibility with Anyscale and GCP.
        # TODO: remove after we are completely off Anyscale
        elif "MATERIALIZATION_TASK_PARAMS" in os.environ:
            logger.info("Found legacy materialization task params in env vars, parsing...")
            task_params.ParseFromString(base64.standard_b64decode(os.environ["MATERIALIZATION_TASK_PARAMS"]))

            # Backwards compatibility for fetching secret access key from materialization task params,
            # if not already found in the secret env var.
            # Anyscale relies on this. Should be removed once Anyscale is completely gone
            # See https://tecton.atlassian.net/browse/TEC-20193
            if task_params.secrets_api_service_url and not secret_params.HasField("secret_service_params"):
                secret_service_params = SecretServiceParams()
                secret_service_params.secrets_api_service_url = task_params.secrets_api_service_url
                secret_service_params.secret_access_api_key = task_params.secret_access_api_key

                secret_params.secret_service_params.CopyFrom(secret_service_params)
        else:
            msg = "Materialization params were not provided"
            raise ValueError(msg)

        run_job(task_params, secret_params)
    except Exception:
        # make sure error details are published out before exiting
        try:
            job_status_client = JobStatusClient(JobMetadataClient.for_params(task_params))
            job_status_client.set_current_stage_failed(TectonManagedStage.ErrorType.UNEXPECTED_ERROR)
            job_status_client.set_overall_state(TectonManagedStage.State.ERROR)
        except Exception as e:
            # Error details won't appear in the job details UI
            logger.error(f"Failed to publish job error details to the job status table: {e}")
        raise


if __name__ == "__main__":
    main()

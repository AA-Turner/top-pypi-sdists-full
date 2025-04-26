import argparse
import base64
import json
import logging
import os.path
import re
import sys

from google.protobuf.json_format import MessageToJson
from pyspark.sql import SparkSession

from tecton_materialization.batch_materialization import batch_materialize_from_params
from tecton_materialization.common.job_metadata import LazyJobMetadataClient
from tecton_materialization.common.task_params import redact_sensitive_fields_from_params
from tecton_materialization.dataset_generation import dataset_generation_from_params
from tecton_materialization.delta_maintenance import run_delta_maintenance
from tecton_materialization.entity_deletion import run_offline_store_deleter
from tecton_materialization.entity_deletion import run_online_store_deleter
from tecton_materialization.feature_export import feature_export_from_params
from tecton_materialization.ingest_materialization import ingest_pushed_df
from tecton_materialization.job_metadata import check_spark_job_uniqueness
from tecton_materialization.stream_materialization import stream_materialize_from_params


try:
    import boto3
    from botocore.errorfactory import ClientError
except ImportError as ex:
    print(f"Unable to import boto3 or botocore.errorfactory.ClientError: {ex}")
    # not available and unused in dataproc
    boto3 = None
    ClientError = None

from tecton_core import conf
from tecton_core.id_helper import IdHelper
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


EMR_CLUSTER_INFO_FILE = "job-flow.json"
EMR_CLUSTER_INFO_PATH = f"/mnt/var/lib/info/{EMR_CLUSTER_INFO_FILE}"

logger = logging.getLogger(__name__)


def _deserialize_materialization_task_params(serialized_materialization_task_params) -> MaterializationTaskParams:
    params = MaterializationTaskParams()
    params.ParseFromString(base64.standard_b64decode(serialized_materialization_task_params))
    return params


def _run_id_from_dbutils(dbutils):
    context = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    run_id = json.loads(context).get("currentRunId", {}).get("id")
    if not run_id:
        msg = f"Unable to get Databricks run ID from context: {context}"
        raise RuntimeError(msg)
    logger.info(f"Found Databricks run ID: {run_id}")
    return str(run_id)


def _run_id_from_emr():
    try:
        with open(EMR_CLUSTER_INFO_PATH, "r") as f:
            emr_cluster_info = json.load(f)
        run_id = emr_cluster_info["jobFlowId"]
    except Exception as e:
        # for yarn docker runtime the file is mounted (not the entire path)
        try:
            with open(EMR_CLUSTER_INFO_FILE, "r") as f:
                emr_cluster_info = json.load(f)
            run_id = emr_cluster_info["jobFlowId"]
        except Exception:
            logger.error(f"Cluster info on EMR: FAILED with: {e}")
            raise e
    logger.info(f"Found EMR run ID: {run_id}")
    return run_id


def databricks_main(env):
    configure_logging()

    dbutils = env["dbutils"]
    spark = env["spark"]

    conf.set("TECTON_RUNTIME_ENV", "DATABRICKS")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "spark")
    run_id = _run_id_from_dbutils(dbutils)
    serialized_params = dbutils.widgets.get("materialization_params")

    if serialized_params.startswith("s3://"):
        print(f"{serialized_params} appears to be an S3 URI, reading contents")
        bucket, key = _parse_bucket_key_from_uri(serialized_params)
        print(f"Bucket: {bucket}, Key: {key}")
        s3 = boto3.resource("s3")
        params_object = s3.Object(bucket, key)
        serialized_params = params_object.get()["Body"].read()
    elif serialized_params.startswith("dbfs:/"):
        print(f"{serialized_params} appears to be an DBFS Path, reading contents")
        dbfsPath = serialized_params.replace("dbfs:/", "/dbfs/")
        if os.path.exists(dbfsPath):
            with open(dbfsPath, "r") as f:
                serialized_params = f.read().strip()
        else:
            msg = f"Unable to find Materializaton Params in DBFS Path: {dbfsPath}"
            raise RuntimeError(msg)

    params = _deserialize_materialization_task_params(serialized_params)
    main(params, run_id, spark, step=None)


def main(params: MaterializationTaskParams, run_id, spark, step, skip_legacy_execution_table_check=False):
    id_ = IdHelper.to_string(params.feature_view.feature_view_id)
    json_params = MessageToJson(params)
    redacted_json_params = redact_sensitive_fields_from_params(json_params)
    msg = f"Starting materialization for the FV '{id_}' params: {redacted_json_params}"
    # Both print and log so it will show up in the log (for Splunk) and on
    # the notebook page
    print(msg)
    logger.info(msg)

    job_metadata_client = LazyJobMetadataClient(params)

    check_spark_job_uniqueness(
        params,
        run_id,
        spark,
        step,
        skip_legacy_execution_table_check,
        job_metadata_client=job_metadata_client,
    )

    # Run job twice if we are injecting a check for idempotency
    tries = 2 if "forced_retry" in params.feature_view.fco_metadata.workspace else 1
    for _ in range(tries):
        if params.HasField("ingest_task_info"):
            assert step is None
            raw_df = spark.read.parquet(params.ingest_task_info.ingest_parameters.ingest_path)
            ingest_pushed_df(spark, raw_df, params)
        elif params.HasField("deletion_task_info"):
            assert step is None
            deletion_parameters = params.deletion_task_info.deletion_parameters
            if deletion_parameters.online:
                run_online_store_deleter(spark, params)
            if deletion_parameters.offline:
                run_offline_store_deleter(spark, params)
        elif params.HasField("delta_maintenance_task_info"):
            assert step is None
            run_delta_maintenance(spark, params)
        elif params.HasField("batch_task_info"):
            batch_materialize_from_params(spark, params, run_id, step=step, job_metadata_client=job_metadata_client)
        elif params.HasField("stream_task_info"):
            stream_materialize_from_params(spark, params, job_metadata_client=job_metadata_client)
        elif params.HasField("feature_export_info"):
            feature_export_from_params(spark, params)
        elif params.HasField("dataset_generation_task_info"):
            dataset_generation_from_params(spark, params)
        else:
            msg = "Unknown task info"
            raise Exception(msg)


# There's a separate entrypoint in EMR, since it doesn't have `dbutils` by which we can read input params.
def _parse_bucket_key_from_uri(serialized_params):
    regex = r"s3://(\S+?)/(\S+)"
    match = re.search(regex, serialized_params)
    return match.group(1), match.group(2)


def emr_main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(description="Tecton materialization library.")
    parser.add_argument(
        "--materialization-params", type=str, help="The parameters for this materialization task", default=None
    )
    parser.add_argument(
        "--spark-session-name", type=str, help="The name of the spark session created for this task", default=None
    )
    parser.add_argument(
        "--materialization-step",
        type=int,
        help="Materialization step",
        default=None,
    )

    parsed_args, unknown_args = parser.parse_known_args()
    print("Parsed: {}".format(parsed_args))
    print("Unknown: {}".format(unknown_args))
    print("Cluster region: {}".format(os.getenv("CLUSTER_REGION")))

    step = parsed_args.materialization_step
    serialized_params = parsed_args.materialization_params
    if os.path.exists(serialized_params):
        print(f"{serialized_params} appears to be a file, reading contents")
        with open(serialized_params, "r") as f:
            serialized_params = f.read()
            print(f"Materialization params contents: {serialized_params}")
    elif serialized_params.startswith("s3://"):
        print(f"{serialized_params} appears to be an S3 URI, reading contents")
        bucket, key = _parse_bucket_key_from_uri(serialized_params)
        print(f"Bucket: {bucket}, Key: {key}")
        s3 = boto3.resource("s3")
        params_object = s3.Object(bucket, key)
        serialized_params = params_object.get()["Body"].read()
    else:
        print(f"{serialized_params} appears to be the contents")

    params = _deserialize_materialization_task_params(serialized_params)

    spark = SparkSession.builder.appName(parsed_args.spark_session_name).getOrCreate()
    run_id = _run_id_from_emr()
    conf.set("TECTON_RUNTIME_ENV", "EMR")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "spark")

    main(params, run_id, spark, step)


def local_test_main(spark, mat_params_path):
    configure_logging()

    with open(mat_params_path, "r") as f:
        serialized_params = f.read()

    params = _deserialize_materialization_task_params(serialized_params)
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "spark")
    main(params, 0, spark, step=None)


def configure_logging() -> None:
    # Set the logging level to INFO since materialization logs are internal.
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    # This spams logs on INFO or above.
    logging.getLogger("py4j.java_gateway").setLevel(logging.WARN)


if __name__ == "__main__":
    emr_main()

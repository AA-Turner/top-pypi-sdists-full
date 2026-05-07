import os
import json
import atexit
import signal
import boto3
from typing import (Any, Dict, Optional)
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

_S3_BUCKET = "warehouse-cidp-prd"
_S3_ENDPOINT = "https://bucket.vpce-0ddf7fdc67d064956-wcpmy6bk.s3.ap-northeast-2.vpce.amazonaws.com"
_S3_REGION = "ap-northeast-2"


def _is_multiline_json(path: str) -> bool:
    target = path
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for fname in files:
                if fname.endswith((".json", ".jsonl")):
                    target = os.path.join(root, fname)
                    break
            if target != path:
                break
    with open(target, "rb") as fh:
        head = fh.read(4096)
    return head.lstrip()[:1] == b"["


def _read_local_json(path: str) -> list:
    if os.path.isfile(path):
        files = [path]
    else:
        files = sorted(
            os.path.join(r, f)
            for r, _, fs in os.walk(path)
            for f in fs
            if f.endswith((".json", ".jsonl"))
        )
    rows = []
    for fp in files:
        if _is_multiline_json(fp):
            with open(fp, "r") as fh:
                obj = json.load(fh)
            if not isinstance(obj, list):
                raise ValueError(
                    f"{fp}: multiline JSON must be a top-level array"
                )
            rows.extend(obj)
        else:
            with open(fp, "r") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        rows.append(json.loads(line))
    return rows


def _read_local_parquet(path: str):
    try:
        import pyarrow.dataset as ds
    except ImportError as e:
        raise ImportError(
            "pyarrow is required for parquet file inputs to upload_table; "
            "install pyarrow or pass a pandas.DataFrame instead"
        ) from e
    table = ds.dataset(path, format="parquet", partitioning="hive").to_table()
    return table.to_pandas()


def _infer_format(path: str, format_arg: Optional[str]) -> str:
    if format_arg is not None:
        if format_arg not in ("json", "parquet"):
            raise ValueError(f"format must be 'json' or 'parquet', got {format_arg!r}")
        return format_arg

    if os.path.isfile(path):
        if path.endswith((".json", ".jsonl")):
            return "json"
        if path.endswith(".parquet"):
            return "parquet"
        raise ValueError(
            "cannot infer format from file extension; pass format='json' or 'parquet'"
        )

    if os.path.isdir(path):
        seen = set()
        for root, _, files in os.walk(path):
            for fname in files:
                if fname.endswith((".json", ".jsonl")):
                    seen.add("json")
                elif fname.endswith(".parquet"):
                    seen.add("parquet")
        if len(seen) == 0:
            raise ValueError(
                "cannot infer format; directory has no .json/.jsonl/.parquet files"
            )
        if len(seen) > 1:
            raise ValueError(
                "mixed file formats in directory; pass format= explicitly"
            )
        return seen.pop()

    raise FileNotFoundError(f"source path not found: {path}")


def _source_to_dataframe(spark, source, format_arg: Optional[str]):
    if isinstance(source, str):
        if not os.path.exists(source):
            raise FileNotFoundError(f"source path not found: {source}")
        fmt = _infer_format(source, format_arg)
        if fmt == "parquet":
            return spark.createDataFrame(_read_local_parquet(source))
        return spark.createDataFrame(_read_local_json(source))

    if isinstance(source, list):
        return spark.createDataFrame(source)

    try:
        import pandas as pd
    except ImportError:
        pd = None
    if pd is not None and isinstance(source, pd.DataFrame):
        return spark.createDataFrame(source)

    raise TypeError(
        f"unsupported source type: {type(source).__name__}; "
        "expected str (path), list[dict], or pandas.DataFrame"
    )


class SparkSessionBuilder:
    def __init__(self, k8s_config="~/.kube/ciap_prd.conf") -> None:
        from pyspark import SparkConf
        from cidp.kube import KubernetesController
        import uuid
        self.spark_session = None
        self._cleaned_up = False
        self._k8s_api = KubernetesController(k8s_config)
        self._suffix = uuid.uuid4().hex[:6]
        self._app_id = self._suffix
        self._service_name = f"spark-{self._app_id}"
        self._options = SparkConf()
        self._my_pod = self._k8s_api.get_my_pod_spec()
        self._my_namespace = self._k8s_api.get_pod_namespace(self._my_pod)
        self.appName(f"{self._my_pod.metadata.name}-{self._app_id}")

        atexit.register(self._cleanup)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def config(self, k: str, v: Any) -> "SparkSessionBuilder":
        self._options.set(k, v)
        return self

    def master(self, master: str) -> "SparkSessionBuilder":
        return self.config("spark.master", master)

    def appName(self, name: str) -> "SparkSessionBuilder":
        return self.config("spark.app.name", name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()

    def _cleanup(self):
        if self._cleaned_up:
            return
        self._cleaned_up = True
        if self.spark_session is not None:
            self.spark_session.stop()
            self.spark_session = None
        self._k8s_api.remove_spark_nodeport(self._my_namespace, self._service_name)

    def _signal_handler(self, signum, frame):
        self._cleanup()
        raise SystemExit(1)

    def getOrCreate(self) -> SparkSession:
        def get_spark_nodeports():
            return self._k8s_api.get_available_ports(count=2)

        driver_port, blockmanager_port = get_spark_nodeports()
        self._k8s_api.create_spark_nodeport(self._my_namespace,
                                            self._service_name,
                                            self._my_pod,
                                            driver_port,
                                            blockmanager_port)
        (self.config("spark.driver.host", f"{self._service_name}.spark-endpoint.cidp.io")
         .config("spark.driver.port", driver_port)
         .config("spark.blockManager.port", blockmanager_port))

        from pyspark.sql import SparkSession
        if self.spark_session is None:
            self.spark_session = SparkSession.builder.config(conf=self._options).getOrCreate()
        return self.spark_session


def write_table(df, dbname: str, tablename: str,
                partition_col: Optional[str] = None,
                partition_value: Optional[Any] = None) -> None:
    if (partition_col is None) != (partition_value is None):
        raise ValueError("partition_col and partition_value must be set together")

    spark = df.sparkSession
    spark.sql(
        f"CREATE DATABASE IF NOT EXISTS `{dbname}` "
        f"LOCATION 's3a://{_S3_BUCKET}/{dbname}'"
    )

    path = f"s3a://{_S3_BUCKET}/{dbname}/{tablename}/"
    table = f"{dbname}.{tablename}"

    if partition_col is None:
        df.write \
          .mode("overwrite") \
          .option("path", path) \
          .format("parquet") \
          .saveAsTable(table)
        return

    prev_mode = spark.conf.get("spark.sql.sources.partitionOverwriteMode", "static")
    try:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
        df.where(F.col(partition_col) == partition_value) \
          .write \
          .mode("overwrite") \
          .option("path", path) \
          .partitionBy(partition_col) \
          .format("parquet") \
          .saveAsTable(table)
    finally:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", prev_mode)


def download_table(dbname: str, tablename: str, output_path: str,
                   partition_col: Optional[str] = None,
                   partition_value: Optional[Any] = None) -> None:
    if (partition_col is None) != (partition_value is None):
        raise ValueError("partition_col and partition_value must be set together")

    if partition_col is None:
        prefix = f"{dbname}/{tablename}/"
    else:
        prefix = f"{dbname}/{tablename}/{partition_col}={partition_value}/"

    s3 = boto3.client(
        service_name="s3",
        endpoint_url=_S3_ENDPOINT,
        region_name=_S3_REGION,
    )
    os.makedirs(output_path, exist_ok=True)

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=_S3_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            s3.download_file(_S3_BUCKET, key, f"{output_path}/{os.path.basename(key)}")


def upload_table(source, dbname: str, tablename: str,
                 format: Optional[str] = None,
                 partition_col: Optional[str] = None,
                 partition_value: Optional[Any] = None,
                 spark=None) -> None:
    if spark is None:
        spark = SparkSession.getActiveSession()
    if spark is None:
        raise ValueError("no active SparkSession; pass spark= explicitly")

    df = _source_to_dataframe(spark, source, format)
    write_table(df, dbname, tablename,
                partition_col=partition_col,
                partition_value=partition_value)
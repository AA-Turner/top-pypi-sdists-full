import os
import atexit
import signal
import boto3
from typing import (Any, Dict, Optional)
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

_S3_BUCKET = "warehouse-cidp-prd"
_S3_ENDPOINT = "https://bucket.vpce-0ddf7fdc67d064956-wcpmy6bk.s3.ap-northeast-2.vpce.amazonaws.com"
_S3_REGION = "ap-northeast-2"


class SparkSessionBuilder:
    def __init__(self, k8s_config="~/.kube/ciap_prd.conf") -> None:
        from datetime import datetime
        from pyspark import SparkConf
        from cidp.kube import KubernetesController
        import uuid
        self.spark_session = None
        self._cleaned_up = False
        self._k8s_api = KubernetesController(k8s_config)
        self._timestamp = datetime.now().strftime("%Y%m%d%H%M")
        self._suffix = uuid.uuid4().hex[:8]
        self._app_id = f"{self._timestamp}-{self._suffix}"
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
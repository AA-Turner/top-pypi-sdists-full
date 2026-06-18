import os
import json
import time
import atexit
import signal
import boto3
from botocore.config import Config
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def _read_local_csv(path: str, csv_options: Optional[dict] = None):
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            "pandas is required for csv inputs to upload_table; "
            "install pandas or pass a pandas.DataFrame instead"
        ) from e

    def _opts_for(fp: str) -> dict:
        per = dict(csv_options or {})
        if "sep" not in per and fp.endswith(".tsv"):
            per["sep"] = "\t"
        return per

    if os.path.isfile(path):
        return pd.read_csv(path, **_opts_for(path))

    files = sorted(
        os.path.join(r, f)
        for r, _, fs in os.walk(path)
        for f in fs if f.endswith((".csv", ".tsv"))
    )
    if not files:
        raise ValueError(f"no .csv/.tsv files found under {path}")
    frames = [pd.read_csv(fp, **_opts_for(fp)) for fp in files]
    return pd.concat(frames, ignore_index=True)


def _fmt_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    f = float(n)
    for u in units:
        if f < 1024 or u == units[-1]:
            return f"{int(f)} B" if u == "B" else f"{f:.1f} {u}"
        f /= 1024


def _describe_source(source) -> str:
    if isinstance(source, str):
        return f"path '{source}'"
    if isinstance(source, list):
        return f"list ({len(source)} rows)"
    try:
        import pandas as pd
    except ImportError:
        pd = None
    if pd is not None and isinstance(source, pd.DataFrame):
        return f"pandas.DataFrame ({len(source)} rows × {len(source.columns)} cols)"
    return type(source).__name__


def _infer_format(path: str, format_arg: Optional[str]) -> str:
    if format_arg is not None:
        if format_arg not in ("json", "parquet", "csv"):
            raise ValueError(
                f"format must be 'json', 'parquet', or 'csv', got {format_arg!r}"
            )
        return format_arg

    if os.path.isfile(path):
        if path.endswith((".json", ".jsonl")):
            return "json"
        if path.endswith(".parquet"):
            return "parquet"
        if path.endswith((".csv", ".tsv")):
            return "csv"
        raise ValueError(
            "cannot infer format from file extension; "
            "pass format='json', 'parquet', or 'csv'"
        )

    if os.path.isdir(path):
        seen = set()
        for root, _, files in os.walk(path):
            for fname in files:
                if fname.endswith((".json", ".jsonl")):
                    seen.add("json")
                elif fname.endswith(".parquet"):
                    seen.add("parquet")
                elif fname.endswith((".csv", ".tsv")):
                    seen.add("csv")
        if len(seen) == 0:
            raise ValueError(
                "cannot infer format; directory has no "
                ".json/.jsonl/.parquet/.csv/.tsv files"
            )
        if len(seen) > 1:
            raise ValueError(
                "mixed file formats in directory; pass format= explicitly"
            )
        return seen.pop()

    raise FileNotFoundError(f"source path not found: {path}")


def _source_to_dataframe(spark, source, format_arg: Optional[str],
                         csv_options: Optional[dict] = None):
    if isinstance(source, str):
        if not os.path.exists(source):
            raise FileNotFoundError(f"source path not found: {source}")
        fmt = _infer_format(source, format_arg)
        if fmt == "parquet":
            return spark.createDataFrame(_read_local_parquet(source))
        if fmt == "csv":
            return spark.createDataFrame(_read_local_csv(source, csv_options))
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


def _parse_s3a_uri(uri: str) -> tuple:
    if not (uri.startswith("s3a://") or uri.startswith("s3://")):
        raise ValueError(
            f"unsupported location scheme (expected s3:// or s3a://): {uri}"
        )
    rest = uri.split("://", 1)[1]
    bucket, _, key = rest.partition("/")
    prefix = key.rstrip("/") + "/"
    return bucket, prefix


def _get_or_create_spark(spark=None):
    if spark is not None:
        return spark
    active = SparkSession.getActiveSession()
    if active is not None:
        return active
    return SparkSessionBuilder().getOrCreate()


def _get_table_location(spark, dbname: str, tablename: str) -> str:
    rows = spark.sql(
        f"DESCRIBE FORMATTED `{dbname}`.`{tablename}`"
    ).collect()
    for r in rows:
        if (r["col_name"] or "").strip().lower() == "location":
            return r["data_type"].strip()
    raise RuntimeError(
        f"could not find Location in DESCRIBE FORMATTED for {dbname}.{tablename}"
    )


def _get_partition_location(spark, dbname: str, tablename: str,
                            ordered) -> str:
    from cidp import _partitions
    spec = _partitions.format_spec(ordered)
    rows = spark.sql(
        f"DESCRIBE FORMATTED `{dbname}`.`{tablename}` PARTITION ({spec})"
    ).collect()
    for r in rows:
        if (r["col_name"] or "").strip().lower() == "location":
            return r["data_type"].strip()
    raise RuntimeError(
        f"could not find Location for partition {spec} of "
        f"{dbname}.{tablename}"
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
                partitions: Optional[Dict[str, Any]] = None) -> None:
    from cidp import _partitions

    _partitions.validate_partitions(partitions)

    spark = df.sparkSession
    spark.sql(
        f"CREATE DATABASE IF NOT EXISTS `{dbname}` "
        f"LOCATION 's3a://{_S3_BUCKET}/{dbname}'"
    )

    path = f"s3a://{_S3_BUCKET}/{dbname}/{tablename}/"
    table = f"{dbname}.{tablename}"

    if partitions is None:
        df.write \
          .mode("overwrite") \
          .option("path", path) \
          .format("parquet") \
          .saveAsTable(table)
        return

    existing = _partitions.existing_table_partition_order(spark, dbname, tablename)
    if existing is not None:
        if set(existing) != set(partitions.keys()):
            raise ValueError(
                f"partition keys mismatch: input={sorted(partitions.keys())}, "
                f"table={existing}"
            )
        ordered_keys = existing
    else:
        ordered_keys = list(partitions.keys())

    ordered = [(k, partitions[k]) for k in ordered_keys]

    filtered = df
    for k, v in ordered:
        filtered = filtered.where(F.col(k) == v)

    prev_mode = spark.conf.get("spark.sql.sources.partitionOverwriteMode", "static")
    try:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
        filtered.write \
                .mode("overwrite") \
                .option("path", path) \
                .partitionBy(*ordered_keys) \
                .format("parquet") \
                .saveAsTable(table)
    finally:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", prev_mode)

    _partitions.add_partition(spark, dbname, tablename, ordered)
    _partitions.verify_registered(spark, dbname, tablename, ordered)
    _partitions.analyze_partition(spark, dbname, tablename, ordered)


def download_table(dbname: str, tablename: str, output_path: str,
                   partitions: Optional[Dict[str, Any]] = None,
                   spark=None) -> None:
    from cidp import _partitions

    _partitions.validate_partitions(partitions)
    spark = _get_or_create_spark(spark)

    s3 = boto3.client(
        service_name="s3",
        endpoint_url=_S3_ENDPOINT,
        region_name=_S3_REGION,
        config=Config(retries={"max_attempts": 10, "mode": "adaptive"}),
    )

    if partitions is None:
        location = _get_table_location(spark, dbname, tablename)
    else:
        table_location = _get_table_location(spark, dbname, tablename)
        bucket_for_walk, _ = _parse_s3a_uri(table_location)
        ordered_keys = _partitions.resolve_download_order(
            s3, spark, bucket_for_walk, dbname, tablename, partitions,
        )
        ordered = [(k, partitions[k]) for k in ordered_keys]
        location = _get_partition_location(
            spark, dbname, tablename, ordered,
        )

    bucket, prefix = _parse_s3a_uri(location)
    print(f"download_table: s3://{bucket}/{prefix} → {output_path}")

    head_resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    contents = head_resp.get("Contents", [])
    data_exists = any(obj["Key"] != prefix for obj in contents)
    if not data_exists:
        raise FileNotFoundError(
            f"directory not found: s3://{bucket}/{prefix} "
            f"(no data files under '{prefix}'). "
            "Verify the table/partition exists in the warehouse."
        )

    os.makedirs(output_path, exist_ok=True)
    paginator = s3.get_paginator("list_objects_v2")
    objects = [
        obj
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix)
        for obj in page.get("Contents", [])
        if obj["Key"] != prefix
    ]

    transfer_cfg = TransferConfig(
        multipart_threshold=8 * 1024 * 1024,
        multipart_chunksize=8 * 1024 * 1024,
        max_concurrency=2,
        use_threads=True,
    )

    def _dl(obj):
        dest = f"{output_path}/{os.path.basename(obj['Key'])}"
        s3.download_file(bucket, obj["Key"], dest, Config=transfer_cfg)
        return obj["Size"]

    n_total = len(objects)
    n_files, n_bytes = 0, 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(_dl, obj): obj for obj in objects}
        for fut in as_completed(futures):
            n_bytes += fut.result()
            n_files += 1
            print(
                f"\rdownload_table: {n_files}/{n_total} "
                f"({_fmt_bytes(n_bytes)})",
                end="", flush=True,
            )
    print()
    elapsed = time.time() - t0
    print(
        f"download_table: downloaded {n_files} files "
        f"({_fmt_bytes(n_bytes)}) in {elapsed:.1f}s"
    )


def upload_table(source, dbname: str, tablename: str,
                 format: Optional[str] = None,
                 partitions: Optional[Dict[str, Any]] = None,
                 spark=None,
                 csv_options: Optional[dict] = None) -> None:
    from cidp import _partitions

    _partitions.validate_partitions(partitions)

    spark = _get_or_create_spark(spark)

    target = f"{dbname}.{tablename}"
    if partitions is not None:
        spec = ", ".join(f"{k}={v}" for k, v in partitions.items())
        target += f" (partition {spec})"
    print(f"upload_table: {_describe_source(source)} → {target}")

    t0 = time.time()
    df = _source_to_dataframe(spark, source, format, csv_options)
    write_table(df, dbname, tablename, partitions=partitions)
    elapsed = time.time() - t0
    print(f"upload_table: done in {elapsed:.1f}s")
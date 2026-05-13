from typing import Any, Dict, List, Optional, Tuple


def validate_partitions(partitions: Optional[Dict[str, Any]]) -> None:
    if partitions is None:
        return
    if not isinstance(partitions, dict):
        raise ValueError(
            f"partitions must be None or dict, got {type(partitions).__name__}"
        )
    if len(partitions) == 0:
        raise ValueError("partitions must be None or non-empty dict")
    for k, v in partitions.items():
        if v is None:
            raise ValueError(f"partition value cannot be None (key={k!r})")


def quote_value(v: Any) -> str:
    if v is None:
        raise ValueError("partition value cannot be None")
    if isinstance(v, bool):
        return "'true'" if v else "'false'"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        escaped = v.replace("'", "''")
        return f"'{escaped}'"
    raise ValueError(
        f"unsupported partition value type: {type(v).__name__}"
    )


def format_spec(ordered: List[Tuple[str, Any]]) -> str:
    return ", ".join(f"`{k}`={quote_value(v)}" for k, v in ordered)


def format_path(ordered: List[Tuple[str, Any]]) -> str:
    return "/".join(f"{k}={v}" for k, v in ordered)


def discover_order_from_s3(
    s3_client,
    bucket: str,
    db: str,
    tbl: str,
    expected_keys: set,
) -> Optional[List[str]]:
    """Walk S3 directory pattern under db/tbl/ to discover partition column
    order. Returns the ordered list of column names, or None if pattern
    detection fails or the discovered key set != expected_keys.
    """
    prefix = f"{db}/{tbl}/"
    order: List[str] = []
    while len(order) < len(expected_keys):
        resp = s3_client.list_objects_v2(
            Bucket=bucket, Prefix=prefix, Delimiter="/", MaxKeys=1,
        )
        common = resp.get("CommonPrefixes") or []
        if not common:
            return None
        first = common[0]["Prefix"]
        # first is "<accumulated_prefix><col=val>/"
        tail = first[len(prefix):].rstrip("/")
        if "=" not in tail:
            return None
        col, _ = tail.split("=", 1)
        if not col:
            return None
        order.append(col)
        prefix = first
    if set(order) != expected_keys:
        return None
    return order


def existing_table_partition_order(spark, db: str, tbl: str) -> Optional[List[str]]:
    """Return partition column names in DDL order if table exists, else None."""
    if not spark.catalog.tableExists(f"{db}.{tbl}"):
        return None
    cols = spark.catalog.listColumns(tableName=tbl, dbName=db)
    return [c.name for c in cols if c.isPartition]


def resolve_order_from_spark(spark, db: str, tbl: str) -> List[str]:
    """For download fallback. Returns DDL-order partition columns; raises if
    table is unknown or has no partition columns.
    """
    order = existing_table_partition_order(spark, db, tbl)
    if not order:
        raise ValueError(
            f"table {db}.{tbl} has no partition columns in the catalog"
        )
    return order


def resolve_download_order(
    s3_client,
    spark,
    bucket: str,
    db: str,
    tbl: str,
    partitions: Dict[str, Any],
) -> List[str]:
    """C (S3 pattern) -> A (Spark catalog) fallback."""
    keys = set(partitions.keys())
    order = discover_order_from_s3(s3_client, bucket, db, tbl, keys)
    if order is not None:
        return order
    if spark is None:
        raise ValueError(
            "cannot resolve partition order from S3 directory pattern; "
            "pass spark= for catalog fallback"
        )
    catalog_order = resolve_order_from_spark(spark, db, tbl)
    if set(catalog_order) != keys:
        raise ValueError(
            f"partition keys mismatch: input={sorted(keys)}, "
            f"table={catalog_order}"
        )
    return catalog_order


def add_partition(
    spark, db: str, tbl: str, ordered: List[Tuple[str, Any]]
) -> None:
    spec = format_spec(ordered)
    spark.sql(
        f"ALTER TABLE `{db}`.`{tbl}` "
        f"ADD IF NOT EXISTS PARTITION ({spec})"
    )


def verify_registered(
    spark, db: str, tbl: str, ordered: List[Tuple[str, Any]]
) -> None:
    expected = format_path(ordered)
    rows = spark.sql(f"SHOW PARTITIONS `{db}`.`{tbl}`").collect()
    present = {row[0] for row in rows}
    if expected not in present:
        raise RuntimeError(
            f"partition {expected!r} was not registered in metastore after "
            f"ADD PARTITION; existing={sorted(present)}"
        )


def analyze_partition(
    spark, db: str, tbl: str, ordered: List[Tuple[str, Any]]
) -> None:
    spec = format_spec(ordered)
    spark.sql(
        f"ANALYZE TABLE `{db}`.`{tbl}` "
        f"PARTITION ({spec}) COMPUTE STATISTICS"
    )

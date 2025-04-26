import json
import logging
import os
from dataclasses import dataclass
from typing import Any
from typing import Optional

from pyspark.sql import DataFrame

from tecton_proto.args.feature_view__client_pb2 import ClusterConfig


logger = logging.getLogger(__name__)


@dataclass
class QueryPlanInfo:
    has_joins: bool
    has_aggregations: bool


# Note: we use an Any for this type since it is difficult to ascertain the appropriate type of Pysparks internals.
def _has_node(node: Any, name: str) -> bool:  # noqa: ANN401
    if node.nodeName() == name:
        return True
    else:
        children = node.children()
        for idx in range(children.size()):
            if _has_node(children.slice(idx, idx + 1).last(), name):
                return True
    return False


def get_query_plan_info_for_df(df: DataFrame) -> QueryPlanInfo:
    plan = df._jdf.queryExecution().logical()
    return QueryPlanInfo(has_joins=_has_node(plan, "Join"), has_aggregations=_has_node(plan, "Aggregate"))


# Log if running on a different spark version than specified for the feature view's batch config
def check_spark_version(config: Optional[ClusterConfig]) -> None:
    if config is None:
        return

    if config.HasField("new_databricks") and config.new_databricks.HasField("pinned_spark_version"):
        expected_spark_version = config.new_databricks.pinned_spark_version
        # eg '9.1'
        actual_spark_version = os.environ.get("DATABRICKS_RUNTIME_VERSION")
    elif config.HasField("new_emr") and config.new_emr.HasField("pinned_spark_version"):
        expected_spark_version = config.new_emr.pinned_spark_version
        try:
            with open("/mnt/var/lib/info/extraInstanceData.json", "r") as f:
                emr_cluster_info = json.load(f)
                actual_spark_version = emr_cluster_info["releaseLabel"]
        except Exception:
            actual_spark_version = None
    else:
        return

    # We do startswith rather than == because databricks lies about its scala version, so we just compare the first part of the dbr.
    if actual_spark_version is not None and not expected_spark_version.startswith(actual_spark_version):
        logger.warning(
            f"Running on spark version {actual_spark_version} rather than configured version {expected_spark_version}"
        )

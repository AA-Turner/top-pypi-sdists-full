from typing import List

from google.protobuf import duration_pb2

from tecton_core.time_utils import to_human_readable_str
from tecton_proto.common.schema__client_pb2 import Schema as SchemaProto


CONTINUOUS_MODE_BATCH_INTERVAL = duration_pb2.Duration(seconds=86400)


def get_input_feature_columns(view_schema: SchemaProto, join_keys: List[str], timestamp_key: str) -> List[str]:
    column_names = (c.name for c in view_schema.columns)
    return [c for c in column_names if c not in join_keys and c != timestamp_key]


def construct_aggregation_interval_name(aggregation_interval: duration_pb2.Duration, is_continuous: bool) -> str:
    if is_continuous:
        return "continuous"
    else:
        return to_human_readable_str(aggregation_interval)

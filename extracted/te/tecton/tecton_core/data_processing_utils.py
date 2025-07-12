import heapq
import logging
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy
import pandas
import pyarrow
import pyarrow.compute

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import duckdb_factory
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.dialect import Dialect
from tecton_core.query.nodes import MergeValidityPeriodsNode
from tecton_core.query.nodes import PandasDataframeWrapper
from tecton_core.query.nodes import TrimValidityPeriodNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.time_utils import get_feature_data_time_limits
from tecton_proto.args.pipeline__client_pb2 import PipelineNode


DEFAULT_TARGET_SCANNED_OFFLINE_ROWS_PER_PARTITION = 5_000_000
DEFAULT_MINIMUM_SPINE_SPLIT_ROWS = 1_000

logger = logging.getLogger(__name__)


def get_num_dependent_fv(node: PipelineNode, visited_inputs: Dict[str, bool]) -> int:
    if node.HasField("feature_view_node"):
        if node.feature_view_node.input_name in visited_inputs:
            return 0
        visited_inputs[node.feature_view_node.input_name] = True
        return 1
    elif node.HasField("transformation_node"):
        ret = 0
        for child in node.transformation_node.inputs:
            ret = ret + get_num_dependent_fv(child.node, visited_inputs)
        return ret
    elif node.HasField("join_inputs_node"):
        ret = 0
        for node in node.join_inputs_node.nodes:
            ret = ret + get_num_dependent_fv(node, visited_inputs)
        return ret
    return 0


def should_infer_timestamp_of_spine(
    feature_definition: FeatureDefinitionWrapper,
    timestamp_key: Optional[str],
) -> bool:
    if feature_definition.is_rtfv:
        # We need to infer the spine timestamp for a RTFV if the user doesn't pass an explicit timestamp key and
        # 1. It has a dependent materialized feature view or
        # 2. It uses a realtime context
        return timestamp_key is None and (
            get_num_dependent_fv(feature_definition.pipeline.root, visited_inputs={}) > 0
            or feature_definition.uses_realtime_context
        )
    else:
        return timestamp_key is None


def infer_pandas_timestamp(spine: pandas.DataFrame) -> Optional[str]:
    dtypes = dict(spine.dtypes)

    if isinstance(spine, pandas.DataFrame):
        timestamp_cols = [(k, v) for (k, v) in dtypes.items() if pandas.api.types.is_datetime64_any_dtype(v)]
    else:
        msg = f"Unexpected data type for spine: {type(spine)}"
        raise TectonValidationError(msg)

    if len(timestamp_cols) > 1 or len(timestamp_cols) == 0:
        msg = f"Could not infer timestamp keys from {dtypes}; please specify explicitly"
        raise TectonValidationError(msg)
    return timestamp_cols[0][0]


def split_range(range_start: datetime, range_end: datetime, interval: timedelta) -> List[Tuple[datetime, datetime]]:
    """
    Splits a time range into multiple smaller ranges where each split time is aligned to the interval.
    The start of the first range and the end of the last range are preserved.
    """
    split_count = int(conf.get_or_none("DUCKDB_RANGE_SPLIT_COUNT"))

    total_seconds = (range_end - range_start).total_seconds()
    interval_seconds = interval.total_seconds()
    split_seconds = total_seconds / split_count

    split_ranges = []
    current_time = range_start

    for i in range(split_count):
        # For the last interval, ensure the end time matches the provided range_end
        if i == split_count - 1:
            aligned_time = range_end
        else:
            # Calculate the next time and align it
            next_time = current_time + timedelta(seconds=split_seconds)
            epoch_seconds = next_time.timestamp()
            aligned_seconds = (epoch_seconds // interval_seconds) * interval_seconds
            aligned_time = datetime.fromtimestamp(aligned_seconds)

            # Ensure the aligned time does not exceed the range_end
            if aligned_time > range_end:
                aligned_time = range_end

        # Append the current range
        split_ranges.append((current_time, aligned_time))
        current_time = aligned_time

    return split_ranges


def split_spine(
    spine: pandas.DataFrame,
    join_keys: List[str],
) -> List[pandas.DataFrame]:
    """
    This is an experimental feature that splits the spine DataFrame into multiple DataFrames based on the spine split
    strategy specified in the configuration. The split strategy can be one of the following:
    - even: Splits the spine into equal-sized chunks
    - minimize_distance: Splits the spine at points where the distance between consecutive keys is maximized
    - agglomerative_clustering: Splits the spine using Agglomerative Clustering based on the bitwise distance between keys
    """
    split_count = int(conf.get_or_none("DUCKDB_SPINE_SPLIT_COUNT"))
    strategy = conf.get_or_none("DUCKDB_SPINE_SPLIT_STRATEGY")

    if strategy == "even":
        return _even_split(spine, join_keys, split_count)
    elif strategy == "minimize_distance":
        return _minimize_distance_split(spine, join_keys, split_count)
    elif strategy == "agglomerative_clustering":
        return _agglomerative_clustering_split(spine, join_keys, split_count)
    else:
        error = f"Unknown spine split strategy: {strategy}"
        raise ValueError(error)


def _even_split(spine: pandas.DataFrame, join_keys: List[str], split_count: int) -> List[pandas.DataFrame]:
    spine_sorted = spine.sort_values(by=join_keys).reset_index(drop=True)

    # Calculate the number of rows per split
    total_rows = len(spine_sorted)
    rows_per_split = total_rows // split_count
    extra_rows = total_rows % split_count

    # Calculate the split indices
    split_indices = []
    start_idx = 0
    for i in range(split_count):
        end_idx = start_idx + rows_per_split + (1 if i < extra_rows else 0)
        split_indices.append((start_idx, end_idx))
        start_idx = end_idx

    # Split the DataFrame into smaller DataFrames
    split_dfs = [spine_sorted.iloc[start:end].reset_index(drop=True) for start, end in split_indices]

    return split_dfs


def _key_to_int(s: Union[str, int]) -> int:
    if isinstance(s, int):
        return s
    # Convert a string to an integer by concatenating the ASCII values of the characters
    # TODO: This may break when the string is too long
    result = 0
    for i, char in enumerate(s):
        result += ord(char) << (8 * (len(s) - i - 1))
    return result


def _minimize_distance_split(spine: pandas.DataFrame, join_keys: List[str], split_count: int) -> List[pandas.DataFrame]:
    # Check join_keys type, we only support str and int now
    if not all(
        pandas.api.types.is_integer_dtype(spine[join_key]) or pandas.api.types.is_string_dtype(spine[join_key])
        for join_key in join_keys
    ):
        error = "The join keys must be of type int or str for the minimize_distance spine split strategy."
        raise ValueError(error)

    # Sort the dataframe by the join_key
    spine_sorted = spine.sort_values(by=join_keys).reset_index(drop=True)

    # Compute distances between consecutive keys
    keys = spine_sorted[join_keys[0]].tolist()

    int_keys = [_key_to_int(key) for key in keys]
    distances = [abs(int_keys[i + 1] - int_keys[i]) for i in range(len(int_keys) - 1)]

    # Determine split points using heapq for efficiency with small split_count
    if split_count > 1 and distances:
        largest_indices = heapq.nlargest(split_count - 1, range(len(distances)), distances.__getitem__)
        split_points = sorted([index + 1 for index in largest_indices])
    else:
        split_points = []

    # Split the dataframe into chunks
    start_idx = 0
    split_dfs = []

    for idx in split_points:
        split_dfs.append(spine_sorted.iloc[start_idx:idx].reset_index(drop=True))
        start_idx = idx

    split_dfs.append(spine_sorted.iloc[start_idx:].reset_index(drop=True))  # Add the last chunk

    return split_dfs


def _agglomerative_clustering_split(
    spine: pandas.DataFrame, join_keys: List[str], split_count: int
) -> List[pandas.DataFrame]:
    # Check join_keys type, we only support str and int now
    if not all(
        pandas.api.types.is_integer_dtype(spine[join_key]) or pandas.api.types.is_string_dtype(spine[join_key])
        for join_key in join_keys
    ):
        error = "The join keys must be of type int or str for the agglomerative_clustering spine split strategy."
        raise ValueError(error)
    try:
        from sklearn.cluster import AgglomerativeClustering
    except ImportError:
        error = "Please install the scikit-learn package to use the agglomerative_clustering spine split strategy."
        raise ImportError(error)

    # Function to compute pairwise distances using the bitwise approach
    def bitwise_distance_matrix(keys: List[str]) -> numpy.ndarray:
        int_keys = numpy.array([_key_to_int(key) for key in keys])
        dist_matrix = numpy.abs(int_keys[:, None] - int_keys)
        return dist_matrix

    # Compute the distance matrix using the custom weighted distance function
    keys = spine[join_keys[0]].tolist()
    dist_matrix = bitwise_distance_matrix(keys)

    # Apply Agglomerative Clustering using the precomputed distance matrix
    clustering = AgglomerativeClustering(n_clusters=split_count, metric="precomputed", linkage="complete")
    spine["cluster"] = clustering.fit_predict(dist_matrix)

    # Split the DataFrame into multiple DataFrames based on the clusters
    grouped = spine.groupby("cluster")
    split_dfs = [group.drop(columns="cluster").reset_index(drop=True) for _, group in grouped]

    spine.drop(columns="cluster", inplace=True)

    return split_dfs


def pyarrow_split_spine(
    spine: pyarrow.Table,
    join_keys: List[str],
    fdw_list: List[FeatureDefinitionWrapper],
    time_column: str,
    # If target_scanned_offline_rows_per_partition is None, it will use the DEFAULT_TARGET_SCANNED_OFFLINE_ROWS_PER_PARTITION
    target_scanned_offline_rows_per_partition: Optional[int] = None,
) -> List[pyarrow.Table]:
    """
    This is an experimental feature that splits the spine DataFrame into multiple DataFrames based on the spine split
    strategy specified in the configuration. The split strategy can be one of the following:
    - even: Splits the spine into equal-sized chunks
    - minimize_distance: Splits the spine at points where the distance between consecutive keys is maximized
    - agglomerative_clustering: Splits the spine using Agglomerative Clustering based on the bitwise distance between keys
    """

    strategy = conf.get_or_none("DUCKDB_SPINE_SPLIT_STRATEGY")

    if strategy == "even":
        if target_scanned_offline_rows_per_partition is None:
            target_scanned_offline_rows_per_partition = DEFAULT_TARGET_SCANNED_OFFLINE_ROWS_PER_PARTITION

        """
        Determine the split count for a spine:
          - For a Feature View, the `fdw_list` contains only one Feature View element,
            the split count is determined by that Feature View.
          - For a Feature Service, the `fdw_list` contains multiple Feature View elements,
            the split count is determined by the Feature View that requires the highest split count.
        TODO(liangqi): Test if we can just sum up the split count of all Feature Views in the Feature Service.
        """
        max_split_count = 1
        for fdw in fdw_list:
            if not fdw.is_feature_table and not fdw.is_temporal and not fdw.is_temporal_aggregate:
                continue

            """
            Calculate the number of splits required for a Feature View:
             1. Determine the total number of rows across the partitions that need to be read for the spine.
                - For example, if the spine spans from 2024-01-10 to 2024-01-30, and the Feature View involves a
                  7-day aggregation, include rows from partitions covering the range 2024-01-03 to 2024-01-30.
             2. Compute the split count by dividing the total number of rows by the `target_scanned_offline_rows_per_partition`.
                - Split count = Total rows / target_scanned_offline_rows_per_partition.
            """
            spine_time_limit = _extract_time_range_from_spine(spine, fdw, time_column)
            split_count = _calculate_split_count(
                fdw.fv_spec.materialized_data_path, spine_time_limit, target_scanned_offline_rows_per_partition
            )
            max_split_count = max(max_split_count, split_count)

        logger.info(f"Split count for spine: {max_split_count}")

        # Adjust spine split count if it exceeds maximum allowed splits based on minimum rows per split
        total_rows = spine.num_rows
        max_allowed_split_count = total_rows // DEFAULT_MINIMUM_SPINE_SPLIT_ROWS + 1
        if max_split_count > max_allowed_split_count:
            logger.info(
                f"Requested split_count ({max_split_count}) exceeds allowable maximum based on total_rows ({total_rows}) and minimum_spine_split_rows({DEFAULT_MINIMUM_SPINE_SPLIT_ROWS})."
                f"Adjusting split_count to {max_allowed_split_count}."
            )
            max_split_count = max_allowed_split_count

        return _even_split_pyarrow(spine, join_keys, max_split_count)
    else:
        error = f"Unknown spine split strategy: {strategy}."
        raise ValueError(error)


def _even_split_pyarrow(
    spine: pyarrow.Table,
    join_keys: List[str],
    split_count: int,
) -> List[pyarrow.Table]:
    sort_indices = pyarrow.compute.sort_indices(spine, sort_keys=[(key, "ascending") for key in join_keys])
    spine_sorted = spine.take(sort_indices)

    total_rows = spine_sorted.num_rows
    rows_per_split = total_rows // split_count
    extra_rows = total_rows % split_count

    # Calculate the split indices
    split_indices = []
    start_idx = 0
    for i in range(split_count):
        end_idx = start_idx + rows_per_split + (1 if i < extra_rows else 0)
        split_indices.append((start_idx, end_idx))
        start_idx = end_idx

    return [spine_sorted.slice(start, end - start) for start, end in split_indices]


def _extract_time_range_from_spine(
    spine: pyarrow.Table, fdw: FeatureDefinitionWrapper, time_column: str
) -> pendulum.period:
    """
    Determine the time range of the spine.
    For example, if the spine spans from 2024-01-10 to 2024-01-30, and the Feature View involves a 7-day aggregation,
    the time range is 2024-01-03 to 2024-01-30.
    """
    connection = duckdb_factory.create_connection()
    try:
        connection.register("spine_table", spine)

        query = f"""
        SELECT
            MIN({time_column}) AS start_time,
            MAX({time_column}) AS end_time
        FROM spine_table
        """
        result = connection.execute(query).fetchall()
        start_time, end_time = result[0]
        spine_raw_time_range = pendulum.period(pendulum.parse(str(start_time)), pendulum.parse(str(end_time)))
        logger.info(f"Spine Raw Time Range is {spine_raw_time_range}")
        spine_time_limit = get_feature_data_time_limits(fdw, spine_raw_time_range)
        logger.info(f"Spine Time limit is {spine_time_limit}")

        return spine_time_limit
    finally:
        connection.close()


def _calculate_split_count(
    materialized_data_path: str, spine_time_limits: pendulum.period, target_scanned_offline_rows_per_partition: int
) -> int:
    total_num_records = _get_total_row_number(materialized_data_path, spine_time_limits)
    logger.info(f"Total number of records in the offline store: {total_num_records}")
    return total_num_records // target_scanned_offline_rows_per_partition + 1


# Calculate the total number of rows within the partitions of a Delta table that overlap with a given time range.
def _get_total_row_number(materialized_data_path: str, spine_time_limits: pendulum.period) -> int:
    # Keeping this import scoped because deltalake library only installed on python > 3.7
    # 6.x EMR versions run python 3.7 so will not be able to import this library, but this method only used in Rift
    from deltalake import DeltaTable

    delta_table = DeltaTable(materialized_data_path)
    add_actions = delta_table.get_add_actions(flatten=True).to_pandas()

    spine_time_limit_start_str = spine_time_limits.start.strftime("%Y-%m-%d")
    spine_time_limit_end_str = spine_time_limits.end.strftime("%Y-%m-%d")

    # Find the closest partition on or before the start time of `spine_time_limits`.
    all_left_partitions = add_actions[add_actions["partition.time_partition"] <= spine_time_limit_start_str]
    if not all_left_partitions.empty:
        # If there are partitions before or at the start time, select the latest one.
        closest_left_partition = all_left_partitions["partition.time_partition"].max()
    else:
        # If no such partitions exist, default to the start time of `spine_time_limits`.
        closest_left_partition = spine_time_limit_start_str

    logger.info(f"Closest left partition: {closest_left_partition}")

    valid_partitions = add_actions[
        (add_actions["partition.time_partition"] >= closest_left_partition)
        & (add_actions["partition.time_partition"] <= spine_time_limit_end_str)
    ]

    total_num_records = 0
    for _, row in valid_partitions.iterrows():
        total_num_records = total_num_records + row["num_records"]
    return total_num_records


def merge_validity_periods(df_list, valid_time_range, fdw):
    df = pandas.concat(df_list)
    qt = UserSpecifiedDataNode(
        dialect=Dialect.DUCKDB,
        compute_mode="rift",
        data=PandasDataframeWrapper(df),
    ).as_ref()

    qt = MergeValidityPeriodsNode(
        dialect=Dialect.DUCKDB,
        compute_mode="rift",
        input_node=qt,
        fdw=fdw,
    ).as_ref()

    qt = TrimValidityPeriodNode(
        dialect=Dialect.DUCKDB,
        compute_mode="rift",
        input_node=qt,
        start=valid_time_range.start,
        end=valid_time_range.end,
    ).as_ref()

    return qt

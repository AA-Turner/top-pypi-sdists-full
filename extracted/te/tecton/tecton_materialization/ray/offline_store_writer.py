import dataclasses
import functools
import logging
import random
import time
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union
from urllib.parse import urlparse

import pyarrow

from tecton_core import duckdb_factory
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.ray.nodes import TimeSpec
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.offlinestore.delta.metadata__client_pb2 import TectonDeltaMetadata


logger = logging.getLogger(__name__)

R = TypeVar("R")
TxnFn = Callable[[], R]


@dataclasses.dataclass
class OfflineStoreParams:
    feature_view_id: str
    feature_view_name: str
    schema: schema_pb2.Schema
    time_spec: TimeSpec
    feature_store_format_version: int
    batch_schedule: Optional[int]
    num_entity_buckets: Optional[int] = None
    view_schema: Optional[schema_pb2.Schema] = None
    has_untiled_offline_store: Optional[bool] = None

    @staticmethod
    def for_feature_definition(fd: FeatureDefinitionWrapper) -> "OfflineStoreParams":
        return OfflineStoreParams(
            feature_view_id=fd.id,
            feature_view_name=fd.name,
            schema=fd.materialization_schema.to_proto(),
            time_spec=TimeSpec.for_feature_definition(fd),
            feature_store_format_version=fd.get_feature_store_format_version,
            # feature tables do not have schedules
            batch_schedule=fd.get_batch_schedule_for_version if not fd.is_feature_table else None,
            num_entity_buckets=fd.offline_store_config.iceberg.num_entity_buckets
            if fd.has_iceberg_offline_store
            else None,
            view_schema=fd.view_schema.to_proto(),
            has_untiled_offline_store=fd.has_untiled_offline_store,
        )


class OfflineStoreWriter(ABC):
    def __init__(
        self,
        store_params: OfflineStoreParams,
        table_uri: str,
        join_keys: List[str],
    ):
        self._feature_params = store_params
        self._table_uri = table_uri
        self._join_keys = join_keys
        self._duckdb_conn = duckdb_factory.create_connection()
        self._retry_exceptions = []

    @abstractmethod
    def delete_time_range(self, interval: TimeInterval) -> None:
        """Filters and deletes previously materialized data within the interval.

        :param interval: The feature data time interval to delete
        """

    @abstractmethod
    def write(
        self, table: Union[pyarrow.Table, pyarrow.RecordBatchReader], tags: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """Writes a pyarrow Table to the base_uri.

        Returns a list of URIs for the written file(s).

        This does NOT commit. Call commit() after calling this to commit your changes.
        """

    @abstractmethod
    def delete_keys(self, keys: pyarrow.Table):
        """Deletes keys from offline store."""

    @abstractmethod
    def commit(self, metadata: Optional[TectonDeltaMetadata] = None) -> Optional[int]:
        """commits transaction to offline store."""

    @abstractmethod
    def transaction_exists(self, metadata: TectonDeltaMetadata) -> bool:
        """checks matching transaction metadata, which signals that a previous task attempt already wrote data
        If the task overwrites a previous materialization task interval then we treat it as a new transaction.

        :param metadata: transaction metadata
        :return: whether the same transaction has been executed before
        """

    def transaction(self, metadata: Optional[TectonDeltaMetadata] = None) -> Callable[[TxnFn], TxnFn]:
        """Returns a decorator which wraps a function in a transaction.

        If the function returns successfully, the Delta transaction will be committed automatically. Any exceptions will
        cause an aborted transaction.

        Any Delta conflicts which occur will result in the function being retried in a new transaction.

        :param metadata: Optional metadata to be added to the transaction.
        """

        def decorator(f: TxnFn, max_attempts=5) -> TxnFn:
            @functools.wraps(f)
            def wrapper() -> R:
                for attempt in range(1, max_attempts + 1):
                    r = f()
                    try:
                        self.commit(metadata)
                        return r
                    except tuple(self._retry_exceptions) as e:
                        if attempt >= max_attempts:
                            logger.error(
                                f"Offline store write transaction failed after {max_attempts} attempts. Aborting..."
                            )
                            raise
                        # Add a random delay (with exponential backoff) before the retries to decrease
                        # the chance of recurrent conflicts between parallel write jobs.
                        exponential_coef = 1.5 ** (attempt - 1)
                        backoff_time = exponential_coef * random.uniform(0, 5)
                        logger.warning(
                            f"Offline store commit attempt {attempt} failed: {e}\nRetrying in {backoff_time} seconds..."
                        )
                        time.sleep(backoff_time)
                    finally:
                        # Clean up any files that were not part of a successful commit
                        self.abort()

            return wrapper

        return decorator

    @abstractmethod
    def abort(self):
        """
        Abort the transaction by cleaning up any files and state.
        Clean up created parquet files that were not part of a successful commit.
        """


def path_from_uri(uri):
    parts = urlparse(uri)
    return parts.netloc + parts.path

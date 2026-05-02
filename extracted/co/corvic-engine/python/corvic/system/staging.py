"""Corvic system data staging protocol."""

from collections.abc import Mapping
from typing import Protocol

import pyarrow as pa
import sqlglot

from corvic.result import InternalError, Ok
from corvic.system.op_graph_executor import TableSliceArgs
from corvic.well_known_types import VectorSimilarityMetric


class StagingDB(Protocol):
    """A connection to some database where staging data can be found."""

    def count_ingested_rows(self, blob_name: str, *other_blob_names: str) -> int:
        """Returns the number of rows of the given blobs available for querying.

        Callers can expect this to be cheap to call.
        """
        ...

    def query_for_blobs(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Query: ...

    @property
    def vector_column_names_to_widths(self) -> Mapping[str, int]: ...

    def query_for_vector_search(
        self,
        input_vector: list[float],
        vector_blob_names: list[str],
        vector_column_name: str,
        column_names: list[str],
        similarity_metric: VectorSimilarityMetric,
    ) -> sqlglot.exp.Query: ...

    def run_select_query(
        self,
        query: sqlglot.exp.Query,
        expected_schema: pa.Schema,
        slice_args: TableSliceArgs | None = None,
    ) -> Ok[pa.RecordBatchReader] | InternalError:
        """Select data from the staging database.

        The schema of the result will match expected_schema. If that's not possible,
        returns an InernalError.
        """
        ...

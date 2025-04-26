from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, Mapping, Protocol, Sequence, Union

from chalk.client.models import (
    ChalkError,
    DatasetFilter,
    DatasetRevisionPreviewResponse,
    DatasetRevisionSummaryResponse,
    FeatureReference,
    FeatureResult,
    QueryMeta,
    QueryStatus,
)
from chalk.features import DataFrame
from chalk.features.resolver import ResolverProtocol
from chalk.integrations.catalogs.base_catalog import BaseCatalog

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl
    import pyarrow as pa


class DatasetPartition(Protocol):
    """Per-partition info for a dataset"""

    performance_summary: str | None
    """Performance information for computing this shard of the dataset"""


class DatasetRevision(Protocol):
    """Class wrapper around revisions for Datasets."""

    revision_id: uuid.UUID
    """UUID for the revision job."""

    creator_id: str
    """UUID for the creator of the job."""

    outputs: list[str]
    """Output features for the dataset revision."""

    givens_uri: str | None
    """Location of the givens stored for the dataset."""

    status: QueryStatus
    """Status of the revision job."""

    filters: DatasetFilter
    """Filters performed on the dataset."""

    num_partitions: int
    """Number of partitions for revision job."""

    output_uris: str
    """Location of the outputs stored for the dataset."""

    output_version: int
    """Storage version of the outputs."""

    num_bytes: int | None = None
    """Number of bytes of the output, updated upon success."""

    created_at: datetime | None = None
    """Timestamp for creation of revision job."""

    started_at: datetime | None = None
    """Timestamp for start of revision job."""

    terminated_at: datetime | None = None
    """Timestamp for end of revision job."""

    dataset_name: str | None = None
    """Name of revision, if given."""

    dataset_id: uuid.UUID | None = None
    """ID of revision, if name is given."""

    dashboard_url: str | None = None
    """url linking to relevant dashboard page"""

    environment: str

    num_computers: int
    """Number of computers this query ran on."""

    branch: str | None = None
    """Name of branch"""

    errors: list[ChalkError] | None = None

    partitions: list[DatasetPartition]

    metadata: Mapping[str, Any] | None = None

    @property
    def url(self) -> str | None:
        """url linking to relevant dashboard page"""
        return self.dashboard_url

    def to_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.DataFrame:
        """Loads a `pl.DataFrame` containing the output. Use `.to_polars_lazyframe()` if you want
        a `LazyFrame` instead, which allows local filtering of datasets that are larger than memory.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.DataFrame
            A `polars.DataFrame` materializing query output data.
        """
        ...

    def to_polars_lazyframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the output. This method is appropriate for working with larger-than-memory datasets.
        Use `.to_polars()` if you want a `DataFrame` instead.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.LazyFrame
            A `pl.LazyFrame` materializing query output data.
        """
        ...

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the output.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.LazyFrame
            A `pl.LazyFrame` materializing query output data.
        """
        ...

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pd.DataFrame:
        """Loads a `pd.DataFrame` containing the output.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pd.DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pd.DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pd.DataFrame
            A `pd.DataFrame` materializing query output data.
        """
        ...

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> DataFrame:
        """Loads a Chalk `DataFrame` containing the output.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data\
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        DataFrame
            A `DataFrame` materializing query output data.
        """
        ...

    def arrow_schema(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> pa.Schema:
        """Returns the schema of the output data.

        Parameters
        ----------
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pa.Schema
            The schema of the output data.
        """
        ...

    def to_arrow(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pa.Table:
        """Loads a `pa.Table` from the raw parquet file outputs.

        Parameters
        ----------
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pa.Table
            A `pa.Table` materializing query output data.
        """
        ...

    def download_uris(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> Sequence[str]:
        """
        Returns a list of the output uris for the revision. Data
        will be stored in .parquet format. The URIs should be considered temporary,
        and will expire after a server-defined time period.
        """
        ...

    def summary(self) -> DatasetRevisionSummaryResponse:
        """
        Returns an object that loads the summary statistics of a dataset revision.
        The dataframe can be retrieved by calling `to_polars()` or `to_pandas()` on the return object.
        Data will be stored in .parquet format. The URIs should be considered temporary,
        and will expire after a server-defined time period.
        """
        ...

    def preview(self) -> DatasetRevisionPreviewResponse:
        """
        Returns an object that loads a preview of a dataset revision.
        The dataframe can be retrieved by calling `to_polars()` or `to_pandas()` on the return object.
        Data will be stored in .parquet format. The URIs should be considered temporary,
        and will expire after a server-defined time period.
        """
        ...

    def wait(
        self,
        timeout: float | timedelta | ellipsis | None = ...,
        show_progress: bool = True,
    ) -> None:
        """
        Waits for an offline query job to complete.
        Raises if the query is unsuccessful, otherwise returns itself on success.

        Parameters
        ----------
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        show_progress
            Whether to show a progress bar
        """
        ...

    def download_data(
        self,
        path: str,
        output_id: bool = False,
        output_ts: Union[bool, str] = False,
        ignore_errors: bool = False,
        executor: ThreadPoolExecutor | None = None,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> None:
        """Downloads output files pertaining to the revision to given path.

        Datasets are stored in Chalk as sharded Parquet files. With this
        method, you can download those raw files into a directory for processing
        with other tools.

        Parameters
        ----------
        path
            A directory where the Parquet files from the dataset will be downloaded.
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        executor:
            The executor to use for parallelizing downloads. If None, the default executor will be used.
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        """
        ...

    def get_input_dataframe(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the inputs.

        Parameters
        ----------
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.LazyFrame
            A `pl.LazyFrame` materializing query input data.
        """
        ...

    def open_in_browser(self, return_url_only: bool = False) -> str:
        """Returns and opens a url that opens the offline query page in
        the Chalk dashboard. Must be logged in.

        Parameters
        ----------
        return_url_only
            If `True`, does not open url in browser. Default is `False`.

        Returns
        -------
        str
            A url redirecting to the Chalk dashboard.
        """
        ...

    def wait_for_completion(
        self,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> None:
        """Waits for the revision job to complete.

        `ChalkClient.offline_query` returns a `DatasetRevision` instance immediately after
        submitting the revision job. This method can be used to wait for the
        revision job to complete.

        Once the revision job is complete, the `status` attribute of the
        `DatasetRevision` instance will be updated to reflect the status of the
        revision job.

        If the revision job was successful, you can then use methods such as
        `get_data_as_pandas()` without having to wait for the revision job to
        complete.

        Parameters
        ----------
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        """
        ...

    def ingest(self, store_online: bool = False, store_offline: bool = True) -> Dataset:
        """Saves this revision to Chalk's online and offline storage.

        Parameters
        ----------
        store_online
            Whether to store the revision in Chalk's online storage.
        store_offline
            Whether to store the revision in Chalk's offline storage.
        """
        ...

    def resolver_replay(
        self,
        resolver: ResolverProtocol,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> Union[pl.DataFrame, pl.LazyFrame, Mapping[str, pl.DataFrame], Mapping[str, pl.LazyFrame],]:
        """
        Downloads the resolver replay data for the given resolver in the revision, provided the revision had store_plan_stages
        enabled.

        The replay data is functionally similar to viewing the intermediate results on the plan explorer.

        If the resolver appears in only one stage of the plan, the resolver's replay data is returned directly.
        If the resolver instead appears in multiple stages of the plan, a mapping of the operation's ID to the replay data
        will be returned. If the resolver does not appear in the plan, an exception will be thrown.

        Parameters
        ----------
        resolver
            The resolver to download the replay data for, or its fqn.
        show_progress
            Whether to show a progress bar
        lazy
            Whether to return Polars LazyFrames
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        """
        ...

    def set_metadata(
        self,
        metadata: Mapping[str, Any],
    ):
        """
        Set metadata for a dataset revision.

        Parameters
        ----------
        metadata
            The metadata (as a dict) that you want to set for a given revision—this will fully replace
            any metadata that has already been previously set.

        Examples
        --------
        >>> from chalk.client import ChalkClient, Dataset
        >>> dataset: Dataset = ChalkClient().get_dataset(dataset_name='my_dataset_name')
        >>> dataset.revisions[0].set_metadata(
        ...     {"metadata": "test"}
        ... )
        """


class Dataset(Protocol):
    """Wrapper around Offline Query results.

    Datasets are obtained by invoking `ChalkClient.offline_query()`.
    `Dataset` instances store important metadata and enable the retrieval of
    offline query outputs.

    Examples
    --------
    >>> from chalk.client import ChalkClient, Dataset
    >>> uids = [1, 2, 3, 4]
    >>> at = datetime.now(tz=timezone.utc)
    >>> dataset: Dataset = ChalkClient().offline_query(
    ...     input={
    ...         User.id: uids,
    ...     },
    ...     input_times=[at] * len(uids),
    ...     output=[
    ...         User.id,
    ...         User.fullname,
    ...         User.email,
    ...         User.name_email_match_score,
    ...     ],
    ...     dataset_name='my_dataset'
    ... )
    >>> df = dataset.get_data_as_pandas()
    >>> df.recompute(features=[User.fraud_score], branch="feature/testing")
    """

    is_finished: bool
    """Whether the most recent `DatasetRevision` is finished or still pending."""

    version: int
    """Storage version number of outputs."""

    revisions: Sequence[DatasetRevision]
    """A list of all `DatasetRevision` instances belonging to this dataset."""

    dataset_name: str | None
    """The unique name for this dataset, if given."""

    dataset_id: uuid.UUID | None
    """The unique UUID for this dataset."""

    errors: Sequence[ChalkError] | None
    """A list of errors in loading the dataset, if they exist."""

    def to_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.DataFrame:
        """Loads a `pl.DataFrame` containing the output. Use `.to_polars_lazyframe()` if you want
        a `LazyFrame` instead, which allows local filtering of datasets that are larger than memory.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.DataFrame
            A `pl.DataFrame` materializing query output data.
        """
        ...

    async def to_polars_async(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.DataFrame:
        """Loads a `pl.DataFrame` containing the output. Use `.to_polars_lazyframe()` if you want
        a `LazyFrame` instead, which allows local filtering of datasets that are larger than memory.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.DataFrame
            A `pl.DataFrame` materializing query output data.
        """
        ...

    def to_arrow(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pa.Table:
        """Loads a `pa.Table` from the raw parquet file outputs.

        Other Parameters
        ----------
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pa.Table
            A `pa.Table` materializing query output data.
        """
        ...

    def arrow_schema(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> pa.Schema:
        """Returns the schema of the output data.

        Parameters
        ----------
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pa.Schema
            The schema of the output data.
        """
        ...

    def to_polars_lazyframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the output. This method is appropriate for working with larger-than-memory datasets.
        Use `.to_polars()` if you want a `DataFrame` instead.

        Other Parameters
        ----------------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.LazyFrame
            A `pl.LazyFrame` materializing query output data.
        """
        ...

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the output.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pl.LazyFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.LazyFrame
            A `pl.LazyFrame` materializing query output data.
        """
        ...

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pd.DataFrame:
        """Loads a `pd.DataFrame` containing the output.

        Other Parameters
        ----------------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pd.DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pd.DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pd.DataFrame
            A `pd.DataFrame` materializing query output data.
        """
        ...

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> DataFrame:
        """Loads a Chalk `DataFrame` containing the output.
        Requires the pertinent Chalk features to be accessible via import

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        DataFrame
            A `DataFrame` materializing query output data.
        """
        ...

    def to_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pd.DataFrame:
        """Loads a `pd.DataFrame` containing the output of the most recent revision.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pd.DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pd.DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pd.DataFrame
            A `pd.DataFrame` materializing query output data.
        """
        ...

    def download_uris(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> list[str]:
        """
        Returns a list of the output uris for the revision. Data
        will be stored in .parquet format. The URIs should be considered temporary,
        and will expire after a server-defined time period.

        Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pd.DataFrame`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `pd.DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        """
        ...

    def wait(
        self,
        timeout: float | timedelta | ellipsis | None = ...,
        show_progress: bool = True,
    ) -> Dataset:
        """
        Waits for an offline query job to complete. Returns a list of errors if unsuccessful, or None if successful.

        Parameters
        ----------
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        show_progress
            Whether to show a progress bar
        """
        ...

    def download_data(
        self,
        path: str,
        executor: ThreadPoolExecutor | None = None,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> None:
        """Downloads output files pertaining to the revision to the given path.

        Datasets are stored in Chalk as sharded Parquet files. With this
        method, you can download those raw files into a directory for processing
        with other tools.

        Parameters
        ----------
        path
            A directory where the Parquet files from the dataset will be downloaded.
        ignore_errors
            Whether to ignore query errors upon fetching data.
        executor
            An executor to use to download the data in parallel. If not specified, the
            default executor will be used.
        show_progress
            Whether to show a progress bar.
        timeout
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Examples
        --------
        >>> from chalk.client import ChalkClient, Dataset
        >>> from datetime import datetime, timezone
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now(tz=timezone.utc)
        >>> dataset = ChalkClient().offline_query(
        ...     input={User.id: uids},
        ...     input_times=[at] * len(uids),
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ...     dataset_name='my_dataset',
        ... )
        >>> dataset.download_data('my_directory')
        """
        ...

    def summary(self) -> DatasetRevisionSummaryResponse:
        """
        Returns an object that loads the summary statistics of a dataset revision.
        The dataframe can be retrieved by calling `to_polars()` or `to_pandas()` on the return object.
        Data will be stored in .parquet format. The URIs should be considered temporary,
        and will expire after a server-defined time period.
        """
        ...

    def preview(self) -> DatasetRevisionPreviewResponse:
        """
        Returns an object that loads a preview of a dataset revision.
        The dataframe can be retrieved by calling `to_polars()` or `to_pandas()` on the return object.
        Data will be stored in .parquet format. The URIs should be considered temporary,
        and will expire after a server-defined time period.
        """
        ...

    def get_input_dataframe(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the inputs that were used to create the dataset.

        Parameters
        ----------
        ignore_errors
            Whether to ignore query errors upon fetching data
        show_progress
            Whether to show a progress bar
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        pl.LazyFrame
            A `pl.LazyFrame` materializing query input data.
        """
        ...

    def open_in_browser(self, return_url_only: bool = False) -> str:
        """Returns and opens a url that opens the offline query page
        in the Chalk dashboard. Must be logged in.

        Parameters
        ----------
        return_url_only
            If True, does not open url in browser. Default is False.

        Returns
        -------
        str
            A url redirecting to the Chalk dashboard.
        """
        ...

    def recompute(
        self,
        features: list[FeatureReference] | None = None,
        branch: str | None = None,
        wait: bool = True,
        show_progress: bool = False,
        store_plan_stages: bool = False,
        correlation_id: str | None = None,
        explain: bool = False,
        tags: list[str] | None = None,
        required_resolver_tags: list[str] | None = None,
        planner_options: Mapping[str, Union[str, int, bool]] | None = None,
        run_asynchronously: bool = False,
        timeout: float | timedelta | None | ellipsis = ...,
    ) -> Dataset:
        """Creates a new revision of this `Dataset` by recomputing the specified features.

        Carries out the new computation on the branch specified when constructing the client.

        Parameters
        ----------
        features
            A list of specific features to recompute. Features that don't exist in the dataset will be added.
            Features that already exist in the dataset will be recomputed.
            If not provided, all the existing features in the dataset will be recomputed.
        branch
            If specified, Chalk will route your request to the relevant branch.
            If None, Chalk will route your request to a non-branch deployment.
            If not specified, Chalk will use the current client's branch info.
        show_progress
            If True, progress bars will be shown while recomputation is running.
            This flag will also be propogated to the methods of the resulting
            `Dataset`.
        correlation_id
            You can specify a correlation ID to be used in logs and web interfaces.
            This should be globally unique, i.e. a `uuid` or similar. Logs generated
            during the execution of your query will be tagged with this correlation id.
        store_plan_stages
            If True, the output of each of the query plan stages will be stored
            in S3/GCS. This will dramatically impact the performance of the query,
            so it should only be used for debugging.
            These files will be visible in the web dashboard's query detail view, and
            can be downloaded in full by clicking on a plan node in the query plan visualizer.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* required_resolver_tags must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        run_asynchronously
            Boots a kubernetes job to run the queries in their own pods, separate from the engine and branch servers.
            This is useful for large datasets and jobs that require a long time to run.
            This must be specified as True to run this job asynchronously,
            even if the previous revision was run asynchronously.

        Raises
        ------
        ValueError
            If no branch was provided to the Chalk Client.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> dataset = ChalkClient(branch="data_science").offline_query(...)
        >>> df = dataset.get_data_as_polars()
        >>> # make changes to resolvers in your project
        >>> dataset.recompute()
        >>> new_df = dataset.get_data_as_polars() # receive newly computed data
        """
        ...

    def ingest(self, store_online: bool = False, store_offline: bool = True) -> Dataset:
        """
        Saves the latest revision of this dataset to Chalk's online and offline storage.

        Parameters
        ----------
        store_online
            Whether to store the revision in Chalk's online storage.
        store_offline
            Whether to store the revision in Chalk's offline storage.
        """
        ...

    def resolver_replay(
        self,
        resolver: ResolverProtocol,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> Union[pl.DataFrame, pl.LazyFrame, Mapping[str, pl.DataFrame], Mapping[str, pl.LazyFrame],]:
        """
        Downloads the resolver replay data for the given resolver in the latest revision of the dataset.

        The replay data is functionally similar to viewing the intermediate results on the plan explorer.

        If the resolver appears in only one stage of the plan, the resolver's replay data is returned directly.
        If the resolver instead appears in multiple stages of the plan, a mapping of the operation's ID to the replay data
        will be returned. If the resolver does not appear in the plan, an exception will be thrown.

        Parameters
        ----------
        resolver
            The resolver to download the replay data for, or its fqn.
        show_progress
            Whether to show progress bars
        timeout
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        """
        ...

    def write_to(self, destination: str, catalog: BaseCatalog | None = None) -> None:
        """
        Writes the dataset to a given destination.

        Parameters
        ----------
        destination
            The destination to write the dataset to.
        catalog
            The catalog to use for writing the dataset.
        """
        ...

    def set_metadata(
        self,
        metadata: Mapping[str, Any],
    ):
        """
        Set metadata for the latest dataset revision of the dataset.

        Parameters
        ----------
        metadata
            The metadata (as a dict) that you want to set for a given revision—this will fully replace
            any metadata that has already been previously set.

        Examples
        --------
        >>> from chalk.client import ChalkClient, Dataset
        >>> dataset: Dataset = ChalkClient().get_dataset(dataset_name='my_dataset_name')
        >>> dataset.set_metadata(
        ...     {"metadata": "test"}
        ... )
        """
        ...


class BulkQueryResponse(Protocol):
    scalars_df: pl.DataFrame | None
    groups_dfs: Dict[str, pl.DataFrame] | None
    errors: list[ChalkError] | None
    meta: QueryMeta | None

    def get_feature_value(self, feature: FeatureReference) -> Any:
        """Convenience method for accessing feature values from the data response.

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        Any
            The value of the feature.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature_value(User.name)
        "Katherine Johnson"
        >>> data.get_feature_value("user.name")
        "Katherine Johnson"
        """
        ...


class QueryBulkResponse(Protocol):
    responses: list[BulkQueryResponse]


class OnlineQueryResult(Protocol):
    data: list[FeatureResult]
    """The output features and any query metadata."""

    errors: list[ChalkError] | None
    """Errors encountered while running the resolvers.

    If no errors were encountered, this field is empty.
    """

    meta: QueryMeta | None
    """Metadata about the query execution.
    Only present if `include_meta=True` is passed to the relevant query method.
    """

    def get_feature(self, feature: FeatureReference) -> FeatureResult | None:
        """Convenience method for accessing feature result from the data response.

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        FeatureResult | None
            The `FeatureResult` for the feature, if it exists.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature(User.name).ts
        datetime.datetime(2023, 2, 5, 23, 25, 26, 427605)
        >>> data.get_feature("user.name").meta.cache_hit
        False
        """
        ...

    def get_feature_value(self, feature: FeatureReference) -> Any:
        """Convenience method for accessing feature values from the data response.

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        Any
            The value of the feature.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature_value(User.name)
        "Katherine Johnson"
        >>> data.get_feature_value("user.name")
        "Katherine Johnson"
        """
        ...

    def to_dict(self, prefix: bool = True) -> dict[str, Any]:
        """Converts the output features to a dictionary.
        Errors are not included in the dictionary.

        Returns
        -------
        dict[str, Any]
            A dictionary of the output features.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> result = ChalkClient().query(...)
        >>> result.to_dict()
        {
            "user.name": "Katherine Johnson",
            "user.email": "katherine@nasa.com"
        }
        """
        ...

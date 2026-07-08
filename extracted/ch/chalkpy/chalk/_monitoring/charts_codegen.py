# AUTO-GENERATED FILE. Do not edit.
from typing import Any, Dict, List, Literal, Optional, Tuple, TypeVar, Union

from chalk._monitoring.charts_enums_codegen import GroupByKind
from chalk._monitoring.charts_series_base import ResolverType, SeriesBase
from chalk.features.resolver import ResolverProtocol


class Series(SeriesBase):
    """
    Class describing a series of data in two dimensions, as in a line chart.
    Series should be instantiated with one of the classmethods that specifies
    the metric to be tracked.
    """

    def __new__(cls, *args, **kwargs):
        raise ValueError("Please construct a Series with a metric classmethod")

    @classmethod
    def feature_request_count_metric(cls, name: Optional[str] = None) -> "FeatureRequestCountSeries":
        """Creates a `Series` of metric kind `FeatureRequestCount`.

        Parameters
        ----------
        name
            A name for your new `feature_request_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureRequestCountSeries
            A new `FeatureRequestCountSeries` instance that inherits from the `Series` class.
        """
        return FeatureRequestCountSeries(
            name=name,
            metric="FEATURE_REQUEST_COUNT",
        )

    @classmethod
    def feature_computed_count_metric(cls, name: Optional[str] = None) -> "FeatureComputedCountSeries":
        """Creates a `Series` of metric kind `FeatureComputedCount`.

        Parameters
        ----------
        name
            A name for your new `feature_computed_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureComputedCountSeries
            A new `FeatureComputedCountSeries` instance that inherits from the `Series` class.
        """
        return FeatureComputedCountSeries(
            name=name,
            metric="FEATURE_COMPUTED_COUNT",
        )

    @classmethod
    def feature_looked_up_count_metric(cls, name: Optional[str] = None) -> "FeatureLookedUpCountSeries":
        """Creates a `Series` of metric kind `FeatureLookedUpCount`.

        Parameters
        ----------
        name
            A name for your new `feature_looked_up_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureLookedUpCountSeries
            A new `FeatureLookedUpCountSeries` instance that inherits from the `Series` class.
        """
        return FeatureLookedUpCountSeries(
            name=name,
            metric="FEATURE_LOOKED_UP_COUNT",
        )

    @classmethod
    def feature_intermediate_count_metric(cls, name: Optional[str] = None) -> "FeatureIntermediateCountSeries":
        """Creates a `Series` of metric kind `FeatureIntermediateCount`.

        Parameters
        ----------
        name
            A name for your new `feature_intermediate_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureIntermediateCountSeries
            A new `FeatureIntermediateCountSeries` instance that inherits from the `Series` class.
        """
        return FeatureIntermediateCountSeries(
            name=name,
            metric="FEATURE_INTERMEDIATE_COUNT",
        )

    @classmethod
    def feature_staleness_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "FeatureStalenessSeries":
        """Creates a `Series` of metric kind `FeatureStaleness`.

        Parameters
        ----------
        name
            A name for your new `feature_staleness` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        FeatureStalenessSeries
            A new `FeatureStalenessSeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return FeatureStalenessSeries(name=name, metric="FEATURE_STALENESS", window_function=window_function)

    @classmethod
    def feature_value_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "FeatureValueSeries":
        """Creates a `Series` of metric kind `FeatureValue`.

        Parameters
        ----------
        name
            A name for your new `feature_value` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        FeatureValueSeries
            A new `FeatureValueSeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return FeatureValueSeries(name=name, metric="FEATURE_VALUE", window_function=window_function)

    @classmethod
    def feature_null_ratio_metric(cls, name: Optional[str] = None) -> "FeatureNullRatioSeries":
        """Creates a `Series` of metric kind `FeatureNullRatio`.

        Parameters
        ----------
        name
            A name for your new `feature_null_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureNullRatioSeries
            A new `FeatureNullRatioSeries` instance that inherits from the `Series` class.
        """
        return FeatureNullRatioSeries(
            name=name,
            metric="FEATURE_NULL_RATIO",
        )

    @classmethod
    def feature_computed_null_ratio_metric(cls, name: Optional[str] = None) -> "FeatureComputedNullRatioSeries":
        """Creates a `Series` of metric kind `FeatureComputedNullRatio`.

        Parameters
        ----------
        name
            A name for your new `feature_computed_null_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureComputedNullRatioSeries
            A new `FeatureComputedNullRatioSeries` instance that inherits from the `Series` class.
        """
        return FeatureComputedNullRatioSeries(
            name=name,
            metric="FEATURE_COMPUTED_NULL_RATIO",
        )

    @classmethod
    def feature_looked_up_null_ratio_metric(cls, name: Optional[str] = None) -> "FeatureLookedUpNullRatioSeries":
        """Creates a `Series` of metric kind `FeatureLookedUpNullRatio`.

        Parameters
        ----------
        name
            A name for your new `feature_looked_up_null_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureLookedUpNullRatioSeries
            A new `FeatureLookedUpNullRatioSeries` instance that inherits from the `Series` class.
        """
        return FeatureLookedUpNullRatioSeries(
            name=name,
            metric="FEATURE_LOOKED_UP_NULL_RATIO",
        )

    @classmethod
    def feature_intermediate_null_ratio_metric(cls, name: Optional[str] = None) -> "FeatureIntermediateNullRatioSeries":
        """Creates a `Series` of metric kind `FeatureIntermediateNullRatio`.

        Parameters
        ----------
        name
            A name for your new `feature_intermediate_null_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FeatureIntermediateNullRatioSeries
            A new `FeatureIntermediateNullRatioSeries` instance that inherits from the `Series` class.
        """
        return FeatureIntermediateNullRatioSeries(
            name=name,
            metric="FEATURE_INTERMEDIATE_NULL_RATIO",
        )

    @classmethod
    def resolver_request_count_metric(cls, name: Optional[str] = None) -> "ResolverRequestCountSeries":
        """Creates a `Series` of metric kind `ResolverRequestCount`.

        Parameters
        ----------
        name
            A name for your new `resolver_request_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ResolverRequestCountSeries
            A new `ResolverRequestCountSeries` instance that inherits from the `Series` class.
        """
        return ResolverRequestCountSeries(
            name=name,
            metric="RESOLVER_REQUEST_COUNT",
        )

    @classmethod
    def resolver_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "ResolverLatencySeries":
        """Creates a `Series` of metric kind `ResolverLatency`.

        Parameters
        ----------
        name
            A name for your new `resolver_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        ResolverLatencySeries
            A new `ResolverLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return ResolverLatencySeries(name=name, metric="RESOLVER_LATENCY", window_function=window_function)

    @classmethod
    def resolver_success_ratio_metric(cls, name: Optional[str] = None) -> "ResolverSuccessRatioSeries":
        """Creates a `Series` of metric kind `ResolverSuccessRatio`.

        Parameters
        ----------
        name
            A name for your new `resolver_success_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ResolverSuccessRatioSeries
            A new `ResolverSuccessRatioSeries` instance that inherits from the `Series` class.
        """
        return ResolverSuccessRatioSeries(
            name=name,
            metric="RESOLVER_SUCCESS_RATIO",
        )

    @classmethod
    def query_count_metric(cls, name: Optional[str] = None) -> "QueryCountSeries":
        """Creates a `Series` of metric kind `QueryCount`.

        Parameters
        ----------
        name
            A name for your new `query_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryCountSeries
            A new `QueryCountSeries` instance that inherits from the `Series` class.
        """
        return QueryCountSeries(
            name=name,
            metric="QUERY_COUNT",
        )

    @classmethod
    def query_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "QueryLatencySeries":
        """Creates a `Series` of metric kind `QueryLatency`.

        Parameters
        ----------
        name
            A name for your new `query_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        QueryLatencySeries
            A new `QueryLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return QueryLatencySeries(name=name, metric="QUERY_LATENCY", window_function=window_function)

    @classmethod
    def query_success_ratio_metric(cls, name: Optional[str] = None) -> "QuerySuccessRatioSeries":
        """Creates a `Series` of metric kind `QuerySuccessRatio`.

        Parameters
        ----------
        name
            A name for your new `query_success_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QuerySuccessRatioSeries
            A new `QuerySuccessRatioSeries` instance that inherits from the `Series` class.
        """
        return QuerySuccessRatioSeries(
            name=name,
            metric="QUERY_SUCCESS_RATIO",
        )

    @classmethod
    def cron_count_metric(cls, name: Optional[str] = None) -> "CronCountSeries":
        """Creates a `Series` of metric kind `CronCount`.

        Parameters
        ----------
        name
            A name for your new `cron_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        CronCountSeries
            A new `CronCountSeries` instance that inherits from the `Series` class.
        """
        return CronCountSeries(
            name=name,
            metric="CRON_COUNT",
        )

    @classmethod
    def cron_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "CronLatencySeries":
        """Creates a `Series` of metric kind `CronLatency`.

        Parameters
        ----------
        name
            A name for your new `cron_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        CronLatencySeries
            A new `CronLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return CronLatencySeries(name=name, metric="CRON_LATENCY", window_function=window_function)

    @classmethod
    def cpu_utilization_percent_metric(cls, name: Optional[str] = None) -> "CpuUtilizationPercentSeries":
        """Creates a `Series` of metric kind `CpuUtilizationPercent`.

        Parameters
        ----------
        name
            A name for your new `cpu_utilization_percent` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        CpuUtilizationPercentSeries
            A new `CpuUtilizationPercentSeries` instance that inherits from the `Series` class.
        """
        return CpuUtilizationPercentSeries(
            name=name,
            metric="CPU_UTILIZATION_PERCENT",
        )

    @classmethod
    def memory_usage_bytes_metric(cls, name: Optional[str] = None) -> "MemoryUsageBytesSeries":
        """Creates a `Series` of metric kind `MemoryUsageBytes`.

        Parameters
        ----------
        name
            A name for your new `memory_usage_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        MemoryUsageBytesSeries
            A new `MemoryUsageBytesSeries` instance that inherits from the `Series` class.
        """
        return MemoryUsageBytesSeries(
            name=name,
            metric="MEMORY_USAGE_BYTES",
        )

    @classmethod
    def total_memory_available_bytes_metric(cls, name: Optional[str] = None) -> "TotalMemoryAvailableBytesSeries":
        """Creates a `Series` of metric kind `TotalMemoryAvailableBytes`.

        Parameters
        ----------
        name
            A name for your new `total_memory_available_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        TotalMemoryAvailableBytesSeries
            A new `TotalMemoryAvailableBytesSeries` instance that inherits from the `Series` class.
        """
        return TotalMemoryAvailableBytesSeries(
            name=name,
            metric="TOTAL_MEMORY_AVAILABLE_BYTES",
        )

    @classmethod
    def network_read_bytes_metric(cls, name: Optional[str] = None) -> "NetworkReadBytesSeries":
        """Creates a `Series` of metric kind `NetworkReadBytes`.

        Parameters
        ----------
        name
            A name for your new `network_read_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        NetworkReadBytesSeries
            A new `NetworkReadBytesSeries` instance that inherits from the `Series` class.
        """
        return NetworkReadBytesSeries(
            name=name,
            metric="NETWORK_READ_BYTES",
        )

    @classmethod
    def network_write_bytes_metric(cls, name: Optional[str] = None) -> "NetworkWriteBytesSeries":
        """Creates a `Series` of metric kind `NetworkWriteBytes`.

        Parameters
        ----------
        name
            A name for your new `network_write_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        NetworkWriteBytesSeries
            A new `NetworkWriteBytesSeries` instance that inherits from the `Series` class.
        """
        return NetworkWriteBytesSeries(
            name=name,
            metric="NETWORK_WRITE_BYTES",
        )

    @classmethod
    def disk_read_bytes_metric(cls, name: Optional[str] = None) -> "DiskReadBytesSeries":
        """Creates a `Series` of metric kind `DiskReadBytes`.

        Parameters
        ----------
        name
            A name for your new `disk_read_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        DiskReadBytesSeries
            A new `DiskReadBytesSeries` instance that inherits from the `Series` class.
        """
        return DiskReadBytesSeries(
            name=name,
            metric="DISK_READ_BYTES",
        )

    @classmethod
    def disk_write_bytes_metric(cls, name: Optional[str] = None) -> "DiskWriteBytesSeries":
        """Creates a `Series` of metric kind `DiskWriteBytes`.

        Parameters
        ----------
        name
            A name for your new `disk_write_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        DiskWriteBytesSeries
            A new `DiskWriteBytesSeries` instance that inherits from the `Series` class.
        """
        return DiskWriteBytesSeries(
            name=name,
            metric="DISK_WRITE_BYTES",
        )

    @classmethod
    def stream_message_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "StreamMessageLatencySeries":
        """Creates a `Series` of metric kind `StreamMessageLatency`.

        Parameters
        ----------
        name
            A name for your new `stream_message_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        StreamMessageLatencySeries
            A new `StreamMessageLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return StreamMessageLatencySeries(name=name, metric="STREAM_MESSAGE_LATENCY", window_function=window_function)

    @classmethod
    def stream_messages_processed_metric(cls, name: Optional[str] = None) -> "StreamMessagesProcessedSeries":
        """Creates a `Series` of metric kind `StreamMessagesProcessed`.

        Parameters
        ----------
        name
            A name for your new `stream_messages_processed` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        StreamMessagesProcessedSeries
            A new `StreamMessagesProcessedSeries` instance that inherits from the `Series` class.
        """
        return StreamMessagesProcessedSeries(
            name=name,
            metric="STREAM_MESSAGES_PROCESSED",
        )

    @classmethod
    def stream_windows_processed_metric(cls, name: Optional[str] = None) -> "StreamWindowsProcessedSeries":
        """Creates a `Series` of metric kind `StreamWindowsProcessed`.

        Parameters
        ----------
        name
            A name for your new `stream_windows_processed` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        StreamWindowsProcessedSeries
            A new `StreamWindowsProcessedSeries` instance that inherits from the `Series` class.
        """
        return StreamWindowsProcessedSeries(
            name=name,
            metric="STREAM_WINDOWS_PROCESSED",
        )

    @classmethod
    def stream_window_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "StreamWindowLatencySeries":
        """Creates a `Series` of metric kind `StreamWindowLatency`.

        Parameters
        ----------
        name
            A name for your new `stream_window_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        StreamWindowLatencySeries
            A new `StreamWindowLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return StreamWindowLatencySeries(name=name, metric="STREAM_WINDOW_LATENCY", window_function=window_function)

    @classmethod
    def stream_lag_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "StreamLagSeries":
        """Creates a `Series` of metric kind `StreamLag`.

        Parameters
        ----------
        name
            A name for your new `stream_lag` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        StreamLagSeries
            A new `StreamLagSeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return StreamLagSeries(name=name, metric="STREAM_LAG", window_function=window_function)

    @classmethod
    def stream_ingest_delay_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "StreamIngestDelaySeries":
        """Creates a `Series` of metric kind `StreamIngestDelay`.

        Parameters
        ----------
        name
            A name for your new `stream_ingest_delay` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        StreamIngestDelaySeries
            A new `StreamIngestDelaySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return StreamIngestDelaySeries(name=name, metric="STREAM_INGEST_DELAY", window_function=window_function)

    @classmethod
    def online_store_used_memory_metric(cls, name: Optional[str] = None) -> "OnlineStoreUsedMemorySeries":
        """Creates a `Series` of metric kind `OnlineStoreUsedMemory`.

        Parameters
        ----------
        name
            A name for your new `online_store_used_memory` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        OnlineStoreUsedMemorySeries
            A new `OnlineStoreUsedMemorySeries` instance that inherits from the `Series` class.
        """
        return OnlineStoreUsedMemorySeries(
            name=name,
            metric="ONLINE_STORE_USED_MEMORY",
        )

    @classmethod
    def online_store_key_count_metric(cls, name: Optional[str] = None) -> "OnlineStoreKeyCountSeries":
        """Creates a `Series` of metric kind `OnlineStoreKeyCount`.

        Parameters
        ----------
        name
            A name for your new `online_store_key_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        OnlineStoreKeyCountSeries
            A new `OnlineStoreKeyCountSeries` instance that inherits from the `Series` class.
        """
        return OnlineStoreKeyCountSeries(
            name=name,
            metric="ONLINE_STORE_KEY_COUNT",
        )

    @classmethod
    def online_store_expired_key_count_metric(cls, name: Optional[str] = None) -> "OnlineStoreExpiredKeyCountSeries":
        """Creates a `Series` of metric kind `OnlineStoreExpiredKeyCount`.

        Parameters
        ----------
        name
            A name for your new `online_store_expired_key_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        OnlineStoreExpiredKeyCountSeries
            A new `OnlineStoreExpiredKeyCountSeries` instance that inherits from the `Series` class.
        """
        return OnlineStoreExpiredKeyCountSeries(
            name=name,
            metric="ONLINE_STORE_EXPIRED_KEY_COUNT",
        )

    @classmethod
    def online_store_requests_per_second_metric(
        cls, name: Optional[str] = None
    ) -> "OnlineStoreRequestsPerSecondSeries":
        """Creates a `Series` of metric kind `OnlineStoreRequestsPerSecond`.

        Parameters
        ----------
        name
            A name for your new `online_store_requests_per_second` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        OnlineStoreRequestsPerSecondSeries
            A new `OnlineStoreRequestsPerSecondSeries` instance that inherits from the `Series` class.
        """
        return OnlineStoreRequestsPerSecondSeries(
            name=name,
            metric="ONLINE_STORE_REQUESTS_PER_SECOND",
        )

    @classmethod
    def online_store_total_memory_metric(cls, name: Optional[str] = None) -> "OnlineStoreTotalMemorySeries":
        """Creates a `Series` of metric kind `OnlineStoreTotalMemory`.

        Parameters
        ----------
        name
            A name for your new `online_store_total_memory` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        OnlineStoreTotalMemorySeries
            A new `OnlineStoreTotalMemorySeries` instance that inherits from the `Series` class.
        """
        return OnlineStoreTotalMemorySeries(
            name=name,
            metric="ONLINE_STORE_TOTAL_MEMORY",
        )

    @classmethod
    def container_memory_bytes_metric(cls, name: Optional[str] = None) -> "ContainerMemoryBytesSeries":
        """Creates a `Series` of metric kind `ContainerMemoryBytes`.

        Parameters
        ----------
        name
            A name for your new `container_memory_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ContainerMemoryBytesSeries
            A new `ContainerMemoryBytesSeries` instance that inherits from the `Series` class.
        """
        return ContainerMemoryBytesSeries(
            name=name,
            metric="CONTAINER_MEMORY_BYTES",
        )

    @classmethod
    def host_memory_bytes_metric(cls, name: Optional[str] = None) -> "HostMemoryBytesSeries":
        """Creates a `Series` of metric kind `HostMemoryBytes`.

        Parameters
        ----------
        name
            A name for your new `host_memory_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        HostMemoryBytesSeries
            A new `HostMemoryBytesSeries` instance that inherits from the `Series` class.
        """
        return HostMemoryBytesSeries(
            name=name,
            metric="HOST_MEMORY_BYTES",
        )

    @classmethod
    def container_cpu_utilization_metric(cls, name: Optional[str] = None) -> "ContainerCpuUtilizationSeries":
        """Creates a `Series` of metric kind `ContainerCpuUtilization`.

        Parameters
        ----------
        name
            A name for your new `container_cpu_utilization` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ContainerCpuUtilizationSeries
            A new `ContainerCpuUtilizationSeries` instance that inherits from the `Series` class.
        """
        return ContainerCpuUtilizationSeries(
            name=name,
            metric="CONTAINER_CPU_UTILIZATION",
        )

    @classmethod
    def gpu_utilization_metric(cls, name: Optional[str] = None) -> "GpuUtilizationSeries":
        """Creates a `Series` of metric kind `GpuUtilization`.

        Parameters
        ----------
        name
            A name for your new `gpu_utilization` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuUtilizationSeries
            A new `GpuUtilizationSeries` instance that inherits from the `Series` class.
        """
        return GpuUtilizationSeries(
            name=name,
            metric="GPU_UTILIZATION",
        )

    @classmethod
    def gpu_tensor_activity_metric(cls, name: Optional[str] = None) -> "GpuTensorActivitySeries":
        """Creates a `Series` of metric kind `GpuTensorActivity`.

        Parameters
        ----------
        name
            A name for your new `gpu_tensor_activity` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuTensorActivitySeries
            A new `GpuTensorActivitySeries` instance that inherits from the `Series` class.
        """
        return GpuTensorActivitySeries(
            name=name,
            metric="GPU_TENSOR_ACTIVITY",
        )

    @classmethod
    def gpu_sm_clock_mhz_metric(cls, name: Optional[str] = None) -> "GpuSmClockMhzSeries":
        """Creates a `Series` of metric kind `GpuSmClockMhz`.

        Parameters
        ----------
        name
            A name for your new `gpu_sm_clock_mhz` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuSmClockMhzSeries
            A new `GpuSmClockMhzSeries` instance that inherits from the `Series` class.
        """
        return GpuSmClockMhzSeries(
            name=name,
            metric="GPU_SM_CLOCK_MHZ",
        )

    @classmethod
    def gpu_power_watts_metric(cls, name: Optional[str] = None) -> "GpuPowerWattsSeries":
        """Creates a `Series` of metric kind `GpuPowerWatts`.

        Parameters
        ----------
        name
            A name for your new `gpu_power_watts` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuPowerWattsSeries
            A new `GpuPowerWattsSeries` instance that inherits from the `Series` class.
        """
        return GpuPowerWattsSeries(
            name=name,
            metric="GPU_POWER_WATTS",
        )

    @classmethod
    def gpu_temperature_celsius_metric(cls, name: Optional[str] = None) -> "GpuTemperatureCelsiusSeries":
        """Creates a `Series` of metric kind `GpuTemperatureCelsius`.

        Parameters
        ----------
        name
            A name for your new `gpu_temperature_celsius` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuTemperatureCelsiusSeries
            A new `GpuTemperatureCelsiusSeries` instance that inherits from the `Series` class.
        """
        return GpuTemperatureCelsiusSeries(
            name=name,
            metric="GPU_TEMPERATURE_CELSIUS",
        )

    @classmethod
    def gpu_throttle_reasons_metric(cls, name: Optional[str] = None) -> "GpuThrottleReasonsSeries":
        """Creates a `Series` of metric kind `GpuThrottleReasons`.

        Parameters
        ----------
        name
            A name for your new `gpu_throttle_reasons` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuThrottleReasonsSeries
            A new `GpuThrottleReasonsSeries` instance that inherits from the `Series` class.
        """
        return GpuThrottleReasonsSeries(
            name=name,
            metric="GPU_THROTTLE_REASONS",
        )

    @classmethod
    def gpu_fp16_activity_metric(cls, name: Optional[str] = None) -> "GpuFp16ActivitySeries":
        """Creates a `Series` of metric kind `GpuFp16Activity`.

        Parameters
        ----------
        name
            A name for your new `gpu_fp16_activity` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        GpuFp16ActivitySeries
            A new `GpuFp16ActivitySeries` instance that inherits from the `Series` class.
        """
        return GpuFp16ActivitySeries(
            name=name,
            metric="GPU_FP16_ACTIVITY",
        )

    @classmethod
    def disk_used_bytes_metric(cls, name: Optional[str] = None) -> "DiskUsedBytesSeries":
        """Creates a `Series` of metric kind `DiskUsedBytes`.

        Parameters
        ----------
        name
            A name for your new `disk_used_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        DiskUsedBytesSeries
            A new `DiskUsedBytesSeries` instance that inherits from the `Series` class.
        """
        return DiskUsedBytesSeries(
            name=name,
            metric="DISK_USED_BYTES",
        )

    @classmethod
    def disk_available_bytes_metric(cls, name: Optional[str] = None) -> "DiskAvailableBytesSeries":
        """Creates a `Series` of metric kind `DiskAvailableBytes`.

        Parameters
        ----------
        name
            A name for your new `disk_available_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        DiskAvailableBytesSeries
            A new `DiskAvailableBytesSeries` instance that inherits from the `Series` class.
        """
        return DiskAvailableBytesSeries(
            name=name,
            metric="DISK_AVAILABLE_BYTES",
        )

    @classmethod
    def resolver_invoker_net_rx_metric(cls, name: Optional[str] = None) -> "ResolverInvokerNetRxSeries":
        """Creates a `Series` of metric kind `ResolverInvokerNetRx`.

        Parameters
        ----------
        name
            A name for your new `resolver_invoker_net_rx` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ResolverInvokerNetRxSeries
            A new `ResolverInvokerNetRxSeries` instance that inherits from the `Series` class.
        """
        return ResolverInvokerNetRxSeries(
            name=name,
            metric="RESOLVER_INVOKER_NET_RX",
        )

    @classmethod
    def resolver_invoker_net_tx_metric(cls, name: Optional[str] = None) -> "ResolverInvokerNetTxSeries":
        """Creates a `Series` of metric kind `ResolverInvokerNetTx`.

        Parameters
        ----------
        name
            A name for your new `resolver_invoker_net_tx` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ResolverInvokerNetTxSeries
            A new `ResolverInvokerNetTxSeries` instance that inherits from the `Series` class.
        """
        return ResolverInvokerNetTxSeries(
            name=name,
            metric="RESOLVER_INVOKER_NET_TX",
        )

    @classmethod
    def resolver_invoker_rows_written_metric(cls, name: Optional[str] = None) -> "ResolverInvokerRowsWrittenSeries":
        """Creates a `Series` of metric kind `ResolverInvokerRowsWritten`.

        Parameters
        ----------
        name
            A name for your new `resolver_invoker_rows_written` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ResolverInvokerRowsWrittenSeries
            A new `ResolverInvokerRowsWrittenSeries` instance that inherits from the `Series` class.
        """
        return ResolverInvokerRowsWrittenSeries(
            name=name,
            metric="RESOLVER_INVOKER_ROWS_WRITTEN",
        )

    @classmethod
    def replica_count_metric(cls, name: Optional[str] = None) -> "ReplicaCountSeries":
        """Creates a `Series` of metric kind `ReplicaCount`.

        Parameters
        ----------
        name
            A name for your new `replica_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ReplicaCountSeries
            A new `ReplicaCountSeries` instance that inherits from the `Series` class.
        """
        return ReplicaCountSeries(
            name=name,
            metric="REPLICA_COUNT",
        )

    @classmethod
    def pull_query_queue_depth_metric(cls, name: Optional[str] = None) -> "PullQueryQueueDepthSeries":
        """Creates a `Series` of metric kind `PullQueryQueueDepth`.

        Parameters
        ----------
        name
            A name for your new `pull_query_queue_depth` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        PullQueryQueueDepthSeries
            A new `PullQueryQueueDepthSeries` instance that inherits from the `Series` class.
        """
        return PullQueryQueueDepthSeries(
            name=name,
            metric="PULL_QUERY_QUEUE_DEPTH",
        )

    @classmethod
    def pull_query_oldest_unacked_age_metric(cls, name: Optional[str] = None) -> "PullQueryOldestUnackedAgeSeries":
        """Creates a `Series` of metric kind `PullQueryOldestUnackedAge`.

        Parameters
        ----------
        name
            A name for your new `pull_query_oldest_unacked_age` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        PullQueryOldestUnackedAgeSeries
            A new `PullQueryOldestUnackedAgeSeries` instance that inherits from the `Series` class.
        """
        return PullQueryOldestUnackedAgeSeries(
            name=name,
            metric="PULL_QUERY_OLDEST_UNACKED_AGE",
        )

    @classmethod
    def pull_query_processed_metric(cls, name: Optional[str] = None) -> "PullQueryProcessedSeries":
        """Creates a `Series` of metric kind `PullQueryProcessed`.

        Parameters
        ----------
        name
            A name for your new `pull_query_processed` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        PullQueryProcessedSeries
            A new `PullQueryProcessedSeries` instance that inherits from the `Series` class.
        """
        return PullQueryProcessedSeries(
            name=name,
            metric="PULL_QUERY_PROCESSED",
        )

    @classmethod
    def pull_query_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "PullQueryLatencySeries":
        """Creates a `Series` of metric kind `PullQueryLatency`.

        Parameters
        ----------
        name
            A name for your new `pull_query_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        PullQueryLatencySeries
            A new `PullQueryLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return PullQueryLatencySeries(name=name, metric="PULL_QUERY_LATENCY", window_function=window_function)

    @classmethod
    def pull_query_max_inflight_metric(cls, name: Optional[str] = None) -> "PullQueryMaxInflightSeries":
        """Creates a `Series` of metric kind `PullQueryMaxInflight`.

        Parameters
        ----------
        name
            A name for your new `pull_query_max_inflight` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        PullQueryMaxInflightSeries
            A new `PullQueryMaxInflightSeries` instance that inherits from the `Series` class.
        """
        return PullQueryMaxInflightSeries(
            name=name,
            metric="PULL_QUERY_MAX_INFLIGHT",
        )

    @classmethod
    def pull_query_concurrency_target_metric(cls, name: Optional[str] = None) -> "PullQueryConcurrencyTargetSeries":
        """Creates a `Series` of metric kind `PullQueryConcurrencyTarget`.

        Parameters
        ----------
        name
            A name for your new `pull_query_concurrency_target` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        PullQueryConcurrencyTargetSeries
            A new `PullQueryConcurrencyTargetSeries` instance that inherits from the `Series` class.
        """
        return PullQueryConcurrencyTargetSeries(
            name=name,
            metric="PULL_QUERY_CONCURRENCY_TARGET",
        )

    @classmethod
    def pull_query_open_connections_metric(cls, name: Optional[str] = None) -> "PullQueryOpenConnectionsSeries":
        """Creates a `Series` of metric kind `PullQueryOpenConnections`.

        Parameters
        ----------
        name
            A name for your new `pull_query_open_connections` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        PullQueryOpenConnectionsSeries
            A new `PullQueryOpenConnectionsSeries` instance that inherits from the `Series` class.
        """
        return PullQueryOpenConnectionsSeries(
            name=name,
            metric="PULL_QUERY_OPEN_CONNECTIONS",
        )

    @classmethod
    def function_call_enqueued_metric(cls, name: Optional[str] = None) -> "FunctionCallEnqueuedSeries":
        """Creates a `Series` of metric kind `FunctionCallEnqueued`.

        Parameters
        ----------
        name
            A name for your new `function_call_enqueued` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FunctionCallEnqueuedSeries
            A new `FunctionCallEnqueuedSeries` instance that inherits from the `Series` class.
        """
        return FunctionCallEnqueuedSeries(
            name=name,
            metric="FUNCTION_CALL_ENQUEUED",
        )

    @classmethod
    def function_call_enqueue_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "FunctionCallEnqueueLatencySeries":
        """Creates a `Series` of metric kind `FunctionCallEnqueueLatency`.

        Parameters
        ----------
        name
            A name for your new `function_call_enqueue_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        FunctionCallEnqueueLatencySeries
            A new `FunctionCallEnqueueLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return FunctionCallEnqueueLatencySeries(
            name=name, metric="FUNCTION_CALL_ENQUEUE_LATENCY", window_function=window_function
        )

    @classmethod
    def function_call_open_connections_metric(cls, name: Optional[str] = None) -> "FunctionCallOpenConnectionsSeries":
        """Creates a `Series` of metric kind `FunctionCallOpenConnections`.

        Parameters
        ----------
        name
            A name for your new `function_call_open_connections` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FunctionCallOpenConnectionsSeries
            A new `FunctionCallOpenConnectionsSeries` instance that inherits from the `Series` class.
        """
        return FunctionCallOpenConnectionsSeries(
            name=name,
            metric="FUNCTION_CALL_OPEN_CONNECTIONS",
        )

    @classmethod
    def function_call_dequeued_metric(cls, name: Optional[str] = None) -> "FunctionCallDequeuedSeries":
        """Creates a `Series` of metric kind `FunctionCallDequeued`.

        Parameters
        ----------
        name
            A name for your new `function_call_dequeued` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FunctionCallDequeuedSeries
            A new `FunctionCallDequeuedSeries` instance that inherits from the `Series` class.
        """
        return FunctionCallDequeuedSeries(
            name=name,
            metric="FUNCTION_CALL_DEQUEUED",
        )

    @classmethod
    def function_call_processing_latency_metric(
        cls,
        window_function: Literal["mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
        name: Optional[str] = None,
    ) -> "FunctionCallProcessingLatencySeries":
        """Creates a `Series` of metric kind `FunctionCallProcessingLatency`.

        Parameters
        ----------
        name
            A name for your new `function_call_processing_latency` `Series`.
            If not provided, a name will be generated for you.
        window_function
            The time window to calculate the metric over.

        Returns
        -------
        FunctionCallProcessingLatencySeries
            A new `FunctionCallProcessingLatencySeries` instance that inherits from the `Series` class.
        """
        if window_function not in {"mean", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return FunctionCallProcessingLatencySeries(
            name=name, metric="FUNCTION_CALL_PROCESSING_LATENCY", window_function=window_function
        )

    @classmethod
    def function_call_queue_depth_metric(cls, name: Optional[str] = None) -> "FunctionCallQueueDepthSeries":
        """Creates a `Series` of metric kind `FunctionCallQueueDepth`.

        Parameters
        ----------
        name
            A name for your new `function_call_queue_depth` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FunctionCallQueueDepthSeries
            A new `FunctionCallQueueDepthSeries` instance that inherits from the `Series` class.
        """
        return FunctionCallQueueDepthSeries(
            name=name,
            metric="FUNCTION_CALL_QUEUE_DEPTH",
        )

    @classmethod
    def function_call_inflight_metric(cls, name: Optional[str] = None) -> "FunctionCallInflightSeries":
        """Creates a `Series` of metric kind `FunctionCallInflight`.

        Parameters
        ----------
        name
            A name for your new `function_call_inflight` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        FunctionCallInflightSeries
            A new `FunctionCallInflightSeries` instance that inherits from the `Series` class.
        """
        return FunctionCallInflightSeries(
            name=name,
            metric="FUNCTION_CALL_INFLIGHT",
        )

    @classmethod
    def query_progress_splits_processed_metric(cls, name: Optional[str] = None) -> "QueryProgressSplitsProcessedSeries":
        """Creates a `Series` of metric kind `QueryProgressSplitsProcessed`.

        Parameters
        ----------
        name
            A name for your new `query_progress_splits_processed` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryProgressSplitsProcessedSeries
            A new `QueryProgressSplitsProcessedSeries` instance that inherits from the `Series` class.
        """
        return QueryProgressSplitsProcessedSeries(
            name=name,
            metric="QUERY_PROGRESS_SPLITS_PROCESSED",
        )

    @classmethod
    def query_progress_splits_queued_metric(cls, name: Optional[str] = None) -> "QueryProgressSplitsQueuedSeries":
        """Creates a `Series` of metric kind `QueryProgressSplitsQueued`.

        Parameters
        ----------
        name
            A name for your new `query_progress_splits_queued` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryProgressSplitsQueuedSeries
            A new `QueryProgressSplitsQueuedSeries` instance that inherits from the `Series` class.
        """
        return QueryProgressSplitsQueuedSeries(
            name=name,
            metric="QUERY_PROGRESS_SPLITS_QUEUED",
        )

    @classmethod
    def query_progress_blocked_drivers_metric(cls, name: Optional[str] = None) -> "QueryProgressBlockedDriversSeries":
        """Creates a `Series` of metric kind `QueryProgressBlockedDrivers`.

        Parameters
        ----------
        name
            A name for your new `query_progress_blocked_drivers` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryProgressBlockedDriversSeries
            A new `QueryProgressBlockedDriversSeries` instance that inherits from the `Series` class.
        """
        return QueryProgressBlockedDriversSeries(
            name=name,
            metric="QUERY_PROGRESS_BLOCKED_DRIVERS",
        )

    @classmethod
    def query_progress_resolver_rows_returned_metric(
        cls, name: Optional[str] = None
    ) -> "QueryProgressResolverRowsReturnedSeries":
        """Creates a `Series` of metric kind `QueryProgressResolverRowsReturned`.

        Parameters
        ----------
        name
            A name for your new `query_progress_resolver_rows_returned` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryProgressResolverRowsReturnedSeries
            A new `QueryProgressResolverRowsReturnedSeries` instance that inherits from the `Series` class.
        """
        return QueryProgressResolverRowsReturnedSeries(
            name=name,
            metric="QUERY_PROGRESS_RESOLVER_ROWS_RETURNED",
        )

    @classmethod
    def query_progress_operator_output_bytes_metric(
        cls, name: Optional[str] = None
    ) -> "QueryProgressOperatorOutputBytesSeries":
        """Creates a `Series` of metric kind `QueryProgressOperatorOutputBytes`.

        Parameters
        ----------
        name
            A name for your new `query_progress_operator_output_bytes` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryProgressOperatorOutputBytesSeries
            A new `QueryProgressOperatorOutputBytesSeries` instance that inherits from the `Series` class.
        """
        return QueryProgressOperatorOutputBytesSeries(
            name=name,
            metric="QUERY_PROGRESS_OPERATOR_OUTPUT_BYTES",
        )

    @classmethod
    def query_progress_operator_rows_processed_metric(
        cls, name: Optional[str] = None
    ) -> "QueryProgressOperatorRowsProcessedSeries":
        """Creates a `Series` of metric kind `QueryProgressOperatorRowsProcessed`.

        Parameters
        ----------
        name
            A name for your new `query_progress_operator_rows_processed` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        QueryProgressOperatorRowsProcessedSeries
            A new `QueryProgressOperatorRowsProcessedSeries` instance that inherits from the `Series` class.
        """
        return QueryProgressOperatorRowsProcessedSeries(
            name=name,
            metric="QUERY_PROGRESS_OPERATOR_ROWS_PROCESSED",
        )

    @classmethod
    def scheduled_query_count_metric(cls, name: Optional[str] = None) -> "ScheduledQueryCountSeries":
        """Creates a `Series` of metric kind `ScheduledQueryCount`.

        Parameters
        ----------
        name
            A name for your new `scheduled_query_count` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ScheduledQueryCountSeries
            A new `ScheduledQueryCountSeries` instance that inherits from the `Series` class.
        """
        return ScheduledQueryCountSeries(
            name=name,
            metric="SCHEDULED_QUERY_COUNT",
        )

    @classmethod
    def scheduled_query_success_ratio_metric(cls, name: Optional[str] = None) -> "ScheduledQuerySuccessRatioSeries":
        """Creates a `Series` of metric kind `ScheduledQuerySuccessRatio`.

        Parameters
        ----------
        name
            A name for your new `scheduled_query_success_ratio` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        ScheduledQuerySuccessRatioSeries
            A new `ScheduledQuerySuccessRatioSeries` instance that inherits from the `Series` class.
        """
        return ScheduledQuerySuccessRatioSeries(
            name=name,
            metric="SCHEDULED_QUERY_SUCCESS_RATIO",
        )

    @classmethod
    def topic_messages_processed_metric(cls, name: Optional[str] = None) -> "TopicMessagesProcessedSeries":
        """Creates a `Series` of metric kind `TopicMessagesProcessed`.

        Parameters
        ----------
        name
            A name for your new `topic_messages_processed` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        TopicMessagesProcessedSeries
            A new `TopicMessagesProcessedSeries` instance that inherits from the `Series` class.
        """
        return TopicMessagesProcessedSeries(
            name=name,
            metric="TOPIC_MESSAGES_PROCESSED",
        )

    @classmethod
    def topic_offset_lag_metric(cls, name: Optional[str] = None) -> "TopicOffsetLagSeries":
        """Creates a `Series` of metric kind `TopicOffsetLag`.

        Parameters
        ----------
        name
            A name for your new `topic_offset_lag` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        TopicOffsetLagSeries
            A new `TopicOffsetLagSeries` instance that inherits from the `Series` class.
        """
        return TopicOffsetLagSeries(
            name=name,
            metric="TOPIC_OFFSET_LAG",
        )

    @classmethod
    def subscription_oldest_unacked_message_age_metric(
        cls, name: Optional[str] = None
    ) -> "SubscriptionOldestUnackedMessageAgeSeries":
        """Creates a `Series` of metric kind `SubscriptionOldestUnackedMessageAge`.

        Parameters
        ----------
        name
            A name for your new `subscription_oldest_unacked_message_age` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        SubscriptionOldestUnackedMessageAgeSeries
            A new `SubscriptionOldestUnackedMessageAgeSeries` instance that inherits from the `Series` class.
        """
        return SubscriptionOldestUnackedMessageAgeSeries(
            name=name,
            metric="SUBSCRIPTION_OLDEST_UNACKED_MESSAGE_AGE",
        )

    @classmethod
    def subscription_num_unacked_messages_metric(
        cls, name: Optional[str] = None
    ) -> "SubscriptionNumUnackedMessagesSeries":
        """Creates a `Series` of metric kind `SubscriptionNumUnackedMessages`.

        Parameters
        ----------
        name
            A name for your new `subscription_num_unacked_messages` `Series`.
            If no name is provided, one will be created.

        Returns
        -------
        SubscriptionNumUnackedMessagesSeries
            A new `SubscriptionNumUnackedMessagesSeries` instance that inherits from the `Series` class.
        """
        return SubscriptionNumUnackedMessagesSeries(
            name=name,
            metric="SUBSCRIPTION_NUM_UNACKED_MESSAGES",
        )


class FeatureRequestCountSeries(SeriesBase):
    """
    Series class for metric `feature_request_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureRequestCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureRequestCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureRequestCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureRequestCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureRequestCountSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_is_null(self) -> "FeatureRequestCountSeries":
        """Attaches a `is_null` group-by to your Series instance.

        Returns
        -------
        FeatureRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.IS_NULL)
        return copy

    def group_by_feature(self) -> "FeatureRequestCountSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureComputedCountSeries(SeriesBase):
    """
    Series class for metric `feature_computed_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureComputedCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureComputedCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureComputedCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureComputedCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureComputedCountSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureComputedCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_is_null(self) -> "FeatureComputedCountSeries":
        """Attaches a `is_null` group-by to your Series instance.

        Returns
        -------
        FeatureComputedCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.IS_NULL)
        return copy

    def group_by_feature(self) -> "FeatureComputedCountSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureComputedCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureLookedUpCountSeries(SeriesBase):
    """
    Series class for metric `feature_looked_up_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureLookedUpCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureLookedUpCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureLookedUpCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureLookedUpCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureLookedUpCountSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureLookedUpCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_is_null(self) -> "FeatureLookedUpCountSeries":
        """Attaches a `is_null` group-by to your Series instance.

        Returns
        -------
        FeatureLookedUpCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.IS_NULL)
        return copy

    def group_by_feature(self) -> "FeatureLookedUpCountSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureLookedUpCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureIntermediateCountSeries(SeriesBase):
    """
    Series class for metric `feature_intermediate_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureIntermediateCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureIntermediateCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureIntermediateCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        is_null:
            Filters for null values.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureIntermediateCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureIntermediateCountSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureIntermediateCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_is_null(self) -> "FeatureIntermediateCountSeries":
        """Attaches a `is_null` group-by to your Series instance.

        Returns
        -------
        FeatureIntermediateCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.IS_NULL)
        return copy

    def group_by_feature(self) -> "FeatureIntermediateCountSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureIntermediateCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureStalenessSeries(SeriesBase):
    """
    Series class for metric `feature_staleness`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
    ) -> "FeatureStalenessSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.

        Returns
        -------
        FeatureStalenessSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
    ) -> "FeatureStalenessSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.

        Returns
        -------
        FeatureStalenessSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureStalenessSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureStalenessSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_feature(self) -> "FeatureStalenessSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureStalenessSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy

    def group_by_cache_hit(self) -> "FeatureStalenessSeries":
        """Attaches a `cache_hit` group-by to your Series instance.

        Returns
        -------
        FeatureStalenessSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy


class FeatureValueSeries(SeriesBase):
    """
    Series class for metric `feature_value`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
    ) -> "FeatureValueSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.

        Returns
        -------
        FeatureValueSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            feature_tag=feature_tag,
            feature=feature,
            equals=True,
        )

    def where_not(
        self,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
    ) -> "FeatureValueSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.

        Returns
        -------
        FeatureValueSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            feature_tag=feature_tag,
            feature=feature,
            equals=False,
        )

    def group_by_feature(self) -> "FeatureValueSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureValueSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureNullRatioSeries(SeriesBase):
    """
    Series class for metric `feature_null_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureNullRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureNullRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureNullRatioSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_feature(self) -> "FeatureNullRatioSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureComputedNullRatioSeries(SeriesBase):
    """
    Series class for metric `feature_computed_null_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureComputedNullRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureComputedNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureComputedNullRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureComputedNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureComputedNullRatioSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureComputedNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_feature(self) -> "FeatureComputedNullRatioSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureComputedNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureLookedUpNullRatioSeries(SeriesBase):
    """
    Series class for metric `feature_looked_up_null_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureLookedUpNullRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureLookedUpNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureLookedUpNullRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureLookedUpNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureLookedUpNullRatioSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureLookedUpNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_feature(self) -> "FeatureLookedUpNullRatioSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureLookedUpNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class FeatureIntermediateNullRatioSeries(SeriesBase):
    """
    Series class for metric `feature_intermediate_null_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureIntermediateNullRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureIntermediateNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FeatureIntermediateNullRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        feature_tag:
            Filters for features matching the given tag(s).
        feature:
            Filters for values pertaining to the given feature.
        feature_status:
            Filters for successes/failures of features.

        Returns
        -------
        FeatureIntermediateNullRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "FeatureIntermediateNullRatioSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        FeatureIntermediateNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_feature(self) -> "FeatureIntermediateNullRatioSeries":
        """Attaches a `feature` group-by to your Series instance.

        Returns
        -------
        FeatureIntermediateNullRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class ResolverRequestCountSeries(SeriesBase):
    """
    Series class for metric `resolver_request_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ResolverRequestCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ResolverRequestCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "ResolverRequestCountSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "ResolverRequestCountSeries":
        """Attaches a `cache_hit` group-by to your Series instance.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_resolver(self) -> "ResolverRequestCountSeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def group_by_resolver_status(self) -> "ResolverRequestCountSeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_deployment_id(self) -> "ResolverRequestCountSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ResolverRequestCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy


class ResolverLatencySeries(SeriesBase):
    """
    Series class for metric `resolver_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ResolverLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ResolverLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "ResolverLatencySeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "ResolverLatencySeries":
        """Attaches a `cache_hit` group-by to your Series instance.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_resolver(self) -> "ResolverLatencySeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def group_by_resolver_status(self) -> "ResolverLatencySeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_deployment_id(self) -> "ResolverLatencySeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ResolverLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy


class ResolverSuccessRatioSeries(SeriesBase):
    """
    Series class for metric `resolver_success_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ResolverSuccessRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        ResolverSuccessRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ResolverSuccessRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        ResolverSuccessRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "ResolverSuccessRatioSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        ResolverSuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "ResolverSuccessRatioSeries":
        """Attaches a `cache_hit` group-by to your Series instance.

        Returns
        -------
        ResolverSuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_resolver(self) -> "ResolverSuccessRatioSeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        ResolverSuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def group_by_deployment_id(self) -> "ResolverSuccessRatioSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ResolverSuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy


class QueryCountSeries(SeriesBase):
    """
    Series class for metric `query_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        computation_context: [Union[List[str], str]] = None,
    ) -> "QueryCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        query_name:
            Filters for queries matching the given name(s).
        query_status:
            Filters for successes/failures of queries.
        computation_context:
            Filters for the computation context of the query.

        Returns
        -------
        QueryCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            computation_context=computation_context,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        computation_context: [Union[List[str], str]] = None,
    ) -> "QueryCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        query_name:
            Filters for queries matching the given name(s).
        query_status:
            Filters for successes/failures of queries.
        computation_context:
            Filters for the computation context of the query.

        Returns
        -------
        QueryCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            computation_context=computation_context,
            equals=False,
        )

    def group_by_query_status(self) -> "QueryCountSeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        QueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_query_name(self) -> "QueryCountSeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        QueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy

    def group_by_deployment_id(self) -> "QueryCountSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        QueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resource_group(self) -> "QueryCountSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        QueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy


class QueryLatencySeries(SeriesBase):
    """
    Series class for metric `query_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        computation_context: [Union[List[str], str]] = None,
    ) -> "QueryLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        query_name:
            Filters for queries matching the given name(s).
        query_status:
            Filters for successes/failures of queries.
        computation_context:
            Filters for the computation context of the query.

        Returns
        -------
        QueryLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            computation_context=computation_context,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        computation_context: [Union[List[str], str]] = None,
    ) -> "QueryLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        query_name:
            Filters for queries matching the given name(s).
        query_status:
            Filters for successes/failures of queries.
        computation_context:
            Filters for the computation context of the query.

        Returns
        -------
        QueryLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            computation_context=computation_context,
            equals=False,
        )

    def group_by_query_status(self) -> "QueryLatencySeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        QueryLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_query_name(self) -> "QueryLatencySeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        QueryLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy

    def group_by_deployment_id(self) -> "QueryLatencySeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        QueryLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resource_group(self) -> "QueryLatencySeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        QueryLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy


class QuerySuccessRatioSeries(SeriesBase):
    """
    Series class for metric `query_success_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        computation_context: [Union[List[str], str]] = None,
    ) -> "QuerySuccessRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        query_name:
            Filters for queries matching the given name(s).
        computation_context:
            Filters for the computation context of the query.

        Returns
        -------
        QuerySuccessRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            computation_context=computation_context,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        computation_context: [Union[List[str], str]] = None,
    ) -> "QuerySuccessRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        query_name:
            Filters for queries matching the given name(s).
        computation_context:
            Filters for the computation context of the query.

        Returns
        -------
        QuerySuccessRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            computation_context=computation_context,
            equals=False,
        )

    def group_by_query_name(self) -> "QuerySuccessRatioSeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        QuerySuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy

    def group_by_deployment_id(self) -> "QuerySuccessRatioSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        QuerySuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resource_group(self) -> "QuerySuccessRatioSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        QuerySuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy


class CronCountSeries(SeriesBase):
    """
    Series class for metric `cron_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "CronCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        CronCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "CronCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        CronCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )


class CronLatencySeries(SeriesBase):
    """
    Series class for metric `cron_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "CronLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        CronLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "CronLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        CronLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "CronLatencySeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        CronLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "CronLatencySeries":
        """Attaches a `cache_hit` group-by to your Series instance.

        Returns
        -------
        CronLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy


class CpuUtilizationPercentSeries(SeriesBase):
    """
    Series class for metric `cpu_utilization_percent`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "CpuUtilizationPercentSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        CpuUtilizationPercentSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
    ) -> "CpuUtilizationPercentSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        CpuUtilizationPercentSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=False,
        )

    def group_by_resource_group(self) -> "CpuUtilizationPercentSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        CpuUtilizationPercentSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_service_kind(self) -> "CpuUtilizationPercentSeries":
        """Attaches a `service_kind` group-by to your Series instance.

        Returns
        -------
        CpuUtilizationPercentSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SERVICE_KIND)
        return copy


class MemoryUsageBytesSeries(SeriesBase):
    """
    Series class for metric `memory_usage_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "MemoryUsageBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        MemoryUsageBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
    ) -> "MemoryUsageBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        MemoryUsageBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=False,
        )

    def group_by_resource_group(self) -> "MemoryUsageBytesSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        MemoryUsageBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_service_kind(self) -> "MemoryUsageBytesSeries":
        """Attaches a `service_kind` group-by to your Series instance.

        Returns
        -------
        MemoryUsageBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SERVICE_KIND)
        return copy


class TotalMemoryAvailableBytesSeries(SeriesBase):
    """
    Series class for metric `total_memory_available_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "TotalMemoryAvailableBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        TotalMemoryAvailableBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
    ) -> "TotalMemoryAvailableBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        TotalMemoryAvailableBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=False,
        )

    def group_by_resource_group(self) -> "TotalMemoryAvailableBytesSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        TotalMemoryAvailableBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_service_kind(self) -> "TotalMemoryAvailableBytesSeries":
        """Attaches a `service_kind` group-by to your Series instance.

        Returns
        -------
        TotalMemoryAvailableBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SERVICE_KIND)
        return copy


class NetworkReadBytesSeries(SeriesBase):
    """
    Series class for metric `network_read_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "NetworkReadBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        NetworkReadBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "NetworkReadBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        NetworkReadBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class NetworkWriteBytesSeries(SeriesBase):
    """
    Series class for metric `network_write_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "NetworkWriteBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        NetworkWriteBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "NetworkWriteBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        NetworkWriteBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class DiskReadBytesSeries(SeriesBase):
    """
    Series class for metric `disk_read_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "DiskReadBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskReadBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "DiskReadBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskReadBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class DiskWriteBytesSeries(SeriesBase):
    """
    Series class for metric `disk_write_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "DiskWriteBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskWriteBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "DiskWriteBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskWriteBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class StreamMessageLatencySeries(SeriesBase):
    """
    Series class for metric `stream_message_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamMessageLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamMessageLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamMessageLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamMessageLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "StreamMessageLatencySeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        StreamMessageLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_resolver(self) -> "StreamMessageLatencySeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        StreamMessageLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class StreamMessagesProcessedSeries(SeriesBase):
    """
    Series class for metric `stream_messages_processed`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamMessagesProcessedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamMessagesProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamMessagesProcessedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamMessagesProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "StreamMessagesProcessedSeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        StreamMessagesProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_resolver(self) -> "StreamMessagesProcessedSeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        StreamMessagesProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class StreamWindowsProcessedSeries(SeriesBase):
    """
    Series class for metric `stream_windows_processed`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamWindowsProcessedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamWindowsProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamWindowsProcessedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamWindowsProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "StreamWindowsProcessedSeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        StreamWindowsProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_resolver(self) -> "StreamWindowsProcessedSeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        StreamWindowsProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class StreamWindowLatencySeries(SeriesBase):
    """
    Series class for metric `stream_window_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamWindowLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamWindowLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamWindowLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamWindowLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "StreamWindowLatencySeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        StreamWindowLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_resolver(self) -> "StreamWindowLatencySeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        StreamWindowLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class StreamLagSeries(SeriesBase):
    """
    Series class for metric `stream_lag`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamLagSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamLagSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamLagSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamLagSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "StreamLagSeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        StreamLagSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_resolver(self) -> "StreamLagSeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        StreamLagSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class StreamIngestDelaySeries(SeriesBase):
    """
    Series class for metric `stream_ingest_delay`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamIngestDelaySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamIngestDelaySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "StreamIngestDelaySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_tag:
            Filters for resolvers matching the given tag(s).
        resolver:
            Filters for values pertaining to the given resolver.
        resolver_status:
            Filters for successes/failures of resolvers.

        Returns
        -------
        StreamIngestDelaySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "StreamIngestDelaySeries":
        """Attaches a `resolver_status` group-by to your Series instance.

        Returns
        -------
        StreamIngestDelaySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def group_by_resolver(self) -> "StreamIngestDelaySeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        StreamIngestDelaySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class OnlineStoreUsedMemorySeries(SeriesBase):
    """
    Series class for metric `online_store_used_memory`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "OnlineStoreUsedMemorySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreUsedMemorySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "OnlineStoreUsedMemorySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreUsedMemorySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class OnlineStoreKeyCountSeries(SeriesBase):
    """
    Series class for metric `online_store_key_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "OnlineStoreKeyCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreKeyCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "OnlineStoreKeyCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreKeyCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class OnlineStoreExpiredKeyCountSeries(SeriesBase):
    """
    Series class for metric `online_store_expired_key_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "OnlineStoreExpiredKeyCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreExpiredKeyCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "OnlineStoreExpiredKeyCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreExpiredKeyCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class OnlineStoreRequestsPerSecondSeries(SeriesBase):
    """
    Series class for metric `online_store_requests_per_second`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "OnlineStoreRequestsPerSecondSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreRequestsPerSecondSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "OnlineStoreRequestsPerSecondSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreRequestsPerSecondSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class OnlineStoreTotalMemorySeries(SeriesBase):
    """
    Series class for metric `online_store_total_memory`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "OnlineStoreTotalMemorySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreTotalMemorySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "OnlineStoreTotalMemorySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        OnlineStoreTotalMemorySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class ContainerMemoryBytesSeries(SeriesBase):
    """
    Series class for metric `container_memory_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "ContainerMemoryBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ContainerMemoryBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
    ) -> "ContainerMemoryBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ContainerMemoryBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=False,
        )

    def group_by_resource_group(self) -> "ContainerMemoryBytesSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        ContainerMemoryBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_service_kind(self) -> "ContainerMemoryBytesSeries":
        """Attaches a `service_kind` group-by to your Series instance.

        Returns
        -------
        ContainerMemoryBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SERVICE_KIND)
        return copy


class HostMemoryBytesSeries(SeriesBase):
    """
    Series class for metric `host_memory_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "HostMemoryBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        HostMemoryBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
    ) -> "HostMemoryBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        HostMemoryBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=False,
        )

    def group_by_resource_group(self) -> "HostMemoryBytesSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        HostMemoryBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_service_kind(self) -> "HostMemoryBytesSeries":
        """Attaches a `service_kind` group-by to your Series instance.

        Returns
        -------
        HostMemoryBytesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SERVICE_KIND)
        return copy


class ContainerCpuUtilizationSeries(SeriesBase):
    """
    Series class for metric `container_cpu_utilization`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "ContainerCpuUtilizationSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ContainerCpuUtilizationSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
    ) -> "ContainerCpuUtilizationSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ContainerCpuUtilizationSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            service_kind=service_kind,
            equals=False,
        )

    def group_by_resource_group(self) -> "ContainerCpuUtilizationSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        ContainerCpuUtilizationSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_service_kind(self) -> "ContainerCpuUtilizationSeries":
        """Attaches a `service_kind` group-by to your Series instance.

        Returns
        -------
        ContainerCpuUtilizationSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SERVICE_KIND)
        return copy


class GpuUtilizationSeries(SeriesBase):
    """
    Series class for metric `gpu_utilization`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuUtilizationSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuUtilizationSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuUtilizationSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuUtilizationSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class GpuTensorActivitySeries(SeriesBase):
    """
    Series class for metric `gpu_tensor_activity`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuTensorActivitySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuTensorActivitySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuTensorActivitySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuTensorActivitySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class GpuSmClockMhzSeries(SeriesBase):
    """
    Series class for metric `gpu_sm_clock_mhz`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuSmClockMhzSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuSmClockMhzSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuSmClockMhzSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuSmClockMhzSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class GpuPowerWattsSeries(SeriesBase):
    """
    Series class for metric `gpu_power_watts`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuPowerWattsSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuPowerWattsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuPowerWattsSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuPowerWattsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class GpuTemperatureCelsiusSeries(SeriesBase):
    """
    Series class for metric `gpu_temperature_celsius`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuTemperatureCelsiusSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuTemperatureCelsiusSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuTemperatureCelsiusSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuTemperatureCelsiusSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class GpuThrottleReasonsSeries(SeriesBase):
    """
    Series class for metric `gpu_throttle_reasons`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuThrottleReasonsSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuThrottleReasonsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuThrottleReasonsSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuThrottleReasonsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class GpuFp16ActivitySeries(SeriesBase):
    """
    Series class for metric `gpu_fp16_activity`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "GpuFp16ActivitySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuFp16ActivitySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "GpuFp16ActivitySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        GpuFp16ActivitySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class DiskUsedBytesSeries(SeriesBase):
    """
    Series class for metric `disk_used_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "DiskUsedBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskUsedBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "DiskUsedBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskUsedBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class DiskAvailableBytesSeries(SeriesBase):
    """
    Series class for metric `disk_available_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "DiskAvailableBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskAvailableBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "DiskAvailableBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        DiskAvailableBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class ResolverInvokerNetRxSeries(SeriesBase):
    """
    Series class for metric `resolver_invoker_net_rx`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "ResolverInvokerNetRxSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ResolverInvokerNetRxSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "ResolverInvokerNetRxSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ResolverInvokerNetRxSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )

    def group_by_deployment_id(self) -> "ResolverInvokerNetRxSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerNetRxSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resolver_type(self) -> "ResolverInvokerNetRxSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerNetRxSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_query_name(self) -> "ResolverInvokerNetRxSeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerNetRxSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class ResolverInvokerNetTxSeries(SeriesBase):
    """
    Series class for metric `resolver_invoker_net_tx`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "ResolverInvokerNetTxSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ResolverInvokerNetTxSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "ResolverInvokerNetTxSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ResolverInvokerNetTxSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )

    def group_by_deployment_id(self) -> "ResolverInvokerNetTxSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerNetTxSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resolver_type(self) -> "ResolverInvokerNetTxSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerNetTxSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_query_name(self) -> "ResolverInvokerNetTxSeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerNetTxSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class ResolverInvokerRowsWrittenSeries(SeriesBase):
    """
    Series class for metric `resolver_invoker_rows_written`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
    ) -> "ResolverInvokerRowsWrittenSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver:
            Filters for values pertaining to the given resolver.

        Returns
        -------
        ResolverInvokerRowsWrittenSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver=resolver,
            equals=True,
        )

    def where_not(
        self,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
    ) -> "ResolverInvokerRowsWrittenSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver:
            Filters for values pertaining to the given resolver.

        Returns
        -------
        ResolverInvokerRowsWrittenSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver=resolver,
            equals=False,
        )

    def group_by_deployment_id(self) -> "ResolverInvokerRowsWrittenSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerRowsWrittenSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resolver_type(self) -> "ResolverInvokerRowsWrittenSeries":
        """Attaches a `resolver_type` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerRowsWrittenSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_resolver(self) -> "ResolverInvokerRowsWrittenSeries":
        """Attaches a `resolver` group-by to your Series instance.

        Returns
        -------
        ResolverInvokerRowsWrittenSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy


class ReplicaCountSeries(SeriesBase):
    """
    Series class for metric `replica_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
    ) -> "ReplicaCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.

        Returns
        -------
        ReplicaCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            service_kind=service_kind,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
    ) -> "ReplicaCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        resolver_type:
            Filters for resolvers by type 'online', 'offline' or 'stream'.

        Returns
        -------
        ReplicaCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            resolver_type=resolver_type,
            service_kind=service_kind,
            equals=False,
        )

    def group_by_deployment_id(self) -> "ReplicaCountSeries":
        """Attaches a `deployment_id` group-by to your Series instance.

        Returns
        -------
        ReplicaCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.DEPLOYMENT_ID)
        return copy

    def group_by_resource_group(self) -> "ReplicaCountSeries":
        """Attaches a `resource_group` group-by to your Series instance.

        Returns
        -------
        ReplicaCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOURCE_GROUP)
        return copy

    def group_by_operation_id(self) -> "ReplicaCountSeries":
        """Attaches a `operation_id` group-by to your Series instance.

        Returns
        -------
        ReplicaCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.OPERATION_ID)
        return copy


class PullQueryQueueDepthSeries(SeriesBase):
    """
    Series class for metric `pull_query_queue_depth`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "PullQueryQueueDepthSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryQueueDepthSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "PullQueryQueueDepthSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryQueueDepthSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class PullQueryOldestUnackedAgeSeries(SeriesBase):
    """
    Series class for metric `pull_query_oldest_unacked_age`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "PullQueryOldestUnackedAgeSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryOldestUnackedAgeSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "PullQueryOldestUnackedAgeSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryOldestUnackedAgeSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class PullQueryProcessedSeries(SeriesBase):
    """
    Series class for metric `pull_query_processed`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "PullQueryProcessedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        PullQueryProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "PullQueryProcessedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        PullQueryProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            query_status=query_status,
            equals=False,
        )

    def group_by_query_status(self) -> "PullQueryProcessedSeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        PullQueryProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy


class PullQueryLatencySeries(SeriesBase):
    """
    Series class for metric `pull_query_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "PullQueryLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        PullQueryLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "PullQueryLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        PullQueryLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            query_status=query_status,
            equals=False,
        )

    def group_by_query_status(self) -> "PullQueryLatencySeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        PullQueryLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy


class PullQueryMaxInflightSeries(SeriesBase):
    """
    Series class for metric `pull_query_max_inflight`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "PullQueryMaxInflightSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryMaxInflightSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "PullQueryMaxInflightSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryMaxInflightSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class PullQueryConcurrencyTargetSeries(SeriesBase):
    """
    Series class for metric `pull_query_concurrency_target`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "PullQueryConcurrencyTargetSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryConcurrencyTargetSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "PullQueryConcurrencyTargetSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryConcurrencyTargetSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class PullQueryOpenConnectionsSeries(SeriesBase):
    """
    Series class for metric `pull_query_open_connections`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "PullQueryOpenConnectionsSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryOpenConnectionsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "PullQueryOpenConnectionsSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        PullQueryOpenConnectionsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class FunctionCallEnqueuedSeries(SeriesBase):
    """
    Series class for metric `function_call_enqueued`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FunctionCallEnqueuedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallEnqueuedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FunctionCallEnqueuedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallEnqueuedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallEnqueuedSeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallEnqueuedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy

    def group_by_query_status(self) -> "FunctionCallEnqueuedSeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        FunctionCallEnqueuedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy


class FunctionCallEnqueueLatencySeries(SeriesBase):
    """
    Series class for metric `function_call_enqueue_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FunctionCallEnqueueLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallEnqueueLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "FunctionCallEnqueueLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallEnqueueLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallEnqueueLatencySeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallEnqueueLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy

    def group_by_query_status(self) -> "FunctionCallEnqueueLatencySeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        FunctionCallEnqueueLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy


class FunctionCallOpenConnectionsSeries(SeriesBase):
    """
    Series class for metric `function_call_open_connections`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "FunctionCallOpenConnectionsSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        FunctionCallOpenConnectionsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            equals=True,
        )

    def where_not(
        self,
    ) -> "FunctionCallOpenConnectionsSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        FunctionCallOpenConnectionsSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallOpenConnectionsSeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallOpenConnectionsSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy


class FunctionCallDequeuedSeries(SeriesBase):
    """
    Series class for metric `function_call_dequeued`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
    ) -> "FunctionCallDequeuedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallDequeuedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            operation_id=operation_id,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
    ) -> "FunctionCallDequeuedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallDequeuedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            operation_id=operation_id,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallDequeuedSeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallDequeuedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy

    def group_by_query_status(self) -> "FunctionCallDequeuedSeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        FunctionCallDequeuedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_operation_id(self) -> "FunctionCallDequeuedSeries":
        """Attaches a `operation_id` group-by to your Series instance.

        Returns
        -------
        FunctionCallDequeuedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.OPERATION_ID)
        return copy


class FunctionCallProcessingLatencySeries(SeriesBase):
    """
    Series class for metric `function_call_processing_latency`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
    ) -> "FunctionCallProcessingLatencySeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallProcessingLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            operation_id=operation_id,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
    ) -> "FunctionCallProcessingLatencySeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        FunctionCallProcessingLatencySeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            query_status=query_status,
            operation_id=operation_id,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallProcessingLatencySeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallProcessingLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy

    def group_by_query_status(self) -> "FunctionCallProcessingLatencySeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        FunctionCallProcessingLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_operation_id(self) -> "FunctionCallProcessingLatencySeries":
        """Attaches a `operation_id` group-by to your Series instance.

        Returns
        -------
        FunctionCallProcessingLatencySeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.OPERATION_ID)
        return copy


class FunctionCallQueueDepthSeries(SeriesBase):
    """
    Series class for metric `function_call_queue_depth`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "FunctionCallQueueDepthSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        FunctionCallQueueDepthSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            equals=True,
        )

    def where_not(
        self,
    ) -> "FunctionCallQueueDepthSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        FunctionCallQueueDepthSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallQueueDepthSeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallQueueDepthSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy


class FunctionCallInflightSeries(SeriesBase):
    """
    Series class for metric `function_call_inflight`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        operation_id: Optional[Union[List[str], str]] = None,
    ) -> "FunctionCallInflightSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        FunctionCallInflightSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            operation_id=operation_id,
            equals=True,
        )

    def where_not(
        self,
        operation_id: Optional[Union[List[str], str]] = None,
    ) -> "FunctionCallInflightSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        FunctionCallInflightSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            function_name=function_name,
            operation_id=operation_id,
            equals=False,
        )

    def group_by_function_name(self) -> "FunctionCallInflightSeries":
        """Attaches a `function_name` group-by to your Series instance.

        Returns
        -------
        FunctionCallInflightSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FUNCTION_NAME)
        return copy

    def group_by_operation_id(self) -> "FunctionCallInflightSeries":
        """Attaches a `operation_id` group-by to your Series instance.

        Returns
        -------
        FunctionCallInflightSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.OPERATION_ID)
        return copy


class QueryProgressSplitsProcessedSeries(SeriesBase):
    """
    Series class for metric `query_progress_splits_processed`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "QueryProgressSplitsProcessedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressSplitsProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "QueryProgressSplitsProcessedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressSplitsProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class QueryProgressSplitsQueuedSeries(SeriesBase):
    """
    Series class for metric `query_progress_splits_queued`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "QueryProgressSplitsQueuedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressSplitsQueuedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "QueryProgressSplitsQueuedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressSplitsQueuedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class QueryProgressBlockedDriversSeries(SeriesBase):
    """
    Series class for metric `query_progress_blocked_drivers`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "QueryProgressBlockedDriversSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressBlockedDriversSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "QueryProgressBlockedDriversSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressBlockedDriversSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class QueryProgressResolverRowsReturnedSeries(SeriesBase):
    """
    Series class for metric `query_progress_resolver_rows_returned`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "QueryProgressResolverRowsReturnedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressResolverRowsReturnedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "QueryProgressResolverRowsReturnedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressResolverRowsReturnedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class QueryProgressOperatorOutputBytesSeries(SeriesBase):
    """
    Series class for metric `query_progress_operator_output_bytes`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "QueryProgressOperatorOutputBytesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressOperatorOutputBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "QueryProgressOperatorOutputBytesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressOperatorOutputBytesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class QueryProgressOperatorRowsProcessedSeries(SeriesBase):
    """
    Series class for metric `query_progress_operator_rows_processed`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "QueryProgressOperatorRowsProcessedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressOperatorRowsProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "QueryProgressOperatorRowsProcessedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        QueryProgressOperatorRowsProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )


class ScheduledQueryCountSeries(SeriesBase):
    """
    Series class for metric `scheduled_query_count`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ScheduledQueryCountSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        ScheduledQueryCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "ScheduledQueryCountSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        query_status:
            Filters for successes/failures of queries.

        Returns
        -------
        ScheduledQueryCountSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            query_status=query_status,
            equals=False,
        )

    def group_by_operation_id(self) -> "ScheduledQueryCountSeries":
        """Attaches a `operation_id` group-by to your Series instance.

        Returns
        -------
        ScheduledQueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.OPERATION_ID)
        return copy

    def group_by_query_status(self) -> "ScheduledQueryCountSeries":
        """Attaches a `query_status` group-by to your Series instance.

        Returns
        -------
        ScheduledQueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_query_name(self) -> "ScheduledQueryCountSeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        ScheduledQueryCountSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class ScheduledQuerySuccessRatioSeries(SeriesBase):
    """
    Series class for metric `scheduled_query_success_ratio`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
    ) -> "ScheduledQuerySuccessRatioSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ScheduledQuerySuccessRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=True,
        )

    def where_not(
        self,
    ) -> "ScheduledQuerySuccessRatioSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------

        Returns
        -------
        ScheduledQuerySuccessRatioSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            equals=False,
        )

    def group_by_operation_id(self) -> "ScheduledQuerySuccessRatioSeries":
        """Attaches a `operation_id` group-by to your Series instance.

        Returns
        -------
        ScheduledQuerySuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.OPERATION_ID)
        return copy

    def group_by_query_name(self) -> "ScheduledQuerySuccessRatioSeries":
        """Attaches a `query_name` group-by to your Series instance.

        Returns
        -------
        ScheduledQuerySuccessRatioSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class TopicMessagesProcessedSeries(SeriesBase):
    """
    Series class for metric `topic_messages_processed`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        topic_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "TopicMessagesProcessedSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        topic_name:
            Filters for SQS topics.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        TopicMessagesProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            topic_name=topic_name,
            partition_name=partition_name,
            equals=True,
        )

    def where_not(
        self,
        topic_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "TopicMessagesProcessedSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        topic_name:
            Filters for SQS topics.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        TopicMessagesProcessedSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            topic_name=topic_name,
            partition_name=partition_name,
            equals=False,
        )

    def group_by_topic_name(self) -> "TopicMessagesProcessedSeries":
        """Attaches a `topic_name` group-by to your Series instance.

        Returns
        -------
        TopicMessagesProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.TOPIC_NAME)
        return copy

    def group_by_partition_name(self) -> "TopicMessagesProcessedSeries":
        """Attaches a `partition_name` group-by to your Series instance.

        Returns
        -------
        TopicMessagesProcessedSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.PARTITION_NAME)
        return copy


class TopicOffsetLagSeries(SeriesBase):
    """
    Series class for metric `topic_offset_lag`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        topic_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "TopicOffsetLagSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        topic_name:
            Filters for SQS topics.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        TopicOffsetLagSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            topic_name=topic_name,
            partition_name=partition_name,
            consumer_group=consumer_group,
            equals=True,
        )

    def where_not(
        self,
        topic_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "TopicOffsetLagSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        topic_name:
            Filters for SQS topics.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        TopicOffsetLagSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            topic_name=topic_name,
            partition_name=partition_name,
            consumer_group=consumer_group,
            equals=False,
        )

    def group_by_topic_name(self) -> "TopicOffsetLagSeries":
        """Attaches a `topic_name` group-by to your Series instance.

        Returns
        -------
        TopicOffsetLagSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.TOPIC_NAME)
        return copy

    def group_by_partition_name(self) -> "TopicOffsetLagSeries":
        """Attaches a `partition_name` group-by to your Series instance.

        Returns
        -------
        TopicOffsetLagSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.PARTITION_NAME)
        return copy

    def group_by_consumer_group(self) -> "TopicOffsetLagSeries":
        """Attaches a `consumer_group` group-by to your Series instance.

        Returns
        -------
        TopicOffsetLagSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CONSUMER_GROUP)
        return copy


class SubscriptionOldestUnackedMessageAgeSeries(SeriesBase):
    """
    Series class for metric `subscription_oldest_unacked_message_age`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        subscription_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "SubscriptionOldestUnackedMessageAgeSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        subscription_name:
            Filters for pub/sub subscriptions.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        SubscriptionOldestUnackedMessageAgeSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            subscription_name=subscription_name,
            partition_name=partition_name,
            equals=True,
        )

    def where_not(
        self,
        subscription_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "SubscriptionOldestUnackedMessageAgeSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        subscription_name:
            Filters for pub/sub subscriptions.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        SubscriptionOldestUnackedMessageAgeSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            subscription_name=subscription_name,
            partition_name=partition_name,
            equals=False,
        )

    def group_by_subscription_name(self) -> "SubscriptionOldestUnackedMessageAgeSeries":
        """Attaches a `subscription_name` group-by to your Series instance.

        Returns
        -------
        SubscriptionOldestUnackedMessageAgeSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SUBSCRIPTION_NAME)
        return copy

    def group_by_partition_name(self) -> "SubscriptionOldestUnackedMessageAgeSeries":
        """Attaches a `partition_name` group-by to your Series instance.

        Returns
        -------
        SubscriptionOldestUnackedMessageAgeSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.PARTITION_NAME)
        return copy


class SubscriptionNumUnackedMessagesSeries(SeriesBase):
    """
    Series class for metric `subscription_num_unacked_messages`
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        subscription_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "SubscriptionNumUnackedMessagesSeries":
        """Attaches a filter to your `Series` instance.

        Parameters
        ----------
        subscription_name:
            Filters for pub/sub subscriptions.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        SubscriptionNumUnackedMessagesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            subscription_name=subscription_name,
            partition_name=partition_name,
            equals=True,
        )

    def where_not(
        self,
        subscription_name: [Union[List[str], str]] = None,
        partition_name: [Union[List[str], str]] = None,
    ) -> "SubscriptionNumUnackedMessagesSeries":
        """Attaches a negative filter to your `Series` instance.

        Parameters
        ----------
        subscription_name:
            Filters for pub/sub subscriptions.
        partition_name:
            Filters for pub/sub or topic partitions.

        Returns
        -------
        SubscriptionNumUnackedMessagesSeries
            A copy of your `Series` with the new filter.
        """
        return self._where(
            subscription_name=subscription_name,
            partition_name=partition_name,
            equals=False,
        )

    def group_by_subscription_name(self) -> "SubscriptionNumUnackedMessagesSeries":
        """Attaches a `subscription_name` group-by to your Series instance.

        Returns
        -------
        SubscriptionNumUnackedMessagesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.SUBSCRIPTION_NAME)
        return copy

    def group_by_partition_name(self) -> "SubscriptionNumUnackedMessagesSeries":
        """Attaches a `partition_name` group-by to your Series instance.

        Returns
        -------
        SubscriptionNumUnackedMessagesSeries
            A copy of your `Series` with the new group-by.
        """
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.PARTITION_NAME)
        return copy

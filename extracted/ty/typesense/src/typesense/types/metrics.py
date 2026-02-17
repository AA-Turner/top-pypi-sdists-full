"""
Typed dictionaries for Typesense metrics responses.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing


class MetricsResponseBase(typing.TypedDict):
    """
    Response schema for metrics retrieval.

    This TypedDict includes system metrics like CPU, memory, disk, and network usage,
    as well as Typesense-specific memory metrics.
    """

    system_cpu_active_percentage: str
    system_disk_total_bytes: str
    system_disk_used_bytes: str
    system_memory_total_bytes: str
    system_memory_used_bytes: str
    system_network_received_bytes: str
    system_network_sent_bytes: str
    typesense_memory_active_bytes: str
    typesense_memory_allocated_bytes: str
    typesense_memory_fragmentation_ratio: str
    typesense_memory_mapped_bytes: str
    typesense_memory_metadata_bytes: str
    typesense_memory_resident_bytes: str
    typesense_memory_retained_bytes: str


class MetricsResponse(MetricsResponseBase):
    """Extended MetricsResponse with optional per-CPU core metrics."""

    system_memory_total_swap_bytes: str
    system_memory_used_swap_bytes: str
    system_cpu1_active_percentage: typing.Optional[str]
    system_cpu2_active_percentage: typing.Optional[str]
    system_cpu3_active_percentage: typing.Optional[str]
    system_cpu4_active_percentage: typing.Optional[str]
    system_cpu5_active_percentage: typing.Optional[str]
    system_cpu6_active_percentage: typing.Optional[str]
    system_cpu7_active_percentage: typing.Optional[str]
    system_cpu8_active_percentage: typing.Optional[str]
    system_cpu9_active_percentage: typing.Optional[str]
    system_cpu10_active_percentage: typing.Optional[str]
    system_cpu11_active_percentage: typing.Optional[str]
    system_cpu12_active_percentage: typing.Optional[str]
    system_cpu13_active_percentage: typing.Optional[str]
    system_cpu14_active_percentage: typing.Optional[str]
    system_cpu15_active_percentage: typing.Optional[str]
    system_cpu16_active_percentage: typing.Optional[str]
    system_cpu17_active_percentage: typing.Optional[str]
    system_cpu18_active_percentage: typing.Optional[str]
    system_cpu19_active_percentage: typing.Optional[str]
    system_cpu20_active_percentage: typing.Optional[str]
    system_cpu21_active_percentage: typing.Optional[str]
    system_cpu22_active_percentage: typing.Optional[str]
    system_cpu23_active_percentage: typing.Optional[str]
    system_cpu24_active_percentage: typing.Optional[str]

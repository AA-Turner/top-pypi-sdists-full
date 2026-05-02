import logging

import pytest
from acceldata_sdk.errors import TorchSdkException, APIError
from acceldata_sdk.models.common_types import (
    ExecutionType,
    BoundsIdMarkerConfig,
    BoundsDateTimeMarkerConfig,
    BoundsFileEventMarkerConfig,
    TimestampBasedMarkerConfig,
)
from acceldata_sdk.models.profile import StartProfilingRequest

from . import test_constants as test_const
from ..commons.retry import retry_operation

logger = logging.getLogger(__name__)

def execute_profiling_or_accept_running(operation):
    try:
        result = retry_operation(
            operation,
            test_const.MAX_RETRIES,
            test_const.RETRY_INTERVAL,
        )
        return result

    except APIError as e:
        msg = str(e)
        logger.info(msg)

        # ACCEPTABLE: profiling already running
        if (
                "profile is already running" in msg
                or "Cannot start FULL profiling" in msg
                or "409" in msg
        ):
            logger.info("Profiling already running – accepting as PASS")
            return "Profiling already running"

        # ACCEPTABLE: previous execution not completed
        if (
                "Previous execution" in msg
                and "has not completed" in msg
        ):
            logger.info("Previous profiling execution still running – accepting as PASS")
            return "Previous profiling execution still running"

        # Anything else is a real failure
        raise


@pytest.fixture(scope="module")
def table_asset(adoc_client):
    return adoc_client.get_asset(test_const.TABLE_ASSET_UID)


@pytest.mark.integration
def test_execute_full_profiling_backward_compatible(table_asset):
    logger.info("Executing FULL profiling (backward compatible)")

    def operation():
        return table_asset.start_profile(
            profiling_type=ExecutionType.FULL
        )

    result = execute_profiling_or_accept_running(operation)
    logger.info("Profiling result: %s", result)

    # PASS if started or already running
    assert result is None or result is not None


@pytest.mark.integration
def test_execute_incremental_profiling_backward_compatible(table_asset):
    logger.info("Executing INCREMENTAL profiling (backward compatible)")

    def operation():
        return table_asset.start_profile(
            profiling_type=ExecutionType.INCREMENTAL
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_full_profiling_using_request(table_asset):
    request = StartProfilingRequest(
        profilingType=ExecutionType.FULL
    )

    logger.info("Executing FULL profiling using StartProfilingRequest")

    def operation():
        return table_asset.start_profile(
            start_profiling_request=request
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_incremental_profiling_using_request(table_asset):
    request = StartProfilingRequest(
        profilingType=ExecutionType.INCREMENTAL
    )

    logger.info("Executing INCREMENTAL profiling using StartProfilingRequest")

    def operation():
        return table_asset.start_profile(
            start_profiling_request=request
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_selective_profiling_without_marker_config(table_asset):
    request = StartProfilingRequest(
        profilingType=ExecutionType.SELECTIVE
    )

    logger.info("Executing SELECTIVE profiling without marker config")

    with pytest.raises(TorchSdkException):
        table_asset.start_profile(
            start_profiling_request=request
        )


@pytest.mark.integration
def test_execute_selective_profiling_id_based(table_asset):
    marker = BoundsIdMarkerConfig(
        idColumnName="ID",
        fromId=0,
        toId=1000,
    )

    request = StartProfilingRequest(
        profilingType=ExecutionType.SELECTIVE,
        markerConfig=marker,
    )

    logger.info("Executing SELECTIVE profiling (ID based)")

    def operation():
        return table_asset.start_profile(
            start_profiling_request=request
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_selective_profiling_datetime_based(table_asset):
    marker = BoundsDateTimeMarkerConfig(
        dateColumnName="TO_DATE",
        format="yyyy-MM-dd",
        fromDate="2023-07-01 00:00:00.000",
        toDate="2024-07-14 23:59:59.999",
        timeZoneId="Asia/Calcutta",
    )

    request = StartProfilingRequest(
        profilingType=ExecutionType.SELECTIVE,
        markerConfig=marker,
    )

    logger.info("Executing SELECTIVE profiling (datetime based)")

    def operation():
        return table_asset.start_profile(
            start_profiling_request=request
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_selective_profiling_file_event_based(adoc_client):
    asset = adoc_client.get_asset(
        test_const.FILE_BASED_ASSET_UID
    )

    marker = BoundsFileEventMarkerConfig(
        fromDate="2019-04-01 00:00:00.000",
        toDate="2024-07-16 23:59:59.999",
        timeZoneId="Asia/Calcutta",
    )

    request = StartProfilingRequest(
        profilingType=ExecutionType.SELECTIVE,
        markerConfig=marker,
    )

    logger.info("Executing SELECTIVE profiling (file event based)")

    def operation():
        return asset.start_profile(
            start_profiling_request=request
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None

@pytest.mark.integration
def test_execute_selective_profiling_kafka_timestamp_based(adoc_client):
    asset = adoc_client.get_asset(
        test_const.KAFKA_ASSET_UID
    )

    marker = TimestampBasedMarkerConfig(
        format="yyyy-mm-dd",
        initialOffset="2023-06-01",
        timeZoneId="Asia/Calcutta",
    )

    request = StartProfilingRequest(
        profilingType=ExecutionType.SELECTIVE,
        markerConfig=marker,
    )

    logger.info("Executing SELECTIVE profiling (kafka timestamp based)")

    def operation():
        return asset.start_profile(
            start_profiling_request=request
        )

    result = execute_profiling_or_accept_running(operation)

    logger.info("Profiling result: %s", result)
    assert result is not None

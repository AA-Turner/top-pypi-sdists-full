from unittest.mock import mock_open, patch

from workflow_server.config import MEMORY_LIMIT_MB
from workflow_server.utils.system_utils import (
    FORCE_GC_MEMORY_PERCENT,
    WARN_MEMORY_PERCENT,
    get_memory_in_use_mb,
    wait_for_available_process,
)


def test_get_memory_in_use_mb_success():
    # Test with 1GB of memory (1024MB)
    test_memory_bytes = "1073741824"
    with patch("builtins.open", mock_open(read_data=test_memory_bytes)):
        result = get_memory_in_use_mb()

        assert result == 1024.0


def test_get_memory_in_use_mb_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        result = get_memory_in_use_mb()

        assert result is None


def test_get_memory_in_use_mb_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError()):
        result = get_memory_in_use_mb()

        assert result is None


def test_get_memory_in_use_mb_zero_memory():
    with patch("builtins.open", mock_open(read_data="0")):
        result = get_memory_in_use_mb()
        assert result == 0.0


@patch("workflow_server.utils.system_utils.time.sleep")
@patch("workflow_server.utils.system_utils.get_memory_in_use_mb")
@patch("workflow_server.utils.system_utils.get_active_process_count")
def test_wait_for_available_process_immediate_availability(mock_get_active_process_count, mock_get_memory, mock_sleep):
    # Mock memory usage below warning limit and process limit below
    mock_get_memory.return_value = MEMORY_LIMIT_MB * (WARN_MEMORY_PERCENT - 0.1)
    mock_get_active_process_count.return_value = 10

    result = wait_for_available_process()

    assert result is True

    # Should not sleep if immediately available
    mock_sleep.assert_not_called()


@patch("workflow_server.utils.system_utils.time.sleep")
@patch("workflow_server.utils.system_utils.get_memory_in_use_mb")
@patch("workflow_server.utils.system_utils.get_active_process_count")
def test_wait_for_available_process_becomes_available(mock_get_active_process_count, mock_get_memory, mock_sleep):
    # First two calls indicate high memory usage, third call shows available memory
    mock_get_memory.side_effect = [
        MEMORY_LIMIT_MB * (WARN_MEMORY_PERCENT + 0.1),
        MEMORY_LIMIT_MB * (WARN_MEMORY_PERCENT + 0.1),
        MEMORY_LIMIT_MB * (WARN_MEMORY_PERCENT - 0.1),
    ]
    mock_get_active_process_count.return_value = 10

    result = wait_for_available_process()

    assert result is True
    # Should sleep twice before becoming available
    assert mock_sleep.call_count == 2


@patch("workflow_server.utils.system_utils.time.sleep")
@patch("workflow_server.utils.system_utils.get_memory_in_use_mb")
@patch("workflow_server.utils.system_utils.get_active_process_count")
def test_wait_for_available_process_never_available(mock_get_active_process_count, mock_get_memory, mock_sleep):
    # Return false if process isn't available from high memory usage
    mock_get_memory.return_value = MEMORY_LIMIT_MB * (WARN_MEMORY_PERCENT + 0.1)
    mock_get_active_process_count.return_value = 13

    result = wait_for_available_process()
    assert result is False

    # Should sleep for each attempt
    assert mock_sleep.call_count == 3


@patch("workflow_server.utils.system_utils.time.sleep")
@patch("workflow_server.utils.system_utils.get_memory_in_use_mb")
@patch("workflow_server.utils.system_utils.get_active_process_count")
def test_wait_for_available_process_memory_none(mock_get_active_process_count, mock_get_memory, mock_sleep):
    # Test when memory reading fails that result is still true
    mock_get_memory.return_value = None
    mock_get_active_process_count.return_value = 10

    result = wait_for_available_process()
    assert result is True


@patch("workflow_server.utils.system_utils.time.sleep")
@patch("workflow_server.utils.system_utils.get_memory_in_use_mb")
@patch("workflow_server.utils.system_utils.get_active_process_count")
def test_wait_for_available_process_high_process_count_but_low_memory(
    mock_get_active_process_count, mock_get_memory, mock_sleep
):
    # Test when process count is high but memory is low
    mock_get_memory.return_value = MEMORY_LIMIT_MB * (FORCE_GC_MEMORY_PERCENT - 0.1)
    mock_get_active_process_count.return_value = 13

    result = wait_for_available_process()
    assert result is True

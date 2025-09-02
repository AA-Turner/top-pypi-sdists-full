# pylint: disable = protected-access
"""Test pyobihai."""

import datetime
from typing import Callable
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import RequestException

from pyobihai import PyObihai

from . import MockResponse
from .const import (
    FAILED_REQUEST,
    INBOUND_CALL_HTML,
    LINE_STATE_XML,
    MOCK_LOGIN,
    NO_ACTIVE_CALLS_HTML,
    OUTBOUND_CALL_HTML,
    STATUS_XML,
)

_GET_REQUEST_PATCH = "pyobihai.PyObihai._get_request"

pytestmark = pytest.mark.usefixtures("mock_response")


def test_get_line_state() -> None:
    """Test PyObihai.get_line_state"""

    my_obi = PyObihai(*MOCK_LOGIN)
    with patch(_GET_REQUEST_PATCH, MagicMock(return_value=LINE_STATE_XML)):
        line_state = my_obi.get_line_state()

    assert line_state == {
        "PHONE1 Port": "On Hook",
        "PHONE1 Port last caller info": "15552345678",
    }


@pytest.mark.parametrize(
    "to_call,expected_result",
    [
        pytest.param(PyObihai.get_device_mac, "9CADEF000000", id="get_device_mac"),
        pytest.param(
            PyObihai.get_device_serial, "123456789011", id="get_device_serial"
        ),
        pytest.param(PyObihai.get_model_name, "OBi200", id="get_model_name"),
        pytest.param(PyObihai.get_hardware_version, "1.4", id="get_hardware_version"),
        pytest.param(
            PyObihai.get_software_version,
            "3.2.2 (Build: 8680EX)",
            id="get_software_version",
        ),
    ],
)
def test_get_status(to_call: Callable, expected_result: str) -> None:
    """Test PyObihai device info functions."""

    my_obi = PyObihai(*MOCK_LOGIN)
    with patch(_GET_REQUEST_PATCH, MagicMock(return_value=STATUS_XML)) as mock_request:
        result = to_call(my_obi)

    mock_request.assert_called_once()
    assert result == expected_result

    # Verify we use the cache after querying.
    mock_request.reset_mock()
    cached_result = to_call(my_obi)
    assert cached_result == expected_result
    mock_request.assert_not_called()


def test_get_status_from_cache() -> None:
    """
    Test PyObihai device info functions don't query the device if we have
    (reasonably) up-to-date data.
    """

    my_obi = PyObihai(*MOCK_LOGIN)
    my_obi._cached_status = STATUS_XML

    with patch(_GET_REQUEST_PATCH, MagicMock()) as mock_request:
        my_obi._get_device_info("Product Information", "HardwareVersion")

    mock_request.assert_not_called()


def test_get_status_cache_update() -> None:
    """Test PyObihai device info functions update the cache after Obihai reboots."""

    my_obi = PyObihai(*MOCK_LOGIN)
    my_obi._cached_status = MockResponse("GARBAGE_DATA", 200)
    my_obi._last_status_check = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) - datetime.timedelta(hours=1)

    with patch(_GET_REQUEST_PATCH, MagicMock(return_value=STATUS_XML)) as mock_request:
        result = my_obi._get_device_info("Product Information", "HardwareVersion")

    assert result == "1.4"
    mock_request.assert_called()


def test_get_state() -> None:
    """Test PyObihai.get_line_state"""

    my_obi = PyObihai(*MOCK_LOGIN)
    with patch(_GET_REQUEST_PATCH, MagicMock(return_value=STATUS_XML)):
        status = my_obi.get_state()

    # I'm worried these could potentially not match up
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    last_reboot = now - datetime.timedelta(
        days=7,
        hours=0,
        minutes=28,
        seconds=58,
        microseconds=now.microsecond,
    )

    assert status == {
        "Reboot Required": "false",
        "Last Reboot": last_reboot,
        "SP1 Service Status": "0",
        "SP2 Service Status": "0",
        "SP4 Service Status": "0",
        "OBiTALK Service Status": "Normal",
    }


@pytest.mark.parametrize(
    "to_call,response,expected_result",
    [
        pytest.param(
            PyObihai.check_account, FAILED_REQUEST, False, id="account_invalid"
        ),
        pytest.param(PyObihai.check_account, STATUS_XML, True, id="account_valid"),
        pytest.param(PyObihai.call_reboot, FAILED_REQUEST, False, id="reboot_failed"),
        pytest.param(PyObihai.call_reboot, STATUS_XML, True, id="reboot_success"),
    ],
)
def test_services(
    to_call: Callable,
    response: MockResponse,
    expected_result: bool,
) -> None:
    """Test PyObihai services functions."""

    my_obi = PyObihai(*MOCK_LOGIN)
    with patch("pyobihai.requests.get", MagicMock(return_value=response)):
        result = to_call(my_obi)

    assert result == expected_result


def test_failed_get_request() -> None:
    """Test PyObihai._get_request() logs an error."""

    side_effect = RequestException("Failure")
    with pytest.raises(RequestException):
        with patch("pyobihai.requests.get", side_effect=side_effect):
            with patch("pyobihai.LOGGER.debug") as logger:
                my_obi = PyObihai(*MOCK_LOGIN)
                my_obi._get_request("testing")

    logger.assert_called_with(side_effect)


def test_non_admin_user() -> None:
    """Test PyObihai generates a user URL."""

    my_obi = PyObihai("192.168.1.100", "user", "password")
    assert my_obi._server.endswith("/user/")


@pytest.mark.parametrize(
    "response,expected_result",
    [
        pytest.param(NO_ACTIVE_CALLS_HTML, "No Active Calls", id="no_calls"),
        pytest.param(INBOUND_CALL_HTML, "Inbound Call", id="inbound_call"),
        pytest.param(OUTBOUND_CALL_HTML, "Outbound Call", id="outbound_call"),
    ],
)
def test_get_call_direction(response: MockResponse, expected_result: str) -> None:
    """Test PyObihai call direction lookup."""

    my_obi = PyObihai(*MOCK_LOGIN)
    with patch(_GET_REQUEST_PATCH, MagicMock(return_value=response)):
        result = my_obi.get_call_direction()

    assert result == {"Call Direction": expected_result}

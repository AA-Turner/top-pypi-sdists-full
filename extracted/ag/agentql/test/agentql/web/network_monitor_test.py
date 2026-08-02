import time

import pytest

from agentql.ext.playwright._network_monitor import (
    DOM_NETWORK_QUIET_THRESHOLD_SECONDS,
    IGNORE_DOM_ACTIVITY_AFTER_SECONDS,
    IGNORE_PENDING_REQUESTS_AFTER_SECONDS,
    PageActivityMonitor,
)

# pylint: disable=protected-access

# making it a bit longer than default threshold to avoid flakiness
DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS = DOM_NETWORK_QUIET_THRESHOLD_SECONDS + 0.05


@pytest.fixture
def page_monitor():
    start_time = time.time()
    monitor = PageActivityMonitor()
    return start_time, monitor


class Request:
    def __init__(self, url):
        self.url = url


@pytest.mark.usefixtures("instant_sleep")
def test_network_monitor_tracking_request_and_response():
    """Test that the page activity monitor tracks requests and responses."""
    monitor = PageActivityMonitor()
    request = Request("https://www.linkedin.com/li/tscp/sct")
    response = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request)
    monitor.track_network_response(response)
    assert len(monitor._response_log) == 1
    assert len(monitor._request_log) == 1
    assert monitor._response_log.pop() == request.url
    assert monitor._request_log.popitem()[0] == request.url


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_network_and_dom_inactivity_with_single_url(page_monitor):
    """Test that the page activity monitor detects inactivity with network and dom inactivity when there is single url."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request_1)
    monitor.track_network_response(response_1)
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_dom_activity(page_monitor):
    """Test that the page activity monitor detects dom activity."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request_1)
    monitor.track_network_response(response_1)
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS - 0.1)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is False


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_network_activity(page_monitor):
    """Test that the page activity monitor detects network activity."""
    start_time, monitor = page_monitor
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request_1)
    monitor.track_network_response(response_1)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is False


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_network_and_dom_inactivity_with_different_urls(page_monitor):
    """Test that the page activity monitor detects inactivity with network and dom inactivity when there are different urls."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    request_2 = Request("https://www.google.com")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_2 = Request("https://www.google.com")
    monitor.track_network_request(request_1)
    monitor.track_network_request(request_2)
    monitor.track_network_response(response_1)
    monitor.track_network_response(response_2)
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_multiple_requests(page_monitor):
    """Test that the page activity monitor detects multiple requests."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    request_2 = Request("https://www.linkedin.com/li/tscp/sct")
    time.sleep(IGNORE_DOM_ACTIVITY_AFTER_SECONDS)
    monitor.track_network_request(request_1)
    monitor.track_network_request(request_2)
    assert monitor.is_page_ready(start_time=start_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_multiple_same_url_only_after_threshold(page_monitor):
    """Test that the page activity monitor will only detect multiple requests to same url after threshold."""
    start_time, monitor = page_monitor
    request = Request("https://www.linkedin.com/li/tscp/sct")
    response = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request)
    monitor.track_network_response(response)
    time.sleep(IGNORE_DOM_ACTIVITY_AFTER_SECONDS)
    monitor.track_network_request(request)
    monitor.track_network_response(response)
    assert monitor.is_page_ready(start_time=start_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_network_inactivity_after_threshold(page_monitor):
    """Test that the page activity monitor detects network inactivity after threshold, even though DOM is active."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    time.sleep(IGNORE_DOM_ACTIVITY_AFTER_SECONDS)
    monitor.track_network_request(request_1)
    monitor.track_network_response(response_1)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    dom_active_time = time.time() * 1000
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_checking_for_missing_responses(page_monitor):
    """Test that the page activity monitor checks for missing responses when detecting inactivity."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request_1)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is False


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_inactivity_for_long_request_over_one_and_half_second(page_monitor):
    """Test that the page activity monitor detects inactivity for a request without response but is inactive for more than 1.5s."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    monitor.track_network_request(request_1)
    time.sleep(IGNORE_PENDING_REQUESTS_AFTER_SECONDS)
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_inactivity_for_long_request_under_one_and_half_second_but_over_one_second(
    page_monitor,
):
    """Test that the page activity monitor detects inactivity for a long request that takes more than 1s."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    dom_active_time = time.time() * 1000
    monitor.track_network_request(request_1)
    time.sleep(1)
    assert monitor.is_page_ready(start_time=start_time) is False
    monitor.track_network_response(response_1)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_inactivity_in_continuous_requests(page_monitor):
    """Test that the page activity monitor detects inactivity in continuous requests."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    request_2 = Request("https://www.google.com")
    response_2 = Request("https://www.google.com")
    request_3 = Request("https://www.amazon.com")
    response_3 = Request("https://www.amazon.com")
    monitor.track_network_request(request_1)
    monitor.track_network_response(response_1)
    dom_active_time = time.time() * 1000
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS - 0.1)
    assert monitor.is_page_ready(start_time=start_time) is False
    monitor.track_network_request(request_2)
    monitor.track_network_response(response_2)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS - 0.1)
    assert monitor.is_page_ready(start_time=start_time) is False
    monitor.track_network_request(request_3)
    monitor.track_network_response(response_3)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_detecting_inactivity_with_out_of_order_reponses(page_monitor):
    """Test that the page activity monitor detects inactivity with out of order responses."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    request_2 = Request("https://www.google.com")
    response_2 = Request("https://www.google.com")
    request_3 = Request("https://www.amazon.com")
    response_3 = Request("https://www.amazon.com")
    dom_active_time = time.time() * 1000
    monitor.track_network_request(request_1)
    monitor.track_network_request(request_2)
    monitor.track_network_response(response_1)
    monitor.track_network_request(request_3)
    monitor.track_network_response(response_2)
    monitor.track_network_response(response_3)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True


@pytest.mark.usefixtures("instant_sleep")
def test_resetting_network_monitor(page_monitor):
    """Test that the page activity monitor resets."""
    start_time, monitor = page_monitor
    request_1 = Request("https://www.linkedin.com/li/tscp/sct")
    response_1 = Request("https://www.linkedin.com/li/tscp/sct")
    request_2 = Request("https://www.google.com")
    response_2 = Request("https://www.google.com")
    request_3 = Request("https://www.amazon.com")
    response_3 = Request("https://www.amazon.com")
    dom_active_time = time.time() * 1000
    monitor.track_network_request(request_1)
    monitor.track_network_request(request_2)
    monitor.track_network_response(response_1)
    monitor.track_network_request(request_3)
    monitor.track_network_response(response_2)
    monitor.track_network_response(response_3)
    time.sleep(DEFAULT_DOM_NETWORK_QUITE_TIMEOUT_SECONDS)
    assert monitor.is_page_ready(start_time=start_time, last_active_dom_time_ms=dom_active_time) is True
    monitor.reset()
    assert len(monitor._request_log) == 0
    assert len(monitor._response_log) == 0
    assert monitor._multi_request_found is False
    assert monitor._last_network_active_time is not None
    assert monitor._page_loaded is False

import pytest
import requests
from mockito import patch
from playwright.sync_api import Locator, sync_playwright

import agentql
from test.utils.http_mocks import create_fake_post

from .constants import (
    ELEMENTS_QUERY,
    ELEMENTS_RESPONSE,
    HTML,
    NO_RESULT_QUERY,
    NONE_RESPONSE,
    QUERY_DATA_ERROR_RESPONSE,
    QUERY_DATA_HTML,
    QUERY_DATA_QUERY,
    QUERY_DATA_RESPONSE,
    QUERY_DATA_RESPONSE_CLEANED,
    RESPONSE,
)


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = agentql.wrap(browser.new_page())
        page.wait_for_page_ready_state = lambda wait_for_network_idle=True: None
        yield page
        browser.close()


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.parametrize("experimental_query_elements_enabled", [True, False])
def test_get_by_prompt(page, experimental_query_elements_enabled: bool):
    """Test that the get_by_prompt method returns the correct locator."""
    patch(requests.post, create_fake_post(RESPONSE)[0])
    expected_locator: Locator = page.locator("[tf623_id='1']")

    # Set the HTML content of the page
    page.set_content(HTML)

    # Call get_by_ai
    result = page.get_by_prompt("test btn", experimental_query_elements_enabled=experimental_query_elements_enabled)  # type: ignore

    assert result

    assert result.get_attribute("tf623_id") == expected_locator.get_attribute("tf623_id")


@pytest.mark.usefixtures("instant_sleep")
def test_get_by_prompt_fast_mode(page):
    """Test that the get_by_prompt method returns the correct locator with fast mode."""
    mock_post, calls = create_fake_post(RESPONSE)

    with patch(requests.post, mock_post):
        expected_locator: Locator = page.locator("[tf623_id='1']")
        # Set the HTML content of the page
        page.set_content(HTML)

        result = page.get_by_prompt("test btn", mode="fast")  # type: ignore

        assert result

        assert result.get_attribute("tf623_id") == expected_locator.get_attribute("tf623_id")

        assert any(kwargs["json"]["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.usefixtures("instant_sleep")
def test_get_by_prompt_error(page):
    """Test that the get_by_prompt method returns None when element is not found."""
    patch(requests.post, create_fake_post(NONE_RESPONSE)[0])

    # Set the HTML content of the page
    page.set_content(HTML)

    # Call get_by_ai
    result = page.get_by_prompt("something not present on page")  # type: ignore

    assert not result


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.parametrize("experimental_query_elements_enabled", [True, False])
def test_query_elements(page, experimental_query_elements_enabled: bool):
    """Test that the query_elements method returns the correct response."""
    patch(requests.post, create_fake_post(ELEMENTS_RESPONSE)[0])

    # Set the HTML content of the page
    page.set_content(HTML)

    response = page.query_elements(
        ELEMENTS_QUERY, experimental_query_elements_enabled=experimental_query_elements_enabled
    )

    assert response.test_btn
    assert response.input_box


@pytest.mark.usefixtures("instant_sleep")
def test_query_elements_fast_mode(page):
    """Test that the query_elements method returns the correct response in fast mode."""
    mock_post, calls = create_fake_post(ELEMENTS_RESPONSE)

    with patch(requests.post, mock_post):
        # Set the HTML content of the page
        page.set_content(HTML)

        response = page.query_elements(ELEMENTS_QUERY, mode="fast")

        assert response.test_btn
        assert response.input_box

        assert any(kwargs["json"]["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.usefixtures("instant_sleep")
def test_query_elements_error(page):
    """Test that the query_elements method handles errors correctly."""
    patch(requests.post, create_fake_post(NONE_RESPONSE)[0])

    # Set the HTML content of the page
    page.set_content(HTML)

    response = page.query_elements(NO_RESULT_QUERY)

    assert not response.error_test_btn


@pytest.mark.usefixtures("instant_sleep")
def test_query_data(page):
    """Test that the query_data method returns the correct data."""
    patch(requests.post, create_fake_post(QUERY_DATA_RESPONSE)[0])

    # Set the HTML content of the page
    page.set_content(QUERY_DATA_HTML)

    response = page.query_data(QUERY_DATA_QUERY)

    assert response == QUERY_DATA_RESPONSE_CLEANED


@pytest.mark.usefixtures("instant_sleep")
def test_query_data_fast_mode(page):
    """Test that the query_data method returns the correct data in fast mode."""
    mock_post, calls = create_fake_post(QUERY_DATA_RESPONSE)

    with patch(requests.post, mock_post):
        # Set the HTML content of the page
        page.set_content(QUERY_DATA_HTML)

        response = page.query_data(QUERY_DATA_QUERY, mode="fast")

        assert response == QUERY_DATA_RESPONSE_CLEANED

        assert any(kwargs["json"]["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.usefixtures("instant_sleep")
def test_query_data_error(page):
    """Test that the query_data method handles errors correctly."""
    patch(requests.post, create_fake_post(QUERY_DATA_ERROR_RESPONSE)[0])

    # Set the HTML content of the page
    page.set_content(QUERY_DATA_HTML)

    response = page.query_data(NO_RESULT_QUERY)

    assert response["error_test_btn"] is None


@pytest.mark.usefixtures("instant_sleep")
def test_debug_info(page):
    """Test that the getter method for last query, response, and accessibility tree returns the correct data."""
    patch(requests.post, create_fake_post(QUERY_DATA_RESPONSE)[0])

    # Set the HTML content of the page
    page.set_content(QUERY_DATA_HTML)

    response = page.query_data(QUERY_DATA_QUERY, wait_for_network_idle=False)

    assert page.get_last_query() == QUERY_DATA_QUERY
    assert page.get_last_response() == response
    assert page.get_last_accessibility_tree() is not None

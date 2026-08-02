import json

import httpx
import pytest
import pytest_asyncio
from mockito import patch
from playwright.async_api import Locator, async_playwright

import agentql
from test.utils.http_mocks import create_fake_async_post

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


# pylint: disable=unused-argument
async def mock_wait_for_page_ready_state(**kwargs):
    return None


@pytest_asyncio.fixture
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await agentql.wrap_async(browser.new_page())
        page.wait_for_page_ready_state = mock_wait_for_page_ready_state  # type: ignore
        yield page
        await browser.close()


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.parametrize("experimental_query_elements_enabled", [True, False])
@pytest.mark.asyncio
async def test_get_by_prompt(page, experimental_query_elements_enabled: bool):
    """Test that the get_by_prompt method returns the correct locator."""
    patch(httpx.AsyncClient.post, create_fake_async_post(RESPONSE)[0])
    expected_locator: Locator = page.locator("[tf623_id='1']")

    # Set the HTML content of the page
    await page.set_content(HTML)

    # Call get_by_ai
    result = await page.get_by_prompt(
        "test btn",
        wait_for_network_idle=False,
        experimental_query_elements_enabled=experimental_query_elements_enabled,
    )  # type: ignore

    assert result

    assert await result.get_attribute("tf623_id") == await expected_locator.get_attribute("tf623_id")


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_get_by_prompt_fast_mode(page):
    """Test that the get_by_prompt method returns the correct locator."""
    mock_post, calls = create_fake_async_post(RESPONSE)

    with patch(httpx.AsyncClient.post, mock_post):
        expected_locator = page.locator("[tf623_id='1']")

        # Set the HTML content of the page
        await page.set_content(HTML)

        # Call get_by_ai
        result = await page.get_by_prompt("test btn", wait_for_network_idle=False, mode="fast")

        assert result

        assert await result.get_attribute("tf623_id") == await expected_locator.get_attribute("tf623_id")

        assert any(json.loads(kwargs["content"].decode("utf-8"))["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_get_by_prompt_error(page):
    """Test that the get_by_prompt method returns the correct locator."""
    patch(httpx.AsyncClient.post, create_fake_async_post(NONE_RESPONSE)[0])

    # Set the HTML content of the page
    await page.set_content(HTML)

    # Call get_by_ai
    result = await page.get_by_prompt("something not present on page", wait_for_network_idle=False)  # type: ignore

    assert not result


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.parametrize("experimental_query_elements_enabled", [True, False])
@pytest.mark.asyncio
async def test_query_elements(page, experimental_query_elements_enabled: bool):
    """Test that the query_elements method returns the correct response."""
    patch(httpx.AsyncClient.post, create_fake_async_post(ELEMENTS_RESPONSE)[0])

    # Set the HTML content of the page
    await page.set_content(HTML)

    response = await page.query_elements(
        ELEMENTS_QUERY,
        wait_for_network_idle=False,
        experimental_query_elements_enabled=experimental_query_elements_enabled,
    )

    assert response.test_btn
    assert response.input_box


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_query_elements_fast_mode(page):
    """Test that the query_elements method returns the correct response in fast mode."""
    mock_post, calls = create_fake_async_post(ELEMENTS_RESPONSE)

    with patch("httpx.AsyncClient.post", mock_post):
        # Set the HTML content of the page
        await page.set_content(HTML)

        response = await page.query_elements(ELEMENTS_QUERY, wait_for_network_idle=False, mode="fast")

        assert response.test_btn
        assert response.input_box

        assert any(json.loads(kwargs["content"].decode("utf-8"))["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_query_elements_error(page):
    """Test that the query_elements method handles errors correctly."""
    patch(httpx.AsyncClient.post, create_fake_async_post(NONE_RESPONSE)[0])

    # Set the HTML content of the page
    await page.set_content(HTML)

    response = await page.query_elements(NO_RESULT_QUERY, wait_for_network_idle=False)

    assert not response.error_test_btn


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_query_data(page):
    """Test that the query_data method returns the correct data."""
    patch(httpx.AsyncClient.post, create_fake_async_post(QUERY_DATA_RESPONSE)[0])

    # Set the HTML content of the page
    await page.set_content(QUERY_DATA_HTML)

    response = await page.query_data(QUERY_DATA_QUERY, wait_for_network_idle=False)

    assert response == QUERY_DATA_RESPONSE_CLEANED


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_query_data_fast_mode(page):
    """Test that the query_data method returns the correct data in fast mode."""
    mock_post, calls = create_fake_async_post(QUERY_DATA_RESPONSE)

    with patch(httpx.AsyncClient.post, mock_post):
        # Set the HTML content of the page
        await page.set_content(HTML)

        response = await page.query_elements(ELEMENTS_QUERY, wait_for_network_idle=False, mode="fast")

        response = await page.query_data(QUERY_DATA_QUERY, wait_for_network_idle=False)

        assert response == QUERY_DATA_RESPONSE_CLEANED

        assert any(json.loads(kwargs["content"].decode("utf-8"))["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_query_data_error(page):
    """Test that the query_data method handles errors correctly."""
    patch(httpx.AsyncClient.post, create_fake_async_post(QUERY_DATA_ERROR_RESPONSE)[0])

    # Set the HTML content of the page
    await page.set_content(QUERY_DATA_HTML)

    response = await page.query_data(NO_RESULT_QUERY, wait_for_network_idle=False)

    assert response["error_test_btn"] is None


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.asyncio
async def test_debug_info(page):
    """Test that the getter method for last query, response, and accessibility tree returns the correct data."""
    patch(httpx.AsyncClient.post, create_fake_async_post(QUERY_DATA_RESPONSE)[0])

    # Set the HTML content of the page
    await page.set_content(QUERY_DATA_HTML)

    response = await page.query_data(QUERY_DATA_QUERY, wait_for_network_idle=False)

    assert page.get_last_query() == QUERY_DATA_QUERY
    assert page.get_last_response() == response
    assert page.get_last_accessibility_tree() is not None

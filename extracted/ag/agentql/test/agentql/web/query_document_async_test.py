import json
import logging
import os

import httpx
import pytest
from mockito import patch

from agentql.tools.async_api import query_document
from test.utils.http_mocks import create_fake_async_post

from .constants import (
    DOCUMENT_PATH,
    INVALID_QUERY,
    QUERY_DOCUMENT_PROMPT,
    QUERY_DOCUMENT_QUERY,
    QUERY_DOCUMENT_RESPONSE,
    QUERY_DOCUMENT_RESPONSE_CLEANED,
)

log = logging.getLogger(__name__)

TEST_PDF_PATH = os.path.join(os.path.dirname(__file__), DOCUMENT_PATH)


@pytest.mark.asyncio
async def test_query_document_valid_params_file_path():
    """Tests that the function accepts a valid file path"""

    patch(httpx.AsyncClient.post, create_fake_async_post(QUERY_DOCUMENT_RESPONSE)[0])
    response = await query_document(
        file_path=TEST_PDF_PATH,
        query=QUERY_DOCUMENT_QUERY,
        mode="fast",
    )
    assert response == QUERY_DOCUMENT_RESPONSE_CLEANED


@pytest.mark.asyncio
async def test_query_document_valid_params_file_path_prompt():
    """Tests that the function accepts a valid file path"""

    patch(httpx.AsyncClient.post, create_fake_async_post(QUERY_DOCUMENT_RESPONSE)[0])
    response = await query_document(
        file_path=TEST_PDF_PATH,
        prompt=QUERY_DOCUMENT_PROMPT,
        mode="fast",
    )
    assert response == QUERY_DOCUMENT_RESPONSE_CLEANED


@pytest.mark.asyncio
async def test_query_document_valid_params_file_path_fast_mode():
    """Tests that the function accepts a valid file path"""
    mock_post, calls = create_fake_async_post(QUERY_DOCUMENT_RESPONSE)

    with patch(httpx.AsyncClient.post, mock_post):
        response = await query_document(
            file_path=TEST_PDF_PATH,
            query=QUERY_DOCUMENT_QUERY,
            mode="fast",
        )
        assert response == QUERY_DOCUMENT_RESPONSE_CLEANED

        assert any(json.loads(kwargs["data"]["body"])["params"]["mode"] == "fast" for _, kwargs in calls)


@pytest.mark.asyncio
async def test_query_document_invalid_params_file_path_not_found():
    """Tests that the function raises a FileNotFoundError if the file path does not exist"""
    with pytest.raises(FileNotFoundError):
        _ = await query_document(
            file_path="invalid_file_path",
            query=QUERY_DOCUMENT_QUERY,
        )


async def test_query_document_invalid_params_invalid_query():
    """Tests that the function raises a ValueError if query is syntactically invalid"""
    with pytest.raises(ValueError):
        _ = await query_document(
            file_path=TEST_PDF_PATH,
            query=INVALID_QUERY,
        )


async def test_query_document_invalid_params_both_query_and_prompt():
    """Tests that the function raises a ValueError if both query and prompt are provided"""
    with pytest.raises(ValueError):
        _ = await query_document(
            file_path=TEST_PDF_PATH,
            query=QUERY_DOCUMENT_QUERY,
            prompt=QUERY_DOCUMENT_PROMPT,
        )


async def test_query_document_invalid_params_no_query_or_prompt():
    """Tests that the function raises a ValueError if no query or prompt is provided"""
    with pytest.raises(ValueError):
        _ = await query_document(
            file_path=TEST_PDF_PATH,
        )

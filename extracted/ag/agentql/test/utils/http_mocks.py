"""Shared HTTP mocking utilities for tests."""

import httpx
from mockito import mock, when


def create_fake_post(response_data):
    """Create a fake HTTP post function for sync tests."""
    calls = []

    def fake_post(*args, **kwargs):
        calls.append((args, kwargs))
        mock_response = mock(httpx.Response)
        when(mock_response).json().thenReturn(response_data)
        when(mock_response).raise_for_status().thenReturn(None)
        return mock_response

    return fake_post, calls


def create_fake_async_post(response_data):
    """Create a fake HTTP post function for async tests."""
    calls = []

    async def fake_post(*args, **kwargs):
        calls.append((args, kwargs))
        mock_response = mock(httpx.Response)
        when(mock_response).json().thenReturn(response_data)
        when(mock_response).raise_for_status().thenReturn(None)
        return mock_response

    return fake_post, calls

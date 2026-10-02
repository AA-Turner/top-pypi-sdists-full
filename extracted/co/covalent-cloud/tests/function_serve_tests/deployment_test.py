# Copyright 2024 Agnostiq Inc.

import unittest
from contextlib import asynccontextmanager
from unittest.mock import patch

from covalent_cloud.function_serve.client import FunctionServeClient
from covalent_cloud.function_serve.common import ServiceStatus, wait_for_deployment_to_be_active
from covalent_cloud.function_serve.models import Deployment, RouteInfo

# NOTE: Abridged record. Needs to be kept up to date.
_DUMMY_FUNCTION_RECORD = {
    "id": "999999999999999",
    "title": "My LLM Service v1",
    "tags": ["llm", "llama2"],
    "invoke_url": "http://fake.covalent.xyz/fn/999999999999999",
    "auth": False,
    "description": "A fake LLM service for testing purposes.",
    "endpoints": [
        {
            "method": "POST",
            "route": "/infer",
            "name": "Non-streaming LLM Chatbot",
            "endpoint_fn": "<function_object_string>",
            "endpoint_fn_source": "def non_streaming(prompt, model):\n...",
            "streaming": False,
            "description": "<doc_string or user's description>",
            "test_endpoint_enabled": True,
        },
        {
            "method": "POST",
            "route": "/infer_streaming",
            "name": "Streaming LLM Chatbot",
            "endpoint_fn": "<function_object_string>",
            "endpoint_fn_source": "def streaming(prompt, model):\n...",
            "streaming": True,
            "description": "<doc_string or user's description>",
            "test_endpoint_enabled": True,
        },
    ],
    "status": "NEW_OBJECT",
}


class TestDeployment(unittest.IsolatedAsyncioTestCase):
    """Test the Deployment class."""

    def setUp(self) -> None:
        self.normal_route = RouteInfo(route="/custom123", method="POST", streaming=False)
        self.streaming_route = RouteInfo(
            route="/custom123_streaming", method="POST", streaming=True
        )
        self.deployment_id = "1234567890"
        self.address = "http://fake-address.com"
        self.name = "Fake Service for Testing"
        self.description = "A fake service for testing purposes."
        self.default_routes = [self.normal_route, self.streaming_route]
        self.status = ServiceStatus.ACTIVE
        self.tags = ["fake-tag", "fake-tag-2"]
        self.default_fsc = FunctionServeClient(
            function_id=self.deployment_id,
            host=self.address,
            token_getter=lambda: "fake-default-token",
        )

    def default_info(self):
        """Return a default Deployment object."""
        info = Deployment(
            function_id=self.deployment_id,
            address=self.address,
            name=self.name,
            description=self.description,
            routes=self.default_routes,
            status=self.status,
            tags=self.tags,
        )
        info.attach_route_methods(overwrite=True)
        return info

    def test_init_from_function_record(self):
        """Initialize a Deployment object with valid data."""

        fake_function_record = _DUMMY_FUNCTION_RECORD.copy()

        info = Deployment.from_function_record(fake_function_record)
        assert info.function_id == fake_function_record["id"]
        assert info.address == fake_function_record["invoke_url"]
        assert info.name == fake_function_record["title"]
        assert len(info.routes) == len(fake_function_record["endpoints"])
        assert info.status == fake_function_record["status"]
        assert info.tags == fake_function_record["tags"]

    def test_error_attribute(self):
        """Test that a deployment's `error` attribute is set correctly."""
        fake_fn_record_with_error = _DUMMY_FUNCTION_RECORD.copy()
        fake_fn_record_with_error["status"] = "ERROR"
        fake_fn_record_with_error["error"] = (
            "Traceback (most recent call last):\nFake error message."
        )

        info = Deployment.from_function_record(fake_fn_record_with_error)

        # Confirm error is assigned to `.error` attribute.
        assert info.error == fake_fn_record_with_error["error"]

        # Confirm error is rendered in the string representation.
        assert "───────── Exception ────────" in str(info)

        # Disable reload and check `wait_for_deployment_to_be_active` logic.
        with patch.object(Deployment, "reload", new=lambda self: None):
            for status in [ServiceStatus.ERROR, ServiceStatus.INACTIVE]:
                info.status = status
                info = wait_for_deployment_to_be_active(info)
                assert info.error == fake_fn_record_with_error["error"]

    def test_token_update(self):
        """Test that setting `info.token` uses the token in requests."""

        def fake_requests_request(*args, **kwargs):
            return FakeResponse(args, kwargs, self.default_info())

        # Patch to simply return call args, kwargs.
        with patch(
            "covalent_cloud.function_serve.client.requests.request",
            fake_requests_request,
        ):
            # Token is not set in `default_info`.
            info = self.default_info()
            response = info.custom123()
            assert "x-api-key" not in response["request_kwargs"]["headers"]

        with patch(
            "covalent_cloud.function_serve.client.requests.request",
            fake_requests_request,
        ):
            # Set token and retry.
            info.token = "fake-token"
            response = info.custom123()
            assert response["request_kwargs"]["headers"]["x-api-key"] == info.token

    def test_builtin_teardown_endpoint(self):
        """Test the builtin `teardown` method."""
        # Patch to do nothing instead of posting.
        with patch("requests.Session.put") as mock_put:
            with patch.object(
                FunctionServeClient, "teardown", wraps=self.default_fsc.teardown
            ) as mock_fsc_teardown:

                # Succeeds with a 'valid' API key.
                info = self.default_info()
                info.teardown()
                mock_fsc_teardown.assert_called_once()
                mock_put.assert_called_once()

    def test_builtin_info_endpoint(self):
        """Test the builtin `info` method."""

        def fake_requests_post(*args, **kwargs):
            return FakeResponse(args, kwargs, self.default_info())

        # Patch to simply return call args, kwargs.
        with patch(
            "covalent_cloud.function_serve.client.requests.post",
            fake_requests_post,
        ):
            with patch.object(
                FunctionServeClient, "info", wraps=self.default_fsc.info
            ) as mock_fsc_info:

                info = self.default_info()
                response = info.info()
                mock_fsc_info.assert_called_once()
                assert response["request_args"][0] == f"{info.address}/info"

    def test_user_endpoint_sync(self):
        """
        Test requests posted to user-defined service endpoints.
        Synchronous, non-streaming requests.
        """

        def fake_requests_post(*args, **kwargs):
            return FakeResponse(args, kwargs, self.default_info())

        # Patch to simply return call args, kwargs.
        with patch(
            "covalent_cloud.function_serve.client.requests.request",
            fake_requests_post,
        ):
            with patch.object(
                FunctionServeClient,
                "_request",
                wraps=self.default_fsc._request,  # pylint: disable=protected-access
            ) as mock_fsc_request:

                info = self.default_info()
                response = info.custom123(some_param="some_value", another_param="another_value")
                mock_fsc_request.assert_called_once()
                assert response["request_kwargs"]["method"] == self.normal_route.method
                assert (
                    response["request_kwargs"]["url"] == f"{info.address}{self.normal_route.route}"
                )
                assert response["request_kwargs"]["json"] == {
                    "some_param": "some_value",
                    "another_param": "another_value",
                }
                assert response["request_kwargs"]["timeout"] is None

    async def test_user_endpoint_async(self):
        """
        Test requests posted to user-defined service endpoints.
        Asynchronous, streaming requests.
        """
        # Patch to simply return call args, kwargs.
        with patch(
            "covalent_cloud.function_serve.client.aiohttp.ClientSession",
            AsyncFakeClientSession,
        ):
            with patch.object(
                FunctionServeClient,
                "_async_request",
                wraps=self.default_fsc._async_request,  # pylint: disable=protected-access
            ) as mock_fsc_async_request:

                info = self.default_info()
                response = await info.async_custom123(
                    some_param="some_value", another_param="another_value"
                )
                mock_fsc_async_request.assert_called_once()
                assert response["request_kwargs"]["method"] == self.normal_route.method
                assert (
                    response["request_kwargs"]["url"] == f"{info.address}{self.normal_route.route}"
                )
                assert response["request_kwargs"]["json"] == {
                    "some_param": "some_value",
                    "another_param": "another_value",
                }

    def test_user_endpoint_streaming_sync(self):
        """
        Test requests posted to user-defined service endpoints.
        Synchronous, streaming requests.
        """

        def fake_requests_post(*args, **kwargs):
            return FakeResponse(args, kwargs, self.default_info())

        # Patch to simply return call args, kwargs.
        with patch(
            "covalent_cloud.function_serve.client.requests.request",
            fake_requests_post,
        ):
            with patch.object(
                FunctionServeClient,
                "_request_streaming",
                wraps=self.default_fsc._request_streaming,  # pylint: disable=protected-access
            ) as mock_fsc_request_streaming:

                info = self.default_info()
                info.token = "fake-token"
                words = []
                for word in info.custom123_streaming(
                    some_param="some_value", another_param="another_value"
                ):
                    words.append(word)
                mock_fsc_request_streaming.assert_called_once()

            assert " ".join(words) == FakeResponse.fake_content

    async def test_user_endpoint_streaming_async(self):
        """
        Test requests posted to user-defined service endpoints.
        Asynchronous, streaming requests.
        """
        # Patch to simply return call args, kwargs.
        with patch(
            "covalent_cloud.function_serve.client.aiohttp.ClientSession",
            FakeClientSession,
        ):
            with patch.object(
                FunctionServeClient,
                "_async_request_streaming",
                wraps=self.default_fsc._async_request_streaming,  # pylint: disable=protected-access
            ) as mock_fsc_async_request_streaming:

                info = self.default_info()
                info.token = "fake-token"
                words = []
                async for word in info.async_custom123_streaming(
                    some_param="some_value", another_param="another_value"
                ):
                    words.append(word)
                mock_fsc_async_request_streaming.assert_called_once()

            assert " ".join(words) == FakeResponse.fake_content


class FakeClientSession:
    """Stand-in for an `aiohttp.ClientSession` object. Avoid making real requests."""

    @asynccontextmanager
    async def request(self, *args, **kwargs):
        """Return a fake response object."""
        try:
            t_obj = TestDeployment()
            t_obj.setUp()
            yield FakeResponse(args, kwargs, info=t_obj.default_info())
        finally:
            pass

    async def __aenter__(self):
        """Return self for use in async context managers."""
        return self

    async def __aexit__(self, *args):
        """Do nothing when exiting async context managers."""
        pass


class AsyncFakeClientSession(FakeClientSession):
    @asynccontextmanager
    async def request(self, *args, **kwargs):
        try:
            t_obj = TestDeployment()
            t_obj.setUp()
            yield AsyncFakeResponse(args, kwargs, info=t_obj.default_info())
        finally:
            pass


class FakeResponse:
    """Stand-in for a `requests.Response` object. Avoid makings real requests."""

    fake_content = "This is a fake generated response from a fake LLM."

    @property
    def content(self):
        """Return a fake response body."""
        return FakeContent(self.fake_content)

    def __init__(self, args, kwargs, info: Deployment, error=False):
        self.request_args = args
        self.request_kwargs = kwargs
        self.info = info
        self.error = error

    @property
    def text(self):
        return self.fake_content

    def raise_for_status(self):
        """Raise a fake exception if necessary."""
        if self.error:
            raise Exception("Fake error")

    def iter_content(self):
        """Iterate over a fake response body."""
        for word in self.fake_content.split():
            yield word

    def json(self):
        """Return a fake response body."""
        d = self.info.model_dump()
        name_map = {
            "id": "function_id",
            "title": "name",
            "invoke_url": "address",
            "endpoints": "routes",
        }
        for m, n in name_map.items():
            d[m] = d.pop(n)
        d["request_args"] = self.request_args
        d["request_kwargs"] = self.request_kwargs
        return d


class AsyncFakeResponse(FakeResponse):
    async def text(self):
        return self.fake_content

    async def json(self):
        return super().json()


class FakeContent:
    """Stand-in for an `aiohttp` response content object."""

    def __init__(self, content):
        self.content = content

    async def iter_any(self):
        """Iterate over a fake response body."""
        for word in self.content.split():
            yield word

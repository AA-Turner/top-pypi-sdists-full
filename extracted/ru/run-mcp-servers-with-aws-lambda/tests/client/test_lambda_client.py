import json
import time
from unittest import mock
from unittest.mock import AsyncMock

import anyio
import pytest
from mcp.shared.message import SessionMessage
from mcp.types import (
    JSONRPCError,
    JSONRPCMessage,
    JSONRPCNotification,
    JSONRPCRequest,
    JSONRPCResponse,
)

from mcp_lambda import (
    LambdaFunctionParameters,
    lambda_function_client,
)

lambda_parameters = LambdaFunctionParameters(
    function_name="mock-function", region_name="us-west-2"
)


def mock_lambda_client(mock_client_creator, response, payload):
    mock_client = AsyncMock()

    mock_payload = AsyncMock()
    mock_payload.__aenter__.return_value = AsyncMock()
    mock_payload.__aenter__.return_value.read = AsyncMock(
        return_value=json.dumps(payload).encode("utf-8")
    )

    mock_client.invoke.return_value = {"Payload": mock_payload} | response

    mock_client_creator.return_value.__aenter__.return_value = mock_client

    return mock_client


@pytest.mark.anyio
@mock.patch("aiobotocore.session.get_session")
@mock.patch("aiobotocore.session.ClientCreatorContext")
async def test_lambda_function_client_success(mock_client_creator, mock_session):
    mock_session.create_client = mock_client_creator

    mock_client = mock_lambda_client(
        mock_client_creator,
        response={"StatusCode": 200},
        payload={
            "jsonrpc": "2.0",
            "id": "response-id",
            "result": {"message": "success"},
        },
    )

    # Create a test message
    test_message = SessionMessage(
        JSONRPCMessage(root=JSONRPCRequest(jsonrpc="2.0", id=1, method="ping"))
    )

    async with lambda_function_client(lambda_parameters) as (read_stream, write_stream):
        # Send a message
        async with write_stream:
            await write_stream.send(test_message)

        # Receive the response
        async with read_stream:
            response = await read_stream.receive()

        # Verify the response
        assert isinstance(response, SessionMessage)
        assert isinstance(response.message, JSONRPCMessage)
        assert isinstance(response.message.root, JSONRPCResponse)
        assert response.message.root.id == "response-id"
        assert response.message.root.result == {"message": "success"}

        # Verify Lambda was invoked with correct parameters
        mock_client.invoke.assert_called_once()
        call_args = mock_client.invoke.call_args[1]
        assert call_args["FunctionName"] == "mock-function"
        assert call_args["InvocationType"] == "RequestResponse"
        assert json.loads(call_args["Payload"].decode("utf-8")) == {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
        }


@pytest.mark.anyio
@mock.patch("aiobotocore.session.get_session")
@mock.patch("aiobotocore.session.ClientCreatorContext")
async def test_lambda_function_notification_success(mock_client_creator, mock_session):
    mock_session.create_client = mock_client_creator

    mock_client = mock_lambda_client(
        mock_client_creator,
        response={"StatusCode": 200},
        payload={},
    )

    # Create a test message
    test_message = SessionMessage(
        JSONRPCMessage(
            root=JSONRPCNotification(jsonrpc="2.0", method="notifications/initialized")
        )
    )

    async with lambda_function_client(lambda_parameters) as (read_stream, write_stream):
        # Send a message
        async with write_stream:
            await write_stream.send(test_message)

        # Test that we don't receive a response
        async with read_stream:
            with pytest.raises(anyio.WouldBlock):
                time.sleep(1)
                read_stream.receive_nowait()

        # Verify Lambda was invoked with correct parameters
        mock_client.invoke.assert_called_once()
        call_args = mock_client.invoke.call_args[1]
        assert call_args["FunctionName"] == "mock-function"
        assert call_args["InvocationType"] == "RequestResponse"
        assert json.loads(call_args["Payload"].decode("utf-8")) == {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }


@pytest.mark.anyio
@mock.patch("aiobotocore.session.get_session")
@mock.patch("aiobotocore.session.ClientCreatorContext")
async def test_lambda_function_client_function_error(mock_client_creator, mock_session):
    mock_session.create_client = mock_client_creator

    mock_client = mock_lambda_client(
        mock_client_creator,
        response={"StatusCode": 200, "FunctionError": "Unhandled"},
        payload={
            "jsonrpc": "2.0",
            "id": "response-id",
            "result": {
                "errorMessage": "Something went wrong",
                "errorType": "RuntimeError",
            },
        },
    )

    # Create a test message
    test_message = SessionMessage(
        JSONRPCMessage(
            root=JSONRPCRequest(
                jsonrpc="2.0", id=1, method="call/tool", params={"hello": "world"}
            )
        )
    )

    async with lambda_function_client(lambda_parameters) as (read_stream, write_stream):
        # Send a message
        async with write_stream:
            await write_stream.send(test_message)

        # Receive the response
        async with read_stream:
            response = await read_stream.receive()

        # Verify the response is an error message
        assert isinstance(response, SessionMessage)
        assert isinstance(response.message, JSONRPCMessage)
        assert isinstance(response.message.root, JSONRPCError)
        assert response.message.root.id == 1
        assert response.message.root.error is not None
        assert response.message.root.error.code == 500
        assert (
            "Function invoke returned a function error"
            in response.message.root.error.message
        )

        # Verify Lambda was invoked with correct parameters
        mock_client.invoke.assert_called_once()
        call_args = mock_client.invoke.call_args[1]
        assert call_args["FunctionName"] == "mock-function"
        assert call_args["InvocationType"] == "RequestResponse"
        assert json.loads(call_args["Payload"].decode("utf-8")) == {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "call/tool",
            "params": {"hello": "world"},
        }


@pytest.mark.anyio
@mock.patch("aiobotocore.session.get_session")
@mock.patch("aiobotocore.session.ClientCreatorContext")
async def test_lambda_function_client_invoke_exception(
    mock_client_creator, mock_session
):
    mock_session.create_client = mock_client_creator

    # Make invoke raise an exception
    mock_client = AsyncMock()
    mock_client_creator.return_value.__aenter__.return_value = mock_client
    mock_client.invoke.side_effect = Exception("Connection error")

    # Create a test message
    test_message = SessionMessage(
        JSONRPCMessage(root=JSONRPCRequest(jsonrpc="2.0", id=1, method="ping"))
    )

    async with lambda_function_client(lambda_parameters) as (read_stream, write_stream):
        # Send a message
        async with write_stream:
            await write_stream.send(test_message)

        # Receive the response
        async with read_stream:
            response = await read_stream.receive()

        # Verify the response is an error message
        assert isinstance(response, SessionMessage)
        assert isinstance(response.message, JSONRPCMessage)
        assert isinstance(response.message.root, JSONRPCError)
        assert response.message.root.id == 1
        assert response.message.root.error is not None
        assert response.message.root.error.code == 500
        assert "Connection error" in response.message.root.error.message

        # Verify Lambda was invoked with correct parameters
        mock_client.invoke.assert_called_once()
        call_args = mock_client.invoke.call_args[1]
        assert call_args["FunctionName"] == "mock-function"
        assert call_args["InvocationType"] == "RequestResponse"
        assert json.loads(call_args["Payload"].decode("utf-8")) == {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
        }


@pytest.mark.anyio
@mock.patch("aiobotocore.session.get_session")
@mock.patch("aiobotocore.session.ClientCreatorContext")
async def test_lambda_function_client_invalid_response(
    mock_client_creator, mock_session
):
    mock_session.create_client = mock_client_creator

    mock_client = mock_lambda_client(
        mock_client_creator,
        response={"StatusCode": 200},
        payload="invalid json",
    )

    # Create a test message
    test_message = SessionMessage(
        JSONRPCMessage(root=JSONRPCRequest(jsonrpc="2.0", id=1, method="ping"))
    )

    async with lambda_function_client(lambda_parameters) as (read_stream, write_stream):
        # Send a message
        async with write_stream:
            await write_stream.send(test_message)

        # Receive the response
        async with read_stream:
            response = await read_stream.receive()

        # Verify the response is an error message
        assert isinstance(response, SessionMessage)
        assert isinstance(response.message, JSONRPCMessage)
        assert isinstance(response.message.root, JSONRPCError)
        assert response.message.root.id == 1
        assert response.message.root.error is not None
        assert response.message.root.error.code == 500
        assert (
            "4 validation errors for JSONRPCMessage"
            in response.message.root.error.message
        )

        # Verify Lambda was invoked with correct parameters
        mock_client.invoke.assert_called_once()
        call_args = mock_client.invoke.call_args[1]
        assert call_args["FunctionName"] == "mock-function"
        assert call_args["InvocationType"] == "RequestResponse"
        assert json.loads(call_args["Payload"].decode("utf-8")) == {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
        }

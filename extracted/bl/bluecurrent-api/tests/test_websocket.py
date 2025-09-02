from unittest.mock import MagicMock
from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect
from websockets.exceptions import (
    InvalidStatus,
    ConnectionClosedError,
    WebSocketException,
)
from websockets.frames import Close

from src.bluecurrent_api.websocket import (
    Websocket,
    WebsocketError,
    RequestLimitReached,
    InvalidApiToken,
    AlreadyConnected,
)

import pytest
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_start(mocker: MockerFixture):
    mocker.patch("src.bluecurrent_api.websocket.Websocket.validate_api_token")
    mock__loop = mocker.patch("src.bluecurrent_api.websocket.Websocket._loop")

    websocket = Websocket()

    mock_receiver = mocker.AsyncMock()
    mock_on_open = mocker.AsyncMock()

    with pytest.raises(WebsocketError):
        await websocket.start(mock_receiver, mock_on_open)

    websocket.auth_token = "123"
    await websocket.start(mock_receiver, mock_on_open)
    mock__loop.assert_called_once_with(mock_receiver, mock_on_open)

    mock_raise_correct_exception = mocker.patch(
        "src.bluecurrent_api.websocket.Websocket.raise_correct_exception"
    )
    err = WebSocketException()
    mock__loop.side_effect = err

    await websocket.start(mock_receiver, mock_on_open)
    mock_raise_correct_exception.assert_called_once_with(err)


@pytest.mark.asyncio
async def test__loop(mocker: MockerFixture):
    websocket = Websocket()
    mock_connect = MagicMock(spec=connect)
    mocker.patch("src.bluecurrent_api.websocket.connect", return_value=mock_connect)
    mock_raise_correct_exception = mocker.patch(
        "src.bluecurrent_api.websocket.Websocket.raise_correct_exception"
    )

    mock_receiver = mocker.AsyncMock()
    mock_on_open = mocker.AsyncMock()

    mock_on_open.side_effect = WebSocketException()
    await websocket._loop(mock_receiver, mock_on_open)
    assert websocket.conn is None
    assert websocket.connected.is_set() is False
    assert websocket.received_charge_points.is_set() is False
    mock_raise_correct_exception.assert_called_once()


@pytest.mark.asyncio
async def test__send_recv_single_message(mocker: MockerFixture):
    websocket = Websocket()
    mock_connect = MagicMock(spec=connect)
    mock_ws = MagicMock(spec=ClientConnection)
    mocker.patch("src.bluecurrent_api.websocket.connect", return_value=mock_connect)
    mock_connect.__aenter__.return_value = mock_ws
    mock_ws.recv.return_value = '{"a": 1}'

    assert await websocket._send_recv_single_message({}) == {"a": 1}

    err = WebSocketException()
    mock_ws.recv.side_effect = err
    with pytest.raises(WebsocketError):
        await websocket._send_recv_single_message({})


@pytest.mark.asyncio
async def test_validate_token(mocker: MockerFixture):
    api_token = "123"
    websocket = Websocket()

    mocker.patch(
        "src.bluecurrent_api.websocket.Websocket._send_recv_single_message",
        return_value={
            "object": "STATUS_API_TOKEN",
            "success": True,
            "token": "abc",
            "customer_id": "123",
        },
    )
    result = await websocket.validate_api_token(api_token)
    assert result == "123"
    assert websocket.auth_token == "Token abc"

    mocker.patch(
        "src.bluecurrent_api.websocket.Websocket._send_recv_single_message",
        return_value={"object": "STATUS_API_TOKEN", "success": False, "error": ""},
    )
    with pytest.raises(InvalidApiToken):
        await websocket.validate_api_token(api_token)

    mocker.patch(
        "src.bluecurrent_api.websocket.Websocket._send_recv_single_message",
        return_value={
            "object": "ERROR",
            "error": 42,
            "message": "Request limit reached",
        },
    )
    with pytest.raises(RequestLimitReached):
        await websocket.validate_api_token(api_token)


@pytest.mark.asyncio
async def test_get_email(mocker: MockerFixture):
    websocket = Websocket()
    mocker.patch(
        "src.bluecurrent_api.websocket.Websocket._send_recv_single_message",
        return_value={"object": "ACCOUNT", "login": "test"},
    )

    with pytest.raises(WebsocketError):
        await websocket.get_email()
    websocket.auth_token = "abc"
    assert await websocket.get_email() == "test"

    mocker.patch(
        "src.bluecurrent_api.websocket.Websocket._send_recv_single_message",
        return_value={"object": "ACCOUNT"},
    )
    with pytest.raises(WebsocketError):
        await websocket.get_email()

    mocker.patch(
        "src.bluecurrent_api.websocket.Websocket._send_recv_single_message",
        return_value={
            "object": "ERROR",
            "error": 42,
            "message": "Request limit reached",
        },
    )
    with pytest.raises(RequestLimitReached):
        await websocket.get_email()


@pytest.mark.asyncio
async def test_send_request(mocker: MockerFixture):
    mock_send = mocker.patch("src.bluecurrent_api.websocket.Websocket._send")
    websocket = Websocket()
    websocket.connected.set()

    # without token
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.auth_token = "123"

    await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    mock_send.assert_called_with(
        {"command": "GET_CHARGE_POINTS", "Authorization": "123"}
    )


@pytest.mark.asyncio
async def test_message_handler(mocker: MockerFixture):
    mock_handle_charge_points = mocker.patch(
        "src.bluecurrent_api.websocket.handle_charge_points"
    )
    mock_handle_status = mocker.patch("src.bluecurrent_api.websocket.handle_status")
    mock_handle_grid = mocker.patch("src.bluecurrent_api.websocket.handle_grid")
    mock_handle_settings = mocker.patch("src.bluecurrent_api.websocket.handle_settings")
    mock_handle_setting_change = mocker.patch(
        "src.bluecurrent_api.websocket.handle_setting_change"
    )

    mock_handle_handle_session_messages = mocker.patch(
        "src.bluecurrent_api.websocket.handle_session_messages"
    )

    websocket = Websocket()

    mock_receiver = mocker.AsyncMock()

    # CHARGE_POINTS flow
    message = {"object": "CHARGE_POINTS"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_charge_points.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    message = {"object": "CHARGE_CARDS"}
    await websocket._message_handler(message, mock_receiver)
    mock_receiver.assert_called_with(message)

    # ch_status flow
    message = {"object": "CH_STATUS"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_status.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # grid_status flow
    message = {"object": "GRID_STATUS"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_grid.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # grid_current flow
    message = {"object": "GRID_CURRENT"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_grid.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # ch_settings flow
    message = {"object": "CH_SETTINGS"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_settings.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # setting change flow
    message = {"object": "STATUS_SET_PLUG_AND_CHARGE"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_setting_change.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # session message flow
    message = {"object": "STATUS_STOP_SESSION"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_handle_session_messages.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # STATUS_START_SESSION
    message = {"object": "STATUS_START_SESSION", "evse_id": "BCU101"}
    await websocket._message_handler(message, mock_receiver)
    mock_handle_handle_session_messages.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # no object
    message = {"value": True}
    with pytest.raises(WebsocketError):
        await websocket._message_handler(message, mock_receiver)

    # unknown command
    message = {"error": 0, "object": "ERROR", "message": "Unknown command"}
    with pytest.raises(WebsocketError):
        await websocket._message_handler(message, mock_receiver)

    # unknown token
    message = {"error": 1, "object": "ERROR", "message": "Invalid Auth Token"}
    with pytest.raises(WebsocketError):
        await websocket._message_handler(message, mock_receiver)

    # token not authorized
    message = {"error": 2, "object": "ERROR", "message": "Not authorized"}
    with pytest.raises(WebsocketError):
        await websocket._message_handler(message, mock_receiver)

    # unknown error
    message = {"error": 9, "object": "ERROR", "message": "Unknown error"}
    with pytest.raises(WebsocketError):
        await websocket._message_handler(message, mock_receiver)

    # limit reached
    message = {"error": 42, "object": "ERROR", "message": "Request limit reached"}
    with pytest.raises(RequestLimitReached):
        await websocket._message_handler(message, mock_receiver)

    # success false
    message = {"success": False, "error": "this is an error"}
    with pytest.raises(WebsocketError):
        await websocket._message_handler(message, mock_receiver)

    # Ignore status
    message = {"object": "STATUS"}
    await websocket._message_handler(message, mock_receiver)
    assert mock_receiver.call_count == 9

    # RECEIVED without error
    message = {"object": "RECEIVED_START_SESSION", "error": ""}
    await websocket._message_handler(message, mock_receiver)
    assert mock_receiver.call_count == 9


@pytest.mark.asyncio
async def test__send(mocker: MockerFixture):
    websocket = Websocket()

    with pytest.raises(WebsocketError):
        await websocket._send({"command": "test"})

    websocket.conn = mocker.MagicMock(spec=ClientConnection)

    await websocket._send({"command": 1})
    websocket.conn.send.assert_called_with('{"command": 1}')


@pytest.mark.asyncio
async def test_disconnect(mocker: MockerFixture):
    websocket = Websocket()

    with pytest.raises(WebsocketError):
        await websocket.disconnect()

    websocket.conn = mocker.MagicMock(spec=ClientConnection)
    await websocket.disconnect()
    websocket.conn.close.assert_called_once()


def make_mock_response(status_code, reason):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.headers = {"x-websocket-reject-reason": reason}
    return mock_response


def test_raise_correct_exception():
    websocket = Websocket()

    with pytest.raises(RequestLimitReached):
        websocket.raise_correct_exception(
            InvalidStatus(make_mock_response(403, "Request limit reached"))
        )

    with pytest.raises(RequestLimitReached):
        websocket.raise_correct_exception(
            ConnectionClosedError(Close(4001, "Request limit reached"), None, None)
        )

    with pytest.raises(AlreadyConnected):
        websocket.raise_correct_exception(
            InvalidStatus(make_mock_response(403, "Already connected"))
        )

    with pytest.raises(WebsocketError):
        websocket.raise_correct_exception(Exception("Some unexpected error"))

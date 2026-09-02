"""Tests for Slack API integration."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.slack_api import SlackAPI, SlackChannel, SlackUser


@pytest.mark.slack
class TestSlackAPI:
    """Test suite for SlackAPI class."""

    def test_init_with_token(self):
        """Test initialization with bot token."""
        api = SlackAPI(token="xoxb-test-token")
        assert api.token == "xoxb-test-token"
        assert api.headers["Authorization"] == "Bearer xoxb-test-token"

    def test_init_with_webhook(self):
        """Test initialization with webhook URL."""
        api = SlackAPI(webhook_url="https://hooks.slack.com/test")
        assert api.webhook_url == "https://hooks.slack.com/test"
        assert api.headers == {}  # No auth headers for webhook

    def test_init_from_env(self):
        """Test initialization from environment variables."""
        with patch.dict("os.environ", {"SLACK_BOT_TOKEN": "xoxb-env-token"}):
            api = SlackAPI()
            assert api.token == "xoxb-env-token"

    def test_init_without_credentials_raises(self):
        """Test initialization without credentials raises error."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(
                ValueError, match="Either SLACK_BOT_TOKEN or SLACK_WEBHOOK_URL"
            ):
                SlackAPI()

    @pytest.mark.asyncio
    async def test_send_webhook_message_success(self):
        """Test sending message via webhook."""
        api = SlackAPI(webhook_url="https://hooks.slack.com/test")

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            result = await api.send_webhook_message("Test message")

            assert result is True
            mock_post.assert_called_once_with(
                "https://hooks.slack.com/test",
                json={"text": "Test message"},
                headers={"Content-Type": "application/json"},
            )

    @pytest.mark.asyncio
    async def test_send_webhook_message_no_url(self):
        """Test sending webhook message without URL raises error."""
        api = SlackAPI(token="xoxb-test-token")

        with pytest.raises(ValueError, match="Webhook URL not configured"):
            await api.send_webhook_message("Test")

    @pytest.mark.asyncio
    async def test_send_message_success(self):
        """Test sending message via API."""
        api = SlackAPI(token="xoxb-test-token")

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "ok": True,
                "ts": "1234567890.123456",
                "channel": "C1234567890",
            }

            result = await api.send_message("#general", "Test message")

            assert result["ts"] == "1234567890.123456"
            assert result["channel"] == "C1234567890"
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_message_with_thread(self):
        """Test sending threaded message."""
        api = SlackAPI(token="xoxb-test-token")

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"ok": True}

            await api.send_message("#general", "Reply", thread_ts="1234567890.123456")

            call_args = mock_request.call_args[1]["json"]
            assert call_args["thread_ts"] == "1234567890.123456"

    @pytest.mark.asyncio
    async def test_send_message_with_blocks(self):
        """Test sending message with blocks."""
        api = SlackAPI(token="xoxb-test-token")
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": "Test"}}]

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"ok": True}

            await api.send_message("#general", "Test", blocks=blocks)

            call_args = mock_request.call_args[1]["json"]
            assert call_args["blocks"] == blocks

    @pytest.mark.asyncio
    async def test_get_channel_list(self):
        """Test getting channel list."""
        api = SlackAPI(token="xoxb-test-token")

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "ok": True,
                "channels": [
                    {
                        "id": "C1234567890",
                        "name": "general",
                        "is_private": False,
                        "is_member": True,
                        "num_members": 10,
                    }
                ],
            }

            channels = await api.get_channel_list()

            assert len(channels) == 1
            assert isinstance(channels[0], SlackChannel)
            assert channels[0].id == "C1234567890"
            assert channels[0].name == "general"
            assert channels[0].is_member is True

    @pytest.mark.asyncio
    async def test_get_user_list(self):
        """Test getting user list."""
        api = SlackAPI(token="xoxb-test-token")

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "ok": True,
                "members": [
                    {
                        "id": "U1234567890",
                        "name": "testuser",
                        "real_name": "Test User",
                        "profile": {"email": "test@example.com"},
                        "is_bot": False,
                        "is_admin": False,
                        "deleted": False,
                    }
                ],
            }

            users = await api.get_user_list()

            assert len(users) == 1
            assert isinstance(users[0], SlackUser)
            assert users[0].id == "U1234567890"
            assert users[0].email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_channel_history(self):
        """Test getting channel message history."""
        api = SlackAPI(token="xoxb-test-token")

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "ok": True,
                "messages": [
                    {
                        "type": "message",
                        "user": "U1234567890",
                        "text": "Hello world",
                        "ts": "1234567890.123456",
                    }
                ],
            }

            messages = await api.get_channel_history("C1234567890")

            assert len(messages) == 1
            assert messages[0]["text"] == "Hello world"

    @pytest.mark.asyncio
    async def test_test_auth(self):
        """Test authentication check."""
        api = SlackAPI(token="xoxb-test-token")

        with patch.object(api, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "ok": True,
                "team": "Test Team",
                "team_id": "T1234567890",
                "user": "testbot",
                "user_id": "U1234567890",
                "bot_id": "B1234567890",
            }

            auth_info = await api.test_auth()

            assert auth_info["team"] == "Test Team"
            assert auth_info["bot_id"] == "B1234567890"

    def test_create_ticket_blocks(self):
        """Test creating ticket notification blocks."""
        api = SlackAPI(token="xoxb-test-token")

        blocks = api.create_ticket_blocks(
            ticket_id="TICKET-123",
            title="Test Ticket",
            description="This is a test",
            status="IN_PROGRESS",
            assignee="John Doe",
            url="https://example.com/ticket/123",
        )

        assert len(blocks) >= 4  # Header, fields, description, context
        assert blocks[0]["type"] == "header"
        assert "TICKET-123" in blocks[0]["text"]["text"]

        # Check for button
        action_block = next((b for b in blocks if b["type"] == "actions"), None)
        assert action_block is not None
        assert action_block["elements"][0]["url"] == "https://example.com/ticket/123"

    @pytest.mark.asyncio
    async def test_make_request_error_handling(self):
        """Test API error handling."""
        api = SlackAPI(token="xoxb-test-token")

        with patch("httpx.AsyncClient.request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "ok": False,
                "error": "channel_not_found",
            }
            mock_request.return_value = mock_response

            with pytest.raises(Exception, match="Slack API error: channel_not_found"):
                await api._make_request("POST", "chat.postMessage", json={})

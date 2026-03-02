"""Telegram Bot API wrapper.

Provides a simple async client for interacting with the Telegram Bot API.
Uses httpx for HTTP requests (already a dependency of the CLI).
"""

import asyncio
from dataclasses import dataclass
from typing import Any, AsyncIterator

import httpx


# Telegram Bot API base URL
API_BASE = "https://api.telegram.org/bot{token}"

# Timeout for long-polling (seconds)
LONG_POLL_TIMEOUT = 30

# HTTP timeout (slightly longer than long-poll to account for network)
HTTP_TIMEOUT = LONG_POLL_TIMEOUT + 10


@dataclass
class TelegramUser:
    """Represents a Telegram user."""

    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramUser":
        return cls(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            username=data.get("username"),
        )

    @property
    def display_name(self) -> str:
        """Get a display name for the user."""
        if self.username:
            return f"@{self.username}"
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


@dataclass
class TelegramChat:
    """Represents a Telegram chat."""

    id: int
    type: str  # "private", "group", "supergroup", "channel"
    title: str | None = None  # For groups/channels
    username: str | None = None
    first_name: str | None = None  # For private chats

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramChat":
        return cls(
            id=data["id"],
            type=data["type"],
            title=data.get("title"),
            username=data.get("username"),
            first_name=data.get("first_name"),
        )

    @property
    def display_name(self) -> str:
        """Get a display name for the chat."""
        if self.title:
            return self.title
        if self.first_name:
            return self.first_name
        return str(self.id)


@dataclass
class TelegramPhotoSize:
    """Represents one size variant of a Telegram photo."""

    file_id: str
    file_unique_id: str
    width: int = 0
    height: int = 0
    file_size: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramPhotoSize":
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            width=data.get("width", 0),
            height=data.get("height", 0),
            file_size=data.get("file_size", 0),
        )


@dataclass
class TelegramVoice:
    """Represents a Telegram voice message."""

    file_id: str
    file_unique_id: str
    duration: int = 0
    mime_type: str = ""
    file_size: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramVoice":
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            duration=data.get("duration", 0),
            mime_type=data.get("mime_type", ""),
            file_size=data.get("file_size", 0),
        )


@dataclass
class TelegramMessage:
    """Represents a Telegram message."""

    message_id: int
    chat: TelegramChat
    text: str | None = None
    caption: str | None = None
    photo: list[TelegramPhotoSize] | None = None
    voice: TelegramVoice | None = None
    from_user: TelegramUser | None = None
    date: int = 0  # Unix timestamp

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramMessage":
        from_user = None
        if "from" in data:
            from_user = TelegramUser.from_dict(data["from"])

        photo = None
        if "photo" in data:
            photo = [TelegramPhotoSize.from_dict(p) for p in data["photo"]]

        voice = None
        if "voice" in data:
            voice = TelegramVoice.from_dict(data["voice"])

        return cls(
            message_id=data["message_id"],
            chat=TelegramChat.from_dict(data["chat"]),
            text=data.get("text"),
            caption=data.get("caption"),
            photo=photo,
            voice=voice,
            from_user=from_user,
            date=data.get("date", 0),
        )

    @property
    def has_media(self) -> bool:
        """Return True if the message contains any media."""
        return bool(self.photo or self.voice)

    @property
    def effective_text(self) -> str | None:
        """Return text content: text field, or caption for media messages."""
        return self.text or self.caption


@dataclass
class TelegramUpdate:
    """Represents a Telegram update (incoming event)."""

    update_id: int
    message: TelegramMessage | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramUpdate":
        message = None
        if "message" in data:
            message = TelegramMessage.from_dict(data["message"])

        return cls(
            update_id=data["update_id"],
            message=message,
        )


class TelegramAPIError(Exception):
    """Error from Telegram Bot API."""

    def __init__(self, error_code: int, description: str):
        self.error_code = error_code
        self.description = description
        super().__init__(f"Telegram API error {error_code}: {description}")


class TelegramBot:
    """Async Telegram Bot API client."""

    def __init__(self, token: str):
        """Initialize the bot with a token.

        Args:
            token: Bot token from @BotFather
        """
        self.token = token
        self._base_url = API_BASE.format(token=token)
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "TelegramBot":
        """Enter async context."""
        self._client = httpx.AsyncClient(timeout=HTTP_TIMEOUT)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get the HTTP client, creating if needed."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=HTTP_TIMEOUT)
        return self._client

    async def _request(
        self,
        method: str,
        **params: Any,
    ) -> dict[str, Any]:
        """Make a request to the Telegram Bot API.

        Args:
            method: API method name (e.g., "getMe", "sendMessage")
            **params: Method parameters

        Returns:
            Response data from the API

        Raises:
            TelegramAPIError: If the API returns an error
        """
        url = f"{self._base_url}/{method}"
        client = self._get_client()

        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}

        response = await client.post(url, json=params)
        data = response.json()

        if not data.get("ok"):
            raise TelegramAPIError(
                error_code=data.get("error_code", 0),
                description=data.get("description", "Unknown error"),
            )

        return data.get("result", {})

    async def get_me(self) -> TelegramUser:
        """Get information about the bot.

        Returns:
            TelegramUser representing the bot
        """
        result = await self._request("getMe")
        return TelegramUser.from_dict(result)

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str | None = "Markdown",
        reply_to_message_id: int | None = None,
        disable_notification: bool = False,
    ) -> TelegramMessage:
        """Send a text message.

        Args:
            chat_id: Target chat ID
            text: Message text (max 4096 characters)
            parse_mode: "Markdown", "HTML", or None for plain text
            reply_to_message_id: Message ID to reply to
            disable_notification: Send silently

        Returns:
            The sent message
        """
        # Truncate if needed
        if len(text) > 4096:
            text = text[:4093] + "..."

        result = await self._request(
            "sendMessage",
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
        )
        return TelegramMessage.from_dict(result)

    async def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: str | None = "Markdown",
    ) -> TelegramMessage:
        """Edit a message's text.

        Args:
            chat_id: Chat containing the message
            message_id: ID of the message to edit
            text: New text
            parse_mode: "Markdown", "HTML", or None

        Returns:
            The edited message
        """
        # Truncate if needed
        if len(text) > 4096:
            text = text[:4093] + "..."

        result = await self._request(
            "editMessageText",
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode,
        )
        return TelegramMessage.from_dict(result)

    async def delete_message(
        self,
        chat_id: int,
        message_id: int,
    ) -> bool:
        """Delete a message.

        Args:
            chat_id: Chat containing the message
            message_id: ID of the message to delete

        Returns:
            True if deletion was successful
        """
        result = await self._request(
            "deleteMessage",
            chat_id=chat_id,
            message_id=message_id,
        )
        return bool(result)

    async def send_chat_action(
        self,
        chat_id: int,
        action: str = "typing",
    ) -> bool:
        """Send a chat action (typing indicator, etc.).

        Args:
            chat_id: Target chat ID
            action: Action type ("typing", "upload_document", etc.)

        Returns:
            True if successful
        """
        result = await self._request(
            "sendChatAction",
            chat_id=chat_id,
            action=action,
        )
        return bool(result)

    async def get_file(self, file_id: str) -> dict[str, Any]:
        """Get file info for downloading.

        Args:
            file_id: Telegram file_id from a message

        Returns:
            File info dict with file_path for downloading
        """
        return await self._request("getFile", file_id=file_id)

    async def download_file(self, file_path: str) -> bytes:
        """Download a file from Telegram servers.

        Args:
            file_path: file_path from getFile response

        Returns:
            Raw file bytes
        """
        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        client = self._get_client()
        response = await client.get(url)
        response.raise_for_status()
        return response.content

    async def download_file_by_id(self, file_id: str) -> bytes:
        """Download a file by its file_id (convenience method).

        Args:
            file_id: Telegram file_id

        Returns:
            Raw file bytes
        """
        file_info = await self.get_file(file_id)
        return await self.download_file(file_info["file_path"])

    async def set_my_commands(
        self,
        commands: list[dict[str, str]],
    ) -> bool:
        """Register bot commands for the Telegram command menu.

        Args:
            commands: List of {"command": "name", "description": "text"} dicts

        Returns:
            True if successful
        """
        result = await self._request("setMyCommands", commands=commands)
        return bool(result)

    async def get_my_commands(self) -> list[dict[str, str]]:
        """Fetch the bot's currently registered commands.

        Returns:
            List of {"command": "name", "description": "text"} dicts.
        """
        result = await self._request("getMyCommands")
        if isinstance(result, list):
            return result
        return []

    async def get_updates(
        self,
        offset: int | None = None,
        timeout: int = LONG_POLL_TIMEOUT,
        allowed_updates: list[str] | None = None,
    ) -> list[TelegramUpdate]:
        """Get updates (incoming messages) using long-polling.

        Args:
            offset: Identifier of the first update to be returned
            timeout: Timeout in seconds for long polling
            allowed_updates: List of update types to receive

        Returns:
            List of updates
        """
        if allowed_updates is None:
            allowed_updates = ["message"]

        result = await self._request(
            "getUpdates",
            offset=offset,
            timeout=timeout,
            allowed_updates=allowed_updates,
        )

        return [TelegramUpdate.from_dict(u) for u in result]

    async def poll_updates(
        self,
        offset: int = 0,
    ) -> AsyncIterator[TelegramUpdate]:
        """Continuously poll for updates.

        This is an async generator that yields updates as they arrive.
        It handles reconnection on errors.

        Args:
            offset: Starting update offset

        Yields:
            TelegramUpdate instances
        """
        current_offset = offset

        while True:
            try:
                updates = await self.get_updates(
                    offset=current_offset + 1 if current_offset is not None else None,
                    timeout=LONG_POLL_TIMEOUT,
                )

                for update in updates:
                    current_offset = update.update_id
                    yield update

            except httpx.TimeoutException:
                # Normal timeout, continue polling
                continue

            except httpx.HTTPError as e:
                # Network error, wait and retry
                await asyncio.sleep(5)
                continue

            except TelegramAPIError as e:
                if e.error_code == 409:
                    # Conflict: another instance is polling
                    raise
                # Other API errors, wait and retry
                await asyncio.sleep(5)
                continue


async def verify_token(token: str) -> TelegramUser | None:
    """Verify a bot token is valid.

    Args:
        token: Bot token to verify

    Returns:
        TelegramUser representing the bot if valid, None otherwise
    """
    try:
        async with TelegramBot(token) as bot:
            return await bot.get_me()
    except (TelegramAPIError, httpx.HTTPError):
        return None

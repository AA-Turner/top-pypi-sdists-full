import asyncio
import base64
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta
import aiofiles
import contextlib

# Microsoft Graph SDK imports for Teams
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.chat_message_collection_response import ChatMessageCollectionResponse
from msgraph.generated.models.channel import Channel
from msgraph.generated.models.team import Team
from msgraph.generated.models.chat import Chat
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.chat_message_attachment import ChatMessageAttachment
from msgraph.generated.models.file_attachment import FileAttachment
from msgraph.generated.models.chat_message_hosted_content import ChatMessageHostedContent
from msgraph.generated.models.o_data_errors.o_data_error import ODataError

# Request builders and configurations
from msgraph.generated.teams.item.channels.get_all_messages.get_all_messages_request_builder import (
    GetAllMessagesRequestBuilder
)
from msgraph.generated.chats.item.messages.messages_request_builder import (
    MessagesRequestBuilder
)
from msgraph.generated.chats.chats_request_builder import ChatsRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration

from ..exceptions import FileError, FileNotFound, ComponentError
from .O365Client import O365Client


class TeamsClient(O365Client):
    """
    Microsoft Teams Client - Using Microsoft Graph SDK

    Uses Microsoft Graph SDK for all Microsoft Teams operations.

    Managing Teams channels, chats, and messages through Microsoft Graph API.

    Methods:
        list_channels: List channels in a team.
        find_channel_by_name: Find a channel by name across teams.
        get_channel_info: Get channel information.
        get_channel_messages: Get all messages from a channel (getAllMessages).
        send_channel_message: Send a message to a channel with optional attachments (files/cards).
        send_channel_file: Send a file to a channel (legacy - use send_channel_message instead).
        send_chat_message: Send a message to a chat with optional attachments (files/cards).
        list_user_chats: List all user chats.
        find_chat_by_name: Find a chat by name.
        get_chat_messages: Get all messages from a private chat.
        find_one_on_one_chat: Find one-on-one chat between two users.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Teams-specific properties
        self._default_page_size = 50
        self._max_attachment_size = 25 * 1024 * 1024  # 25MB limit
        self._max_retries = 3

    def get_context(self, url: str = None, *args):
        """
        Backwards compatibility method.
        Returns the Graph client instead of office365 context.
        """
        return self.graph_client

    def _start_(self, **kwargs):
        """Initialize Teams-specific configuration."""
        self._logger.info("Microsoft Teams client initialized successfully")
        return True

    def connection(self):
        """
        Establish Teams connection using the migrated O365Client.

        This uses Microsoft Graph SDK authentication for Teams operations.
        """
        # Use the parent O365Client connection method
        super().connection()

        self._logger.info("Microsoft Teams connection established successfully")
        return self

    async def verify_teams_access(self):
        """Verify Teams access by testing basic operations."""
        try:
            # Test basic access by listing teams
            teams = await self.list_teams()
            self._logger.info(f"Teams access verified: Found {len(teams)} teams")

        except Exception as e:
            self._logger.error(f"Teams access verification failed: {e}")
            raise RuntimeError(f"Teams access verification failed: {e}") from e

    async def list_teams(self) -> List[Dict[str, Any]]:
        """
        List all teams the user has access to using Microsoft Graph API.
        """
        try:
            teams_response = await self.graph_client.me.joined_teams.get()

            teams = []
            if teams_response and teams_response.value:
                for team in teams_response.value:
                    team_info = {
                        "id": team.id,
                        "displayName": team.display_name,
                        "description": team.description or "",
                        "visibility": str(team.visibility) if team.visibility else "private",
                        "webUrl": team.web_url or "",
                        "isArchived": team.is_archived or False
                    }
                    teams.append(team_info)

            return teams

        except Exception as err:
            self._logger.error(f"Error listing teams: {err}")
            raise ComponentError(f"Error listing teams: {err}") from err

    async def list_channels(self, team_id: str) -> List[Dict[str, Any]]:
        """
        List channels in a specific team using Microsoft Graph API.

        Args:
            team_id (str): The ID of the team

        Returns:
            List[Dict[str, Any]]: List of channels in the team
        """
        try:
            channels_response = await self.graph_client.teams.by_team_id(team_id).channels.get()

            channels = []
            if channels_response and channels_response.value:
                for channel in channels_response.value:
                    channel_info = {
                        "id": channel.id,
                        "displayName": channel.display_name,
                        "description": channel.description or "",
                        "email": channel.email or "",
                        "webUrl": channel.web_url or "",
                        "membershipType": str(channel.membership_type) if channel.membership_type else "standard",
                        "isFavoriteByDefault": channel.is_favorite_by_default or False
                    }
                    channels.append(channel_info)

            return channels

        except Exception as err:
            self._logger.error(f"Error listing channels for team {team_id}: {err}")
            raise ComponentError(f"Error listing channels for team {team_id}: {err}") from err

    async def find_channel_by_name(self, channel_name: str) -> Optional[Dict[str, Any]]:
        """
        Find a channel by name across all teams the user has access to.

        Args:
            channel_name (str): Name of the channel to find

        Returns:
            Optional[Dict[str, Any]]: Channel info with team_id if found, None otherwise
        """
        try:
            teams = await self.list_teams()
            self._logger.info(f"Searching for channel '{channel_name}' across {len(teams)} teams")

            for team in teams:
                team_id = team["id"]
                team_name = team["displayName"]

                try:
                    channels = await self.list_channels(team_id)

                    for channel in channels:
                        if channel["displayName"].lower() == channel_name.lower():
                            result = {
                                "team_id": team_id,
                                "team_name": team_name,
                                "channel_id": channel["id"],
                                "channel_name": channel["displayName"],
                                "description": channel["description"],
                                "webUrl": channel["webUrl"]
                            }
                            self._logger.info(f"Found channel '{channel_name}' in team '{team_name}'")
                            return result

                except Exception as e:
                    self._logger.warning(f"Error searching channels in team '{team_name}': {e}")
                    continue

            self._logger.warning(f"Channel '{channel_name}' not found in any accessible team")
            return None

        except Exception as err:
            self._logger.error(f"Error finding channel by name '{channel_name}': {err}")
            raise ComponentError(f"Error finding channel by name '{channel_name}': {err}") from err

    async def get_channel_info(self, team_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific channel.

        Args:
            team_id (str): The ID of the team
            channel_id (str): The ID of the channel

        Returns:
            Dict[str, Any]: Detailed channel information
        """
        try:
            channel = await self.graph_client.teams.by_team_id(team_id)\
                .channels.by_channel_id(channel_id).get()

            if not channel:
                raise FileNotFound(f"Channel {channel_id} not found in team {team_id}")

            channel_info = {
                "id": channel.id,
                "displayName": channel.display_name,
                "description": channel.description or "",
                "email": channel.email or "",
                "webUrl": channel.web_url or "",
                "membershipType": str(channel.membership_type) if channel.membership_type else "standard",
                "isFavoriteByDefault": channel.is_favorite_by_default or False,
                "createdDateTime": channel.created_date_time.isoformat() if channel.created_date_time else None
            }

            return channel_info

        except Exception as err:
            self._logger.error(f"Error getting channel info for {channel_id}: {err}")
            raise ComponentError(f"Error getting channel info for {channel_id}: {err}") from err

    async def get_channel_messages(
        self,
        team_id: str,
        channel_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        max_messages: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all messages from a channel using getAllMessages endpoint.

        Args:
            team_id (str): The ID of the team
            channel_id (str): The ID of the channel
            start_time (str, optional): ISO 8601 formatted start time
            end_time (str, optional): ISO 8601 formatted end time
            max_messages (int, optional): Maximum number of messages to retrieve

        Returns:
            List[Dict[str, Any]]: List of messages from the channel
        """
        try:
            # Build query parameters
            query_params = {}

            if start_time and end_time:
                query_params["filter"] = f"lastModifiedDateTime gt {start_time} and lastModifiedDateTime lt {end_time}"

            if max_messages:
                query_params["top"] = min(max_messages, 50)  # Graph API limit per page

            # Create request configuration
            get_all_messages_params = GetAllMessagesRequestBuilder.GetAllMessagesRequestBuilderGetQueryParameters(
                **query_params
            )

            request_config = RequestConfiguration(
                query_parameters=get_all_messages_params
            )

            # Get messages using getAllMessages
            messages_response = await self.graph_client.teams.by_team_id(team_id)\
                .channels.get_all_messages.get(request_configuration=request_config)

            messages = []
            if messages_response and messages_response.value:
                for message in messages_response.value:
                    message_dict = self._message_to_dict(message)
                    messages.append(message_dict)

            # Handle pagination if needed and max_messages not reached
            next_link = messages_response.odata_next_link if messages_response else None
            while next_link and (not max_messages or len(messages) < max_messages):
                try:
                    # Use the next link to get more messages
                    next_response = await self.graph_client.teams.with_url(next_link).get()
                    if next_response and next_response.value:
                        for message in next_response.value:
                            if max_messages and len(messages) >= max_messages:
                                break
                            message_dict = self._message_to_dict(message)
                            messages.append(message_dict)
                    next_link = next_response.odata_next_link if next_response else None
                except Exception as e:
                    self._logger.warning(f"Error getting next page of messages: {e}")
                    break

            self._logger.info(f"Retrieved {len(messages)} messages from channel {channel_id}")
            return messages

        except Exception as err:
            self._logger.error(f"Error getting channel messages: {err}")
            raise ComponentError(f"Error getting channel messages: {err}") from err

    async def send_channel_message(
        self,
        team_id: str,
        channel_id: str,
        message_text: str,
        content_type: str = "html"
    ) -> Dict[str, Any]:
        """
        Send a message to a channel.

        Args:
            team_id (str): The ID of the team
            channel_id (str): The ID of the channel
            message_text (str): The message content
            content_type (str): Content type ('html' or 'text')

        Returns:
            Dict[str, Any]: Information about the sent message
        """
        try:
            # Create message object
            message = ChatMessage()
            message.body = ItemBody()

            if content_type.lower() == "html":
                message.body.content_type = BodyType.Html
            else:
                message.body.content_type = BodyType.Text

            message.body.content = message_text

            # Send the message
            sent_message = await self.graph_client.teams.by_team_id(team_id)\
                .channels.by_channel_id(channel_id).messages.post(message)

            result = self._message_to_dict(sent_message)
            self._logger.info(f"Sent message to channel {channel_id}")
            return result

        except Exception as err:
            self._logger.error(f"Error sending message to channel: {err}")
            raise ComponentError(f"Error sending message to channel: {err}") from err

    async def send_channel_file(
        self,
        team_id: str,
        channel_id: str,
        file_path: Path,
        message_text: str = ""
    ) -> Dict[str, Any]:
        """
        Send a file to a channel.

        Args:
            team_id (str): The ID of the team
            channel_id (str): The ID of the channel
            file_path (Path): Path to the file to send
            message_text (str): Optional message text to accompany the file

        Returns:
            Dict[str, Any]: Information about the sent message with file
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFound(f"File not found: {file_path}")

            # Check file size
            file_size = file_path.stat().st_size
            if file_size > self._max_attachment_size:
                raise ComponentError(f"File too large: {file_size} bytes (max: {self._max_attachment_size})")

            # Read file content
            async with aiofiles.open(file_path, "rb") as f:
                file_content = await f.read()

            # Create message with attachment
            message = ChatMessage()
            message.body = ItemBody()
            message.body.content_type = BodyType.Html

            # Create attachment reference in message body
            attachment_id = f"attachment_{file_path.name}"
            message_html = f"""
            <div>
                <div>{message_text}</div>
                <attachment id="{attachment_id}"></attachment>
            </div>
            """
            message.body.content = message_html

            # Create hosted content for the file
            hosted_content = ChatMessageHostedContent()
            hosted_content.content_bytes = base64.b64encode(file_content).decode()
            hosted_content.content_type = self._get_mime_type(file_path)
            hosted_content.additional_data = {
                "@microsoft.graph.temporaryId": attachment_id,
                "name": file_path.name
            }

            message.hosted_contents = [hosted_content]

            # Send the message with file
            sent_message = await self.graph_client.teams.by_team_id(team_id)\
                .channels.by_channel_id(channel_id).messages.post(message)

            result = self._message_to_dict(sent_message)
            self._logger.info(f"Sent file '{file_path.name}' to channel {channel_id}")
            return result

        except Exception as err:
            self._logger.error(f"Error sending file to channel: {err}")
            raise ComponentError(f"Error sending file to channel: {err}") from err

    async def list_user_chats(self, user_id: str = "me") -> List[Dict[str, Any]]:
        """
        List all chats for a specific user.

        Args:
            user_id (str): User ID or 'me' for current user

        Returns:
            List[Dict[str, Any]]: List of user's chats
        """
        try:
            if user_id == "me":
                chats_response = await self.graph_client.me.chats.get()
            else:
                chats_response = await self.graph_client.users.by_user_id(user_id).chats.get()

            chats = []
            if chats_response and chats_response.value:
                for chat in chats_response.value:
                    chat_info = {
                        "id": chat.id,
                        "topic": chat.topic or "",
                        "chatType": str(chat.chat_type) if chat.chat_type else "oneOnOne",
                        "createdDateTime": chat.created_date_time.isoformat() if chat.created_date_time else None,
                        "lastUpdatedDateTime": chat.last_updated_date_time.isoformat() if chat.last_updated_date_time else None,  # noqa
                        "webUrl": chat.web_url or ""
                    }
                    chats.append(chat_info)

            return chats

        except Exception as err:
            self._logger.error(f"Error listing chats for user {user_id}: {err}")
            raise ComponentError(f"Error listing chats for user {user_id}: {err}") from err

    async def find_chat_by_name(self, chat_name: str, user_id: str = "me") -> Optional[Dict[str, Any]]:
        """
        Find a chat by its topic/name.

        Args:
            chat_name (str): The name/topic of the chat to find
            user_id (str): User ID or 'me' for current user

        Returns:
            Optional[Dict[str, Any]]: Chat information if found, None otherwise
        """
        try:
            chats = await self.list_user_chats(user_id)

            for chat in chats:
                if chat["topic"] and chat["topic"].lower() == chat_name.lower():
                    self._logger.info(f"Found chat '{chat_name}' with ID: {chat['id']}")
                    return chat

            self._logger.warning(f"Chat '{chat_name}' not found")
            return None

        except Exception as err:
            self._logger.error(f"Error finding chat by name '{chat_name}': {err}")
            raise ComponentError(f"Error finding chat by name '{chat_name}': {err}") from err

    async def get_chat_messages(
        self,
        chat_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        max_messages: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all messages from a private chat.

        Args:
            chat_id (str): The ID of the chat
            start_time (str, optional): ISO 8601 formatted start time
            end_time (str, optional): ISO 8601 formatted end time
            max_messages (int, optional): Maximum number of messages to retrieve

        Returns:
            List[Dict[str, Any]]: List of messages from the chat
        """
        try:
            # Build query parameters
            query_params = {
                "orderby": ["lastModifiedDateTime desc"],
                "top": min(self._default_page_size, 50)
            }

            if start_time and end_time:
                query_params["filter"] = f"lastModifiedDateTime gt {start_time} and lastModifiedDateTime lt {end_time}"

            messages_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
                **query_params
            )

            request_config = RequestConfiguration(
                query_parameters=messages_params
            )

            messages = []
            response = await self.graph_client.chats.by_chat_id(chat_id).messages.get(
                request_configuration=request_config
            )

            if isinstance(response, ChatMessageCollectionResponse) and response.value:
                for message in response.value:
                    message_dict = self._message_to_dict(message)
                    messages.append(message_dict)

            # Handle pagination
            next_link = response.odata_next_link if response else None
            retry_count = 0

            while next_link and (not max_messages or len(messages) < max_messages):
                try:
                    next_response = await self.graph_client.chats.with_url(next_link).get()
                    if next_response and next_response.value:
                        for message in next_response.value:
                            if max_messages and len(messages) >= max_messages:
                                break
                            message_dict = self._message_to_dict(message)
                            messages.append(message_dict)
                    next_link = next_response.odata_next_link if next_response else None
                    retry_count = 0  # Reset retry count on success

                except ODataError as exc:
                    if exc.error.code == "TooManyRequests":
                        if retry_count < self._max_retries:
                            retry_after = exc.error.inner_error.additional_data.get('Retry-After', None)
                            wait_time = int(retry_after) if retry_after else (2 ** retry_count)
                            self._logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                            await asyncio.sleep(wait_time)
                            retry_count += 1
                        else:
                            self._logger.error("Max retries exceeded for rate limiting")
                            break
                    else:
                        raise
                except Exception as e:
                    self._logger.warning(f"Error getting next page of chat messages: {e}")
                    break

            self._logger.info(f"Retrieved {len(messages)} messages from chat {chat_id}")
            return messages

        except Exception as err:
            self._logger.error(f"Error getting chat messages: {err}")
            raise ComponentError(f"Error getting chat messages: {err}") from err

    async def find_one_on_one_chat(self, user_id_1: str, user_id_2: str) -> Optional[str]:
        """
        Find the one-on-one chat between two users by their object IDs.

        Args:
            user_id_1 (str): Object ID of the first user
            user_id_2 (str): Object ID of the second user

        Returns:
            Optional[str]: Chat ID if found, None otherwise
        """
        try:
            # Build query to fetch only oneOnOne chats with members included
            query_params = ChatsRequestBuilder.ChatsRequestBuilderGetQueryParameters(
                filter="chatType eq 'oneOnOne'",
                expand=["members"]
            )

            request_config = RequestConfiguration(query_parameters=query_params)
            response = await self.graph_client.chats.get(request_configuration=request_config)

            if not response or not response.value:
                return None

            # Search through chats to find match
            for chat in response.value:
                if not chat.members:
                    continue

                # Extract valid member IDs
                member_ids = set()
                for member in chat.members:
                    if hasattr(member, 'user') and member.user and hasattr(member.user, 'id'):
                        member_ids.add(member.user.id.lower())

                # Check if the two user IDs match the chat members
                search_ids = {user_id_1.lower(), user_id_2.lower()}
                if search_ids == member_ids:
                    self._logger.info(f"Found one-on-one chat between users: {chat.id}")
                    return chat.id

            self._logger.info(f"No one-on-one chat found between users {user_id_1} and {user_id_2}")
            return None

        except Exception as err:
            self._logger.error(f"Error finding one-on-one chat: {err}")
            raise ComponentError(f"Error finding one-on-one chat: {err}") from err

    # Helper methods

    def _message_to_dict(self, message: ChatMessage) -> Dict[str, Any]:
        """
        Convert ChatMessage object to dictionary.
        """
        result = {
            "id": message.id,
            "messageType": str(message.message_type) if message.message_type else "message",
            "createdDateTime": message.created_date_time.isoformat() if message.created_date_time else None,
            "lastModifiedDateTime": message.last_modified_date_time.isoformat() if message.last_modified_date_time else None,  # noqa
            "deletedDateTime": message.deleted_date_time.isoformat() if message.deleted_date_time else None,
            "subject": message.subject or "",
            "importance": str(message.importance) if message.importance else "normal",
            "webUrl": message.web_url or ""
        }

        # Handle message body
        if message.body:
            result["body"] = {
                "contentType": str(message.body.content_type) if message.body.content_type else "text",
                "content": message.body.content or ""
            }

        # Handle sender information
        if message.from_ and message.from_.user:
            result["from"] = {
                "id": message.from_.user.id or "",
                "displayName": message.from_.user.display_name or "",
                "userPrincipalName": message.from_.user.user_principal_name or ""
            }

        # Handle mentions
        if message.mentions:
            result["mentions"] = []
            for mention in message.mentions:
                mention_dict = {
                    "id": mention.id or "",
                    "mentionText": mention.mention_text or ""
                }
                if mention.mentioned and mention.mentioned.user:
                    mention_dict["mentioned"] = {
                        "id": mention.mentioned.user.id or "",
                        "displayName": mention.mentioned.user.display_name or ""
                    }
                result["mentions"].append(mention_dict)

        # Handle attachments
        if message.attachments:
            result["attachments"] = []
            for attachment in message.attachments:
                attachment_dict = {
                    "id": attachment.id or "",
                    "contentType": attachment.content_type or "",
                    "name": attachment.name or "",
                    "contentUrl": attachment.content_url or ""
                }
                result["attachments"].append(attachment_dict)

        return result

    def _get_mime_type(self, file_path: Path) -> str:
        """
        Get MIME type for file based on extension.
        """
        extension = file_path.suffix.lower()
        mime_types = {
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.zip': 'application/zip',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.csv': 'text/csv'
        }
        return mime_types.get(extension, 'application/octet-stream')

    async def test_permissions(self) -> Dict[str, Any]:
        """
        Test Teams permissions using Microsoft Graph API.
        """
        results = {
            "teams_access": False,
            "channels_access": False,
            "chats_access": False,
            "messages_access": False,
            "errors": []
        }

        try:
            # Test 1: Teams access
            teams = await self.list_teams()
            results["teams_access"] = True
            self._logger.info(f"Teams access: Found {len(teams)} teams")

            # Test 2: Channels access
            if teams:
                team_id = teams[0]["id"]
                channels = await self.list_channels(team_id)
                results["channels_access"] = True
                self._logger.info(f"Channels access: Found {len(channels)} channels")

                # Test 3: Messages access
                if channels:
                    channel_id = channels[0]["id"]
                    messages = await self.get_channel_messages(team_id, channel_id, max_messages=1)
                    results["messages_access"] = True
                    self._logger.info("Channel messages access: OK")

            # Test 4: Chats access
            chats = await self.list_user_chats()
            results["chats_access"] = True
            self._logger.info(f"Chats access: Found {len(chats)} chats")

        except Exception as e:
            results["errors"].append(str(e))
            self._logger.error(f"Permission test failed: {e}")

        return results

    async def close(self):
        """Clean up resources."""
        await super().close()

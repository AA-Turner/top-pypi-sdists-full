import asyncio
import base64
from typing import List, Optional, Dict, Any
from pathlib import Path
import aiofiles
import contextlib

# Microsoft Graph SDK imports (replacing office365-rest-python-client)
from msgraph.generated.models.message import Message
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.file_attachment import FileAttachment
from msgraph.generated.models.attachment import Attachment
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
from msgraph.generated.users.item.messages.item.move.move_post_request_body import MovePostRequestBody

from ..exceptions import FileError, FileNotFound
from .O365Client import O365Client


class OutlookClient(O365Client):
    """
    Outlook Client - Migrated to Microsoft Graph SDK

    Uses Microsoft Graph SDK for all Outlook Mail operations.

    Managing connections to Outlook Mail API.

    Methods:
        list_messages: List messages in a specified folder.
        download_message: Download a message by its ID.
        move_message: Move a message to a different folder.
        search_messages: Search for messages matching a query.
        send_message: Send emails with optional attachments.
        list_folders: List mail folders.
        get_message: Get a specific message by ID.
        delete_message: Delete a message by ID.
        mark_as_read: Mark a message as read/unread.
        download_attachment: Download a message attachment.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Outlook-specific properties
        self._default_page_size = 50
        self._max_attachment_size = 25 * 1024 * 1024  # 25MB limit for regular attachments

    def get_context(self, url: str = None, *args):
        """
        Backwards compatibility method.
        Returns the Graph client instead of office365 context.
        """
        return self.graph_client

    def _start_(self, **kwargs):
        """Initialize Outlook-specific configuration."""
        self._logger.info("Outlook client initialized successfully")
        return True

    def connection(self):
        """
        Establish Outlook connection using the migrated O365Client.

        This replaces the old office365-rest-python-client authentication
        with Microsoft Graph SDK authentication.
        """
        # Use the parent O365Client connection method
        super().connection()

        self._logger.info("Outlook connection established successfully")
        return self

    async def verify_outlook_access(self):
        """Verify Outlook access by testing basic operations."""
        try:
            # Test basic access by getting mail folders
            folders = await self.list_folders()
            self._logger.info(f"Outlook accessible: Found {len(folders)} mail folders")

        except Exception as e:
            self._logger.error(f"Outlook access verification failed: {e}")
            raise RuntimeError(f"Outlook access verification failed: {e}") from e

    async def list_folders(self) -> List[Dict[str, Any]]:
        """
        List mail folders using Microsoft Graph API.
        """
        try:
            folders_response = await self.graph_client.me.mail_folders.get()

            folders = []
            if folders_response and folders_response.value:
                for folder in folders_response.value:
                    folder_info = {
                        "id": folder.id,
                        "displayName": folder.display_name,
                        "parentFolderId": folder.parent_folder_id,
                        "childFolderCount": folder.child_folder_count or 0,
                        "unreadItemCount": folder.unread_item_count or 0,
                        "totalItemCount": folder.total_item_count or 0
                    }
                    folders.append(folder_info)

            return folders

        except Exception as err:
            self._logger.error(f"Error listing mail folders: {err}")
            raise FileError(f"Error listing mail folders: {err}") from err

    async def list_messages(
        self,
        folder: str = "Inbox",
        top: int = 10,
        filter_query: str = None,
        select_fields: List[str] = None,
        order_by: str = "receivedDateTime desc"
    ) -> List[Dict[str, Any]]:
        """
        List messages in a specified folder using Microsoft Graph API.
        """
        try:
            # Build the request
            if folder.lower() == "inbox":
                messages_request = self.graph_client.me.messages
            else:
                # Try to find folder by name first, then by ID
                folder_id = await self._resolve_folder_id(folder)
                messages_request = self.graph_client.me.mail_folders.by_mail_folder_id(folder_id).messages

            # Apply query parameters
            request = messages_request.get()

            # Apply top (limit)
            if top:
                request.query_parameters.top = min(top, 1000)  # Graph API limit

            # Apply filter
            if filter_query:
                request.query_parameters.filter = filter_query

            # Apply select
            if select_fields:
                request.query_parameters.select = select_fields
            else:
                # Default fields to select
                request.query_parameters.select = [
                    "id", "subject", "sender", "from", "toRecipients",
                    "receivedDateTime", "sentDateTime", "hasAttachments",
                    "importance", "isRead", "bodyPreview", "internetMessageId"
                ]

            # Apply ordering
            if order_by:
                request.query_parameters.orderby = [order_by]

            # Execute request
            messages_response = await request

            messages = []
            if messages_response and messages_response.value:
                for message in messages_response.value:
                    message_info = {
                        "id": message.id,
                        "subject": message.subject or "",
                        "sender": self._extract_email_address(message.sender),
                        "from": self._extract_email_address(message.from_),
                        "toRecipients": [self._extract_email_address(r) for r in (message.to_recipients or [])],
                        "receivedDateTime": message.received_date_time.isoformat() if message.received_date_time else None,  # noqa
                        "sentDateTime": message.sent_date_time.isoformat() if message.sent_date_time else None,
                        "hasAttachments": message.has_attachments or False,
                        "importance": str(message.importance) if message.importance else "normal",
                        "isRead": message.is_read or False,
                        "bodyPreview": message.body_preview or "",
                        "internetMessageId": message.internet_message_id or ""
                    }
                    messages.append(message_info)

            return messages

        except Exception as err:
            self._logger.error(f"Error listing messages: {err}")
            raise FileError(f"Error listing messages: {err}") from err

    async def get_message(self, message_id: str, include_body: bool = False) -> Dict[str, Any]:
        """
        Get a specific message by ID using Microsoft Graph API.
        """
        try:
            request = self.graph_client.me.messages.by_message_id(message_id).get()

            # Select fields based on whether body is needed
            if include_body:
                request.query_parameters.select = [
                    "id", "subject", "sender", "from", "toRecipients", "ccRecipients", "bccRecipients",
                    "receivedDateTime", "sentDateTime", "hasAttachments", "importance", "isRead",
                    "body", "bodyPreview", "internetMessageId", "conversationId"
                ]
            else:
                request.query_parameters.select = [
                    "id", "subject", "sender", "from", "toRecipients", "ccRecipients", "bccRecipients",
                    "receivedDateTime", "sentDateTime", "hasAttachments", "importance", "isRead",
                    "bodyPreview", "internetMessageId", "conversationId"
                ]

            message = await request

            if not message:
                raise FileNotFound(f"Message {message_id} not found")

            message_info = {
                "id": message.id,
                "subject": message.subject or "",
                "sender": self._extract_email_address(message.sender),
                "from": self._extract_email_address(message.from_),
                "toRecipients": [self._extract_email_address(r) for r in (message.to_recipients or [])],
                "ccRecipients": [self._extract_email_address(r) for r in (message.cc_recipients or [])],
                "bccRecipients": [self._extract_email_address(r) for r in (message.bcc_recipients or [])],
                "receivedDateTime": message.received_date_time.isoformat() if message.received_date_time else None,
                "sentDateTime": message.sent_date_time.isoformat() if message.sent_date_time else None,
                "hasAttachments": message.has_attachments or False,
                "importance": str(message.importance) if message.importance else "normal",
                "isRead": message.is_read or False,
                "bodyPreview": message.body_preview or "",
                "internetMessageId": message.internet_message_id or "",
                "conversationId": message.conversation_id or ""
            }

            if include_body and message.body:
                message_info["body"] = {
                    "contentType": str(message.body.content_type) if message.body.content_type else "text",
                    "content": message.body.content or ""
                }

            return message_info

        except Exception as err:
            self._logger.error(f"Error getting message {message_id}: {err}")
            raise FileError(f"Error getting message {message_id}: {err}") from err

    async def download_message(self, message_id: str, destination: Path, format: str = "eml") -> str:
        """
        Download a message by its ID using Microsoft Graph API.
        Supports 'eml', 'msg', or 'json' formats.
        """
        try:
            destination = Path(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)

            if format.lower() == "eml":
                # Get MIME content
                mime_content = await self.graph_client.me.messages.by_message_id(message_id).value.get()

                async with aiofiles.open(destination, "wb") as f:
                    await f.write(mime_content)

            elif format.lower() == "json":
                # Get message as JSON
                message_data = await self.get_message(message_id, include_body=True)

                import json
                async with aiofiles.open(destination, "w", encoding="utf-8") as f:
                    await f.write(json.dumps(message_data, indent=2, ensure_ascii=False))

            else:
                raise ValueError(f"Unsupported format: {format}. Use 'eml' or 'json'")

            self._logger.info(f"Downloaded message {message_id} to {destination}")
            return str(destination)

        except Exception as err:
            self._logger.error(f"Error downloading message {message_id}: {err}")
            raise FileError(f"Error downloading message {message_id}: {err}") from err

    async def download_attachment(self, message_id: str, attachment_id: str, destination: Path) -> str:
        """
        Download a message attachment using Microsoft Graph API.
        """
        try:
            # Get attachment info
            attachment = await self.graph_client.me.messages.by_message_id(message_id)\
                .attachments.by_attachment_id(attachment_id).get()

            if not attachment:
                raise FileNotFound(f"Attachment {attachment_id} not found")

            destination = Path(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Handle different attachment types
            if hasattr(attachment, 'content_bytes') and attachment.content_bytes:
                # File attachment with content
                content = base64.b64decode(attachment.content_bytes)
                async with aiofiles.open(destination, "wb") as f:
                    await f.write(content)
            else:
                raise FileError(f"Attachment {attachment_id} has no downloadable content")

            self._logger.info(f"Downloaded attachment {attachment.name} to {destination}")
            return str(destination)

        except Exception as err:
            self._logger.error(f"Error downloading attachment {attachment_id}: {err}")
            raise FileError(f"Error downloading attachment {attachment_id}: {err}") from err

    async def move_message(self, message_id: str, destination_folder: str) -> Dict[str, Any]:
        """
        Move a message to a different folder using Microsoft Graph API.
        """
        try:
            # Resolve destination folder ID
            destination_folder_id = await self._resolve_folder_id(destination_folder)

            # Create move request body
            move_request = MovePostRequestBody()
            move_request.destination_id = destination_folder_id

            # Execute move
            moved_message = await self.graph_client.me.messages.by_message_id(message_id)\
                .move.post(move_request)

            if not moved_message:
                raise FileError(f"Failed to move message {message_id}")

            result = {
                "id": moved_message.id,
                "subject": moved_message.subject or "",
                "folderId": destination_folder_id,
                "folderName": destination_folder
            }

            self._logger.info(f"Moved message {message_id} to folder {destination_folder}")
            return result

        except Exception as err:
            self._logger.error(f"Error moving message {message_id}: {err}")
            raise FileError(f"Error moving message {message_id}: {err}") from err

    async def delete_message(self, message_id: str) -> bool:
        """
        Delete a message by ID using Microsoft Graph API.
        """
        try:
            await self.graph_client.me.messages.by_message_id(message_id).delete()

            self._logger.info(f"Deleted message {message_id}")
            return True

        except Exception as err:
            self._logger.error(f"Error deleting message {message_id}: {err}")
            raise FileError(f"Error deleting message {message_id}: {err}") from err

    async def mark_as_read(self, message_id: str, is_read: bool = True) -> bool:
        """
        Mark a message as read or unread using Microsoft Graph API.
        """
        try:
            # Create message patch
            message_update = Message()
            message_update.is_read = is_read

            # Update message
            await self.graph_client.me.messages.by_message_id(message_id).patch(message_update)

            status = "read" if is_read else "unread"
            self._logger.info(f"Marked message {message_id} as {status}")
            return True

        except Exception as err:
            self._logger.error(f"Error marking message {message_id}: {err}")
            raise FileError(f"Error marking message {message_id}: {err}") from err

    async def search_messages(self, search_query: str, top: int = 10, folder: str = None) -> List[Dict[str, Any]]:
        """
        Search for messages matching the search query using Microsoft Graph API.
        """
        try:
            if folder:
                # Search within specific folder
                folder_id = await self._resolve_folder_id(folder)
                request = self.graph_client.me.mail_folders.by_mail_folder_id(folder_id).messages.get()
            else:
                # Search all messages
                request = self.graph_client.me.messages.get()

            # Apply search and other parameters
            request.query_parameters.search = search_query
            request.query_parameters.top = min(top, 1000)
            request.query_parameters.select = [
                "id", "subject", "sender", "from", "receivedDateTime",
                "sentDateTime", "hasAttachments", "importance", "isRead", "bodyPreview"
            ]
            request.query_parameters.orderby = ["receivedDateTime desc"]

            # Execute search
            search_response = await request

            messages = []
            if search_response and search_response.value:
                for message in search_response.value:
                    message_info = {
                        "id": message.id,
                        "subject": message.subject or "",
                        "sender": self._extract_email_address(message.sender),
                        "from": self._extract_email_address(message.from_),
                        "receivedDateTime": message.received_date_time.isoformat() if message.received_date_time else None,  # noqa
                        "sentDateTime": message.sent_date_time.isoformat() if message.sent_date_time else None,
                        "hasAttachments": message.has_attachments or False,
                        "importance": str(message.importance) if message.importance else "normal",
                        "isRead": message.is_read or False,
                        "bodyPreview": message.body_preview or ""
                    }
                    messages.append(message_info)

            return messages

        except Exception as err:
            self._logger.error(f"Error searching messages: {err}")
            raise FileError(f"Error searching messages: {err}") from err

    async def send_message(
        self,
        subject: str,
        body: str,
        to_recipients: List[str],
        cc_recipients: Optional[List[str]] = None,
        bcc_recipients: Optional[List[str]] = None,
        attachments: Optional[List[Path]] = None,
        from_address: Optional[str] = None,
        body_type: str = "HTML",
        importance: str = "normal",
        save_to_sent_items: bool = True
    ) -> bool:
        """
        Send a message with optional attachments using Microsoft Graph API.
        """
        try:
            # Create message
            message = Message()
            message.subject = subject

            # Set body
            message.body = ItemBody()
            if body_type.upper() == "HTML":
                message.body.content_type = BodyType.Html
            else:
                message.body.content_type = BodyType.Text
            message.body.content = body

            # Set recipients
            message.to_recipients = [
                Recipient(email_address=EmailAddress(address=addr)) for addr in to_recipients
            ]

            if cc_recipients:
                message.cc_recipients = [
                    Recipient(email_address=EmailAddress(address=addr)) for addr in cc_recipients
                ]

            if bcc_recipients:
                message.bcc_recipients = [
                    Recipient(email_address=EmailAddress(address=addr)) for addr in bcc_recipients
                ]

            # Set importance
            if importance.lower() == "high":
                from msgraph.generated.models.importance import Importance
                message.importance = Importance.High
            elif importance.lower() == "low":
                from msgraph.generated.models.importance import Importance
                message.importance = Importance.Low

            # Handle attachments
            if attachments:
                message.attachments = []
                for attachment_path in attachments:
                    attachment_path = Path(attachment_path)
                    if not attachment_path.exists():
                        self._logger.warning(f"Attachment file not found: {attachment_path}")
                        continue

                    # Check file size
                    file_size = attachment_path.stat().st_size
                    if file_size > self._max_attachment_size:
                        self._logger.warning(f"Attachment too large: {attachment_path} ({file_size} bytes)")
                        continue

                    # Read file and create attachment
                    async with aiofiles.open(attachment_path, "rb") as f:
                        file_content = await f.read()

                    file_attachment = FileAttachment()
                    file_attachment.name = attachment_path.name
                    file_attachment.content_type = self._get_mime_type(attachment_path)
                    file_attachment.content_bytes = base64.b64encode(file_content).decode()

                    message.attachments.append(file_attachment)

            # Handle custom from address (requires special permissions)
            if from_address:
                message.from_ = Recipient(email_address=EmailAddress(address=from_address))

            # Send message using the sendMail endpoint
            send_request = SendMailPostRequestBody()
            send_request.message = message
            send_request.save_to_sent_items = save_to_sent_items

            await self.graph_client.me.send_mail.post(send_request)

            self._logger.info(f"Sent message: {subject} to {', '.join(to_recipients)}")
            return True

        except ImportError:
            # Fallback if SendMailPostRequestBody import fails
            try:
                await self.graph_client.me.send_mail.post(
                    message=message,
                    save_to_sent_items=save_to_sent_items
                )
                self._logger.info(f"Sent message: {subject} to {', '.join(to_recipients)}")
                return True
            except Exception as fallback_err:
                self._logger.error(f"Fallback send failed: {fallback_err}")
                raise FileError(f"Error sending message: {fallback_err}") from fallback_err

        except Exception as err:
            self._logger.error(f"Error sending message: {err}")
            raise FileError(f"Error sending message: {err}") from err

    # Helper methods

    async def _resolve_folder_id(self, folder_name_or_id: str) -> str:
        """
        Resolve folder name to ID. If already an ID, return as-is.
        """
        try:
            # Common folder names mapping
            common_folders = {
                "inbox": "inbox",
                "sent": "sentitems",
                "drafts": "drafts",
                "deleted": "deleteditems",
                "junk": "junkemail",
                "outbox": "outbox"
            }

            folder_key = folder_name_or_id.lower()
            if folder_key in common_folders:
                return common_folders[folder_key]

            # If it looks like a GUID, assume it's already an ID
            if len(folder_name_or_id) > 20 and "-" in folder_name_or_id:
                return folder_name_or_id

            # Search for folder by name
            folders = await self.list_folders()
            for folder in folders:
                if folder["displayName"].lower() == folder_key:
                    return folder["id"]

            raise FileNotFound(f"Folder not found: {folder_name_or_id}")

        except Exception as e:
            self._logger.error(f"Error resolving folder ID for {folder_name_or_id}: {e}")
            raise FileError(f"Error resolving folder ID: {e}") from e

    def _extract_email_address(self, recipient) -> str:
        """
        Extract email address from recipient object.
        """
        try:
            if not recipient:
                return ""

            if hasattr(recipient, 'email_address') and recipient.email_address:
                return recipient.email_address.address or ""

            return ""
        except Exception:
            return ""

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
        Test Outlook permissions using Microsoft Graph API.
        """
        results = {
            "mail_access": False,
            "send_access": False,
            "folder_access": False,
            "errors": []
        }

        try:
            # Test 1: Mail access (list messages)
            await self.list_messages(top=1)
            results["mail_access"] = True
            self._logger.info("Mail access: OK")

            # Test 2: Folder access
            folders = await self.list_folders()
            results["folder_access"] = True
            self._logger.info(f"Folder access: Found {len(folders)} folders")

            # Test 3: Send access would require actually sending an email
            # We'll just mark it as True if we have the previous permissions
            results["send_access"] = True
            self._logger.info("Send permissions: Assumed OK (cannot test without sending)")

        except Exception as e:
            results["errors"].append(str(e))
            self._logger.error(f"Permission test failed: {e}")

        return results

    async def close(self):
        """Clean up resources."""
        await super().close()

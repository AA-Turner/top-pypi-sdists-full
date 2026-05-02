
from typing import Type
from datetime import datetime
from zoneinfo import ZoneInfo

from bson import ObjectId
from letschatty.models.utils.types import StrObjectId
from ....models.utils import MessageType, Status
from ....models.messages import ChattyMessage, TextMessage, ImageMessage, VideoMessage, DocumentMessage, StickerMessage, AudioMessage, ContactMessage, LocationMessage, CentralNotification, ReactionMessage
from ....models.messages.chatty_messages.schema import ChattyContentText, ChattyContentImage, ChattyContentVideo, ChattyContentDocument, ChattyContentSticker, ChattyContentAudio, ChattyContentContacts, ChattyContentLocation, ChattyContentCentral, ChattyContentReaction, ChattyContent, ChattyContext
from ....models.messages.chatty_messages.base.message_draft import MessageDraft

class fromMessageDraftFactory:
    """This factory takes a message request and instantiates the corresponding ChattyMessage"""
    @staticmethod
    def from_draft(message: MessageDraft, sent_by: StrObjectId) -> ChattyMessage:
        match message.type:
            case MessageType.TEXT.value:
                return fromMessageDraftFactory.instance_text_message(message, sent_by)
            case MessageType.IMAGE.value:
                return fromMessageDraftFactory.instance_image_message(message, sent_by)
            case MessageType.VIDEO.value:
                return fromMessageDraftFactory.instance_video_message(message, sent_by)
            case MessageType.DOCUMENT.value:
                return fromMessageDraftFactory.instance_document_message(message, sent_by)
            case MessageType.AUDIO.value:
                return fromMessageDraftFactory.instance_audio_message(message, sent_by)
            case MessageType.STICKER.value:
                return fromMessageDraftFactory.instance_sticker_message(message, sent_by)
            case MessageType.CONTACT.value:
                return fromMessageDraftFactory.instance_contact_message(message, sent_by)
            case MessageType.LOCATION.value:
                return fromMessageDraftFactory.instance_location_message(message, sent_by)
            case MessageType.CENTRAL.value:
                return fromMessageDraftFactory.instance_central_notification(message, sent_by)
            case MessageType.REACTION.value:
                return fromMessageDraftFactory.instance_reaction_message(message, sent_by)
            case _:
                raise ValueError(f"Invalid message type: {message.type} - valid types: {MessageType.values()}")

    @staticmethod
    def instance_text_message(message: MessageDraft, sent_by: StrObjectId) -> TextMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=TextMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_image_message(message: MessageDraft, sent_by: StrObjectId) -> ImageMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=ImageMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_video_message(message: MessageDraft, sent_by: StrObjectId) -> VideoMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=VideoMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_document_message(message: MessageDraft, sent_by: StrObjectId) -> DocumentMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=DocumentMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_audio_message(message: MessageDraft, sent_by: StrObjectId) -> AudioMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=AudioMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_sticker_message(message: MessageDraft, sent_by: StrObjectId) -> StickerMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=StickerMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_contact_message(message: MessageDraft, sent_by: StrObjectId) -> ContactMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=ContactMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_location_message(message: MessageDraft, sent_by: StrObjectId) -> LocationMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=LocationMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_central_notification(message: MessageDraft, sent_by: StrObjectId) -> CentralNotification:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=CentralNotification, sent_by=sent_by) #type: ignore

    @staticmethod
    def instance_reaction_message(message: MessageDraft, sent_by: StrObjectId) -> ReactionMessage:
        return fromMessageDraftFactory.instantiate_message(message=message, message_type=ReactionMessage, sent_by=sent_by) #type: ignore

    @staticmethod
    def instantiate_message(message: MessageDraft, message_type: Type[ChattyMessage], sent_by: StrObjectId) -> ChattyMessage:
        return message_type(
            id=str(ObjectId()),
            created_at=datetime.now(tz=ZoneInfo("UTC")),
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
            content=message.content,#type: ignore
            status=Status.WAITING,
            is_incoming_message=False,
            context=message.context,#type: ignore
            sent_by=sent_by,
            subtype=message.subtype#type: ignore
        )

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from ....models.utils import MessageType
from ....models.messages.chatty_messages.schema import ChattyContent, ChattyContentImage, ChattyContentVideo, ChattyContentDocument, ChattyContentAudio, ChattyContentSticker, ChattyContentLocation, ChattyContentContacts, ChattyContentReaction, ChattyContentText, ChattyContentCentral, ChattyContentInteractive, ChattyContentButton
from ....models.messages import ChattyMessage, AudioMessage, DocumentMessage, ImageMessage, LocationMessage, StickerMessage, TextMessage, VideoMessage, ReactionMessage, CentralNotification, ContactMessage, InteractiveMessage, ButtonMessage

if TYPE_CHECKING:
    from ....models.messages import ChattyMessageJson

class JsonMessageFactory:
    """This factory takes a ChattyMessageJson (database message model) and instantiates the corresponding ChattyMessage"""
    @staticmethod
    def from_json(message_json : ChattyMessageJson) -> ChattyMessage:
        return JsonMessageFactory.match_and_instantiate(message_json)

    @staticmethod
    def match_and_instantiate(message_json : ChattyMessageJson) -> ChattyMessage:

        match message_json.type:
            case MessageType.TEXT:
                return JsonMessageFactory.generate_text_message(message_json)
            case MessageType.IMAGE:
                return JsonMessageFactory.generate_image_message(message_json)
            case MessageType.VIDEO:
                return JsonMessageFactory.generate_video_message(message_json)
            case MessageType.DOCUMENT:
                return JsonMessageFactory.generate_document_message(message_json)
            case MessageType.AUDIO:
                return JsonMessageFactory.generate_audio_message(message_json)
            case MessageType.STICKER:
                return JsonMessageFactory.generate_sticker_message(message_json)
            case MessageType.LOCATION:
                return JsonMessageFactory.generate_location_message(message_json)
            case MessageType.CONTACT:
                return JsonMessageFactory.generate_contact_message(message_json)
            case MessageType.CENTRAL:
                return JsonMessageFactory.generate_central_notification(message_json)
            case MessageType.REACTION:
                return JsonMessageFactory.generate_reaction_message(message_json)
            case MessageType.INTERACTIVE:
                return JsonMessageFactory.generate_interactive_message(message_json)
            case MessageType.BUTTON:
                return JsonMessageFactory.generate_button_message(message_json)
            case _:
                 raise ValueError(f"Message type {message_json.type} not supported - valid types: {MessageType.values()}")

    @staticmethod
    def instantiate_message(tp: type[ChattyMessage], message_json: ChattyMessageJson, chatty_content: ChattyContent) -> ChattyMessage:
        return tp(
        id=message_json.id,
        created_at=message_json.created_at,
        updated_at=message_json.updated_at,
        content=chatty_content,
        status=message_json.status if message_json.status is not None else "READ",
        is_incoming_message=message_json.is_incoming_message,
        sent_by=message_json.sent_by,
        referral=message_json.referral,
        subtype=message_json.subtype,
        context=message_json.context
        )

    @staticmethod
    def generate_button_message(message_json : ChattyMessageJson) -> ButtonMessage:
        chatty_content = ChattyContentButton(**message_json.content)
        return JsonMessageFactory.instantiate_message(ButtonMessage, message_json, chatty_content)

    @staticmethod
    def generate_reaction_message(message_json : ChattyMessageJson) -> ReactionMessage:
        chatty_content = ChattyContentReaction(**message_json.content)
        return JsonMessageFactory.instantiate_message(ReactionMessage, message_json, chatty_content)

    @staticmethod
    def generate_text_message(message_json : ChattyMessageJson) -> TextMessage:
        chatty_content = ChattyContentText(**message_json.content)
        return JsonMessageFactory.instantiate_message(TextMessage, message_json, chatty_content)

    @staticmethod
    def generate_image_message(message_json : ChattyMessageJson) -> ImageMessage:
        chatty_content = ChattyContentImage(**message_json.content)
        return JsonMessageFactory.instantiate_message(ImageMessage, message_json, chatty_content)

    @staticmethod
    def generate_video_message(message_json : ChattyMessageJson) -> VideoMessage:
        chatty_content = ChattyContentVideo(**message_json.content)
        return JsonMessageFactory.instantiate_message(VideoMessage, message_json, chatty_content)
    @staticmethod
    def generate_document_message(message_json : ChattyMessageJson) -> DocumentMessage:
        chatty_content = ChattyContentDocument(**message_json.content)
        return JsonMessageFactory.instantiate_message(DocumentMessage, message_json, chatty_content)

    @staticmethod
    def generate_audio_message(message_json : ChattyMessageJson) -> AudioMessage:
        chatty_content = ChattyContentAudio(**message_json.content)
        return JsonMessageFactory.instantiate_message(AudioMessage, message_json, chatty_content)

    @staticmethod
    def generate_sticker_message(message_json : ChattyMessageJson) -> StickerMessage:
        chatty_content = ChattyContentSticker(**message_json.content)
        return JsonMessageFactory.instantiate_message(StickerMessage, message_json, chatty_content)

    @staticmethod
    def generate_location_message(message_json : ChattyMessageJson) -> LocationMessage:
        chatty_content = ChattyContentLocation(**message_json.content)
        return JsonMessageFactory.instantiate_message(LocationMessage, message_json, chatty_content)

    @staticmethod
    def generate_contact_message(message_json : ChattyMessageJson) -> ContactMessage:
        chatty_content = ChattyContentContacts(**message_json.content)
        return JsonMessageFactory.instantiate_message(ContactMessage, message_json, chatty_content)

    @staticmethod
    def generate_central_notification(message_json : ChattyMessageJson) -> CentralNotification:
        chatty_content = ChattyContentCentral(**message_json.content)
        return JsonMessageFactory.instantiate_message(CentralNotification, message_json, chatty_content)

    @staticmethod
    def generate_interactive_message(message_json : ChattyMessageJson) -> InteractiveMessage:
        chatty_content = ChattyContentInteractive(**message_json.content)
        return JsonMessageFactory.instantiate_message(InteractiveMessage, message_json, chatty_content)


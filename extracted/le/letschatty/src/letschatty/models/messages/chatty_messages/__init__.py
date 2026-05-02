from typing import Union, TypeAlias
from .audio import AudioMessage
from .document import DocumentMessage
from .image import ImageMessage
from .location import LocationMessage
from .sticker import StickerMessage
from .text import TextMessage
from .video import VideoMessage
from .reaction import ReactionMessage
from .central_notification import CentralNotification
from .contact import ContactMessage
from .base import ChattyMessageJson, MessageDraft, SendMessagesFromAgentToChat
from .interactive import InteractiveMessage
from .button import ButtonMessage
from .schema.chatty_content.content_central import CentralNotificationStatus

ChattyMessage : TypeAlias = Union[AudioMessage, DocumentMessage, ImageMessage, LocationMessage, StickerMessage, TextMessage, VideoMessage, ReactionMessage, CentralNotification, ContactMessage, ButtonMessage]
ChattyMediaMessage : TypeAlias = Union[AudioMessage, ImageMessage, VideoMessage, StickerMessage, DocumentMessage]

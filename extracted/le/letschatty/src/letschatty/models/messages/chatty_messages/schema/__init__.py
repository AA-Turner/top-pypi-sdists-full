from typing import TypeAlias, Union
from .chatty_content.content_image import ChattyContentImage
from .chatty_content.content_text import ChattyContentText
from .chatty_content.content_video import ChattyContentVideo
from .chatty_content.content_audio import ChattyContentAudio
from .chatty_content.content_reaction import ChattyContentReaction
from .chatty_content.content_location import ChattyContentLocation
from .chatty_content.content_contacts import ChattyContentContacts
from .chatty_content.content_document import ChattyContentDocument
from .chatty_content.content_sticker import ChattyContentSticker
from .chatty_content.content_central import ChattyContentCentral
from .chatty_content.content_interactive import ChattyContentInteractive
from .chatty_content.content_button import ChattyContentButton
from .chatty_context.chatty_context import ChattyContext
from .chatty_referal.chatty_referal import ChattyReferral


ChattyContent : TypeAlias = Union[ChattyContentImage, ChattyContentText, ChattyContentVideo, ChattyContentAudio, ChattyContentReaction, ChattyContentLocation, ChattyContentContacts, ChattyContentDocument, ChattyContentSticker, ChattyContentCentral, ChattyContentInteractive, ChattyContentButton]


from ...models.messages.chatty_messages.schema import ChattyContent, ChattyContentText, ChattyContentContacts, ChattyContentLocation, ChattyContentImage, ChattyContentVideo, ChattyContentAudio, ChattyContentDocument, ChattyContentSticker, ChattyContentReaction
class MessageTextOrCaptionOrPreview:
    @staticmethod
    def get_content_preview(message_content: ChattyContent) -> str:
        if isinstance(message_content, ChattyContentText):
            return message_content.body
        elif isinstance(message_content, ChattyContentContacts):
            return "👥 Mensaje de tipo contacto"
        elif isinstance(message_content, ChattyContentLocation):
            return "📍 Mensaje de tipo ubicación"
        elif isinstance(message_content, ChattyContentImage):
            return "🖼️ Mensaje de tipo imagen"
        elif isinstance(message_content, ChattyContentVideo):
            return "🎥 Mensaje de tipo video"
        elif isinstance(message_content, ChattyContentAudio):
            return "🔊 Mensaje de tipo audio"
        elif isinstance(message_content, ChattyContentDocument):
            return "📄 Mensaje de tipo documento"
        elif isinstance(message_content, ChattyContentSticker):
            return "😀 Mensaje de tipo sticker"
        elif isinstance(message_content, ChattyContentReaction):
            return "❤️ Mensaje de tipo reacción"
        else:

            return "Vista previa del mensaje"

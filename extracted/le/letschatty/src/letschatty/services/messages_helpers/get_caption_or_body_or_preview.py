from ...models.messages.chatty_messages.schema import ChattyContent, ChattyContentButton, ChattyContentText, ChattyContentContacts, ChattyContentLocation, ChattyContentImage, ChattyContentVideo, ChattyContentAudio, ChattyContentDocument, ChattyContentSticker, ChattyContentReaction
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
        elif isinstance(message_content, ChattyContentAudio) and not message_content.transcription:
            return "🔊 Mensaje de tipo audio"
        elif isinstance(message_content, ChattyContentAudio) and message_content.transcription:
            return "🔊 Audio: " + message_content.transcription
        elif isinstance(message_content, ChattyContentDocument):
            return "📄 Mensaje de tipo documento"
        elif isinstance(message_content, ChattyContentSticker):
            return "😀 Mensaje de tipo sticker"
        elif isinstance(message_content, ChattyContentReaction):
            if message_content.emoji:
                return f"❤️ Reaccionó con {message_content.emoji}"
            return "❌ Quitó su reacción"
        elif isinstance(message_content, ChattyContentButton):
            return "🔗 Botón: " + message_content.payload
        else:

            return "Vista previa del mensaje"

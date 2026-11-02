from datetime import datetime
from typing import Optional

from letschatty.models.utils.types import StrObjectId
from ....models.utils import Status, MessageSubtype
from ....models.messages import TextMessage
from ....models.messages.chatty_messages import DocumentMessage, ImageMessage, VideoMessage
from ....models.messages.chatty_messages.base.message_base import Message
from ....models.messages.chatty_messages.schema import (
    ChattyContentDocument,
    ChattyContentImage,
    ChattyContentText,
    ChattyContentVideo,
    ChattyContext,
)
from ....models.messages.chatty_messages.schema.chatty_context.template_rendering import TemplateRendering
from ....models.messages.message_templates.header_media import TemplateHeaderKind, TemplateHeaderMedia

# Qué mensaje representa a cada tipo de encabezado. Una plantilla con encabezado multimedia es, para
# quien la recibe, un archivo con texto debajo — exactamente un mensaje de media con caption, que es
# algo que Chatty ya sabe guardar y mostrar.
_MEDIA_MESSAGE_BY_KIND = {
    TemplateHeaderKind.IMAGE: (ImageMessage, ChattyContentImage),
    TemplateHeaderKind.VIDEO: (VideoMessage, ChattyContentVideo),
    TemplateHeaderKind.DOCUMENT: (DocumentMessage, ChattyContentDocument),
}


class fromTemplateFactory:
    """This factory takes a message request and instantiates the corresponding ChattyMessage"""

    @staticmethod
    def from_template(message_id: str, body: str, template_name: str, campaign_id: Optional[str], creator_id: StrObjectId, created_at: datetime, updated_at: datetime, status: Status, continuous_conversation_id: Optional[StrObjectId] = None, meta_template_id: Optional[str] = None, header_media: Optional[TemplateHeaderMedia] = None, rendering: Optional[TemplateRendering] = None) -> Message:
        return fromTemplateFactory.instantiate_message(message_id=message_id, body=body, template_name=template_name, campaign_id=campaign_id, creator_id=creator_id, created_at=created_at, updated_at=updated_at, status=status, continuous_conversation_id=continuous_conversation_id, meta_template_id=meta_template_id, header_media=header_media, rendering=rendering)

    @staticmethod
    def instantiate_message(message_id: str, body: str, template_name: str, campaign_id: str | None, creator_id: StrObjectId, created_at: datetime, updated_at: datetime, status: Status, continuous_conversation_id: Optional[StrObjectId] = None, meta_template_id: Optional[str] = None, header_media: Optional[TemplateHeaderMedia] = None, rendering: Optional[TemplateRendering] = None) -> Message:
        """El mensaje que queda guardado en el chat por una plantilla enviada.

        Si la plantilla lleva encabezado multimedia, se guarda como **mensaje de media con caption**:
        el archivo arriba y el cuerpo debajo, que es lo que realmente recibió el cliente. Antes se
        guardaba sólo el texto, así que en el chat aparecía como un mensaje suelto y la imagen no
        estaba en ningún lado.

        El `subtype` sigue siendo TEMPLATE en los dos casos — de ahí sale `is_template_message`, así que
        cambiar el tipo del mensaje no afecta la detección de plantillas ni el "ya se envió esta".

        La `url` que llega acá tiene que ser NUESTRA (S3), no la del CDN de Meta: esa caduca y el chat
        quedaría con una imagen rota a los 30 días.
        """
        context = ChattyContext(
            template_name=template_name,
            campaign_id=campaign_id,
            continuous_conversation_id=continuous_conversation_id,
            meta_template_id=meta_template_id,
        )
        # Encabezado de texto, pie y botones: lo que el cliente vio además del cuerpo. Sólo se setea si
        # hay algo, así una plantilla de cuerpo solo guarda exactamente lo mismo que antes.
        if rendering is not None and not rendering.is_empty:
            context.template_rendering = rendering
        common = dict(
            id=message_id, created_at=created_at, updated_at=updated_at, status=status,
            is_incoming_message=False, context=context, sent_by=creator_id,
            subtype=MessageSubtype.TEMPLATE,
        )

        media_classes = _MEDIA_MESSAGE_BY_KIND.get(header_media.kind) if header_media else None
        if media_classes is None or not header_media.url:
            # Plantilla de sólo texto (o sin archivo resuelto): el mensaje de siempre, sin cambios.
            return TextMessage(content=ChattyContentText(body=body), **common)

        message_cls, content_cls = media_classes
        return message_cls(
            content=content_cls(
                url=header_media.url,
                caption=body,
                mime_type=header_media.mime_type,
                filename=header_media.filename,
            ),
            **common,
        )

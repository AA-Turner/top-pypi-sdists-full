from typing import Annotated, TypeAlias, Union
from pydantic import Discriminator, Tag
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
from ...utils.types.message_types import MessageType

# ⚠️ TODO tipo de mensaje instanciable DEBE estar en este mapa: es el tipo de
# Chat.messages, así que un mensaje cuya clase no figure acá se resuelve por el
# camino permisivo de abajo en vez de por su clase real. InteractiveMessage
# faltó durante años sin romper nada porque nunca se instanciaba (INTERACTIVE
# era uncontrolled); al volverse un mensaje real (0.4.523), el primer nfm_reply
# tiraba el chat. El test de regresión vive en test_interactive_content.py
# (round-trip por ChatFactory, no sólo por JsonMessageFactory).
_CLASE_POR_TIPO = {
    MessageType.AUDIO: AudioMessage,
    MessageType.DOCUMENT: DocumentMessage,
    MessageType.IMAGE: ImageMessage,
    MessageType.LOCATION: LocationMessage,
    MessageType.STICKER: StickerMessage,
    MessageType.TEXT: TextMessage,
    MessageType.VIDEO: VideoMessage,
    MessageType.REACTION: ReactionMessage,
    MessageType.CENTRAL: CentralNotification,
    MessageType.CONTACT: ContactMessage,
    MessageType.BUTTON: ButtonMessage,
    MessageType.INTERACTIVE: InteractiveMessage,
}

#: La unión de siempre, sin discriminar: pydantic prueba rama por rama y se queda
#: con la PRIMERA que valide.
#:
#: Se mantiene como `ChattyMessage` —el nombre público— por dos razones concretas:
#: `isinstance(x, ChattyMessage)` (lo usa `chatty_message_factory`) y
#: `typing.get_args(ChattyMessage)` sólo funcionan sobre una Union PLANA; sobre un
#: `Annotated[...]` el primero tira `TypeError: Subscripted generics cannot be used
#: with class and instance checks`. Además es la red del discriminador para un
#: `type` sin clase — ver `_tag_por_tipo`.
ChattyMessage: TypeAlias = Union[
    AudioMessage, DocumentMessage, ImageMessage, LocationMessage, StickerMessage,
    TextMessage, VideoMessage, ReactionMessage, CentralNotification, ContactMessage,
    ButtonMessage, InteractiveMessage,
]

_SIN_CLASE = "__sin_clase__"


def _tag_por_tipo(value) -> str:
    """Rutea un mensaje a SU clase usando el campo `type`.

    Sin esto la unión resolvía por orden de declaración, y como
    `ChattyContentDocument` hereda de `ChattyContentMedia` con todos sus campos
    opcionales (`filename` incluido), aceptaba también la forma de una imagen, un
    video o un sticker. `DocumentMessage` iba antes que los tres, así que los tres
    volvían de Mongo como `DocumentMessage`: el dato guardado decía `sticker` y la
    relectura devolvía un documento. El síntoma visible era la preview del inbox
    ("📄 Mensaje de tipo documento" sobre una imagen), porque
    `MessageTextOrCaptionOrPreview` decide por la CLASE del content, no por `type`.

    Un `type` que no tenga clase cae en `ChattyMessage` (la unión plana), que es exactamente el
    comportamiento anterior: el arreglo no puede dejar peor a ningún documento ya
    guardado, ni rechazar un chat entero por un mensaje raro — que es el modo de
    falla que este archivo ya advertía arriba.
    """
    tipo = value.get("type") if isinstance(value, dict) else getattr(value, "type", None)
    try:
        tipo = MessageType(tipo)
    except ValueError:
        return _SIN_CLASE
    return str(tipo.value) if tipo in _CLASE_POR_TIPO else _SIN_CLASE


#: EL TIPO QUE VA EN LOS CAMPOS PYDANTIC que se validan desde datos crudos
#: (`Chat.messages`, `ChatPreview.last_message`, `TemporaryChat.messages`).
#: Para anotar variables, argumentos y retornos usá `ChattyMessage`, que es la unión
#: plana: son el mismo conjunto de clases, pero sólo ésta lleva el discriminador.
ChattyMessageField: TypeAlias = Annotated[
    Union[tuple(
        [Annotated[clase, Tag(str(tipo.value))] for tipo, clase in _CLASE_POR_TIPO.items()]
        + [Annotated[ChattyMessage, Tag(_SIN_CLASE)]]
    )],
    Discriminator(_tag_por_tipo),
]

ChattyMediaMessage : TypeAlias = Union[AudioMessage, ImageMessage, VideoMessage, StickerMessage, DocumentMessage]

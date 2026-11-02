from typing import Union
from .text_content import MetaTextContent
from .multimedia_content import MetaImageContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaStickerContent
from .location_content import MetaLocationContent
from .contacts_content import MetaContactContent
from .system_content import MetaSystemContent
from .interactive_content import MetaInteractiveContent
from .button_content import MetaButtonContent
from .order_content import MetaOrderContent
from .reaction_content import MetaReactionContent

MetaContent = Union[MetaTextContent, MetaImageContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaStickerContent, MetaLocationContent, MetaContactContent, MetaSystemContent, MetaInteractiveContent, MetaButtonContent, MetaOrderContent, MetaReactionContent]
MetaMediaContent = Union[MetaImageContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaStickerContent]
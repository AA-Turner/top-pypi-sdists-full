"""Cómo le llegó una plantilla al cliente, más allá del cuerpo.

Una plantilla enviada se guarda como un mensaje de texto (o de media con caption) con el cuerpo ya
completado. El encabezado de texto, el pie y los botones se perdían: en el chat la plantilla se veía
como un texto suelto, sin los botones que el cliente sí recibió. Esto es lo que faltaba, congelado
al momento del envío — no se vuelve a leer la plantilla después, porque puede editarse o borrarse y
el chat tiene que mostrar lo que se MANDÓ.

Vive en `ChattyContext` (como `edited_at`) para que viaje con el mensaje a Mongo, al frontend y al
evento `chat.message.sent` sin tocar ninguna lista de campos, y sirve para cualquier tipo de mensaje
(texto, imagen, video, documento).

Sin dependencias a propósito: lo importa `ChattyContext`, y traerlo desde `message_templates` cargaría
ese paquete entero (campañas, chats) adentro del modelo del mensaje.
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class TemplateRenderedButton(BaseModel):
    """Un botón tal como lo vio el cliente. Se dibuja inerte: los botones los toca el cliente.

    `type` es texto y no el enum de Meta a propósito: un tipo de botón nuevo no puede impedir que se
    guarde el mensaje (un mensaje que no valida tira el chat entero).
    """

    type: str
    text: Optional[str] = None
    # URL: el enlace final, con el sufijo ya completado. Sin completar queda el `{{1}}` de la plantilla.
    url: Optional[str] = None
    phone_number: Optional[str] = None
    # COPY_CODE: el código que se mandó.
    code: Optional[str] = None


class TemplateRendering(BaseModel):
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    buttons: List[TemplateRenderedButton] = Field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.header_text or self.footer_text or self.buttons)

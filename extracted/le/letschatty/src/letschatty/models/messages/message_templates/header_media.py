from __future__ import annotations
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    # Sólo para tipar. En tiempo de ejecución no se importa, así que `raw_meta_template` puede importar
    # este módulo sin generar un ciclo — y la enum de allá sigue siendo la única fuente de los formatos.
    from .raw_meta_template import HeaderFormat


class TemplateHeaderKind(StrEnum):
    """Formatos de encabezado multimedia que Chatty sabe enviar.

    El valor es literalmente el que Meta espera en el payload (`{"type": "image", ...}`), en minúscula,
    así que nunca hay que mapearlo de nuevo al serializar.

    LOCATION queda deliberadamente afuera: su parámetro no es un archivo sino latitud/longitud/nombre/
    dirección, o sea otro modelo y otra UI. Un encabezado de TEXTO tampoco entra acá — o no lleva
    parámetro (texto fijo) o lleva uno de tipo texto, que es otro caso.
    """

    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"

    @classmethod
    def from_header_format(cls, header_format: HeaderFormat | str | None) -> Optional[TemplateHeaderKind]:
        """Traduce el `format` del encabezado que devuelve Meta (IMAGE/VIDEO/…) al kind del payload.

        Devuelve `None` cuando el encabezado NO es multimedia (TEXT, LOCATION) o cuando el formato es
        uno que no manejamos. Esa respuesta `None` es la que usa el builder para decidir si el
        componente `header` corresponde: así un formato nuevo de Meta nunca genera un payload roto,
        simplemente no arma el componente.
        """
        if header_format is None:
            return None
        try:
            return cls(str(header_format).lower())
        except ValueError:
            return None


class TemplateHeaderMedia(BaseModel):
    """El archivo que viaja en el encabezado de una plantilla, en UN envío concreto.

    Meta trata el multimedia del encabezado como un **parámetro**: el archivo que se sube al crear la
    plantilla es sólo un ejemplo para que el revisor apruebe, así que **cada envío tiene que traer el
    suyo**. Por eso esto vive en los datos del envío (`FilledTemplateData`) y no en la plantilla.

    `url` + `mime_type` es lo que manda el cliente: un archivo ya subido a nuestro S3, exactamente la
    misma referencia que usa un mensaje de media normal.

    `media_id` lo completa api-chatty resolviéndolo contra Meta justo antes de armar el payload. El
    paquete no hace I/O — no baja de S3 ni habla con Meta —, así que lo recibe ya resuelto. Si llega
    vacío, el builder falla ruidosamente en vez de mandar un payload incompleto.
    """

    kind: TemplateHeaderKind
    url: str = Field(description="URL del archivo en nuestro S3")
    mime_type: str
    filename: Optional[str] = Field(
        default=None,
        description="Nombre visible del archivo. Meta sólo lo usa en los DOCUMENT.",
    )
    media_id: Optional[str] = Field(
        default=None,
        description="Id de Meta, resuelto por api-chatty. El paquete sólo lo lee.",
    )

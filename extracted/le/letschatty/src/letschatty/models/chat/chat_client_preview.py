from typing import Any, ClassVar, Dict, Optional, Tuple

from pydantic import BaseModel, Field

from .marcas_de_meta import MarcaDeMeta
from .no_contactar import NoContactar


class ChatClientPreview(BaseModel):
    """La persona como la muestra, la busca y la filtra la bandeja.

    Es una copia de los campos de `clients` que necesita la bandeja y nada más: la persona
    completa (email, documento, datos de formularios) vive en `clients` y se lee aparte. La
    escribe `ClientCollection` en la misma operación que la persona, en todos sus chats
    (fan-out); el guardado entero de un chat nunca la toca.

    `user_id` (el BSUID) está acá aunque la bandeja no lo muestre porque es con lo que se le
    escribe a un contacto que no muestra el teléfono: sin él, enviar a ese chat necesitaría
    otra lectura. `no_contactar` está porque las audiencias y la bandeja filtran los chats por él
    (`client.no_contactar`): sin la copia, filtrar necesitaría unir con `clients`. `marcas_de_meta`, por
    lo mismo (`client.marcas_de_meta.<tipo>.vence`; ver `marcas_de_meta.py`).
    """

    #: Los campos que se copian de `clients` al chat. Es la lista del fan-out.
    FIELDS: ClassVar[Tuple[str, ...]] = ("name", "waid", "user_id", "username", "country", "no_contactar", "marcas_de_meta")

    name: str = Field(default="")
    waid: Optional[str] = Field(default=None, description="Teléfono de WhatsApp")
    user_id: Optional[str] = Field(default=None, description="BSUID: identidad cuando no hay teléfono")
    username: Optional[str] = Field(default=None, description="Alias de WhatsApp. Sólo para mostrar; nunca es clave")
    country: Optional[str] = Field(default=None)
    no_contactar: Optional[NoContactar] = Field(default=None, frozen=True, description="Copia del de la persona. None = se lo puede contactar")
    marcas_de_meta: Dict[str, MarcaDeMeta] = Field(default_factory=dict, frozen=True, description="Copia de las de la persona (por tipo). Vencidas no valen")

    @property
    def se_puede_contactar(self) -> bool:
        return self.no_contactar is None

    def to_document(self) -> Dict[str, Any]:
        """Como va a Mongo: fechas como fecha y sin `no_contactar` si no está marcado (las audiencias
        cuentan «marcado» como «existe y no es null», y un índice parcial por `$exists` lo incluiría)."""
        document = self.model_dump()
        if self.no_contactar is None:
            document.pop("no_contactar", None)
        if not self.marcas_de_meta:
            document.pop("marcas_de_meta", None)
        return document

    def get_identity(self) -> Optional[str]:
        """Con qué se le escribe: el teléfono si lo hay, si no el BSUID."""
        return self.waid or self.user_id

    def get_waid(self) -> Optional[str]:
        return self.waid

    def get_user_id(self) -> Optional[str]:
        return self.user_id

    def get_name(self) -> str:
        return self.name

    def get_country(self) -> Optional[str]:
        return self.country

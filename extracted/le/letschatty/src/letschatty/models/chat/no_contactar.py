from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator


class NoContactar(BaseModel):
    """«No contactar» (plan 9 del flujo de atención): el contacto pidió que no le escribamos.

    Es del CONTACTO y para siempre: si escribe se le contesta, pero queda afuera de todo lo que sale
    por iniciativa nuestra — seguimientos (fijos y de IA), campañas, audiencias, plantillas y
    reactivaciones. Distinto de «bloqueado» (`Area.BLOCKED`: spam/abuso, no se le contesta ni se
    notifica), que sigue igual. Se marca a mano desde el chat; detectarlo solo queda para después.

    Desde 0.5 vive en la persona (`clients.no_contactar`) y en la preview de cada uno de sus chats
    (`chats.client.no_contactar`), que es lo que filtran las audiencias y la bandeja. Lo escribe SÓLO
    `ClientCollection.set_no_contactar`, que actualiza la persona y todos sus chats en la misma pasada
    y, al desmarcar, borra la clave (no la deja en null). Frozen en `Client` y en la preview, para que
    nadie lo cambie en memoria y espere que un guardado lo lleve.
    """

    desde: datetime = Field(description="Cuándo se marcó (UTC)")
    por: Optional[str] = Field(
        default=None,
        description="Id de quien lo marcó (un usuario; texto libre para no romper si lo marca un sistema)",
    )
    motivo: Optional[str] = Field(default=None, description="Por qué, si lo dijeron")

    @field_validator("desde")
    @classmethod
    def _en_utc(cls, valor: datetime) -> datetime:
        # Mongo devuelve fechas sin zona (en UTC): compararlas con una con zona explota.
        return valor if valor.tzinfo else valor.replace(tzinfo=ZoneInfo("UTC"))

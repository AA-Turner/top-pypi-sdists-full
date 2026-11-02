"""El motivo actual de un chat: cuál es, cuándo se le asignó y cómo se decidió.

Lo escribe SÓLO api-chatty —el camino de atención de la entrada, empresas con la beta
`flujo_de_atencion`— con un `$set` de `motivo`, nunca guardando el chat entero: por eso
`Chat.motivo` es frozen, como `proximo_recordatorio_at` y los contadores de seguimientos. Lo leen
la reclasificación por inactividad, los filtros y las métricas futuras (spec del flujo de atención
configurable, frontend `docs/superpowers/specs/2026-09-29-flujos-de-atencion-configurables-design.md`
§2 «Fuente y chat»).

`origen` es un `str` y NO un StrEnum, a propósito: este dato se guarda en cada chat, y un valor
nuevo en un enum revienta al parsear el chat ENTERO en todo servicio parado en un pin viejo de
letschatty. Los valores conocidos están en `ORIGENES_DEL_MOTIVO`; uno desconocido se acepta tal cual.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator

from ..utils.types.identifier import StrObjectId

# La fuente (link, anuncio, QR) declaró el motivo: no se clasificó.
ORIGEN_FUENTE = "fuente"
# La IA lo eligió con certeza.
ORIGEN_CLASIFICADO = "clasificado"
# La IA dudó, le preguntó al cliente y eligió con la respuesta.
ORIGEN_PREGUNTADO = "preguntado"
# No hubo coincidencia (o no había otros motivos): quedó en «Consulta general».
ORIGEN_CONSULTA_GENERAL = "consulta_general"

# 0.6.16 — «Pasar a otro motivo»: la IA del flujo lo cambió en medio de la conversación (herramienta
# `cambiar_motivo` de la acción de IA).
ORIGEN_CAMBIADO_POR_IA = "cambiado_por_ia"

ORIGENES_DEL_MOTIVO = frozenset(
    {ORIGEN_FUENTE, ORIGEN_CLASIFICADO, ORIGEN_PREGUNTADO, ORIGEN_CONSULTA_GENERAL, ORIGEN_CAMBIADO_POR_IA}
)


class MotivoEnChat(BaseModel):
    motivo_id: StrObjectId = Field(description="El motivo aplicado en la última entrada del chat")
    asignado_at: datetime = Field(description="Cuándo se aplicó (UTC)")
    origen: str = Field(description="Cómo se decidió: ver ORIGENES_DEL_MOTIVO. Texto libre a propósito.")

    # 0.6.9 / 0.5.11 — «Si responde» del motivo o de una rama: hasta cuándo puede haber una marca esperando la
    # primera respuesta del cliente (la marca vive en `atencion_en_chat`). Es la compuerta BARATA de api-chatty:
    # sin esto (o vencido) un entrante no hace ni una lectura. None = no hay nada esperando.
    si_responde_hasta: Optional[datetime] = Field(default=None)

    @field_validator("asignado_at", "si_responde_hasta")
    @classmethod
    def _en_utc(cls, valor: Optional[datetime]) -> Optional[datetime]:
        # Mongo devuelve fechas sin zona (en UTC): compararlas con una con zona explota.
        if valor is None:
            return None
        return valor if valor.tzinfo else valor.replace(tzinfo=ZoneInfo("UTC"))

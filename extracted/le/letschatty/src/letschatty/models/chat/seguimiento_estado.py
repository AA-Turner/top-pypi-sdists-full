"""En qué está la conversación respecto de los seguimientos (plan 9 del flujo de atención).

Tres estados, automáticos (nadie los toca a mano en esta versión):

| Estado | Cuándo |
|---|---|
| `activa` | todo lo normal: alguien escribió y la conversación sigue |
| `en_seguimiento` | le escribimos, no contestó, y corren los seguimientos del flujo |
| `sin_respuesta` | terminaron los seguimientos y nunca contestó |

Transiciones (las hace api-chatty):
1. Arrancan los seguimientos → `en_seguimiento`.
2. Terminan sin respuesta → `sin_respuesta` + se aplica el cierre (`Seguimientos.al_terminar`), y se
   guarda la etapa del funnel en la que se cayó (`etapa_al_caer`).
3. El cliente escribe (en cualquier estado) → `activa`; si estaba `sin_respuesta`, se aplica
   `al_terminar.si_vuelve` del bloque que cerró (`clave`).

Vive en `Chat.seguimiento_estado`. `None` = el chat nunca pasó por esto: se lee como `activa`
(los chats viejos cargan sin tocar nada).

`estado` es un `str` y NO un StrEnum, a propósito, como `MotivoEnChat.origen`: esto se guarda en
cada chat, y un valor nuevo en un enum revienta al parsear el chat ENTERO en todo servicio parado
en un pin viejo de letschatty (ya hay estados pensados para la épica de las áreas, como «esperando
a la empresa»). Los conocidos están en `EstadoDeSeguimiento`; uno desconocido se acepta tal cual.
Por lo mismo, nada acá valida combinaciones: un chat que no se puede leer es peor que un dato raro.
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import List, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator

from ..utils.types.identifier import StrObjectId


class EstadoDeSeguimiento(StrEnum):
    """Los valores conocidos de `EstadoDelSeguimiento.estado` (que es texto libre: ver arriba)."""

    ACTIVA = "activa"
    EN_SEGUIMIENTO = "en_seguimiento"
    SIN_RESPUESTA = "sin_respuesta"


ESTADOS_DE_SEGUIMIENTO = frozenset(e.value for e in EstadoDeSeguimiento)


class EtapaDelFunnel(BaseModel):
    funnel_id: StrObjectId
    stage_id: StrObjectId


class EstadoDelSeguimiento(BaseModel):
    estado: str = Field(description="Ver EstadoDeSeguimiento. Texto libre a propósito.")
    desde: datetime = Field(description="Cuándo entró en este estado (UTC)")
    clave: Optional[str] = Field(
        default=None,
        description=(
            "El bloque de seguimientos que lo puso en este estado, con la clave de las cadenas de "
            "api-chatty (`consulta_general`, `motivo:<id>`, `rama:<id>:<califica|no_califica>`). Con "
            "ella se encuentra el `si_vuelve` a aplicar y el total de pasos para «2 de 3»."
        ),
    )
    etapa_al_caer: Optional[EtapaDelFunnel] = Field(
        default=None,
        description="Sólo en `sin_respuesta`: la etapa del funnel en la que estaba al caerse. None = no estaba en un funnel.",
    )
    etiquetas_del_cierre: List[StrObjectId] = Field(
        default_factory=list,
        description=(
            "Sólo en `sin_respuesta`: las etiquetas que el cierre le SUMÓ de verdad (no las que ya "
            "tenía). Son las que saca `si_vuelve.quitar_etiquetas_del_cierre`, aunque después se haya "
            "editado el cierre."
        ),
    )

    @field_validator("desde")
    @classmethod
    def _en_utc(cls, valor: datetime) -> datetime:
        # Mongo devuelve fechas sin zona (en UTC): compararlas con una con zona explota.
        return valor if valor.tzinfo else valor.replace(tzinfo=ZoneInfo("UTC"))

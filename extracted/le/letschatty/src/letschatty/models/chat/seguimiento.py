"""El seguimiento como dato del chat.

Un `Seguimiento` es un contacto proactivo del negocio hacia un cliente que no contestó:
un mensaje (de una persona, de un workflow, de una campaña), un mensaje de la IA (smart
follow-up) o un recordatorio resuelto («lo llamé»). Vive embebido en `Chat.seguimientos`.

**La lista es la verdad.** `recalcular` deriva desde la lista y los mensajes entrantes todo
lo que se lee: el `ordinal` dentro del ciclo, si el cliente respondió (`respondido_at`) y los
tres contadores que el chat denormaliza para filtrar. Nunca se incrementa nada a mano.

Un ciclo es lo que pasa entre dos mensajes del cliente. Cuando el cliente escribe, el ÚLTIMO
seguimiento del ciclo queda respondido con ese mensaje; los anteriores del mismo ciclo quedan
sin respuesta, que es la verdad: hicieron falta tres. `anulado_at` conserva los auto-marcados
que un agente sacó: no cuentan, pero la métrica no miente.
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from ..utils.types.executor_types import ExecutorType
from ..utils.types.identifier import StrObjectId
from ..utils.types.serializer_type import SerializerType

UTC = ZoneInfo("UTC")


class SeguimientoTipo(StrEnum):
    MENSAJE = "mensaje"
    MENSAJE_IA = "mensaje_ia"
    RECORDATORIO = "recordatorio"


class SeguimientoOrigen(StrEnum):
    HUMANO = "humano"
    WORKFLOW = "workflow"
    SMART_FOLLOW_UP = "smart_follow_up"
    CAMPANA = "campaña"
    MANUAL = "manual"


class SeguimientoExecutor(BaseModel):
    """Quién firmó. Copia mínima de `Executor` para no importar el modelo de ejecución (que
    arrastra Source, FlowPreview y User) desde el modelo del chat. A veces está raro porque
    se reusan api-keys: por eso `origen` existe aparte y no se deriva de acá."""
    id: StrObjectId
    type: ExecutorType
    name: str


def _a_utc(v):
    if isinstance(v, datetime) and v.tzinfo is None:
        return v.replace(tzinfo=UTC)
    return v


class Seguimiento(BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), frozen=True)
    at: datetime
    tipo: SeguimientoTipo
    origen: SeguimientoOrigen
    message_id: Optional[str] = Field(default=None)
    recordatorio_id: Optional[StrObjectId] = Field(default=None)
    executor: SeguimientoExecutor
    workflow_id: Optional[StrObjectId] = Field(default=None)
    ordinal: int = Field(default=1)
    respondido_at: Optional[datetime] = Field(default=None)
    respuesta_message_id: Optional[str] = Field(default=None)
    anulado_at: Optional[datetime] = Field(default=None)

    @field_validator("at", "respondido_at", "anulado_at", mode="before")
    @classmethod
    def _fechas_utc(cls, v):
        return _a_utc(v)

    @property
    def activo(self) -> bool:
        return self.anulado_at is None

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        """Igual que `FlowStateAssignedToChat`: con el serializer de base las fechas van como
        `datetime`, no como string, o «sin seguimiento hace N días» devuelve vacío."""
        serializer = kwargs.pop("serializer", SerializerType.API)
        loaded = self.model_dump(mode="json", **kwargs)
        if serializer == SerializerType.DATABASE:
            loaded["at"] = self.at
            loaded["respondido_at"] = self.respondido_at
            loaded["anulado_at"] = self.anulado_at
        return loaded


Entrante = Tuple[datetime, str]  # (created_at, message_id) de un mensaje del cliente


def recalcular(
    seguimientos: List[Seguimiento], entrantes: List[Entrante],
) -> Tuple[List[Seguimiento], int, int, Optional[datetime]]:
    """Deriva ordinales, respuestas y contadores desde la lista y los entrantes.

    Devuelve `(lista, total, consecutivos, ultimo_at)`. La lista vuelve ordenada por `at`
    y completa (los anulados adentro, sin tocar). Idempotente: correrla dos veces da lo mismo.
    """
    entrantes = sorted(((_a_utc(at), mid) for at, mid in entrantes), key=lambda e: e[0])
    ordenados = sorted(seguimientos, key=lambda s: s.at)

    def _ciclo_de(at: datetime) -> int:
        """Índice del último entrante anterior o igual a `at`; -1 si no hay."""
        idx = -1
        for i, (e_at, _) in enumerate(entrantes):
            if e_at <= at:
                idx = i
            else:
                break
        return idx

    resultado: List[Seguimiento] = []
    activos_por_ciclo: Dict[int, List[int]] = {}  # ciclo -> posiciones en `resultado`
    for s in ordenados:
        if not s.activo:
            resultado.append(s)
            continue
        ciclo = _ciclo_de(s.at)
        posiciones = activos_por_ciclo.setdefault(ciclo, [])
        actualizado = s.model_copy(update={
            "ordinal": len(posiciones) + 1,
            "respondido_at": None,
            "respuesta_message_id": None,
        })
        posiciones.append(len(resultado))
        resultado.append(actualizado)

    # El último activo de cada ciclo queda respondido por el entrante que cierra el ciclo.
    for ciclo, posiciones in activos_por_ciclo.items():
        siguiente = ciclo + 1
        if siguiente < len(entrantes):
            e_at, e_id = entrantes[siguiente]
            pos = posiciones[-1]
            resultado[pos] = resultado[pos].model_copy(
                update={"respondido_at": e_at, "respuesta_message_id": e_id},
            )

    activos = [s for s in resultado if s.activo]
    total = len(activos)
    ciclo_actual = len(entrantes) - 1
    consecutivos = len(activos_por_ciclo.get(ciclo_actual, [])) if entrantes else 0
    ultimo = max((s.at for s in activos), default=None)
    return resultado, total, consecutivos, ultimo

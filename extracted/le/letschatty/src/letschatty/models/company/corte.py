"""El corte del servicio por falta de pago: el estado de una empresa y qué permite.

Lo CALCULA billing (`lambdas`, `shared/billing/corte.py`) y lo GUARDA api-chatty en la empresa
(`EmpresaModel.corte`). Lo que permite cada estado vive acá, una sola vez, porque lo preguntan
api-chatty (rutas y envíos), cintia (antes de gastar) y copilot.

Reglas que no se rompen:
- `None` es «al día»: así quedan todas las empresas de antes de esta función.
- El estado guardado puede estar viejo: `estado_efectivo` corta en el instante exacto de
  `corta_el` / `gracia_hasta`, aunque el barrido de billing todavía no haya corrido.
- `solo_avisar` muestra la franja y no frena nada (primer ciclo en prod).
- Recibir mensajes de los clientes finales NO es una acción de este catálogo: nunca se corta.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class EstadoDeCorte(StrEnum):
    AL_DIA = "al_dia"
    AVISO = "aviso"
    RESTRINGIDA = "restringida"
    BLOQUEADA = "bloqueada"
    GRACIA = "gracia"
    EXENTA = "exenta"


class MotivoDeCorte(StrEnum):
    VENCIMIENTO = "vencimiento"
    GRACIA_VENCIDA = "gracia_vencida"
    ACUERDO = "acuerdo"
    PAGO = "pago"
    #: Terminó la prueba gratis de una empresa que se registró sola y no pagó (billing, `corte.py`).
    PRUEBA_TERMINADA = "prueba_terminada"


class AccionCortable(StrEnum):
    USAR_LA_APP = "usar_la_app"
    ENVIAR_COMO_PERSONA = "enviar_como_persona"
    ENVIAR_PLANTILLA = "enviar_plantilla"
    IA = "ia"
    CAMPANA = "campana"
    AUTOMATIZACION_QUE_ENVIA = "automatizacion_que_envia"
    PROGRAMADO_DEL_SISTEMA = "programado_del_sistema"


#: Lo que gasta por su cuenta: se frena desde `restringida`.
_LO_QUE_GASTA_SOLO = frozenset({
    AccionCortable.IA,
    AccionCortable.CAMPANA,
    AccionCortable.AUTOMATIZACION_QUE_ENVIA,
    AccionCortable.PROGRAMADO_DEL_SISTEMA,
})


def _utc(momento: datetime) -> datetime:
    return momento if momento.tzinfo else momento.replace(tzinfo=timezone.utc)


class CorteDeServicio(BaseModel):
    estado: EstadoDeCorte = EstadoDeCorte.AL_DIA
    vencio_el: Optional[str] = Field(default=None, description="Vencimiento impago, 'YYYY-MM-DD' (el de «Mi plan»).")
    restringe_el: Optional[datetime] = None
    corta_el: Optional[datetime] = None
    gracia_hasta: Optional[datetime] = None
    inminente: bool = False
    solo_avisar: bool = False
    motivo: Optional[MotivoDeCorte] = None
    calculado_en: Optional[datetime] = None

    def estado_efectivo(self, ahora: datetime) -> EstadoDeCorte:
        ahora = _utc(ahora)
        if self.estado in (EstadoDeCorte.AVISO, EstadoDeCorte.RESTRINGIDA) and self.corta_el and ahora >= _utc(self.corta_el):
            return EstadoDeCorte.BLOQUEADA
        if self.estado == EstadoDeCorte.GRACIA and self.gracia_hasta and ahora >= _utc(self.gracia_hasta):
            return EstadoDeCorte.BLOQUEADA
        if self.estado == EstadoDeCorte.AVISO and self.restringe_el and ahora >= _utc(self.restringe_el):
            return EstadoDeCorte.RESTRINGIDA
        return self.estado

    def permite(self, accion: AccionCortable, ahora: datetime) -> bool:
        if self.solo_avisar:
            return True
        estado = self.estado_efectivo(ahora)
        if estado == EstadoDeCorte.BLOQUEADA:
            return False
        if estado == EstadoDeCorte.RESTRINGIDA:
            return accion not in _LO_QUE_GASTA_SOLO
        return True


def corte_permite(corte: Optional[CorteDeServicio], accion: AccionCortable, ahora: datetime) -> bool:
    """Lo único que tiene que preguntar quien actúa por la empresa. Sin corte, todo se permite."""
    return corte is None or corte.permite(accion, ahora)

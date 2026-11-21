"""«Era una pregunta frecuente»: la tercera salida de «¿Por qué escribió?» (0.6.57.10, 2026-11-19).

El nuevo inicio del flujo (pedido de Axel con MA Distribución): «¿Por qué escribió?» tiene dos salidas —se
identificó → el motivo; no se identificó → «Sin motivo» (lo que antes se llamaba Consulta general, que ahora vuelve
siempre a clasificar)— y un RESULTADO aparte: la pregunta frecuente. Una pregunta frecuente (horarios, dirección,
medios de pago) no es un motivo: la IA la contesta y el chat queda donde estaba, sin forzarle un motivo; el mensaje
siguiente se clasifica normal.

Esto es lo que la empresa le suma a esa salida (`Recepcion.pregunta_frecuente`). None = la IA contesta y nada más.
La salida sólo existe en el nuevo inicio: la versión del inicio la guarda api-chatty (campo suelto
`atencion_inicio` de `recepciones`, como `atencion_estado`) y es la que le pide al clasificador esta salida.

Un lector en un pin anterior descarta `pregunta_frecuente` al leer y, si vuelve a guardar la recepción entera, lo
pierde: orden de deploy letschatty → api-chatty → frontend/MCP.
"""
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from letschatty.models.utils.types.identifier import StrObjectId

from .acciones_fijas import AccionesFijas

MAX_HORAS_PARA_ARCHIVAR = 720
LARGO_MAXIMO_INDICACION = 1000


class SalidaPreguntaFrecuente(BaseModel):
    acciones: Optional[AccionesFijas] = Field(
        default=None,
        description="Acciones fijas cuando sale «Era una pregunta frecuente» (p. ej. la etiqueta «Pregunta frecuente»)",
    )
    archivar_despues_de_horas: Optional[int] = Field(
        default=None, ge=1, le=MAX_HORAS_PARA_ARCHIVAR,
        description="Archivar el chat si el cliente no vuelve a escribir en estas horas. None = no se archiva",
    )
    chatty_ai_agent_id: Optional[StrObjectId] = Field(
        default=None, description="Qué agente contesta la pregunta. None = el de «Sin motivo» (Consulta general)",
    )
    indicacion: str = Field(
        default="", max_length=LARGO_MAXIMO_INDICACION,
        description="Cómo contesta la IA las preguntas frecuentes («si preguntan por envíos, mandá el link»)",
    )

    @field_validator("indicacion")
    @classmethod
    def _limpiar(cls, v: str) -> str:
        return (v or "").strip()

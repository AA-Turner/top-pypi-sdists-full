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

`atiende` (0.6.102 / 0.6.57.15, 2026-11-26, pedido de Axel): quién atiende la pregunta frecuente. «ia» (lo de
siempre, y lo que leen las recepciones guardadas antes) o «equipo»: la IA no contesta y el chat queda esperando
agente como un chat sin IA, donde estaba (sin indicación, sin agente y sin archivar: eso es de la IA). Si la empresa
no tiene agente de IA, api-chatty atiende con el equipo aunque diga «ia». `QuienAtiende` es un enum CERRADO: un
valor nuevo exige actualizar primero a api-chatty, el único que escribe la recepción.
"""
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from letschatty.models.utils.types.identifier import StrObjectId

from .acciones_fijas import AccionesFijas

MAX_HORAS_PARA_ARCHIVAR = 720
LARGO_MAXIMO_INDICACION = 1000


class QuienAtiende(StrEnum):
    IA = "ia"  # contesta la IA (un turno, con la indicación de la salida)
    EQUIPO = "equipo"  # la IA no contesta: queda esperando agente, como un chat sin IA


class SalidaPreguntaFrecuente(BaseModel):
    atiende: QuienAtiende = Field(
        default=QuienAtiende.IA,
        description="Quién atiende la pregunta frecuente: ia (contesta la IA) o equipo (queda esperando agente)",
    )
    acciones: Optional[AccionesFijas] = Field(
        default=None,
        description="Acciones fijas cuando sale «Era una pregunta frecuente» (p. ej. la etiqueta «Pregunta frecuente»)",
    )
    archivar_despues_de_horas: Optional[int] = Field(
        default=None, ge=1, le=MAX_HORAS_PARA_ARCHIVAR,
        description="Archivar el chat si el cliente no vuelve a escribir en estas horas. None = no se archiva",
    )
    chatty_ai_agent_id: Optional[StrObjectId] = Field(
        default=None, description="Qué agente contesta la pregunta (sólo con atiende=ia). None = el de «Sin motivo»",
    )
    indicacion: str = Field(
        default="", max_length=LARGO_MAXIMO_INDICACION,
        description="Cómo contesta la IA las preguntas frecuentes («si preguntan por envíos, mandá el link»)",
    )

    @field_validator("indicacion")
    @classmethod
    def _limpiar(cls, v: str) -> str:
        return (v or "").strip()

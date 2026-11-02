"""Cuando el cliente responde (y se cortan los seguimientos).

Se ejecuta como una acción más, encolada DESPUÉS del primer envío (poner o sacar la IA del chat,
asignar), no como un caso especial del envío: así no compite con la corrida que está mandando.

Enums cerrados: `IaAlResponder` y `ModoAsignacion` son CERRADOS. Un valor nuevo, o un campo nuevo
en un modelo que ya existe, exige actualizar PRIMERO al escritor (api-chatty, el único servicio
que escribe estos documentos) antes de que algo lo guarde: un lector en un pin viejo falla al
leer un valor de enum que no conoce y descarta los campos desconocidos de los modelos conocidos
al volver a guardar. Sólo la unión de acciones tiene respaldo (`AccionDesconocida`).
"""
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field, model_validator

from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode
from letschatty.models.utils.types.identifier import StrObjectId

if TYPE_CHECKING:
    # Ciclo de tipos real: AlResponder → AccionPrecalificar → Precalificacion → Rama → AlResponder.
    # `precalificacion.py` define `AccionDeGestion` y la inyecta en este módulo (ver su final); el
    # import de abajo de todo garantiza que eso pase aunque se importe sólo este módulo.
    from .precalificacion import AccionDeGestion


class IaAlResponder(StrEnum):
    NO = "no"
    AUTONOMA = "autonoma"
    SUGIERE = "sugiere"  # sugiere y una persona aprueba


_MODO = {
    IaAlResponder.NO: ChattyAIMode.OFF,
    IaAlResponder.AUTONOMA: ChattyAIMode.AUTONOMOUS,
    IaAlResponder.SUGIERE: ChattyAIMode.SUGGESTIONS,
}


class ModoAsignacion(StrEnum):
    ROUND_ROBIN = "round_robin"  # entre los disponibles, o los de un equipo
    FIJO = "fijo"  # una persona
    NADIE = "nadie"  # queda esperando que alguien lo tome


class Asignacion(BaseModel):
    modo: ModoAsignacion = ModoAsignacion.NADIE
    user_id: Optional[StrObjectId] = Field(default=None, description="Sólo con modo fijo")
    business_area_id: Optional[StrObjectId] = Field(
        default=None, description="Sólo con round robin: reparte entre los disponibles de ese equipo"
    )

    @model_validator(mode="after")
    def validar_destino(self) -> "Asignacion":
        if self.modo == ModoAsignacion.FIJO:
            if not self.user_id:
                raise ValueError("La asignación fija va a una persona")
            if self.business_area_id:
                raise ValueError("La asignación fija va a una persona, no a un equipo")
        elif self.modo == ModoAsignacion.ROUND_ROBIN:
            if self.user_id:
                raise ValueError("El round robin reparte entre las personas disponibles, no lleva una persona")
        elif self.user_id or self.business_area_id:
            raise ValueError("Sin asignación no se elige persona ni equipo")
        return self


class AlResponder(BaseModel):
    """Dos decisiones independientes —si sigue la IA y a quién le queda— que se heredan POR
    SEPARADO de «Consulta general»: cada campo en None es «como en Consulta general». Pisar la IA
    no resetea la asignación (ni al revés). La herencia la resuelve `herencia.py`; un
    `AlResponder` efectivo tiene `ia` y `asignar` siempre definidos."""

    ia: Optional[IaAlResponder] = Field(default=None, description="None = como en «Consulta general»")
    chatty_ai_agent_id: Optional[StrObjectId] = Field(
        default=None, description="None = el agente de «Consulta general»"
    )
    asignar: Optional[Asignacion] = Field(
        default=None,
        description=(
            "A qué persona le queda. Si la IA sigue, aplica cuando la IA escala. "
            "None = como en «Consulta general»."
        ),
    )
    # 0.6.9 / 0.5.11 — «Si responde → Lo gestiona la IA». Qué hace la IA cuando el cliente responde a
    # la RESPUESTA RÁPIDA del motivo: `ia_responde` (responder, con una indicación opcional),
    # `precalificar` (con su precalificación y sus ramas) o `agendar`. Es la misma acción que puede ser
    # la respuesta del motivo, pero arranca recién con la respuesta del cliente (la respuesta rápida ya
    # salió). Sólo vale cuando la respuesta efectiva es una respuesta rápida; con otra respuesta se
    # ignora. Se hereda como los demás campos (None = como en «Consulta general»); para «la IA responde
    # como siempre» sin heredar nada, `{"tipo": "ia_responde"}` sin indicación. En una rama no puede
    # precalificar, y un motivo que precalifica en la respuesta no puede precalificar acá también.
    gestion_ia: Optional["AccionDeGestion"] = Field(
        default=None,
        description=(
            "Qué hace la IA cuando el cliente responde a la respuesta rápida: ia_responde | precalificar | "
            "agendar. None = como en «Consulta general»."
        ),
    )

    def modo_de_ia(self) -> ChattyAIMode:
        if self.ia is None:
            raise ValueError("AlResponder sin resolver: usar configuracion_efectiva")
        return _MODO[self.ia]


# Resuelve `AccionDeGestion` (ver TYPE_CHECKING arriba). Abajo de todo a propósito: si este módulo se
# importa primero, `precalificacion` encuentra `AlResponder` ya definido.
from . import precalificacion as _precalificacion  # noqa: E402,F401

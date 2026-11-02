"""«Como en Consulta general»: la configuración efectiva de un motivo y de una rama.

Una sola implementación para todos los consumidores. Se apila en capas: lo que no hace nada
(`por_defecto`) → Consulta general → el motivo → la rama. Cada capa pisa sólo lo que define.

- Si Consulta general tiene un bloque (o una decisión de «cuando responde») sin definir —motivos
  guardados antes de 2026-09-29—, se completa con lo que no hace nada: sin respuesta, sin
  seguimientos, sin IA, sin asignar; nunca con un valor inventado. Su origen es `por_defecto`.
- «Cuando responde» se hereda CAMPO POR CAMPO (`ia`, `asignar`, `chatty_ai_agent_id`): un motivo
  que sólo dice «la IA sigue» conserva la asignación de Consulta general. El origen de cada campo
  va en `origen["al_responder.<campo>"]`; `origen["al_responder"]` dice quién definió el bloque.
- `al_responder.gestion_ia` («Si responde → Lo gestiona la IA», 0.6.9) se hereda como un campo más
  de «Cuando responde». Un `agendar` ahí sin agente también toma el agente efectivo
  (`origen["al_responder.gestion_ia.chatty_ai_agent_id"]`).
- `si_responde` (acciones fijas) NO pasa por acá: no se hereda. Tampoco `Rama.acciones` (0.6.14).
- `derivar_cuando` (0.6.14) viaja DENTRO de la acción (`ia_responde`, `agendar`, `Precalificacion`): se
  hereda con ella, entera, como `indicacion`.
- `mensaje_al_derivar` (0.6.15) igual: dentro de la acción, se hereda con ella.
- Una acción `agendar` efectiva sin agente toma el agente efectivo (`al_responder.chatty_ai_agent_id`
  de la misma configuración): «None = el agente heredado» queda resuelto acá y no en cada ejecutor.
  De dónde salió ese agente va en `origen["respuesta.chatty_ai_agent_id"]` (sólo cuando se
  completó; `origen["respuesta"]` sigue diciendo quién definió la acción).
- La configuración efectiva de Consulta general misma no tiene capa «motivo»: lo que define es
  `consulta_general` y lo que falta, `por_defecto`.
- Lo que devuelve es una COPIA: mutarlo no cambia a Consulta general, al motivo ni a la rama.
"""
from typing import Literal, Optional

from pydantic import BaseModel

from ..motivo import Motivo
from .accion import Accion
from .acciones_basicas import AccionAgendar, AccionNada
from .al_responder import AlResponder, Asignacion, IaAlResponder
from .precalificacion import Rama
from .seguimientos import ModoSeguimientos, Seguimientos

Origen = Literal["motivo", "consulta_general", "rama", "por_defecto"]

_CAMPOS_AL_RESPONDER = ("ia", "asignar", "chatty_ai_agent_id", "gestion_ia")
_BLOQUES = ("respuesta", "seguimientos", "al_responder")
_ORIGEN_AGENTE_DE_AGENDAR = "respuesta.chatty_ai_agent_id"
_ORIGEN_AGENTE_DE_GESTION = "al_responder.gestion_ia.chatty_ai_agent_id"


class ConfiguracionEfectiva(BaseModel):
    respuesta: Accion
    seguimientos: Seguimientos
    al_responder: AlResponder
    origen: dict[str, Origen]


def _por_defecto() -> ConfiguracionEfectiva:
    return ConfiguracionEfectiva(
        respuesta=AccionNada(),
        seguimientos=Seguimientos(modo=ModoSeguimientos.NINGUNO),
        al_responder=AlResponder(ia=IaAlResponder.NO, asignar=Asignacion(), chatty_ai_agent_id=None),
        origen={k: "por_defecto" for k in (*_BLOQUES, *(f"al_responder.{c}" for c in _CAMPOS_AL_RESPONDER))},
    )


def _encima(
    base: ConfiguracionEfectiva,
    quien: Origen,
    respuesta: Optional[Accion],
    seguimientos: Optional[Seguimientos],
    al_responder: Optional[AlResponder],
) -> ConfiguracionEfectiva:
    """Apila una capa sobre `base`: pisa lo que la capa define y hereda el resto (con su origen)."""
    origen = dict(base.origen)
    if respuesta is not None:
        origen["respuesta"] = quien
        # El agente completado era de la acción de abajo; ésta se completa (o no) al final.
        origen.pop(_ORIGEN_AGENTE_DE_AGENDAR, None)
    if seguimientos is not None:
        origen["seguimientos"] = quien
    if al_responder is not None:
        origen["al_responder"] = quien
    if al_responder is not None and al_responder.gestion_ia is not None:
        origen.pop(_ORIGEN_AGENTE_DE_GESTION, None)

    campos = {}
    for campo in _CAMPOS_AL_RESPONDER:
        propio = getattr(al_responder, campo) if al_responder is not None else None
        if propio is None:
            campos[campo] = getattr(base.al_responder, campo)
        else:
            campos[campo] = propio
            origen[f"al_responder.{campo}"] = quien

    return ConfiguracionEfectiva(
        respuesta=(respuesta if respuesta is not None else base.respuesta).model_copy(deep=True),
        seguimientos=(seguimientos if seguimientos is not None else base.seguimientos).model_copy(deep=True),
        al_responder=AlResponder(**campos).model_copy(deep=True),
        origen=origen,
    )


def _agendar_con_agente(efectiva: ConfiguracionEfectiva) -> ConfiguracionEfectiva:
    """Se aplica UNA vez, sobre la configuración final: si se aplicara en cada capa, un `agendar`
    heredado quedaría con el agente de Consulta general aunque el motivo eligiera otro."""
    r = efectiva.respuesta
    agente = efectiva.al_responder.chatty_ai_agent_id
    if isinstance(r, AccionAgendar) and r.chatty_ai_agent_id is None and agente is not None:
        efectiva.respuesta = r.model_copy(update={"chatty_ai_agent_id": agente})
        efectiva.origen[_ORIGEN_AGENTE_DE_AGENDAR] = efectiva.origen["al_responder.chatty_ai_agent_id"]
    g = efectiva.al_responder.gestion_ia
    if isinstance(g, AccionAgendar) and g.chatty_ai_agent_id is None and agente is not None:
        efectiva.al_responder.gestion_ia = g.model_copy(update={"chatty_ai_agent_id": agente})
        efectiva.origen[_ORIGEN_AGENTE_DE_GESTION] = efectiva.origen["al_responder.chatty_ai_agent_id"]
    return efectiva


def configuracion_efectiva(motivo: Motivo, consulta_general: Motivo) -> ConfiguracionEfectiva:
    if not consulta_general.is_fallback:
        raise ValueError("La base de la herencia tiene que ser «Consulta general» (is_fallback=True)")
    general = _encima(
        _por_defecto(),
        "consulta_general",
        consulta_general.respuesta,
        consulta_general.seguimientos,
        consulta_general.al_responder,
    )
    quien: Origen = "consulta_general" if motivo.is_fallback else "motivo"
    return _agendar_con_agente(
        _encima(general, quien, motivo.respuesta, motivo.seguimientos, motivo.al_responder)
    )


def rama_efectiva(rama: Rama, motivo: ConfiguracionEfectiva) -> ConfiguracionEfectiva:
    return _agendar_con_agente(_encima(motivo, "rama", rama.enviar, rama.seguimientos, rama.al_responder))

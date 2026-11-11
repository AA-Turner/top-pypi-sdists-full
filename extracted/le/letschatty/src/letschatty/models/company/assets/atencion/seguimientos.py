"""Seguimientos cuando no responde.

- `fijos`: pasos «después de X minutos desde el primer envío» → una respuesta rápida o crear un
  pendiente. Se ejecutan como un workflow de copilot generado desde esta definición (copilot ya
  sabe no ejecutar un paso si el cliente respondió).
- `ia`: dos formas. La de siempre, el componente `FollowUpStrategy` del agente (`follow_up_strategy_id`,
  compartido entre motivos), o (0.6.16) los seguimientos de IA PROPIOS del bloque (`ia`: una instrucción
  para todos y/o una por seguimiento, los tiempos y «sólo días hábiles»), que se editan desde el flujo sin
  tocar a ningún otro motivo. Más las respuestas rápidas que la IA puede usar.
- `ninguno`: explícito. En un motivo, `seguimientos=None` quiere decir «como en Consulta general»;
  para decir «este motivo no hace seguimientos aunque la general sí» hace falta este valor.
- `si_responde` (plan 7c): acciones fijas cuando el cliente responde a un seguimiento del bloque; la
  contracara de `al_terminar`.
- `al_terminar` (plan 9): el cierre combinable — siempre pasa a «Sin respuesta» (del sistema) y,
  además, etiquetar / archivar / dejar esperando / pendiente / mover a etapa, más `si_vuelve`.

Todo seguimiento que se manda o se crea se registra en el chat (la lista y los contadores de
`models/chat/seguimiento.py`); eso lo hacen los ejecutores, no el modelo.

Enums cerrados: `ModoSeguimientos`, `SiVuelveA` y `CierreSinRespuesta` (legado) son CERRADOS. Un
valor nuevo, o un campo nuevo en un modelo que ya existe, exige actualizar PRIMERO al escritor
(api-chatty, el único servicio que escribe estos documentos) antes de que algo lo guarde: un lector en un pin viejo
falla al leer un valor de enum que no conoce y descarta los campos desconocidos de los modelos
conocidos al volver a guardar. Sólo la unión de acciones tiene respaldo (`AccionDesconocida`).
"""
from enum import StrEnum
from typing import Annotated, Any, Optional, Union

from pydantic import BaseModel, Field, Tag, field_validator, model_validator
from pydantic.json_schema import SkipJsonSchema

from letschatty.models.chat.quality_scoring import QualityScore
from letschatty.models.utils.types.identifier import StrObjectId

from .acciones_basicas import (
    DESCONOCIDA,
    TIPOS_DE_ACCION,
    AccionCrearPendiente,
    AccionDesconocida,
    AccionRespuestaRapida,
    discriminador_con_respaldo,
)
from .acciones_fijas import AccionesFijas


class ModoSeguimientos(StrEnum):
    FIJOS = "fijos"
    IA = "ia"
    NINGUNO = "ninguno"


# Un paso fijo sólo manda una respuesta rápida o crea un pendiente. Todo otro tipo CONOCIDO está
# prohibido (no es «uno nuevo» que haya que conservar): se deriva de la lista única.
TIPOS_DE_PASO = frozenset({"respuesta_rapida", "crear_pendiente"})
TIPOS_PROHIBIDOS_EN_PASO = TIPOS_DE_ACCION - TIPOS_DE_PASO

AccionDePaso = Annotated[
    Union[
        Annotated[AccionRespuestaRapida, Tag("respuesta_rapida")],
        Annotated[AccionCrearPendiente, Tag("crear_pendiente")],
        Annotated[SkipJsonSchema[AccionDesconocida], Tag(DESCONOCIDA)],
    ],
    discriminador_con_respaldo(TIPOS_DE_PASO),
]


class PasoDeSeguimiento(BaseModel):
    despues_de_minutos: int = Field(ge=1, description="Desde el primer envío, no desde el paso anterior")
    accion: AccionDePaso

    @model_validator(mode="after")
    def solo_pasos_permitidos(self) -> "PasoDeSeguimiento":
        # Un tipo conocido pero no permitido acá (p. ej. ia_responde) cae en el respaldo por el
        # discriminador; lo distinguimos de un tipo realmente nuevo para no aceptarlo en silencio.
        if isinstance(self.accion, AccionDesconocida) and self.accion.tipo in TIPOS_PROHIBIDOS_EN_PASO:
            raise ValueError(f"Un paso de seguimiento fijo no puede ser «{self.accion.tipo}»")
        return self


#: 0.6.16 — los seguimientos de IA propios del bloque (`Seguimientos.ia`).
MAX_PASOS_DE_IA = 10
MAX_LARGO_INDICACION_DE_SEGUIMIENTO = 1000


def _limpiar_indicacion(v: str) -> str:
    texto = (v or "").strip()
    if len(texto) > MAX_LARGO_INDICACION_DE_SEGUIMIENTO:
        raise ValueError(
            f"La instrucción de un seguimiento tiene hasta {MAX_LARGO_INDICACION_DE_SEGUIMIENTO} caracteres"
        )
    return texto


class PasoDeSeguimientoIa(BaseModel):
    """Un seguimiento de IA del bloque: CUÁNDO (como un paso fijo, «desde el primer envío») y, opcional, qué
    tiene que hacer la IA en ESTE seguimiento (se suma a la instrucción para todos)."""

    despues_de_minutos: int = Field(ge=1, description="Desde el primer envío, no desde el paso anterior")
    indicacion: str = Field(default="", description="La instrucción de este seguimiento (se suma a la de todos)")

    @field_validator("indicacion")
    @classmethod
    def _indicacion(cls, v: str) -> str:
        return _limpiar_indicacion(v)


class SeguimientosDeIa(BaseModel):
    """0.6.16 — Los seguimientos de IA PROPIOS de un bloque (motivo, Consulta general o rama). Reemplazan a la
    `FollowUpStrategy` compartida del agente para ese bloque: se editan desde el flujo y no cambian ningún otro
    motivo.

    - `indicacion`: «una instrucción para todos» (vale en cada seguimiento).
    - `pasos[i].indicacion`: «una instrucción por seguimiento» (se suma a la de todos en ESE seguimiento).
      Las dos formas pueden ir juntas; cada seguimiento necesita al menos una de las dos.
    - `pasos[i].despues_de_minutos`: como los fijos, desde el primer envío, en orden y sin repetir.
    - `solo_dias_habiles`: los seguimientos salen de lunes a viernes (en la zona de la recepción); se combina
      con `Seguimientos.solo_en_horario`.

    El runtime (api-chatty) los arma como una cadena de copilot igual que los fijos: cada paso le pide a la IA
    UN seguimiento con su instrucción, y el último termina en «Sin respuesta» con `al_terminar`, exactamente
    como los fijos."""

    indicacion: str = Field(default="", description="La instrucción para todos los seguimientos")
    pasos: list[PasoDeSeguimientoIa] = Field(default_factory=list)
    solo_dias_habiles: bool = Field(default=False, description="Sólo de lunes a viernes")

    @field_validator("indicacion")
    @classmethod
    def _indicacion(cls, v: str) -> str:
        return _limpiar_indicacion(v)

    @model_validator(mode="after")
    def validar(self) -> "SeguimientosDeIa":
        if not self.pasos:
            raise ValueError("Los seguimientos de IA necesitan al menos un seguimiento")
        if len(self.pasos) > MAX_PASOS_DE_IA:
            raise ValueError(f"Hasta {MAX_PASOS_DE_IA} seguimientos de IA")
        minutos = [p.despues_de_minutos for p in self.pasos]
        if minutos != sorted(set(minutos)):
            raise ValueError("Los pasos van en orden y sin repetir el momento")
        if not self.indicacion and any(not p.indicacion for p in self.pasos):
            raise ValueError(
                "Cada seguimiento de IA necesita una instrucción: la de todos o la suya"
            )
        return self

    def indicacion_del_paso(self, numero: int) -> str:
        """La instrucción completa del seguimiento `numero` (1..n): la de todos y la suya, en ese orden."""
        if not 1 <= numero <= len(self.pasos):
            raise ValueError(f"El seguimiento {numero} no existe (hay {len(self.pasos)})")
        partes = [self.indicacion, self.pasos[numero - 1].indicacion]
        return "\n\n".join(p for p in partes if p)


class CierreSinRespuesta(StrEnum):
    """LEGADO (hasta 0.4.562): el cierre era UNA cosa, en `AlTerminar.que`. Desde 0.4.563 el cierre es
    combinable y este enum sólo sirve para LEER documentos viejos (`AlTerminar._desde_que`). No se
    escribe más; queda exportado para que el código que lo importa siga cargando."""

    NADA = "nada"
    ARCHIVAR = "archivar"
    DEJAR_ESPERANDO = "dejar_esperando"
    MOVER_A_ETAPA = "mover_a_etapa"
    CREAR_PENDIENTE = "crear_pendiente"


class AccionesDeEtiquetas(BaseModel):
    """Etiquetas que el cierre le suma y le saca al chat."""

    agregar: list[StrObjectId] = Field(default_factory=list)
    quitar: list[StrObjectId] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar(self) -> "AccionesDeEtiquetas":
        if len(set(self.agregar)) != len(self.agregar) or len(set(self.quitar)) != len(self.quitar):
            raise ValueError("Hay una etiqueta repetida")
        if set(self.agregar) & set(self.quitar):
            raise ValueError("Una etiqueta no se puede agregar y sacar a la vez")
        return self

    @property
    def vacio(self) -> bool:
        return not (self.agregar or self.quitar)


class EtapaDestino(BaseModel):
    target_funnel_id: StrObjectId
    target_stage_id: StrObjectId


class SiVuelveA(StrEnum):
    # Vuelve a la etapa del funnel en la que estaba cuando se cayó (`etapa_al_caer` del chat).
    ETAPA_ANTERIOR = "etapa_anterior"
    # Va a una etapa elegida acá.
    ETAPA_FIJA = "etapa_fija"
    # Pasa de nuevo por el flujo de atención: se clasifica como un chat que entra.
    RECLASIFICAR = "reclasificar"


class SiVuelve(BaseModel):
    """Qué pasa cuando un chat «Sin respuesta» vuelve a escribir. Volver a «Activa» y cortar los
    seguimientos lo hace el sistema siempre; esto es lo que se le suma."""

    a: SiVuelveA = SiVuelveA.ETAPA_ANTERIOR
    target_funnel_id: Optional[StrObjectId] = None
    target_stage_id: Optional[StrObjectId] = None
    quitar_etiquetas_del_cierre: bool = Field(
        default=False, description="Le saca las etiquetas que le sumó el cierre (`AlTerminar.etiquetas.agregar`)"
    )

    @model_validator(mode="after")
    def validar(self) -> "SiVuelve":
        if self.a == SiVuelveA.ETAPA_FIJA:
            if not (self.target_funnel_id and self.target_stage_id):
                raise ValueError("Volver a una etapa fija necesita el funnel y la etapa")
        elif self.target_funnel_id or self.target_stage_id:
            raise ValueError("El funnel y la etapa sólo van con «etapa fija»")
        return self


# Las claves del documento viejo (hasta 0.4.562). Las nuevas, para saber si un documento ya viene
# con la forma combinable.
_CLAVES_VIEJAS = frozenset({"que", "target_funnel_id", "target_stage_id"})
_CLAVES_NUEVAS = frozenset({"etiquetas", "archivar", "dejar_esperando", "mover_a", "si_vuelve", "despues_de_minutos",
                            "workflow_ids", "quality_score"})

#: El cierre sale 24 h después del último paso, salvo que el bloque diga otra cosa (`AlTerminar.despues_de_minutos`).
ESPERA_DEL_CIERRE_POR_DEFECTO_MINUTOS = 24 * 60
#: El tope de copilot entre dos eslabones (60 días).
MAX_ESPERA_DEL_CIERRE_MINUTOS = 60 * 24 * 60


class AlTerminar(BaseModel):
    """El cierre de los seguimientos: qué pasa cuando terminaron y el cliente nunca contestó.

    - **Siempre (del sistema, no es un campo):** el chat pasa a «Sin respuesta»
      (`Chat.seguimiento_estado`) y se registra la etapa del funnel en la que se cayó.
    - **Además, combinables:** etiquetar (agregar/sacar), archivar, dejar esperando (sacarle el
      agente), crear un pendiente (`pendiente_titulo`), mover a una etapa (`mover_a`) y, desde 0.6.57,
      enganchar workflows (`workflow_ids`; como en `AccionesFijas`: uno que ya estaba no se duplica) y, desde
      0.6.57.2, calificar el lead (`quality_score`, p. ej. «no respondió → mala»).
    - **Si vuelve a escribir** (`si_vuelve`): vuelve a la etapa donde estaba (default), va a una etapa
      fija o pasa de nuevo por el flujo; y opcionalmente se le sacan las etiquetas del cierre.

    Compatibilidad: un documento viejo (`que` + `target_funnel_id`/`target_stage_id`) se lee como la
    forma nueva con esa única acción; lo que el viejo guardaba de más y no usaba (un título con
    `que="archivar"`, p. ej.) se descarta, para que no se convierta en una acción que antes no corría.

    ⚠️ Orden de despliegue: un lector en 0.4.562 o antes lee la forma nueva como «nada» (ignora las
    claves que no conoce y `que` falta) y, si vuelve a guardar, la pierde. api-chatty tiene que estar
    en esta versión ANTES de que el frontend escriba la forma nueva.

    ⚠️ `quality_score` (0.6.57.2) tiene el mismo orden: letschatty → api-chatty → frontend. Un lector en un
    pin anterior descarta el campo al leer y, si vuelve a guardar, lo pierde (acá no lanza: el cierre sólo
    queda sin esa acción; en `AccionesFijas`, un `si_responde` con SÓLO la calificación sí deja de leerse).
    """

    etiquetas: AccionesDeEtiquetas = Field(default_factory=AccionesDeEtiquetas)
    archivar: bool = False
    dejar_esperando: bool = Field(
        default=False,
        description="Le saca el agente: el chat vuelve a «esperando agente». Es el `dejar_esperando` viejo.",
    )
    pendiente_titulo: Optional[str] = Field(default=None, description="Con título se crea un pendiente; None = no")
    mover_a: Optional[EtapaDestino] = None
    si_vuelve: SiVuelve = Field(default_factory=SiVuelve)
    # 0.6.22 — «Si no responde» sin mandar mensajes: cuántos minutos espera el cierre. Con pasos, desde el último
    # paso (None = 24 h, lo de siempre). SIN pasos (`Seguimientos.solo_cierre`, modo fijos), desde que el chat entra
    # al bloque (o desde la última respuesta del negocio, que rearma la espera): «a las 24 h pasa a Sin respuesta,
    # sin escribirle».
    despues_de_minutos: Optional[int] = Field(
        default=None,
        ge=1,
        le=MAX_ESPERA_DEL_CIERRE_MINUTOS,
        description=(
            "Minutos hasta pasar a «Sin respuesta»: desde el último paso, o sin pasos desde la entrada. "
            "None = 24 h después del último paso."
        ),
    )
    workflow_ids: list[StrObjectId] = Field(
        default_factory=list,
        description="Workflows (de la empresa) que se enganchan al chat al pasar a «Sin respuesta»",
    )
    quality_score: Optional[QualityScore] = Field(
        default=None,
        description="«Calificar lead» al pasar a «Sin respuesta» (p. ej. mala). None = no califica",
    )

    @model_validator(mode="before")
    @classmethod
    def _desde_que(cls, data: Any) -> Any:
        """Lee el documento viejo: `que` → la acción equivalente de la forma nueva."""
        if not isinstance(data, dict) or not (_CLAVES_VIEJAS & data.keys()):
            return data
        data = dict(data)
        que = data.pop("que", None)
        funnel_id = data.pop("target_funnel_id", None)
        stage_id = data.pop("target_stage_id", None)
        if _CLAVES_NUEVAS & data.keys():
            # Ya viene con la forma nueva: las claves viejas que quedaron colgadas no mandan.
            return data
        que = CierreSinRespuesta(que) if que is not None else CierreSinRespuesta.NADA
        if que != CierreSinRespuesta.CREAR_PENDIENTE:
            # El viejo guardaba el título aunque no creara un pendiente; acá un título ES crearlo.
            data.pop("pendiente_titulo", None)
        if que == CierreSinRespuesta.ARCHIVAR:
            data["archivar"] = True
        elif que == CierreSinRespuesta.DEJAR_ESPERANDO:
            data["dejar_esperando"] = True
        elif que == CierreSinRespuesta.MOVER_A_ETAPA:
            if not (funnel_id and stage_id):
                raise ValueError("Mover a etapa necesita el funnel y la etapa")
            data["mover_a"] = {"target_funnel_id": funnel_id, "target_stage_id": stage_id}
        elif que == CierreSinRespuesta.CREAR_PENDIENTE and not (data.get("pendiente_titulo") or "").strip():
            raise ValueError("Crear un pendiente necesita un título")
        return data

    @field_validator("pendiente_titulo")
    @classmethod
    def limpiar_titulo(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not v.strip():
            raise ValueError("Crear un pendiente necesita un título")
        return v.strip()

    @model_validator(mode="after")
    def validar(self) -> "AlTerminar":
        if self.archivar and self.dejar_esperando:
            raise ValueError("Archivar y dejar esperando no van juntos: el chat termina en un solo lugar")
        if len(set(self.workflow_ids)) != len(self.workflow_ids):
            raise ValueError("Hay un workflow repetido")
        return self

    @property
    def hay_acciones(self) -> bool:
        """¿Hace algo además de pasar a «Sin respuesta»?"""
        return bool(
            not self.etiquetas.vacio or self.archivar or self.dejar_esperando or self.pendiente_titulo or self.mover_a
            or self.workflow_ids or self.quality_score
        )


class Seguimientos(BaseModel):
    modo: ModoSeguimientos
    pasos: list[PasoDeSeguimiento] = Field(default_factory=list)
    follow_up_strategy_id: Optional[StrObjectId] = None
    # 0.6.16: los seguimientos de IA propios del bloque (en vez de la estrategia compartida del agente).
    ia: Optional[SeguimientosDeIa] = Field(
        default=None,
        description=(
            "Seguimientos de IA propios del bloque: instrucción para todos y/o una por seguimiento, tiempos y "
            "«sólo días hábiles». Con esto no va `follow_up_strategy_id`."
        ),
    )
    fast_answer_ids: list[StrObjectId] = Field(default_factory=list)
    solo_en_horario: bool = Field(default=False, description="Usa el horario de la recepción")
    al_terminar: AlTerminar = Field(default_factory=AlTerminar)
    si_responde: Optional[AccionesFijas] = Field(
        default=None,
        description=(
            "Plan 7c: qué se le hace al chat cuando responde a un seguimiento de este bloque (la primera "
            "respuesta, dentro de las 24 h, con el seguimiento como último saliente). Viaja y se hereda con "
            "el bloque entero. None = nada."
        ),
    )

    # ------------------------------------------------------------------ la cadena (0.6.16)

    @property
    def solo_cierre(self) -> bool:
        """0.6.22 — ¿«Si no responde» sin mensajes? Fijos SIN pasos y con `al_terminar.despues_de_minutos`: la cadena
        es sólo el eslabón de cierre, que pasa el chat a «Sin respuesta» (con las acciones del cierre) si en ese tiempo
        el cliente no escribió."""
        return (
            self.modo == ModoSeguimientos.FIJOS
            and not self.pasos
            and self.al_terminar.despues_de_minutos is not None
        )

    @property
    def espera_del_cierre_minutos(self) -> int:
        """Minutos entre el último paso (o la entrada, en `solo_cierre`) y el cierre «Sin respuesta»."""
        return self.al_terminar.despues_de_minutos or ESPERA_DEL_CIERRE_POR_DEFECTO_MINUTOS

    @property
    def de_ia_propios(self) -> bool:
        """¿Son seguimientos de IA PROPIOS del bloque (`ia`), no la estrategia compartida del agente?"""
        return self.modo == ModoSeguimientos.IA and self.ia is not None

    @property
    def arma_cadena(self) -> bool:
        """¿El bloque se arma como una cadena de copilot (con su cierre «Sin respuesta»)? Los fijos con pasos y
        los de IA propios del bloque. La estrategia compartida del agente no (la corre el Smart Follow Up)."""
        return (self.modo == ModoSeguimientos.FIJOS and (bool(self.pasos) or self.solo_cierre)) or self.de_ia_propios

    @property
    def pasos_de_la_cadena(self) -> list:
        """Los pasos de la cadena, en orden: los fijos (`PasoDeSeguimiento`) o los de IA (`PasoDeSeguimientoIa`).
        Los dos tienen `despues_de_minutos` («desde el primer envío»). [] si el bloque no arma cadena o es
        `solo_cierre` (la cadena es sólo el eslabón de cierre)."""
        if self.modo == ModoSeguimientos.FIJOS:
            return list(self.pasos)
        if self.de_ia_propios:
            return list(self.ia.pasos)
        return []

    @model_validator(mode="after")
    def validar_modo(self) -> "Seguimientos":
        if self.modo == ModoSeguimientos.FIJOS:
            if not self.pasos and self.al_terminar.despues_de_minutos is None:
                # 0.6.22: sin pasos vale sólo con «pasar a Sin respuesta después de…» (`solo_cierre`).
                raise ValueError("Los seguimientos fijos necesitan al menos un paso")
            minutos = [p.despues_de_minutos for p in self.pasos]
            if minutos != sorted(set(minutos)):
                raise ValueError("Los pasos van en orden y sin repetir el momento")
            # Los dos modos no se mezclan: lo de la IA en un fijo sería configuración muerta.
            if self.follow_up_strategy_id:
                raise ValueError("Los seguimientos fijos no llevan estrategia de IA")
            if self.fast_answer_ids:
                raise ValueError("Los seguimientos fijos no llevan respuestas rápidas de la IA: van en los pasos")
            if self.ia is not None:
                raise ValueError("Los seguimientos fijos no llevan seguimientos de IA")
        elif self.modo == ModoSeguimientos.IA:
            if self.follow_up_strategy_id and self.ia is not None:
                raise ValueError(
                    "Los seguimientos de IA van con la estrategia del agente o con los del motivo, no con los dos"
                )
            if not self.follow_up_strategy_id and self.ia is None:
                raise ValueError("Los seguimientos de IA necesitan una estrategia o sus seguimientos")
            # Con la estrategia del agente, `al_terminar` se guarda pero no corre (la estrategia no tiene final:
            # termina con su `area_after_reaching_max`). No se rechaza: hay documentos guardados así.
            if self.pasos:
                raise ValueError("Los seguimientos de IA no llevan pasos fijos")
        else:
            if self.pasos or self.follow_up_strategy_id or self.fast_answer_ids or self.ia is not None:
                raise ValueError("«ninguno» no lleva pasos ni estrategia")
            if self.al_terminar != AlTerminar():
                raise ValueError("«ninguno» no tiene un final: sin seguimientos no hay «al terminar»")
            if self.solo_en_horario:
                raise ValueError("«ninguno» no lleva horario: no hay nada que mandar")
            if self.si_responde is not None:
                raise ValueError("«ninguno» no tiene seguimientos a los que responder")
        return self

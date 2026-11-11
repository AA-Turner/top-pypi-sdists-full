"""Las acciones «hoja»: las que no contienen otras acciones.

`AccionPrecalificar` vive en `precalificacion.py` porque contiene ramas, y una rama contiene
acciones; separarla es lo que evita el ciclo de imports. La unión completa está en `accion.py`.

Cerrado a propósito: un campo NUEVO en una acción que ya existe exige actualizar primero al
escritor (api-chatty, el único servicio que escribe estos documentos); un lector en un pin viejo
descarta los campos que no conoce al volver a guardar. Sólo un TIPO nuevo tiene respaldo
(`AccionDesconocida`).

`TIPOS_DE_ACCION` vive acá y es la ÚNICA lista de tipos: la unión completa, la de las ramas y la
de los pasos de seguimiento se derivan de ella. Un tipo nuevo se agrega acá y en su unión.

⚠️ `tipo` sobrevive a `exclude_unset` (ver `_AccionBase`), pero NO a `exclude_defaults=True`:
como su valor ES el default del Literal, ese volcado lo tira y deja un documento que no se puede
volver a leer. Nunca uses `exclude_defaults` con estos modelos ni con nada que los contenga.
"""
import re
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag, field_validator
from pydantic.json_schema import SkipJsonSchema

from letschatty.models.utils.types.identifier import StrObjectId

from .turno import RecordatoriosDelTurno

DESCONOCIDA = "desconocida"

TIPOS_DE_ACCION = frozenset(
    {"respuesta_rapida", "ia_responde", "precalificar", "agendar", "crear_pendiente", "accion_personalizada", "nada"}
)


#: «Derivar a una persona cuando…» del motivo (0.6.14): casos cortos en lenguaje natural («pide hablar con
#: alguien», «está enojado»). Viven al lado de cada `indicacion` —`AccionIaResponde`, `AccionAgendar` y
#: `Precalificacion`— y valen sólo en los chats de ese motivo mientras la IA tiene ese paso activo: no son
#: los `control_triggers` del agente (ésos valen en todos los chats del agente). api-chatty los manda a
#: CINTIA en `atencion_en_chat.ia.derivar_cuando` y la IA escala (ESCALATE) cuando aplica uno; el chat
#: queda para quien diga «Cuando responde → ¿a quién le queda?».
MAX_CASOS_DE_DERIVACION = 10
MAX_LARGO_DE_CASO = 120


def limpiar_casos_de_derivacion(casos: list[str]) -> list[str]:
    """Cada caso en una línea (sin saltos ni espacios repetidos), sin los vacíos; hasta
    `MAX_CASOS_DE_DERIVACION` casos de hasta `MAX_LARGO_DE_CASO` caracteres, sin repetidos."""
    limpios = [" ".join(c.split()) for c in casos]
    limpios = [c for c in limpios if c]
    for c in limpios:
        if len(c) > MAX_LARGO_DE_CASO:
            raise ValueError(f"Cada caso para derivar a una persona tiene hasta {MAX_LARGO_DE_CASO} caracteres")
    if len(limpios) > MAX_CASOS_DE_DERIVACION:
        raise ValueError(f"Hasta {MAX_CASOS_DE_DERIVACION} casos para derivar a una persona")
    if len({c.casefold() for c in limpios}) != len(limpios):
        raise ValueError("Hay un caso para derivar a una persona repetido")
    return limpios


def campo_derivar_cuando() -> Any:
    return Field(
        default_factory=list,
        description=(
            "Derivar a una persona cuando…: casos en los que la IA escala en este motivo "
            f"(hasta {MAX_CASOS_DE_DERIVACION}, de hasta {MAX_LARGO_DE_CASO} caracteres)"
        ),
    )


#: «Mensaje al derivar» del motivo (0.6.15): lo que recibe el cliente cuando la IA de este paso escala a una
#: persona (por un caso de `derivar_cuando` o por un control trigger del agente), EN VEZ del cierre que
#: improvisaría la IA. Lo manda api-chatty al escalar, una vez y tal cual: la IA nunca lo reescribe. Vive al
#: lado de `indicacion` y `derivar_cuando` (`AccionIaResponde`, `AccionAgendar`, `Precalificacion`) y se
#: hereda con la acción. Un único token, `{cuando_atienden}`, que api-chatty resuelve al mandarlo con el
#: horario de la recepción («en unos minutos», «mañana a las 9», «el lunes a las 9», «apenas podamos»).
MAX_LARGO_MENSAJE_AL_DERIVAR = 500
TOKEN_CUANDO_ATIENDEN = "{cuando_atienden}"
_TOKEN = re.compile(r"\{[^{}]*\}")


def limpiar_mensaje_al_derivar(valor: Optional[str]) -> Optional[str]:
    """Sin espacios en los bordes; vacío = None. Hasta `MAX_LARGO_MENSAJE_AL_DERIVAR` caracteres (con el token
    sin resolver) y sin otro `{…}` que `{cuando_atienden}`: un token mal escrito saldría literal al cliente."""
    if valor is None:
        return None
    texto = valor.strip()
    if not texto:
        return None
    if len(texto) > MAX_LARGO_MENSAJE_AL_DERIVAR:
        raise ValueError(f"El mensaje al derivar tiene hasta {MAX_LARGO_MENSAJE_AL_DERIVAR} caracteres")
    if any(t != TOKEN_CUANDO_ATIENDEN for t in _TOKEN.findall(texto)):
        raise ValueError("El mensaje al derivar sólo puede usar {cuando_atienden}")
    return texto


def campo_mensaje_al_derivar() -> Any:
    return Field(
        default=None,
        description=(
            "Mensaje al derivar: lo que recibe el cliente cuando la IA de este motivo lo pasa a una persona "
            f"(hasta {MAX_LARGO_MENSAJE_AL_DERIVAR} caracteres; admite {TOKEN_CUANDO_ATIENDEN})"
        ),
    )


#: «Pasar a otro motivo» (0.6.16): una herramienta de la IA del flujo. En cualquier turno de una acción de IA
#: (`ia_responde`, `agendar`, `Precalificacion`) la IA puede decidir que el cliente en realidad consulta por OTRO
#: motivo y cambiarlo. Ese turno hace SÓLO el cambio (no le escribe al cliente); api-chatty aplica el motivo nuevo
#: (capas de entrada, sus seguimientos, sin su respuesta fija) y pide UN turno nuevo de la IA con las
#: instrucciones del motivo nuevo («venías de X: seguí la charla sin volver a saludar»).
#:
#: `None` = el default por contexto, y el default lo resuelve el runtime, no el modelo: PRENDIDO en «Consulta
#: general» (el chat todavía no tiene un motivo de verdad) y APAGADO en cualquier otro motivo. Como la acción se
#: hereda entera, un motivo que hereda la respuesta de Consulta general hereda también su `cambiar_motivo`
#: explícito; con `None` vale el default del motivo DEL CHAT (`cambiar_motivo_activo`).
#: Tope (api-chatty): `MAX_CAMBIOS_DE_MOTIVO_POR_IA` cambios hechos por la IA por chat en
#: `VENTANA_CAMBIOS_DE_MOTIVO_HORAS`; pasado el tope la herramienta no se ofrece.
MAX_MOTIVOS_PARA_CAMBIAR = 50
MAX_CAMBIOS_DE_MOTIVO_POR_IA = 3
VENTANA_CAMBIOS_DE_MOTIVO_HORAS = 24


class CambiarMotivo(BaseModel):
    """«Pasar a otro motivo» en una acción de IA. `motivo_ids` vacío = cualquier motivo activo que la IA puede
    elegir (`ai_assignable`); con ids, sólo esos (los que estén activos y `ai_assignable` al momento del turno).
    El motivo actual del chat nunca se ofrece."""

    activo: bool = Field(default=True, description="¿La IA puede pasar el chat a otro motivo en este paso?")
    motivo_ids: list[StrObjectId] = Field(
        default_factory=list, description="A cuáles; vacío = a cualquier motivo activo que la IA puede elegir"
    )

    @field_validator("motivo_ids")
    @classmethod
    def _ids(cls, v: list[StrObjectId]) -> list[StrObjectId]:
        if len(v) > MAX_MOTIVOS_PARA_CAMBIAR:
            raise ValueError(f"Hasta {MAX_MOTIVOS_PARA_CAMBIAR} motivos a los que pasar")
        if len({str(i) for i in v}) != len(v):
            raise ValueError("Hay un motivo repetido entre los motivos a los que pasar")
        return v


def campo_cambiar_motivo() -> Any:
    return Field(
        default=None,
        description=(
            "Pasar a otro motivo: si la IA de este paso puede cambiar el motivo del chat. None = por defecto "
            "(prendido en Consulta general, apagado en un motivo)"
        ),
    )


def cambiar_motivo_activo(valor: Optional[CambiarMotivo], *, en_consulta_general: bool) -> bool:
    """¿La herramienta está prendida? Explícito manda; `None` = prendida sólo si el chat está en Consulta
    general."""
    if valor is None:
        return bool(en_consulta_general)
    return bool(valor.activo)


class _AccionBase(BaseModel):
    """Base de toda acción. `tipo` es el discriminador: se serializa SIEMPRE, también con
    exclude_unset (un PATCH que lo omite deja un documento que no se puede volver a leer)."""

    def model_post_init(self, __context: Any) -> None:
        self.model_fields_set.add("tipo")


class AccionRespuestaRapida(_AccionBase):
    tipo: Literal["respuesta_rapida"] = "respuesta_rapida"
    fast_answer_id: StrObjectId
    ia_acompana: bool = Field(
        default=False,
        description=(
            "La IA puede sumar un mensaje antes y otro después de la respuesta rápida "
            "(conectores). Sin esto, la respuesta sale tal cual y la manda api-chatty."
        ),
    )


class AccionIaResponde(_AccionBase):
    tipo: Literal["ia_responde"] = "ia_responde"
    indicacion: str = Field(default="", description="Qué tiene que hacer la IA con este motivo")
    # 0.6.14: «Derivar a una persona cuando…» (ver `limpiar_casos_de_derivacion`).
    derivar_cuando: list[str] = campo_derivar_cuando()
    # 0.6.15: «Mensaje al derivar» (ver `limpiar_mensaje_al_derivar`).
    mensaje_al_derivar: Optional[str] = campo_mensaje_al_derivar()
    # 0.6.16: «Pasar a otro motivo» (ver `CambiarMotivo`).
    cambiar_motivo: Optional[CambiarMotivo] = campo_cambiar_motivo()

    @field_validator("derivar_cuando")
    @classmethod
    def _casos(cls, v: list[str]) -> list[str]:
        return limpiar_casos_de_derivacion(v)

    @field_validator("mensaje_al_derivar")
    @classmethod
    def _mensaje(cls, v: Optional[str]) -> Optional[str]:
        return limpiar_mensaje_al_derivar(v)


class AccionAgendar(_AccionBase):
    tipo: Literal["agendar"] = "agendar"
    chatty_ai_agent_id: Optional[StrObjectId] = Field(
        default=None, description="None = el agente heredado; usa la agenda que ese agente ya tiene"
    )
    # 0.6.9 / 0.5.11: la instrucción del motivo para agendar («ofrecé turnos de tarde», «pedí el
    # barrio»). Vale sólo para este motivo (la IA la recibe en el turno), no es un componente del
    # agente: no afecta a ningún otro chat.
    indicacion: str = Field(default="", description="Cómo tiene que agendar la IA en este motivo")
    # 0.6.14: «Derivar a una persona cuando…» (ver `limpiar_casos_de_derivacion`).
    derivar_cuando: list[str] = campo_derivar_cuando()
    # 0.6.15: «Mensaje al derivar» (ver `limpiar_mensaje_al_derivar`).
    mensaje_al_derivar: Optional[str] = campo_mensaje_al_derivar()
    # 0.6.16: «Pasar a otro motivo» (ver `CambiarMotivo`).
    cambiar_motivo: Optional[CambiarMotivo] = campo_cambiar_motivo()
    # 0.6.57.1: «Recordatorios del turno» del motivo (ver `turno.RecordatoriosDelTurno`). None = vale la
    # config del agente (`pgp_configs.avisos_de_reunion`), como hasta ahora; con valor, gana la del motivo.
    recordatorios: Optional[RecordatoriosDelTurno] = Field(
        default=None,
        description="Recordatorios del turno de este motivo. None = los del agente (pgp_configs.avisos_de_reunion)",
    )

    @field_validator("derivar_cuando")
    @classmethod
    def _casos(cls, v: list[str]) -> list[str]:
        return limpiar_casos_de_derivacion(v)

    @field_validator("mensaje_al_derivar")
    @classmethod
    def _mensaje(cls, v: Optional[str]) -> Optional[str]:
        return limpiar_mensaje_al_derivar(v)


class AccionCrearPendiente(_AccionBase):
    tipo: Literal["crear_pendiente"] = "crear_pendiente"
    titulo: str
    asignar_a_user_id: Optional[StrObjectId] = Field(default=None)

    @field_validator("titulo")
    @classmethod
    def titulo_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El pendiente necesita un título")
        return v.strip()


class AccionPersonalizada(_AccionBase):
    tipo: Literal["accion_personalizada"] = "accion_personalizada"
    capacidad_id: StrObjectId


class AccionNada(_AccionBase):
    tipo: Literal["nada"] = "nada"


class AccionDesconocida(_AccionBase):
    """Un tipo que este pin de letschatty no conoce. Se conserva entero (extra="allow") para que
    leer y volver a guardar no borre nada, y ningún ejecutor lo ejecuta."""

    model_config = ConfigDict(extra="allow")
    tipo: str


def discriminador_con_respaldo(conocidos: frozenset[str]) -> Discriminator:
    def _tipo(v: Any) -> str:
        tipo = v.get("tipo") if isinstance(v, dict) else getattr(v, "tipo", None)
        return tipo if isinstance(tipo, str) and tipo in conocidos else DESCONOCIDA

    return Discriminator(_tipo)


# Lo que puede ir en una rama de precalificación: todo menos precalificar (no se anida).
_TIPOS_DE_RAMA = TIPOS_DE_ACCION - {"precalificar"}

AccionDeRama = Annotated[
    Union[
        Annotated[AccionRespuestaRapida, Tag("respuesta_rapida")],
        Annotated[AccionIaResponde, Tag("ia_responde")],
        Annotated[AccionAgendar, Tag("agendar")],
        Annotated[AccionCrearPendiente, Tag("crear_pendiente")],
        Annotated[AccionPersonalizada, Tag("accion_personalizada")],
        Annotated[AccionNada, Tag("nada")],
        Annotated[SkipJsonSchema[AccionDesconocida], Tag(DESCONOCIDA)],
    ],
    discriminador_con_respaldo(_TIPOS_DE_RAMA),
]

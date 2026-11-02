"""Precalificación: la IA pide datos y/o evalúa un criterio, y sigue por una de dos ramas.

Reemplaza a `ai_agents_v2/pre_qualify_config.py::PreQualifyConfig`, que nada ejecuta. El estado
por chat (pendiente / evaluando / califica / no califica) sigue viviendo en
`ChattyAIAgentInChat.pre_qualify_status`. Los datos se guardan en los campos de formulario del
contacto (`FormField.field_key`), no en el chat.

`objetivo` dice para qué sirve el criterio, y es un literal CERRADO: un valor nuevo exige
actualizar primero al escritor (api-chatty). El campo en sí es tolerante hacia atrás: un documento
sin `objetivo` carga como «negocio», y un lector en un pin anterior lo ignora al leer — pero lo
DESCARTA si vuelve a guardar el documento entero.
"""
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, Tag, field_validator, model_validator
from pydantic.json_schema import SkipJsonSchema

from letschatty.models.utils.types.identifier import StrObjectId

from . import al_responder as _al_responder
from .acciones_basicas import (
    DESCONOCIDA,
    AccionAgendar,
    AccionDeRama,
    AccionDesconocida,
    AccionIaResponde,
    AccionNada,
    CambiarMotivo,
    _AccionBase,
    campo_cambiar_motivo,
    campo_derivar_cuando,
    campo_mensaje_al_derivar,
    discriminador_con_respaldo,
    limpiar_casos_de_derivacion,
    limpiar_mensaje_al_derivar,
)
from .acciones_fijas import AccionesFijas
from .al_responder import AlResponder
from .seguimientos import Seguimientos


class DatoAPedir(BaseModel):
    field_key: str = Field(min_length=1, description="`FormField.field_key` de la empresa")
    obligatorio: bool = True

    @field_validator("field_key")
    @classmethod
    def limpiar_field_key(cls, v: str) -> str:
        # Limpio para que "cuit" y "cuit " cuenten como el mismo dato (y apunten al mismo campo).
        if not v.strip():
            raise ValueError("El dato a pedir necesita un campo")
        return v.strip()


class Rama(BaseModel):
    """Qué pasa después del resultado. Lo que queda en None hereda del motivo, que a su vez
    hereda de «Consulta general»."""

    enviar: AccionDeRama = Field(default_factory=AccionNada)
    seguimientos: Optional[Seguimientos] = None
    al_responder: Optional[AlResponder] = None
    target_funnel_id: Optional[StrObjectId] = None
    target_stage_id: Optional[StrObjectId] = None
    # 0.6.9 / 0.5.11: acciones fijas cuando el cliente responde al mensaje de la rama (una vez, 24 h).
    # NO se hereda del motivo: el del motivo ya se aplicó con la primera respuesta del cliente.
    si_responde: Optional[AccionesFijas] = Field(
        default=None, description="Acciones fijas cuando el cliente responde al mensaje de la rama"
    )
    # 0.6.14: acciones fijas que se aplican EN EL MOMENTO en que corre la rama (la IA decidió califica /
    # no califica; en «sugiere», cuando una persona aprueba), además de lo que manda `enviar`: etiquetas,
    # productos, etapa y/o un pendiente. Como `si_responde`: `{}` no vale (400) y `null` = nada; no se
    # hereda del motivo. La etapa va acá o en `target_funnel_id`/`target_stage_id`, no distinta en los dos.
    acciones: Optional[AccionesFijas] = Field(
        default=None, description="Acciones fijas que se aplican apenas corre la rama"
    )

    @model_validator(mode="after")
    def validar(self) -> "Rama":
        if getattr(self.enviar, "tipo", None) == "precalificar":
            raise ValueError("Una rama no puede precalificar otra vez")
        gestion = self.al_responder.gestion_ia if self.al_responder is not None else None
        if getattr(gestion, "tipo", None) == "precalificar":
            raise ValueError("Una rama no puede precalificar otra vez")
        if self.target_stage_id and not self.target_funnel_id:
            raise ValueError("Para elegir una etapa hace falta el funnel")
        a = self.acciones
        if a is not None and a.target_funnel_id and self.target_funnel_id and (
            (a.target_funnel_id, a.target_stage_id) != (self.target_funnel_id, self.target_stage_id)
        ):
            raise ValueError("La rama ya mueve a otra etapa: elegí la etapa en un solo lugar")
        return self


ObjetivoPrecalificacion = Literal["negocio", "pauta", "ambos"]


class Precalificacion(BaseModel):
    datos: list[DatoAPedir] = Field(default_factory=list)
    criterio: str = Field(default="", description="Vacío = califica al completar los obligatorios")
    # 0.6.9 / 0.5.11: la instrucción del motivo para precalificar («preguntá primero la zona», «no
    # menciones precios»). Vale sólo para este motivo (la IA la recibe en el turno), no es un
    # componente del agente. No reemplaza al criterio: el criterio decide, la indicación dice cómo.
    indicacion: str = Field(default="", description="Cómo tiene que precalificar la IA en este motivo")
    # 0.6.14: «Derivar a una persona cuando…» mientras precalifica (ver `limpiar_casos_de_derivacion`).
    derivar_cuando: list[str] = campo_derivar_cuando()
    # 0.6.15: «Mensaje al derivar» mientras precalifica (ver `limpiar_mensaje_al_derivar`).
    mensaje_al_derivar: Optional[str] = campo_mensaje_al_derivar()
    # 0.6.16: «Pasar a otro motivo» mientras precalifica (ver `CambiarMotivo`).
    cambiar_motivo: Optional[CambiarMotivo] = campo_cambiar_motivo()
    # Para qué precalificás:
    # - «negocio»: el criterio califica para el negocio. Es el comportamiento de antes del campo y
    #   no toca la calidad del lead.
    # - «pauta» / «ambos»: cuando la IA decide `califica`, la rama además marca la calidad del lead
    #   como buena → api-chatty emite `chat.quality_score.good` → QualifiedLead a Meta (uno por
    #   chat). `no_califica` nunca marca calidad (no se manda «malo»: Meta no lo usa).
    # El objetivo no mueve funnel ni etapa por sí mismo: eso sigue siendo lo que diga cada rama.
    objetivo: ObjetivoPrecalificacion = Field(
        default="negocio",
        description="negocio = no toca la calidad; pauta/ambos = la rama califica marca calidad buena (QualifiedLead)",
    )
    califica: Rama = Field(default_factory=Rama)
    no_califica: Rama = Field(default_factory=Rama)

    @field_validator("derivar_cuando")
    @classmethod
    def _casos(cls, v: list[str]) -> list[str]:
        return limpiar_casos_de_derivacion(v)

    @field_validator("mensaje_al_derivar")
    @classmethod
    def _mensaje(cls, v: Optional[str]) -> Optional[str]:
        return limpiar_mensaje_al_derivar(v)

    @model_validator(mode="after")
    def validar(self) -> "Precalificacion":
        if not self.datos and not self.criterio.strip():
            raise ValueError("La precalificación necesita datos o un criterio")
        claves = [d.field_key for d in self.datos]
        if len(claves) != len(set(claves)):
            raise ValueError("Hay un dato repetido")
        return self


class AccionPrecalificar(_AccionBase):
    tipo: Literal["precalificar"] = "precalificar"
    precalificacion: Precalificacion


# «Si responde → Lo gestiona la IA» (`AlResponder.gestion_ia`): las acciones de IA que pueden arrancar
# cuando el cliente responde a la respuesta rápida del motivo. Con respaldo para un tipo nuevo.
TIPOS_DE_GESTION = frozenset({"ia_responde", "precalificar", "agendar"})

AccionDeGestion = Annotated[
    Union[
        Annotated[AccionIaResponde, Tag("ia_responde")],
        Annotated[AccionPrecalificar, Tag("precalificar")],
        Annotated[AccionAgendar, Tag("agendar")],
        Annotated[SkipJsonSchema[AccionDesconocida], Tag(DESCONOCIDA)],
    ],
    discriminador_con_respaldo(TIPOS_DE_GESTION),
]

# El ciclo AlResponder → AccionPrecalificar → Precalificacion → Rama → AlResponder: se inyecta el tipo
# en el módulo de AlResponder (que lo anota como string) y se reconstruyen los cuatro modelos.
_al_responder.AccionDeGestion = AccionDeGestion
AlResponder.model_rebuild(force=True)
Rama.model_rebuild(force=True)
Precalificacion.model_rebuild(force=True)
AccionPrecalificar.model_rebuild(force=True)

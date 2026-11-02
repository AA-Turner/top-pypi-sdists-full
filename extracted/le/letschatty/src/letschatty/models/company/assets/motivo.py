"""El motivo de consulta: por qué escribió esta persona.

Un motivo es una CLASIFICACIÓN, no un procedimiento. Apunta a un workflow, no lo contiene —
porque hay workflows que no son motivos (recuperación de carrito, postventa, cobranza) y
meterlos como motivos falsos arruina el eje sobre el que la empresa quiere reportar.

`tag_id` es el tag espejo: es cómo el resto del sistema lee el motivo. Existe para no tener
que agregar un miembro a `AttributeType`, que es un StrEnum validado — un criterio guardado
con un valor nuevo revienta al parsear en todo servicio parado en un pin viejo de letschatty.
"""
from typing import Any, ClassVar, Optional

from pydantic import Field, field_validator, model_validator

from ...base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from ...utils.types import StrObjectId
from .atencion.accion import Accion
from .atencion.acciones_fijas import AccionesFijas
from .atencion.al_responder import AlResponder, Asignacion, ModoAsignacion
from .atencion.seguimientos import Seguimientos
from .account_scope import normalize_account_ids
from .automation import Automation

# `assets/__init__` hace `from .motivo import *`: sin esto reexportaría Accion, AlResponder,
# Seguimientos, Automation… como si fueran de `letschatty.models.company.assets`.
__all__ = ["Motivo", "MotivoPreview"]


class MotivoPreview(ChattyAssetPreview):
    is_fallback: bool = Field(default=False)
    ai_assignable: bool = Field(default=True)
    active: bool = Field(default=True)
    borrador: bool = Field(default=False)
    # Los lleva el preview porque el listado los MUESTRA: una pantalla de motivos
    # que tuviera que pedir el detalle de cada uno para saber a qué workflow
    # apunta haría N requests para pintar una lista.
    description: str = Field(default="")
    workflow_id: Optional[StrObjectId] = Field(default=None)
    account_ids: list[StrObjectId] = Field(default_factory=list)

    @field_validator("account_ids", mode="before")
    @classmethod
    def _normalize_account_ids(cls, value: Any) -> list[str]:
        return normalize_account_ids(value)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {
            "is_fallback": 1,
            "ai_assignable": 1,
            "active": 1,
            "borrador": 1,
            "description": 1,
            "workflow_id": 1,
            "account_ids": 1,
        }

    @classmethod
    def from_asset(cls, asset: "Motivo") -> "MotivoPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            is_fallback=asset.is_fallback,
            ai_assignable=asset.ai_assignable,
            active=asset.active,
            borrador=asset.borrador,
            description=asset.description,
            workflow_id=asset.workflow_id,
            account_ids=asset.account_ids,
        )


class Motivo(CompanyAssetModel):
    name: str = Field(description="Cómo lo ve la empresa. 'Curso Python Inicial'")
    description: str = Field(
        default="",
        description=(
            "Cuándo aplica este motivo. NO es un campo descriptivo: es el prompt que lee el "
            "clasificador para elegir. Obligatorio si ai_assignable."
        ),
    )
    tag_id: StrObjectId = Field(
        description="El tag espejo que este motivo posee. Es cómo lo lee el resto del sistema."
    )
    workflow_id: Optional[StrObjectId] = Field(
        default=None, description="Qué workflow dispara. Puntero: borrar el motivo no lo borra."
    )
    automation: Optional[Automation] = Field(
        default=None, description="Efectos inmediatos al entrar al motivo"
    )
    product_ids: list[StrObjectId] = Field(default_factory=list)
    is_fallback: bool = Field(
        default=False,
        description=(
            "La red de contención («Consulta general»). Exactamente una por CUENTA de WhatsApp: la "
            "que tiene `account_ids == []` es la de la cuenta por defecto (y la de toda cuenta que "
            "no tenga la suya); la de otra cuenta lleva ESA cuenta en `account_ids`."
        ),
    )
    account_ids: list[StrObjectId] = Field(
        default_factory=list,
        description=(
            "En qué cuentas (números) de WhatsApp vale el motivo. Vacío = en todas, las que se "
            "conecten después incluidas. En Consulta general (is_fallback) no es un alcance: vacío "
            "es la de la cuenta por defecto y una cuenta es la Consulta general de ESA cuenta. "
            "Se valida al ESCRIBIR (api-chatty); al leer se normaliza y no levanta."
        ),
    )
    ai_assignable: bool = Field(
        default=True, description="Si el clasificador lo puede elegir"
    )
    active: bool = Field(default=True)

    # --- Flujo de atención configurable (spec 2026-09-29) ---------------------------------
    # None en un bloque = «como en Consulta general». En Consulta general (is_fallback) lo que
    # falte lo reporta `bloques_sin_definir()`: se exige al ESCRIBIR (api-chatty, /atencion),
    # no al leer, para no romper motivos guardados antes de esta versión.
    bienvenida_fast_answer_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "Bienvenida propia. Pisa la general SÓLO cuando la fuente declara este motivo: por "
            "WhatsApp directo la bienvenida sale antes de clasificar y va la general."
        ),
    )
    respuesta: Optional[Accion] = Field(default=None, description="¿Qué les enviamos?")
    seguimientos: Optional[Seguimientos] = Field(default=None, description="Si no responde")
    al_responder: Optional[AlResponder] = Field(default=None, description="Cuando responde")
    # 0.6.9 / 0.5.11 — «Si responde»: acciones fijas (etiquetas, productos, etapa, pendiente) cuando el
    # cliente responde a la respuesta del motivo. UNA vez por entrada y dentro de las 24 h. NO se
    # hereda de «Consulta general» (None = no hace nada): `AccionesFijas` no tiene un «nada» explícito
    # con el que un motivo pudiera pisar lo heredado.
    si_responde: Optional[AccionesFijas] = Field(
        default=None, description="Acciones fijas cuando el cliente responde a la respuesta del motivo"
    )
    receta_id: Optional[str] = Field(
        default=None, description="De qué receta salió. Informativo: editar no la rompe."
    )
    # 0.6.22 — «Asignar a una persona» AL ENTRAR: apenas el chat entra al motivo (después de lo que se le envía), le
    # queda a una persona fija o al reparto por turnos. No se hereda de «Consulta general» (None = no asigna al
    # entrar). Es otra cosa que `al_responder.asignar` («si la IA necesita a una persona…»), que sigue valiendo para
    # cuando la IA escala; al entrar gana éste. `nadie` no vale: para no asignar, None.
    asignar_al_entrar: Optional[Asignacion] = Field(
        default=None, description="A quién le queda el chat apenas entra al motivo. None = a nadie (como hoy)."
    )
    # 0.6.22 — Un motivo recién creado nace en BORRADOR: inactivo (los chats reales no entran por él) hasta que se
    # completa «¿Qué les enviamos?». Lo escribe sólo api-chatty: al crear (`borrador: true`) y al completarlo o
    # activarlo a mano (lo baja). Con `borrador` el motivo SIEMPRE está inactivo (lo fuerza el validador).
    borrador: bool = Field(
        default=False,
        description="Nació sin respuesta: inactivo hasta completar «¿Qué les enviamos?» (al completarla se activa).",
    )

    preview_class: ClassVar[type[MotivoPreview]] = MotivoPreview

    @field_validator("account_ids", mode="before")
    @classmethod
    def _normalize_account_ids(cls, value: Any) -> list[str]:
        return normalize_account_ids(value)

    @model_validator(mode="after")
    def validate_motivo(self) -> "Motivo":
        if self.ai_assignable and not self.description.strip():
            raise ValueError(
                "description es obligatoria cuando ai_assignable=True: es el prompt del clasificador"
            )
        gestion = self.al_responder.gestion_ia if self.al_responder is not None else None
        if getattr(self.respuesta, "tipo", None) == "precalificar" and getattr(gestion, "tipo", None) == "precalificar":
            raise ValueError(
                "El motivo ya precalifica en la respuesta: «Lo gestiona la IA» no puede precalificar otra vez"
            )
        if self.asignar_al_entrar is not None and self.asignar_al_entrar.modo == ModoAsignacion.NADIE:
            raise ValueError("Asignar al entrar va a una persona o al reparto: para no asignar, sacalo")
        if self.is_fallback:
            self.borrador = False
        if self.borrador:
            self.active = False
        if self.is_fallback:
            self.active = True
            if self.bienvenida_fast_answer_id:
                raise ValueError(
                    "Consulta general no tiene bienvenida propia: su bienvenida es la general"
                )
        return self

    def precalificacion_definida(self) -> Optional[tuple[str, Any]]:
        """(dónde, `Precalificacion`) de la precalificación que ESTE motivo define, o None: la de su
        respuesta (`respuesta.precalificacion`) o la de «Si responde → Lo gestiona la IA»
        (`al_responder.gestion_ia.precalificacion`). No pueden estar las dos (lo valida `validate_motivo`).
        Es lo que identifica a la rama `rama:<id de este motivo>:<califica|no_califica>`."""
        p = getattr(self.respuesta, "precalificacion", None) if getattr(self.respuesta, "tipo", None) == "precalificar" else None
        if p is not None:
            return "respuesta.precalificacion", p
        gestion = self.al_responder.gestion_ia if self.al_responder is not None else None
        if getattr(gestion, "tipo", None) == "precalificar":
            return "al_responder.gestion_ia.precalificacion", gestion.precalificacion
        return None

    def bloques_sin_definir(self) -> list[str]:
        """En Consulta general, lo que todavía no se configuró (es la base de la herencia: no
        puede decir «como en Consulta general»). En cualquier otro motivo, [].

        «Cuando responde» se hereda campo por campo, así que un `al_responder` definido pero a
        medias también falta: se reportan `al_responder.ia` y/o `al_responder.asignar`. El agente
        (`chatty_ai_agent_id`) puede quedar en None."""
        if not self.is_fallback:
            return []
        faltan = [b for b in ("respuesta", "seguimientos", "al_responder") if getattr(self, b) is None]
        if self.al_responder is not None:
            faltan += [f"al_responder.{c}" for c in ("ia", "asignar") if getattr(self.al_responder, c) is None]
        return faltan

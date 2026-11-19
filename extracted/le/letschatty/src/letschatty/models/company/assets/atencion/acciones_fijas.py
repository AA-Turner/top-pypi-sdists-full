"""Acciones fijas: lo que se le hace a un chat sin mandarle nada (plan 7c).

Las usan `Seguimientos.si_responde` (cuando el cliente responde a un seguimiento) y, desde 0.6.9 /
0.5.11, `Motivo.si_responde` y `Rama.si_responde` (cuando el cliente responde a la respuesta del
motivo o de la rama, una sola vez y dentro de las 24 h): se suman etiquetas y productos, se mueve el
chat a una etapa y/o se crea un pendiente (`pendiente_titulo`, para quien tiene el chat). Desde 0.6.14
también `Rama.acciones` (en el momento en que corre la rama, no cuando el cliente responde). Desde 0.6.57
(2026-11-02, QA de Alan: «de última todas las acciones se pueden hacer en un workflow») también se
enganchan workflows (`workflow_ids`): api-chatty los engancha con `link_flow_to_chat` (uno que ya estaba
no se duplica; un chat bloqueado o archivado no recibe ninguno). Desde 0.6.57.2 también se puede
«Calificar lead» (`quality_score`: buena / neutral / mala): api-chatty la aplica con el mismo ejecutor
(`Automation.quality_score`), que además avisa a Meta / Google cuando es «buena» (una vez por chat). Las
aplica api-chatty con el ejecutor de automatizaciones de siempre; copilot no las ve.

Un campo nuevo acá exige actualizar PRIMERO al escritor (api-chatty): un lector en un pin viejo
descarta los campos que no conoce al volver a guardar. Y peor: unas acciones con SÓLO el campo nuevo
(un `si_responde` que únicamente engancha un workflow) le llegan como `{}` y el validador de «al menos
una cosa» LANZA, así que ese motivo deja de poder leerse (falla `/atencion` y la entrada de los chats de
la empresa). Para volver atrás api-chatty, primero sumarles otra acción o borrar el `si_responde`.
Lo mismo vale para `quality_score` (0.6.57.2): orden de deploy letschatty → api-chatty → frontend, y un
`si_responde` con SÓLO la calificación, leído por un pin anterior a 0.6.57.2, deja de poder leerse.
Igual con `identificar_motivo` y `asignar` (0.6.57.7): un `si_responde` de Consulta general con SÓLO «Identificar el motivo»,
leído por un pin anterior, deja de poder leerse.
"""
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from letschatty.models.chat.quality_scoring import QualityScore
from letschatty.models.company.assets.atencion.al_responder import Asignacion, ModoAsignacion
from letschatty.models.utils.types.identifier import StrObjectId


class AccionesFijas(BaseModel):
    tag_ids: list[StrObjectId] = Field(default_factory=list, description="Etiquetas que se suman al chat")
    product_ids: list[StrObjectId] = Field(default_factory=list, description="Productos que se suman al chat")
    target_funnel_id: Optional[StrObjectId] = None
    target_stage_id: Optional[StrObjectId] = None
    pendiente_titulo: Optional[str] = Field(
        default=None,
        description="Crear un pendiente con este título (para quien tiene el chat). None = no crea pendiente",
    )
    workflow_ids: list[StrObjectId] = Field(
        default_factory=list,
        description="Workflows (de la empresa) que se enganchan al chat. Uno que ya estaba no se duplica",
    )
    quality_score: Optional[QualityScore] = Field(
        default=None,
        description="«Calificar lead»: la calidad del lead (buena, neutral o mala). None = no califica",
    )
    # 0.6.57.7 (2026-11-18, pedido de Axel: «no tiene nada que ver quién lo envió con identificarlo y reasignar a la
    # persona»). Sólo en `si_responde` de Consulta general (lo valida `Motivo`): cuando el cliente responde, el
    # clasificador identifica el motivo con lo que escribió y, si encuentra uno, el chat pasa a ese motivo (con lo
    # de ese motivo al entrar). No hace falta una IA que converse. Lo corre api-chatty (docs/atencion.md).
    # 0.6.57.7 — «Asignar a alguien del equipo» cuando responde: una persona fija o el reparto (como
    # `Motivo.asignar_al_entrar`). `nadie` no vale: para no asignar, None. No le saca el chat a otra persona.
    asignar: Optional[Asignacion] = Field(
        default=None, description="A quién le queda el chat cuando responde. None = no asigna",
    )
    identificar_motivo: bool = Field(
        default=False,
        description="«Identificar el motivo y pasarlo»: con la respuesta del cliente, el chat pasa al motivo que corresponda",
    )

    @field_validator("pendiente_titulo")
    @classmethod
    def limpiar_titulo(cls, v: Optional[str]) -> Optional[str]:
        # Vacío es «sin pendiente», no un pendiente sin título.
        return v.strip() or None if isinstance(v, str) else v

    @model_validator(mode="after")
    def validar(self) -> "AccionesFijas":
        if bool(self.target_funnel_id) != bool(self.target_stage_id):
            raise ValueError("Mover a etapa necesita el funnel y la etapa")
        if not (self.tag_ids or self.product_ids or self.target_funnel_id or self.pendiente_titulo
                or self.workflow_ids or self.quality_score or self.identificar_motivo or self.asignar):
            raise ValueError(
                "Elegí al menos una etiqueta, un producto, una etapa, un pendiente, un workflow, una calificación, "
                "a quién asignarlo o identificar el motivo")
        if self.asignar is not None and self.asignar.modo == ModoAsignacion.NADIE:
            raise ValueError("Asignar va a una persona o al reparto: para no asignar, sacalo")
        if len(set(self.tag_ids)) != len(self.tag_ids) or len(set(self.product_ids)) != len(self.product_ids):
            raise ValueError("Hay una etiqueta o un producto repetido")
        if len(set(self.workflow_ids)) != len(self.workflow_ids):
            raise ValueError("Hay un workflow repetido")
        return self

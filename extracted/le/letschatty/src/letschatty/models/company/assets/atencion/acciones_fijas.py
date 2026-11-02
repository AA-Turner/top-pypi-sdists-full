"""Acciones fijas: lo que se le hace a un chat sin mandarle nada (plan 7c).

Las usan `Seguimientos.si_responde` (cuando el cliente responde a un seguimiento) y, desde 0.6.9 /
0.5.11, `Motivo.si_responde` y `Rama.si_responde` (cuando el cliente responde a la respuesta del
motivo o de la rama, una sola vez y dentro de las 24 h): se suman etiquetas y productos, se mueve el
chat a una etapa y/o se crea un pendiente (`pendiente_titulo`, para quien tiene el chat). Desde 0.6.14
también `Rama.acciones` (en el momento en que corre la rama, no cuando el cliente responde). Las aplica
api-chatty con el ejecutor de automatizaciones de siempre; copilot no las ve.

Un campo nuevo acá exige actualizar PRIMERO al escritor (api-chatty): un lector en un pin viejo
descarta los campos que no conoce al volver a guardar.
"""
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

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

    @field_validator("pendiente_titulo")
    @classmethod
    def limpiar_titulo(cls, v: Optional[str]) -> Optional[str]:
        # Vacío es «sin pendiente», no un pendiente sin título.
        return v.strip() or None if isinstance(v, str) else v

    @model_validator(mode="after")
    def validar(self) -> "AccionesFijas":
        if bool(self.target_funnel_id) != bool(self.target_stage_id):
            raise ValueError("Mover a etapa necesita el funnel y la etapa")
        if not (self.tag_ids or self.product_ids or self.target_funnel_id or self.pendiente_titulo):
            raise ValueError("Elegí al menos una etiqueta, un producto, una etapa o un pendiente")
        if len(set(self.tag_ids)) != len(self.tag_ids) or len(set(self.product_ids)) != len(self.product_ids):
            raise ValueError("Hay una etiqueta o un producto repetido")
        return self

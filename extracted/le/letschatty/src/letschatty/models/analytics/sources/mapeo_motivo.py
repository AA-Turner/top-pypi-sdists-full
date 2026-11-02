"""Cómo llegó una fuente a los motivos que declara (`SourceBase.mapeo_motivo`, 0.5.10).

Spec: frontend/docs/superpowers/specs/2026-10-09-lanzamiento-flujo-pagina-completa-y-mapeo.md §4–5.

`Literal` y no `StrEnum` a propósito: un enum nuevo entra al snapshot de valores guardados
(`tests/enum_values_snapshot.json`) sin necesidad.
"""
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

OrigenDeMapeo = Literal["persona", "ia"]
EstadoDeMapeo = Literal["pendiente", "sugerido", "confirmado"]


class MapeoDeMotivo(BaseModel):
    """Quién mapeó la fuente a sus motivos y en qué quedó.

    - `origen="ia"`, `estado="pendiente"`: se le pidió a la IA que lea el anuncio y todavía no
      contestó (o no encontró nada claro). El runtime trata la fuente como sin motivos.
    - `estado="sugerido"`: la IA propuso `motivo_ids` (autocalificada); falta que una persona
      confirme o cambie.
    - `estado="confirmado"`: lo decidió o lo confirmó una persona. La IA nunca pisa un mapeo
      con `origen="persona"`.
    """

    origen: OrigenDeMapeo = Field(description="Quién mapeó: una persona o la IA.")
    estado: EstadoDeMapeo = Field(description="pendiente, sugerido (por la IA) o confirmado.")
    confianza: Optional[float] = Field(
        default=None, ge=0, le=1, description="Confianza de la IA en el primer motivo (0 a 1)."
    )
    razon: Optional[str] = Field(default=None, description="Por qué la IA eligió esos motivos.")
    at: datetime = Field(description="Cuándo se escribió este estado (UTC).")

    @field_validator("at", mode="after")
    @classmethod
    def at_en_utc(cls, valor: datetime) -> datetime:
        """Naive = UTC (lo que devuelve Mongo); con zona, se pasa a UTC."""
        if valor.tzinfo is None:
            return valor.replace(tzinfo=timezone.utc)
        return valor.astimezone(timezone.utc)

"""La entrada: «¿Por dónde entró?». Agrupa fuentes y les aplica lo mismo.

Una entrada NO guarda sus fuentes: la pertenencia vive en `Source.entrada_id` (O(1) en el
runtime) y la API calcula la lista. La `regla` sólo decide a qué entrada caen las fuentes
NUEVAS que no declaran una. La entrada no tiene IA ni agente propio: eso lo decide el motivo.

Spec: frontend/docs/superpowers/specs/2026-10-05-entradas-y-migracion-design.md
"""
from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from ....base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from ....utils.types import StrObjectId
from ..account_scope import applies_to_account, normalize_account_ids

__all__ = ["Entrada", "EntradaPreview", "ReglaDeEntrada"]


class ReglaDeEntrada(BaseModel):
    """Qué fuentes NUEVAS caen solas en esta entrada. Strings, no enums: no entran al snapshot de enums."""

    tipos: list[str] = Field(default_factory=list)  # valores de SourceType (p. ej. "pure_ad")
    categorias: list[str] = Field(default_factory=list)  # SourceBase.category

    def cubre(self, tipo: Optional[str], categoria: Optional[str]) -> bool:
        return bool((tipo and tipo in self.tipos) or (categoria and categoria in self.categorias))


class EntradaPreview(ChattyAssetPreview):
    motivo_id: Optional[StrObjectId] = None

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"motivo_id": 1}

    @classmethod
    def from_asset(cls, asset: "Entrada") -> "EntradaPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            motivo_id=asset.motivo_id,
        )


class Entrada(CompanyAssetModel):
    name: str
    orden: int = Field(default=0)
    regla: Optional[ReglaDeEntrada] = Field(default=None)
    tag_ids: list[StrObjectId] = Field(default_factory=list)
    product_ids: list[StrObjectId] = Field(default_factory=list)
    target_funnel_id: Optional[StrObjectId] = Field(default=None)
    target_stage_id: Optional[StrObjectId] = Field(default=None)
    motivo_id: Optional[StrObjectId] = Field(default=None)
    solo_chats_nuevos: bool = Field(default=False)
    workflow_ids: list[StrObjectId] = Field(default_factory=list)
    account_ids: list[StrObjectId] = Field(
        default_factory=list,
        description=(
            "A qué cuentas (números) de WhatsApp se limita la entrada. Vacío = todas, las que se "
            "conecten después incluidas."
        ),
    )

    preview_class: ClassVar[type[EntradaPreview]] = EntradaPreview

    @field_validator("account_ids", mode="before")
    @classmethod
    def _normalize_account_ids(cls, value: Any) -> list[str]:
        return normalize_account_ids(value)

    def applies_to(self, account_id: Optional[str], default_account_id: Optional[str] = None) -> bool:
        """¿Vale para un chat de esa cuenta? Vacío = sí. Un chat sin cuenta es el de la por defecto."""
        return applies_to_account(self.account_ids, account_id, default_account_id)

    @model_validator(mode="after")
    def validar(self) -> "Entrada":
        if bool(self.target_funnel_id) != bool(self.target_stage_id):
            raise ValueError("tablero y etapa van juntos")
        if not self.name.strip():
            raise ValueError("la entrada necesita un nombre")
        return self

    def hace_algo(self) -> bool:
        return bool(
            self.tag_ids
            or self.product_ids
            or self.target_funnel_id
            or self.motivo_id
            or self.workflow_ids
        )

"""Capacidades a medida: la puerta para integraciones y desarrollos por cliente.

El flujo no sabe cómo se genera un PDF: sabe que existe una capacidad con un ejecutor. La
elige el cliente en el selector de acción (etiqueta «A medida») y la ejecuta un despachador
genérico (cintia-lambdas) hacia un PGP o un Claude Managed Agent.
"""
from typing import Any, ClassVar, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from ....base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel


class EjecutorDeCapacidad(BaseModel):
    tipo: Literal["pgp", "cma"]
    pgp_url: Optional[str] = None
    cma_id: Optional[str] = None

    @model_validator(mode="after")
    def coincide(self) -> "EjecutorDeCapacidad":
        if self.tipo == "pgp" and (not self.pgp_url or self.cma_id):
            raise ValueError("Un ejecutor pgp lleva pgp_url y nada más")
        if self.tipo == "cma" and (not self.cma_id or self.pgp_url):
            raise ValueError("Un ejecutor cma lleva cma_id y nada más")
        return self


class CapacidadPreview(ChattyAssetPreview):
    activa: bool = Field(default=True)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"activa": 1}

    @classmethod
    def from_asset(cls, asset: "Capacidad") -> "CapacidadPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            activa=asset.activa,
        )


class Capacidad(CompanyAssetModel):
    name: str = Field(description="Cómo la ve el cliente en el selector. 'Cotización en PDF'")
    ejecutor: EjecutorDeCapacidad
    activa: bool = Field(default=True)

    preview_class: ClassVar[type[CapacidadPreview]] = CapacidadPreview

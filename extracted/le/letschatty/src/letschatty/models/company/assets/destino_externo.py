"""Destino externo: «a dónde mandamos» las acciones externas de una empresa (0.6.57.1).

Diseño: api-chatty `docs/precalificacion-con-accion-externa.md` §4.1 y §4.6 (doc de este repo:
`docs/acciones-externas.md`). Colección `destinos_externos`.

Lo crea un Admin u Owner de la empresa (módulo INTEGRATIONS) desde Integraciones. El secreto lo genera
Chatty (32 bytes, prefijo `whsec_`, Standard Webhooks), se muestra UNA vez y se guarda CIFRADO (no
hasheado: hay que firmar con él). Al rotarlo, el anterior sigue firmando hasta `rota_hasta` (24 h): cada
envío lleva las dos firmas.

Acá sólo se validan las reglas ESTÁTICAS de la URL (https, puerto 443, sin usuario ni fragmento). El
filtro de SSRF de verdad (resolver el DNS en cada envío y rechazar IPs privadas, loopback, link-local,
CGNAT y la VPC; sin redirects; conexión fijada a la IP validada) lo hace api-chatty al mandar.

Los secretos cifrados nunca salen en el volcado para el frontend ni para la API (`exclude_fields`):
sólo el de base de datos los lleva.
"""
from datetime import datetime
from typing import Any, ClassVar, Optional
from urllib.parse import urlsplit

from pydantic import Field, field_validator, model_validator

from ...base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from ...utils.types import StrObjectId
from ...utils.types.serializer_type import SerializerType

__all__ = ["DestinoExterno", "DestinoExternoPreview", "validar_url_de_destino"]

#: Prefijo del secreto (Standard Webhooks). Lo genera api-chatty; este modelo guarda sólo el cifrado.
PREFIJO_SECRETO = "whsec_"
TIMEOUT_MIN_S = 1
TIMEOUT_MAX_S = 15
TIMEOUT_DEFAULT_S = 10
MAX_LARGO_URL = 2048
#: Cuánto firma el secreto anterior después de una rotación.
HORAS_DE_DOBLE_FIRMA = 24

_SECRETOS = {"secreto_cifrado", "secreto_anterior_cifrado"}


def validar_url_de_destino(url: str) -> str:
    """Las reglas estáticas de una URL de destino (y de una imagen de la respuesta): https, puerto 443
    (o sin puerto), con host, sin usuario/contraseña ni fragmento. Devuelve la URL sin espacios en los
    bordes. NO resuelve el DNS: eso lo hace api-chatty en cada envío."""
    url = (url or "").strip()
    if not url:
        raise ValueError("La URL es obligatoria")
    if len(url) > MAX_LARGO_URL:
        raise ValueError(f"La URL tiene hasta {MAX_LARGO_URL} caracteres")
    if any(c.isspace() for c in url):
        raise ValueError("La URL no puede tener espacios")
    partes = urlsplit(url)
    if partes.scheme.lower() != "https":
        raise ValueError("La URL tiene que ser https")
    if not partes.hostname:
        raise ValueError("La URL necesita un dominio")
    if partes.username is not None or partes.password is not None:
        raise ValueError("La URL no puede llevar usuario ni contraseña")
    try:
        puerto = partes.port
    except ValueError:
        raise ValueError("El puerto de la URL no es válido") from None
    if puerto not in (None, 443):
        raise ValueError("La URL tiene que usar el puerto 443")
    if partes.fragment:
        raise ValueError("La URL no puede llevar #fragmento")
    return url


class DestinoExternoPreview(ChattyAssetPreview):
    url: str = Field(default="")
    activo: bool = Field(default=True)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"url": 1, "activo": 1}

    @classmethod
    def from_asset(cls, asset: "DestinoExterno") -> "DestinoExternoPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            url=asset.url,
            activo=asset.activo,
        )


class DestinoExterno(CompanyAssetModel):
    name: str = Field(min_length=1, max_length=120, description="Cómo lo ve la empresa: «Entradas UTN.LABS»")
    url: str = Field(description="https, puerto 443, sin usuario")
    secreto_cifrado: Optional[str] = Field(
        default=None, description="El secreto de firma, CIFRADO. Sólo en la base: nunca sale al frontend ni a la API"
    )
    secreto_anterior_cifrado: Optional[str] = Field(
        default=None, description="El secreto de antes de la última rotación, CIFRADO; firma hasta `rota_hasta`"
    )
    rota_hasta: Optional[datetime] = Field(
        default=None, description="Hasta cuándo firma también el secreto anterior (24 h después de rotar)"
    )
    timeout_s: int = Field(default=TIMEOUT_DEFAULT_S, ge=TIMEOUT_MIN_S, le=TIMEOUT_MAX_S)
    activo: bool = Field(default=True)
    creado_por: Optional[StrObjectId] = Field(default=None, description="El usuario que lo creó")

    preview_class: ClassVar[type[DestinoExternoPreview]] = DestinoExternoPreview
    database_datetime_fields: ClassVar[set[str]] = {"rota_hasta"}
    exclude_fields: ClassVar[dict[SerializerType, set[str]]] = {
        SerializerType.FRONTEND: _SECRETOS,
        SerializerType.FRONTEND_ASSET_PREVIEW: _SECRETOS,
        SerializerType.API: _SECRETOS,
    }

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        v = " ".join(v.split())
        if not v:
            raise ValueError("El destino necesita un nombre")
        return v

    @field_validator("url")
    @classmethod
    def _url(cls, v: str) -> str:
        return validar_url_de_destino(v)

    @model_validator(mode="after")
    def _rotacion(self) -> "DestinoExterno":
        if (self.secreto_anterior_cifrado is None) != (self.rota_hasta is None):
            raise ValueError("El secreto anterior va con su `rota_hasta` (y al revés)")
        if self.secreto_anterior_cifrado is not None and self.secreto_cifrado is None:
            raise ValueError("No hay secreto anterior sin un secreto actual")
        return self

    @property
    def tiene_secreto(self) -> bool:
        return bool(self.secreto_cifrado)

    def secretos_que_firman(self, ahora: datetime) -> list[str]:
        """Los secretos CIFRADOS con los que se firma un envío en `ahora`: el actual y, durante la
        rotación, también el anterior. Descifrarlos es cosa de api-chatty."""
        secretos = [self.secreto_cifrado] if self.secreto_cifrado else []
        if self.secreto_anterior_cifrado and self.rota_hasta is not None and ahora < self.rota_hasta:
            secretos.append(self.secreto_anterior_cifrado)
        return secretos

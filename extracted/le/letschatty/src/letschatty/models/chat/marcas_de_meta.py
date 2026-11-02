"""Marcas del contacto que pone Meta (plantillas no entregadas, Prioridad 1 etapa 3; ver api-chatty
docs/plantillas-no-entregadas.md).

Una marca NO dice cómo es el contacto: dice qué contestó Meta y cuándo. Es una copia con vencimiento de lo
que sabe Meta, que es la fuente de verdad (decisión de Alan y el PM, 2026-10-23):

- «Sin WhatsApp» (131026): queda afuera de las campañas 30 días; vencida, la próxima campaña lo vuelve a
  probar; si Meta lo rechaza otra vez, 90 días. Se borra antes si la persona escribe, si le llega
  cualquier mensaje o si se edita su teléfono.
- «No quiere marketing» (131050): afuera de las campañas de MARKETING 90 días, después se vuelve a probar
  igual. Se borra antes sólo si le llega una plantilla de marketing (que escriba no levanta su baja en Meta).
- Siempre se puede quitar a mano.

Vive como «No contactar»: en la persona (`clients.marcas_de_meta.<tipo>`) y copiada en la preview de cada
uno de sus chats (`chats.client.marcas_de_meta.<tipo>`), que es lo que filtran la bandeja y las audiencias.
La escribe SÓLO `ClientCollection.set_marca_de_meta`. Vencida se queda guardada (es lo que cuenta `veces`
para el plazo largo) pero no vale: quien filtra mira `vence > ahora`.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from enum import StrEnum
from typing import Dict, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator


class TipoDeMarca(StrEnum):
    SIN_WHATSAPP = "sin_whatsapp"
    NO_QUIERE_MARKETING = "no_quiere_marketing"


TIPO_POR_CODIGO: Dict[int, TipoDeMarca] = {
    131026: TipoDeMarca.SIN_WHATSAPP,
    131050: TipoDeMarca.NO_QUIERE_MARKETING,
}

#: Plazo de la primera marca y el de una que se repite después de vencer.
PLAZO_PRIMERA: Dict[TipoDeMarca, timedelta] = {
    TipoDeMarca.SIN_WHATSAPP: timedelta(days=30),
    TipoDeMarca.NO_QUIERE_MARKETING: timedelta(days=90),
}
PLAZO_REPETIDA: Dict[TipoDeMarca, timedelta] = {
    TipoDeMarca.SIN_WHATSAPP: timedelta(days=90),
    TipoDeMarca.NO_QUIERE_MARKETING: timedelta(days=90),
}

TITULO: Dict[TipoDeMarca, str] = {
    TipoDeMarca.SIN_WHATSAPP: "Sin WhatsApp",
    TipoDeMarca.NO_QUIERE_MARKETING: "No quiere marketing",
}


def _utc(valor: datetime) -> datetime:
    # Mongo devuelve fechas sin zona (en UTC): compararlas con una con zona explota.
    return valor if valor.tzinfo else valor.replace(tzinfo=ZoneInfo("UTC"))


def tipo_de_marca(codigo: Optional[int]) -> Optional[TipoDeMarca]:
    """El tipo de marca que pone un código de Meta, o None si ese código no marca al contacto."""
    try:
        return TIPO_POR_CODIGO.get(int(codigo)) if codigo is not None else None
    except (TypeError, ValueError):
        return None


class MarcaDeMeta(BaseModel):
    tipo: TipoDeMarca
    codigo: int = Field(description="El código de Meta que la puso (131026, 131050)")
    desde: datetime = Field(description="El rechazo que abrió esta marca (UTC)")
    ultimo_rechazo: datetime = Field(description="El último rechazo de Meta por este motivo (UTC)")
    vence: datetime = Field(description="Hasta cuándo vale; después se vuelve a probar (UTC)")
    veces: int = Field(default=1, description="Cuántas veces seguidas Meta lo rechazó al volver a probar")

    @field_validator("desde", "ultimo_rechazo", "vence")
    @classmethod
    def _en_utc(cls, valor: datetime) -> datetime:
        return _utc(valor)

    def vigente(self, ahora: datetime) -> bool:
        return self.vence > _utc(ahora)

    @classmethod
    def por_rechazo(cls, tipo: TipoDeMarca, codigo: int, ahora: datetime,
                    previa: Optional["MarcaDeMeta"] = None) -> "MarcaDeMeta":
        """La marca después de un rechazo de Meta.

        Con una marca vigente (se mandó igual, «incluirlos igual»), sólo se anota el rechazo: el plazo no se
        estira. Con una vencida, Meta lo volvió a rechazar al probar: marca nueva con el plazo largo. Sin
        marca previa: la primera, con el plazo corto."""
        ahora = _utc(ahora)
        if previa is not None and previa.vigente(ahora):
            return previa.model_copy(update={"ultimo_rechazo": ahora})
        veces = previa.veces + 1 if previa is not None else 1
        plazo = PLAZO_PRIMERA[tipo] if veces == 1 else PLAZO_REPETIDA[tipo]
        return cls(tipo=tipo, codigo=codigo, desde=ahora, ultimo_rechazo=ahora, vence=ahora + plazo, veces=veces)


def marcas_vigentes(marcas: Optional[Dict[str, MarcaDeMeta]], ahora: datetime) -> Dict[str, MarcaDeMeta]:
    return {tipo: marca for tipo, marca in (marcas or {}).items() if marca.vigente(ahora)}

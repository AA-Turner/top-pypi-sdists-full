"""Por qué Meta no entregó una plantilla, en castellano y con qué hacer.

Meta avisa con un status `failed` y un código. Los más comunes en prod (7 días al 2026-10-22, ~400 por
día, casi todos de campañas): 131049 tope de marketing por persona 66%, 131026 sin WhatsApp 21%,
130472 grupo de control de Meta 6%, 131048 número limitado por spam 5%, 131050 la persona bajó el
marketing 1%. Una sola tabla para el aviso del chat, el resultado de la campaña y las marcas del
contacto: si cambia un texto, cambia en los tres.

`cuenta_como_falla`: el grupo de control (130472) no es falla de nadie; la campaña lo muestra aparte.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Dict, Optional

from pydantic import BaseModel


class MotivoDeNoEntrega(StrEnum):
    TOPE_DE_MARKETING = "tope_de_marketing"
    SIN_WHATSAPP = "sin_whatsapp"
    GRUPO_DE_CONTROL = "grupo_de_control"
    NO_QUIERE_MARKETING = "no_quiere_marketing"
    NUMERO_LIMITADO = "numero_limitado"
    PROBLEMA_DE_PAGO = "problema_de_pago"
    OTRO = "otro"


@dataclass(frozen=True)
class DescripcionDeMotivo:
    texto: str
    """Para el aviso del chat y el detalle del destinatario: qué pasó."""
    que_hacer: str
    cuenta_como_falla: bool = True


MOTIVO_POR_CODIGO: Dict[int, MotivoDeNoEntrega] = {
    131049: MotivoDeNoEntrega.TOPE_DE_MARKETING,
    131026: MotivoDeNoEntrega.SIN_WHATSAPP,
    130472: MotivoDeNoEntrega.GRUPO_DE_CONTROL,
    131050: MotivoDeNoEntrega.NO_QUIERE_MARKETING,
    131048: MotivoDeNoEntrega.NUMERO_LIMITADO,
    131042: MotivoDeNoEntrega.PROBLEMA_DE_PAGO,
}

DESCRIPCIONES: Dict[MotivoDeNoEntrega, DescripcionDeMotivo] = {
    MotivoDeNoEntrega.TOPE_DE_MARKETING: DescripcionDeMotivo(
        texto="Meta no lo entregó: esta persona ya recibió muchos mensajes de marketing (de todas las empresas).",
        que_hacer="Se puede volver a intentar mañana."),
    MotivoDeNoEntrega.SIN_WHATSAPP: DescripcionDeMotivo(
        texto="Meta no lo entregó: el número no tiene WhatsApp o no puede recibir mensajes.",
        que_hacer="Revisá que el número esté bien escrito."),
    MotivoDeNoEntrega.GRUPO_DE_CONTROL: DescripcionDeMotivo(
        texto="Meta no lo entregó: esta persona está en un grupo de control de Meta que no recibe marketing.",
        que_hacer="No es una falla: Meta deja a algunas personas sin marketing para medir.",
        cuenta_como_falla=False),
    MotivoDeNoEntrega.NO_QUIERE_MARKETING: DescripcionDeMotivo(
        texto="Meta no lo entregó: esta persona pidió no recibir ofertas de esta empresa.",
        que_hacer="No le mandes marketing; los mensajes de utilidad sí le llegan."),
    MotivoDeNoEntrega.NUMERO_LIMITADO: DescripcionDeMotivo(
        texto="Meta no lo entregó: está limitando el número de la empresa por reportes o bloqueos.",
        que_hacer="Bajá el volumen de marketing y revisá tus plantillas."),
    MotivoDeNoEntrega.PROBLEMA_DE_PAGO: DescripcionDeMotivo(
        texto="Meta no lo entregó: la cuenta de WhatsApp tiene un problema de pago.",
        que_hacer="Revisá el método de pago en Meta Business."),
    MotivoDeNoEntrega.OTRO: DescripcionDeMotivo(
        texto="Meta no lo entregó.",
        que_hacer="Revisá el detalle de Meta."),
}


def motivo_de_no_entrega(codigo: Optional[int]) -> MotivoDeNoEntrega:
    if codigo is None:
        return MotivoDeNoEntrega.OTRO
    return MOTIVO_POR_CODIGO.get(codigo, MotivoDeNoEntrega.OTRO)


def descripcion_de(motivo: MotivoDeNoEntrega) -> DescripcionDeMotivo:
    return DESCRIPCIONES[motivo]


def texto_de_no_entrega(codigo: Optional[int], detalle_de_meta: Optional[str] = None) -> str:
    """«<qué pasó> <qué hacer>». Con un código que no conocemos, va lo que dijo Meta, tal cual."""
    motivo = motivo_de_no_entrega(codigo)
    d = descripcion_de(motivo)
    if motivo == MotivoDeNoEntrega.OTRO:
        crudo = (detalle_de_meta or "").strip()
        sufijo = f" Código {codigo}" if codigo is not None else ""
        if crudo:
            return f"{d.texto}{sufijo}: {crudo}"
        return f"{d.texto[:-1]}{sufijo}." if sufijo else d.texto
    return f"{d.texto} {d.que_hacer}"


class NoEntrega(BaseModel):
    """Lo que se guarda en el mensaje (`messages.$.no_entrega`) cuando Meta no lo entregó.

    Ya calculado, para que quien lee el mensaje crudo de Mongo (campaigns-lambda, que no usa este
    paquete) no tenga que repetir la tabla."""
    motivo: MotivoDeNoEntrega
    codigo: Optional[int] = None
    texto: str
    cuenta_como_falla: bool = True

    @classmethod
    def desde_error(cls, codigo: Optional[int], detalle_de_meta: Optional[str] = None) -> "NoEntrega":
        motivo = motivo_de_no_entrega(codigo)
        return cls(motivo=motivo, codigo=codigo, texto=texto_de_no_entrega(codigo, detalle_de_meta),
                   cuenta_como_falla=descripcion_de(motivo).cuenta_como_falla)

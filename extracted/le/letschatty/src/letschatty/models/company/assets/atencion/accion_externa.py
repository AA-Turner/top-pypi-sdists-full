"""Acción externa de una rama: avisarle a un sistema del cliente (0.6.57.1).

Diseño: api-chatty `docs/precalificacion-con-accion-externa.md` §4.1 (doc de este repo:
`docs/acciones-externas.md`).

`Rama.accion_externa` dispara un POST firmado (Standard Webhooks) a un `DestinoExterno` de la empresa
cuando corre la rama (`al_aprobar`) o cuando la Agendadora reservó un turno (`al_agendar`, sólo si la
rama agenda). La respuesta del sistema externo (mensajes, etiquetas, datos) vuelve al chat. Es un campo
propio de la rama y no un tipo de `enviar` ni de `AccionesFijas`: convive con los dos.

Lo ejecuta SÓLO api-chatty (una implementación de firma, reintentos y log); copilot nunca habla con la
URL del cliente. Un campo nuevo acá exige actualizar primero al escritor (api-chatty): un lector en un pin
viejo descarta los campos que no conoce al volver a guardar la rama.
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from letschatty.models.utils.types.identifier import StrObjectId

#: Cuándo sale: al aprobarse la rama (la IA decidió y, en «sugiere», una persona aprobó) o después de
#: que la Agendadora reservó el turno (con el turno en el payload). Una de las dos en v1.
CuandoAccionExterna = Literal["al_aprobar", "al_agendar"]
#: Si fallan todos los reintentos: siempre hay aviso en el chat; «asignar» además pasa el chat a una
#: persona (la de «Cuando responde → ¿a quién le queda?»).
SiFallaAccionExterna = Literal["avisar", "asignar"]

#: Hasta cuántos datos del contacto viajan.
MAX_DATOS_DE_LA_ACCION = 30


class AccionExterna(BaseModel):
    destino_id: StrObjectId = Field(description="El `DestinoExterno` de la empresa al que se avisa")
    cuando: CuandoAccionExterna = Field(
        default="al_aprobar", description="al_aprobar = cuando corre la rama; al_agendar = cuando la IA reservó el turno"
    )
    datos: Optional[list[str]] = Field(
        default=None,
        description="Qué datos del contacto van (field_key). None = los de la precalificación. Nada del historial",
    )
    esperar_respuesta: bool = Field(
        default=True,
        description="El «enviar» de la rama espera la respuesta del sistema externo (hasta 30 s) antes de salir",
    )
    si_falla: SiFallaAccionExterna = Field(
        default="avisar", description="avisar = aviso en el chat; asignar = aviso y el chat pasa a una persona"
    )

    @field_validator("datos")
    @classmethod
    def _datos(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return None
        limpios = [d.strip() for d in v]
        if any(not d for d in limpios):
            raise ValueError("Un dato de la acción externa necesita un campo")
        if not limpios:
            raise ValueError("Elegí al menos un dato, o dejalo vacío (null) para mandar los de la precalificación")
        if len(limpios) > MAX_DATOS_DE_LA_ACCION:
            raise ValueError(f"Hasta {MAX_DATOS_DE_LA_ACCION} datos por acción externa")
        if len(set(limpios)) != len(limpios):
            raise ValueError("Hay un dato repetido en la acción externa")
        return limpios

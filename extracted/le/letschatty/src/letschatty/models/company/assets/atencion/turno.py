"""Agendar desde el motivo: los recordatorios del turno y el aviso de fin de turno (0.6.57.1).

Diseño: api-chatty `docs/precalificacion-con-accion-externa.md` §4.8 (doc de este repo:
`docs/acciones-externas.md`).

- `RecordatoriosDelTurno` vive en `AccionAgendar.recordatorios`. Tiene la forma de
  `pgp_configs.avisos_de_reunion` del agente (cintia-lambdas `avisos_de_reunion.py`) para reusar ese
  código. Precedencia: lo del motivo gana; sin `recordatorios` en el motivo vale la config del agente.
- `AvisoFinDeTurnoAgendar` es lo que manda `responder-calendar` (cintia-lambdas) a
  `POST …/atencion/ia/chat/{chat_id}` al cerrar un turno de agendar, con el `Turno` reservado. Con eso
  api-chatty cierra el estado de atención (hoy queda `activa` 7 días) y dispara la acción externa
  `al_agendar` si la rama la tiene.

Este módulo no importa nada del flujo (lo importa `acciones_basicas`): así no hay ciclo.
"""
import re
from datetime import datetime
from typing import Literal, Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, Field, field_validator, model_validator

#: Hasta cuántos avisos por turno (los de `avisos_de_reunion` del agente también son hasta 4).
MAX_AVISOS_DEL_TURNO = 4
#: Cuánto antes del turno sale un aviso, en minutos: de 15 minutos a 30 días.
MIN_ANTES_MIN = 15
MAX_ANTES_MIN = 43200
#: El texto libre de un aviso (si la ventana de 24 h está abierta al dispararse). Mismo tope que un
#: mensaje de texto de WhatsApp.
MAX_LARGO_TEXTO_DEL_AVISO = 4096
#: Variables de la plantilla que salen del TURNO. Cualquier otra tiene que ser un `field_key` del
#: contacto (lo que juntó la precalificación).
VARIABLES_DEL_TURNO = frozenset({"nombre", "fecha", "horario", "link"})
#: Un `field_key` como lo normaliza `FormField` (minúsculas, números y guion bajo).
_FIELD_KEY = re.compile(r"^[a-z0-9_]{1,64}$")
#: Una variable posicional de plantilla de Meta: «1», «2»…
_POSICION = re.compile(r"^[1-9][0-9]?$")
#: En el texto libre: `{{1}}`, `{{nombre}}` o `{{<field_key>}}`.
_VARIABLE_EN_TEXTO = re.compile(r"\{\{\s*([^{}]*?)\s*\}\}")


def _es_variable_valida(valor: str) -> bool:
    return valor in VARIABLES_DEL_TURNO or bool(_FIELD_KEY.match(valor))


class PlantillaDelAviso(BaseModel):
    """La plantilla de WhatsApp que sale si la ventana de 24 h está cerrada (siempre hace falta: un
    recordatorio suele salir un día después de la última charla). Que exista y esté aprobada en la
    cuenta del motivo lo valida api-chatty al guardar."""

    nombre: str = Field(min_length=1, max_length=512, description="El nombre de la plantilla en Meta")
    idioma: str = Field(default="es", min_length=2, max_length=15, description="Código de idioma de Meta (es, es_AR, en_US)")

    @field_validator("nombre", "idioma")
    @classmethod
    def _limpiar(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("La plantilla necesita nombre e idioma")
        return v


class AvisoDelTurno(BaseModel):
    antes_min: int = Field(ge=MIN_ANTES_MIN, le=MAX_ANTES_MIN, description="Cuántos minutos antes del turno sale")
    plantilla: PlantillaDelAviso
    texto: Optional[str] = Field(
        default=None,
        description=(
            "Opcional: si al dispararse la ventana de 24 h está abierta, sale este texto en vez de la plantilla. "
            "Admite {{nombre}}, {{fecha}}, {{horario}}, {{link}} y {{<field_key>}}"
        ),
    )
    variables: dict[str, str] = Field(
        default_factory=dict,
        description='Las variables de la plantilla, por posición: {"1": "nombre", "2": "fecha", "3": "<field_key>"}',
    )

    @field_validator("texto")
    @classmethod
    def _texto(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if len(v) > MAX_LARGO_TEXTO_DEL_AVISO:
            raise ValueError(f"El texto del recordatorio tiene hasta {MAX_LARGO_TEXTO_DEL_AVISO} caracteres")
        for nombre in _VARIABLE_EN_TEXTO.findall(v):
            if not _es_variable_valida(nombre):
                raise ValueError(f"El texto del recordatorio usa una variable que no existe: {{{{{nombre}}}}}")
        return v

    @field_validator("variables")
    @classmethod
    def _variables(cls, v: dict[str, str]) -> dict[str, str]:
        limpias: dict[str, str] = {}
        for posicion, valor in v.items():
            posicion = str(posicion).strip()
            valor = str(valor).strip()
            if not _POSICION.match(posicion):
                raise ValueError(f"La variable de la plantilla va por posición («1», «2»…), no «{posicion}»")
            if not _es_variable_valida(valor):
                raise ValueError(
                    f"La variable {posicion} tiene que ser nombre, fecha, horario, link o un campo del contacto, no «{valor}»"
                )
            limpias[posicion] = valor
        posiciones = sorted(int(p) for p in limpias)
        if posiciones != list(range(1, len(posiciones) + 1)):
            raise ValueError("Las variables de la plantilla van de la 1 en adelante, sin saltear ninguna")
        return {str(p): limpias[str(p)] for p in posiciones}


class RecordatoriosDelTurno(BaseModel):
    """«Recordatorios del turno» de un `agendar`. `avisos` vacío + `pendiente` = sólo el pendiente."""

    pendiente: bool = Field(default=True, description="Crear el pendiente del turno en el chat para el equipo")
    avisos: list[AvisoDelTurno] = Field(
        default_factory=list, description=f"Los recordatorios al cliente, hasta {MAX_AVISOS_DEL_TURNO}"
    )

    @model_validator(mode="after")
    def _validar(self) -> "RecordatoriosDelTurno":
        if len(self.avisos) > MAX_AVISOS_DEL_TURNO:
            raise ValueError(f"Hasta {MAX_AVISOS_DEL_TURNO} recordatorios por turno")
        antes = [a.antes_min for a in self.avisos]
        if len(antes) != len(set(antes)):
            raise ValueError("Hay dos recordatorios a la misma distancia del turno")
        if not self.pendiente and not self.avisos:
            raise ValueError("Los recordatorios necesitan el pendiente o al menos un aviso: para no recordar nada, sacalos")
        return self


class Turno(BaseModel):
    """El turno que reservó la IA agendadora. `evento_id` es el del calendario (Google): lleva el
    `chat_id`, así un chat tiene un turno y un reintento no lo duplica."""

    inicio: datetime
    fin: datetime
    zona: str = Field(description="Zona horaria IANA del turno, p. ej. America/Argentina/Buenos_Aires")
    calendario: Optional[str] = Field(default=None, description="El id del calendario donde quedó")
    evento_id: Optional[str] = Field(default=None, description="El id del evento en el calendario")

    @field_validator("zona")
    @classmethod
    def _zona(cls, v: str) -> str:
        v = v.strip()
        try:
            ZoneInfo(v)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError(f"Zona horaria desconocida: «{v}»") from None
        return v

    @model_validator(mode="after")
    def _orden(self) -> "Turno":
        if (self.inicio.tzinfo is None) != (self.fin.tzinfo is None):
            raise ValueError("El inicio y el fin del turno van los dos con zona o los dos sin")
        if self.fin <= self.inicio:
            raise ValueError("El turno termina después de empezar")
        return self


AccionDelTurnoDeAgendar = Literal["AGENDADO", "DERIVADO", "NO_QUISO", "SIGUE"]


class AvisoFinDeTurnoAgendar(BaseModel):
    """Lo que avisa `responder-calendar` al cerrar un turno de agendar (por la misma ruta que la
    unificada: `POST …/atencion/ia/chat/{chat_id}`).

    - `AGENDADO`: reservó; `turno` obligatorio. api-chatty cierra el estado, guarda el turno y dispara la
      acción externa `al_agendar`.
    - `DERIVADO`: pasó a una persona (un caso de `derivar_cuando`); `NO_QUISO`: el cliente no quiso turno.
      Los dos cierran el estado y aplican lo de la rama para ese caso.
    - `SIGUE`: el turno de la IA terminó pero la charla de agendar sigue (no cierra nada).
    """

    tipo: Literal["agendar"] = "agendar"
    accion: AccionDelTurnoDeAgendar
    turno: Optional[Turno] = None
    razon: str = Field(default="", max_length=1000, description="Por qué terminó así, en una línea (para el log)")

    @model_validator(mode="after")
    def _validar(self) -> "AvisoFinDeTurnoAgendar":
        if self.accion == "AGENDADO" and self.turno is None:
            raise ValueError("Un aviso AGENDADO trae el turno")
        if self.accion != "AGENDADO" and self.turno is not None:
            raise ValueError("Sólo un aviso AGENDADO trae turno")
        return self

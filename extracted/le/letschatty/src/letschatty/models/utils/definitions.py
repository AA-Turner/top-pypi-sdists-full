from enum import StrEnum
import logging
import os
from typing import Annotated, Any, Optional

from pydantic import BeforeValidator

_logger = logging.getLogger(__name__)

class Environment(StrEnum):
    PRODUCTION = "PROD"
    DEVELOPMENT = "DEV"
    LOCAL = "LOCAL"

class Area(StrEnum):
    # `FOLLOW_UP = "FOLLOW UP"` se sacó en 0.4.563 (plan 9 del flujo de atención): nadie la usaba
    # (prod 2026-10-02: 0 chats con esa área en las 426 empresas, contado por índice
    # `company_id + area`). «Está en seguimiento» ahora es `Chat.seguimiento_estado`, que no es un
    # área. ⚠️ No se contaron los OTROS documentos que guardan un `Area` y dos estrategias de
    # seguimiento quedaron ilegibles en prod (2026-10-06). Desde 0.5.5 todo campo persistido de
    # tipo `Area` lee los valores sacados (ver `AREAS_SACADAS` abajo). NO volver a agregarlo.
    WAITING_AGENT = "WAITING AGENT"
    WITH_AGENT = "WITH AGENT"
    ARCHIVED = "ARCHIVED"
    BLOCKED = "BLOCKED"
    INBOX = "INBOX"

    @classmethod
    def list_all(cls) -> list[str]:
        return [area.value for area in cls]


# ── Valores que se sacaron de `Area` y cómo se leen hoy ─────────────────────────────────────
# `Area` se guarda en muchos documentos (chats, estrategias de seguimiento, automatizaciones,
# campañas, eventos...). Sacar un miembro del enum NO borra el valor de esos documentos: sin un
# lector tolerante, el documento deja de poder leerse (incidente 2026-10-06: dos estrategias de
# seguimiento con `area_after_reaching_max: "FOLLOW UP"` tiraron un `ValidationError` en cada
# lectura). Por eso cada campo persistido de tipo `Area` usa `AreaTolerante` (obligatorio) o
# `AreaOpcionalTolerante` (opcional), y el test `tests/test_enum_values_snapshot.py` falla si un
# valor guardado alguna vez deja de poder leerse. Ver CLAUDE.md, «Sacar un valor de un enum que
# se guarda».
#
# Para un campo OBLIGATORIO hace falta un reemplazo: va en este mapa.
AREAS_SACADAS: dict[str, Area] = {
    # Sacada en 0.4.563 (plan 9). Un chat «en seguimiento» no estaba archivado ni con un agente:
    # lo más cercano, y que no lo esconde de la bandeja, es esperando agente.
    "FOLLOW UP": Area.WAITING_AGENT,
}

_valores_avisados: set[tuple[str, str]] = set()


def avisar_valor_legado_una_vez(tipo: str, valor: Any, leido_como: Any) -> None:
    """WARNING una sola vez por proceso y por (tipo, valor): un documento viejo no tiene que
    llenar el log en cada lectura, pero tiene que quedar dicho que existe."""
    clave = (tipo, str(valor))
    if clave in _valores_avisados:
        return
    _valores_avisados.add(clave)
    _logger.warning(
        "[VALOR_LEGADO] %s=%r ya no es un valor válido; se lee como %r. "
        "Hay documentos guardados con ese valor.", tipo, valor, leido_como,
    )


def _leer_area(valor: Any) -> Any:
    """Lector de un `Area` obligatoria: los valores sacados se traducen con `AREAS_SACADAS`.
    Un string desconocido que no está en el mapa sigue fallando: no hay forma honesta de
    adivinarlo, y un campo obligatorio no tiene un «no hace nada»."""
    if isinstance(valor, str) and not isinstance(valor, Area) and valor not in Area._value2member_map_:
        if valor in AREAS_SACADAS:
            reemplazo = AREAS_SACADAS[valor]
            avisar_valor_legado_una_vez("Area", valor, reemplazo.value)
            return reemplazo
    return valor


def _leer_area_opcional(valor: Any) -> Any:
    """Lector de un `Area` opcional: cualquier string que hoy no es un `Area` (un valor sacado
    o uno desconocido) se lee como `None` («no mueve el chat»)."""
    if isinstance(valor, str) and not isinstance(valor, Area) and valor not in Area._value2member_map_:
        avisar_valor_legado_una_vez("Area", valor, None)
        return None
    return valor


AreaTolerante = Annotated[Area, BeforeValidator(_leer_area)]
AreaOpcionalTolerante = Annotated[Optional[Area], BeforeValidator(_leer_area_opcional)]

frontend_areas_to_backend_areas = {
    "esperando agente": Area.WAITING_AGENT,
    "asignar a agente": Area.WITH_AGENT,
    "con agente": Area.WITH_AGENT,
    "archivados": Area.ARCHIVED,
}
backend_areas_to_frontend_areas = {
    Area.WAITING_AGENT: "esperando agente",
    Area.WITH_AGENT: "con agente",
    Area.ARCHIVED: "archivados",
}
"""La versión instalada de letschatty, leída UNA vez por proceso.

CHAT-363: ``importlib.metadata.version("letschatty")`` se llamaba en cada evento de
analytics. Si el dist-info falta en ese instante (por ejemplo, el paquete se está
reinstalando en el entorno vivo), levantaba ``PackageNotFoundError`` y un campo
cosmético (``specversion``) hacía fallar el procesamiento de un mensaje entrante.

Reglas:
- La primera lectura exitosa se guarda y no se vuelve a leer.
- Sin metadata se devuelve ``"unknown"`` y se avisa con un WARNING una sola vez.
  No se guarda: la próxima llamada vuelve a intentar, así el valor real aparece
  apenas el dist-info vuelve.
- Sólo se ataja ``PackageNotFoundError``: cualquier otro error es un bug y sube.
"""
from __future__ import annotations

import logging
from importlib import metadata

logger = logging.getLogger("letschatty.package_version")

PACKAGE_NAME = "letschatty"
UNKNOWN_VERSION = "unknown"

_version: str | None = None
_warned = False


def package_version() -> str:
    global _version, _warned
    if _version is not None:
        return _version
    try:
        _version = metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        if not _warned:
            _warned = True
            logger.warning(
                "[PACKAGE_VERSION_UNKNOWN] No se encontró la metadata de %s; "
                "los eventos salen con specversion=%r hasta que vuelva.",
                PACKAGE_NAME,
                UNKNOWN_VERSION,
            )
        return UNKNOWN_VERSION
    return _version


def _reset_for_tests() -> None:
    global _version, _warned
    _version = None
    _warned = False

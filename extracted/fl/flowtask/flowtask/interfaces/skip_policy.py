"""Politica compartida de `skipError` para iteracion y ramificacion (FEAT-554).

Los cuatro caminos de ejecucion descritos en el spec (§2 D4) —
`IteratorBase.async_job`, `Loop.exec_component`, `BaseLoop.exec_component` y
`ThreadJob.execute_job`— comparten ESTE clasificador aunque sigan siendo
call-sites separados (§7 #7).
"""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from asyncdb.exceptions import NoDataFound, ProviderError  # verified: IteratorBase.py:8

from ..exceptions import (  # verified: IteratorBase.py:9-14
    ComponentError,
    DataNotFound,
    FileNotFound,
    NotSupported,
)
from .log import SkipErrors  # verified: IteratorBase.py:17

if TYPE_CHECKING:
    from logging import Logger

#: Nombres de metrica publicados por los iteradores (spec §5 Observabilidad).
SKIPPED_ITERATIONS_METRIC: str = "SKIPPED_ITERATIONS"
FAILED_ITERATIONS_METRIC: str = "FAILED_ITERATIONS"

#: Default del umbral de fallos consecutivos (spec §2 D2, §8 Q2 -> 10).
DEFAULT_MAX_CONSECUTIVE_FAILURES: int = 10

#: Familia "sin datos". SE COMPRUEBA PRIMERA: NoDataFound hereda de ProviderError.
DATA_ERRORS: tuple[type[BaseException], ...] = (NoDataFound, DataNotFound, FileNotFound)
#: Familia "fallo de componente/proveedor".
COMPONENT_ERRORS: tuple[type[BaseException], ...] = (ProviderError, ComponentError, NotSupported)


class ErrorFamily(Enum):
    """Familia a la que pertenece una excepcion de iteracion."""

    DATA = "data"
    COMPONENT = "component"
    GENERIC = "generic"


class Disposition(Enum):
    """Que debe hacer el call-site con la excepcion."""

    RETURN = "return"
    RAISE = "raise"


class _SkippedIteration:
    """Sentinel unico devuelto por una iteracion saltada (S8, spec §7 #10)."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "<SKIPPED_ITERATION>"

    def __bool__(self) -> bool:
        return False


#: Valor UNICO devuelto tanto bajo `skip` como bajo `log` (spec §5).
SKIPPED_ITERATION: _SkippedIteration = _SkippedIteration()


def classify(err: BaseException) -> ErrorFamily:
    """Clasifica una excepcion en su familia.

    Args:
        err: la excepcion capturada por el call-site.

    Returns:
        `ErrorFamily.DATA` para la familia sin-datos, `COMPONENT` para
        provider/component/not-supported, `GENERIC` para el resto.
    """
    # DATA_ERRORS must be checked FIRST: NoDataFound inherits from ProviderError
    for exc_type in DATA_ERRORS:
        if isinstance(err, exc_type):
            return ErrorFamily.DATA
    for exc_type in COMPONENT_ERRORS:
        if isinstance(err, exc_type):
            return ErrorFamily.COMPONENT
    return ErrorFamily.GENERIC


def resolve_skip(
    job: Any,
    err: BaseException,
    *,
    logger: Logger,
    step_name: str,
) -> Disposition:
    """Decide si una iteracion fallida se salta o aborta el bucle.

    Replica el patron existente de `IteratorBase.py:231-247` y lo generaliza a
    cualquier familia de excepcion.

    Args:
        job: el componente envuelto. Se consulta `job.skipError` — el del PASO
            ENVUELTO, no el del iterador (spec §7 #5).
        err: la excepcion capturada.
        logger: logger del call-site (`self._logger`).
        step_name: nombre del paso, para el mensaje de log.

    Returns:
        `Disposition.RETURN` bajo `SKIP` y `LOG`; `Disposition.RAISE` bajo
        `ENFORCE` y tambien cuando `job` no expone `skipError`.
    """
    try:
        skip_error = job.skipError
    except AttributeError:
        # Job without skipError attribute defaults to ENFORCE (replicate IteratorBase.py:247)
        return Disposition.RAISE

    if skip_error == SkipErrors.SKIP:
        logger.warning(
            f"Component {job!s} was Skipped, error: {err}"
        )
        return Disposition.RETURN
    elif skip_error == SkipErrors.LOG:
        logger.error(
            f"Component {job!s} was Skipped, error: {err}"
        )
        return Disposition.RETURN
    else:
        # ENFORCE or None - abort
        return Disposition.RAISE


class ConsecutiveFailureTracker:
    """Contabilidad de una corrida de iteraciones (spec §2 D2, §7 #10).

    Lleva exitos, saltos y fallos CONSECUTIVOS. El contador de consecutivos se
    resetea en cada iteracion exitosa (§7 #4).
    """

    def __init__(
        self,
        max_failures: int | None = DEFAULT_MAX_CONSECUTIVE_FAILURES,
    ) -> None:
        """Args:
            max_failures: umbral de fallos consecutivos. `0` o `None` lo
                desactivan (spec §5).
        """
        self.max_failures = max_failures
        self.successes: int = 0
        self.skipped: int = 0
        self.consecutive: int = 0
        self.last_error: BaseException | None = None

    @property
    def enabled(self) -> bool:
        """`True` si el umbral esta activo (no es `0` ni `None`)."""
        # 0 and None disable the threshold
        return self.max_failures is not None and self.max_failures > 0

    def record_success(self) -> None:
        """Registra una iteracion exitosa y RESETEA los consecutivos."""
        self.successes += 1
        self.consecutive = 0
        self.last_error = None

    def record_skip(self, err: BaseException) -> bool:
        """Registra una iteracion saltada.

        Returns:
            `True` si se alcanzo el umbral y el bucle debe ABORTAR.
        """
        self.skipped += 1
        self.consecutive += 1
        self.last_error = err
        # Return True if threshold is enabled and consecutive >= max_failures
        return self.enabled and self.consecutive >= self.max_failures

    def publish(self, component: Any) -> None:
        """Publica las metricas de la corrida via `component.add_metric`.

        Args:
            component: el iterador (expone `add_metric`, `stat.py:35`).
        """
        component.add_metric(SKIPPED_ITERATIONS_METRIC, self.skipped)
        component.add_metric(FAILED_ITERATIONS_METRIC, self.consecutive)
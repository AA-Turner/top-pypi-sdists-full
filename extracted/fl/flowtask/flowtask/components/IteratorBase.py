# -*- coding: utf-8 -*-
from typing import Any
import threading
from threading import Semaphore
import asyncio
from collections.abc import Callable
from navconfig.logging import logging
from asyncdb.exceptions import NoDataFound, ProviderError
from ..exceptions import (
    ComponentError,
    NotSupported,
    DataNotFound,
    FileNotFound
)

from ..interfaces.flow import FlowComponent
from ..interfaces.skip_policy import (
    DEFAULT_MAX_CONSECUTIVE_FAILURES,
    Disposition,
    ErrorFamily,
    SKIPPED_ITERATION,
    classify,
    resolve_skip,
)


class ThreadJob(threading.Thread):
    def __init__(self, job: Any, step_name: str, semaphore: Semaphore):
        super().__init__()
        self.step_name = step_name
        self.job = job
        self.exc = None
        self.result = None
        self.semaphore = semaphore
        self._logger = logging.getLogger(
            f"FlowTask.ThreadJob.{step_name}"
        )

    def run(self):
        try:
            asyncio.run(self.execute_job(self.job, self.step_name))
        except Exception as ex:
            self.exc = ex
        finally:
            # Release semaphore
            self.semaphore.release()

    async def execute_job(self, job: Any, step_name: str):
        """Ejecuta un job de iteracion dentro de un hilo.

        Contrato tras FEAT-554 (spec §3 M7): aplica la MISMA clasificacion
        `skipError` que `IteratorBase.async_job`, incluidos los fallos de
        `job.start()` (§8 Q5). Hoy NO la consulta en absoluto: cualquier
        excepcion se guarda en `self.exc` y se re-lanza al join, de modo que
        `skipError: skip` no tiene efecto en modo paralelo.

        Efectos: fija `self.result` (resultado o `SKIPPED_ITERATION`) y
        `self.exc` (`None` salvo que la disposicion sea abortar).

        Consumidores del camino paralelo: `FileList`, `MergeFileList`,
        `PandasIterator`.
        """
        try:
            start = getattr(job, "start", None)
            if not callable(start):
                raise ComponentError(f"Error running Function on {step_name}")
            try:
                if asyncio.iscoroutinefunction(start):
                    st = await job.start()
                else:
                    st = job.start()
                self._logger.debug(f"STARTED: {st}")
            except Exception as err:
                # Errores en start() también consultan skipError
                self._apply_error_policy(job, err, step_name)
                return

            run = getattr(job, "run", None)
            if asyncio.iscoroutinefunction(run):
                self.result = await job.run()
            else:
                self.result = job.run()
            # Éxito: self.result ya está asignado, self.exc = None
        except (NoDataFound, DataNotFound, FileNotFound) as err:
            self._apply_error_policy(job, err, step_name)
        except (ProviderError, ComponentError, NotSupported) as err:
            self._apply_error_policy(job, err, step_name)
        except Exception as err:
            self._logger.exception(err)
            self._apply_error_policy(job, err, step_name)
        finally:
            try:
                close = getattr(job, "close", None)
                if asyncio.iscoroutinefunction(close):
                    await job.close()
                else:
                    job.close()
            except Exception:
                pass

    def _apply_error_policy(self, job: Any, err: Exception, step_name: str):
        """Aplica la politica de skipError a un error, sin relanzar.

        Si la disposicion es RETURN (skip/log), asigna self.result = SKIPPED_ITERATION
        y self.exc = None. Si es RAISE, asigna self.exc a la excepcion que
        corresponda a la familia.

        D3 (spec §2): la familia de datos es INCONDICIONAL — no consulta
        `skipError`. Se asigna siempre a `self.exc` (nunca al sentinel),
        para que el join del call-site (`FileList.run` y companeros) la
        atrape con su propio `except (NoDataFound, DataNotFound, ...):
        continue`, sin pasar por el tracker de fallos consecutivos — la
        misma garantia que `IteratorBase._dispatch_error` da al camino
        secuencial.
        """
        family = classify(err)
        if family == ErrorFamily.DATA:
            self.exc = DataNotFound(f"{err!s}")
            return

        if resolve_skip(job, err, logger=self._logger, step_name=step_name) is Disposition.RETURN:
            # Saltar la iteracion: no relanzar, simplemente marcar
            self.result = SKIPPED_ITERATION
            self.exc = None
            return

        # Disposicion RAISE: clasificar la excepcion y asignarla a self.exc
        if family == ErrorFamily.COMPONENT:
            self.exc = err
        else:
            self.exc = ComponentError(f"Iterator Error on {step_name}, error: {err}")
        # No relanzamos: el join() re-lanzará si self.exc is not None


class IteratorBase(FlowComponent):
    """
    IteratorBase

    :interface: true

    Overview

        The IteratorBase class is an abstract component for handling iterative tasks. It extends the FlowComponent class
        and provides methods for starting tasks, retrieving steps, and executing jobs asynchronously.

    :widths: auto

        | iterate         |   No     | Boolean flag indicating if the component should                               |
        |                 |          | iterate the components or return the list, defaults to False.                 |

        The methods in this class manage the execution of iterative tasks, including initialization, step retrieval,
        job creation, and asynchronous execution.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          IteratorBase:
          # attributes here
        ```
    """
    #: Umbral de fallos CONSECUTIVOS antes de abortar la iteracion (spec §2 D2).
    #: 0 o None desactivan el umbral. Heredado por las 7 subclases; el YAML
    #: puede sobreescribirlo por tarea.
    max_consecutive_failures: int = DEFAULT_MAX_CONSECUTIVE_FAILURES
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.iterate: bool = False
        self._iterator: bool = True
        self._conditions: dict = {}
        super(IteratorBase, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        if self.previous:
            self.data = self.input
        return True

    def get_step(self):
        params = None
        try:
            if not self._TaskPile:
                raise ComponentError("No Components in TaskPile")
            step, idx = self._TaskPile.nextStep(self.StepName)
            params = step.params()
            try:
                if params["conditions"]:
                    self._conditions[step.name] = params["conditions"]
            except KeyError:
                pass
            params["ENV"] = self._environment
            # program
            if hasattr(self, "_program"):
                params["_program"] = self._program
            # params
            params["params"] = self._params
            # parameters
            params["parameters"] = self._parameters
            # useful to change variables in set var components
            params["_vars"] = self._vars
            # variables dictionary
            params["variables"] = self._variables
            params["_args"] = self._args
            # argument list for components (or tasks) that need argument lists
            params["arguments"] = self._arguments
            # for components with conditions, we can add more conditions
            conditions = params.get("conditions", {})
            step_conds = self._conditions.get(step.name, {})
            if self.conditions is not None:
                step_conds = {**self.conditions, **step_conds}
            params["conditions"] = {**conditions, **step_conds}
            # attributes only usable component-only
            params["attributes"] = self._attributes
            # the current Pile of components
            params["TaskPile"] = self._TaskPile
            # params['TaskName'] = step_name
            params["debug"] = self._debug
            params["argparser"] = self._argparser
            # the current in-memory connector
            params["memory"] = self._memory
            # propagate task storage so SubTask resolves the same storage
            params["taskstorage"] = self._taskstore
            params["storage_name"] = self._storage_name
            target = step.component
            # remove this element from tasks, doesn't need to run again
            self._TaskPile.delStep(idx)
            # return target and params
            return [step, target, params]
        finally:
            pass

    def get_job(self, target, **params):
        job = None
        try:
            job = target(job=self, loop=self._loop, stat=self.stat, **params)
            return job
        except Exception as err:
            raise ComponentError(
                f"Generic Component Error on {target}, error: {err}"
            ) from err

    def _dispatch_error(self, job, err, step_name):
        """Decide que hacer con una excepcion de iteracion.

        Args:
            job: el componente envuelto (se consulta `job.skipError`).
            err: la excepcion capturada.
            step_name: nombre del paso.

        Returns:
            `SKIPPED_ITERATION` cuando la politica permite saltar.

        Raises:
            La excepcion que corresponde a la familia. Para la familia de
            datos, SIEMPRE (D3 — incondicional, ver spec §2). Para las
            demas, solo cuando la politica es ENFORCE. Ver la tabla
            "Decision fijada" del task.
        """
        family = classify(err)
        if family == ErrorFamily.DATA:
            # D3: el "continue" ante datos-sin-encontrar es INCONDICIONAL —
            # no consulta `skipError` y por tanto tampoco pasa por el
            # tracker de fallos consecutivos del call-site. Bajo `skip`/
            # `log`, devolver aqui SKIPPED_ITERATION haria que el call-site
            # lo contabilizara como un salto real, rompiendo D3 (spec §2:
            # "el continue ante DataNotFound sigue siendo incondicional").
            raise DataNotFound(f"{err!s}") from err
        if resolve_skip(job, err, logger=self._logger, step_name=step_name) is Disposition.RETURN:
            return SKIPPED_ITERATION
        if family == ErrorFamily.COMPONENT:
            raise err
        else:
            self._logger.exception(f"Iterator Error on {step_name}, error: {err}")
            raise ComponentError(f"Iterator Error on {step_name}, error: {err}") from err

    async def async_job(self, job, step_name):
        """Ejecuta un job de iteracion aplicando la politica `skipError`.

        Contrato tras FEAT-554 (spec §3 M2):
          - `(NoDataFound, DataNotFound, FileNotFound)`: consulta
            `job.skipError` (comportamiento existente) -- verified: :231-247
          - `(ProviderError, ComponentError, NotSupported)`: NUEVO, consulta
            `job.skipError` en vez de `raise NotSupported` -- verified: :249-251
          - `Exception`: NUEVO, consulta `job.skipError` en vez de re-lanzar
            directamente -- verified: :253-256
          - Fallos de `job.start()`: NUEVO, tambien consultan `job.skipError`
            (§8 Q5 resuelta) -- verified: :213-218

        Args:
            job: el componente a ejecutar en esta iteracion.
            step_name: nombre del paso, para logs y mensajes de error.

        Returns:
            El resultado del job, o `SKIPPED_ITERATION` si la iteracion se
            salto. `skip` y `log` devuelven el MISMO valor (S8).

        Raises:
            La excepcion correspondiente cuando `job.skipError` is ENFORCE.
        """
        try:
            start = getattr(job, "start", None)
            if not callable(start):
                raise ComponentError(f"Error running Function on {step_name}")
            try:
                if asyncio.iscoroutinefunction(start):
                    st = await job.start()
                else:
                    st = job.start()
                self._logger.debug(f"STARTED: {st}")
            except Exception as err:
                return self._dispatch_error(job, err, step_name)

            run = getattr(job, "run", None)
            if asyncio.iscoroutinefunction(run):
                result = await job.run()
            else:
                result = job.run()
            self._result = result
            return self._result
        except (NoDataFound, DataNotFound, FileNotFound) as err:
            return self._dispatch_error(job, err, step_name)
        except (ProviderError, ComponentError, NotSupported) as err:
            return self._dispatch_error(job, err, step_name)
        except Exception as err:
            return self._dispatch_error(job, err, step_name)
        finally:
            try:
                close = getattr(job, "close", None)
                if asyncio.iscoroutinefunction(close):
                    await job.close()
                else:
                    job.close()
            except Exception:
                pass

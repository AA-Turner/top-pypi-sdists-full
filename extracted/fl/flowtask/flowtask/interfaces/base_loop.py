import asyncio
from collections.abc import Callable
from typing import Any

from asyncdb.exceptions import NoDataFound, ProviderError

from ..exceptions import ComponentError, DataNotFound, FileNotFound, NotSupported
from ..utils.stats import StepMonitor
from .flow import FlowComponent
from .skip_policy import (
    SKIPPED_ITERATION,
    Disposition,
    ErrorFamily,
    classify,
    resolve_skip,
)


class BaseLoop(FlowComponent):
    """
    BaseLoop Interface.

    :interface: true

    Structural base for all Iterators (Switch, Loop, IF).

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          BaseLoop:
          # attributes here
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop | None = None,
        job: Callable | None = None,
        stat: Callable | None = None,
        **kwargs,
    ):
        self._conditions: dict = {}
        self._default = kwargs.get("default", None)
        self._tracked_components = set()
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def _define_tracking_components(self, *components):
        """
        Define the components to track in the loop.

        Args:
            components: A list of component names to track.
        """
        for component in components:
            self._tracked_components.add(component.get('component'))
        if self._default:
            self._tracked_components.add(self._default)

    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        if self.previous:
            self.data = self.input
        return True

    async def close(self):
        pass

    def get_component(self, step):
        params = None
        try:
            if not self._TaskPile:
                raise ComponentError(
                    "No Components in TaskPile"
                )
            params = step.params()
            try:
                if params["conditions"]:
                    self._conditions[step.name] = params["conditions"]
            except KeyError:
                pass
            if self.stat:
                parent_stat = self.stat.parent()
                stat = StepMonitor(name=step.name, parent=parent_stat)
                parent_stat.add_step(stat)
            else:
                stat = None
            params["ENV"] = self._environment
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
            target = step.component
            # return target and params
            return [target, params, stat]
        finally:
            pass

    def create_component(
        self,
        target,
        value: Any = None,
        stat: Any = None,
        **params
    ):
        """get_component.

        Create a new component instance.
        """
        try:
            return target(
                job=self,
                loop=self._loop,
                stat=stat,
                input_result=value,
                **params
            )
        except Exception as err:
            raise ComponentError(
                f"Component Error on {target}: {err}"
            ) from err

    def _dispatch_error(self, job, err, step_name):
        """Decide que hacer con una excepcion de RAMA.

        Gemelo del de `IteratorBase`, pero sin umbral: `IF`/`Switch` son
        ramificacion, no iteracion (spec §2 D4).
        """
        if resolve_skip(job, err, logger=self._logger, step_name=step_name) is Disposition.RETURN:
            return SKIPPED_ITERATION
        family = classify(err)
        if family is ErrorFamily.DATA:
            raise DataNotFound(f"{err!s}") from err
        elif family is ErrorFamily.COMPONENT:
            # Leave original exception intact (don't narrow to NotSupported)
            raise err
        else:
            # GENERIC
            raise ComponentError(f"Error running Component {step_name}, error: {err}") from err

    async def exec_component(self, job, step_name):
        """Ejecuta el componente de la rama.

        Contrato tras FEAT-554 (spec §3 M6): misma clasificacion que
        `IteratorBase.async_job` para las familias no-de-datos
        -- verified: base_loop.py:201-209 (hoy estrecha a NotSupported).

        **NO** aplica `max_consecutive_failures`: `IF`/`Switch` son
        RAMIFICACION, no iteracion; "skip" omite el componente de la rama, no
        reanuda un bucle (spec §2 D4).

        Consumidores: `IF` (`IF.py:9`), `Switch` (`Switch.py:11`).

        Returns:
            El resultado del componente, o `SKIPPED_ITERATION` si se omitio.
        """
        try:
            start = getattr(job, "start", None)
            if callable(start):
                try:
                    if asyncio.iscoroutinefunction(start):
                        st = await job.start()
                    else:
                        st = job.start()
                    self._logger.debug(f"STARTED: {st}")
                except (NoDataFound, DataNotFound, FileNotFound) as err:
                    return self._dispatch_error(job, err, step_name)
                except (ProviderError, ComponentError, NotSupported) as err:
                    return self._dispatch_error(job, err, step_name)
                except Exception as err:
                    # Familia generica en start(): tambien debe consultar
                    # skipError (misma clasificacion que async_job, §3 M6) —
                    # sin este bloque, un fallo generico en start() escapa
                    # crudo, ignorando la politica por completo.
                    return self._dispatch_error(job, err, step_name)
            else:
                raise ComponentError(
                    f"Error running Function on {step_name}"
                )
            try:
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
            except Exception as err:  # noqa: BLE001
                return self._dispatch_error(job, err, step_name)
        finally:
            try:
                close = getattr(job, "close", None)
                if asyncio.iscoroutinefunction(close):
                    await job.close()
                else:
                    job.close()
            except Exception as e:  # noqa: BLE001
                self._logger.warning(f"Error closing job: {e}")

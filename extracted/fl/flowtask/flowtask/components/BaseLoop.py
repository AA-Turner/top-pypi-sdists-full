from collections.abc import Callable
import asyncio
from typing import Any
from asyncdb.exceptions import NoDataFound, ProviderError
from .flow import FlowComponent
from ..exceptions import (
    ComponentError,
    DataNotFound,
    NotSupported,
    FileNotFound
)
from ..utils.stats import StepMonitor
from ..interfaces.log import SkipErrors


class BaseLoop(FlowComponent):
    """
    BaseLoop Interface.

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
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._conditions: dict = {}
        self._default = kwargs.get("default", None)
        self._tracked_components = set()
        super(BaseLoop, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

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

    async def exec_component(self, job, step_name):
        start = getattr(job, "start", None)
        if callable(start):
            try:
                if asyncio.iscoroutinefunction(start):
                    st = await job.start()
                else:
                    st = job.start()
                self._logger.debug(f"STARTED: {st}")
            except (NoDataFound, DataNotFound) as err:
                raise DataNotFound(f"{err!s}") from err
            except (ProviderError, ComponentError, NotSupported) as err:
                raise ComponentError(
                    f"Error running Start Function on {step_name}, error: {err}"
                ) from err
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
            try:
                if job.skipError == SkipErrors.SKIP:
                    self._logger.warning(
                        f"Component {job!s} was Skipped, error: {err}"
                    )
                    self._result = self.data
                    return self._result
                elif job.skipError == SkipErrors.ENFORCE:
                    # Enforcing to Raise Error:
                    raise DataNotFound(f"{err!s}") from err
                else:
                    # Log Only
                    self._logger.error(
                        f"Component {job!s} was Skipped, error: {err}"
                    )
            except AttributeError:
                raise DataNotFound(f"{err!s}") from err
        except (ProviderError, ComponentError, NotSupported) as err:
            raise NotSupported(
                f"Error running Component {step_name}, error: {err}"
            ) from err
        except Exception as err:
            self._logger.exception(err, exc_info=True)
            raise ComponentError(
                f"Iterator Error on {step_name}, error: {err}"
            ) from err
        finally:
            try:
                close = getattr(job, "close", None)
                if asyncio.iscoroutinefunction(close):
                    await job.close()
                else:
                    job.close()
            except Exception:
                pass

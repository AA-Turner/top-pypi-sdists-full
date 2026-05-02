import asyncio
import copy
from collections.abc import Callable
from navconfig.logging import logging
from asyncdb.exceptions import NoDataFound, ProviderError
from ..utils.stats import StepMonitor
from ..interfaces.log import SkipErrors
from ..exceptions import DataNotFound, NotSupported, ComponentError
from ..utils import cPrint
from .flow import FlowComponent


class GroupComponent(FlowComponent):
    """
    GroupComponent

    Overview

        This component executes a group of other FlowTask components sequentially as a single unit.
        It allows chaining multiple tasks together and provides error handling for various scenarios.

    :widths: auto

        | component_list (list)  |   Yes    | List of dictionaries defining the components to be executed in the group. Each dictionary                      |
        |                        |          | should contain the following keys:                                                                             |
        |                        |          |   - "component": The FlowTask component class to be used.                                                      |
        |                        |          |   - "params": A dictionary containing parameters to be passed to the component.                                |
        |                        |          | (Optional)                                                                                                     |
        |                        |          |   - "conditions": A dictionary containing conditions that must be met before running the component. (Optional) |
        | stat (Callable)        |    No    | Optional callback function for step-level monitoring and statistics collection.                                |
        | skipError              |    No    | Defines the behavior when a component within the group raises an error.                                        |
        |                        |          | Valid options are:                                                                                             |
        |                        |          |   SkipErrors: Skip This makes the component continue his execution.                                            |
        |                        |          |   SkipErrors: Raise This Raise the error and interrupt execution.                                              |

    Return

        The component modifies the data received from the previous component and returns the final output after
        all components in the group have been executed.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GroupComponent:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        component_list: list = None,
        **kwargs,
    ):
        """Init Method."""
        self._params = {}
        self._components = component_list
        self._conditions: dict = {}
        super(GroupComponent, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        return True

    async def close(self):
        pass

    async def run(self):
        steps = []
        prev = self.previous
        result = None
        for step in self._components:
            step = copy.deepcopy(step)
            step_name = step.name
            try:
                _prev = prev
                component = self.get_component(step=step, previous=prev)
                prev = component
            except Exception as e:
                raise ComponentError(f"{e!s}") from e
            # calling start method for component
            start = getattr(component, "start", None)
            if callable(start):
                try:
                    if asyncio.iscoroutinefunction(start):
                        st = await component.start()
                    else:
                        st = component.start()
                    logging.debug(f"{step_name} STARTED: {st}")
                except (NoDataFound, DataNotFound) as err:
                    if component.skipError == SkipErrors.SKIP:
                        self._logger.warning(
                            f"::: SKIPPING Error on {step_name} :::: "
                        )
                        prev = _prev
                        continue
                    raise DataNotFound(
                        f'Data Not Found over {step_name}'
                    ) from err
                except (ProviderError, ComponentError, NotSupported) as err:
                    raise ComponentError(
                        f"Group Error: calling Start on {step.name}, error: {err}"
                    ) from err
            else:
                raise ComponentError(f"Group Error: missing Start on {step.name}")
            # then, calling the run method:
            try:
                run = getattr(component, "run", None)
                if asyncio.iscoroutinefunction(run):
                    result = await run()
                else:
                    result = run()
            except (NoDataFound, DataNotFound) as err:
                if component.skipError == SkipErrors.SKIP:
                    self._logger.warning(
                        f"::: SKIPPING Error on {step_name} :::: "
                    )
                    prev = _prev
                    continue
                raise DataNotFound(
                    f'Data Not Found over {step_name}'
                ) from err
            except (ProviderError, ComponentError, NotSupported) as err:
                if component.skipError == SkipErrors.SKIP:
                    self._logger.warning(
                        f"::: SKIPPING Error on {step_name} :::: "
                    )
                    prev = _prev
                    continue
                raise NotSupported(
                    f"Group Error: Not Supported on {step.name}, error: {err}"
                ) from err
            except Exception as err:
                if component.skipError == SkipErrors.SKIP:
                    self._logger.warning(
                        f"::: SKIPPING Error on {step_name} :::: "
                    )
                    prev = _prev
                    continue
                raise ComponentError(
                    f"Group Error: Calling Start on {step.name}, error: {err}"
                ) from err
            finally:
                steps.append(step_name)
                try:
                    close = getattr(component, "close", None)
                    if asyncio.iscoroutinefunction(close):
                        await close()
                    else:
                        close()
                except Exception as e:  # pylint: disable=W0703
                    logging.warning(e)
        self._result = result
        return self._result

    def get_component(self, step, previous):
        if self.stat:
            parent_stat = self.stat.parent()
            stat = StepMonitor(name=step.name, parent=parent_stat)
            parent_stat.add_step(stat)
        else:
            stat = None
        params = step.params
        try:
            if params["conditions"]:
                self._conditions[step.name] = params["conditions"]
        except KeyError:
            pass
        params["ENV"] = self._environment
        # params
        if self._params:
            try:
                params["params"] = {**params["params"], **self._params}
            except (KeyError, TypeError):
                pass
        # parameters
        if self._parameters:
            parameters = params.get("parameters", {})
            params["parameters"] = {**parameters, **self._parameters}
        if hasattr(self, "_program"):
            params["_program"] = self._program
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
        job = None
        try:
            job = target(job=previous, loop=self._loop, stat=stat, **params)
            job.SetPile(self._TaskPile)
            cPrint(
                f"LOADED STEP: {step.name}",
                level="DEBUG"
            )
            return job
        except Exception as err:
            raise ComponentError(
                f"Component Error on {target}, error: {err}"
            ) from err

from collections.abc import Callable, Awaitable
import asyncio
from typing import Any
from pandas import DataFrame
from asyncdb.exceptions import NoDataFound, ProviderError, DriverError
from .flow import FlowComponent
from ..exceptions import (
    ComponentError,
    DataNotFound,
    NotSupported,
    FileNotFound
)
from ..utils.stats import StepMonitor
from ..interfaces.log import SkipErrors


class Loop(FlowComponent):
    """
    Loop.

    Overview:
        The Loop class is a FlowComponent that is used to iterate over the next Component and execute them in a
        sequential order.
        It extends the FlowComponent class and provides methods for starting tasks, retrieving steps,
        and executing jobs asynchronously.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Loop:
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
        self._generator = kwargs.get("generator", None)  # Predefined generator
        self._iterate: bool = kwargs.get('iterate', False)
        self._iterable = kwargs.get("iterable", None)    # Custom iterable
        self._done: bool = False  # Flag to indicate if iteration is complete
        # Component to be executed when finished.
        self._ondone: str = kwargs.get("onDone", None)
        super(Loop, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        if self.previous:
            self.data = self.input

        # check if previous data is an iterable:
        if isinstance(self.data, DataFrame):
            self._iterable = self.data.iterrows()
        elif self._iterate is True or hasattr(self.data, '__iter__'):
            self._iterable = self.data
        elif self._generator:
            self._iterable = self._resolve_generator(self._generator)
        elif self._iterable and not hasattr(self._iterable, "__iter__"):
            raise ComponentError(
                "'iterable' must be an iterable object."
            )

        self._iterator = iter(self._iterable)
        return True

    def _resolve_generator(self, generator_name):
        """
        Resolve predefined generators like 'days_of_week' or 'days_of_month'.
        """
        # Define predefined generators here.
        # Each generator should return a list of values.
        # For example, 'days_of_week' could return a list of weekdays,
        # and 'days_of_month' could return a list of days of the month.
        predefined_generators = {
            "days_of_week": lambda: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "days_of_month": lambda: [f"Day {i}" for i in range(1, 32)],
        }
        if generator_name not in predefined_generators:
            raise ComponentError(
                f"Unknown generator: {generator_name}"
            )
        return predefined_generators[generator_name]()

    async def close(self):
        pass

    def get_component(self, step, idx):
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
            # remove this element from tasks, doesn't need to run again
            self._TaskPile.delStep(idx)
            # return target and params
            return [target, params]
        finally:
            pass

    def create_component(self, target, value: Any = None, **params):
        """get_component.

        Create a new component instance.
        """
        try:
            return target(
                job=self,
                loop=self._loop,
                stat=self.stat,
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

    async def run(self):
        """Async Run Method."""
        # iterate over next Component
        step, idx = self._TaskPile.nextStep(self.StepName)
        target, params = self.get_component(step, idx)
        step_name = step.name
        i = 0
        results = []
        while True:
            try:
                # Get the next item from the iterator
                item = next(self._iterator)
                self.setTaskVar('value', item)
                cp = self.create_component(target, item, **params)
                try:
                    result = await self.exec_component(cp, step_name)
                    results.append(result)
                    i += 1
                except (NoDataFound, DataNotFound) as err:
                    # its a data component a no data was found
                    self._logger.notice(
                        f"Data not Found over {step_name} at {i} iteration, got: {err}"
                    )
                    i += 1
                    continue
            except StopIteration:
                self._done = True
                break  # Exit loop when iteration is complete
        # when iteration is finished, return the results collected:
        if self.stat:
            parent_stat = self.stat.parent()
            stat = StepMonitor(name=step_name, parent=parent_stat)
            parent_stat.add_step(stat)
            stat.add_metric('ITERATIONS', i)
        self._result = results
        return self._result

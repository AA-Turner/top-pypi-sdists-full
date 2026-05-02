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

from .flow import FlowComponent
from ..interfaces.log import SkipErrors


class ThreadJob(threading.Thread):
    def __init__(self, job: Any, step_name: str, semaphore: Semaphore):
        super().__init__()
        self.step_name = step_name
        self.job = job
        self.exc = None
        self.result = None
        self.semaphore = semaphore

    def run(self):
        try:
            asyncio.run(self.execute_job(self.job, self.step_name))
        except Exception as ex:
            self.exc = ex
        finally:
            # Release semaphore
            self.semaphore.release()

    async def execute_job(self, job: Any, step_name: str):
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
            raise ComponentError(f"Error running Function on {step_name}")
        try:
            run = getattr(job, "run", None)
            if asyncio.iscoroutinefunction(run):
                self.result = await job.run()
            else:
                self.result = job.run()
            return self.result
        except (NoDataFound, DataNotFound) as err:
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


class IteratorBase(FlowComponent):
    """
    IteratorBase

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

    async def async_job(self, job, step_name):
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

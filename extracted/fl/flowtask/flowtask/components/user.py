from typing import Optional, Any, Union
from collections.abc import Callable
from abc import ABC, abstractmethod
import asyncio
import random
from pathlib import Path, PurePath
import aiohttp
import orjson
from navconfig import config
from navconfig.logging import logging
from asyncdb.utils.types import SafeDict
from asyncdb.drivers.base import BaseDriver
from aiohttp.client_exceptions import ContentTypeError
from ..exceptions import ComponentError, DataNotFound
from ..utils import fnExecutor
from ..utils.constants import get_constant, get_func_value, is_constant, is_function
from ..interfaces import (
    FuncSupport,
    DBSupport,
    MaskSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
)
from ..interfaces.dataframes import PandasDataframe
from ..interfaces.http import ua
from .abstract import AbstractFlow


class UserComponent(
    DBSupport,
    FuncSupport,
    MaskSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
    PandasDataframe,
    AbstractFlow
):
    """
    UserComponent
      Abstract Base Component for User-defined Components.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Optional[Callable] = None,
        stat: Optional[Callable] = None,
        **kwargs,
    ):
        # stats object:
        self._memory: Optional[BaseDriver] = None
        self.StepName: Optional[str] = None

        self._variables: dict = {}  # variables
        self._vars = {}  # other vars
        self._mask = {}  # masks for function replacing
        self._params = {}  # other parameters
        self._ua = random.choice(ua)  # rotating UA
        self._filestore: Any = None
        self._retry_count: int = 0
        self.encoding: str = "UTF-8"
        self.accept: str = "application/xhtml+xml"
        ## Function Support
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Config Environment
        try:
            self._environment = kwargs["ENV"]
            del kwargs["ENV"]
        except (KeyError, AttributeError):
            self._environment = config
        # program
        try:
            self._program = kwargs["program"]
            del kwargs["program"]
        except KeyError:
            self._program = "navigator"
        # getting the Task Pile (components pile)
        self._TaskPile = kwargs.pop(
            "TaskPile",
            {}
        )
        if self._TaskPile:
            setattr(self, "TaskPile", self._TaskPile)
        # Template Parser
        try:
            self._tplparser = kwargs["template"]
            del kwargs["template"]
        except KeyError:
            self._tplparser = None
        # for changing vars (in components with "vars" feature):
        try:
            self._vars = kwargs["_vars"]
            del kwargs["_vars"]
        except KeyError:
            pass
        # memcache connector
        try:
            self._memory = kwargs["memory"]
            del kwargs["memory"]
        except KeyError:
            try:
                self._memory = self._vars["memory"]
                del self._vars["memory"]
            except KeyError:
                pass
        # attributes (root-level of component arguments):
        try:
            self._attributes = kwargs["attributes"]
            del kwargs["attributes"]
        except KeyError:
            self._attributes = {}
        # conditions:
        if "conditions" in kwargs:
            self.conditions: dict = kwargs.pop("conditions", {})
        # params:
        try:
            self._params = kwargs["params"]
            del kwargs["params"]
        except KeyError:
            self._params = {}
        # parameters
        try:
            self._parameters = kwargs["parameters"]
            del kwargs["parameters"]
        except KeyError:
            self._parameters = []
        # arguments list
        self._arguments = kwargs.pop(
            "arguments",
            []
        )
        # processing variables
        try:
            variables = kwargs["variables"]
            del kwargs["variables"]
            if isinstance(variables, str):
                try:
                    variables = orjson.loads(variables)
                except ValueError:
                    try:
                        variables = dict(x.split(":") for x in variables.split(","))
                    except (TypeError, ValueError, IndexError):
                        variables = {}
            if variables:
                for arg, val in variables.items():
                    self._variables[arg] = val
        except KeyError:
            pass
        # previous Job has variables, need to update from existing
        if job:
            self._component = job
            if isinstance(job, list):
                self._multi = True
                variables = {}
                for j in job:
                    variables = {**variables, **j.variables}
                try:
                    self._variables = {**self._variables, **variables}
                except Exception as err:
                    print(err)
            else:
                try:
                    self._variables = {**self._variables, **job.variables}
                except Exception as err:
                    logging.error(f"User Component Error: {err}")
        # mask processing:
        try:
            masks = kwargs["_masks"]
            del kwargs["_masks"]
        except KeyError:
            masks = {}
        # filling Masks:
        if "masks" in kwargs:
            self._mask = kwargs["masks"]
            del kwargs["masks"]
            object.__setattr__(self, "masks", self._mask)
        for mask, replace in masks.items():
            self._mask[mask] = replace  # override component's masks
        try:
            for mask, replace in self._mask.items():
                # first: making replacement of masks based on vars:
                try:
                    if mask in self._variables:
                        value = self._variables[mask]
                    else:
                        value = replace.format(**self._variables)
                except Exception as err:
                    value = replace
                value = fnExecutor(value, env=self._environment)
                self._mask[mask] = value
        except Exception as err:
            logging.debug(f"Mask Error: {err}")
        try:
            self._params = {**self._params, **kwargs}
        except (TypeError, ValueError):
            pass
        ## parameters:
        for arg, val in self._params.items():
            # print('ALL PARAMETERS: ', arg, val)
            try:
                if arg == "no-worker":
                    continue
                if arg == self.StepName:
                    values = dict(x.split(":") for x in self._params[arg].split(","))
                    for key, value in values.items():
                        self._params[key] = value
                        object.__setattr__(self, key, value)
                elif arg not in ["program", "TaskPile", "TaskName", "StepName"]:
                    try:
                        setattr(self, arg, val)
                    except Exception as err:
                        logging.warning(f"UserComponent: Wrong Parameter: {arg}={val}")
                        logging.exception(err)
            except (AttributeError, KeyError) as err:
                self._logger.error(err)
        # Localization
        LocaleSupport.__init__(self, **kwargs)
        # processing the variables:
        if hasattr(self, "vars"):
            for key, val in self._vars.items():
                if key in self.vars:
                    self.vars[key] = val

    def config(self, key, default: Any = None) -> Any:
        return self._environment.get(key, fallback=default)

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"<{type(self).__name__}>"

    def set_filestore(self, store):
        if not store:
            raise RuntimeError(
                "Unable to detect File Storage."
            )
        self._filestore = store

    def set_taskstore(self, store):
        self._taskstore = store

    def SetPile(self, pile):
        self._TaskPile = pile

    # Abstract Context Methods:
    async def __aenter__(self):
        if not self._started:
            await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.close()
        except Exception as exc:
            self._logger.warning(
                f"Error Closing Component: {exc!s}"
            )
        return self

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    def user_params(self):
        return self._params

    @abstractmethod
    async def start(self, **kwargs):
        """
        start.
            Initialize (if needed) a task
        """

    @abstractmethod
    async def run(self):
        """
        run.
            Close (if needed) a task
        """

    @abstractmethod
    async def close(self):
        """
        close.
            Close (if needed) a task
        """

    def set_conditions(self, name: str = "conditions"):
        if hasattr(self, name):
            obj = getattr(self, name)
            for condition, val in obj.items():
                if hasattr(self, condition):
                    obj[condition] = getattr(self, condition)
                elif is_constant(val):
                    obj[condition] = get_constant(val)
                elif is_function(val):
                    obj[condition] = get_func_value(val)
                if condition in self._variables:
                    obj[condition] = self._variables[condition]
                if condition in self._mask:
                    obj[condition] = self._mask[condition]
            if "pattern" in obj:
                # getting conditions as patterns
                pattern = obj["pattern"]
                del obj["pattern"]
                for field in pattern:
                    if field in self._params:
                        obj[field] = self._params[field]
                    else:
                        result = None
                        val = pattern[field]
                        result = self.getFunc(val)
                        obj[field] = result
            if self.conditions:
                for k, v in self.conditions.items():
                    # print('NEW CONDITION: ', k, v)
                    result = v
                    try:
                        if is_constant(v):
                            result = get_constant(v)
                        elif is_function(v):
                            result = get_func_value(v)
                    except Exception as err:
                        logging.exception(err)
                    obj[k] = result

    def set_variables(self, obj):
        return obj.format_map(SafeDict(**self._variables))

    async def session(
        self,
        url: str,
        method: str = "get",
        headers: Optional[dict] = None,
        auth: Optional[dict] = None,
        data: Optional[dict] = None,
    ):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        proxy = None
        hdrs = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self._ua,
        }
        if headers:
            hdrs = {**hdrs, **headers}
        self._logger.debug(f"Session URL: {url}")
        async with aiohttp.ClientSession(auth) as session:
            if method == "get":
                obj = session.get(url, headers=hdrs, timeout=timeout, proxy=proxy)
            elif method == "post":
                obj = session.post(
                    url, headers=hdrs, timeout=timeout, proxy=proxy, data=data
                )
            async with obj as response:
                if (status := response.status) not in (200, 204, 203, 206, 404):
                    if hasattr(self, "retry"):
                        # retrying the self.session
                        self._logger.warning(
                            f"Retrying Session: status: {status}, {response}"
                        )
                        await asyncio.sleep(1.5)
                        self._retry_count += 1
                        if self._retry_count < 3:
                            self.add_metric("RETRIES", self._retry_count)
                            return await self.session(
                                url,
                                method=method,
                                headers=headers,
                                auth=auth,
                                data=data,
                            )
                    raise ComponentError(
                        f"Error on Session: status: {status}, {response}"
                    )
                self._retry_count = 0
                try:
                    return await response.json()
                except ContentTypeError:
                    return await response.text()

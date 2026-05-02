import os
from typing import Optional, Any, Union, ParamSpec
from abc import abstractmethod
from collections.abc import Callable
import random
import glob
from pathlib import Path, PurePath
import asyncio
from tqdm import tqdm
import orjson
from navconfig import config
from ..conf import (
    FILE_STORAGES,
    TASK_STORAGES
)
from ..exceptions import (
    FileNotFound
)
from ..utils import SafeDict
from ..utils.constants import (
    get_constant,
    get_func_value,
    is_constant,
    is_function
)
from ..interfaces import (
    FuncSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
    MaskSupport,
    SkipErrors
)
from .abstract import AbstractFlow


P = ParamSpec("P")


class FlowComponent(
    FuncSupport,
    MaskSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
    AbstractFlow
):
    """Abstract

    Overview:

            Helper for building components that consume REST APIs.

    """
    _version = "1.0.0"

    def __init__(
        self,
        job: Optional[Union[Callable, list]] = None,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        # Task Related Component Name
        # TODO: migration from TaskName to Component Step Name.
        # self.TaskName: Optional[str] = kwargs.pop('step_name', None)
        self.StepName: Optional[str] = kwargs.pop('step_name', None)
        # Future Logic: trigger logic:
        self.runIf: list = []
        self.triggers: list = []
        self._attrs: dict = {}  # attributes
        self._variables = {}  # variables
        self._params = {}  # other parameters
        self._args: dict = {}
        self._filestore: Any = FILE_STORAGES.get('default')
        self._taskstore: Any = kwargs.get('taskstorage', None)
        if not self._taskstore:
            self._taskstore = TASK_STORAGES['default']
        self._started: bool = False  # Avoid multiple start methods.
        # Config Environment
        self._environment = kwargs.pop('ENV', config)
        # Object Name:
        self.__name__: str = self.__class__.__name__
        # program
        self._program = kwargs.get('program', 'navigator')
        # getting the argument parser:
        self._argparser = kwargs.pop('argparser', None)
        # getting the Task Pile (components pile)
        self._TaskPile = kwargs.pop(
            "TaskPile",
            {}
        )
        if self._TaskPile:
            setattr(self, "TaskPile", self._TaskPile)
        # for changing vars (in components with "vars" feature):
        self._vars = kwargs.get('vars', {})   # other vars
        # attributes (root-level of component arguments):
        self._attributes: dict = kwargs.pop("attributes", {})
        if self._attributes:
            self.add_metric("ATTRIBUTES", self._attributes)
        self._args: dict = kwargs.pop("_args", {})
        # conditions:
        if "conditions" in kwargs:
            self.conditions: dict = kwargs.pop("conditions", {})
        # params:
        self._params = kwargs.pop("params", {})
        # parameters
        self._parameters = kwargs.pop(
            "parameters", []
        )
        # arguments list
        self._arguments = kwargs.pop(
            "arguments", []
        )
        # Calling Super:
        super().__init__(*args, **kwargs)
        if 'input' in kwargs:
            self._input_result = kwargs.pop('input')
        # processing variables
        try:
            variables = kwargs.pop("variables", {})
            if isinstance(variables, str):
                try:
                    variables = orjson.loads(variables)
                except ValueError:
                    try:
                        variables = dict(x.split(":") for x in variables.split(","))
                    except (TypeError, ValueError, IndexError):
                        variables = {}
            for arg, val in variables.items():
                self._variables[arg] = val
        except KeyError:
            pass
        # previous Job has variables, need to update from existing
        self._multi: bool = False
        if isinstance(job, (AbstractFlow, list, )):
            self._component = job
            if isinstance(job, list):
                variables = {}
                for j in job:
                    if isinstance(j, AbstractFlow):
                        variables = {**variables, **j.variables}
                self._multi = True
                try:
                    self._variables = {**self._variables, **variables}
                except Exception as err:
                    print(err)
            else:
                try:
                    self._variables = {**self._variables, **job.variables}
                except Exception as err:
                    print(err)
        # call masks processing:
        self._mask_processing(variables=self._variables)
        # existing parameters:
        try:
            self._params = {**kwargs, **self._params}
        except (TypeError, ValueError):
            pass
        for arg, val in self._params.items():
            try:
                if arg == "no-worker":
                    continue
                if arg == self.StepName:
                    values = dict(x.split(":") for x in self._params[arg].split(","))
                    for key, value in values.items():
                        self._params[key] = value
                        object.__setattr__(self, key, value)
                elif arg not in ["program", "TaskPile", "TaskName"]:
                    if self.StepName in self._attributes:
                        # extracting this properties from Attributes:
                        new_args = self._attributes.pop(self.StepName, {})
                        self._attributes = {**self._attributes, **new_args}
                    self._attrs[arg] = val
                    if arg in self._attributes:
                        val = self._attributes[arg]
                    try:
                        setattr(self, arg, val)
                    except Exception as err:
                        self._logger.warning(f"Wrong Attribute: {arg}={val}")
                        self._logger.exception(err)
            except (AttributeError, KeyError) as err:
                self._logger.error(err)
        # attributes: component-based parameters (only for that component):
        for key, val in self._attributes.items():
            # TODO: check Attributes
            if key in self._attributes:
                # i need to override attibute
                current_val = self._attributes[key]
                if isinstance(current_val, dict):
                    val = {**current_val, **val}
                elif isinstance(current_val, list):
                    current_val.append(val)
                    val = current_val
                try:
                    object.__setattr__(self, key, val)
                    self._attrs[key] = val
                except (ValueError, AttributeError) as err:
                    self._logger.error(err)
        # processing the variables:
        if hasattr(self, "vars"):
            for key, val in self._vars.items():
                if key in self.vars:
                    self.vars[key] = val
        ### File Storage:
        self._fileStorage = FILE_STORAGES
        # SkipError:
        if self.skipError == "skip":
            self.skipError = SkipErrors.SKIP
        elif self.skipError == "log":
            self.skipError = SkipErrors.LOG
        else:
            self.skipError = SkipErrors.ENFORCE

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

        Run operations declared inside Component.
        """

    @abstractmethod
    async def close(self):
        """
        close.

        Close (if needed) component requirements.
        """

    def ComponentName(self):
        return self.__name__

    def user_params(self):
        return self._params

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    def setVar(self, name, value):
        self._variables[name] = value

    def setTaskVar(self, name: str, value: Any):
        name = f"{self.StepName}_{name}"
        self._variables[name] = value

    def set_attributes(self, name: str = "pattern"):
        if hasattr(self, name):
            obj = getattr(self, name)
            for field, val in obj.items():
                if field in self._params:
                    # already calculated:
                    self._attrs[field] = self._params[field]
                    setattr(self, field, self._params[field])
                elif field in self._attributes:
                    self._attrs[field] = self._attributes[field]
                    setattr(self, field, self._attributes[field])
                elif field in self._parameters:
                    self._attrs[field] = self._parameters[field]
                    setattr(self, field, self._parameters[field])
                elif field in self._variables:
                    self._attrs[field] = self._variables[field]
                    setattr(self, field, self._variables[field])
                else:
                    value = self.getFunc(val)
                    self._attrs[field] = value
                    setattr(self, field, value)
            del self._attrs["pattern"]

    def get_obj(self, name, parent):
        try:
            if not parent:
                return getattr(self, name)
            else:
                return parent[name]
        except AttributeError:
            return False

    def get_pattern(self, obj):
        try:
            pattern = obj["pattern"]
            # del obj['pattern']
            return pattern, obj
        except Exception:
            return None, obj

    def process_pattern(self, name: str = "file", parent=None):
        if not (obj := self.get_obj(name, parent)):
            return False
        # pattern has the form {file, value}:
        if not isinstance(obj, dict):
            return obj

        # first, I need the pattern object:
        pattern, obj = self.get_pattern(obj)
        if pattern is None:
            return obj

        # processing the rest of variables:
        if self._vars and f"{name}.pattern" in self._vars:
            pattern = self._vars[f"{name}.pattern"]
        elif self._variables and "pattern" in self._variables:
            pattern = self._variables["pattern"]
        elif "value" in self._variables:
            pattern = pattern.format_map(SafeDict(value=self._variables["value"]))
        if self._vars and f"{name}.value" in self._vars:
            result = self._vars[f"{name}.value"]
            return pattern.format_map(SafeDict(value=result))
        elif "value" in obj:
            # simple replacement:
            result = self.getFunc(obj["value"])
            return pattern.format_map(SafeDict(value=result))
        elif "values" in obj:
            variables = {}
            result = obj["values"]
            for key, val in result.items():
                variables[key] = self.getFunc(val)
            return pattern.format_map(SafeDict(**variables))
        else:
            # multi-value replacement
            variables = {}
            if self._variables:
                pattern = pattern.format_map(SafeDict(**self._variables))
            for key, val in obj.items():
                if key in self._variables:
                    variables[key] = self._variables[key]
                else:
                    variables[key] = self.getFunc(val)
            # Return the entire object with the formatted pattern
            return pattern.format_map(SafeDict(**variables))

    def process_mask(self, name):
        if hasattr(self, name):
            obj = getattr(self, name)
            for key, value in obj.items():
                if key in self._vars:
                    obj[key] = self._vars[key]
                elif self._vars and f"{name}.{key}" in self._vars:
                    obj[key] = self._vars[f"{name}.{key}"]
                elif key in self._variables:
                    obj[key] = self._variables[key]
                else:
                    # processing mask
                    for mask, replace in self._mask.items():
                        if mask in value:
                            obj[key] = value.replace(mask, str(replace))
            return obj
        else:
            return {}

    def var_replacement(self, obj: dict):
        """var_replacement.

        Replacing occurrences of Variables into an String.
        Args:
            obj (Any): Any kind of object.

        Returns:
            Any: Object with replaced variables.
        """
        if not isinstance(obj, dict):
            return obj
        for var, replace in obj.items():
            if var in self._mask:
                value = self._mask[var]
            else:
                if isinstance(replace, str):
                    value = replace.format_map(SafeDict(**self._variables))
                elif var in self._variables:
                    value = self._variables[var]
                else:
                    value = replace
            if isinstance(obj, PurePath):
                value = Path(value).resolve()
            obj[var] = value
        return obj

    def set_variables(self, obj):
        return obj.format_map(SafeDict(**self._variables))

    def set_conditions(self, name: str = "conditions"):
        if hasattr(self, name):
            obj = getattr(self, name)
            for condition, val in obj.items():
                self._logger.notice(
                    f":: Condition : {condition} = {val}"
                )
                if hasattr(self, condition):
                    obj[condition] = getattr(self, condition)
                elif is_constant(val):
                    obj[condition] = get_constant(val)
                elif is_function(val):
                    obj[condition] = get_func_value(val)
                if condition in self._variables:
                    obj[condition] = self._variables[condition]
                elif condition in self._mask:
                    obj[condition] = self._mask[condition]
                elif condition in self.conditions:
                    obj[condition] = val
            if "pattern" in obj:
                pattern = obj["pattern"]
                del obj["pattern"]
                # getting conditions as patterns
                for field in pattern:
                    if field in obj:
                        # already settled
                        continue
                    if field in self._params:
                        obj[field] = self._params[field]
                    else:
                        result = None
                        val = pattern[field]
                        if is_constant(val):
                            result = get_constant(val)
                        else:
                            result = self.getFunc(val)
                        obj[field] = result

    def conditions_replacement(self, obj: str):
        """conditions_replacement.

        Replacing occurrences of Conditions into an String.
        Args:
            obj (Any): Any kind of object.

        Returns:
            Any: Object with replaced conditions.
        """
        try:
            return obj.format_map(SafeDict(**self.conditions))
        except (KeyError, ValueError) as err:
            self._logger.error(f"Error in conditions_replacement: {err}")
            return obj
        except Exception as err:
            self._logger.error(f"Error in conditions_replacement: {err}")
            return obj

    def get_filename(self):
        """
        get_filename.
        Detect if File exists.
        """
        if not self.filename:  # pylint: disable=E0203
            if hasattr(self, "file") and self.file:
                file = self.get_filepattern()
                if filelist := glob.glob(os.path.join(self.directory, file)):
                    self.filename = filelist[0]
                    self._variables["__FILEPATH__"] = self.filename
                    self._variables["__FILENAME__"] = os.path.basename(self.filename)
                else:
                    raise FileNotFound(f"File is empty or doesn't exists: {file}")
            elif self.previous:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = filenames[0]
                        self._variables["__FILEPATH__"] = self.filename
                        self._variables["__FILENAME__"] = os.path.basename(
                            self.filename
                        )
                    except IndexError as e:
                        raise FileNotFound(
                            f"({__name__}): File is empty or doesn't exists"
                        ) from e
            else:
                raise FileNotFound(f"({__name__}): File is empty or doesn't exists")
        else:
            return self.filename

    def _print_data_(self, df, title: str = None) -> None:
        if not title:
            title = self.__class__.__name__
        print(f"::: Printing {title} === ")
        print("Data: ", df)
        if df.empty:
            print("The DataFrame is empty.")
        else:
            for column, t in df.dtypes.items():
                print(f"{column} -> {t} -> {df[column].iloc[0]}")

    # Processing Tasks
    def split_parts(self, task_list, num_parts: int = 5) -> list:
        part_size, remainder = divmod(len(task_list), num_parts)
        parts = []
        start = 0
        for i in range(num_parts):
            # Distribute the remainder across the first `remainder` parts
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(task_list[start:end])
            start = end
        return parts

    async def _processing_tasks(
        self,
        tasks: list,
        description: str = ': Processing :',
        show_progress: bool = False,
        concurrently: bool = True,
        chunk_size: int = 10,
        return_exceptions: bool = False,
    ) -> Any:
        """Process tasks concurrently."""
        results = []
        total_tasks = len(tasks)
        pbar = None
        if show_progress:
            pbar = tqdm(total=total_tasks, desc=description)
        try:
            if concurrently:
                for chunk in self.split_parts(tasks, num_parts=chunk_size):
                    # ─── Wrap every coroutine in this chunk into a Task ───
                    if show_progress:
                        pending = [asyncio.create_task(coro) for coro in chunk]
                        # Schedule only this chunk concurrently:
                        for coro in asyncio.as_completed(pending):
                            res = await coro
                            results.append(res)
                            pbar.update(1)
                            await asyncio.sleep(0)
                    else:
                        result = await asyncio.gather(*chunk, return_exceptions=return_exceptions)
                        results.extend(result)
            else:
                # run every task in a sequential manner:
                for task in tasks:
                    try:
                        res = await task
                        results.append(res)
                        if show_progress:
                            pbar.update(1)
                            await asyncio.sleep(
                                random.uniform(0, 0.25)
                            )
                    except Exception as e:
                        self._logger.error(
                            f"Processing Task error: {str(e)}"
                        )
        finally:
            if show_progress:
                pbar.close()
        return results

    def get_version(self) -> str:
        return self._version

from typing import Optional
from abc import ABC
import asyncio
import importlib
import builtins
from navconfig.logging import logging
## functions
import querysource.utils.functions as qsfunctions  # pylint: disable=W0401,C0411
from ..utils import functions as ffunctions  # pylint: disable=W0614,W0401
from ..exceptions import ComponentError, ConfigError
from ..types import SafeDict


class FuncSupport(ABC):
    """
    Interface for adding Add Support for Function Replacement.
    """
    def __init__(self, *args, **kwargs):
        self._loop = self.event_loop(evt=kwargs.get('loop', None))
        super().__init__(*args, **kwargs)

    def event_loop(
        self, evt: Optional[asyncio.AbstractEventLoop] = None
    ) -> asyncio.AbstractEventLoop:
        if evt is not None:
            asyncio.set_event_loop(evt)
            return evt
        else:
            try:
                return asyncio.get_event_loop()
            except RuntimeError as exc:
                raise RuntimeError(
                    f"There is no Event Loop: {exc}"
                ) from exc

    def _get_function(self, fname):
        try:
            # First: check if function exists on QuerySource:
            return getattr(qsfunctions, fname)
        except (TypeError, AttributeError):
            pass
        # Second: check if function exists on FlowTask:
        try:
            return getattr(ffunctions, fname)
        except (TypeError, AttributeError):
            pass

        # Then, try to get the function from globals()
        try:
            func = globals().get(fname)
            if func:
                return func
        except (TypeError, AttributeError):
            pass

        # Third: check if function exists on builtins:
        try:
            return getattr(builtins, fname)
        except (TypeError, AttributeError):
            pass

        # If the function name contains dots, try to import the module and get the attribute
        if '.' in fname:
            components = fname.split('.')
            module_name = '.'.join(components[:-1])
            attr_name = components[-1]

            try:
                module = importlib.import_module(module_name)
                func = getattr(module, attr_name)
                return func
            except (ImportError, AttributeError) as e:
                # Function doesn't exists:
                raise ConfigError(
                    f"Function {fname} doesn't exists.: {e}"
                ) from e
        logging.warning(
            f"Function {fname} not found in any known modules."
        )
        return None

    def getFunc(self, val):
        try:
            if isinstance(val, list):
                fname, args = (val + [{}])[:2]  # Safely unpack with default args
                fn = self._get_function(fname)
                if isinstance(args, dict):
                    return fn(**args)
                elif isinstance(args, list):
                    return fn(*args)
                else:
                    return fn()
            elif val in self._variables:
                return self._variables[val]
            elif val in self._mask:
                return self._mask[val]
            else:
                return val
        except ConfigError:
            pass
        except Exception as err:
            raise ComponentError(
                f"{__name__}: Error parsing Function {val!r}: {err}"
            ) from err

    def get_filepattern(self):
        if not hasattr(self, "file"):
            return None
        fname = self.file["pattern"]
        result = None
        try:
            val = self.file.get("value", fname)
            if isinstance(val, str):
                if val in self._variables:
                    # get from internal variables
                    result = self._variables[val]
            elif isinstance(val, list):
                func = val[0]
                func, args = (val + [{}])[:2]  # Safely unpack with default args
                fn = self._get_function(fname)
                try:
                    result = fn(**args) if args else fn()
                except (TypeError, AttributeError):
                    try:
                        if args:
                            result = globals()[func](**args)
                        else:
                            result = globals()[func]()
                    except (TypeError, ValueError) as e:
                        logging.error(str(e))
            else:
                result = val
        except ConfigError:
            pass
        except (NameError, KeyError) as err:
            logging.warning(f"FilePattern Error: {err}")
        return fname.format_map(SafeDict(value=result))

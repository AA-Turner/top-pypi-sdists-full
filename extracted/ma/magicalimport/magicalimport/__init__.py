import logging
import os.path
import sys
from importlib import import_module as import_module_original
from importlib.util import spec_from_file_location
from importlib.util import module_from_spec

logger = logging.getLogger(__name__)


# Moved from compat.py
def _create_module(module_id, path):
    spec = spec_from_file_location(module_id, path)
    module = module_from_spec(spec)
    sys.modules[module_id] = module
    spec.loader.exec_module(module)
    return module


def expose_all_members(module, globals_=None, _depth=2):
    members = {k: v for k, v in module.__dict__.items() if not k.startswith("_")}
    return expose_members(module, members, globals_=globals_, _depth=_depth)


def expose_members(module, members, globals_=None, _depth=1):
    if globals_ is None:
        frame = sys._getframe(_depth)  # xxx: black magic
        globals_ = frame.f_globals
    globals_.update({k: module.__dict__[k] for k in members})
    return globals_


def _module_id_from_path(path):
    logger.debug("	-> %s (path)", path)

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)

    module_id = "{}.{}".format(dirname.replace("/", "_"), basename.rsplit(".py", 1)[0])
    logger.debug("	<- %s (module_id)", module_id)
    return module_id


_FAILED = set()  # singleton


def import_from_physical_path(path, as_=None, here=None, _depth=1, cwd=True):
    global _FAILED

    if here is None:
        if cwd:
            here = os.getcwd()
        elif _depth > 0:
            frame = sys._getframe(_depth)  # xxx: black magic
            here = frame.f_globals["__file__"]
        else:
            raise ValueError(
                "invalid option found _depth={}, cwd={}".format(_depth, cwd)
            )
    if here is not None:
        here = here if os.path.isdir(here) else os.path.dirname(here)
        here = os.path.abspath(here)
        path = os.path.join(here, path)

    path = os.path.normpath(os.path.abspath(path))

    module_id = as_ or _module_id_from_path(path)
    if module_id in sys.modules:
        return sys.modules[module_id]

    guess_path = path.replace("/__init__.py", "")

    if as_ is None:
        for sys_path in sys.path:
            if not guess_path.startswith(sys_path):
                continue

            guessed_module = (
                guess_path[len(sys_path) :]
                .lstrip("/")
                .rsplit(".py", 1)[0]
                .replace("/", ".")
            )
            if guessed_module in _FAILED:
                continue

            try:
                m = import_module_original(guessed_module)
                return m
            except ModuleNotFoundError:
                _FAILED.add(guessed_module)
            except ImportError as e:
                if ImportError.__module__ != ModuleNotFoundError.__module__:
                    if str(e).startswith("No module named"):
                        _FAILED.add(guessed_module)
                        continue
                raise

    if "." in module_id and as_ is None:
        parent_module_id = module_id.rsplit(".")[0]
        if parent_module_id not in sys.modules:
            init_py = os.path.join(os.path.dirname(path), "__init__.py")
            if os.path.exists(init_py):
                _create_module(parent_module_id, init_py)
            else:
                # TODO: don't have to create __init__.py
                try:
                    with open(init_py, "w"):
                        pass
                    _create_module(parent_module_id, init_py)
                    # # xxx: using fake module as parent module
                    # import magicalimport._fake as fake_module

                    # parent_module = _create_module(parent_module_id, fake_module.__file__)
                    # parent_module.__file__ = init_py
                except PermissionError as e:
                    module_id = module_id.replace(".", "_")
                    logger.warn(
                        "open %s, cannot accessable (%r). new module_id is %r",
                        init_py,
                        e,
                        module_id,
                    )
    try:
        return _create_module(module_id, path)
    except (FileNotFoundError, OSError) as e:
        raise ModuleNotFoundError(e)


def import_module(module_path, here=None, sep=":", _depth=2, cwd=True):
    _, ext = os.path.splitext(module_path)
    if ext == ".py":
        m = import_from_physical_path(module_path, here=here, _depth=_depth, cwd=cwd)
        logger.debug("import module %s", m)
        return m
    else:
        try:
            return import_module_original(module_path)
        except ImportError as e:
            if ImportError.__module__ == ModuleNotFoundError.__module__:
                raise
            raise ModuleNotFoundError(e)


def import_symbol(sym, here=None, sep=":", ns=None, silent=False, _depth=3, cwd=True):
    if ns is not None and sep not in sym:
        sym = "{}{}{}".format(ns, sep, sym)
    module_path, fn_name = sym.rsplit(sep, 2)
    try:
        module = import_module(module_path, here=here, sep=sep, _depth=_depth, cwd=cwd)
    except (
        ImportError,
        ModuleNotFoundError,
    ) as e:  # ModuleNotFoundError is subclass of ImportError
        if not silent:
            sys.stderr.write("could not import {!r}\n{}\n".format(sym, e))
        raise
    try:
        return getattr(module, fn_name)
    except AttributeError as e:
        if not silent:
            sys.stderr.write("could not import {!r}\n{}\n".format(sym, e))
        raise ImportError(e)

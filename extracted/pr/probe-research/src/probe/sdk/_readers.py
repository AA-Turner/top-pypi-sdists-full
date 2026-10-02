"""Readers (and two writers) that open files from C, told to the recorder.

The read recorder watches Python's ``open`` audit event (PEP 578), and a
library that opens its files from C or Rust never raises it. For the ones
measured to matter -- Parquet, Arrow memory maps (the Hugging Face ``datasets``
cache), HDF5, safetensors, and ``torch.save`` -- this module wraps the Python
entry point so the path reaches the recorder all the same:

* ``pyarrow.parquet``: ``ParquetFile(path)``, ``read_metadata`` and
  ``read_schema`` note the file they open; ``ParquetDataset.read()`` notes
  the files that read scans -- after the
  partition filter, capped (MAX_DATASET_FILES) -- and never at construction:
  opening a dataset is not reading it. ``read_table`` and ``read_pandas`` (and
  pandas' ``read_parquet``) go through one of the two, so they are seen too.
  Only a dataset made from local PATHS is listed, as its wrapped ``__init__``
  saw them (one made before the recorder started is not): one made from a
  file object (pandas' ``read_parquet(file)`` opens the file itself and hands
  pyarrow the handle) was opened with Python's ``open``, which the audit hook
  already saw -- and its native dataset is never touched:
  ``_dataset.filesystem`` on it SEGFAULTS pyarrow (18 to 25 at least).
  A ``pyarrow.dataset`` Dataset read on its own (``to_table``, ``scanner``) is
  NOT: its types are immutable C++ wrappers, and a proxy would break every
  ``isinstance`` check; the coverage says so.
* ``pyarrow.memory_map(path, mode)``: ``"r"`` is a read, any other mode a write.
* ``h5py.File(path, mode)``: ``"r"`` is a read; ``"w"``, ``"w-"``, ``"x"``,
  ``"a"`` and ``"r+"`` are writes.
* ``safetensors.safe_open`` (a stand-in class: ``isinstance`` still works)
  and every framework module's ``load_file``.
* ``torch.save(obj, path)``: a write (it writes from C++). ``torch.load`` opens
  its file with Python's ``open`` and needs no wrapper.

A wrapper hands the recorder the path and its CALLER's frame (so Probe's own
calls are told apart exactly as the audit hook tells them), and does nothing
else: no stat, no read, no listing of its own -- with no run recording it
costs a function call. Only local paths are noted (a URI, a file object or a
remote filesystem is not a file on this machine). A wrapper judges only the
arguments its caller passed, never a property of the library's own objects:
those are native, lazy, and can crash the process (see ``pyarrow.parquet``).

INSTALLED LAZILY. :func:`install` patches the libraries already imported and
puts a finder first on ``sys.meta_path`` that patches the others right after
they are imported; nothing here imports any of them. The classes are patched in
place, so they are seen however they were imported. A function a module bound
by name BEFORE the patch (``from safetensors import safe_open`` in a library
imported before ``probe.init()`` -- transformers does) is pointed at its
wrapper once, at install (`_Patcher.rebind`); one held any other way (a default
argument, an attribute) keeps the original.

STDLIB ONLY, and valid on every Python with audit hooks: the same source runs
inside the hook ``probe exec`` and a run's spawned workers get through an
injected ``sitecustomize`` (``inputs.CHILD_SITE_CODE``), where Probe may not be
importable.
"""

from __future__ import annotations

import functools
import itertools
import os
import sys
import threading
import time

#: The files one ``ParquetDataset.read()`` notes at most (a million-file
#: dataset is not listed in the caller's time); past it the recorder is told
#: the list was cut (``truncated``).
MAX_DATASET_FILES = 10_000

_WRITE_MODES = ("w", "w-", "x", "a", "r+")


def _local_path(value):
    """``value`` as a local path string, or None: a file object, a buffer, a
    URI (``s3://``, ``hf://``, ``file://``...) is not a file this hook sees."""
    try:
        if isinstance(value, bytes):
            value = os.fsdecode(value)
        elif not isinstance(value, str) and hasattr(value, "__fspath__"):
            value = os.fspath(value)
            if isinstance(value, bytes):
                value = os.fsdecode(value)
    except Exception:  # noqa: BLE001 -- a user object's __fspath__ may raise
        return None
    if not isinstance(value, str) or not value or "://" in value:
        return None
    return value


def _local_fs(filesystem) -> bool:
    """A pyarrow (or fsspec) filesystem that is this machine's disk."""
    return filesystem is None or type(filesystem).__name__ == "LocalFileSystem"


#: Set on a ``ParquetDataset`` by its wrapped ``__init__``: True when it was
#: made from local paths (`_local_paths`), which ``read()`` may then list.
_LOCAL_SOURCE = "_probe_local_source"


def _local_paths(source) -> bool:
    """Whether a ``ParquetDataset`` source is local PATHS -- a str or
    ``os.PathLike`` (what pyarrow itself takes for a path), or a list of them
    -- and not a file object, a buffer or a URI. Judged from the argument
    alone."""

    def one(value) -> bool:
        return (isinstance(value, str) or hasattr(value, "__fspath__")) and _local_path(value) is not None

    if isinstance(source, list):
        return bool(source) and all(one(value) for value in source)
    return one(source)


def _class_proxy(original: type, before, home: str) -> type:
    """A stand-in for a CLASS that must be wrapped (``safetensors.safe_open``,
    a Rust type that cannot be patched or subclassed): calling it calls
    ``before`` and returns an instance of the REAL class, and ``isinstance``
    / ``issubclass`` against it answer for the real class. It pickles by
    reference as ``home``'s attribute, where it is installed."""

    class _Proxy(type):
        def __call__(cls, *args, **kwargs):
            try:
                before(args, kwargs, sys._getframe(1))
            except Exception:  # noqa: BLE001
                pass
            return original(*args, **kwargs)

        def __instancecheck__(cls, obj) -> bool:
            return isinstance(obj, original)

        def __subclasscheck__(cls, sub) -> bool:
            return issubclass(sub, original)

        def __getattr__(cls, name):
            return getattr(original, name)

    return _Proxy(
        original.__name__,
        (),
        {
            "__module__": home or original.__module__,
            "__qualname__": original.__qualname__,
            "__doc__": original.__doc__,
            "__wrapped__": original,
        },
    )


class _Patcher:
    """One recorder's wrappers: ``note_read(path, frame)``,
    ``note_write(path, frame)`` and ``truncated()`` are the recorder's;
    ``active()`` says whether anything records in this process now (a
    wrapper with a cost of its own -- a dataset's file listing -- asks it
    first)."""

    def __init__(self, note_read, note_write, truncated, active=lambda: True) -> None:
        self.note_read = note_read
        self.note_write = note_write
        self.truncated = truncated
        self.active = active
        #: Marks this patcher's wrappers, so a second import (a reload) is
        #: patched again but nothing is wrapped twice by the same recorder.
        self.token = object()
        #: id(original) -> (original, its ONE wrapper), reused at every place
        #: the original is reachable (``torch.save`` and
        #: ``torch.serialization.save``): a function pickles by reference, by
        #: its module and name, and two wrappers of one function made
        #: ``Pool.map(pq.read_metadata, ...)`` fail to pickle.
        self.wrappers: dict = {}
        #: The ids in `wrappers` whose original a module holds as a global
        #: (not a method): what `rebind` looks for.
        self.globals: set = set()

    # -- the wrappers ------------------------------------------------------

    def _tell(self, note, path, frame) -> None:
        path = _local_path(path)
        if path is None:
            return
        try:
            note(path, frame)
        except Exception:  # noqa: BLE001 -- recording never breaks the caller
            pass

    def _wrap(self, original, before, home: str):
        """``original``'s one wrapper, ``before(args, kwargs, frame)`` called
        first. A CLASS gets a class back (`_class_proxy`): ``isinstance`` and
        ``issubclass`` against it keep working."""
        if getattr(original, "__probe_wrapped_by__", None) is self.token:
            return original
        known = self.wrappers.get(id(original))
        if known is not None and known[0] is original:
            return known[1]
        if isinstance(original, type):
            wrapped = _class_proxy(original, before, home)
        else:

            @functools.wraps(original)
            def wrapped(*args, **kwargs):
                try:
                    before(args, kwargs, sys._getframe(1))
                except Exception:  # noqa: BLE001
                    pass
                return original(*args, **kwargs)

        wrapped.__probe_wrapped_by__ = self.token
        self.wrappers[id(original)] = (original, wrapped)
        return wrapped

    def _set(self, owner, name, before) -> None:
        original = getattr(owner, name, None)
        if original is None or not callable(original):
            return
        home = owner.__name__ if not isinstance(owner, type) else getattr(owner, "__module__", "")
        wrapped = self._wrap(original, before, home)
        if wrapped is not original:
            try:
                setattr(owner, name, wrapped)
            except (AttributeError, TypeError):
                return
            if not isinstance(owner, type):
                self.globals.add(id(original))

    def rebind(self, budget_s: float = 0.25) -> None:
        """Point every module global that IS a patched original at its one
        wrapper: a name imported before the patch (``from safetensors import
        safe_open``, ``from safetensors.torch import load_file as
        safe_load_file``) would otherwise keep reading unseen. Once, at
        install, within ``budget_s``; identity only, never a name guess. A
        class is left alone in the module its ``__module__`` names. A type
        made in Rust or C often names ``builtins``, and is then replaced
        where it is defined too (``safetensors._safetensors_rust.safe_open``,
        when safetensors was imported before the recorder started): harmless,
        since the stand-in answers ``isinstance`` for it (`_class_proxy`)."""
        if not self.globals:
            return
        stop = time.monotonic() + budget_s
        wrappers, wanted = self.wrappers, self.globals
        for module in list(sys.modules.values()):
            if time.monotonic() >= stop:
                return
            space = getattr(module, "__dict__", None)
            if not isinstance(space, dict):
                continue
            try:
                hits = [name for name, value in space.items() if id(value) in wanted]
            except RuntimeError:  # the module changed while it was read
                continue
            for name in hits:
                value = space.get(name)
                pair = wrappers.get(id(value))
                if pair is None or pair[0] is not value:
                    continue
                if isinstance(value, type) and getattr(value, "__module__", None) == space.get("__name__"):
                    continue
                space[name] = pair[1]

    # -- per library -----------------------------------------------------------

    def pyarrow(self, module) -> None:
        def memory_map(args, kwargs, frame):
            path = args[0] if args else kwargs.get("path")
            mode = args[1] if len(args) > 1 else kwargs.get("mode", "r")
            note = self.note_read if (mode or "r") == "r" else self.note_write
            self._tell(note, path, frame)

        self._set(module, "memory_map", memory_map)
        lib = getattr(module, "lib", None)
        if lib is not None:
            self._set(lib, "memory_map", memory_map)

    def parquet(self, module) -> None:
        core = sys.modules.get("pyarrow.parquet.core", module)

        def parquet_file(args, kwargs, frame):
            # (self, source, *, ..., filesystem=None, ...)
            if _local_fs(kwargs.get("filesystem")):
                self._tell(self.note_read, args[1] if len(args) > 1 else kwargs.get("source"), frame)

        def dataset_init(args, kwargs, frame):
            # (self, path_or_paths, filesystem=None, ...): whether the dataset
            # is made from local paths, from the caller's arguments only -- the
            # dataset pyarrow builds from a file object crashes the process
            # when its `filesystem` is read, so `dataset_read` never asks it.
            dataset = args[0] if args else None
            source = args[1] if len(args) > 1 else kwargs.get("path_or_paths")
            filesystem = args[2] if len(args) > 2 else kwargs.get("filesystem")
            setattr(dataset, _LOCAL_SOURCE, _local_fs(filesystem) and _local_paths(source))

        def dataset_read(args, kwargs, frame):
            if not self.active():
                return  # nothing records: no listing at all
            dataset = args[0] if args else None
            # A dataset made from anything but local paths is left alone: a
            # file object was opened with Python's `open`, which the audit
            # hook saw, and a remote one is not a file on this machine.
            if getattr(dataset, _LOCAL_SOURCE, False) is not True:
                return
            inner = getattr(dataset, "_dataset", None)
            if inner is None:
                return
            fragments = inner.get_fragments(filter=getattr(dataset, "_filter_expression", None))
            taken = list(itertools.islice(fragments, MAX_DATASET_FILES + 1))
            if len(taken) > MAX_DATASET_FILES:
                del taken[MAX_DATASET_FILES:]
                self.truncated()
            for fragment in taken:
                self._tell(self.note_read, getattr(fragment, "path", None), frame)

        def footer(args, kwargs, frame):
            # read_metadata / read_schema (where, memory_map=False, decryption_properties=None,
            # filesystem=None, ...): they open the file, then hand ParquetFile a file object.
            filesystem = args[3] if len(args) > 3 else kwargs.get("filesystem")
            if _local_fs(filesystem):
                self._tell(self.note_read, args[0] if args else kwargs.get("where"), frame)

        for cls_name, method, before in (
            ("ParquetFile", "__init__", parquet_file),
            ("ParquetDataset", "__init__", dataset_init),
            ("ParquetDataset", "read", dataset_read),
        ):
            cls = getattr(core, cls_name, None)
            if isinstance(cls, type):
                self._set(cls, method, before)
        for owner in {id(core): core, id(module): module}.values():
            self._set(owner, "read_metadata", footer)
            self._set(owner, "read_schema", footer)

    def h5py(self, module) -> None:
        def h5_file(args, kwargs, frame):
            # (self, name, mode='r', ...)
            name = args[1] if len(args) > 1 else kwargs.get("name")
            mode = args[2] if len(args) > 2 else kwargs.get("mode")
            write = (mode or "r") in _WRITE_MODES
            self._tell(self.note_write if write else self.note_read, name, frame)

        cls = getattr(module, "File", None)
        if isinstance(cls, type):
            self._set(cls, "__init__", h5_file)

    def safetensors(self, module) -> None:
        def first(args, kwargs, frame):
            self._tell(self.note_read, args[0] if args else kwargs.get("filename"), frame)

        self._set(module, "safe_open", first)
        if module.__name__ != "safetensors":
            self._set(module, "load_file", first)

    def torch(self, module) -> None:
        def save(args, kwargs, frame):
            self._tell(self.note_write, args[1] if len(args) > 1 else kwargs.get("f"), frame)

        self._set(module, "save", save)
        serialization = sys.modules.get("torch.serialization")
        if serialization is not None:
            self._set(serialization, "save", save)

    def patches(self) -> dict:
        """module name -> what to patch once it is imported."""
        out = {
            "pyarrow": self.pyarrow,
            "pyarrow.parquet": self.parquet,
            "h5py": self.h5py,
            "safetensors": self.safetensors,
            "torch": self.torch,
        }
        for framework in ("torch", "numpy", "flax", "tensorflow", "paddle", "mlx"):
            out["safetensors." + framework] = self.safetensors
        return out


class _PatchingLoader:
    """A module's own loader, and the patch run right after it executed."""

    def __init__(self, loader, patch) -> None:
        self._loader = loader
        self._patch = patch

    def create_module(self, spec):
        create = getattr(self._loader, "create_module", None)
        return create(spec) if create is not None else None

    def exec_module(self, module) -> None:
        self._loader.exec_module(module)
        try:
            self._patch(module)
        except Exception:  # noqa: BLE001 -- a patch that fails leaves the library as it was
            pass

    def __getattr__(self, name):
        return getattr(self._loader, name)


class _Finder:
    """First on ``sys.meta_path``: finds nothing itself, but hands a wanted
    module's spec back with a loader that patches it after it runs."""

    def __init__(self, patches: dict) -> None:
        self.patches = patches
        self._busy = threading.local()

    def find_spec(self, name, path=None, target=None):
        patch = self.patches.get(name)
        if patch is None or getattr(self._busy, "on", False):
            return None
        self._busy.on = True
        try:
            spec = None
            for finder in list(sys.meta_path):
                find = getattr(finder, "find_spec", None)
                if finder is self or find is None:
                    continue
                spec = find(name, path, target)
                if spec is not None:
                    break
        finally:
            self._busy.on = False
        if spec is None or spec.loader is None or not hasattr(spec.loader, "exec_module"):
            return spec
        spec.loader = _PatchingLoader(spec.loader, patch)
        return spec


def install(note_read, note_write, truncated=lambda: None, active=lambda: True) -> None:
    """Wrap the readers above for one recorder: those already imported now,
    the rest as they are imported. ``note_read(path, frame)`` /
    ``note_write(path, frame)`` get a local path and the caller's frame;
    ``truncated()`` says a dataset's file list was cut; ``active()`` whether
    anything records now. Never raises."""
    try:
        patcher = _Patcher(note_read, note_write, truncated, active)
        patches = patcher.patches()
        sys.meta_path.insert(0, _Finder(patches))
        for name, patch in patches.items():
            module = sys.modules.get(name)
            if module is not None:
                try:
                    patch(module)
                except Exception:  # noqa: BLE001
                    pass
        patcher.rebind()
    except Exception:  # noqa: BLE001 -- the recorder works without them
        pass

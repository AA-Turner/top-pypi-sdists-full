"""Import modules on demand.

Lazy importing is a detail best kept to library writers. Application writers
should not need to use lazy imports at all. Callees are in a much better
position to know whether it is safe to delay or reorder imports, so it is they
who should be lazy on behalf of their callers.

PEP-690 (Lazy Imports, Rejected) [1] and its associated discussion threads give
more background on lazy imports.

[1] https://peps.python.org/pep-0690/
"""

import importlib.abc
import importlib.machinery
import importlib.util
import sys
import types


class _LazyModule(types.ModuleType):
    """A subclass of the module type which triggers loading upon attribute access."""

    # Originally from importlib.util._LazyModule.
    #
    # 2023-12-30(corvic): Add addition checks to avoid import edge cases

    def __getattribute__(self, attr: str):
        """Trigger the load of the module and return the attribute."""
        # All module metadata must be garnered from __spec__ in order to avoid
        # using mutated values.
        # Stop triggering this method.
        self.__class__ = types.ModuleType
        assert self.__spec__ is not None
        assert self.__spec__.loader is not None
        # Get the original name to make sure no object substitution occurred
        # in sys.modules.
        original_name = self.__spec__.name
        if attr.startswith("__"):
            if attr == "__path__":
                raise ValueError(
                    f"{original_name!r} used in nested import; lazy loading is unsafe"
                )
            if attr not in ("__spec__", "__file__"):
                # __spec__ is what from X import Y first uses
                # __file__ is called by benign introspection routines
                raise ValueError(
                    f"unexpected {original_name!r}.{attr}: lazy loading is unsafe"
                )
        # Figure out exactly what attributes were mutated between the creation
        # of the module and now.
        attrs_then = self.__spec__.loader_state["__dict__"]
        attrs_now = self.__dict__
        # Code that set the attribute may have kept a reference to the
        # assigned object, making identity more important than equality.
        attrs_updated = {
            key: value
            for key, value in attrs_now.items()
            if key not in attrs_then or id(value) != id(attrs_then[key])
        }
        self.__spec__.loader.exec_module(self)
        # If exec_module() was used directly there is no guarantee the module
        # object was put into sys.modules.
        if original_name in sys.modules and id(self) != id(sys.modules[original_name]):
            raise ValueError(
                f"module object for {original_name!r} changed in sys.modules \
during lazy load"
            )
        # Update after loading since that's what would happen in an eager
        # loading situation.
        self.__dict__.update(attrs_updated)
        return getattr(self, attr)

    def __delattr__(self, attr: str):
        """Trigger the load and then perform the deletion."""
        # To trigger the load and raise an exception if the attribute
        # doesn't exist.
        self.__getattribute__(attr)
        delattr(self, attr)


class _LazyLoader(importlib.abc.Loader):
    """A loader that creates a module which defers loading until attribute access."""

    # Originally from importlib.util.LazyLoader.
    #
    # 2023-12-30(corvic): Modified to use _LazyModule

    @staticmethod
    def __check_eager_loader(loader: importlib.abc.Loader):
        if not hasattr(loader, "exec_module"):
            raise TypeError("loader must define exec_module()")

    def __init__(self, loader: importlib.abc.Loader):
        self.__check_eager_loader(loader)
        self.loader = loader

    def create_module(self, spec: importlib.machinery.ModuleSpec):
        return self.loader.create_module(spec)

    def exec_module(self, module: types.ModuleType):
        """Make the module load lazily."""
        assert module.__spec__ is not None
        module.__spec__.loader = self.loader
        module.__loader__ = self.loader
        # Don't need to worry about deep-copying as trying to set an attribute
        # on an object would have triggered the load,
        # e.g. ``module.__spec__.loader = None`` would trigger a load from
        # trying to access module.__spec__.
        loader_state = {}
        loader_state["__dict__"] = module.__dict__.copy()
        loader_state["__class__"] = module.__class__
        module.__spec__.loader_state = loader_state
        module.__class__ = _LazyModule


def lazy_import(name: str):
    """Delay import of a module until one of its attributes is accessed.

    Commonly used to wrap modules that take a long time to import so that the
    importing module doesn't also take a long time to import.

    Since this changes when import happens from the import statement site to
    when the module is used, errors that would normally be raised when
    the caller imports the module will be postponed and out of context.

    Additional caveats from importlib.util.LazyLoader, which lazy_import wraps:

        This class only works with loaders that define exec_module() as control
        over what module type is used for the module is required. For those
        same reasons, the loader's create_module() method must return None or a
        type for which its __class__ attribute can be mutated along with not
        using slots. Finally, modules which substitute the object placed into
        sys.modules will not work as there is no way to properly replace the
        module references throughout the interpreter safely; ValueError is
        raised if such a substitution is detected.

    Example of use:

        import typing

        if typing.TYPE_CHECKING:
            import slow_module
        else:
            slow_module = lazy_import("slow_module")

    There are limitations to how long loading can be deferred and how a lazy
    module can be used.

    In a nested module, e.g., parent.slow_module, even if the child module
    loading is deferred, the parent module must be loaded to resolve the child
    module attribute itself:

        # Parent is loaded even if child is deferred.
        slow_module = lazy_import("parent.slow_module")

        # Deferring the parent doesn't help
        parent = lazy_import("parent")
        # ... parent must be loaded now to resolve the attribute access
        # parent.slow_module
        slow_module = lazy_import("parent.slow_module")

    For these cases, the only resolution is to move the import statement inside
    a function.

    A lazy module should only be used with direct attribute access or in part
    of a from-import statement. Other uses, like alongside a multi-level import
    statement, may result in loading states that break module invariants.

        slow_module = lazy_import("slow_module")

        # Safe uses of a lazy module
        slow_module.func()
        slow_module.FIELD
        from slow_module import sub_module

        # Unsafe uses of a lazy module
        import slow_module.sub_module

    lazy_import raises a ValueError if it detects an unsafe usage.
    """
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.find_spec(name)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError(f"module {name} not found")
    loader = _LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

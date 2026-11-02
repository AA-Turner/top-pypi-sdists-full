from ..init_imports import importlib,sys
# ============================================================
# Lazy-import machinery (std-lib only, self-contained)
# ============================================================
class _MissingModule:
    """Placeholder for a heavy dependency that isn't installed.

    Importing abstract_utilities no longer fails just because an optional
    third-party package is absent; instead the error is deferred until the
    feature that needs it is actually used.
    """

    __slots__ = ("_name",)

    def __init__(self, name):
        object.__setattr__(self, "_name", name)

    def _raise(self):
        raise ModuleNotFoundError(
            f"Optional dependency '{self._name}' is required for this feature "
            f"but is not installed. Install it to use this functionality."
        )

    def __getattr__(self, attr):
        self._raise()

    def __call__(self, *args, **kwargs):
        self._raise()

    def __bool__(self):
        return False

    def __repr__(self):
        return f"<MissingModule {self._name!r}>"


def _lazy_module(name):
    """Return ``name`` as a genuine module whose execution is deferred.

    Uses :class:`importlib.util.LazyLoader`, so the returned object *is* a real
    module object: attribute access (e.g. ``pd.DataFrame``) transparently
    triggers the actual import the first time it happens, and works correctly
    with ``isinstance``/``issubclass`` checks. Already-imported modules are
    returned as-is, and a missing dependency yields a :class:`_MissingModule`.
    """
    existing = sys.modules.get(name)
    if existing is not None:
        return existing
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ModuleNotFoundError, ValueError):
        spec = None
    if spec is None or spec.loader is None:
        return _MissingModule(name)
    try:
        loader = importlib.util.LazyLoader(spec.loader)
        spec.loader = loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        loader.exec_module(module)
        return module
    except Exception:
        return _MissingModule(name)


class _LazyCallable:
    """Deferred proxy for a callable (function) living in a heavy module.

    Resolution is delayed until the callable is invoked or one of its
    attributes is accessed.
    """

    __slots__ = ("_module", "_attr", "_resolved")

    def __init__(self, module, attr):
        object.__setattr__(self, "_module", module)
        object.__setattr__(self, "_attr", attr)
        object.__setattr__(self, "_resolved", None)

    def _resolve(self):
        resolved = object.__getattribute__(self, "_resolved")
        if resolved is None:
            mod = importlib.import_module(object.__getattribute__(self, "_module"))
            resolved = getattr(mod, object.__getattribute__(self, "_attr"))
            object.__setattr__(self, "_resolved", resolved)
        return resolved

    def __call__(self, *args, **kwargs):
        return self._resolve()(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._resolve(), name)


class _LazyTypeMeta(type):
    """Metaclass that makes a placeholder behave like the real class on demand.

    This lets a deferred class be used in ``isinstance`` / ``issubclass``
    checks and be instantiated, all while delaying the underlying import until
    one of those operations actually happens.
    """

    def _resolve(cls):
        cache = cls.__dict__.get("_cache")
        if cache is None:
            mod = importlib.import_module(cls._module_name)
            cache = getattr(mod, cls._attr_name)
            cls._cache = cache
        return cache

    def __instancecheck__(cls, instance):
        return isinstance(instance, cls._resolve())

    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, cls._resolve())

    def __call__(cls, *args, **kwargs):
        return cls._resolve()(*args, **kwargs)


def _lazy_type(module, attr):
    """Return a deferred stand-in for a class (safe in ``isinstance`` checks)."""

    return _LazyTypeMeta(
        attr,
        (),
        {"_module_name": module, "_attr_name": attr, "_cache": None},
    )

from ...imports import *
nullProxy_logger = logging.getLogger("abstract.lazy_import")


class nullProxy:
    """
    Safe, chainable, callable placeholder for missing modules/attributes.
    """

    def __init__(self, name, path=(),fallback=None):
        self._name = name
        self._path = path
        self.fallback=fallback
    def __getattr__(self, attr):
        return nullProxy(self._name, self._path + (attr,))

    def __call__(self, *args, **kwargs):
        if self.fallback is not None:
            try:
                return self.fallback(*args, **kwargs)
            except Exception as e:
                logger.info(f"{e}")
        nullProxy_logger.warning(
            "[lazy_import] Call to missing module/attr: %s.%s args=%s kwargs=%s",
            self._name,
            ".".join(self._path),
            args,
            kwargs,
        )
        return None

    def __repr__(self):
        full = ".".join((self._name, *self._path))
        return f"<nullProxy {full}>"

    def __bool__(self):
        return False  # safe in conditionals

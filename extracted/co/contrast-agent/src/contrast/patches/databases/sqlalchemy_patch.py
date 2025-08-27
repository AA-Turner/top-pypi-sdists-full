# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.patches.databases import dbapi2
from contrast.utils import Namespace
from contrast.utils.patch_utils import (
    register_module_patcher,
    unregister_module_patcher,
)

from contrast_vendor import structlog as logging
from contrast_vendor.wrapt import FunctionWrapper


logger = logging.getLogger("contrast")


ENGINE_DEFAULT_MODULE = "sqlalchemy.engine.default"


class module(Namespace):
    # saved version of the original (unpatched) method
    # this value is None iff the method is currently unpatched
    unpatched_method = None


def dialect_init_wrapper(wrapped, instance, args, kwargs):
    """
    Wrapt decides to separate `instance` from `args`. Don't worry that `instance`
    isn't passed back in to `wrapped` at call-time! This is already handled internally
    by wrapt.

    See https://wrapt.readthedocs.io/en/latest/wrappers.html#function-wrappers.
    """
    if getattr(instance, "is_async", False):
        logger.debug(
            "WARNING: Detected async sqlalchemy dialect - will not instrument",
            instance=instance,
            args=args,
            kwargs=kwargs,
        )
    elif "dbapi" in kwargs:
        dbapi2.instrument_adapter(kwargs["dbapi"], "sqlalchemy")
    else:
        logger.debug(
            "WARNING: couldn't extract dbapi adapter from dialect",
            instance=instance,
            args=args,
            kwargs=kwargs,
        )

    return wrapped(*args, **kwargs)


def patch_sqlalchemy(sqlalchemy_engine_default):
    """
    SQLAlchemy performs some downright demonic introspection on the __init__ methods
    for DefaultDialect and subclasses (see sqlalchemy.util.langhelpers.get_cls_kwargs).
    The only way we can get around this is to use wrapt's magic to create a very well-
    behaved patch for this method. If we tried to use build_and_apply_patch here, or
    even if we created a naive wrapper for this method, SQLAlchemy's introspection
    would lead to failures internal to the library.

    Hopefully one day this will be our one true patching strategy, as it's
    shockingly robust - it successfully imitates the original method even against
    tactics as powerful as argument introspection.

    Additionally, the patch_manager is not equipped to handle this case. This is
    likely due to the fact that the wrapped method is an instance of a callable class,
    not actually a function. If we want to make use of wrapt wrappers in the future,
    we will need to update the patch_manager accordingly. We also can't check for
    __wrapped__, because DefaultDialect is already wrapped by SQLAlchemy!
    """
    if module.unpatched_method is not None:
        return

    orig_method = sqlalchemy_engine_default.DefaultDialect.__init__
    module.unpatched_method = orig_method
    wrapped_method = FunctionWrapper(orig_method, dialect_init_wrapper)

    sqlalchemy_engine_default.DefaultDialect.__init__ = wrapped_method


def register_patches():
    register_module_patcher(patch_sqlalchemy, ENGINE_DEFAULT_MODULE)


def reverse_patches():
    """
    Note: this doesn't reverse-patch any dbapi2 adapters that were patched as a
    result of this module's patch.
    """
    unregister_module_patcher(ENGINE_DEFAULT_MODULE)
    sqlalchemy_engine_default = sys.modules.get(ENGINE_DEFAULT_MODULE)
    if None in (sqlalchemy_engine_default, module.unpatched_method):
        return

    sqlalchemy_engine_default.DefaultDialect.__init__ = module.unpatched_method
    module.unpatched_method = None

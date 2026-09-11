"""Unit tests for the package's public surface and its lazy re-exports.

`routed` is the only module here that imports pyspark's Spark Connect client at
module scope, so the package resolves the routed names through a module-level
``__getattr__`` instead of importing them eagerly. That keeps a consumer who only
touches the errors or the registry from paying for a Connect import -- and, in
the version set where grpcio has no build for this interpreter, from failing to
import the package at all.

That indirection is worth its own tests: a typo in the name set would turn a
public function into an ``AttributeError`` at kernel start, and a missing guard
would turn an ordinary typo into a confusing ImportError from deep inside pyspark.
"""

import importlib.util

import pytest

from sagemaker_studio.utils import udf as udf_pkg


def test_the_eager_names_need_no_pyspark():
    """Errors and registry come from modules with no pyspark import at all."""
    assert udf_pkg.UDFRegistrationError is not None
    assert callable(udf_pkg.register_sidecar)
    assert callable(udf_pkg.client_python_version)


def test_an_unknown_attribute_raises_attribute_error_naming_the_module():
    with pytest.raises(AttributeError) as excinfo:
        udf_pkg.no_such_name
    message = str(excinfo.value)
    assert "no_such_name" in message
    assert "sagemaker_studio.utils.udf" in message


def test_every_advertised_name_is_actually_reachable():
    """`__all__` is a promise; an entry that does not resolve is a broken import.

    Covers both halves at once: the eagerly imported names and the ones the
    lazy ``__getattr__`` resolves.
    """
    if importlib.util.find_spec("grpc") is None:
        pytest.skip("the routed names need pyspark Spark Connect, which needs grpcio")
    missing = [name for name in udf_pkg.__all__ if not hasattr(udf_pkg, name)]
    assert missing == []


def test_the_lazy_names_are_exactly_the_ones_routed_owns():
    """Guards against a name drifting out of the lazy set and back to eager.

    If a routed name were dropped from `_ROUTED_NAMES` it would still resolve --
    via the module import that something else triggered -- so this asserts the
    set itself, not just reachability.
    """
    assert udf_pkg._ROUTED_NAMES == {
        "SidecarPythonUDF",
        "SidecarUserDefinedFunction",
        "install_udf_interceptor",
        "install_udf_register_routing",
        "pandas_udf",
        "udf",
        "uninstall_udf_register_routing",
    }
    # and every one of them is advertised
    assert udf_pkg._ROUTED_NAMES <= set(udf_pkg.__all__)

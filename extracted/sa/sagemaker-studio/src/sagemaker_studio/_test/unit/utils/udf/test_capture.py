"""Unit tests for UDF source/freevar capture and registration-time validation."""

import base64
import importlib.util
import json
import json as json_alias  # aliased on purpose: exercises `import X as Y` synthesis
import pickle
import threading
import types
import xml.etree.ElementTree as etree  # noqa: N813 - dotted on purpose: tests `import a.b.c as Y`

import __main__ as main_module  # the `__main__` module itself; see its test below
import pytest

from sagemaker_studio.utils.udf.capture import (
    FUTURE_PREAMBLE,
    build_request,
    capture,
    validate_freevar,
)
from sagemaker_studio.utils.udf.errors import UDFRegistrationError


def test_captures_a_plain_function_body_without_decorators():
    def add_one(x):
        return x + 1

    captured = capture(add_one)
    assert captured.name == "add_one"
    assert "def add_one(x):" in captured.source
    assert captured.source.startswith(FUTURE_PREAMBLE)
    assert captured.freevars == {}


def test_strips_decorator_lines_so_the_source_execs_cleanly():
    src = "@some_decorator\n@another\ndef f(x):\n    return x\n"
    captured = capture(
        _compile_named(
            src, "f", globals_={"some_decorator": lambda fn: fn, "another": lambda fn: fn}
        )
    )
    assert "@some_decorator" not in captured.source
    assert captured.source.rstrip().endswith("return x")


def test_strips_a_multiline_decorator_call():
    def with_return_type(**kwargs):
        def wrap(fn):
            return fn

        return wrap

    @with_return_type(
        returnType="string",
    )
    def f(x):
        return x

    captured = capture(f)
    assert "with_return_type" not in captured.source
    assert "returnType" not in captured.source
    assert captured.source.rstrip().endswith("return x")
    namespace = {}
    exec(compile(captured.source, "<udf>", "exec"), namespace)
    assert namespace["f"](5) == 5


def test_undecorated_function_source_survives_verbatim_including_comments():
    # ast.unparse drops comments and reformats; that's only an acceptable
    # trade when there's a decorator to actually remove. An undecorated
    # function must round-trip untouched, or sidecar tracebacks point at code
    # the user never wrote.
    def add_one(x):
        # keep this comment
        return x + 1

    captured = capture(add_one)
    body = captured.source[len(FUTURE_PREAMBLE) :]
    assert "# keep this comment" in body


def test_dedents_a_nested_function():
    def outer():
        def inner(x):
            return x * 2

        return inner

    captured = capture(outer())
    body = captured.source[len(FUTURE_PREAMBLE) :]
    assert body.startswith("def inner(x):")


def test_captures_data_freevars_by_value():
    factor = 7

    def scale(x):
        return x * factor

    captured = capture(scale)
    assert captured.freevars == {"factor": 7}


def test_lambda_is_captured_as_a_named_assignment():
    my_udf = lambda x: x + 1  # noqa: E731 - exercising the lambda path on purpose
    captured = capture(my_udf, name="my_lambda_udf")
    body = captured.source[len(FUTURE_PREAMBLE) :]
    assert body.strip() == "my_lambda_udf = lambda x: x + 1"
    assert captured.name == "my_lambda_udf"
    # Prove the emitted source is exec-able, not just string-equal: it must
    # define the requested name and compute the right value.
    namespace = {}
    exec(compile(captured.source, "<udf>", "exec"), namespace)
    assert namespace["my_lambda_udf"](4) == 5


def test_lambda_refuses_rather_than_guess_when_two_share_one_line():
    # Both lambdas share one physical source line, so line number alone can't
    # tell them apart, and there is no reliable column-based way to pick the
    # *target* function's lambda over the other one -- a silently wrong
    # capture is the one outcome this module must never produce, so it must
    # raise here rather than pick a (possibly wrong) side. This targets the
    # non-leftmost lambda deliberately, to prove this isn't just "leftmost
    # always wins" in disguise.
    noop, my_udf = (lambda x: x), (lambda x: x + 1)  # noqa: E731
    del noop

    with pytest.raises(UDFRegistrationError) as excinfo:
        capture(my_udf, name="my_lambda_udf")
    assert "named `def`" in str(excinfo.value)


def test_lambda_refuses_when_source_fragment_is_not_standalone():
    # Each dict entry sits on its own physical line, so inspect.getsourcelines
    # isolates just that one line (e.g. '"a": lambda x: x + 1,') -- which is
    # not valid standalone Python and fails to parse. This must refuse, not
    # silently capture nothing or the wrong thing.
    handlers = {
        "a": lambda x: x + 1,
    }

    with pytest.raises(UDFRegistrationError):
        capture(handlers["a"], name="h")


def test_lambda_disambiguates_two_lambda_arguments_on_separate_lines():
    # Two lambdas in one statement, one per physical line -- the realistic
    # "two lambda arguments to one call" shape from the bug report.
    other, my_udf = (
        lambda x: x + 100,
        lambda x: x + 1,
    )  # noqa: E731
    del other

    captured = capture(my_udf, name="my_lambda_udf")
    body = captured.source[len(FUTURE_PREAMBLE) :]
    assert body.strip() == "my_lambda_udf = lambda x: x + 1"


def test_future_preamble_keeps_annotations_unevaluated():
    # A pandas_udf body annotated with pd.Series must not need pandas in the
    # sidecar; the future import turns annotations into strings.
    import types as _types

    src = "def f(s: pd.Series) -> pd.Series:\n    return s + 1\n"
    captured = capture(
        _compile_named(src, "f", globals_={"pd": _types.SimpleNamespace(Series=object)})
    )
    namespace = {}
    exec(compile(captured.source, "<udf>", "exec"), namespace)  # no `pd` defined
    assert callable(namespace["f"])


def test_imports_are_carried_through():
    def slugify(s):
        return s

    captured = capture(slugify, imports=["import re", "import json"])
    assert captured.imports == ["import re", "import json"]


# -- validation ---------------------------------------------------------- #

# The tests below need REAL Spark Connect objects, and Connect needs grpcio,
# which Brazil does not build for every interpreter this package is tested
# against. Only they are skipped; the rest of the module still runs.
HAVE_CONNECT = importlib.util.find_spec("grpc") is not None
requires_connect = pytest.mark.skipif(not HAVE_CONNECT, reason="pyspark Spark Connect needs grpcio")


def _live_spark_session():
    """A REAL pyspark session object, uninitialised.

    Deliberately not a look-alike class defined here. The rule is qualified by
    module as well as type name, because matching the bare name refused ordinary
    picklable data -- a pandas DataFrame is also called "DataFrame". A stand-in
    named `SparkSession` would therefore assert the bug rather than the rule.
    `__new__` avoids building a real connection.
    """
    from pyspark.sql.connect.session import SparkSession

    return SparkSession.__new__(SparkSession)


def _live_connect_client():
    from pyspark.sql.connect.client.core import SparkConnectClient

    return SparkConnectClient.__new__(SparkConnectClient)


@requires_connect
def test_rejects_a_captured_live_session():
    with pytest.raises(UDFRegistrationError) as excinfo:
        validate_freevar("spark", _live_spark_session())
    message = str(excinfo.value)
    assert "live" in message
    assert "'spark'" in message  # names the offending variable


@requires_connect
def test_rejects_a_captured_connect_client():
    with pytest.raises(UDFRegistrationError) as excinfo:
        validate_freevar("client", _live_connect_client())
    assert "'client'" in str(excinfo.value)  # names the offending variable


def test_rejects_a_nested_closure():
    def make(n):
        def inner(x):
            return x + n

        return inner

    with pytest.raises(UDFRegistrationError) as excinfo:
        validate_freevar("helper", make(3))
    message = str(excinfo.value)
    assert "nested closure" in message
    assert "'helper'" in message  # names the offending variable


def test_accepts_a_plain_module_level_function_as_a_freevar():
    validate_freevar("helper", validate_freevar)  # no closure, picklable by reference


def test_rejects_a_non_picklable_value():
    import threading

    with pytest.raises(UDFRegistrationError) as excinfo:
        validate_freevar("lock", threading.Lock())
    assert "picklable" in str(excinfo.value)


@requires_connect
def test_capture_validates_every_freevar():
    session = _live_spark_session()

    def bad(x):
        return session

    with pytest.raises(UDFRegistrationError):
        capture(bad)


# -- request ------------------------------------------------------------- #


def test_build_request_pickles_freevars_and_carries_the_schema():
    def scale(x):
        return x

    captured = capture(scale, imports=["import re"])
    captured = type(captured)(
        name=captured.name, source=captured.source, freevars={"factor": 3}, imports=captured.imports
    )
    request = build_request(captured, return_type_json='{"type":"long"}', eval_type=100)

    assert request["name"] == "scale"
    assert request["eval_type"] == 100
    assert request["return_type_json"] == '{"type":"long"}'
    assert request["imports"] == ["import re"]
    assert pickle.loads(base64.b64decode(request["freevars_pickle_b64"])) == {"factor": 3}
    assert request["protocol"] == 1


def _compile_named(src, name, globals_=None):
    namespace = {} if globals_ is None else dict(globals_)
    # Give inspect.getsource something to find by writing the source into
    # linecache under a synthetic filename.
    import linecache

    filename = f"<test-{name}>"
    linecache.cache[filename] = (len(src), None, src.splitlines(True), filename)
    exec(compile(src, filename, "exec"), namespace)
    return namespace[name]


# -- module / notebook globals -------------------------------------------- #
#
# `inspect.getclosurevars` reports enclosing-scope names in `.nonlocals` and
# module-level names in `.globals`. In a notebook, "module level" is "defined in
# an earlier cell" -- so these module-level values model exactly that shape.

NB_THRESHOLD = 5
MODULE_LEVEL_SESSION = _live_spark_session() if HAVE_CONNECT else None
unpicklable_global = threading.Lock()


def test_a_module_level_constant_is_captured_as_a_freevar():
    # THE ordinary notebook shape: a UDF referring to a constant from an earlier
    # cell. Dropping `.globals` made this raise NameError on the worker, while
    # the identical notebook works on Glue 5.
    def over_threshold(x):
        return x > NB_THRESHOLD

    assert capture(over_threshold).freevars == {"NB_THRESHOLD": 5}


def test_the_notebook_constant_shape_survives_capture_exec_and_cloudpickle():
    """End-to-end over the exact `NB_THRESHOLD` shape, the way the sidecar does it.

    capture -> build_request -> unpickle freevars -> replay imports -> exec the
    source -> cloudpickle the rebuilt function. With `.globals` dropped, the
    exec'd function raised NameError the moment it ran.
    """
    pytest.importorskip("pyspark", reason="cloudpickle round trip needs pyspark")
    from pyspark.serializers import CloudPickleSerializer

    def over_threshold(x):
        return x > NB_THRESHOLD

    request = build_request(
        capture(over_threshold), return_type_json='{"type":"boolean"}', eval_type=100
    )

    namespace = {}
    for statement in request["imports"]:
        exec(statement, namespace)
    namespace.update(pickle.loads(base64.b64decode(request["freevars_pickle_b64"])))
    exec(request["source"], namespace)
    rebuilt = namespace["over_threshold"]
    assert rebuilt(6) is True
    assert rebuilt(4) is False

    # The sidecar's final step: the rebuilt function must be cloudpicklable and
    # must still see its captured global after the round trip.
    serializer = CloudPickleSerializer()
    round_tripped = serializer.loads(serializer.dumps(rebuilt))
    assert round_tripped(6) is True
    assert round_tripped(4) is False


def test_a_referenced_module_becomes_a_synthesised_import_not_a_pickled_module():
    def dump(x):
        return json_alias.dumps(x)

    captured = capture(dump)
    # A module cannot be pickled, so it must not appear as a freevar at all.
    assert "json_alias" not in captured.freevars
    assert captured.imports == ["import json as json_alias"]

    namespace = {}
    for statement in captured.imports:
        exec(statement, namespace)
    exec(captured.source, namespace)
    assert namespace["dump"]({"a": 1}) == '{"a": 1}'


def test_a_module_referenced_under_its_own_name_needs_no_alias():
    def dump(x):
        return json.dumps(x)

    assert capture(dump).imports == ["import json"]


def test_a_submodule_reference_synthesises_a_dotted_import():
    # The statement is built from the module's own `__name__`, which is what is
    # actually importable -- not the dotted path the caller happened to type.
    # (`os.path`, for instance, has `__name__ == "posixpath"`.)
    def parse(x):
        return etree.fromstring(x)

    assert capture(parse).imports == ["import xml.etree.ElementTree as etree"]


def test_a_caller_supplied_import_is_not_shadowed_by_a_synthesised_one():
    def dump(x):
        return json_alias.dumps(x)

    # The caller's own statement binds `json_alias`, so no second, conflicting
    # statement may be appended after it.
    captured = capture(dump, imports=["import ujson as json_alias"])
    assert captured.imports == ["import ujson as json_alias"]


def test_referencing_main_itself_is_refused_by_name():
    def leaky(x):
        return main_module.anything

    with pytest.raises(UDFRegistrationError) as excinfo:
        capture(leaky)
    message = str(excinfo.value)
    assert "'main_module'" in message
    assert "__main__" in message


@requires_connect
def test_an_unshippable_global_is_refused_at_definition_time_by_name():
    def leaky(x):
        return str(MODULE_LEVEL_SESSION)

    with pytest.raises(UDFRegistrationError) as excinfo:
        capture(leaky)
    message = str(excinfo.value)
    assert "'MODULE_LEVEL_SESSION'" in message
    assert "live" in message


def test_a_notebook_defined_helper_is_refused_rather_than_failing_in_the_sidecar():
    """A `__main__`-defined function pickles BY REFERENCE, and the sidecar's own
    `__main__` is the sidecar server -- so it must be refused HERE, not fail at
    build time inside the sidecar's `pickle.loads`."""
    helper = types.FunctionType((lambda x: x).__code__, {"__name__": "__main__"}, "helper")
    helper.__module__ = "__main__"
    # It pickles fine locally, which is exactly why the check has to be explicit.
    assert pickle.dumps(validate_freevar, protocol=5)

    with pytest.raises(UDFRegistrationError) as excinfo:
        validate_freevar("helper", helper)
    message = str(excinfo.value)
    assert "'helper'" in message
    assert "__main__" in message


class NotebookCfg:
    """A class "defined in a notebook cell": `__module__` is forced to `__main__`
    below, and the class itself is injected into the real `__main__` by the test
    that uses it -- so an instance pickles LOCALLY, by reference to
    `__main__.NotebookCfg`, exactly as it would from a notebook."""

    def __init__(self, n):
        self.n = n


NotebookCfg.__module__ = "__main__"
NB_CFG = NotebookCfg(7)


def test_an_instance_of_a_notebook_defined_class_is_refused_at_definition_time(monkeypatch):
    """A config object built in an earlier cell: the VALUE is ordinary data, but its
    CLASS is `__main__`-defined, so it pickles by reference to `__main__.Cfg` and
    the sidecar's `pickle.loads` raises `AttributeError: Can't get attribute`.
    One level of indirection out from the `__main__` function/class check, and just
    as ordinary a notebook shape -- so it must be refused HERE too.
    """
    monkeypatch.setattr(main_module, "NotebookCfg", NotebookCfg, raising=False)

    def f(x):
        return x + NB_CFG.n

    # It pickles fine locally, which is exactly why the check has to be explicit:
    # `pickle.dumps` below would never have caught this.
    payload = pickle.dumps(NB_CFG, protocol=5)

    with pytest.raises(UDFRegistrationError) as excinfo:
        capture(f)  # definition time: no sidecar, no worker, nothing sent
    message = str(excinfo.value)
    assert "'NB_CFG'" in message  # the symbol...
    assert "'NotebookCfg'" in message  # ...and the class that cannot be resolved
    assert "__main__" in message

    # And the late failure that refusal prevents: a `__main__` without the class --
    # which is what the sidecar's `__main__` is -- cannot load the same payload.
    monkeypatch.delattr(main_module, "NotebookCfg")
    with pytest.raises(AttributeError):
        pickle.loads(payload)


def nb_fact(n):
    """A self-recursive UDF as a notebook cell defines it: a module-level `def`
    whose `__module__` is `__main__`."""
    return 1 if n <= 1 else n * nb_fact(n - 1)


nb_fact.__module__ = "__main__"


def test_a_self_recursive_udf_captures_nothing_and_still_recurses():
    """`exec`ing the captured source BINDS `nb_fact` in the sidecar's fresh
    namespace before the function is ever called, and a body resolves its globals
    at CALL time -- so the self-reference needs no capture at all. Capturing it
    instead refused an ordinary recursive UDF, with a message about inlining the
    helper's body that is meaningless for self-reference.
    """
    pytest.importorskip("pyspark", reason="cloudpickle round trip needs pyspark")
    from pyspark.serializers import CloudPickleSerializer

    captured = capture(nb_fact)
    assert captured.freevars == {}

    # Recursion through the exec'd binding is the part worth proving.
    namespace = {}
    exec(captured.source, namespace)
    assert namespace["nb_fact"](5) == 120

    serializer = CloudPickleSerializer()
    round_tripped = serializer.loads(serializer.dumps(namespace["nb_fact"]))
    assert round_tripped(5) == 120


def test_a_notebook_helper_that_is_not_the_udf_itself_is_still_refused():
    """The self-reference skip is exactly the function's own name, nothing wider:
    a DIFFERENT `__main__` function referenced from the body is still refused."""

    def calls_nb_fact(x):
        return nb_fact(x)

    with pytest.raises(UDFRegistrationError) as excinfo:
        capture(calls_nb_fact)
    assert "'nb_fact'" in str(excinfo.value)


def test_an_attribute_name_colliding_with_a_module_global_is_not_captured():
    """`getclosurevars` resolves `co_names`, which holds ATTRIBUTE names too.

    `x.unpicklable_global()` puts `unpicklable_global` in `co_names`, so it is
    looked up in the module globals and would be refused as unpicklable -- even
    though the UDF never references it as a bare name. Only bare-name loads may
    count, or ordinary UDFs get rejected for nothing.
    """

    def call_method(x):
        return x.unpicklable_global()

    assert capture(call_method).freevars == {}


# -- live-value rejection is module-qualified ------------------------------- #


def test_a_pandas_dataframe_is_shippable_despite_the_name_collision():
    """`type(v).__name__ == "DataFrame"` is true for pandas too.

    Closing over a small lookup table is an ordinary notebook pattern. An
    unqualified name match refused it at definition time claiming it "holds a
    live DataFrame", which was both wrong and misleading.
    """
    import pandas as pd

    validate_freevar("LOOKUP", pd.DataFrame({"a": [1, 2]}))


@requires_connect
def test_a_live_connect_dataframe_is_still_refused():
    from pyspark.sql.connect.dataframe import DataFrame

    with pytest.raises(UDFRegistrationError) as excinfo:
        validate_freevar("DF", DataFrame.__new__(DataFrame))
    assert "live DataFrame" in str(excinfo.value)


def test_a_module_whose_name_merely_starts_with_a_live_prefix_is_shippable():
    """ "socketserver" is not "socket"; the prefix match is boundary-aware."""
    import socketserver

    validate_freevar("SRV", socketserver.TCPServer.__new__(socketserver.TCPServer))


def test_a_real_socket_is_still_refused():
    import socket

    with pytest.raises(UDFRegistrationError):
        validate_freevar("SOCK", socket.socket())


# -- unparsable source and unshippable modules ---------------------------- #
#
# Every AST helper here parses text it did not produce, so each one has to answer
# "I could not tell" without raising. The distinction between `None` and an empty
# set is load-bearing -- see `_loaded_names`' docstring -- so these assert the
# exact sentinel, not merely falsiness.


def test_a_callable_with_no_readable_source_is_refused_by_name():
    """A builtin has no source, so the routed path can never ship it."""
    with pytest.raises(UDFRegistrationError) as excinfo:
        capture(len)
    message = str(excinfo.value)
    assert "could not read this function's source" in message
    assert "notebook cell" in message  # tells the user what to do instead


def test_unparsable_import_statements_are_skipped_not_fatal():
    from sagemaker_studio.utils.udf.capture import _imported_names

    assert _imported_names(["import json", "this is not python ("]) == {"json"}


def test_loaded_names_returns_none_when_the_source_cannot_be_parsed():
    """`None` means "could not tell", which makes the caller ship everything.

    An empty set would mean "nothing is referenced" and would silently DROP real
    captures, so this must not collapse to `set()`.
    """
    from sagemaker_studio.utils.udf.capture import _loaded_names

    assert _loaded_names("def broken(:") is None


def test_self_bound_names_is_empty_when_the_source_cannot_be_parsed():
    from sagemaker_studio.utils.udf.capture import _self_bound_names

    assert _self_bound_names("def broken(:") == set()


def test_lambda_capture_gives_up_when_no_lambda_sits_on_the_target_line():
    from sagemaker_studio.utils.udf.capture import _lambda_source

    assert _lambda_source("x = lambda v: v\n", "my_udf", target_lineno=99) is None


def test_lambda_capture_gives_up_on_unparsable_source():
    from sagemaker_studio.utils.udf.capture import _lambda_source

    assert _lambda_source("lambda (:", "my_udf", None) is None


def test_a_module_without_a_name_cannot_be_shipped_and_says_so():
    """Modules travel as replayed imports, so a nameless one has no representation."""
    from sagemaker_studio.utils.udf.capture import _module_import_statement

    class _Nameless:
        __name__ = ""

    with pytest.raises(UDFRegistrationError) as excinfo:
        _module_import_statement("mod", _Nameless())
    assert "'mod'" in str(excinfo.value)  # names the offending variable

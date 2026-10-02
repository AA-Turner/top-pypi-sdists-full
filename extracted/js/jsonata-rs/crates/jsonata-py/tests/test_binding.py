"""pytest suite for the `jsonata` (jsonata-rs) Python bindings."""
import jsonata
import pytest


def test_literal_arithmetic():
    assert jsonata.Jsonata("1+2*3").evaluate(None) == 7


def test_path():
    assert jsonata.Jsonata("foo.bar").evaluate({"foo": {"bar": 42}}) == 42


def test_array_index():
    assert jsonata.Jsonata("a[1]").evaluate({"a": [10, 20, 30]}) == 20


def test_string_concat():
    assert jsonata.Jsonata('a & "!"').evaluate({"a": "hi"}) == "hi!"


def test_number_division():
    assert jsonata.Jsonata("$ / 2").evaluate(2) == 1
    assert jsonata.Jsonata("$ / 2").evaluate(1) == 0.5


def test_map_hof():
    assert jsonata.Jsonata("$map([1,2,3], function($v){$v*$v})").evaluate(None) == [1, 4, 9]


def test_sum():
    data = {"items": [{"price": 1.5}, {"price": 2.5}]}
    assert jsonata.Jsonata("$sum(items.price)").evaluate(data) == 4


def test_object_construct():
    assert jsonata.Jsonata('{"n": $count(a)}').evaluate({"a": [1, 2, 3]}) == {"n": 3}


def test_sort():
    assert jsonata.Jsonata("$sort([3,1,2])").evaluate(None) == [1, 2, 3]


def test_null_preserved():
    assert jsonata.Jsonata("a").evaluate({"a": None}) is None


def test_string_function():
    assert jsonata.Jsonata("$uppercase($)").evaluate("hello") == "HELLO"


def test_bindings():
    assert jsonata.Jsonata("$x + 1").evaluate(None, {"x": 41}) == 42


def test_module_evaluate():
    assert jsonata.evaluate("$.a + $.b", {"a": 2, "b": 3}) == 5


def test_custom_function():
    expr = jsonata.Jsonata("$greet(name)")
    expr.register_function("greet", lambda n: "Hello, " + n + "!")
    assert expr.evaluate({"name": "World"}) == "Hello, World!"


def test_custom_function_two_args():
    expr = jsonata.Jsonata("$add(2, 3)")
    expr.register_function("add", lambda a, b: a + b)
    assert expr.evaluate(None) == 5


def test_syntax_error():
    with pytest.raises(jsonata.JsonataError) as exc:
        jsonata.Jsonata("1 +")
    assert exc.value.code == "S0207"


def test_runtime_error():
    with pytest.raises(jsonata.JsonataError) as exc:
        jsonata.Jsonata("$error('boom')").evaluate(None)
    assert exc.value.code == "D3137"


def test_version():
    assert isinstance(jsonata.__version__, str)


# The following tests guard the runtime contract promised by the type stub
# (crates/jsonata-py/jsonata.pyi). If an attribute here changes, the stub must
# change too — keep them in lockstep.

def test_error_attributes_match_stub():
    with pytest.raises(jsonata.JsonataError) as exc:
        jsonata.Jsonata("1 +")
    err = exc.value
    assert isinstance(err.code, str)      # stub: code: str
    assert isinstance(err.position, int)  # stub: position: int


def test_internal_error_subclasses_jsonata_error():
    # `except JsonataError` must keep catching engine panics.
    assert issubclass(jsonata.JsonataInternalError, jsonata.JsonataError)


def test_public_api_is_exported():
    for name in (
        "Jsonata",
        "evaluate",
        "JsonataError",
        "JsonataInternalError",
        "UndefinedType",
        "UNDEFINED",
        "__version__",
    ):
        assert hasattr(jsonata, name), name


def test_package_ships_py_typed():
    # PEP 561 marker must be present so type checkers honor the stub.
    import importlib.util
    import pathlib

    spec = importlib.util.find_spec("jsonata")
    assert spec is not None and spec.submodule_search_locations, (
        "jsonata should install as a package (maturin wraps the compiled module "
        "when a stub is present)"
    )
    pkg_dir = pathlib.Path(next(iter(spec.submodule_search_locations)))
    assert (pkg_dir / "py.typed").is_file()
    assert (pkg_dir / "__init__.pyi").is_file()

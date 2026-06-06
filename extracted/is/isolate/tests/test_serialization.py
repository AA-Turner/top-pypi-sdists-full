import importlib
import sys
import traceback
from functools import partial

import pytest
from isolate.connections.common import (
    ExceptionDeserializationError,
    SerializationError,
    load_serialized_object,
    serialize_object,
)


@pytest.mark.parametrize(
    "method",
    [
        "pickle",
        "dill",
        "cloudpickle",
    ],
)
def test_serialize_object(method):
    func = partial(eval, "2 + 2")
    serialized = serialize_object(method, func)
    deserialized = load_serialized_object(method, serialized)
    assert deserialized() == 4


def test_deserialize_exception():
    serialized = serialize_object("pickle", ValueError("some error"))
    regular_obj = load_serialized_object("pickle", serialized)
    assert isinstance(regular_obj, ValueError)
    assert regular_obj.args == ("some error",)


def test_deserialize_raised_exception():
    serialized = serialize_object("pickle", ValueError("some error"))
    with pytest.raises(ValueError) as exc_info:
        load_serialized_object("pickle", serialized, was_it_raised=True)
    assert exc_info.value.args == ("some error",)


def test_deserialize_raised_exception_with_unimportable_type_preserves_traceback(
    tmp_path,
    monkeypatch,
):
    module_name = "remote_only_exc_for_isolate_test"
    module_path = tmp_path / f"{module_name}.py"
    module_path.write_text("class RemoteOnlyError(Exception):\n    pass\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    remote_module = importlib.import_module(module_name)

    try:
        raise remote_module.RemoteOnlyError("remote boom")
    except remote_module.RemoteOnlyError as exc:
        serialized = serialize_object("pickle", exc)
        stringized_traceback = traceback.format_exc()

    sys.modules.pop(module_name, None)
    sys.path.remove(str(tmp_path))

    with pytest.raises(ExceptionDeserializationError) as exc_info:
        load_serialized_object(
            "pickle",
            serialized,
            was_it_raised=True,
            stringized_traceback=stringized_traceback,
        )

    assert exc_info.value.message == "Error while deserializing the given object"
    assert exc_info.value.original_traceback is not None
    assert exc_info.value.original_stringized_traceback == stringized_traceback
    assert isinstance(exc_info.value.__cause__, ModuleNotFoundError)


def error_while_serializing():
    anon = lambda: 2 + 2  # anonymous functions are not  # noqa: E731
    # serializable by pickle
    with pytest.raises(SerializationError) as exc_info:
        serialize_object("pickle", anon)

    assert exc_info.match("Error while serializing the given object")

    dill_serialized_lambda = serialize_object("dill", anon)

    with pytest.raises(SerializationError) as exc_info:
        load_serialized_object("pickle", dill_serialized_lambda)

    assert exc_info.match("Error while deserializing the given object")


def error_while_loading_backend():
    with pytest.raises(SerializationError) as exc_info:
        serialize_object("$$$", 1)

    assert exc_info.match("Error while preparing the serialization backend")

    with pytest.raises(SerializationError) as exc_info:
        load_serialized_object("$$$", b"1")

    assert exc_info.match("Error while preparing the serialization backend")

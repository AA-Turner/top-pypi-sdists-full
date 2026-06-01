from enum import Enum
from typing import Any, Optional, Union

import pytest
from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core.temporal.context_handler_interceptor import _validate_activity_args


class SimpleModel(BaseModel):
    name: str
    value: int


class NestedInner(BaseModel):
    x: int
    y: int


class NestedModel(BaseModel):
    label: str
    inner: NestedInner


class ModelWithDefaults(BaseModel):
    name: str
    score: float = 0.0


class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class ModelWithOptionalField(BaseModel):
    name: str
    tag: Optional[str] = None


def fn_no_params() -> None:
    pass


def fn_no_hints(a, b):  # noqa: ANN001, ANN201
    pass


def fn_all_any(a: Any, b: Any) -> None:
    pass


def fn_simple(name: str, value: int) -> None:
    pass


def fn_single_model(model: SimpleModel) -> None:
    pass


def fn_nested_model(data: NestedModel) -> None:
    pass


def fn_model_with_defaults(data: ModelWithDefaults) -> None:
    pass


def fn_optional_str(name: str, tag: Optional[str] = None) -> None:
    pass


def fn_union(value: Union[int, str]) -> None:
    pass


def fn_pipe_union(value: int | str) -> None:
    pass


def fn_list_of_int(items: list[int]) -> None:
    pass


def fn_dict_str_int(mapping: dict[str, int]) -> None:
    pass


def fn_enum_param(color: Color) -> None:
    pass


def fn_with_default(name: str, count: int = 10) -> None:
    pass


def fn_mixed(name: str, model: SimpleModel, flag: bool) -> None:
    pass


def fn_multiple_models(a: SimpleModel, b: NestedModel) -> None:
    pass


def fn_optional_model(name: str, model: Optional[SimpleModel] = None) -> None:
    pass


def fn_list_of_models(items: list[SimpleModel]) -> None:
    pass


def fn_bool(flag: bool) -> None:
    pass


def fn_model_with_opt_field(m: ModelWithOptionalField) -> None:
    pass


def fn_complex(
    name: str,
    model: SimpleModel,
    tags: list[str],
    metadata: dict[str, Any],
    count: int = 5,
) -> None:
    pass


class _Svc:
    def process(self, data: SimpleModel) -> None:
        pass


_svc_process = _Svc().process


def fn_bad_forward_ref(x: "NonExistentType") -> None:  # noqa: F821
    pass


@pytest.mark.parametrize(
    "fn, args, expected",
    [
        pytest.param(fn_no_params, [], [], id="no_params_no_args"),
        pytest.param(fn_simple, ["hello", 42], ["hello", 42], id="simple_matching_types"),
        pytest.param(
            fn_single_model,
            [{"name": "test", "value": 42}],
            [SimpleModel(name="test", value=42)],
            id="dict_to_simple_model",
        ),
        pytest.param(
            fn_nested_model,
            [{"label": "point", "inner": {"x": 1, "y": 2}}],
            [NestedModel(label="point", inner=NestedInner(x=1, y=2))],
            id="dict_to_nested_model",
        ),
        pytest.param(
            fn_model_with_defaults,
            [{"name": "hi"}],
            [ModelWithDefaults(name="hi")],
            id="model_defaults_partial",
        ),
        pytest.param(
            fn_model_with_defaults,
            [{"name": "hi", "score": 9.5}],
            [ModelWithDefaults(name="hi", score=9.5)],
            id="model_defaults_full",
        ),
        pytest.param(
            fn_multiple_models,
            [{"name": "a", "value": 1}, {"label": "b", "inner": {"x": 0, "y": 0}}],
            [SimpleModel(name="a", value=1), NestedModel(label="b", inner=NestedInner(x=0, y=0))],
            id="multiple_models",
        ),
        pytest.param(
            fn_list_of_models,
            [[{"name": "a", "value": 1}, {"name": "b", "value": 2}]],
            [[SimpleModel(name="a", value=1), SimpleModel(name="b", value=2)]],
            id="list_of_models",
        ),
        pytest.param(
            fn_optional_model,
            ["hello", None],
            ["hello", None],
            id="optional_model_none",
        ),
        pytest.param(
            fn_optional_model,
            ["hello", {"name": "x", "value": 1}],
            ["hello", SimpleModel(name="x", value=1)],
            id="optional_model_dict",
        ),
        pytest.param(fn_no_hints, ["a", 2], ["a", 2], id="no_type_hints"),
        pytest.param(fn_all_any, ["hello", {"x": 1}], ["hello", {"x": 1}], id="any_type_hints"),
        pytest.param(fn_optional_str, ["hello", "world"], ["hello", "world"], id="optional_str_value"),
        pytest.param(fn_optional_str, ["hello", None], ["hello", None], id="optional_str_none"),
        pytest.param(fn_union, [42], [42], id="union_int"),
        pytest.param(fn_union, ["hello"], ["hello"], id="union_str"),
        pytest.param(fn_pipe_union, [42], [42], id="pipe_union"),
        pytest.param(fn_enum_param, ["red"], [Color.RED], id="enum_from_str"),
        pytest.param(fn_enum_param, [Color.GREEN], [Color.GREEN], id="enum_already_enum"),
        pytest.param(fn_list_of_int, [[1, 2, 3]], [[1, 2, 3]], id="list_of_int"),
        pytest.param(fn_dict_str_int, [{"a": 1, "b": 2}], [{"a": 1, "b": 2}], id="dict_str_int"),
        pytest.param(fn_with_default, ["hello"], ["hello"], id="fewer_args_than_params"),
        pytest.param(fn_simple, ["a", 1, "extra"], ["a", 1, "extra"], id="more_args_than_params"),
        pytest.param(
            fn_single_model,
            [{"name": "x", "value": 1}, "extra_arg"],
            [SimpleModel(name="x", value=1), "extra_arg"],
            id="more_args_with_model",
        ),
        pytest.param(fn_with_default, [], [], id="empty_args_with_defaults"),
        pytest.param(
            fn_complex,
            ["test_name", {"name": "m", "value": 10}, ["tag1", "tag2"], {"key": "val"}, 3],
            ["test_name", SimpleModel(name="m", value=10), ["tag1", "tag2"], {"key": "val"}, 3],
            id="complex_all_args",
        ),
        pytest.param(
            fn_complex,
            ["test_name", {"name": "m", "value": 10}, ["tag1"], {"k": 1}],
            ["test_name", SimpleModel(name="m", value=10), ["tag1"], {"k": 1}],
            id="complex_optional_omitted",
        ),
        pytest.param(
            fn_model_with_opt_field,
            [{"name": "test"}],
            [ModelWithOptionalField(name="test")],
            id="optional_field_missing",
        ),
        pytest.param(
            fn_model_with_opt_field,
            [{"name": "test", "tag": "v1"}],
            [ModelWithOptionalField(name="test", tag="v1")],
            id="optional_field_provided",
        ),
        pytest.param(
            fn_single_model,
            [SimpleModel(name="ok", value=1)],
            [SimpleModel(name="ok", value=1)],
            id="already_instantiated_model",
        ),
        pytest.param(fn_simple, ["hello", 3.0], ["hello", 3], id="int_from_float"),
        pytest.param(fn_bool, [True], [True], id="bool_coercion"),
        pytest.param(
            fn_single_model,
            [{"wrong_field": "oops"}],
            [{"wrong_field": "oops"}],
            id="invalid_dict_for_model_keeps_original",
        ),
        pytest.param(
            fn_list_of_int,
            ["not_a_list"],
            ["not_a_list"],
            id="wrong_type_keeps_original",
        ),
        pytest.param(
            fn_mixed,
            ["hello", {"bad": "dict"}, "not_bool"],
            ["hello", {"bad": "dict"}, "not_bool"],
            id="partial_validation_failure",
        ),
        pytest.param(
            fn_simple,
            [None, None],
            [None, None],
            id="none_for_non_optional_keeps_original",
        ),
        pytest.param(lambda a, b: None, [1, 2], [1, 2], id="lambda_no_hints"),
        pytest.param(
            _svc_process,
            [{"name": "a", "value": 1}],
            [SimpleModel(name="a", value=1)],
            id="bound_method",
        ),
        pytest.param(fn_bad_forward_ref, ["hello"], ["hello"], id="unresolvable_forward_ref"),
    ],
)
def test_validates_args(fn: Any, args: list, expected: list) -> None:
    result = _validate_activity_args(fn, args)
    assert list(result) == expected


_SKIP = {"_skip_registering": True, "retry_policy_max_attempts": 0}


@workflows.activity(**_SKIP)
async def act_simple(name: str, value: int) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_single_model(model: SimpleModel) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_nested_model(data: NestedModel) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_multiple_models(a: SimpleModel, b: NestedModel) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_optional_model(name: str, model: Optional[SimpleModel] = None) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_list_of_models(items: list[SimpleModel]) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_enum_param(color: Color) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_with_default(name: str, count: int = 10) -> None:
    pass


@workflows.activity(**_SKIP)
async def act_complex(
    name: str,
    model: SimpleModel,
    tags: list[str],
    metadata: dict[str, Any],
    count: int = 5,
) -> None:
    pass


@pytest.mark.parametrize(
    "fn, args, expected",
    [
        pytest.param(act_simple, ["hello", 42], ["hello", 42], id="simple_matching_types"),
        pytest.param(
            act_single_model,
            [{"name": "test", "value": 42}],
            [SimpleModel(name="test", value=42)],
            id="dict_to_simple_model",
        ),
        pytest.param(
            act_nested_model,
            [{"label": "point", "inner": {"x": 1, "y": 2}}],
            [NestedModel(label="point", inner=NestedInner(x=1, y=2))],
            id="dict_to_nested_model",
        ),
        pytest.param(
            act_multiple_models,
            [{"name": "a", "value": 1}, {"label": "b", "inner": {"x": 0, "y": 0}}],
            [SimpleModel(name="a", value=1), NestedModel(label="b", inner=NestedInner(x=0, y=0))],
            id="multiple_models",
        ),
        pytest.param(
            act_list_of_models,
            [[{"name": "a", "value": 1}, {"name": "b", "value": 2}]],
            [[SimpleModel(name="a", value=1), SimpleModel(name="b", value=2)]],
            id="list_of_models",
        ),
        pytest.param(
            act_optional_model,
            ["hello", {"name": "x", "value": 1}],
            ["hello", SimpleModel(name="x", value=1)],
            id="optional_model_dict",
        ),
        pytest.param(
            act_optional_model,
            ["hello", None],
            ["hello", None],
            id="optional_model_none",
        ),
        pytest.param(act_enum_param, ["red"], [Color.RED], id="enum_from_str"),
        pytest.param(act_with_default, ["hello"], ["hello"], id="fewer_args_than_params"),
        pytest.param(
            act_complex,
            ["test_name", {"name": "m", "value": 10}, ["tag1", "tag2"], {"key": "val"}, 3],
            ["test_name", SimpleModel(name="m", value=10), ["tag1", "tag2"], {"key": "val"}, 3],
            id="complex_all_args",
        ),
    ],
)
def test_validates_activity_args(fn: Any, args: list, expected: list) -> None:
    """WFL-1243: _validate_activity_args must resolve type hints on @activity-wrapped functions (Python 3.14+)."""
    result = _validate_activity_args(fn, args)
    assert list(result) == expected

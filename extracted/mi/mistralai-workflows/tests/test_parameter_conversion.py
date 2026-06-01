"""Tests for parameter conversion functions.

Tests convert_params_dict_to_user_args which validates input using generated
Pydantic models and converts to function arguments.
"""

import pytest
from pydantic import BaseModel, ValidationError

from mistralai.workflows.core.definition.validation._parameter_conversion import (
    convert_params_dict_to_user_args,
    convert_params_dict_to_user_args_and_kwargs,
    convert_query_update_result_to_temporal_format,
    convert_result_to_temporal_format,
)
from mistralai.workflows.core.definition.validation._schema_generator import (
    generate_pydantic_model_from_params,
    generate_pydantic_model_from_return_type,
)


class UserModel(BaseModel):
    name: str
    value: int


class NestedModel(BaseModel):
    outer: str
    inner: UserModel


class SchemaA(BaseModel):
    model_config = {"extra": "forbid"}
    prompt: str


class SchemaB(BaseModel):
    model_config = {"extra": "forbid"}
    count: int


class TestConvertParamsDictToUserArgs:
    def test_rejects_extra_fields(self):
        def my_func(name: str) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str},
            func=my_func,
        )

        with pytest.raises(ValidationError) as exc_info:
            convert_params_dict_to_user_args(
                {"name": "test", "extra": "bad"},
                {"name": str},
                model,
            )

        error_msg = str(exc_info.value).lower()
        assert "extra" in error_msg or "additional" in error_msg

    def test_accepts_valid_input(self):
        def my_func(name: str) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str},
            func=my_func,
        )

        result = convert_params_dict_to_user_args(
            {"name": "test"},
            {"name": str},
            model,
        )

        assert result == ("test",)

    def test_returns_empty_tuple_when_no_params(self):
        model = generate_pydantic_model_from_params("my_func", {})
        result = convert_params_dict_to_user_args({}, {}, model)
        assert result == ()

    def test_non_dict_falsy_param_treated_as_empty(self):
        """When Temporal passes a non-dict falsy value (e.g. 0) for a workflow
        whose wrapper expects dict|None, the conversion must not raise.
        This mirrors what happens when start_workflow("name", 0, ...) is called
        for a workflow with a default parameter like `initial_progress: int = 0`.
        """

        def my_func(initial_progress: int = 0) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"initial_progress": int},
            func=my_func,
        )

        # Temporal delivers params=0 (an int, not a dict) to the wrapper.
        # The conversion should coerce it to {} and use the default value.
        result = convert_params_dict_to_user_args(0, {"initial_progress": int}, model)
        assert result == (0,)

    def test_none_param_treated_as_empty_for_regular_model(self):
        """When Temporal passes None for a no-arg workflow, conversion must not raise."""
        model = generate_pydantic_model_from_params("my_func", {})
        result = convert_params_dict_to_user_args(None, {}, model)
        assert result == ()

    def test_multiple_params_returns_tuple_in_order(self):
        def my_func(name: str, count: int) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str, "count": int},
            func=my_func,
        )

        result = convert_params_dict_to_user_args(
            {"name": "test", "count": 42},
            {"name": str, "count": int},
            model,
        )

        assert result == ("test", 42)

    def test_single_basemodel_param_returns_model_instance(self):
        model = generate_pydantic_model_from_params(
            "my_func",
            {"data": UserModel},
            func=lambda data: None,
        )

        result = convert_params_dict_to_user_args(
            {"name": "test", "value": 42},
            {"data": UserModel},
            model,
        )

        assert len(result) == 1
        assert isinstance(result[0], UserModel)
        assert result[0].name == "test"
        assert result[0].value == 42

    def test_nested_model_validation(self):
        model = generate_pydantic_model_from_params(
            "my_func",
            {"data": NestedModel},
            func=lambda data: None,
        )

        result = convert_params_dict_to_user_args(
            {"outer": "hello", "inner": {"name": "test", "value": 10}},
            {"data": NestedModel},
            model,
        )

        assert len(result) == 1
        assert isinstance(result[0], NestedModel)
        assert result[0].outer == "hello"
        assert result[0].inner.name == "test"


class TestConvertResultToTemporalFormat:
    def test_none_result_returns_none(self):
        result = convert_result_to_temporal_format(None, None)
        assert result is None

    def test_basemodel_result_returns_dict(self):
        model_instance = UserModel(name="test", value=42)
        result = convert_result_to_temporal_format(model_instance, None)
        assert result == {"name": "test", "value": 42}

    def test_primitive_with_output_model_wraps_in_result(self):
        output_model = generate_pydantic_model_from_return_type("my_func", int)
        result = convert_result_to_temporal_format(42, output_model)
        assert result == {"result": 42}

    def test_primitive_without_output_model_returns_as_is(self):
        result = convert_result_to_temporal_format(42, None)
        assert result == 42

    def test_dict_with_output_model_validates_and_dumps(self):
        result = convert_result_to_temporal_format(
            {"name": "test", "value": 10},
            UserModel,
        )
        assert result == {"name": "test", "value": 10}


class TestConvertQueryUpdateResultToTemporalFormat:
    def test_none_result_returns_none(self):
        result = convert_query_update_result_to_temporal_format(None, None)
        assert result is None

    def test_basemodel_result_returns_dict(self):
        model_instance = UserModel(name="test", value=42)
        result = convert_query_update_result_to_temporal_format(model_instance, None)
        assert result == {"name": "test", "value": 42}

    def test_primitive_returns_as_is(self):
        result = convert_query_update_result_to_temporal_format(42, None)
        assert result == 42

    def test_string_returns_as_is(self):
        result = convert_query_update_result_to_temporal_format("hello", None)
        assert result == "hello"


class TestConvertParamsDictToUserArgsAndKwargs:
    def test_explicit_params_and_extra_kwargs(self):
        def my_func(name: str, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str},
            func=my_func,
            allow_extra=True,
        )

        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"name": "test", "extra1": "val1", "extra2": 42},
            {"name": str},
            model,
        )

        assert args == ("test",)
        assert kwargs == {"extra1": "val1", "extra2": 42}

    def test_only_kwargs_no_explicit_params(self):
        model = generate_pydantic_model_from_params(
            "my_func",
            {},
            allow_extra=True,
        )

        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"a": 1, "b": "two", "c": True},
            {},
            model,
        )

        assert args == ()
        assert kwargs == {"a": 1, "b": "two", "c": True}

    def test_no_extra_kwargs_returns_empty_dict(self):
        def my_func(name: str, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str},
            func=my_func,
            allow_extra=True,
        )

        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"name": "test"},
            {"name": str},
            model,
        )

        assert args == ("test",)
        assert kwargs == {}

    def test_multiple_explicit_params_and_extra_kwargs(self):
        def my_func(name: str, count: int, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str, "count": int},
            func=my_func,
            allow_extra=True,
        )

        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"name": "test", "count": 5, "filter": "active"},
            {"name": str, "count": int},
            model,
        )

        assert args == ("test", 5)
        assert kwargs == {"filter": "active"}

    def test_single_basemodel_param_and_extra_kwargs(self):
        model = generate_pydantic_model_from_params(
            "my_func",
            {"data": UserModel},
            func=lambda data: None,
            allow_extra=True,
        )

        # With allow_extra, a wrapper model is created with a "data" field,
        # so the input dict uses the param name as a key.
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"data": {"name": "test", "value": 42}, "extra_field": "bonus"},
            {"data": UserModel},
            model,
        )

        assert len(args) == 1
        assert isinstance(args[0], UserModel)
        assert args[0].name == "test"
        assert args[0].value == 42
        assert kwargs == {"extra_field": "bonus"}

    def test_empty_params_dict(self):
        model = generate_pydantic_model_from_params(
            "my_func",
            {},
            allow_extra=True,
        )

        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {},
            {},
            model,
        )

        assert args == ()
        assert kwargs == {}


class TestUnionBaseModelParam:
    def _make_model(self):
        return generate_pydantic_model_from_params(
            "my_func",
            {"params": SchemaA | SchemaB},
            func=lambda params: None,
        )

    def test_schema_a_input_returns_schema_a_instance(self):
        model = self._make_model()
        result = convert_params_dict_to_user_args(
            {"prompt": "hello"},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(result) == 1
        assert isinstance(result[0], SchemaA)
        assert result[0].prompt == "hello"

    def test_schema_b_input_returns_schema_b_instance(self):
        model = self._make_model()
        result = convert_params_dict_to_user_args(
            {"count": 42},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(result) == 1
        assert isinstance(result[0], SchemaB)
        assert result[0].count == 42

    def test_invalid_input_raises_validation_error(self):
        model = self._make_model()
        with pytest.raises(ValidationError):
            convert_params_dict_to_user_args(
                {"unknown": "field"},
                {"params": SchemaA | SchemaB},
                model,
            )

    def test_extra_fields_forbidden_raises_error(self):
        """Test that extra fields are rejected when all schemas have extra='forbid'"""
        model = self._make_model()
        with pytest.raises(ValidationError) as exc_info:
            convert_params_dict_to_user_args(
                {"prompt": "hello", "extra_field": "unexpected"},
                {"params": SchemaA | SchemaB},
                model,
            )

        error_msg = str(exc_info.value).lower()
        assert "extra" in error_msg or "additional" in error_msg


class TestUnionBaseModelParamWithKwargs:
    def _make_model(self):
        return generate_pydantic_model_from_params(
            "my_func",
            {"params": SchemaA | SchemaB},
            func=lambda params, **kwargs: None,
            allow_extra=True,
        )

    def test_schema_a_input_with_extra_kwargs(self):
        model = self._make_model()
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"params": {"prompt": "hello"}, "extra_field": "extra_value"},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(args) == 1
        assert isinstance(args[0], SchemaA)
        assert args[0].prompt == "hello"
        assert kwargs == {"extra_field": "extra_value"}

    def test_schema_b_input_with_extra_kwargs(self):
        model = self._make_model()
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"params": {"count": 42}, "another_extra": "value"},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(args) == 1
        assert isinstance(args[0], SchemaB)
        assert args[0].count == 42
        assert kwargs == {"another_extra": "value"}

    def test_union_with_no_extra_kwargs(self):
        model = self._make_model()
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"params": {"prompt": "test"}},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(args) == 1
        assert isinstance(args[0], SchemaA)
        assert args[0].prompt == "test"
        assert kwargs == {}


class TestUnionHandlingComparison:
    """Test that union handling works correctly in both kwargs and non-kwargs scenarios."""

    def test_union_without_kwargs_uses_rootmodel(self):
        """Test that without kwargs, union uses RootModel and extracts from .root"""
        from pydantic import RootModel

        model = generate_pydantic_model_from_params(
            "my_func",
            {"params": SchemaA | SchemaB},
            func=lambda params: None,
            allow_extra=False,
        )

        # Verify it's a RootModel
        assert issubclass(model, RootModel)

        args = convert_params_dict_to_user_args(
            {"prompt": "hello"},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(args) == 1
        assert isinstance(args[0], SchemaA)
        assert args[0].prompt == "hello"

    def test_union_with_kwargs_uses_regular_model(self):
        """Test that with kwargs, union uses regular model and extracts from field"""
        from pydantic import RootModel

        model = generate_pydantic_model_from_params(
            "my_func",
            {"params": SchemaA | SchemaB},
            func=lambda params, **kwargs: None,
            allow_extra=True,
        )

        # Verify it's NOT a RootModel
        assert not issubclass(model, RootModel)

        args, kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"params": {"count": 42}, "extra_field": "extra_value"},
            {"params": SchemaA | SchemaB},
            model,
        )
        assert len(args) == 1
        assert isinstance(args[0], SchemaB)
        assert args[0].count == 42
        assert kwargs == {"extra_field": "extra_value"}

    def test_both_scenarios_produce_correct_types(self):
        """Test that both scenarios correctly resolve the union to the appropriate type"""
        # Test SchemaA in both scenarios
        model_no_kwargs = generate_pydantic_model_from_params(
            "my_func",
            {"params": SchemaA | SchemaB},
            func=lambda params: None,
            allow_extra=False,
        )

        model_with_kwargs = generate_pydantic_model_from_params(
            "my_func",
            {"params": SchemaA | SchemaB},
            func=lambda params, **kwargs: None,
            allow_extra=True,
        )

        # Test SchemaA
        args_no_kwargs = convert_params_dict_to_user_args(
            {"prompt": "test"},
            {"params": SchemaA | SchemaB},
            model_no_kwargs,
        )

        args_with_kwargs, kwargs_with_kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"params": {"prompt": "test"}},
            {"params": SchemaA | SchemaB},
            model_with_kwargs,
        )

        # Both should produce SchemaA instances
        assert isinstance(args_no_kwargs[0], SchemaA)
        assert isinstance(args_with_kwargs[0], SchemaA)
        assert args_no_kwargs[0].prompt == args_with_kwargs[0].prompt == "test"

        # Test SchemaB
        args_no_kwargs = convert_params_dict_to_user_args(
            {"count": 99},
            {"params": SchemaA | SchemaB},
            model_no_kwargs,
        )

        args_with_kwargs, kwargs_with_kwargs = convert_params_dict_to_user_args_and_kwargs(
            {"params": {"count": 99}},
            {"params": SchemaA | SchemaB},
            model_with_kwargs,
        )

        # Both should produce SchemaB instances
        assert isinstance(args_no_kwargs[0], SchemaB)
        assert isinstance(args_with_kwargs[0], SchemaB)
        assert args_no_kwargs[0].count == args_with_kwargs[0].count == 99


class TestUnionWithNoneBaseModelParam:
    def _make_model(self, union_type):
        return generate_pydantic_model_from_params(
            "my_func",
            {"params": union_type},
            func=lambda params: None,
        )

    def test_schema_a_input_returns_schema_a_instance(self):
        model = self._make_model(SchemaA | SchemaB | None)
        result = convert_params_dict_to_user_args(
            {"prompt": "hello"},
            {"params": SchemaA | SchemaB | None},
            model,
        )
        assert len(result) == 1
        assert isinstance(result[0], SchemaA)
        assert result[0].prompt == "hello"

    def test_schema_b_input_returns_schema_b_instance(self):
        model = self._make_model(SchemaA | SchemaB | None)
        result = convert_params_dict_to_user_args(
            {"count": 7},
            {"params": SchemaA | SchemaB | None},
            model,
        )
        assert len(result) == 1
        assert isinstance(result[0], SchemaB)
        assert result[0].count == 7

    def test_invalid_input_raises_validation_error(self):
        model = self._make_model(SchemaA | SchemaB | None)
        with pytest.raises(ValidationError):
            convert_params_dict_to_user_args(
                {"unknown": "field"},
                {"params": SchemaA | SchemaB | None},
                model,
            )

    def test_none_input_returns_none_arg(self):
        # Passing None directly simulates a null Temporal payload.
        # RootModel[SchemaA | None].model_validate(None) resolves to root=None.
        model = self._make_model(SchemaA | None)
        result = convert_params_dict_to_user_args(
            None,  # type: ignore[arg-type]
            {"params": SchemaA | None},
            model,
        )
        assert result == (None,)


class TestRawNonDictArgs:
    """Test convert_params_dict_to_user_args with raw non-dict inputs.

    Temporal's start_workflow(name, arg) passes `arg` as-is to the wrapper.
    When `arg` is a primitive (int, str, bool), the conversion layer must
    wrap it into {param_name: value} for single-param workflows.
    """

    def test_raw_int_single_param(self):
        def my_func(value: int = 0) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"value": int}, func=my_func)
        result = convert_params_dict_to_user_args(42, {"value": int}, model)
        assert result == (42,)

    def test_raw_string_single_param(self):
        def my_func(name: str) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"name": str}, func=my_func)
        result = convert_params_dict_to_user_args("Alice", {"name": str}, model)
        assert result == ("Alice",)

    def test_raw_bool_single_param(self):
        def my_func(flag: bool = False) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"flag": bool}, func=my_func)
        result = convert_params_dict_to_user_args(True, {"flag": bool}, model)
        assert result == (True,)

    def test_raw_falsy_int_single_param(self):
        def my_func(value: int = 0) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"value": int}, func=my_func)
        result = convert_params_dict_to_user_args(0, {"value": int}, model)
        assert result == (0,)

    def test_raw_empty_string_single_param(self):
        def my_func(text: str = "") -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"text": str}, func=my_func)
        result = convert_params_dict_to_user_args("", {"text": str}, model)
        assert result == ("",)

    def test_raw_false_single_param(self):
        def my_func(flag: bool = False) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"flag": bool}, func=my_func)
        result = convert_params_dict_to_user_args(False, {"flag": bool}, model)
        assert result == (False,)

    def test_raw_int_no_params_falls_back_to_empty(self):
        """Raw non-dict with zero params should fall back to empty (ignore the value)."""
        model = generate_pydantic_model_from_params("my_func", {})
        result = convert_params_dict_to_user_args(42, {}, model)
        assert result == ()

    def test_raw_int_multi_params_falls_back_to_defaults(self):
        """Raw non-dict with multiple params should fall back to defaults."""

        def my_func(x: int = 10, y: int = 20) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"x": int, "y": int}, func=my_func)
        result = convert_params_dict_to_user_args(42, {"x": int, "y": int}, model)
        assert result == (10, 20)


class TestRawNonDictArgsAndKwargs:
    """Test convert_params_dict_to_user_args_and_kwargs with raw non-dict inputs.

    Same scenarios as TestRawNonDictArgs but for handlers that accept **kwargs.
    """

    def test_raw_int_single_param_with_kwargs(self):
        def my_func(value: int = 0, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"value": int}, func=my_func, allow_extra=True)
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(42, {"value": int}, model)
        assert args == (42,)
        assert kwargs == {}

    def test_raw_string_single_param_with_kwargs(self):
        def my_func(name: str, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"name": str}, func=my_func, allow_extra=True)
        args, kwargs = convert_params_dict_to_user_args_and_kwargs("Alice", {"name": str}, model)
        assert args == ("Alice",)
        assert kwargs == {}

    def test_raw_falsy_int_single_param_with_kwargs(self):
        def my_func(value: int = 0, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"value": int}, func=my_func, allow_extra=True)
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(0, {"value": int}, model)
        assert args == (0,)
        assert kwargs == {}

    def test_none_no_params_with_kwargs(self):
        model = generate_pydantic_model_from_params("my_func", {}, allow_extra=True)
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(None, {}, model)
        assert args == ()
        assert kwargs == {}

    def test_raw_int_no_params_with_kwargs(self):
        """Raw non-dict with zero explicit params should fall back to empty."""
        model = generate_pydantic_model_from_params("my_func", {}, allow_extra=True)
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(42, {}, model)
        assert args == ()
        assert kwargs == {}

    def test_raw_int_multi_params_with_kwargs_falls_back(self):
        """Raw non-dict with multiple params should fall back to defaults."""

        def my_func(x: int = 10, y: int = 20, **kwargs) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"x": int, "y": int}, func=my_func, allow_extra=True)
        args, kwargs = convert_params_dict_to_user_args_and_kwargs(42, {"x": int, "y": int}, model)
        assert args == (10, 20)
        assert kwargs == {}

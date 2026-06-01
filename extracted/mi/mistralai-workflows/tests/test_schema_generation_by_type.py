from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

import pytest
from pydantic import BaseModel, ConfigDict, RootModel, ValidationError
from typing_extensions import TypedDict

from mistralai.workflows.core.definition.validation._schema_generator import (
    generate_pydantic_model_from_params,
    generate_pydantic_model_from_return_type,
)


class UserBaseModel(BaseModel):
    name: str
    value: int


class UserStrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


class NestedUserModel(BaseModel):
    outer_name: str
    inner: UserBaseModel


@dataclass
class SimpleDataclass:
    name: str
    count: int


@dataclass
class NestedDataclass:
    outer: str
    inner: SimpleDataclass


@dataclass
class DataclassWithBaseModel:
    name: str
    model: UserBaseModel


@dataclass
class DataclassWithDefaults:
    name: str
    count: int = 0
    active: bool = True


class BaseModelWithDataclass(BaseModel):
    name: str
    data: SimpleDataclass


class SimpleTypedDict(TypedDict):
    name: str
    value: int


class NestedTypedDict(TypedDict):
    outer: str
    inner: SimpleTypedDict


class SimpleEnum(Enum):
    OPTION_A = "a"
    OPTION_B = "b"


class RegularPythonClass:
    def __init__(self, name: str):
        self.name = name


def generate_schema_from_params(params: dict, func_name: str = "test_func") -> dict:
    def dummy_func() -> None:
        pass

    model = generate_pydantic_model_from_params(func_name, params, func=dummy_func)
    return model.model_json_schema()


class TestSingleBaseModelReturnsUnchanged:
    def test_single_basemodel_returns_original(self):
        def my_func(data: UserBaseModel) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"data": UserBaseModel}, func=my_func)
        assert result is UserBaseModel

    def test_single_strict_basemodel_returns_original(self):
        def my_func(data: UserStrictModel) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"data": UserStrictModel}, func=my_func)
        assert result is UserStrictModel

    def test_single_nested_basemodel_returns_original(self):
        def my_func(data: NestedUserModel) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"data": NestedUserModel}, func=my_func)
        assert result is NestedUserModel


class TestGeneratedWrapperForbidsExtra:
    def test_primitives_wrapper_forbids_extra(self):
        schema = generate_schema_from_params({"name": str, "count": int})
        assert schema.get("additionalProperties") is False

    def test_empty_params_forbids_extra(self):
        schema = generate_schema_from_params({})
        assert schema.get("additionalProperties") is False

    def test_mixed_params_wrapper_forbids_extra(self):
        schema = generate_schema_from_params({"name": str, "model": UserBaseModel})
        assert schema.get("additionalProperties") is False

    def test_multiple_basemodels_wrapper_forbids_extra(self):
        schema = generate_schema_from_params(
            {
                "model1": UserBaseModel,
                "model2": UserStrictModel,
            }
        )
        assert schema.get("additionalProperties") is False


class TestUserBaseModelsPreserved:
    def test_basemodel_in_wrapper_preserves_user_config(self):
        schema = generate_schema_from_params({"name": str, "model": UserBaseModel})
        defs = schema.get("$defs", {})
        user_model_def = defs.get("UserBaseModel")
        assert user_model_def is not None
        assert user_model_def.get("additionalProperties") is not False

    def test_strict_basemodel_in_wrapper_preserves_config(self):
        schema = generate_schema_from_params({"name": str, "model": UserStrictModel})
        defs = schema.get("$defs", {})
        strict_model_def = defs.get("UserStrictModel")
        assert strict_model_def is not None
        assert strict_model_def.get("additionalProperties") is False


class TestDataclassTransformation:
    def test_dataclass_transformed_to_forbid_extra(self):
        schema = generate_schema_from_params({"data": SimpleDataclass})
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False

    def test_nested_dataclass_both_transformed(self):
        schema = generate_schema_from_params({"data": NestedDataclass})
        defs = schema.get("$defs", {})
        assert "NestedDataclass_ForbidExtra" in defs
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["NestedDataclass_ForbidExtra"].get("additionalProperties") is False
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False

    def test_dataclass_with_primitive_both_strict(self):
        schema = generate_schema_from_params({"data": SimpleDataclass, "count": int})
        assert schema.get("additionalProperties") is False
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False


class TestTypedDictBehavior:
    def test_typeddict_forbids_extra(self):
        schema = generate_schema_from_params({"data": SimpleTypedDict})
        defs = schema.get("$defs", {})
        assert "SimpleTypedDict" in defs
        assert defs["SimpleTypedDict"].get("additionalProperties") is False

    def test_nested_typeddict_both_forbid_extra(self):
        schema = generate_schema_from_params({"data": NestedTypedDict})
        defs = schema.get("$defs", {})
        assert "NestedTypedDict" in defs
        assert "SimpleTypedDict" in defs
        assert defs["NestedTypedDict"].get("additionalProperties") is False
        assert defs["SimpleTypedDict"].get("additionalProperties") is False


class TestCollectionsWithTransformableTypes:
    def test_list_of_dataclass_transforms_items(self):
        schema = generate_schema_from_params({"items": List[SimpleDataclass]})
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False

    def test_dict_of_dataclass_transforms_values(self):
        schema = generate_schema_from_params({"mapping": Dict[str, SimpleDataclass]})
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False

    def test_optional_dataclass_transforms(self):
        schema = generate_schema_from_params({"data": Optional[SimpleDataclass]})
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False

    def test_list_of_basemodel_preserves_user_config(self):
        schema = generate_schema_from_params({"items": List[UserBaseModel]})
        defs = schema.get("$defs", {})
        assert "UserBaseModel" in defs
        assert defs["UserBaseModel"].get("additionalProperties") is not False


class TestMixedBaseModelAndDataclass:
    def test_basemodel_preserved_dataclass_transformed(self):
        schema = generate_schema_from_params(
            {
                "user_model": UserBaseModel,
                "data": SimpleDataclass,
            }
        )
        defs = schema.get("$defs", {})
        assert schema.get("additionalProperties") is False
        assert "UserBaseModel" in defs
        assert defs["UserBaseModel"].get("additionalProperties") is not False
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False


class TestRegularPythonClassesFail:
    def test_regular_class_fails(self):
        with pytest.raises(Exception) as exc_info:
            generate_schema_from_params({"obj": RegularPythonClass})
        assert "Unable to generate pydantic-core schema" in str(exc_info.value)


class TestUnionTypes:
    def test_union_with_dataclass_transforms(self):
        schema = generate_schema_from_params({"value": Union[str, SimpleDataclass]})
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs
        assert defs["SimpleDataclass_ForbidExtra"].get("additionalProperties") is False


class TestEnumAndLiteral:
    def test_enum_generates_valid_schema(self):
        schema = generate_schema_from_params({"option": SimpleEnum})
        assert schema.get("additionalProperties") is False

    def test_literal_generates_valid_schema(self):
        schema = generate_schema_from_params({"mode": Literal["fast", "slow"]})
        assert schema.get("additionalProperties") is False


class TestSingleNonBaseModelParams:
    def test_single_dataclass_creates_wrapper(self):
        schema = generate_schema_from_params({"data": SimpleDataclass})
        assert schema.get("additionalProperties") is False
        defs = schema.get("$defs", {})
        assert "SimpleDataclass_ForbidExtra" in defs

    def test_single_typeddict_creates_wrapper(self):
        schema = generate_schema_from_params({"data": SimpleTypedDict})
        assert schema.get("additionalProperties") is False
        defs = schema.get("$defs", {})
        assert "SimpleTypedDict" in defs


class TestCrossTypeNesting:
    def test_dataclass_containing_basemodel_preserves_basemodel(self):
        schema = generate_schema_from_params({"data": DataclassWithBaseModel})
        defs = schema.get("$defs", {})
        assert "DataclassWithBaseModel_ForbidExtra" in defs
        assert defs["DataclassWithBaseModel_ForbidExtra"].get("additionalProperties") is False
        assert "UserBaseModel" in defs
        assert defs["UserBaseModel"].get("additionalProperties") is not False

    def test_basemodel_containing_dataclass_preserves_dataclass(self):
        schema = generate_schema_from_params({"model": BaseModelWithDataclass, "extra": str})
        defs = schema.get("$defs", {})
        assert "BaseModelWithDataclass" in defs
        assert "SimpleDataclass" in defs
        assert defs["SimpleDataclass"].get("additionalProperties") is not False


class TestDataclassWithDefaults:
    def test_dataclass_defaults_preserved(self):
        schema = generate_schema_from_params({"data": DataclassWithDefaults})
        defs = schema.get("$defs", {})
        assert "DataclassWithDefaults_ForbidExtra" in defs
        transformed = defs["DataclassWithDefaults_ForbidExtra"]
        assert transformed.get("additionalProperties") is False
        assert "name" in transformed.get("required", [])
        assert "count" not in transformed.get("required", [])
        assert "active" not in transformed.get("required", [])


class TestAdditionalCollections:
    def test_optional_basemodel_preserves_config(self):
        schema = generate_schema_from_params({"data": Optional[UserBaseModel]})
        defs = schema.get("$defs", {})
        assert "UserBaseModel" in defs
        assert defs["UserBaseModel"].get("additionalProperties") is not False

    def test_list_of_typeddict_preserves_config(self):
        schema = generate_schema_from_params({"items": List[SimpleTypedDict]})
        defs = schema.get("$defs", {})
        assert "SimpleTypedDict" in defs
        assert defs["SimpleTypedDict"].get("additionalProperties") is False

    def test_dict_of_typeddict_preserves_config(self):
        schema = generate_schema_from_params({"mapping": Dict[str, SimpleTypedDict]})
        defs = schema.get("$defs", {})
        assert "SimpleTypedDict" in defs
        assert defs["SimpleTypedDict"].get("additionalProperties") is False


class TestFunctionSignatureDefaults:
    def test_param_with_default_not_required(self):
        def my_func(name: str, count: int = 10) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str, "count": int},
            func=my_func,
        )
        schema = model.model_json_schema()
        assert "name" in schema.get("required", [])
        assert "count" not in schema.get("required", [])

    def test_all_params_with_defaults(self):
        def my_func(name: str = "default", count: int = 0) -> None:
            pass

        model = generate_pydantic_model_from_params(
            "my_func",
            {"name": str, "count": int},
            func=my_func,
        )
        schema = model.model_json_schema()
        assert schema.get("required") is None or schema.get("required") == []


class TestGeneratePydanticModelFromReturnType:
    def test_none_return_type_returns_none(self):
        result = generate_pydantic_model_from_return_type("my_func", type(None))
        assert result is None

    def test_basemodel_return_type_returns_unchanged(self):
        result = generate_pydantic_model_from_return_type("my_func", UserBaseModel)
        assert result is UserBaseModel

    def test_strict_basemodel_return_type_returns_unchanged(self):
        result = generate_pydantic_model_from_return_type("my_func", UserStrictModel)
        assert result is UserStrictModel

    def test_primitive_return_type_creates_wrapper(self):
        result = generate_pydantic_model_from_return_type("my_func", str)
        assert result is not None
        assert "result" in result.model_fields
        schema = result.model_json_schema()
        assert "result" in schema.get("properties", {})

    def test_optional_basemodel_returns_basemodel(self):
        result = generate_pydantic_model_from_return_type("my_func", Optional[UserBaseModel])
        assert result is UserBaseModel

    def test_optional_primitive_creates_wrapper(self):
        result = generate_pydantic_model_from_return_type("my_func", Optional[int])
        assert result is not None
        assert "result" in result.model_fields

    def test_union_with_none_extracts_non_none_type(self):
        result = generate_pydantic_model_from_return_type("my_func", Union[str, None])
        assert result is not None
        assert "result" in result.model_fields

    def test_model_name_uses_suffix(self):
        result = generate_pydantic_model_from_return_type("my_func", int, model_suffix="Result")
        assert result.__name__ == "my_func_Result"

    def test_union_with_multiple_non_none_types_preserves_all(self):
        result = generate_pydantic_model_from_return_type("my_func", Union[str, int, None])
        assert result is not None
        assert "result" in result.model_fields
        instance_str = result(result="hello")
        instance_int = result(result=42)
        assert instance_str.result == "hello"
        assert instance_int.result == 42

    def test_union_without_none_preserves_all_types(self):
        result = generate_pydantic_model_from_return_type("my_func", Union[str, int])
        assert result is not None
        assert "result" in result.model_fields
        instance_str = result(result="hello")
        instance_int = result(result=42)
        assert instance_str.result == "hello"
        assert instance_int.result == 42


class TestAllowExtraParameter:
    def test_allow_extra_false_rejects_extra_fields(self):
        def my_func(city: str) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"city": str}, func=my_func, allow_extra=False)

        instance = model(city="Paris")
        assert instance.city == "Paris"

        with pytest.raises(ValidationError) as exc_info:
            model(city="Paris", units="celsius")
        assert "units" in str(exc_info.value)

    def test_allow_extra_true_accepts_extra_fields(self):
        def my_func(city: str) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"city": str}, func=my_func, allow_extra=True)

        instance = model(city="Paris", units="celsius", language="fr")
        assert instance.city == "Paris"
        assert instance.model_extra == {"units": "celsius", "language": "fr"}

    def test_allow_extra_default_is_false(self):
        def my_func(city: str) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"city": str}, func=my_func)

        with pytest.raises(ValidationError):
            model(city="Paris", extra_field="value")

    def test_allow_extra_with_empty_params(self):
        model = generate_pydantic_model_from_params("my_func", {}, allow_extra=True)

        instance = model(any_field="value", another="test")
        assert instance.model_extra == {"any_field": "value", "another": "test"}

    def test_allow_extra_preserves_explicit_field_types(self):
        def my_func(count: int) -> None:
            pass

        model = generate_pydantic_model_from_params("my_func", {"count": int}, func=my_func, allow_extra=True)

        instance = model(count=42, extra="allowed")
        assert instance.count == 42
        assert instance.model_extra == {"extra": "allowed"}

        with pytest.raises(ValidationError):
            model(count="not_an_int", extra="allowed")


class SchemaA(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str


class SchemaB(BaseModel):
    model_config = ConfigDict(extra="forbid")
    count: int


class TestBareUnionOfBaseModels:
    def test_union_returns_root_model_subclass(self):
        def my_func(params: SchemaA | SchemaB) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | SchemaB}, func=my_func)
        assert issubclass(result, RootModel)

    def test_union_schema_has_top_level_any_of(self):
        def my_func(params: SchemaA | SchemaB) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | SchemaB}, func=my_func)
        schema = result.model_json_schema()
        assert "anyOf" in schema
        assert len(schema["anyOf"]) == 2

    def test_union_schema_has_no_params_wrapper(self):
        def my_func(params: SchemaA | SchemaB) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | SchemaB}, func=my_func)
        schema = result.model_json_schema()
        assert "properties" not in schema or "params" not in schema.get("properties", {})

    def test_union_with_none_returns_root_model_subclass(self):
        def my_func(params: SchemaA | SchemaB | None) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | SchemaB | None}, func=my_func)
        assert issubclass(result, RootModel)

    def test_union_with_none_schema_has_two_basemodel_variants(self):
        def my_func(params: SchemaA | SchemaB | None) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | SchemaB | None}, func=my_func)
        schema = result.model_json_schema()
        # anyOf entries: SchemaA, SchemaB, and null
        assert "anyOf" in schema
        variants = schema["anyOf"]
        assert any(v.get("type") == "null" for v in variants)
        non_null = [v for v in variants if v.get("type") != "null"]
        assert len(non_null) == 2

    def test_optional_single_basemodel_returns_root_model_subclass(self):
        def my_func(params: SchemaA | None) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | None}, func=my_func)
        assert issubclass(result, RootModel)

    def test_optional_single_basemodel_schema_has_anyof_with_null(self):
        def my_func(params: SchemaA | None) -> None:
            pass

        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | None}, func=my_func)
        schema = result.model_json_schema()
        assert "anyOf" in schema
        variants = schema["anyOf"]
        assert any(v.get("type") == "null" for v in variants)
        non_null = [v for v in variants if v.get("type") != "null"]
        assert len(non_null) == 1

    def test_typing_optional_spelling_returns_root_model(self):
        from typing import Optional

        result = generate_pydantic_model_from_params("my_func", {"params": Optional[SchemaA]})
        assert issubclass(result, RootModel)


class TestUnionParamValidation:
    def test_mixed_union_basemodel_and_primitive_raises(self):
        with pytest.raises(TypeError, match="unsupported union members: str"):
            generate_pydantic_model_from_params("my_func", {"params": SchemaA | str})

    def test_mixed_union_basemodel_and_int_raises(self):
        with pytest.raises(TypeError, match="unsupported union members: int"):
            generate_pydantic_model_from_params("my_func", {"params": SchemaA | int})

    def test_mixed_union_multiple_bad_members_lists_all(self):
        with pytest.raises(TypeError, match="str") as exc_info:
            generate_pydantic_model_from_params("my_func", {"params": SchemaA | str | int})
        assert "int" in str(exc_info.value)

    def test_mixed_union_error_names_param_and_func(self):
        with pytest.raises(TypeError, match="'data' of 'process'"):
            generate_pydantic_model_from_params("process", {"data": SchemaA | str})

    def test_pure_primitive_union_does_not_raise(self):
        # str | int has no BaseModel member — falls through to general path, no error
        result = generate_pydantic_model_from_params("my_func", {"params": str | int})
        assert not issubclass(result, RootModel)

    def test_primitive_optional_does_not_raise(self):
        # str | None has no BaseModel member — no error
        result = generate_pydantic_model_from_params("my_func", {"params": str | None})
        assert not issubclass(result, RootModel)

    def test_mixed_union_with_kwargs_does_not_raise(self):
        # allow_extra=True bypasses the single-param branch entirely
        result = generate_pydantic_model_from_params("my_func", {"params": SchemaA | str}, allow_extra=True)
        assert not issubclass(result, RootModel)

    def test_typing_optional_spelling_does_not_raise(self):
        from typing import Optional

        # Optional[A] is Union[A, None] — should be accepted
        result = generate_pydantic_model_from_params("my_func", {"params": Optional[SchemaA]})
        assert issubclass(result, RootModel)

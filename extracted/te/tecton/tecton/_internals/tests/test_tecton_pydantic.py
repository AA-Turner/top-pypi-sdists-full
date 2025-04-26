from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pytest

from tecton._internals import tecton_pydantic
from tecton._internals.tecton_pydantic import pydantic_v1


@dataclass
class TestTectonPydantic__BasicTypeTestCase:
    annotation: type
    valid_values: Any
    invalid_values: Any


TYPE_TESTS = [
    TestTectonPydantic__BasicTypeTestCase(int, valid_values=[1], invalid_values=[None, 1.0, "1"]),
    TestTectonPydantic__BasicTypeTestCase(Optional[int], valid_values=[1, None], invalid_values=[1.0, "1"]),
    TestTectonPydantic__BasicTypeTestCase(bool, valid_values=[True, False], invalid_values=[None, 1, "True"]),
    # Typeguard, which we use for typechecking Pydantic V1, permits integer as floats.
    TestTectonPydantic__BasicTypeTestCase(float, valid_values=[1.0, 1], invalid_values=[None, "1.0"]),
    TestTectonPydantic__BasicTypeTestCase(str, valid_values=[""], invalid_values=[None, 1]),
    TestTectonPydantic__BasicTypeTestCase(
        datetime, valid_values=[datetime(2022, 1, 1)], invalid_values=[1, "2020-07-10 15:00:00"]
    ),
    TestTectonPydantic__BasicTypeTestCase(timedelta, valid_values=[timedelta(seconds=1)], invalid_values=[1]),
    TestTectonPydantic__BasicTypeTestCase(Any, valid_values=[1, None, ""], invalid_values=[]),
    TestTectonPydantic__BasicTypeTestCase(List[int], valid_values=[[], [1, 2]], invalid_values=[[1, ""]]),
    TestTectonPydantic__BasicTypeTestCase(Tuple[int, str], valid_values=[(1, "foo")], invalid_values=[(1, 2)]),
]


# This test checks a couple of things:
# 1) Some of the exact typechecking behavior that we get from typeguard.
# 2) That the type checking is wired up correct with pydantic, i.e. it's run before typeguard type coercion.
@pytest.mark.parametrize("test_case", TYPE_TESTS)
def test_type_checking(test_case: TestTectonPydantic__BasicTypeTestCase):
    class TestModel(tecton_pydantic.StrictModel):
        field: test_case.annotation

    for valid_value in test_case.valid_values:
        TestModel(field=valid_value)

    for invalid_value in test_case.invalid_values:
        with pytest.raises(pydantic_v1.ValidationError):
            TestModel(field=invalid_value)


@pytest.mark.parametrize("base_type", [tecton_pydantic.StrictModel, tecton_pydantic.StrictFrozenModel])
def test_extra_fields_disallowed(base_type):
    class TestModel(base_type):
        field: int

    with pytest.raises(pydantic_v1.ValidationError):
        TestModel(field=1, extra_field=2)


def test_frozen_model():
    class TestModel(tecton_pydantic.StrictFrozenModel):
        field: int

    instance = TestModel(field=1)

    with pytest.raises(TypeError):
        instance.field = 2


def test_banned_union():
    with pytest.raises(TypeError, match=r"Unions with Pydantic coercible types are not allowed"):

        class TestModel(tecton_pydantic.StrictModel):
            field: Union[int, float]


def test_banned_nested_union():
    with pytest.raises(TypeError, match=r"Unions with Pydantic coercible types are not allowed"):

        class TestModel(tecton_pydantic.StrictModel):
            field: Dict[str, Union[datetime, timedelta]]


class TestForwardDeclaredModel(tecton_pydantic.StrictModel):
    field: "TestForwardDeclaredSubModel"


class TestForwardDeclaredSubModel(tecton_pydantic.StrictModel):
    field: int


TestForwardDeclaredModel.update_forward_refs()


def test_forward_declaration():
    TestForwardDeclaredModel(field=TestForwardDeclaredSubModel(field=1))


def test_nested_model_parsing():
    class SubModel(tecton_pydantic.StrictModel):
        field: int

    class Model(tecton_pydantic.StrictModel):
        submodel: SubModel
        optional_submodel: Optional[SubModel]

    Model(**{"submodel": {"field": 1}, "optional_submodel": {"field": 2}})  # noqa: PIE804

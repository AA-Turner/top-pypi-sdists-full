from collections.abc import Callable
from typing import Any

import numpy as np
import pytest
from pydantic import BaseModel, Field

from numpydantic import NDArray, Shape
from numpydantic.dtype import Number


@pytest.fixture(scope="function")
def array_model() -> Callable[[tuple[int, ...], type | np.dtype], type[BaseModel]]:
    def _model(
        shape: tuple[int, ...] = (10, 10), dtype: type | np.dtype = float
    ) -> type[BaseModel]:
        shape_str = ", ".join([str(s) for s in shape])

        class MyModel(BaseModel):
            array: NDArray[Shape[shape_str], dtype]

        return MyModel

    return _model


@pytest.fixture(scope="session")
def model_rgb() -> type[BaseModel]:
    class RGB(BaseModel):
        array: (
            NDArray[Shape["* x, * y"], Number]
            | NDArray[Shape["* x, * y, 3 r_g_b"], Number]
            | NDArray[Shape["* x, * y, 3 r_g_b, 4 r_g_b_a"], Number]
            | None
        ) = Field(None)

    return RGB


@pytest.fixture(scope="session")
def model_blank() -> type[BaseModel]:
    """A model with any shape and dtype"""

    class BlankModel(BaseModel):
        array: NDArray[Shape["*, ..."], Any]

    return BlankModel

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any
from typing import Iterator
from typing import Mapping
from typing import MutableMapping
from typing import Optional

import numpy
import pyarrow

from tecton_core import data_types


_LOAD_FN_NAME = "load_context"
_RESERVED_MODEL_CONTEXT_KEY = "model"
_TECTON_MODEL_SPEC_NAME = "_tecton_custom_model"

_CONTEXT_PARAM = Mapping[str, Any]
_DEFAULT_BATCH_SIZE = 50_000


def tecton_type_to_pyarrow(tecton_type: data_types.DataType) -> pyarrow.DataType:
    if tecton_type == data_types.Int32Type():
        return pyarrow.int32()
    if tecton_type == data_types.Int64Type():
        return pyarrow.int64()
    if tecton_type == data_types.Float32Type():
        return pyarrow.float32()
    if tecton_type == data_types.Float64Type():
        return pyarrow.float64()
    if tecton_type == data_types.StringType():
        return pyarrow.string()
    if isinstance(tecton_type, data_types.ArrayType):
        return pyarrow.list_(tecton_type_to_pyarrow(tecton_type.element_type))
    msg = f"Invalid tecton type found {tecton_type}"
    raise ValueError(msg)


def pyarrow_batch_to_numpy_dict(batch: pyarrow.RecordBatch) -> Mapping[str, numpy.ndarray]:
    # zero_copy_only=False is needed to allow conversion of non-primitive types see more:
    # https://arrow.apache.org/docs/python/generated/pyarrow.Int16Array.html#pyarrow.Int16Array.to_numpy
    return {name: column.to_numpy(zero_copy_only=False) for name, column in zip(batch.schema.names, batch.columns)}


class CustomModelContainerBase:
    _data_dir: Path
    _model_file_path: str

    # Late init params
    _context: MutableMapping[str, Any]

    def __init__(self, data_dir: str, model_file_path: str = "model.py") -> None:
        self._data_dir = Path(data_dir)
        self._model_file_path = model_file_path
        self._context = {}

    def load(self):
        model_module = self._load_model_module()
        _load_fn = getattr(model_module, _LOAD_FN_NAME, None)

        if not _load_fn:
            msg = f"`{_LOAD_FN_NAME}` function is missing in the model repo"
            raise AttributeError(msg)

        _load_fn(self._data_dir, self._context)
        if not self._model:
            msg = "No 'model' found in the context. `load` function should initialize the model and put it in the context with 'model' key."
            raise ValueError(msg)
        return model_module

    def predict(self, input: pyarrow.RecordBatch) -> numpy.ndarray:
        raise NotImplementedError

    def _load_model_module(self):
        spec = importlib.util.spec_from_file_location(_TECTON_MODEL_SPEC_NAME, self._data_dir / self._model_file_path)
        model_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_module)
        return model_module

    @property
    def _model(self):
        model = self._context.get(_RESERVED_MODEL_CONTEXT_KEY, None)
        return model


# TODO(jiadong): Implement custom model batch function.
def default_batch_fn(
    batch: pyarrow.RecordBatch,
) -> Iterator[pyarrow.RecordBatch]:
    index = 0
    while index < batch.num_rows:
        num_rows = min(_DEFAULT_BATCH_SIZE, batch.num_rows - index)
        yield batch.take(list(range(index, index + num_rows)))
        index += num_rows


@dataclass
class CustomModelBatchFuncConfig:
    # TODO(jiadong): Add necessary params to batch function config such as user-provided batch size.

    # Note: _final_kwargs is a late init object.
    _final_kwargs: Optional[Mapping[str, Any]] = None

    @classmethod
    def create(cls) -> CustomModelBatchFuncConfig:
        return cls()

    def load(self):
        self._final_kwargs = MappingProxyType({})
        return self

    def kwargs(self) -> Mapping[str, Any]:
        if self._final_kwargs is None:
            msg = "`load` must be called prior to calling `kwargs`."
            raise ValueError(msg)
        return self._final_kwargs

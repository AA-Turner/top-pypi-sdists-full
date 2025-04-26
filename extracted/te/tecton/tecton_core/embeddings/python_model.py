from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any
from typing import Callable
from typing import List
from typing import Mapping
from typing import Optional

import numpy
import pyarrow

from tecton_core import schema
from tecton_core.embeddings.model_container import _CONTEXT_PARAM
from tecton_core.embeddings.model_container import CustomModelContainerBase
from tecton_core.embeddings.model_container import pyarrow_batch_to_numpy_dict
from tecton_core.embeddings.model_container import tecton_type_to_pyarrow
from tecton_core.errors import TectonValidationError


_PREDICT_FN = Optional[Callable[[Mapping[str, numpy.ndarray], _CONTEXT_PARAM], numpy.ndarray]]
_PREDICT_FN_NAME = "predict"


class PythonModelContainer(CustomModelContainerBase):
    _predict: _PREDICT_FN = None

    def load(self):
        model_module = super().load()
        self._predict = getattr(model_module, _PREDICT_FN_NAME, None)
        self._validate_python_model()

    def predict(self, input: pyarrow.RecordBatch) -> numpy.ndarray:
        numpy_dict = pyarrow_batch_to_numpy_dict(input)
        output = self._predict(numpy_dict, self._context)
        if not isinstance(output, numpy.ndarray):
            msg = "Model output from predict should be a numpy array"
            raise TypeError(msg)
        return output

    def _validate_python_model(self):
        if self._predict is None:
            msg = "Model file must have a `predict` function with signature `predict(inputs, context)`."
            raise TectonValidationError(msg)


def python_model_inference(
    batch: pyarrow.RecordBatch,
    model: PythonModelContainer,
    input_columns: List[schema.Column],
    output_column: schema.Column,
    model_input_schema: List[schema.Column],
) -> pyarrow.RecordBatch:
    input_batch = batch.select([col.name for col in input_columns])
    model_input_names = [col.name for col in model_input_schema]

    # Rename input columns to model input schema column names.
    # TODO(jiadong): we can use pyarrow built-in `rename_columns` when we upgrade pyarrow to 16.0+.
    input_columns = [input_batch.column(i) for i in range(input_batch.num_columns)]
    input_batch = pyarrow.RecordBatch.from_arrays(input_columns, model_input_names)

    output = _python_model_predict(model=model, input_batch=input_batch)
    output = _convert_numpy_to_arrow(output, batch.num_rows, tecton_type_to_pyarrow(output_column.dtype))

    batch_with_results = pyarrow.RecordBatch.from_arrays(
        [*batch.columns, output],
        schema=batch.schema.append(pyarrow.field(output_column.name, output.type)),
    )
    return batch_with_results


def _python_model_predict(model: PythonModelContainer, input_batch: pyarrow.RecordBatch) -> numpy.ndarray:
    return model.predict(input_batch)


def _convert_numpy_to_arrow(
    output: numpy.ndarray, num_of_rows: int, output_column_type: pyarrow.DataType
) -> pyarrow.Array:
    # If the output is scalar but is 2d (n x 1), then conversion to pyArrow will fail with scalar output_column_type
    # so we need to remove that extra dimension
    if output.ndim == 2 and not isinstance(output_column_type, pyarrow.ListType):
        output = output.squeeze()

    if output.shape[0] != num_of_rows:
        msg = "Output of model should have a single row per input row. "
        raise TectonValidationError(msg)
    return pyarrow.array(list(output), type=output_column_type)


@dataclass
class PythonModelInferenceFuncConfig:
    _model_dir: str
    _model_file_path: str
    _extra_kwargs: Mapping[str, Any]

    # Note: _final_kwargs is a late init object.
    _final_kwargs: Optional[Mapping[str, Any]] = None

    @classmethod
    def create(
        cls,
        model_dir: str,
        model_file_path: str,
        input_columns: List[schema.Column],
        output_column: schema.Column,
        model_input_schema: List[schema.Column],
    ) -> PythonModelInferenceFuncConfig:
        return cls(
            _model_dir=model_dir,
            _model_file_path=model_file_path,
            _extra_kwargs=MappingProxyType(
                {
                    "input_columns": input_columns,
                    "output_column": output_column,
                    "model_input_schema": model_input_schema,
                }
            ),
        )

    def load(self):
        model_container = PythonModelContainer(data_dir=self._model_dir, model_file_path=self._model_file_path)
        model_container.load()
        self._final_kwargs = MappingProxyType(dict(model=model_container, **self._extra_kwargs))
        return self

    def kwargs(self) -> Mapping[str, Any]:
        if self._final_kwargs is None:
            msg = "`load` must be called prior to calling `kwargs`."
            raise ValueError(msg)
        return self._final_kwargs

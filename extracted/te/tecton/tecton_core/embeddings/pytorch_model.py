from __future__ import annotations

from collections import abc
from dataclasses import dataclass
from logging import getLogger
from types import MappingProxyType
from typing import Any
from typing import Callable
from typing import List
from typing import Mapping
from typing import Optional

import numpy
import pyarrow
import torch

from tecton_core import schema
from tecton_core.embeddings import execution_utils
from tecton_core.embeddings.model_container import CustomModelContainerBase
from tecton_core.embeddings.model_container import tecton_type_to_pyarrow
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError


logger = getLogger(__name__)

_PRE_PROCESSOR_FN_NAME = "preprocessor"
_POST_PROCESSOR_FN_NAME = "postprocessor"

_CONTEXT_PARAM = Mapping[str, Any]
_PRE_PROCESSOR_FN = Optional[Callable[[Mapping[str, numpy.ndarray], _CONTEXT_PARAM], Mapping[str, torch.Tensor]]]
_POST_PROCESSOR_FN = Optional[Callable[[torch.Tensor, _CONTEXT_PARAM], numpy.ndarray]]

_MAX_BISECT_RECURSION_LEVEL = 8


def _default_pytorch_preprocessor(input: Mapping[str, numpy.ndarray]) -> Mapping[str, torch.Tensor]:
    return {name: torch.tensor(array) for name, array in input.items()}


class PytorchModelContainer(CustomModelContainerBase):
    _preprocessor: _PRE_PROCESSOR_FN = None
    _postprocessor: _POST_PROCESSOR_FN = None

    def load(self):
        model_module = super().load()
        self._preprocessor = getattr(model_module, _PRE_PROCESSOR_FN_NAME, None)
        self._postprocessor = getattr(model_module, _POST_PROCESSOR_FN_NAME, None)

    def predict(self, input: pyarrow.RecordBatch) -> numpy.ndarray:
        numpy_dict = {
            name: column.to_numpy(zero_copy_only=False) for name, column in zip(input.schema.names, input.columns)
        }
        if self._preprocessor:
            input = self._preprocessor(numpy_dict, self._context)
        else:
            input = _default_pytorch_preprocessor(numpy_dict)

        if not isinstance(input, abc.Mapping):
            msg = f"`preprocessor` needs to return a 'Mapping[str, torch.Tensor]', but received '{type(input)}'"
            raise TypeError(msg)

        for k, v in input.items():
            if not isinstance(v, torch.Tensor):
                msg = f"`preprocessor` needs to return a 'Mapping[str, torch.Tensor]' but detected '{k}' returned by preprocessor is an instance of type {type(v)}."
                raise TypeError(msg)

        with torch.no_grad():
            output = self._model(**input)

        if isinstance(output, torch.Tensor):
            output = output.cpu()

        if self._postprocessor:
            output = self._postprocessor(output, self._context)

            if not isinstance(output, numpy.ndarray):
                msg = (
                    f"`postprocessor` needs to return a 'numpy.ndarray' but detected an instance of type {type(output)}"
                )
                raise TypeError(msg)
        else:
            output = output.numpy()

        return output


def pytorch_model_inference(
    batch: pyarrow.RecordBatch,
    *,
    model: PytorchModelContainer,
    input_columns: List[schema.Column],
    output_column: schema.Column,
    cuda_device: str,
    model_input_schema: List[schema.Column],
) -> pyarrow.RecordBatch:
    with torch.device(cuda_device):
        return _pytorch_model_inference(batch, model, input_columns, output_column, model_input_schema)


def _pytorch_model_inference(
    batch: pyarrow.RecordBatch,
    model: PytorchModelContainer,
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

    output = _pytorch_model_predict(model=model, input_batch=input_batch)
    output = _convert_pytorch_to_arrow(output, batch.num_rows, tecton_type_to_pyarrow(output_column.dtype))

    batch_with_results = pyarrow.RecordBatch.from_arrays(
        [*batch.columns, output],
        schema=batch.schema.append(pyarrow.field(output_column.name, output.type)),
    )
    return batch_with_results


def _pytorch_model_predict(
    model: PytorchModelContainer, input_batch: pyarrow.RecordBatch, recursion_level: int = 0
) -> numpy.ndarray:
    try:
        return model.predict(input_batch)
    except torch.cuda.OutOfMemoryError as oom_exc:
        logger.warning(torch.cuda.memory_summary())
        logger.warning(f"Out of Memory. {oom_exc}\n")
        execution_utils.gc_all(torch.cuda.current_device())
    return _pytorch_model_predict_with_bisect(model=model, input_batch=input_batch, recursion_level=recursion_level + 1)


def _pytorch_model_predict_with_bisect(
    model: PytorchModelContainer, input_batch: pyarrow.RecordBatch, recursion_level: int
) -> numpy.ndarray:
    if recursion_level == _MAX_BISECT_RECURSION_LEVEL:
        msg = "Inference is out of memory and out of retries."
        raise TectonInternalError(msg)

    logger.warning(
        f"Attempt {recursion_level}/{_MAX_BISECT_RECURSION_LEVEL} to bisect the input batch and trying again."
    )
    input_size = input_batch.num_rows
    mid_point = input_size // 2

    first_half = input_batch.slice(offset=0, length=mid_point)
    second_half = input_batch.slice(offset=mid_point)
    return numpy.concatenate(
        [
            _pytorch_model_predict(model, first_half, recursion_level),
            _pytorch_model_predict(model, second_half, recursion_level),
        ]
    )


def _convert_pytorch_to_arrow(
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
class PytorchModelInferenceFuncConfig:
    _model_dir: str
    _model_file_path: str
    _extra_kwargs: Mapping[str, Any]
    _cuda_device: str

    # Note: _final_kwargs is a late init object.
    _final_kwargs: Optional[Mapping[str, Any]] = None

    @classmethod
    def create(
        cls,
        model_dir: str,
        model_file_path: str,
        cuda_device: str,
        input_columns: List[schema.Column],
        output_column: schema.Column,
        model_input_schema: List[schema.Column],
    ) -> PytorchModelInferenceFuncConfig:
        return cls(
            _model_dir=model_dir,
            _model_file_path=model_file_path,
            _cuda_device=cuda_device,
            _extra_kwargs=MappingProxyType(
                {
                    "cuda_device": cuda_device,
                    "input_columns": input_columns,
                    "output_column": output_column,
                    "model_input_schema": model_input_schema,
                }
            ),
        )

    def load(self):
        model_container = PytorchModelContainer(data_dir=self._model_dir, model_file_path=self._model_file_path)
        with torch.device(self._cuda_device):
            model_container.load()

        self._final_kwargs = MappingProxyType(dict(model=model_container, **self._extra_kwargs))
        return self

    def kwargs(self) -> Mapping[str, Any]:
        if self._final_kwargs is None:
            msg = "`load` must be called prior to calling `kwargs`."
            raise ValueError(msg)
        return self._final_kwargs

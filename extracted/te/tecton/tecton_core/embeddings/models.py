from __future__ import annotations

import random
import types
from dataclasses import dataclass
from logging import getLogger
from typing import Any
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple

import numpy.random
import pyarrow
import pyarrow.compute as pc
import torch
import torch.nn.functional as F
from numpy import typing as np_typing
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import BatchEncoding
from transformers import PretrainedConfig
from transformers import tokenization_utils_base

from tecton_core.embeddings import execution_utils


logger = getLogger(__name__)

_MAX_INFERENCE_ATTEMPTS = 2
# Fraction of GPU memory to use for the token budget estimation.
_MAX_GPU_ALLOCATION = 0.3
_DEFAULT_GPU_TOKEN_BUDGET = 10_000
_DEFAULT_CPU_TOKEN_BUDGET = 1_000
_MAX_TOKENIZATION_LENGTH = 512
_DEFAULT_TORCH_DTYPE = torch.float32
_INPUT_IDS_COL_NAME = "_tecton_internal_input_ids"
_TOKEN_TYPE_IDS_COL_NAME = "_tecton_internal_token_type_ids"
_ATTENTION_MASK_COL_NAME = "_tecton_internal_attention_mask"
INPUT_IDS_COL = "input_ids"
TOKEN_TYPE_IDS_COL = "token_type_ids"
ATTENTION_MASK_COL = "attention_mask"


@dataclass
class InferenceParameters:
    max_input_size: int
    output_size: int
    torch_dtype: torch.dtype
    model_type: str
    _config: PretrainedConfig

    @classmethod
    def from_config(cls, config: PretrainedConfig) -> InferenceParameters:
        return InferenceParameters(
            max_input_size=config.max_position_embeddings or _MAX_TOKENIZATION_LENGTH,
            torch_dtype=config.torch_dtype or _DEFAULT_TORCH_DTYPE,
            output_size=config.hidden_size,
            model_type=config.model_type,
            _config=config,
        )


@dataclass
class ModelContainer:
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase
    model: torch.nn.Module
    config: InferenceParameters

    @classmethod
    def load(cls, filepath: str, device_name: str) -> ModelContainer:
        with torch.device(device_name):
            model = AutoModel.from_pretrained(
                filepath,
                use_safetensors=True,
                use_cache=False,
                local_files_only=True,
                trust_remote_code=False,
            )
            return cls(
                tokenizer=AutoTokenizer.from_pretrained(filepath, trust_remote_code=False),
                model=model.eval(),
                config=InferenceParameters.from_config(model.config),
            )


# Follows pattern from: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
def _mean_pooling(*, token_embeddings: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    input_mask_expanded = attention_mask.unsqueeze(dim=-1).expand(token_embeddings.size()).to(token_embeddings.dtype)
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
    sum_mask = torch.sum(input_mask_expanded, dim=1)
    # NOTE: clamps to 1e-9 to avoid NaN from the division
    return sum_embeddings / torch.clamp(sum_mask, min=1e-9)


def _embed_pytorch_core_logic(
    *,
    encoded_input: Mapping[str, torch.Tensor],
    model: torch.nn.Module,
) -> torch.Tensor:
    with torch.no_grad():
        model_output = model(**encoded_input)

    # TODO: encapsulate this as its own nn.Module so we can have a single nn.Module representation of our model.
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    sentence_embeddings = _mean_pooling(
        token_embeddings=token_embeddings, attention_mask=encoded_input[ATTENTION_MASK_COL]
    )
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
    return sentence_embeddings


def _embed_pytorch_core_logic_with_bisect(
    *,
    encoded_input: Mapping[str, torch.Tensor],
    model: torch.nn.Module,
) -> torch.Tensor:
    # All tensors should have the same size at this point.
    mid_point = len(encoded_input[INPUT_IDS_COL].size()) // 2

    first_chunk, second_chunk = {}, {}

    for key, value in encoded_input.items():
        first_half, second_half = value[:mid_point], value[mid_point:]
        first_chunk[key] = first_half
        second_chunk[key] = second_half

    return torch.cat(
        [
            _embed_pytorch_core_logic(encoded_input=first_chunk, model=model),
            _embed_pytorch_core_logic(encoded_input=second_chunk, model=model),
        ]
    )


def _embed_pytorch_core_logic_with_retries(
    *,
    encoded_input: Mapping[str, torch.Tensor],
    model: torch.nn.Module,
    max_attempts: int = _MAX_INFERENCE_ATTEMPTS,
) -> torch.Tensor:
    while max_attempts > 0:
        max_attempts -= 1
        try:
            return _embed_pytorch_core_logic(encoded_input=encoded_input, model=model)
        except torch.cuda.OutOfMemoryError as oom_exc:
            logger.warning(torch.cuda.memory_summary())
            logger.warning(f"Out of Memory. {oom_exc}\n Trying again {max_attempts} more time(s).")
            execution_utils.gc_all(torch.cuda.current_device())
            if max_attempts == 0:
                break
    logger.warning("Failed to embed strings after multiple attempts. Bisecting batch and trying again.")
    return _embed_pytorch_core_logic_with_bisect(encoded_input=encoded_input, model=model)


def _convert_pytorch_to_arrow(sentence_embeddings: torch.Tensor, num_nulls_end: int = 0) -> pyarrow.Array:
    if len(sentence_embeddings.shape) != 2:
        msg = f"Cannot convert torch.Tensor of shape: {sentence_embeddings.shape}, must be a 2d tensor."
        raise ValueError(msg)
    if sentence_embeddings.dtype != torch.float32:
        msg = f"Cannot convert torch.Tensor of dtype: {sentence_embeddings.dtype}, must be torch.float32."
        raise ValueError(msg)

    sentence_embeddings = sentence_embeddings.cpu().numpy()

    # NOTE: we need to convert our sentence_embeddings to a list and pad it with any nulls.
    sentence_embeddings = [*sentence_embeddings, *(None for _ in range(num_nulls_end))]

    # NOTE: using dynamic sized pyarrow list due to https://github.com/apache/arrow/issues/35697
    return pyarrow.array(list(sentence_embeddings), type=pyarrow.list_(pyarrow.float32()))


def _random_string(tokenizer: tokenization_utils_base.PreTrainedTokenizerBase, max_tokens_in_string: int) -> str:
    num_tokens = numpy.random.randint(3, max_tokens_in_string)
    random_token_ids = numpy.random.randint(0, tokenizer.vocab_size, size=num_tokens)
    tokens = tokenizer.convert_ids_to_tokens(random_token_ids)
    return tokenizer.convert_tokens_to_string(tokens)


def _record_batch_from_vocab(
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase, tokens_per_line: int, rows: int, column_name: str
) -> pyarrow.RecordBatch:
    text_array = []
    vocab = list(tokenizer.get_vocab().keys())
    # TODO replace below with _random_string once we use tokenization before batching
    for i in range(rows):
        text_array.append(
            {column_name: " ".join([random.choice(vocab) for _ in range(random.randint(3, tokens_per_line))])}
        )
    schema = pyarrow.schema([pyarrow.field(column_name, pyarrow.string())])
    return pyarrow.RecordBatch.from_pylist(text_array, schema=schema)


def _embed_pytorch(
    *,
    batch: pyarrow.RecordBatch,
    model: torch.nn.Module,
    input_column_name: str,
    output_column_name: str,
) -> pyarrow.RecordBatch:
    input_column = batch.column(input_column_name)
    null_index = pc.index(pc.is_null(input_column), pyarrow.scalar(True)).as_py()

    if null_index == 0:
        # NOTE: this case means that they are all null! Short circuit and create the embeddings directly.
        sentence_embeddings = pyarrow.nulls(len(input_column), pyarrow.list_(pyarrow.float32()))
    elif null_index > -1:
        # No batch contains null value after non-null value.
        # The rule is last microbatch always only has null values. Any microbatch before the last one should not have any null value.
        msg = "Unexpected non-null value in the null value microbatch"
        raise ValueError(msg)
    else:
        input_ids = torch.tensor(batch.column(_INPUT_IDS_COL_NAME).to_pylist())
        token_type_ids = torch.tensor(batch.column(_TOKEN_TYPE_IDS_COL_NAME).to_pylist())
        attention_mask = torch.tensor(batch.column(_ATTENTION_MASK_COL_NAME).to_pylist())

        encoded_input = {
            INPUT_IDS_COL: input_ids,
            TOKEN_TYPE_IDS_COL: token_type_ids,
            ATTENTION_MASK_COL: attention_mask,
        }

        sentence_embeddings = _embed_pytorch_core_logic_with_retries(encoded_input=encoded_input, model=model)

        sentence_embeddings = _convert_pytorch_to_arrow(sentence_embeddings)

    columns_to_drop = [_INPUT_IDS_COL_NAME, _TOKEN_TYPE_IDS_COL_NAME, _ATTENTION_MASK_COL_NAME]
    remaining_columns = [batch.column(col_name) for col_name in batch.schema.names if col_name not in columns_to_drop]
    remaing_schema = pyarrow.schema(
        [batch.schema.field(col_name) for col_name in batch.schema.names if col_name not in columns_to_drop]
    )
    batch_with_results = pyarrow.RecordBatch.from_arrays(
        [*remaining_columns, sentence_embeddings],
        schema=remaing_schema.append(pyarrow.field(output_column_name, sentence_embeddings.type)),
    )
    return batch_with_results


def _token_budget_from_tokens(tokens: BatchEncoding) -> int:
    total_tokens = 0
    for i in range(len(tokens.items())):
        total_tokens += len(tokens.tokens(i))
    return total_tokens


def embed_pytorch(
    batch: pyarrow.RecordBatch,
    *,
    model: ModelContainer,
    input_column_name: str,
    output_column_name: str,
    cuda_device: str,
) -> pyarrow.RecordBatch:
    with torch.device(cuda_device):
        results = _embed_pytorch(
            batch=batch,
            model=model.model,
            input_column_name=input_column_name,
            output_column_name=output_column_name,
        )
    return results


def _estimate_token_budget_for_gpu(
    inference_info: Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]],
) -> int:
    """
    Estimate the token budget for a given model on a GPU by running inference on a small batch of data that is
    generated from the token vocabulary in the model's vocabulary. The amount of memory used on the GPU for that small
    batch is then used to infer the amount of memory that would be used by a larger batch and worked back into a
    token budget.

    This method is not perfect and has some limitations:
    * The method to estimate the number of tokens from a string's length get more inaccurate as the strings gets shorter,
    due small strings having a less consistent number of tokens per character.
    * A small increase in the number of tokens can dramatically increase the size of the array due to padding, thereby
      increasing the memory usage.
    * GPU_MEMORY_FRACTION is set to a lower number since the number of tokens per line is determined by the line that
      expands to the most tokens.
    """
    inference_func, inference_config = inference_info
    inference_kwargs = inference_config[0].load().kwargs()
    model_container: ModelContainer = inference_kwargs["model"]
    input_column_name = inference_kwargs["input_column_name"]
    batches_to_estimate = 3
    synthetic_batch = _record_batch_from_vocab(model_container.tokenizer, 300, 10000, input_column_name)
    batches = list(
        dynamic_token_batching(
            synthetic_batch,
            token_budget=_DEFAULT_GPU_TOKEN_BUDGET,
            column_name=input_column_name,
            tokenizer=model_container.tokenizer,
            max_input_size=model_container.config.max_input_size,
        )
    )
    print("Estimating token budget for GPU.")
    with torch.device("cuda:0"):
        budgets = []
        for dynamic_batch in batches[:batches_to_estimate]:
            memory_tracker = execution_utils.CudaMemoryTracker("cuda:0")
            with memory_tracker:
                _embed_pytorch(
                    batch=dynamic_batch,
                    model=inference_kwargs["model"].model,
                    input_column_name=inference_kwargs["input_column_name"],
                    output_column_name=inference_kwargs["output_column_name"],
                )
            # See doc string for explanation of the formula
            memory_usage = memory_tracker.get_usage_data()
            max_token_budget = memory_usage.max_token_budget_from_mem_alloc(_DEFAULT_GPU_TOKEN_BUDGET)
            estimated_safe_token_budget = int(max_token_budget * _MAX_GPU_ALLOCATION)
            budgets.append(estimated_safe_token_budget)
        print(f"Estimated token budgets: {budgets}, using {min(budgets)} as the budget.")
        return min(budgets)


def estimate_token_budget(
    inference: Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]],
    device_type: str,
) -> int:
    if device_type == "cpu":
        print(
            f"No estimation method implemented for CPU, using default CPU token budget of {_DEFAULT_CPU_TOKEN_BUDGET}."
        )
        return _DEFAULT_CPU_TOKEN_BUDGET
    else:
        try:
            token_budget = _estimate_token_budget_for_gpu(inference)
            if token_budget <= 0:
                msg = "Token budget estimation returned a negative value."
                raise ValueError(msg)
            return token_budget
        except Exception as e:
            logger.warning(f"Failed to estimate token budget for GPU: {e}")
            return _DEFAULT_GPU_TOKEN_BUDGET


@dataclass
class EmbedPytorchFuncConfig:
    _model_filename: str
    _cuda_device: str
    _extra_kwargs: Mapping[str, Any]

    # Note: _final_kwargs is a late init object.
    _final_kwargs: Optional[Mapping[str, Any]] = None

    @classmethod
    def create(
        cls, model_filename: str, cuda_device: str, input_column_name: str, output_column_name: str
    ) -> EmbedPytorchFuncConfig:
        return cls(
            _model_filename=model_filename,
            _cuda_device=cuda_device,
            _extra_kwargs=types.MappingProxyType(
                {
                    "cuda_device": cuda_device,
                    "input_column_name": input_column_name,
                    "output_column_name": output_column_name,
                }
            ),
        )

    def load(self):
        model_container = ModelContainer.load(self._model_filename, device_name=self._cuda_device)
        self._final_kwargs = types.MappingProxyType(dict(model=model_container, **self._extra_kwargs))
        return self

    def kwargs(self) -> Mapping[str, Any]:
        if self._final_kwargs is None:
            msg = "`load` must be called prior to calling `kwargs`."
            raise ValueError(msg)
        return self._final_kwargs


def dynamic_token_batching(
    batch: pyarrow.RecordBatch,
    *,
    token_budget: int,
    column_name: str,
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase,
    max_input_size: int,
) -> Iterator[pyarrow.RecordBatch]:
    """Split the batch into a set of microbatches.

    The logic for the split is as follows:
    1. split the batch into non-null batch and null batch
    2. if non-null batch has rows:
        a. tokenize the input column in the non-null batch
        b. the data should be sorted according to token count of the tokenized input column
        c. calculate the number of rows that can fit within our token budget w/ padding
        d. build the microbatch and yield it while maintaining other data in those rows
    3. if null batch has rows, yield the null batch as the last microbatch
    """

    batch, null_batch = _split_batch_by_null_value(batch, column_name)

    if batch.num_rows > 0:
        col = batch.column(column_name)
        encoded_col = tokenizer(col.to_pylist(), truncation=True, max_length=max_input_size)

        input_ids = numpy.array([numpy.array(seq) for seq in encoded_col[INPUT_IDS_COL]], dtype=object)
        token_type_ids = numpy.array([numpy.array(seq) for seq in encoded_col[TOKEN_TYPE_IDS_COL]], dtype=object)
        attention_mask = numpy.array([numpy.array(seq) for seq in encoded_col[ATTENTION_MASK_COL]], dtype=object)

        lengths = numpy.fromiter(map(len, input_ids), dtype=int)
        sorted_indices = numpy.argsort(lengths)[::-1]

        index = 0
        while index < batch.num_rows:
            max_token_count = lengths[sorted_indices[index]]

            #  Calculate the number of rows we can support according to our token budget (assumes padding)
            #  This is simply `budget // max_token_count` since our data is sorted by length desc.
            #  NOTE: we ensure that we always take one item in the case that our token budget is smaller than
            #  a single row.
            num_rows = max((token_budget // max_token_count), 1)
            end = min(index + num_rows, batch.num_rows)
            microbatch_indices = sorted_indices[index:end]

            input_ids_microbatch = _pad_batch_to_length(
                input_ids.take(microbatch_indices, axis=0), max_token_count, tokenizer.pad_token_type_id
            )
            token_type_ids_microbatch = _pad_batch_to_length(
                token_type_ids.take(microbatch_indices, axis=0), max_token_count, tokenizer.pad_token_type_id
            )
            attention_mask_microbatch = _pad_batch_to_length(
                attention_mask.take(microbatch_indices, axis=0), max_token_count, tokenizer.pad_token_type_id
            )

            microbatch = batch.take(microbatch_indices)

            new_columns = [
                pyarrow.array(input_ids_microbatch),
                pyarrow.array(token_type_ids_microbatch),
                pyarrow.array(attention_mask_microbatch),
            ]
            new_schemas = [
                pyarrow.field(_INPUT_IDS_COL_NAME, pyarrow.list_(pyarrow.int64())),
                pyarrow.field(_TOKEN_TYPE_IDS_COL_NAME, pyarrow.list_(pyarrow.int64())),
                pyarrow.field(_ATTENTION_MASK_COL_NAME, pyarrow.list_(pyarrow.int64())),
            ]
            microbatch = pyarrow.RecordBatch.from_arrays(
                [*microbatch.columns, *new_columns],
                schema=pyarrow.schema(list(microbatch.schema) + new_schemas),
            )
            yield microbatch
            index = end

    if null_batch.num_rows > 0:
        yield null_batch


def _split_batch_by_null_value(
    batch: pyarrow.RecordBatch, column_name: str
) -> Tuple[pyarrow.RecordBatch, pyarrow.RecordBatch]:
    column = batch.column(column_name)
    null_filter = pc.is_null(column)
    non_null_filter = pc.invert(null_filter)

    null_batch = batch.filter(null_filter)
    non_null_batch = batch.filter(non_null_filter)

    return non_null_batch, null_batch


def _pad_batch_to_length(
    batch: np_typing.ArrayLike, max_length: int, padding_value: int, padding_side: str = "right"
) -> np_typing.ArrayLike:
    return [_pad_tokens_to_length(tokens, max_length, padding_value, padding_side) for tokens in batch]


def _pad_tokens_to_length(
    tokens: np_typing.ArrayLike, max_length: int, padding_value: int, padding_side: str = "right"
) -> np_typing.ArrayLike:
    if padding_side == "right":
        pad_width = (0, max_length - len(tokens))
    else:
        pad_width = (max_length - len(tokens), 0)

    return numpy.pad(tokens, pad_width, mode="constant", constant_values=padding_value)


@dataclass
class DynamicBatchingFuncConfig:
    _model_filename: str
    _token_budget: int
    _column_name: str

    # Note: _final_kwargs is a late init object.
    _final_kwargs: Optional[Mapping[str, Any]] = None

    @classmethod
    def create(cls, token_budget: int, column_name: str, model_filename: str) -> DynamicBatchingFuncConfig:
        return cls(_token_budget=token_budget, _column_name=column_name, _model_filename=model_filename)

    def load(self):
        model_container = ModelContainer.load(self._model_filename, device_name="cpu")
        self._final_kwargs = types.MappingProxyType(
            {
                "token_budget": self._token_budget,
                "column_name": self._column_name,
                "tokenizer": model_container.tokenizer,
                "max_input_size": model_container.config.max_input_size,
            }
        )
        return self

    def kwargs(self) -> Mapping[str, Any]:
        if self._final_kwargs is None:
            msg = "`load` must be called prior to calling `kwargs`."
            raise ValueError(msg)
        return self._final_kwargs

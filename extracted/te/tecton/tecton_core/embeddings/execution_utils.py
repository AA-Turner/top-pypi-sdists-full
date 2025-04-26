from __future__ import annotations

import dataclasses
import gc
import sys
import traceback
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Union

import pyarrow.parquet


if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

if sys.version_info >= (3, 10):
    from typing import Concatenate
    from typing import ParamSpec
else:
    from typing_extensions import Concatenate
    from typing_extensions import ParamSpec


# NOTE [ Python Traceback Reference Cycle Problem ]
#
# When using sys.exc_info(), it is important to **not** store the exc_info[2],
# which is the traceback, because otherwise you will run into the traceback
# reference cycle problem, i.e., the traceback holding reference to the frame,
# and the frame (which holds reference to all the object in its temporary scope)
# holding reference the traceback.
#  https://github.com/python/cpython/issues/75188


class KeyErrorMessage(str):
    r"""str subclass that returns itself in repr"""

    def __repr__(self):
        return self


class ExceptionWrapper:
    """Wraps an exception and traceback for exception handling in a multi-threaded execution setting."""

    def __init__(self, exc_info=None, where="in background"):
        # It is important that we don't store exc_info, see
        # NOTE [ Python Traceback Reference Cycle Problem ]
        if exc_info is None:
            exc_info = sys.exc_info()
        self.exc_type = exc_info[0]
        self.exc_msg = "".join(traceback.format_exception(*exc_info))
        self.where = where

    def reraise(self):
        r"""Reraises the wrapped exception in the current thread"""
        # Format a message such as: "Caught ValueError in DataLoader worker
        # process 2. Original Traceback:", followed by the traceback.
        msg = f"Caught {self.exc_type.__name__} {self.where}.\nOriginal {self.exc_msg}"
        if self.exc_type is KeyError:
            # KeyError calls repr() on its argument (usually a dict key). This
            # makes stack traces unreadable. It will not be changed in Python
            # (https://github.com/python/cpython/issues/46903), so we work around it.
            msg = KeyErrorMessage(msg)
        elif getattr(self.exc_type, "message", None):
            # Some exceptions have first argument as non-str but explicitly
            # have message field
            raise self.exc_type(message=msg)
        try:
            exception = self.exc_type(msg)
        except TypeError:
            # If the exception takes multiple arguments, don't try to
            # instantiate since we don't know how to
            raise RuntimeError(msg) from None
        raise exception


Item = Union[pyarrow.RecordBatch, ExceptionWrapper]
P = ParamSpec("P")
PreprocessorCallable = Callable[Concatenate[Item, P], Iterable[Item]]
ModelCallable = Callable[Concatenate[Item, P], Item]


def data_preprocessor_one_step(item: Item, func: PreprocessorCallable, func_kwargs: P.kwargs) -> Iterable[Item]:
    if isinstance(item, ExceptionWrapper):
        return (item,)

    try:
        return func(item, **func_kwargs)
    except Exception:
        return (ExceptionWrapper(where="in data preprocessor"),)


def model_inference_one_step(item: Item, func: ModelCallable, func_kwargs: P.kwargs) -> Item:
    if isinstance(item, ExceptionWrapper):
        return item

    try:
        return func(item, **func_kwargs)
    except Exception:
        return ExceptionWrapper(where="in model inference")


class FuncConfig(Protocol):
    def load(self) -> FuncConfig: ...

    def kwargs(self) -> Mapping[str, Any]: ...


def gc_all(device: Optional[Union[str, int]] = None) -> None:
    """
    Run the garbage collector for the main thread and the GPU
    """
    # Python GC before cleaning up GPU memory to ensure that we release
    # unreferenced PyTorch tensors.
    import torch

    gc.collect()
    if torch.cuda.is_available():
        if device is not None:
            with torch.cuda.device(device):
                torch.cuda.empty_cache()


@dataclasses.dataclass
class CudaMemoryUsageData:
    # Memory allocated before measurements started
    starting_alloc_bytes: int
    # Peak allocated memory during the measurement period
    max_alloc_bytes: int
    # Memory allocated during the measurement period. max_alloc - starting_alloc
    new_alloc_bytes: int
    # Device memory - starting_alloc
    starting_free_memory_bytes: int
    # The total memory on the device
    device_memory_bytes: int
    # Map of memory stats provided by torch.cuda.memory_stats
    _memory_stats: Mapping[str, Any]

    def max_token_budget_from_mem_alloc(self, sample_token_budget: int) -> int:
        """
        1. Calculates what proportion of available memory was allocated during the execution
        2. Calculates how of those "sample batches" would fit into available memory
        3. Multiplies the token budget of the sample batch by how many batches would've fit into memory
        """
        proportion_of_free_memory_allocated = self.new_alloc_bytes / self.starting_free_memory_bytes
        token_budget_multiplier = 1 / proportion_of_free_memory_allocated
        return int(sample_token_budget * token_budget_multiplier)


class CudaMemoryTracker:
    def __init__(self, device: Optional[str] = None) -> None:
        import torch

        self.device = device if device is not None else torch.cuda.current_device()
        self._data: Optional[CudaMemoryUsageData] = None
        self._device_memory = None
        self._starting_alloc = None
        self._starting_free_memory = None

    def __enter__(self) -> "CudaMemoryTracker":
        import torch

        gc_all(self.device)
        torch.cuda.reset_peak_memory_stats(self.device)
        self._device_memory = torch.cuda.get_device_properties(self.device).total_memory
        self._starting_alloc = torch.cuda.memory_allocated(self.device)
        self._starting_free_memory = self._device_memory - self._starting_alloc
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import torch

        torch.cuda.synchronize(self.device)
        self._data = CudaMemoryUsageData(
            starting_free_memory_bytes=self._starting_free_memory,
            starting_alloc_bytes=self._starting_alloc,
            max_alloc_bytes=torch.cuda.max_memory_allocated(self.device),
            new_alloc_bytes=torch.cuda.max_memory_allocated(self.device) - self._starting_alloc,
            device_memory_bytes=self._device_memory,
            _memory_stats=torch.cuda.memory_stats(self.device),
        )

    def get_usage_data(self) -> CudaMemoryUsageData:
        if self._data is None:
            msg = "CudaMemoryTracker was not properly exited"
            raise RuntimeError(msg)
        return self._data

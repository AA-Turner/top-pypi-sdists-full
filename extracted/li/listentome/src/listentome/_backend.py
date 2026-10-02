from __future__ import annotations

from collections.abc import Callable
from typing import Literal, Protocol, TypeAlias

from ._devices import Device

DType: TypeAlias = Literal["float32", "int32", "int16", "int8", "uint8"]

ITEMSIZE: dict[DType, int] = {"float32": 4, "int32": 4, "int16": 2, "int8": 1, "uint8": 1}

StreamCallback: TypeAlias = "Callable[[memoryview | None, memoryview | None, int], None]"
"""Called on the audio thread with `(indata, outdata, frames)`.

`indata` is a read-only view of captured bytes (or `None` for output-only streams).
`outdata` is a writable view the callback must fill (or `None` for input-only streams).
"""


class RawStream(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def close(self) -> None: ...


class Backend(Protocol):
    def devices(self) -> list[Device]: ...
    def default_input(self) -> Device | None: ...
    def default_output(self) -> Device | None: ...
    def open(
        self,
        *,
        samplerate: int,
        blocksize: int,
        dtype: DType,
        input_channels: int,
        output_channels: int,
        input_device: int | None,
        output_device: int | None,
        callback: StreamCallback,
    ) -> RawStream: ...

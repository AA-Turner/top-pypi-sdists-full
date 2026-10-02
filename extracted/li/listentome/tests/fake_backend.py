from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

from listentome import Device, DType, StreamCallback


@dataclass
class FakeRawStream:
    callback: StreamCallback
    input_bytes: int
    output_bytes: int
    frames: int
    interval: float
    started: bool = False
    closed: bool = False
    written: bytearray = field(default_factory=bytearray)
    _thread: threading.Thread | None = None
    _stop: threading.Event = field(default_factory=threading.Event)

    def start(self) -> None:
        self.started = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            indata = memoryview(bytes(self.input_bytes)).toreadonly() if self.input_bytes else None
            outbuf = bytearray(self.output_bytes)
            outdata = memoryview(outbuf) if self.output_bytes else None
            self.callback(indata, outdata, self.frames)
            self.written.extend(outbuf)
            time.sleep(self.interval)

    def stop(self) -> None:
        self._stop.set()

    def close(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join()
        self.closed = True


@dataclass
class FakeBackend:
    device_list: list[Device] = field(
        default_factory=lambda: [
            Device(index=0, name="Fake Mic", max_input_channels=2, max_output_channels=0, default_samplerate=48000.0),
            Device(
                index=1, name="Fake Speaker", max_input_channels=0, max_output_channels=2, default_samplerate=48000.0
            ),
        ]
    )
    interval: float = 0.001
    streams: list[FakeRawStream] = field(default_factory=list)

    def devices(self) -> list[Device]:
        return self.device_list

    def default_input(self) -> Device | None:
        return next((d for d in self.device_list if d.max_input_channels), None)

    def default_output(self) -> Device | None:
        return next((d for d in self.device_list if d.max_output_channels), None)

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
    ) -> FakeRawStream:
        from listentome._backend import ITEMSIZE

        itemsize = ITEMSIZE[dtype]
        stream = FakeRawStream(
            callback=callback,
            input_bytes=blocksize * input_channels * itemsize,
            output_bytes=blocksize * output_channels * itemsize,
            frames=blocksize,
            interval=self.interval,
        )
        self.streams.append(stream)
        return stream

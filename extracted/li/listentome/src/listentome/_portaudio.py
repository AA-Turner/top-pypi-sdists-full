from __future__ import annotations

import ctypes.util
import threading
from typing import Any

from cffi import FFI

from ._backend import ITEMSIZE, DType, StreamCallback
from ._devices import Device
from ._exceptions import PortAudioError

_CDEF = """
typedef int PaError;
typedef int PaDeviceIndex;
typedef int PaHostApiIndex;
typedef double PaTime;
typedef unsigned long PaSampleFormat;
typedef unsigned long PaStreamFlags;
typedef void PaStream;

typedef struct PaDeviceInfo {
    int structVersion;
    const char *name;
    PaHostApiIndex hostApi;
    int maxInputChannels;
    int maxOutputChannels;
    PaTime defaultLowInputLatency;
    PaTime defaultLowOutputLatency;
    PaTime defaultHighInputLatency;
    PaTime defaultHighOutputLatency;
    double defaultSampleRate;
} PaDeviceInfo;

typedef struct PaStreamParameters {
    PaDeviceIndex device;
    int channelCount;
    PaSampleFormat sampleFormat;
    PaTime suggestedLatency;
    void *hostApiSpecificStreamInfo;
} PaStreamParameters;

typedef struct PaStreamCallbackTimeInfo {
    PaTime inputBufferAdcTime;
    PaTime currentTime;
    PaTime outputBufferDacTime;
} PaStreamCallbackTimeInfo;

typedef unsigned long PaStreamCallbackFlags;

typedef int PaStreamCallback(
    const void *input, void *output, unsigned long frameCount,
    const PaStreamCallbackTimeInfo *timeInfo,
    PaStreamCallbackFlags statusFlags, void *userData);

PaError Pa_Initialize(void);
PaError Pa_Terminate(void);
const char *Pa_GetErrorText(PaError errorCode);
PaDeviceIndex Pa_GetDeviceCount(void);
PaDeviceIndex Pa_GetDefaultInputDevice(void);
PaDeviceIndex Pa_GetDefaultOutputDevice(void);
const PaDeviceInfo *Pa_GetDeviceInfo(PaDeviceIndex device);
PaError Pa_OpenStream(
    PaStream **stream,
    const PaStreamParameters *inputParameters,
    const PaStreamParameters *outputParameters,
    double sampleRate,
    unsigned long framesPerBuffer,
    PaStreamFlags streamFlags,
    PaStreamCallback *streamCallback,
    void *userData);
PaError Pa_StartStream(PaStream *stream);
PaError Pa_StopStream(PaStream *stream);
PaError Pa_CloseStream(PaStream *stream);
"""

_SAMPLE_FORMATS: dict[DType, int] = {
    "float32": 0x00000001,
    "int32": 0x00000002,
    "int16": 0x00000008,
    "int8": 0x00000010,
    "uint8": 0x00000020,
}

_PA_CONTINUE = 0


_LIBRARY_CANDIDATES = (
    "/opt/homebrew/lib/libportaudio.dylib",
    "/usr/local/lib/libportaudio.dylib",
    "libportaudio.so.2",
)


def _load_library(ffi: FFI) -> Any:
    name = ctypes.util.find_library("portaudio")
    candidates = (name,) + _LIBRARY_CANDIDATES if name else _LIBRARY_CANDIDATES
    for candidate in candidates:
        try:
            return ffi.dlopen(candidate)
        except OSError:
            continue
    raise PortAudioError("PortAudio library not found; install it (e.g. `brew install portaudio`)")


class PortAudioBackend:
    def __init__(self) -> None:
        self._ffi = FFI()
        self._ffi.cdef(_CDEF)
        self._lib = _load_library(self._ffi)
        self._check(self._lib.Pa_Initialize())

    def _check(self, code: int) -> None:
        if code < 0:
            message = self._ffi.string(self._lib.Pa_GetErrorText(code)).decode()
            raise PortAudioError(message)

    def _device(self, index: int) -> Device:
        info = self._lib.Pa_GetDeviceInfo(index)
        return Device(
            index=index,
            name=self._ffi.string(info.name).decode(errors="replace"),
            max_input_channels=info.maxInputChannels,
            max_output_channels=info.maxOutputChannels,
            default_samplerate=info.defaultSampleRate,
        )

    def devices(self) -> list[Device]:
        count = self._lib.Pa_GetDeviceCount()
        self._check(count)
        return [self._device(i) for i in range(count)]

    def default_input(self) -> Device | None:
        index = self._lib.Pa_GetDefaultInputDevice()
        return self._device(index) if index >= 0 else None

    def default_output(self) -> Device | None:
        index = self._lib.Pa_GetDefaultOutputDevice()
        return self._device(index) if index >= 0 else None

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
    ) -> _PortAudioStream:
        ffi, lib = self._ffi, self._lib
        itemsize = ITEMSIZE[dtype]

        def resolve(device: int | None, default: int) -> int:
            return device if device is not None else default

        in_params = ffi.NULL
        if input_channels:
            in_params = ffi.new("PaStreamParameters *")
            in_params.device = resolve(input_device, lib.Pa_GetDefaultInputDevice())
            in_params.channelCount = input_channels
            in_params.sampleFormat = _SAMPLE_FORMATS[dtype]
            in_params.suggestedLatency = lib.Pa_GetDeviceInfo(in_params.device).defaultLowInputLatency
            in_params.hostApiSpecificStreamInfo = ffi.NULL

        out_params = ffi.NULL
        if output_channels:
            out_params = ffi.new("PaStreamParameters *")
            out_params.device = resolve(output_device, lib.Pa_GetDefaultOutputDevice())
            out_params.channelCount = output_channels
            out_params.sampleFormat = _SAMPLE_FORMATS[dtype]
            out_params.suggestedLatency = lib.Pa_GetDeviceInfo(out_params.device).defaultLowOutputLatency
            out_params.hostApiSpecificStreamInfo = ffi.NULL

        @ffi.callback("PaStreamCallback")  # type: ignore[untyped-decorator]
        def c_callback(
            input_ptr: Any, output_ptr: Any, frames: int, time_info: Any, status: Any, user_data: Any
        ) -> int:
            indata = None
            if input_ptr != ffi.NULL:
                indata = memoryview(ffi.buffer(input_ptr, frames * input_channels * itemsize)).toreadonly()
            outdata = None
            if output_ptr != ffi.NULL:
                outdata = memoryview(ffi.buffer(output_ptr, frames * output_channels * itemsize))
            callback(indata, outdata, frames)
            return _PA_CONTINUE

        stream_ptr = ffi.new("PaStream **")
        self._check(
            lib.Pa_OpenStream(stream_ptr, in_params, out_params, float(samplerate), blocksize, 0, c_callback, ffi.NULL)
        )
        return _PortAudioStream(self, stream_ptr[0], c_callback)


class _PortAudioStream:
    def __init__(self, backend: PortAudioBackend, stream: Any, keepalive: Any) -> None:
        self._backend = backend
        self._stream = stream
        self._keepalive = keepalive
        self._lock = threading.Lock()
        self._closed = False

    def start(self) -> None:
        self._backend._check(self._backend._lib.Pa_StartStream(self._stream))

    def stop(self) -> None:
        self._backend._check(self._backend._lib.Pa_StopStream(self._stream))

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
        self._backend._check(self._backend._lib.Pa_CloseStream(self._stream))


_default_backend: PortAudioBackend | None = None
_default_backend_lock = threading.Lock()


def default_backend() -> PortAudioBackend:
    global _default_backend
    with _default_backend_lock:
        if _default_backend is None:
            _default_backend = PortAudioBackend()
        return _default_backend

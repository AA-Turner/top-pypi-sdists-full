"""Explicit PCM16 WAV decoding and file-reference publication for selected recordings."""

import math
import struct
import wave
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from labqoat.references import AssetRef
from labqoat.storage.asset_publisher import AssetPublisher
from labqoat.storage.file_access import FileAccess


@dataclass(frozen=True, slots=True)
class Audio:
    """Finite interleaved samples with explicit sample rate and channel count."""

    samples: tuple[float, ...]
    sample_rate: int
    channels: int = 1

    def __post_init__(self) -> None:
        """Reject ambiguous shape and nonfinite waveforms before consumption."""
        if self.sample_rate < 1 or self.channels < 1 or len(self.samples) % self.channels:
            raise ValueError("Audio requires a positive rate, channels and complete interleaved frames")
        if not all(math.isfinite(sample) for sample in self.samples):
            raise ValueError("Audio samples must be finite")

    @classmethod
    def load(cls, reference: AssetRef | Mapping[str, object], assets: FileAccess) -> "Audio":
        """Acquire and decode one selected recording, releasing its lease after decoding."""
        with assets.local_file(reference) as path:
            return cls.read_wav(path)

    @classmethod
    def read_wav(cls, path: Path, *, start_frame: int = 0, frames: int | None = None) -> "Audio":
        """Decode at most 16 million selected PCM16 frames without implicit resampling."""
        with wave.open(str(path), "rb") as stream:
            if stream.getsampwidth() != 2 or stream.getcomptype() != "NONE":
                raise ValueError("Audio helper requires PCM16 WAV; use your decoder for other codecs")
            available = stream.getnframes() - start_frame
            count = available if frames is None else frames
            if start_frame < 0 or count < 0 or count > available or count > 16_000_000:
                raise ValueError("Requested audio frames exceed the recording or decoding limit")
            stream.setpos(start_frame)
            raw = stream.readframes(count)
            if len(raw) != count * stream.getnchannels() * 2:
                raise ValueError("Truncated WAV frames")
            samples = tuple(value[0] / 32768.0 for value in struct.iter_unpack("<h", raw))
            return cls(samples, stream.getframerate(), stream.getnchannels())

    def write_wav(self, path: Path) -> None:
        """Encode clipped PCM16 in bounded chunks while preserving rate and channels."""
        with wave.open(str(path), "wb") as stream:
            stream.setnchannels(self.channels)
            stream.setsampwidth(2)
            stream.setframerate(self.sample_rate)
            for start in range(0, len(self.samples), 65536):
                samples = self.samples[start : start + 65536]
                values = (max(-32768, min(32767, round(sample * 32768))) for sample in samples)
                stream.writeframesraw(struct.pack(f"<{len(samples)}h", *values))

    def publish_wav(self, publisher: AssetPublisher) -> AssetRef:
        """Return a durable immutable reference using the execution host's output capability."""
        with TemporaryDirectory(prefix="labqoat-audio-") as directory:
            path = Path(directory) / "audio.wav"
            self.write_wav(path)
            return publisher.publish(path, media_type="audio/wav")

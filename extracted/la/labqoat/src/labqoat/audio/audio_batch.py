"""Framework-neutral padding with original frame lengths for selected audio batches."""

from collections.abc import Sequence
from dataclasses import dataclass

from labqoat.audio.audio import Audio


@dataclass(frozen=True, slots=True)
class AudioBatch:
    """Padded interleaved recordings and frame lengths suitable for loader collation."""

    samples: tuple[tuple[float, ...], ...]
    frame_lengths: tuple[int, ...]
    sample_rate: int
    channels: int

    @classmethod
    def pad(cls, recordings: Sequence[Audio]) -> "AudioBatch":
        """Pad with zeros only after the sampler-selected recordings have been decoded."""
        if not recordings:
            raise ValueError("Audio batch cannot be empty")
        rate, channels = recordings[0].sample_rate, recordings[0].channels
        if any((audio.sample_rate, audio.channels) != (rate, channels) for audio in recordings):
            raise ValueError("Audio batch requires matching sample rates and channels")
        width = max(len(audio.samples) for audio in recordings)
        samples = tuple(audio.samples + (0.0,) * (width - len(audio.samples)) for audio in recordings)
        return cls(samples, tuple(len(audio.samples) // channels for audio in recordings), rate, channels)

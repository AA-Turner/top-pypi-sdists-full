import numpy as np

from dreadnode.core.exceptions import catch_import_error
from dreadnode.core.transforms import Transform
from dreadnode.core.types import Audio


def _audio_to_numpy(audio: Audio) -> tuple[np.ndarray, int]:
    """
    Convert Audio object to numpy array and sample rate.

    Returns:
        Tuple of (audio_array, sample_rate) where audio_array is float64 in [-1, 1].
    """
    with catch_import_error("dreadnode"):
        import soundfile as sf

    data = audio._data

    if isinstance(data, np.ndarray):
        sample_rate = audio._sample_rate
        if sample_rate is None:
            raise ValueError("Sample rate is required for numpy array audio")
        # Normalize to float64 in [-1, 1]
        if data.dtype in (np.int16, np.int32):
            data = data.astype(np.float64) / np.iinfo(data.dtype).max  # ty: ignore[no-matching-overload]
        elif data.dtype == np.uint8:
            data = (data.astype(np.float64) - 128) / 128  # ty: ignore[no-matching-overload]
        elif data.dtype not in (np.float32, np.float64):
            data = data.astype(np.float64)  # ty: ignore[no-matching-overload]
        return data, sample_rate

    if isinstance(data, str) or hasattr(data, "__fspath__"):
        # File path (str or PathLike)
        audio_data, sample_rate = sf.read(str(data), dtype="float64")
        return audio_data, sample_rate

    if isinstance(data, bytes):
        import io

        audio_data, sample_rate = sf.read(io.BytesIO(data), dtype="float64")
        return audio_data, sample_rate

    raise TypeError(f"Unsupported audio data type: {type(data)}")


def _numpy_to_audio(
    data: np.ndarray,
    sample_rate: int,
    *,
    caption: str | None = None,
    format: str | None = None,
) -> Audio:
    """
    Convert numpy array back to Audio object.

    Args:
        data: Audio samples as numpy array (float in [-1, 1] range).
        sample_rate: Sample rate in Hz.
        caption: Optional caption.
        format: Optional format (default: wav).
    """
    # Clip to valid range
    data = np.clip(data, -1.0, 1.0)
    return Audio(data, sample_rate=sample_rate, caption=caption, format=format or "wav")


# =============================================================================
# Noise Transforms
# =============================================================================


def add_white_noise(
    *,
    snr_db: float = 20.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """
    Add white Gaussian noise to audio at a specified signal-to-noise ratio.

    White noise has equal power across all frequencies and is commonly used
    to test ASR robustness. Higher SNR means cleaner audio.

    Args:
        snr_db: Target signal-to-noise ratio in decibels. Common values:
            - 40 dB: Very clean, noise barely perceptible
            - 20 dB: Noticeable noise, still intelligible
            - 10 dB: Significant noise, challenging for ASR
            - 0 dB: Equal signal and noise power
        seed: Random seed for reproducibility.

    Returns:
        Transform that adds white noise to Audio.

    Reference:
        Standard audio augmentation technique used in SpecAugment and
        other ASR robustness methods.
    """
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, snr_db: float = snr_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Calculate signal power
        signal_power = np.mean(data**2)
        if signal_power == 0:
            return audio

        # Calculate noise power for target SNR
        # SNR_db = 10 * log10(signal_power / noise_power)
        noise_power = signal_power / (10 ** (snr_db / 10))
        noise_std = np.sqrt(noise_power)

        # Generate and add noise
        noise = rng.normal(0, noise_std, data.shape)
        noisy_data = data + noise

        return _numpy_to_audio(noisy_data, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_white_noise", modality="audio")


def add_pink_noise(
    *,
    snr_db: float = 20.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """
    Add pink (1/f) noise to audio at a specified signal-to-noise ratio.

    Pink noise has equal power per octave (power spectral density ∝ 1/f),
    making it sound more natural than white noise. It's commonly found in
    natural and electronic systems.

    Args:
        snr_db: Target signal-to-noise ratio in decibels.
        seed: Random seed for reproducibility.

    Returns:
        Transform that adds pink noise to Audio.

    Reference:
        Pink noise is used in audio testing and masking studies.
        See: Voss & Clarke, "1/f noise in music and speech" (1975).
    """
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, snr_db: float = snr_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Generate pink noise using Voss-McCartney algorithm
        n_samples = data.shape[0]

        # Simple pink noise approximation using filtered white noise
        white = rng.standard_normal(n_samples)

        # Apply 1/f filter in frequency domain
        fft = np.fft.rfft(white)
        freqs = np.fft.rfftfreq(n_samples)
        # Avoid division by zero at DC
        freqs[0] = 1e-10
        # Pink noise: scale by 1/sqrt(f) for power spectrum ∝ 1/f
        fft *= 1 / np.sqrt(freqs)
        pink = np.fft.irfft(fft, n_samples)

        # Normalize and scale to target SNR
        signal_power = np.mean(data**2)
        if signal_power == 0:
            return audio

        noise_power = signal_power / (10 ** (snr_db / 10))
        pink = pink * np.sqrt(noise_power / np.mean(pink**2))

        # Handle stereo
        if data.ndim == 2:
            pink = np.column_stack([pink] * data.shape[1])

        noisy_data = data + pink

        return _numpy_to_audio(noisy_data, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_pink_noise", modality="audio")


# =============================================================================
# Volume/Amplitude Transforms
# =============================================================================


def change_volume(
    *,
    gain_db: float = 0.0,
) -> Transform[Audio, Audio]:
    """
    Change audio volume by a specified gain in decibels.

    Args:
        gain_db: Gain to apply in decibels. Positive values increase volume,
            negative values decrease. Common values:
            - +6 dB: Roughly doubles perceived loudness
            - -6 dB: Roughly halves perceived loudness
            - +20 dB: Very loud (may clip)
            - -20 dB: Very quiet

    Returns:
        Transform that adjusts Audio volume.

    Reference:
        Basic audio augmentation for ASR robustness testing.
        See: Park et al., "SpecAugment" (2019).
    """

    def transform(audio: Audio, *, gain_db: float = gain_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Convert dB to linear gain
        gain_linear = 10 ** (gain_db / 20)
        scaled_data = data * gain_linear

        return _numpy_to_audio(scaled_data, sample_rate, caption=audio._caption)

    return Transform(transform, name="change_volume", modality="audio")


def normalize_volume(
    *,
    target_db: float = -3.0,
) -> Transform[Audio, Audio]:
    """
    Normalize audio to a target peak level in decibels.

    Args:
        target_db: Target peak level in dB relative to full scale (dBFS).
            - 0 dB: Maximum level (may cause clipping with lossy codecs)
            - -3 dB: Common target for headroom
            - -6 dB: Conservative target

    Returns:
        Transform that normalizes Audio to target level.
    """

    def transform(audio: Audio, *, target_db: float = target_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Find current peak
        current_peak = np.max(np.abs(data))
        if current_peak == 0:
            return audio

        # Calculate gain needed
        target_linear = 10 ** (target_db / 20)
        gain = target_linear / current_peak
        normalized_data = data * gain

        return _numpy_to_audio(normalized_data, sample_rate, caption=audio._caption)

    return Transform(transform, name="normalize_volume", modality="audio")


# =============================================================================
# Temporal Transforms
# =============================================================================


def change_speed(
    *,
    rate: float = 1.0,
) -> Transform[Audio, Audio]:
    """
    Change audio playback speed by resampling.

    This affects both tempo and pitch proportionally (like playing a
    vinyl record at the wrong speed). For tempo change without pitch
    change, use time_stretch().

    Args:
        rate: Speed multiplier. Values > 1.0 speed up (shorter duration,
            higher pitch), values < 1.0 slow down (longer, lower pitch).
            - 1.0: No change
            - 2.0: Double speed, one octave higher
            - 0.5: Half speed, one octave lower

    Returns:
        Transform that changes Audio speed.

    Reference:
        Speed perturbation is a standard augmentation technique.
        See: Ko et al., "Audio Augmentation for Speech Recognition" (2015).
    """
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, rate: float = rate) -> Audio:
        if rate <= 0:
            raise ValueError("Rate must be positive")
        if rate == 1.0:
            return audio

        data, sample_rate = _audio_to_numpy(audio)

        # Calculate new number of samples
        original_length = data.shape[0]
        new_length = int(original_length / rate)

        if new_length == 0:
            raise ValueError("Rate too high - would result in empty audio")

        # Resample each channel
        if data.ndim == 1:
            resampled = signal.resample(data, new_length)
        else:
            resampled = np.column_stack(
                [signal.resample(data[:, ch], new_length) for ch in range(data.shape[1])]
            )

        return _numpy_to_audio(resampled, sample_rate, caption=audio._caption)

    return Transform(transform, name="change_speed", modality="audio")


def time_stretch(
    *,
    rate: float = 1.0,
) -> Transform[Audio, Audio]:
    """
    Change audio tempo without affecting pitch using phase vocoder.

    This is a more sophisticated transform that preserves pitch while
    changing duration. Useful for testing ASR systems against speaking
    rate variations.

    Args:
        rate: Time stretch factor. Values > 1.0 make audio shorter (faster
            tempo), values < 1.0 make it longer (slower tempo).
            - 1.0: No change
            - 1.5: 50% faster, same pitch
            - 0.75: 25% slower, same pitch

    Returns:
        Transform that time-stretches Audio.

    Reference:
        Phase vocoder technique. See: Laroche & Dolson,
        "Improved Phase Vocoder Time-Scale Modification of Audio" (1999).
    """
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, rate: float = rate) -> Audio:
        if rate <= 0:
            raise ValueError("Rate must be positive")
        if rate == 1.0:
            return audio

        data, sample_rate = _audio_to_numpy(audio)

        # Phase vocoder parameters
        n_fft = 2048
        hop_length = n_fft // 4

        def _phase_vocoder(y: np.ndarray, rate: float) -> np.ndarray:
            """Apply phase vocoder time stretching to mono signal."""
            # STFT
            _, _, stft = signal.stft(y, fs=sample_rate, nperseg=n_fft, noverlap=n_fft - hop_length)

            # Time stretch in frequency domain
            n_frames = stft.shape[1]
            new_n_frames = int(np.ceil(n_frames / rate))

            # Interpolate magnitude and phase
            time_steps = np.arange(new_n_frames) * rate
            time_steps = np.clip(time_steps, 0, n_frames - 1)

            # Simple linear interpolation of complex STFT
            indices = time_steps.astype(int)
            frac = time_steps - indices
            indices_next = np.minimum(indices + 1, n_frames - 1)

            stretched = stft[:, indices] * (1 - frac) + stft[:, indices_next] * frac

            # ISTFT
            _, reconstructed = signal.istft(
                stretched, fs=sample_rate, nperseg=n_fft, noverlap=n_fft - hop_length
            )

            return reconstructed

        # Apply to each channel
        if data.ndim == 1:
            stretched = _phase_vocoder(data, rate)
        else:
            channels = [_phase_vocoder(data[:, ch], rate) for ch in range(data.shape[1])]
            min_len = min(len(ch) for ch in channels)
            stretched = np.column_stack([ch[:min_len] for ch in channels])

        return _numpy_to_audio(stretched, sample_rate, caption=audio._caption)

    return Transform(transform, name="time_stretch", modality="audio")


def pitch_shift(
    *,
    semitones: float = 0.0,
) -> Transform[Audio, Audio]:
    """
    Shift audio pitch without changing duration.

    Uses time stretching followed by resampling to achieve pitch shift
    while maintaining original duration.

    Args:
        semitones: Pitch shift in semitones (half steps). Positive values
            shift up, negative shift down.
            - 12: One octave up
            - -12: One octave down
            - 7: Perfect fifth up
            - 2: Whole step up

    Returns:
        Transform that pitch-shifts Audio.

    Reference:
        Yakura & Sakuma, "Robust Audio Adversarial Example for a
        Physical Attack" (2019) - pitch shifting as perturbation.
    """
    with catch_import_error("dreadnode"):
        from scipy import signal

    async def transform(audio: Audio, *, semitones: float = semitones) -> Audio:
        if semitones == 0:
            return audio

        data, sample_rate = _audio_to_numpy(audio)
        original_length = data.shape[0]

        # Pitch shift = time stretch + resample
        # To shift pitch up by n semitones, we:
        # 1. Time stretch by 2^(n/12) (make it longer)
        # 2. Resample to original length (speeds up, raising pitch)
        rate = 2 ** (semitones / 12)

        # Time stretch (make longer for pitch up, shorter for pitch down).
        # time_stretch() is an async Transform — must be awaited.
        stretched_audio = await time_stretch(rate=1 / rate)(audio)

        # Get stretched data
        stretched_data, _ = _audio_to_numpy(stretched_audio)

        # Resample back to original length
        if stretched_data.ndim == 1:
            resampled = signal.resample(stretched_data, original_length)
        else:
            resampled = np.column_stack(
                [
                    signal.resample(stretched_data[:, ch], original_length)
                    for ch in range(stretched_data.shape[1])
                ]
            )

        return _numpy_to_audio(resampled, sample_rate, caption=audio._caption)

    return Transform(transform, name="pitch_shift", modality="audio")


# =============================================================================
# Filter Transforms
# =============================================================================


def apply_low_pass_filter(
    *,
    cutoff_hz: float = 4000.0,
    order: int = 5,
) -> Transform[Audio, Audio]:
    """
    Apply a Butterworth low-pass filter to remove high frequencies.

    Low-pass filtering simulates telephone-quality audio or muffled sound.
    Useful for testing ASR robustness to bandwidth-limited audio.

    Args:
        cutoff_hz: Cutoff frequency in Hz. Frequencies above this are attenuated.
            - 8000 Hz: Wideband speech (preserves most speech information)
            - 4000 Hz: Narrowband/telephone quality
            - 2000 Hz: Heavily muffled
        order: Filter order (steepness of cutoff). Higher = steeper.

    Returns:
        Transform that applies low-pass filter to Audio.

    Reference:
        Common audio perturbation for robustness testing.
    """
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, cutoff_hz: float = cutoff_hz, order: int = order) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Nyquist frequency
        nyquist = sample_rate / 2
        if cutoff_hz >= nyquist:
            return audio  # No filtering needed

        # Design Butterworth filter
        normalized_cutoff = cutoff_hz / nyquist
        b, a = signal.butter(order, normalized_cutoff, btype="low")

        # Apply filter
        if data.ndim == 1:
            filtered = signal.filtfilt(b, a, data)
        else:
            filtered = np.column_stack(
                [signal.filtfilt(b, a, data[:, ch]) for ch in range(data.shape[1])]
            )

        return _numpy_to_audio(filtered, sample_rate, caption=audio._caption)

    return Transform(transform, name="apply_low_pass_filter", modality="audio")


def apply_high_pass_filter(
    *,
    cutoff_hz: float = 200.0,
    order: int = 5,
) -> Transform[Audio, Audio]:
    """
    Apply a Butterworth high-pass filter to remove low frequencies.

    High-pass filtering removes bass and rumble. Useful for simulating
    small speakers or removing background noise.

    Args:
        cutoff_hz: Cutoff frequency in Hz. Frequencies below this are attenuated.
            - 80 Hz: Removes sub-bass
            - 200 Hz: Removes bass, thin sound
            - 500 Hz: Removes low-mids, tinny sound
        order: Filter order (steepness of cutoff). Higher = steeper.

    Returns:
        Transform that applies high-pass filter to Audio.
    """
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, cutoff_hz: float = cutoff_hz, order: int = order) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Nyquist frequency
        nyquist = sample_rate / 2
        if cutoff_hz <= 0:
            return audio

        # Design Butterworth filter
        normalized_cutoff = min(cutoff_hz / nyquist, 0.99)  # Avoid instability
        b, a = signal.butter(order, normalized_cutoff, btype="high")

        # Apply filter
        if data.ndim == 1:
            filtered = signal.filtfilt(b, a, data)
        else:
            filtered = np.column_stack(
                [signal.filtfilt(b, a, data[:, ch]) for ch in range(data.shape[1])]
            )

        return _numpy_to_audio(filtered, sample_rate, caption=audio._caption)

    return Transform(transform, name="apply_high_pass_filter", modality="audio")


def apply_band_pass_filter(
    *,
    low_hz: float = 300.0,
    high_hz: float = 3400.0,
    order: int = 5,
) -> Transform[Audio, Audio]:
    """
    Apply a Butterworth band-pass filter to keep only a frequency range.

    Band-pass filtering simulates telephone audio (300-3400 Hz is standard
    PSTN bandwidth) or other bandwidth-limited channels.

    Args:
        low_hz: Lower cutoff frequency in Hz.
        high_hz: Upper cutoff frequency in Hz.
        order: Filter order (steepness of cutoff). Higher = steeper.

    Returns:
        Transform that applies band-pass filter to Audio.

    Reference:
        PSTN telephone bandwidth is 300-3400 Hz, commonly used to
        simulate real-world telephony conditions.
    """
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(
        audio: Audio,
        *,
        low_hz: float = low_hz,
        high_hz: float = high_hz,
        order: int = order,
    ) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Nyquist frequency
        nyquist = sample_rate / 2
        low_normalized = max(low_hz / nyquist, 0.01)
        high_normalized = min(high_hz / nyquist, 0.99)

        if low_normalized >= high_normalized:
            raise ValueError("Low cutoff must be less than high cutoff")

        # Design Butterworth filter
        b, a = signal.butter(order, [low_normalized, high_normalized], btype="band")

        # Apply filter
        if data.ndim == 1:
            filtered = signal.filtfilt(b, a, data)
        else:
            filtered = np.column_stack(
                [signal.filtfilt(b, a, data[:, ch]) for ch in range(data.shape[1])]
            )

        return _numpy_to_audio(filtered, sample_rate, caption=audio._caption)

    return Transform(transform, name="apply_band_pass_filter", modality="audio")


# =============================================================================
# Acoustic Effect Transforms
# =============================================================================


def add_reverb(
    *,
    decay: float = 0.5,
    delay_ms: float = 50.0,
    wet_dry_mix: float = 0.3,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """
    Add reverberation effect to simulate room acoustics.

    Reverb simulates sound reflections in an acoustic space. This is
    relevant for testing ASR systems deployed in real environments.

    Args:
        decay: Decay factor for reflections (0-1). Higher = longer reverb tail.
        delay_ms: Initial delay in milliseconds (simulates room size).
        wet_dry_mix: Mix ratio of reverb to original (0 = dry, 1 = full reverb).
        seed: Random seed for impulse response generation.

    Returns:
        Transform that adds reverb to Audio.

    Reference:
        Room acoustics simulation is used in physical adversarial
        attack research. See: Yakura & Sakuma (2019).
    """
    rng = np.random.default_rng(seed)

    def transform(
        audio: Audio,
        *,
        decay: float = decay,
        delay_ms: float = delay_ms,
        wet_dry_mix: float = wet_dry_mix,
    ) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Generate simple impulse response
        delay_samples = int(delay_ms * sample_rate / 1000)
        ir_length = int(sample_rate * 0.5)  # 500ms impulse response

        # Create impulse response with exponential decay
        ir = np.zeros(ir_length)
        ir[0] = 1.0  # Direct sound

        # Add early reflections
        n_reflections = 6
        for i in range(n_reflections):
            reflection_delay = delay_samples * (i + 1)
            if reflection_delay < ir_length:
                reflection_amp = decay ** (i + 1)
                # Add some randomness to reflection timing
                jitter = int(rng.integers(-delay_samples // 4, delay_samples // 4))
                idx = min(max(reflection_delay + jitter, 0), ir_length - 1)
                ir[idx] += reflection_amp * rng.uniform(0.8, 1.0)

        # Add diffuse reverb tail
        tail_start = delay_samples * (n_reflections + 1)
        if tail_start < ir_length:
            t = np.arange(ir_length - tail_start)
            tail = rng.standard_normal(ir_length - tail_start)
            tail *= np.exp(-t / (decay * sample_rate * 0.3))
            tail *= decay ** (n_reflections + 1) * 0.5
            ir[tail_start:] += tail

        # Normalize IR
        ir = ir / np.max(np.abs(ir))

        # Convolve with audio
        if data.ndim == 1:
            reverb = np.convolve(data, ir, mode="full")[: len(data)]
        else:
            reverb = np.column_stack(
                [
                    np.convolve(data[:, ch], ir, mode="full")[: len(data)]
                    for ch in range(data.shape[1])
                ]
            )

        # Mix wet and dry
        mixed = (1 - wet_dry_mix) * data + wet_dry_mix * reverb

        return _numpy_to_audio(mixed, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_reverb", modality="audio")


def add_echo(
    *,
    delay_ms: float = 200.0,
    decay: float = 0.5,
    n_echoes: int = 3,
) -> Transform[Audio, Audio]:
    """
    Add discrete echo effect to audio.

    Unlike reverb, echo produces distinct repetitions of the original
    sound at regular intervals.

    Args:
        delay_ms: Delay between echoes in milliseconds.
        decay: Amplitude decay per echo (0-1).
        n_echoes: Number of echo repetitions.

    Returns:
        Transform that adds echo to Audio.
    """

    def transform(
        audio: Audio,
        *,
        delay_ms: float = delay_ms,
        decay: float = decay,
        n_echoes: int = n_echoes,
    ) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        delay_samples = int(delay_ms * sample_rate / 1000)

        # Calculate output length
        total_delay = delay_samples * n_echoes
        output_length = len(data) + total_delay

        # Create output array
        if data.ndim == 1:
            output = np.zeros(output_length)
            output[: len(data)] = data
            for i in range(1, n_echoes + 1):
                start = delay_samples * i
                amp = decay**i
                output[start : start + len(data)] += data * amp
        else:
            output = np.zeros((output_length, data.shape[1]))
            output[: len(data)] = data
            for i in range(1, n_echoes + 1):
                start = delay_samples * i
                amp = decay**i
                output[start : start + len(data)] += data * amp

        return _numpy_to_audio(output, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_echo", modality="audio")


# =============================================================================
# Compression/Distortion Transforms
# =============================================================================


def apply_dynamic_range_compression(
    *,
    threshold_db: float = -20.0,
    ratio: float = 4.0,
    attack_ms: float = 5.0,
    release_ms: float = 50.0,
) -> Transform[Audio, Audio]:
    """
    Apply dynamic range compression to reduce volume differences.

    Compression reduces the dynamic range by attenuating signals above
    a threshold. This is common in broadcast audio and telephony.

    Args:
        threshold_db: Level above which compression kicks in (dBFS).
        ratio: Compression ratio (e.g., 4:1 means 4dB input -> 1dB output above threshold).
        attack_ms: Time to reach full compression after signal exceeds threshold.
        release_ms: Time to release compression after signal falls below threshold.

    Returns:
        Transform that applies compression to Audio.

    Reference:
        Dynamic range compression is ubiquitous in audio systems and
        affects how audio is perceived by both humans and machines.
    """

    def transform(
        audio: Audio,
        *,
        threshold_db: float = threshold_db,
        ratio: float = ratio,
        attack_ms: float = attack_ms,
        release_ms: float = release_ms,
    ) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Convert threshold to linear
        threshold_linear = 10 ** (threshold_db / 20)

        # Calculate time constants
        attack_coeff = np.exp(-1.0 / (attack_ms * sample_rate / 1000))
        release_coeff = np.exp(-1.0 / (release_ms * sample_rate / 1000))

        # Process mono or first channel to get envelope
        mono = data if data.ndim == 1 else data[:, 0]

        # Calculate envelope with attack/release
        envelope = np.zeros(len(mono))
        current_level = 0.0

        for i, sample in enumerate(np.abs(mono)):
            if sample > current_level:
                current_level = attack_coeff * current_level + (1 - attack_coeff) * sample
            else:
                current_level = release_coeff * current_level + (1 - release_coeff) * sample
            envelope[i] = current_level

        # Calculate gain reduction
        gain = np.ones(len(envelope))
        above_threshold = envelope > threshold_linear
        if np.any(above_threshold):
            # Gain reduction in dB
            level_db = 20 * np.log10(np.maximum(envelope[above_threshold], 1e-10))
            threshold_db_val = 20 * np.log10(threshold_linear)
            excess_db = level_db - threshold_db_val
            reduced_excess_db = excess_db / ratio
            gain_reduction_db = excess_db - reduced_excess_db
            gain[above_threshold] = 10 ** (-gain_reduction_db / 20)

        # Apply gain
        compressed = data * gain if data.ndim == 1 else data * gain[:, np.newaxis]

        return _numpy_to_audio(compressed, sample_rate, caption=audio._caption)

    return Transform(transform, name="apply_dynamic_range_compression", modality="audio")


def add_clipping(
    *,
    threshold: float = 0.8,
) -> Transform[Audio, Audio]:
    """
    Apply hard clipping distortion to audio.

    Clipping occurs when audio exceeds the maximum level and is
    "clipped" to the limit, creating harmonic distortion.

    Args:
        threshold: Clipping threshold (0-1). Samples exceeding ±threshold
            are clipped to ±threshold.

    Returns:
        Transform that clips Audio.

    Reference:
        Clipping distortion is common in overdriven systems and can
        significantly affect ASR performance.
    """

    def transform(audio: Audio, *, threshold: float = threshold) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        clipped = np.clip(data, -threshold, threshold)
        return _numpy_to_audio(clipped, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_clipping", modality="audio")


# =============================================================================
# Segment/Temporal Manipulation Transforms
# =============================================================================


def trim_silence(
    *,
    threshold_db: float = -40.0,
    min_silence_ms: float = 100.0,
) -> Transform[Audio, Audio]:
    """
    Remove leading and trailing silence from audio.

    Args:
        threshold_db: Amplitude threshold below which is considered silence (dBFS).
        min_silence_ms: Minimum duration of silence to trim.

    Returns:
        Transform that trims silence from Audio.
    """

    def transform(
        audio: Audio,
        *,
        threshold_db: float = threshold_db,
        min_silence_ms: float = min_silence_ms,
    ) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        # Convert threshold to linear
        threshold_linear = 10 ** (threshold_db / 20)
        min_samples = int(min_silence_ms * sample_rate / 1000)

        # Get mono for analysis
        mono = data if data.ndim == 1 else np.mean(data, axis=1)

        # Find non-silent regions
        above_threshold = np.abs(mono) > threshold_linear

        if not np.any(above_threshold):
            # All silence, return as-is
            return audio

        # Find first and last non-silent sample
        nonzero_indices = np.where(above_threshold)[0]
        start = max(0, nonzero_indices[0] - min_samples)
        end = min(len(data), nonzero_indices[-1] + min_samples)

        trimmed = data[start:end] if data.ndim == 1 else data[start:end, :]

        return _numpy_to_audio(trimmed, sample_rate, caption=audio._caption)

    return Transform(transform, name="trim_silence", modality="audio")


def add_fade(
    *,
    fade_in_ms: float = 10.0,
    fade_out_ms: float = 10.0,
) -> Transform[Audio, Audio]:
    """
    Add fade-in and fade-out to audio.

    Fades help avoid clicks at audio boundaries.

    Args:
        fade_in_ms: Fade-in duration in milliseconds.
        fade_out_ms: Fade-out duration in milliseconds.

    Returns:
        Transform that adds fades to Audio.
    """

    def transform(
        audio: Audio, *, fade_in_ms: float = fade_in_ms, fade_out_ms: float = fade_out_ms
    ) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        fade_in_samples = int(fade_in_ms * sample_rate / 1000)
        fade_out_samples = int(fade_out_ms * sample_rate / 1000)

        # Create fade curves
        if fade_in_samples > 0 and fade_in_samples < len(data):
            fade_in = np.linspace(0, 1, fade_in_samples)
            if data.ndim == 1:
                data[:fade_in_samples] *= fade_in
            else:
                data[:fade_in_samples] *= fade_in[:, np.newaxis]

        if fade_out_samples > 0 and fade_out_samples < len(data):
            fade_out = np.linspace(1, 0, fade_out_samples)
            if data.ndim == 1:
                data[-fade_out_samples:] *= fade_out
            else:
                data[-fade_out_samples:] *= fade_out[:, np.newaxis]

        return _numpy_to_audio(data, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_fade", modality="audio")


# =============================================================================
# Spectral / Adversarial Transforms
# =============================================================================


def ultrasonic_shift(
    *,
    carrier_ratio: float = 0.9,
) -> Transform[Audio, Audio]:
    """
    Amplitude-modulate the signal onto a near-Nyquist carrier (DolphinAttack-style).

    Shifts the audible speech spectrum up toward the top of the representable band
    so it is hard for a human to perceive, while the sidebands can still be recovered
    (e.g. by a microphone/ASR front-end's nonlinearity). Tests whether an audio model
    transcribes content that is inaudible to a human reviewer.

    Args:
        carrier_ratio: Carrier frequency as a fraction of the Nyquist rate (0-1).
            Higher pushes the content closer to inaudible.

    Returns:
        Transform that carrier-modulates Audio.

    Reference:
        Zhang et al., "DolphinAttack: Inaudible Voice Commands" (CCS 2017).
    """

    def transform(audio: Audio, *, carrier_ratio: float = carrier_ratio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        nyquist = sample_rate / 2
        carrier_hz = max(1.0, min(carrier_ratio, 0.99)) * nyquist
        n = data.shape[0]
        carrier = np.cos(2 * np.pi * carrier_hz * np.arange(n) / sample_rate)
        if data.ndim == 1:
            modulated = data * carrier
        else:
            modulated = data * carrier[:, np.newaxis]
        return _numpy_to_audio(modulated, sample_rate, caption=audio._caption)

    return Transform(transform, name="ultrasonic_shift", modality="audio")


def spectral_inversion() -> Transform[Audio, Audio]:
    """
    Mirror the frequency spectrum (``f`` -> ``nyquist - f``).

    Multiplying successive samples by an alternating ``+1/-1`` sign flips the
    spectrum end-for-end, scrambling speech into an unintelligible signal that a
    matching inverse recovers. Probes robustness to simple reversible obfuscation.

    Returns:
        Transform that spectrally inverts Audio.
    """

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        sign = np.where(np.arange(n) % 2 == 0, 1.0, -1.0)
        if data.ndim == 1:
            inverted = data * sign
        else:
            inverted = data * sign[:, np.newaxis]
        return _numpy_to_audio(inverted, sample_rate, caption=audio._caption)

    return Transform(transform, name="spectral_inversion", modality="audio")


def bit_crush(
    *,
    bits: int = 6,
    downsample: int = 1,
) -> Transform[Audio, Audio]:
    """
    Reduce bit depth (and optionally sample rate) to add quantization distortion.

    A lo-fi degradation: quantizing to a handful of bits and holding samples
    (sample-and-hold downsampling) introduces the aliasing/quantization artifacts of
    a poor codec, useful for probing ASR robustness to heavily degraded audio.

    Args:
        bits: Target bit depth (1-16). Lower = coarser quantization.
        downsample: Sample-and-hold factor (1 = none, 4 = keep every 4th sample's value).

    Returns:
        Transform that bit-crushes Audio.
    """
    if bits < 1 or bits > 16:
        raise ValueError("bits must be between 1 and 16")
    if downsample < 1:
        raise ValueError("downsample must be >= 1")

    def transform(audio: Audio, *, bits: int = bits, downsample: int = downsample) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        levels = 2 ** (bits - 1)
        crushed = np.round(data * levels) / levels
        if downsample > 1:
            n = crushed.shape[0]
            idx = (np.arange(n) // downsample) * downsample
            idx = np.clip(idx, 0, n - 1)
            crushed = crushed[idx]
        return _numpy_to_audio(crushed, sample_rate, caption=audio._caption)

    return Transform(transform, name="bit_crush", modality="audio")


def add_tone(
    *,
    freq_hz: float = 1000.0,
    gain_db: float = -12.0,
) -> Transform[Audio, Audio]:
    """
    Mix a continuous sine tone into the audio.

    Injects a pure interfering tone (a masking/DTMF-like carrier) alongside the
    speech. Tests whether an audio model can be distracted or steered by an added
    signal a human would dismiss as background noise.

    Args:
        freq_hz: Tone frequency in Hz.
        gain_db: Tone level relative to full scale (dBFS); more negative = quieter.

    Returns:
        Transform that mixes a tone into Audio.
    """

    def transform(audio: Audio, *, freq_hz: float = freq_hz, gain_db: float = gain_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        amplitude = 10 ** (gain_db / 20)
        tone = amplitude * np.sin(2 * np.pi * freq_hz * np.arange(n) / sample_rate)
        if data.ndim == 1:
            mixed = data + tone
        else:
            mixed = data + tone[:, np.newaxis]
        return _numpy_to_audio(mixed, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_tone", modality="audio")


def audio_steganography(
    payload: str,
    *,
    terminator: str = "\x00\x00\x00",
    name: str = "audio_steganography",
) -> Transform[Audio, Audio]:
    """
    Hide a text payload in the least-significant bit of PCM samples.

    Mirrors :func:`dreadnode.transforms.image.image_steganography` for audio: the
    payload is imperceptible on playback but recoverable from the raw samples,
    probing whether an audio model reads hidden instructions.

    Args:
        payload: Text to embed.
        terminator: Byte sequence marking the end of the payload (for extraction).
        name: Transform name.

    Returns:
        Transform that embeds the payload in Audio's LSBs.
    """
    full_payload = payload + terminator
    payload_bits = np.array(
        [int(b) for byte in full_payload.encode("utf-8") for b in format(byte, "08b")],
        dtype=np.int16,
    )

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        flat = data.reshape(-1)
        if payload_bits.shape[0] > flat.shape[0]:
            raise ValueError(
                f"Payload too large: {payload_bits.shape[0]} bits > {flat.shape[0]} samples. "
                "Use a longer audio clip or a shorter payload."
            )
        ints = np.clip(np.round(flat * 32767), -32767, 32767).astype(np.int16)
        ints[: payload_bits.shape[0]] = (ints[: payload_bits.shape[0]] & ~1) | payload_bits
        stego = (ints.astype(np.float64) / 32767).reshape(data.shape)
        return _numpy_to_audio(stego, sample_rate, caption=audio._caption)

    return Transform(transform, name=name, modality="audio")


# =============================================================================
# AugLy-style + adversarial audio augmentations
# =============================================================================


def _broadcast(vec: np.ndarray, data: np.ndarray) -> np.ndarray:
    """Broadcast a 1-D per-sample vector across mono or stereo ``data``."""
    return vec if data.ndim == 1 else vec[:, np.newaxis]


def add_brown_noise(
    *,
    snr_db: float = 20.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Add brown (1/f^2, "red") noise — deeper rumble than pink noise."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, snr_db: float = snr_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        white = rng.standard_normal(n)
        fft = np.fft.rfft(white)
        freqs = np.fft.rfftfreq(n)
        freqs[0] = 1e-10
        fft *= 1.0 / freqs
        brown = np.fft.irfft(fft, n)
        signal_power = np.mean(data**2)
        if signal_power == 0:
            return audio
        noise_power = signal_power / (10 ** (snr_db / 10))
        brown *= np.sqrt(noise_power / np.mean(brown**2))
        return _numpy_to_audio(data + _broadcast(brown, data), sample_rate, caption=audio._caption)

    return Transform(transform, name="add_brown_noise", modality="audio")


def add_babble_noise(
    *,
    snr_db: float = 15.0,
    n_talkers: int = 4,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Add multi-talker babble (syllable-rate modulated, speech-band noise)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, snr_db: float = snr_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        t = np.arange(n) / sample_rate
        babble = np.zeros(n)
        for _ in range(n_talkers):
            voice = rng.standard_normal(n)
            mod = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(2, 6) * t + rng.uniform(0, 2 * np.pi))
            babble += voice * mod
        nyq = sample_rate / 2
        b, a = signal.butter(4, [300 / nyq, min(3400 / nyq, 0.99)], btype="band")
        babble = signal.filtfilt(b, a, babble)
        signal_power = np.mean(data**2)
        if signal_power == 0 or np.mean(babble**2) == 0:
            return audio
        noise_power = signal_power / (10 ** (snr_db / 10))
        babble *= np.sqrt(noise_power / np.mean(babble**2))
        return _numpy_to_audio(data + _broadcast(babble, data), sample_rate, caption=audio._caption)

    return Transform(transform, name="add_babble_noise", modality="audio")


def add_clicks(
    *,
    rate_per_sec: float = 5.0,
    amplitude: float = 0.5,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Add impulsive clicks/crackle (vinyl/scratch artifacts)."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, rate_per_sec: float = rate_per_sec) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = data.copy()
        n = data.shape[0]
        n_clicks = int(rate_per_sec * n / sample_rate)
        if n_clicks <= 0:
            return audio
        positions = rng.integers(0, n, size=n_clicks)
        signs = rng.choice([-1.0, 1.0], size=n_clicks)
        for p, s in zip(positions, signs, strict=True):
            out[p] = np.clip(out[p] + s * amplitude, -1.0, 1.0)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_clicks", modality="audio")


def time_masking(
    *,
    max_ms: float = 100.0,
    n_masks: int = 2,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Zero out random time spans (SpecAugment time masking)."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, max_ms: float = max_ms, n_masks: int = n_masks) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = data.copy()
        n = data.shape[0]
        max_samples = max(2, int(max_ms * sample_rate / 1000))
        for _ in range(n_masks):
            w = int(rng.integers(1, max_samples))
            start = int(rng.integers(0, max(1, n - w)))
            out[start : start + w] = 0.0
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="time_masking", modality="audio")


def frequency_masking(
    *,
    n_bands: int = 2,
    max_band: float = 0.15,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Zero out random frequency bands via STFT (SpecAugment frequency masking)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    rng = np.random.default_rng(seed)

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)

        def mask(y: np.ndarray) -> np.ndarray:
            _, _, stft = signal.stft(y, fs=sample_rate, nperseg=512)
            n_freq = stft.shape[0]
            for _ in range(n_bands):
                bw = max(1, int(n_freq * rng.uniform(0.02, max_band)))
                start = int(rng.integers(0, max(1, n_freq - bw)))
                stft[start : start + bw, :] = 0
            _, rec = signal.istft(stft, fs=sample_rate, nperseg=512)
            return rec[: len(y)] if len(rec) >= len(y) else np.pad(rec, (0, len(y) - len(rec)))

        if data.ndim == 1:
            out = mask(data)
        else:
            out = np.column_stack([mask(data[:, c]) for c in range(data.shape[1])])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="frequency_masking", modality="audio")


def reverse_audio() -> Transform[Audio, Audio]:
    """Reverse the audio in time (temporal obfuscation)."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        return _numpy_to_audio(data[::-1], sample_rate, caption=audio._caption)

    return Transform(transform, name="reverse_audio", modality="audio")


def tremolo(
    *,
    rate_hz: float = 5.0,
    depth: float = 0.5,
) -> Transform[Audio, Audio]:
    """Modulate amplitude with a low-frequency oscillator (tremolo)."""

    def transform(audio: Audio, *, rate_hz: float = rate_hz, depth: float = depth) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        lfo = 1 - depth / 2 + depth / 2 * np.sin(2 * np.pi * rate_hz * np.arange(n) / sample_rate)
        return _numpy_to_audio(data * _broadcast(lfo, data), sample_rate, caption=audio._caption)

    return Transform(transform, name="tremolo", modality="audio")


def vibrato(
    *,
    rate_hz: float = 5.0,
    depth_ms: float = 2.0,
) -> Transform[Audio, Audio]:
    """Modulate pitch with a low-frequency oscillator via fractional delay (vibrato)."""

    def transform(audio: Audio, *, rate_hz: float = rate_hz, depth_ms: float = depth_ms) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        delay = depth_ms / 1000 * sample_rate
        idx = np.arange(n) + delay * np.sin(2 * np.pi * rate_hz * np.arange(n) / sample_rate)
        idx = np.clip(idx, 0, n - 1)
        base = np.arange(n)
        if data.ndim == 1:
            out = np.interp(idx, base, data)
        else:
            out = np.column_stack([np.interp(idx, base, data[:, c]) for c in range(data.shape[1])])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="vibrato", modality="audio")


def wow_flutter(
    *,
    wow_hz: float = 0.5,
    flutter_hz: float = 6.0,
    depth_ms: float = 3.0,
) -> Transform[Audio, Audio]:
    """Add tape-style pitch drift combining slow "wow" and fast "flutter"."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        t = np.arange(n) / sample_rate
        delay = depth_ms / 1000 * sample_rate
        mod = 0.6 * np.sin(2 * np.pi * wow_hz * t) + 0.4 * np.sin(2 * np.pi * flutter_hz * t)
        idx = np.clip(np.arange(n) + delay * mod, 0, n - 1)
        base = np.arange(n)
        if data.ndim == 1:
            out = np.interp(idx, base, data)
        else:
            out = np.column_stack([np.interp(idx, base, data[:, c]) for c in range(data.shape[1])])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="wow_flutter", modality="audio")


def granular_shuffle(
    *,
    grain_ms: float = 50.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Chop into short grains and randomly reorder them (granular scrambling)."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, grain_ms: float = grain_ms) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        g = max(1, int(grain_ms * sample_rate / 1000))
        n = data.shape[0]
        n_grains = n // g
        if n_grains < 2:
            return audio
        grains = [data[i * g : (i + 1) * g] for i in range(n_grains)]
        order = rng.permutation(n_grains)
        shuffled = [grains[i] for i in order]
        tail = data[n_grains * g :]
        out = (
            np.concatenate([*shuffled, tail], axis=0)
            if len(tail)
            else np.concatenate(shuffled, axis=0)
        )
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="granular_shuffle", modality="audio")


def sample_dropout(
    *,
    loss_ratio: float = 0.1,
    segment_ms: float = 20.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Zero random short segments to simulate packet loss / VoIP dropout."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, loss_ratio: float = loss_ratio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = data.copy()
        seg = max(1, int(segment_ms * sample_rate / 1000))
        n_segments = data.shape[0] // seg
        for i in range(n_segments):
            if rng.random() < loss_ratio:
                out[i * seg : (i + 1) * seg] = 0.0
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="sample_dropout", modality="audio")


def pre_emphasis(
    *,
    coeff: float = 0.97,
) -> Transform[Audio, Audio]:
    """Apply a pre-emphasis high-shelf (``y[n] = x[n] - coeff*x[n-1]``)."""

    def transform(audio: Audio, *, coeff: float = coeff) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        if data.ndim == 1:
            out = np.append(data[0], data[1:] - coeff * data[:-1])
        else:
            out = np.vstack([data[0], data[1:] - coeff * data[:-1]])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="pre_emphasis", modality="audio")


def notch_filter(
    *,
    freq_hz: float = 1000.0,
    quality: float = 30.0,
) -> Transform[Audio, Audio]:
    """Remove a narrow frequency band with an IIR notch filter."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, freq_hz: float = freq_hz, quality: float = quality) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        w0 = freq_hz / (sample_rate / 2)
        if not 0 < w0 < 1:
            return audio
        b, a = signal.iirnotch(w0, quality)
        if data.ndim == 1:
            out = signal.filtfilt(b, a, data)
        else:
            out = np.column_stack([signal.filtfilt(b, a, data[:, c]) for c in range(data.shape[1])])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="notch_filter", modality="audio")


def peaking_equalizer(
    *,
    freq_hz: float = 1000.0,
    gain_db: float = 6.0,
    q: float = 1.0,
) -> Transform[Audio, Audio]:
    """Boost or cut a frequency band with an RBJ peaking-EQ biquad."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, freq_hz: float = freq_hz, gain_db: float = gain_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        big_a = 10 ** (gain_db / 40)
        w0 = 2 * np.pi * freq_hz / sample_rate
        alpha = np.sin(w0) / (2 * q)
        cos_w0 = np.cos(w0)
        a0 = 1 + alpha / big_a
        b = [(1 + alpha * big_a) / a0, (-2 * cos_w0) / a0, (1 - alpha * big_a) / a0]
        a = [1.0, (-2 * cos_w0) / a0, (1 - alpha / big_a) / a0]
        out = signal.lfilter(b, a, data, axis=0)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="peaking_equalizer", modality="audio")


def soft_clip(
    *,
    gain: float = 3.0,
) -> Transform[Audio, Audio]:
    """Apply smooth (tanh) overdrive saturation instead of hard clipping."""

    def transform(audio: Audio, *, gain: float = gain) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = np.tanh(gain * data) / np.tanh(gain)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="soft_clip", modality="audio")


def ring_modulation(
    *,
    freq_hz: float = 500.0,
    mix: float = 1.0,
) -> Transform[Audio, Audio]:
    """Multiply by an audible carrier tone (ring modulation / metallic timbre)."""

    def transform(audio: Audio, *, freq_hz: float = freq_hz, mix: float = mix) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        carrier = np.sin(2 * np.pi * freq_hz * np.arange(n) / sample_rate)
        ring = data * _broadcast(carrier, data)
        out = (1 - mix) * data + mix * ring
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="ring_modulation", modality="audio")


def downsample_telephone(
    *,
    target_hz: int = 8000,
) -> Transform[Audio, Audio]:
    """Resample down to ``target_hz`` and back (telephone-bandwidth degradation)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, target_hz: int = target_hz) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        if target_hz >= sample_rate:
            return audio
        n = data.shape[0]
        n_down = max(1, int(n * target_hz / sample_rate))
        down = signal.resample(data, n_down, axis=0)
        up = signal.resample(down, n, axis=0)
        return _numpy_to_audio(up, sample_rate, caption=audio._caption)

    return Transform(transform, name="downsample_telephone", modality="audio")


def loop_audio(
    *,
    count: int = 2,
) -> Transform[Audio, Audio]:
    """Repeat the clip ``count`` times end-to-end."""
    if count < 1:
        raise ValueError("count must be >= 1")

    def transform(audio: Audio, *, count: int = count) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = np.concatenate([data] * count, axis=0)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="loop_audio", modality="audio")


def polarity_inversion() -> Transform[Audio, Audio]:
    """Flip the waveform polarity (multiply by -1) — inaudible, breaks phase-sensitive models."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        return _numpy_to_audio(-data, sample_rate, caption=audio._caption)

    return Transform(transform, name="polarity_inversion", modality="audio")


def time_shift(
    *,
    shift_ms: float = 100.0,
    rollover: bool = True,
) -> Transform[Audio, Audio]:
    """Shift the signal in time, wrapping around (rollover) or padding with silence."""

    def transform(audio: Audio, *, shift_ms: float = shift_ms, rollover: bool = rollover) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        s = int(shift_ms * sample_rate / 1000)
        if rollover:
            out = np.roll(data, s, axis=0)
        else:
            out = np.zeros_like(data)
            if s >= 0:
                out[s:] = data[: len(data) - s] if s < len(data) else out[s:]
            else:
                out[:s] = data[-s:]
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="time_shift", modality="audio")


def gain_transition(
    *,
    start_gain_db: float = -20.0,
    end_gain_db: float = 0.0,
) -> Transform[Audio, Audio]:
    """Ramp the gain linearly from ``start_gain_db`` to ``end_gain_db`` across the clip."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        gains = np.linspace(10 ** (start_gain_db / 20), 10 ** (end_gain_db / 20), n)
        return _numpy_to_audio(data * _broadcast(gains, data), sample_rate, caption=audio._caption)

    return Transform(transform, name="gain_transition", modality="audio")


def air_absorption(
    *,
    distance_m: float = 10.0,
) -> Transform[Audio, Audio]:
    """Attenuate high frequencies with distance (atmospheric air absorption)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio, *, distance_m: float = distance_m) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        cutoff = max(1000.0, 12000.0 - distance_m * 400.0)
        nyq = sample_rate / 2
        if cutoff >= nyq:
            return audio
        b, a = signal.butter(2, cutoff / nyq, btype="low")
        if data.ndim == 1:
            out = signal.filtfilt(b, a, data)
        else:
            out = np.column_stack([signal.filtfilt(b, a, data[:, c]) for c in range(data.shape[1])])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="air_absorption", modality="audio")


def _shelf_coeffs(kind: str, sample_rate: int, freq_hz: float, gain_db: float, q: float) -> tuple:
    """RBJ low/high-shelf biquad coefficients (normalized)."""
    big_a = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * freq_hz / sample_rate
    cw, sw = np.cos(w0), np.sin(w0)
    alpha = sw / (2 * q)
    two_sqrt_a_alpha = 2 * np.sqrt(big_a) * alpha
    if kind == "low":
        b0 = big_a * ((big_a + 1) - (big_a - 1) * cw + two_sqrt_a_alpha)
        b1 = 2 * big_a * ((big_a - 1) - (big_a + 1) * cw)
        b2 = big_a * ((big_a + 1) - (big_a - 1) * cw - two_sqrt_a_alpha)
        a0 = (big_a + 1) + (big_a - 1) * cw + two_sqrt_a_alpha
        a1 = -2 * ((big_a - 1) + (big_a + 1) * cw)
        a2 = (big_a + 1) + (big_a - 1) * cw - two_sqrt_a_alpha
    else:
        b0 = big_a * ((big_a + 1) + (big_a - 1) * cw + two_sqrt_a_alpha)
        b1 = -2 * big_a * ((big_a - 1) + (big_a + 1) * cw)
        b2 = big_a * ((big_a + 1) + (big_a - 1) * cw - two_sqrt_a_alpha)
        a0 = (big_a + 1) - (big_a - 1) * cw + two_sqrt_a_alpha
        a1 = 2 * ((big_a - 1) - (big_a + 1) * cw)
        a2 = (big_a + 1) - (big_a - 1) * cw - two_sqrt_a_alpha
    return [b0 / a0, b1 / a0, b2 / a0], [1.0, a1 / a0, a2 / a0]


def low_shelf_filter(
    *, freq_hz: float = 200.0, gain_db: float = 6.0, q: float = 0.707
) -> Transform[Audio, Audio]:
    """Boost or cut frequencies below a corner (low-shelf EQ)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        b, a = _shelf_coeffs("low", sample_rate, freq_hz, gain_db, q)
        return _numpy_to_audio(
            signal.lfilter(b, a, data, axis=0), sample_rate, caption=audio._caption
        )

    return Transform(transform, name="low_shelf_filter", modality="audio")


def high_shelf_filter(
    *, freq_hz: float = 4000.0, gain_db: float = 6.0, q: float = 0.707
) -> Transform[Audio, Audio]:
    """Boost or cut frequencies above a corner (high-shelf EQ)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        b, a = _shelf_coeffs("high", sample_rate, freq_hz, gain_db, q)
        return _numpy_to_audio(
            signal.lfilter(b, a, data, axis=0), sample_rate, caption=audio._caption
        )

    return Transform(transform, name="high_shelf_filter", modality="audio")


def band_stop_filter(
    *, low_hz: float = 800.0, high_hz: float = 1200.0, order: int = 4
) -> Transform[Audio, Audio]:
    """Attenuate a frequency band (Butterworth band-stop / band-reject)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        nyq = sample_rate / 2
        lo, hi = max(low_hz / nyq, 0.01), min(high_hz / nyq, 0.99)
        if lo >= hi:
            return audio
        b, a = signal.butter(order, [lo, hi], btype="bandstop")
        if data.ndim == 1:
            out = signal.filtfilt(b, a, data)
        else:
            out = np.column_stack([signal.filtfilt(b, a, data[:, c]) for c in range(data.shape[1])])
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="band_stop_filter", modality="audio")


def seven_band_parametric_eq(
    *,
    gains_db: tuple[float, float, float, float, float, float, float] = (3, -3, 3, -3, 3, -3, 3),
    q: float = 1.0,
) -> Transform[Audio, Audio]:
    """Apply a 7-band parametric EQ (cascaded peaking biquads across the spectrum)."""
    with catch_import_error("dreadnode"):
        from scipy import signal

    bands = (63.0, 160.0, 400.0, 1000.0, 2500.0, 6300.0, 12000.0)

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = data
        for freq, gain in zip(bands, gains_db, strict=True):
            if freq >= sample_rate / 2 or gain == 0:
                continue
            big_a = 10 ** (gain / 40)
            w0 = 2 * np.pi * freq / sample_rate
            alpha = np.sin(w0) / (2 * q)
            cw = np.cos(w0)
            a0 = 1 + alpha / big_a
            b = [(1 + alpha * big_a) / a0, (-2 * cw) / a0, (1 - alpha * big_a) / a0]
            a = [1.0, (-2 * cw) / a0, (1 - alpha / big_a) / a0]
            out = signal.lfilter(b, a, out, axis=0)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="seven_band_parametric_eq", modality="audio")


def aliasing(
    *,
    factor: int = 3,
) -> Transform[Audio, Audio]:
    """Decimate without an anti-alias filter, then upsample — foldover/aliasing artifacts."""
    if factor < 2:
        raise ValueError("factor must be >= 2")

    def transform(audio: Audio, *, factor: int = factor) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        down = data[::factor]
        up = np.repeat(down, factor, axis=0)
        if up.shape[0] >= n:
            up = up[:n]
        else:
            pad = [(0, n - up.shape[0])] + [(0, 0)] * (data.ndim - 1)
            up = np.pad(up, pad, mode="edge")
        return _numpy_to_audio(up, sample_rate, caption=audio._caption)

    return Transform(transform, name="aliasing", modality="audio")


def limiter(
    *,
    threshold_db: float = -3.0,
    release_ms: float = 50.0,
) -> Transform[Audio, Audio]:
    """Peak-limit the signal with a smoothed envelope (softer than hard clipping)."""

    def transform(audio: Audio, *, threshold_db: float = threshold_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        threshold = 10 ** (threshold_db / 20)
        mono = data if data.ndim == 1 else np.mean(np.abs(data), axis=1)
        env = np.abs(mono)
        release_coeff = np.exp(-1.0 / (release_ms * sample_rate / 1000))
        smoothed = np.zeros(len(env))
        current = 0.0
        for i, v in enumerate(env):
            current = max(v, release_coeff * current + (1 - release_coeff) * v)
            smoothed[i] = current
        gain = np.minimum(1.0, threshold / np.maximum(smoothed, 1e-8))
        out = data * _broadcast(gain, data)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="limiter", modality="audio")


def add_short_noises(
    *,
    n_bursts: int = 5,
    burst_ms: float = 50.0,
    snr_db: float = 10.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Add sparse short noise bursts at random offsets (transient interference)."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio, *, n_bursts: int = n_bursts) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = data.copy()
        n = data.shape[0]
        blen = max(1, int(burst_ms * sample_rate / 1000))
        signal_power = np.mean(data**2)
        if signal_power == 0:
            return audio
        amp = np.sqrt(signal_power / (10 ** (snr_db / 10)))
        for _ in range(n_bursts):
            start = int(rng.integers(0, max(1, n - blen)))
            burst = rng.standard_normal(blen) * amp
            out[start : start + blen] += _broadcast(burst, data)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="add_short_noises", modality="audio")


def repeat_part(
    *,
    segment_ms: float = 100.0,
    position: float = 0.5,
    repeats: int = 2,
) -> Transform[Audio, Audio]:
    """Duplicate a sub-segment inline (stutter / repeated-frame artifact)."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        seg = max(1, int(segment_ms * sample_rate / 1000))
        start = min(int(position * n), max(0, n - seg))
        end = start + seg
        insert = np.concatenate([data[start:end]] * repeats, axis=0)
        out = np.concatenate([data[:end], insert, data[end:]], axis=0)
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="repeat_part", modality="audio")


def ogg_codec_roundtrip() -> Transform[Audio, Audio]:
    """Encode to OGG/Vorbis and decode back, injecting lossy-codec artifacts."""
    with catch_import_error("dreadnode"):
        import soundfile as sf

    def transform(audio: Audio) -> Audio:
        import io

        data, sample_rate = _audio_to_numpy(audio)
        buf = io.BytesIO()
        sf.write(buf, data, sample_rate, format="OGG", subtype="VORBIS")
        buf.seek(0)
        decoded, sr2 = sf.read(buf, dtype="float64")
        return _numpy_to_audio(decoded, sr2, caption=audio._caption)

    return Transform(transform, name="ogg_codec_roundtrip", modality="audio")


# =============================================================================
# Modulated-delay effects, distortion, and channel simulation (round 2)
# =============================================================================


def chorus(
    *,
    rate_hz: float = 1.5,
    depth_ms: float = 5.0,
    mix: float = 0.5,
    voices: int = 3,
) -> Transform[Audio, Audio]:
    """Layer LFO-modulated delayed voices for a chorus/ensemble effect."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        base = np.arange(n)
        wet = np.zeros_like(data, dtype=np.float64)
        for v in range(max(1, voices)):
            delay = depth_ms / 1000 * sample_rate * (0.5 + 0.5 * v / max(1, voices))
            phase = v * 2 * np.pi / max(1, voices)
            idx = np.clip(
                base + delay * (1 + np.sin(2 * np.pi * rate_hz * base / sample_rate + phase)),
                0,
                n - 1,
            )
            if data.ndim == 1:
                wet += np.interp(idx, base, data)
            else:
                wet += np.column_stack(
                    [np.interp(idx, base, data[:, c]) for c in range(data.shape[1])]
                )
        wet /= max(1, voices)
        out = (1 - mix) * data + mix * wet
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="chorus", modality="audio")


def flanger(
    *,
    rate_hz: float = 0.5,
    depth_ms: float = 3.0,
    mix: float = 0.5,
) -> Transform[Audio, Audio]:
    """Sweep a short modulated delay to create a flanging comb filter."""

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        n = data.shape[0]
        base = np.arange(n)
        delay = depth_ms / 1000 * sample_rate
        idx = np.clip(
            base + delay * (0.5 + 0.5 * np.sin(2 * np.pi * rate_hz * base / sample_rate)), 0, n - 1
        )
        if data.ndim == 1:
            delayed = np.interp(idx, base, data)
        else:
            delayed = np.column_stack(
                [np.interp(idx, base, data[:, c]) for c in range(data.shape[1])]
            )
        out = (1 - mix) * data + mix * delayed
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="flanger", modality="audio")


def harmonic_distortion(
    *,
    amount: float = 0.3,
) -> Transform[Audio, Audio]:
    """Cubic waveshaping that adds harmonics (analog-style distortion)."""

    def transform(audio: Audio, *, amount: float = amount) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        out = (1 + amount) * data - amount * data**3
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="harmonic_distortion", modality="audio")


def dc_offset(
    *,
    offset: float = 0.05,
) -> Transform[Audio, Audio]:
    """Add a constant DC bias to the waveform."""

    def transform(audio: Audio, *, offset: float = offset) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        return _numpy_to_audio(data + offset, sample_rate, caption=audio._caption)

    return Transform(transform, name="dc_offset", modality="audio")


def adjust_duration(
    *,
    target_seconds: float = 2.0,
) -> Transform[Audio, Audio]:
    """Pad with silence or crop to a fixed duration."""

    def transform(audio: Audio, *, target_seconds: float = target_seconds) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        target = max(1, int(target_seconds * sample_rate))
        n = data.shape[0]
        if n >= target:
            out = data[:target]
        else:
            pad = [(0, target - n)] + [(0, 0)] * (data.ndim - 1)
            out = np.pad(data, pad, mode="constant")
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="adjust_duration", modality="audio")


def apply_impulse_response(
    *,
    rt60_ms: float = 300.0,
    mix: float = 1.0,
    seed: int | None = None,
) -> Transform[Audio, Audio]:
    """Convolve with a synthetic room impulse response (over-the-air playback simulation)."""
    rng = np.random.default_rng(seed)

    def transform(audio: Audio) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        length = max(2, int(rt60_ms / 1000 * sample_rate))
        decay = np.exp(-np.arange(length) / (rt60_ms / 1000 * sample_rate / 3))
        ir = rng.standard_normal(length) * decay
        ir[0] = 1.0
        ir /= np.max(np.abs(ir))
        if data.ndim == 1:
            wet = np.convolve(data, ir, mode="full")[: len(data)]
        else:
            wet = np.column_stack(
                [
                    np.convolve(data[:, c], ir, mode="full")[: len(data)]
                    for c in range(data.shape[1])
                ]
            )
        out = (1 - mix) * data + mix * wet
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="apply_impulse_response", modality="audio")


def dtmf_tone(
    *,
    digit: str = "5",
    gain_db: float = -12.0,
) -> Transform[Audio, Audio]:
    """Mix a DTMF (touch-tone) dual-frequency tone over the audio."""
    dtmf = {
        "1": (697, 1209),
        "2": (697, 1336),
        "3": (697, 1477),
        "4": (770, 1209),
        "5": (770, 1336),
        "6": (770, 1477),
        "7": (852, 1209),
        "8": (852, 1336),
        "9": (852, 1477),
        "*": (941, 1209),
        "0": (941, 1336),
        "#": (941, 1477),
    }

    def transform(audio: Audio, *, digit: str = digit) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        f1, f2 = dtmf.get(digit, (770, 1336))
        n = data.shape[0]
        t = np.arange(n) / sample_rate
        amp = 10 ** (gain_db / 20)
        tone = amp * (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)) / 2
        return _numpy_to_audio(data + _broadcast(tone, data), sample_rate, caption=audio._caption)

    return Transform(transform, name="dtmf_tone", modality="audio")


def reverse_segments(
    *,
    segment_ms: float = 100.0,
) -> Transform[Audio, Audio]:
    """Reverse the audio within fixed-length segments (local temporal scramble)."""

    def transform(audio: Audio, *, segment_ms: float = segment_ms) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        seg = max(1, int(segment_ms * sample_rate / 1000))
        out = data.copy()
        for i in range(data.shape[0] // seg):
            out[i * seg : (i + 1) * seg] = data[i * seg : (i + 1) * seg][::-1]
        return _numpy_to_audio(out, sample_rate, caption=audio._caption)

    return Transform(transform, name="reverse_segments", modality="audio")


def loudness_normalize(
    *,
    target_db: float = -20.0,
) -> Transform[Audio, Audio]:
    """Normalize to a target RMS loudness (perceptual level, not peak)."""

    def transform(audio: Audio, *, target_db: float = target_db) -> Audio:
        data, sample_rate = _audio_to_numpy(audio)
        rms = np.sqrt(np.mean(data**2))
        if rms == 0:
            return audio
        gain = 10 ** (target_db / 20) / rms
        return _numpy_to_audio(data * gain, sample_rate, caption=audio._caption)

    return Transform(transform, name="loudness_normalize", modality="audio")

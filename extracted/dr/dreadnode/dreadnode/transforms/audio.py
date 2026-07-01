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

    def transform(audio: Audio, *, semitones: float = semitones) -> Audio:
        if semitones == 0:
            return audio

        data, sample_rate = _audio_to_numpy(audio)
        original_length = data.shape[0]

        # Pitch shift = time stretch + resample
        # To shift pitch up by n semitones, we:
        # 1. Time stretch by 2^(n/12) (make it longer)
        # 2. Resample to original length (speeds up, raising pitch)
        rate = 2 ** (semitones / 12)

        # Time stretch (make longer for pitch up, shorter for pitch down)
        time_stretch_transform = time_stretch(rate=1 / rate)
        stretched_audio = time_stretch_transform(audio)

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

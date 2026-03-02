import librosa
import soundfile as sf
import os


def trim_and_save_audio(ref_path, deg_path, trim_duration, sr):
    # Load the reference and degraded audio
    ref_audio, ref_sr = librosa.load(ref_path, sr=sr)
    deg_audio, deg_sr = librosa.load(deg_path, sr=sr)

    # Calculate the number of samples corresponding to the trim duration
    ref_trim_samples = int(trim_duration * ref_sr)
    deg_trim_samples = int(trim_duration * deg_sr)

    # Trim both audios to the specified duration
    ref_audio_trimmed = ref_audio[:ref_trim_samples]
    deg_audio_trimmed = deg_audio[:deg_trim_samples]

    # Get the directory and filename, append '_short' before the file extension
    ref_dir, ref_filename = os.path.split(ref_path)
    deg_dir, deg_filename = os.path.split(deg_path)

    ref_short_path = os.path.join(ref_dir, f"{os.path.splitext(ref_filename)[0]}_short.wav")
    deg_short_path = os.path.join(deg_dir, f"{os.path.splitext(deg_filename)[0]}_short.wav")

    # Save the trimmed audios
    sf.write(ref_short_path, ref_audio_trimmed, ref_sr)
    sf.write(deg_short_path, deg_audio_trimmed, deg_sr)


# Example usage:
trim_and_save_audio("audio/p239_021.wav", "audio/p239_021_opus.wav", trim_duration=0.2, sr=16000)

import numpy as np
import pandas as pd
import librosa
import time
from scipy.signal import convolve2d
from numba import njit
from scipy.ndimage import uniform_filter1d


# 1. CMVN Original Version
def cmvnw_original(vec, win_size=301, variance_normalization=False):
    eps = 2**-30
    rows, cols = vec.shape
    pad_size = int((win_size - 1) / 2)
    vec_pad = np.lib.pad(vec, ((pad_size, pad_size), (0, 0)), "symmetric")
    mean_subtracted = np.zeros(np.shape(vec), dtype=np.float32)

    for i in range(rows):
        window = vec_pad[i : i + win_size, :]
        window_mean = np.mean(window, axis=0)
        mean_subtracted[i, :] = vec[i, :] - window_mean

    if variance_normalization:
        variance_normalized = np.zeros(np.shape(vec), dtype=np.float32)
        vec_pad_variance = np.lib.pad(mean_subtracted, ((pad_size, pad_size), (0, 0)), "symmetric")

        for i in range(rows):
            window = vec_pad_variance[i : i + win_size, :]
            window_variance = np.std(window, axis=0)
            variance_normalized[i, :] = mean_subtracted[i, :] / (window_variance + eps)
        return variance_normalized
    else:
        return mean_subtracted


# 3. Optimized Version with SciPy + Numba
@njit
def mean_subtraction(vec, mean):
    return vec - mean


@njit
def variance_normalization(mean_subtracted, squared_mean, mean, eps):
    variance = np.sqrt(squared_mean - mean**2)
    return mean_subtracted / (variance + eps)


def cmvnw_numba_scipy(vec, win_size=301, variance_normalization_flag=False):
    eps = 2**-30
    rows, cols = vec.shape

    # Ensure window size is odd
    assert win_size % 2 == 1, "Window size must be odd!"

    # Padding
    pad_size = (win_size - 1) // 2
    vec_pad = np.pad(vec, ((pad_size, pad_size), (0, 0)), mode="symmetric")

    # Create convolution kernel
    kernel = np.ones((win_size, 1), dtype=np.float32) / win_size

    # Compute the mean using convolve2d with no padding
    mean = convolve2d(vec_pad, kernel, mode="same", boundary="fill", fillvalue=0)[pad_size : pad_size + rows, :]

    # Subtract mean using Numba
    mean_subtracted = mean_subtraction(vec, mean)

    if variance_normalization_flag:
        # Compute squared values for variance
        squared_vec = vec**2
        squared_mean = convolve2d(vec_pad**2, kernel, mode="same", boundary="fill", fillvalue=0)[pad_size : pad_size + rows, :]

        # Perform variance normalization using Numba
        return variance_normalization(mean_subtracted, squared_mean, mean, eps)

    return mean_subtracted


from scipy.signal import convolve


def cmvnw_optimized(vec, win_size=301, variance_normalization=False):
    """
    Optimized version of cmvnw function using vectorized operations with improved accuracy.
    """
    rows, cols = vec.shape
    assert isinstance(win_size, int), "Size must be of type 'int'!"
    assert win_size % 2 == 1, "Windows size must be odd!"

    # Create a window for convolution
    window = np.ones(win_size) / win_size

    # Pad the input array
    pad_size = (win_size - 1) // 2
    vec_pad = np.pad(vec, ((pad_size, pad_size), (0, 0)), mode="symmetric")

    # Compute local mean using convolution
    local_mean = convolve(vec_pad, window.reshape(-1, 1), mode="valid")

    # Subtract mean
    mean_subtracted = vec - local_mean

    if variance_normalization:
        # Pad the mean_subtracted array for variance calculation
        mean_subtracted_pad = np.pad(mean_subtracted, ((pad_size, pad_size), (0, 0)), mode="symmetric")

        # Compute local variance
        local_var = convolve(mean_subtracted_pad**2, window.reshape(-1, 1), mode="valid")
        local_std = np.sqrt(np.maximum(local_var, 2**-30))  # Use same epsilon as original

        # Normalize by standard deviation
        output = mean_subtracted / local_std
    else:
        output = mean_subtracted

    return output


import numpy as np


def cmvnwR(vec, win_size=301, variance_normalization=False):
    eps = 2**-30
    rows, cols = vec.shape

    # Windows size must be odd.
    assert isinstance(win_size, int) and win_size % 2 == 1, "Windows size must be an odd integer!"

    # Padding and initial definitions
    pad_size = (win_size - 1) // 2
    vec_pad = np.pad(vec, ((pad_size, pad_size), (0, 0)), "symmetric")
    mean_subtracted = np.empty_like(vec, dtype=np.float32)

    # Compute the mean-subtracted features
    for i in range(rows):
        window = vec_pad[i : i + win_size, :]
        mean_subtracted[i, :] = vec[i, :] - np.mean(window, axis=0)

    if variance_normalization:
        variance_normalized = np.empty_like(vec, dtype=np.float32)
        vec_pad_variance = np.pad(mean_subtracted, ((pad_size, pad_size), (0, 0)), "symmetric")

        # Compute the variance-normalized features
        for i in range(rows):
            window = vec_pad_variance[i : i + win_size, :]
            variance_normalized[i, :] = mean_subtracted[i, :] / (np.std(window, axis=0) + eps)
        return variance_normalized
    else:
        return mean_subtracted


from numba import jit


@jit(nopython=True)
def cmvnw_exact1(vec, win_size=301, variance_normalization=False):
    """
    Optimized version of cmvnw function using Numba for acceleration while maintaining exact precision.
    """
    rows, cols = vec.shape
    assert win_size % 2 == 1, "Windows size must be odd!"

    eps = 2**-30
    pad_size = (win_size - 1) // 2

    # Padding
    vec_pad = np.empty((rows + win_size - 1, cols), dtype=vec.dtype)
    vec_pad[pad_size:-pad_size] = vec
    for i in range(pad_size):
        vec_pad[i] = vec[pad_size - i - 1]
        vec_pad[-i - 1] = vec[-pad_size + i]

    # Mean subtraction
    mean_subtracted = np.empty_like(vec)
    for i in range(rows):
        window = vec_pad[i : i + win_size]
        window_mean = np.mean(window, axis=0)
        mean_subtracted[i] = vec[i] - window_mean

    if variance_normalization:
        # Padding for variance calculation
        var_pad = np.empty((rows + win_size - 1, cols), dtype=vec.dtype)
        var_pad[pad_size:-pad_size] = mean_subtracted
        for i in range(pad_size):
            var_pad[i] = mean_subtracted[pad_size - i - 1]
            var_pad[-i - 1] = mean_subtracted[-pad_size + i]

        # Variance normalization
        output = np.empty_like(vec)
        for i in range(rows):
            window = var_pad[i : i + win_size]
            window_std = np.std(window, axis=0)
            output[i] = mean_subtracted[i] / (window_std + eps)
    else:
        output = mean_subtracted

    return output


# Function to process a single audio file
def process_audio(file_path, sr=16000, frame_ms=32, overlap_ms=4, n_mfcc=13, fmax=5000):
    audio, _ = librosa.load(file_path, sr=sr)
    hop_length = int(sr * (frame_ms - overlap_ms) / 1000)
    n_fft = int(sr * frame_ms / 1000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length, fmax=fmax)
    return mfcc.T


# Function to apply all versions of CMVN and measure time
def run_cmvn_test(audio_mfcc, win_size, variance_normalization=False):
    # Run all versions
    results = {}

    # 1. Original
    start_time = time.time()
    results["original"] = cmvnw_original(audio_mfcc, win_size=win_size, variance_normalization=variance_normalization)
    original_time = time.time() - start_time
    # print(f"Original function took: {original_time:.4f} seconds")

    # 4. Numba + SciPy Hybrid
    start_time = time.time()
    results["cmvnwR"] = cmvnwR(audio_mfcc, win_size=win_size, variance_normalization=variance_normalization)
    numba_scipy_time = time.time() - start_time
    # print(f"Numba + SciPy hybrid function took: {numba_scipy_time:.4f} seconds")

    # Compare results
    for key in results:
        if not np.allclose(results["original"], results[key], atol=1e-6, rtol=1e-6):
            print(f"Results do not match for {key}!")

    # Print speed gains
    # print(f"\nSpeed gains:")
    # print(f"Fully Numba: {original_time / numba_time:.2f}x")
    # print(f"Optimized (SciPy): {original_time / optimized_time:.2f}x")
    # print(f"Numba + SciPy hybrid: {original_time / numba_scipy_time:.2f}x\n")

    return original_time, numba_scipy_time  # , original_time / numba_scipy_time


# Main function to process audio from CSV
def process_audio_from_csv(csv_path, win_size=301, variance_normalization=True):
    df = pd.read_csv(csv_path)

    org_times = []
    optimised_times = []
    gain = []

    for idx, row in df.iterrows():
        audio_path = row["ref_wave"]
        print(f"\nProcessing file: {audio_path}")

        # Compute MFCC features
        mfcc = process_audio(audio_path, sr=16000, frame_ms=32, overlap_ms=4, n_mfcc=13, fmax=5000)

        # Run CMVN test
        resutlss = run_cmvn_test(mfcc, win_size=win_size, variance_normalization=variance_normalization)
        org_times.append(resutlss[0])
        optimised_times.append(resutlss[1])
        # gain.append(resutlss[2])

    return org_times, optimised_times  # , gain


# Run the process on your CSV file
csv_path = "audio_samples_1.csv"  # Update this to your correct CSV path
process_audio_from_csv(csv_path, win_size=301, variance_normalization=True)

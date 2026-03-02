import numpy as np
from numba import jit


# Original function
def cmvnw_original(vec, win_size=301, variance_normalization=False):
    eps = 2**-30
    rows, cols = vec.shape
    assert isinstance(win_size, int), "Size must be of type 'int'!"
    assert win_size % 2 == 1, "Windows size must be odd!"

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
        output = variance_normalized
    else:
        output = mean_subtracted

    return output


# Optimized function
import numpy as np


def cmvnw(vec, win_size=301, variance_normalization=False):
    eps = 2**-30
    rows, cols = vec.shape

    # Windows size must be odd.
    assert isinstance(win_size, int), "Size must be of type 'int'!"
    assert win_size % 2 == 1, "Window size must be odd!"

    # Padding
    pad_size = (win_size - 1) // 2
    vec_pad = np.pad(vec, ((pad_size, pad_size), (0, 0)), mode="symmetric")

    # Calculate the mean using convolution
    window = np.ones(win_size) / win_size
    mean = np.convolve(vec_pad[:, 0], window, mode="valid")
    mean = np.tile(mean[:, np.newaxis], (1, cols))

    # Mean subtraction
    mean_subtracted = vec - mean

    if variance_normalization:
        # Calculate the variance using convolution
        squared_window = np.ones(win_size) / win_size
        squared_mean = np.convolve(vec_pad[:, 0] ** 2, squared_window, mode="valid")
        variance = squared_mean - (mean[:, 0] ** 2 * win_size)
        variance = np.tile(variance[:, np.newaxis], (1, cols))

        # Variance normalization
        variance_normalized = mean_subtracted / (np.sqrt(variance) + eps)
        output = variance_normalized
    else:
        output = mean_subtracted

    return output


# Comparison function
def compare_outputs(original, optimized, name1="Original", name2="Optimized"):
    print(f"{name1} output shape: {original.shape}, dtype: {original.dtype}")
    print(f"{name2} output shape: {optimized.shape}, dtype: {optimized.dtype}")

    print(f"{name1} output contains NaN: {np.isnan(original).any()}")
    print(f"{name2} output contains NaN: {np.isnan(optimized).any()}")

    print(f"{name1} output contains inf: {np.isinf(original).any()}")
    print(f"{name2} output contains inf: {np.isinf(optimized).any()}")

    # Check if shapes match
    if original.shape != optimized.shape:
        print("Error: Shapes do not match!")
        return

    # Convert both to float64 for comparison
    original_float64 = original.astype(np.float64)
    optimized_float64 = optimized.astype(np.float64)

    # Compare
    is_close = np.allclose(original_float64, optimized_float64, atol=1e-6, rtol=1e-6)
    print(f"Outputs are close: {is_close}")

    if not is_close:
        diff = original_float64 - optimized_float64
        print(f"Max absolute difference: {np.max(np.abs(diff))}")
        print(f"Min difference: {np.min(diff)}")
        print(f"Median difference: {np.median(diff)}")

        # Find the indices of the maximum difference
        max_diff_index = np.unravel_index(np.argmax(np.abs(diff)), diff.shape)
        print(f"Max difference at index: {max_diff_index}")
        print(f"Original value at max diff: {original[max_diff_index]}")
        print(f"Optimized value at max diff: {optimized[max_diff_index]}")


# Test the functions
np.random.seed(0)  # for reproducibility
test_input = np.random.rand(10000, 13).astype(np.float32)

# Run all three functions
original_output = cmvnw_original(test_input, win_size=301, variance_normalization=True)
optimized_output = cmvnw_optimized(test_input, win_size=301, variance_normalization=True)

# Compare outputs
print("Comparing Original vs Optimized:")
compare_outputs(original_output, optimized_output)

# Timing comparison
import time


def time_function(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time


print("\nTiming comparison:")
_, original_time = time_function(cmvnw_original, test_input, win_size=301, variance_normalization=True)
_, optimized_time = time_function(cmvnw_optimized, test_input, win_size=301, variance_normalization=True)

print(f"Original function time: {original_time:.6f} seconds")
print(f"Optimized function time: {optimized_time:.6f} seconds")
print(f"Speedup: {original_time / optimized_time:.2f}x")

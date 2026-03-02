import numpy as np
from numpy.lib.stride_tricks import as_strided


def sliding_window_mfcc(mfcc, window_shape, step, pad_with_zeros=False):
    """
    Create sliding windows from the MFCC features, with optional padding.

    Args:
        mfcc (np.ndarray): MFCC feature matrix (n_mfcc, time_steps).
        window_shape (tuple): Shape of the sliding window (n_mfcc, cols_per_patch).
        step (int): Step size for the sliding window.
        pad_with_zeros (bool): If True, pad the MFCC array with zeros to ensure all columns are included.

    Returns:
        list: List of MFCC patches (each patch is a 2D numpy array).
    """
    n_mfcc, time_steps = mfcc.shape

    # If padding is enabled and time_steps does not align with step and window size
    if pad_with_zeros:
        padding_needed = (time_steps - window_shape[1]) % step
        if padding_needed != 0:
            padding_amount = step - padding_needed
            # Pad the MFCC matrix with zeros along the time_steps (columns)
            mfcc = np.pad(mfcc, ((0, 0), (0, padding_amount)), mode="constant", constant_values=0)
            time_steps = mfcc.shape[1]  # Update time_steps after padding

    window_mfcc = []

    # Create sliding windows
    for i in range(0, time_steps - window_shape[1] + 1, step):
        window_mfcc.append(mfcc[:, i : i + window_shape[1]])

    return window_mfcc


def sliding_window_mfcc_strided(mfcc, window_shape, step, pad_with_zeros=False):
    """
    Create sliding windows from the MFCC features using as_strided for efficiency.

    Args:
        mfcc (np.ndarray): MFCC feature matrix (n_mfcc, time_steps).
        window_shape (tuple): Shape of the sliding window (n_mfcc, cols_per_patch).
        step (int): Step size for the sliding window.
        pad_with_zeros (bool): If True, pad the MFCC array with zeros to ensure all columns are included.

    Returns:
        np.ndarray: 3D array of sliding windows.
    """
    n_mfcc, time_steps = mfcc.shape

    # If padding is enabled and time_steps does not align with step and window size
    if pad_with_zeros:
        padding_needed = (time_steps - window_shape[1]) % step
        if padding_needed != 0:
            padding_amount = step - padding_needed
            # Pad the MFCC matrix with zeros along the time_steps (columns)
            mfcc = np.pad(mfcc, ((0, 0), (0, padding_amount)), mode="constant", constant_values=0)
            time_steps = mfcc.shape[1]  # Update time_steps after padding

    # Define the shape and strides for the sliding windows
    new_shape = (n_mfcc, (time_steps - window_shape[1]) // step + 1, window_shape[1])
    new_strides = (mfcc.strides[0], step * mfcc.strides[1], mfcc.strides[1])

    # Use as_strided to generate the sliding windows
    window_mfcc = as_strided(mfcc, shape=new_shape, strides=new_strides)

    return window_mfcc


# Fake 2D data to simulate MFCC features
fake_mfcc = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18]])

# Parameters
window_shape = (3, 3)  # (n_mfcc, cols_per_patch)
step = 2  # Step size for sliding window

# Without padding
print("Without Padding:")
patches_no_padding = sliding_window_mfcc(fake_mfcc, window_shape, step, pad_with_zeros=False)
for idx, patch in enumerate(patches_no_padding):
    print(f"Patch {idx + 1}:\n{patch}\n")

# With padding
print("With Padding:")
patches_with_padding = sliding_window_mfcc(fake_mfcc, window_shape, step, pad_with_zeros=True)
patches_with_padding_strided = sliding_window_mfcc_strided(fake_mfcc, window_shape, step, pad_with_zeros=True)
for idx, patch in enumerate(patches_with_padding):
    print(f"Patch {idx + 1}:\n{patch}\n")
print("##############")
for idx, patch in enumerate(patches_with_padding_strided.transpose(1, 0, 2)):
    print(f"Patch {idx + 1}:\n{patch}\n")

import librosa
import numpy as np
from numpy.lib.stride_tricks import as_strided


# 1. Load a sample audio file from librosa
audio_file = librosa.example("trumpet")  # Replace with your own file path if needed
ref_signal, sr = librosa.load(audio_file, sr=1600)  # Load with original sample rate

# 2. Compute MFCC features for the reference signal
n_mfcc = 13  # Number of MFCC coefficients
hop_length = 256  # You can adjust this if needed
n_fft = 2048  # You can adjust this if needed
win_length = 512
mfcc_ref = librosa.feature.mfcc(y=ref_signal, sr=sr, n_mfcc=n_mfcc, fmax=16000, win_length=win_length, hop_length=hop_length)

# 3. Get time stamps for each frame in the MFCC array
num_frames_ref = mfcc_ref.shape[1]
time_ref = librosa.frames_to_time(range(num_frames_ref), sr=sr, hop_length=hop_length, n_fft=n_fft)

# Print the MFCC shape and first few time stamps
print("MFCC shape:", mfcc_ref.shape)
print("First few time stamps:", time_ref[:5])


# 4. Define the sliding window function
def sliding_window_mfcc_strided(mfcc, window_shape, step, time_stamps, pad_with_zeros=False):
    """
    Create sliding windows from the MFCC features using as_strided for efficiency,
    and return the MFCC patches and the time ranges for each patch separately.

    Args:
        mfcc (np.ndarray): MFCC feature matrix (n_mfcc, time_steps).
        window_shape (tuple): Shape of the sliding window (n_mfcc, cols_per_patch).
        step (int): Step size for the sliding window.
        time_stamps (np.ndarray): Array of time stamps for each column (frame) of the MFCC matrix.
        pad_with_zeros (bool): If True, pad the MFCC array with zeros to ensure all columns are included.

    Returns:
        np.ndarray: 3D array of sliding MFCC windows (n_mfcc, num_patches, cols_per_patch).
        list: List of time ranges for each patch as (start_time, end_time).
    """
    n_mfcc, time_steps = mfcc.shape

    # If padding is enabled and time_steps do not align with step and window size
    if pad_with_zeros:
        padding_needed = (time_steps - window_shape[1]) % step
        if padding_needed != 0:
            padding_amount = step - padding_needed
            # Pad the MFCC matrix with zeros along the time_steps (columns)
            mfcc = np.pad(mfcc, ((0, 0), (0, padding_amount)), mode="constant", constant_values=0)
            time_steps = mfcc.shape[1]  # Update time_steps after padding

            # Calculate time increment based on the last two values of the time_stamps array
            time_increment = time_stamps[-1] - time_stamps[-2]

            # Extend the time_stamps array to account for the padded zeros
            extra_times = [time_stamps[-1] + (i + 1) * time_increment for i in range(padding_amount)]
            time_stamps = np.concatenate([time_stamps, extra_times])

    # Define the shape and strides for the sliding windows
    new_shape = (n_mfcc, (time_steps - window_shape[1]) // step + 1, window_shape[1])
    new_strides = (mfcc.strides[0], step * mfcc.strides[1], mfcc.strides[1])

    # Use as_strided to generate the sliding windows
    window_mfcc = as_strided(mfcc, shape=new_shape, strides=new_strides)

    # Calculate the time range for each patch
    patch_times = []
    for i in range(new_shape[1]):  # new_shape[1] is the number of patches
        start_frame = i * step
        end_frame = start_frame + window_shape[1] - 1
        start_time = time_stamps[start_frame]
        end_time = time_stamps[end_frame] if end_frame < len(time_stamps) else time_stamps[-1]  # Handle case where end_frame exceeds
        patch_times.append((start_time, end_time))

    # Return the MFCC patches and their corresponding time ranges separately
    return window_mfcc, patch_times


# 5. Apply the sliding window function to the MFCC
xx = 6
window_shape = (n_mfcc, xx)  # 5 columns per patch (example)
step = 3  # Step size for the sliding window (example)

mfcc_patches, patch_times = sliding_window_mfcc_strided(mfcc_ref, window_shape, step, time_ref, pad_with_zeros=True)

# 6. Verify the output: MFCC patches and corresponding time ranges
print(f"Number of patches: {len(patch_times)}")
print("Shape of windowed MFCC patches:", mfcc_patches.shape)
print("First few patches' time ranges:")
for i in range(xx):
    print(f"Patch {i+1}: from {patch_times[i][0]:.3f}s to {patch_times[i][1]:.3f}s")

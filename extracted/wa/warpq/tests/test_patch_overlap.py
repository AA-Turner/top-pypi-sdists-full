import numpy as np

# Example array of size 13x500
arr = np.random.rand(13, 103)

# Parameters
patch_size = 9  # number of columns per patch
step_size = 6  # step size in columns (controls how far to move between patches)

# Initialize lists to store start and end points of each patch
start_end_points = []

# Loop through the array, creating patches with a given step size
for start_col in range(0, arr.shape[1] - patch_size + 1, step_size):
    # Define start and end points for the current patch
    start_point = start_col
    end_point = start_col + patch_size

    # Store the start and end points
    start_end_points.append((start_point, end_point))

    # (Optional) If you want to extract the patch itself:
    patch = arr[:, start_col:end_point]  # Extract patch

    # You can process the patch as needed in your code

# Print start and end points for each patch
for idx, (start, end) in enumerate(start_end_points):
    print(f"Patch {idx+1}: Start Col = {start}, End Col = {end}")

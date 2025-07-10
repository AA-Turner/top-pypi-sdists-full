from AOT_biomaps.Config import config

import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from scipy.interpolate import RegularGridInterpolator
from scipy.signal import hilbert as np_hilbert
if config.get_process()  == 'gpu':
    import cupy as cp
    from cupyx.scipy.signal import hilbert as cp_hilbert
    import pynvml

def reshape_field(field,factor):
    """
    Downsample the acoustic field using interpolation to reduce its size for faster processing.
    This method uses interpolation to estimate values on a coarser grid.
    """
    try:
        if field is None:
            raise ValueError("Acoustic field is not generated. Please generate the field first.")

        if len(factor) == 3:
            # Create new grid for 3D field
            x = np.arange(field.shape[0])
            y = np.arange(field.shape[1])
            z = np.arange(field.shape[2])

            # Create interpolating function
            interpolator = RegularGridInterpolator((x, y, z), field)

            # Create new coarser grid points
            x_new = np.linspace(0, field.shape[0] - 1, field.shape[0] // factor[0])
            y_new = np.linspace(0, field.shape[1] - 1, field.shape[1] // factor[1])
            z_new = np.linspace(0, field.shape[2] - 1, field.shape[2] // factor[2])

            # Create meshgrid for new points
            x_grid, y_grid, z_grid = np.meshgrid(x_new, y_new, z_new, indexing='ij')

            # Interpolate values
            points = np.stack((x_grid.flatten(), y_grid.flatten(), z_grid.flatten()), axis=-1)
            smoothed_field = interpolator(points).reshape(x_grid.shape)

            return smoothed_field

        elif len(factor) == 4:
            # Create new grid for 4D field
            x = np.arange(field.shape[0])
            y = np.arange(field.shape[1])
            z = np.arange(field.shape[2])
            w = np.arange(field.shape[3])

            # Create interpolating function
            interpolator = RegularGridInterpolator((x, y, z, w), field)

            # Create new coarser grid points
            x_new = np.linspace(0, field.shape[0] - 1, field.shape[0] // factor[0])
            y_new = np.linspace(0, field.shape[1] - 1, field.shape[1] // factor[1])
            z_new = np.linspace(0, field.shape[2] - 1, field.shape[2] // factor[2])
            w_new = np.linspace(0, field.shape[3] - 1, field.shape[3] // factor[3])

            # Create meshgrid for new points
            x_grid, y_grid, z_grid, w_grid = np.meshgrid(x_new, y_new, z_new, w_new, indexing='ij')

            # Interpolate values
            points = np.stack((x_grid.flatten(), y_grid.flatten(), z_grid.flatten(), w_grid.flatten()), axis=-1)
            smoothed_field = interpolator(points).reshape(x_grid.shape)

            return smoothed_field

        else:
            raise ValueError("Invalid dimension for downsampling. Supported dimensions are: 3D, 4D.")

    except Exception as e:
        print(f"Error in interpolate_reshape_field method: {e}")
        raise

def calculate_envelope_squared(field, isGPU= config.get_process() == 'gpu'):
    """
    Calculate the analytic envelope of the acoustic field using either CPU or GPU.

    Parameters:
    - use_gpu (bool): If True, use GPU for computation. Otherwise, use CPU.

    Returns:
    - envelope (numpy.ndarray or cupy.ndarray): The squared analytic envelope of the acoustic field.
    """
    try:                
        if field is None:
            raise ValueError("Acoustic field is not generated. Please generate the field first.")

        if isGPU:

            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming you want to check the first GPU
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            total_memory = info.total / (1024 ** 2)  # Convert to MB
            used_memory = info.used / (1024 ** 2)  # Convert to MB
            free_memory = int(total_memory - used_memory)
            
            if free_memory < field.nbytes / (1024 ** 2):
                print(f"GPU memory insufficient {int(field.nbytes / (1024 ** 2))} MB, Free GPU memory: {free_memory} MB, falling back to CPU.")
                isGPU = False
                acoustic_field = np.asarray(field)
            else:
                acoustic_field = cp.asarray(field)                   
        else:
            acoustic_field = np.asarray(field)

        if len(acoustic_field.shape) not in [3, 4]:
            raise ValueError("Input acoustic field must be a 3D or 4D array.")

        def process_slice(slice_index,isGPU):
            """Calculate the envelope for a given slice of the acoustic field."""
            if isGPU:
                hilbert = cp_hilbert
            else:
                hilbert = np_hilbert

            if len(acoustic_field.shape) == 3:
                return np.abs(hilbert(acoustic_field[slice_index], axis=0))**2
            elif len(acoustic_field.shape) == 4:
                envelope_slice = np.zeros_like(acoustic_field[slice_index])
                for y in range(acoustic_field.shape[2]):
                    for z in range(acoustic_field.shape[1]):
                        envelope_slice[:, z, y, :] = np.abs(hilbert(acoustic_field[slice_index][:, z, y, :], axis=0))**2
                return envelope_slice

        # Determine the number of slices to process in parallel
        num_slices = acoustic_field.shape[0]
        slice_indices = [(i,) for i in range(num_slices)]

        if isGPU:
            # Use GPU directly without multithreading
            envelopes = [process_slice(slice_index,isGPU) for slice_index in slice_indices]
        else:
            # Use ThreadPoolExecutor to parallelize the computation on CPU
            with ThreadPoolExecutor() as executor:
                envelopes = list(executor.map(lambda index: process_slice(index,isGPU), slice_indices))

        # Combine the results into a single array
        if isGPU:
            return cp.stack(envelopes, axis=0).get()
        else:
            return np.stack(envelopes, axis=0)

    except Exception as e:
        print(f"Error in calculate_envelope_squared method: {e}")
        raise

def getPattern(pathFile):
    """
    Get the pattern from a file path.

    Args:
        pathFile (str): Path to the file containing the pattern.

    Returns:
        str: The pattern string.
    """
    try:
        # Pattern between first _ and last _
        pattern = os.path.basename(pathFile).split('_')[1:-1]
        pattern_str = ''.join(pattern)
        return pattern_str
    except Exception as e:
        print(f"Error reading pattern from file: {e}")
        return None

def getAngle(pathFile):
    """
    Get the angle from a file path.

    Args:
        pathFile (str): Path to the file containing the angle.

    Returns:
        int: The angle in degrees.
    """
    try:
        # Angle between last _ and .
        angle_str = os.path.basename(pathFile).split('_')[-1].replace('.', '')
        if angle_str.startswith('0'):
            angle_str = angle_str[1:]
        elif angle_str.startswith('1'):
            angle_str = '-' + angle_str[1:]
        else:
            raise ValueError("Invalid angle format in file name.")
        return int(angle_str)
    except Exception as e:
        print(f"Error reading angle from file: {e}")
        return None

def next_power_of_2(n):
    """Calculate the next power of 2 greater than or equal to n."""
    return int(2 ** np.ceil(np.log2(n)))
        

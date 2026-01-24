"""
Core functionality for reading and writing EXR files.
"""

import numpy as np
import OpenEXR
import Imath


def read_exr(path: str) -> np.ndarray:
    """
    Read an EXR file and return it as a numpy array.
    
    Args:
        path (str): Path to the EXR file
        
    Returns:
        np.ndarray: Image data as (H, W, C) array where C is 3 (RGB) or 4 (RGBA)
        
    Raises:
        ValueError: If no RGB(A) channels are found in the EXR file
        FileNotFoundError: If the file doesn't exist
    """
    exr_file = OpenEXR.InputFile(path)
    dw = exr_file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    # Standard channel order for RGB(A)
    standard_channels = ['R', 'G', 'B', 'A']
    file_channels = list(exr_file.header()['channels'].keys())
    # Determine which standard channels are present
    present_channels = [c for c in standard_channels if c in file_channels]
    if not present_channels:
        raise ValueError("No RGB(A) channels found in EXR file.")
    channel_arrays = []
    for c in present_channels:
        channel_data = exr_file.channel(c, Imath.PixelType(Imath.PixelType.FLOAT))
        arr = np.frombuffer(channel_data, dtype=np.float32).reshape(size[1], size[0])
        channel_arrays.append(arr)
    # Stack into a (H, W, C) array, where C is 3 (RGB) or 4 (RGBA)
    return np.stack(channel_arrays, axis=-1)


def write_exr(path: str, img: np.ndarray):
    """
    Write a numpy array to an EXR file as RGB or RGBA depending on channel count.
    
    Args:
        path (str): Output path for the EXR file
        img (np.ndarray): Image data with shape (H, W, 3) or (H, W, 4), dtype float32 or float64
        
    Raises:
        ValueError: If img doesn't have 3 or 4 channels
    """
    if img.shape[2] == 3:
        channels = ['R', 'G', 'B']
    elif img.shape[2] == 4:
        channels = ['R', 'G', 'B', 'A']
    else:
        raise ValueError("img must have 3 (RGB) or 4 (RGBA) channels")
    header = OpenEXR.Header(img.shape[1], img.shape[0])
    # Set channel types
    header['channels'] = {c: Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)) for c in channels}
    exr_file = OpenEXR.OutputFile(path, header)
    # Prepare channel data
    channel_data = {c: img[..., i].astype(np.float32).tobytes() for i, c in enumerate(channels)}
    exr_file.writePixels(channel_data)
    exr_file.close()


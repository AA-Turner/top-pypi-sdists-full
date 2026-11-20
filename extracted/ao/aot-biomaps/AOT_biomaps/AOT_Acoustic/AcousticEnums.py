from enum import Enum

class TypeSim(Enum):
    """
    Enum for the type of simulation to be performed.

    Selection of simulation types:
    - KWAVE: k-Wave simulation.
    - FIELD2: Field II simulation.
    - HYDRO: Hydrophone acquisition.
    """
    KWAVE = 'k-wave'
    """k-Wave simulation."""

    FIELD2 = 'Field2'
    """Field II simulation."""

    HYDRO = 'Hydrophone'
    """Hydrophone acquisition."""

    SIMPLE_SIM = 'SimpleSim'
    """Simple simulation for testing purposes."""

class Dim(Enum):
    """
    Enum for the dimension of the acoustic field.

    Selection of dimensions:
    - D2: 2D field.
    - D3: 3D field.
    """
    D2 = '2D'
    """2D field."""
    D3 = '3D'
    """3D field."""

class FormatSave(Enum):
    """
    Enum for different file formats to save the acoustic field.

    Selection of file formats:
    - HDR_IMG: Interfile format (.hdr and .img).
    - H5: HDF5 format (.h5).
    - NPY: NumPy format (.npy).
    """
    HDR_IMG = '.hdr'
    """Interfile format (.hdr and .img)."""
    H5 = '.h5'
    """HDF5 format (.h5)."""
    NPY = '.npy'
    """NumPy format (.npy)."""

class WaveType(Enum):
    """
    Enum for different types of acoustic waves.

    Selection of wave types:
    - FocusedWave: A wave type where the energy is focused at a specific point.
    - StructuredWave: A wave type characterized by a specific pattern or structure.
    - PlaneWave: A wave type where the wavefronts are parallel and travel in a single direction.
    """
    FocusedWave = 'focus'
    """A wave type where the energy is focused at a specific point."""
    StructuredWave = 'structured'
    """A wave type characterized by a specific pattern or structure."""
    PlaneWave = 'plane'
    """A wave type where the wavefronts are parallel and travel in a single direction."""

class ApodType(Enum):
    """
    Enum for different types of apodization.

    Selection of apodization types:
    - Rectangular: A simple rectangular apodization.
    - Hanning: A Hanning window apodization.
    - Hamming: A Hamming window apodization.
    - Blackman: A Blackman window apodization.
    - gaussian: A Gaussian window apodization.
    """
    Rectangular = 'rectangular'
    """A simple rectangular apodization."""
    Hanning = 'hanning'
    """A Hanning window apodization."""
    Hamming = 'hamming'
    """A Hamming window apodization."""
    Blackman = 'blackman'
    """A Blackman window apodization."""
    Gaussian = 'gaussian'
    """A Gaussian window apodization."""
    Tukey = 'tukey'
    """A Tukey window apodization."""
"""Acoustic-field generation and I/O for AOT-biomaps.

The :class:`AcousticField` base class provides common functionality for
k-Wave, SIMPLE_SIM, and hydrophone-derived acoustic fields. GPU k-Wave envelope
generation uses a streaming I/Q pipeline: pressure is consumed one time step at
a time and the envelope is written directly to a VRAM output buffer.

When the complete output does not fit in VRAM, a dynamically sized GPU ring
buffer is combined with two pinned host staging buffers. CUDA events protect
ring-buffer reuse while a dedicated CUDA stream transfers completed chunks to
host memory asynchronously.
"""

from __future__ import annotations

import copy
import logging
import math
import os
import platform
import shutil
import subprocess
import tempfile
import uuid
from abc import ABC, abstractmethod

import h5py
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert as scipy_hilbert

from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Acoustic.AcousticEnums import Dim, FormatSave, TypeSim, WaveType
from AOT_biomaps.AOT_Acoustic.AcousticTools import (
    get_gpu_memory_info,
    _resample_axis,
    allocate_pinned_staging_buffers,
    calculate_envelope,
    calculate_envelope_squared,
    compute_target_sizes,
    get_gpu_output_budget_bytes,
    get_iq_envelope_kernel,
    get_transfer_chunk_frames,
    loadmat,
    resample_bandlimited
)
from AOT_biomaps.AOT_Medium import Medium
from AOT_biomaps.Settings import Params

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the runtime
    cp = None
    CUPY_AVAILABLE = False


def _to_numpy_array(array):
    """Return a NumPy view/copy of an array, handling CuPy arrays explicitly."""
    if CUPY_AVAILABLE and isinstance(array, cp.ndarray):
        return cp.asnumpy(array)
    return np.asarray(array)


# k-Wave Python API imports are optional so that the package remains importable
# for users who only load or post-process previously generated fields.
KWAVE_AVAILABLE = False
KWAVE_STREAMING_AVAILABLE = False
KWAVE_BINARIES_AVAILABLE = False

try:
    import kwave
    from kwave.utils.signals import tone_burst
    from kwave.ksource import kSource
    from kwave.ksensor import kSensor
    KWAVE_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the optional k-Wave package
    kwave = None
    tone_burst = None
    kSource = None
    kSensor = None

try:
    from kwave.solvers.kspace_solver import Simulation
    from kwave.solvers.validation import validate_simulation
    from kwave.kspaceFirstOrder import _expand_for_pml_outside
    KWAVE_STREAMING_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the installed k-Wave version
    Simulation = None
    validate_simulation = None
    _expand_for_pml_outside = None

try:
    from kwave.kspaceFirstOrder import kspaceFirstOrder
except ImportError:  # pragma: no cover - some k-Wave versions expose only Simulation
    kspaceFirstOrder = None


def _detect_kwave_cuda_binary():
    """Return whether the installed k-Wave CUDA executable can be launched."""
    if kwave is None:
        return False
    binary_root = os.path.join(os.path.dirname(kwave.__file__), "bin")
    system = platform.system().lower()
    if system == "linux":
        binary_path = os.path.join(binary_root, "linux", "kspaceFirstOrder-CUDA")
    elif system == "darwin":
        binary_path = os.path.join(binary_root, "mac", "kspaceFirstOrder-CUDA")
    elif system == "windows":
        binary_path = os.path.join(binary_root, "windows", "kspaceFirstOrder-CUDA.exe")
    else:
        return False

    if not os.path.isfile(binary_path):
        return False
    try:
        result = subprocess.run(
            [binary_path, "-h"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


KWAVE_BINARIES_AVAILABLE = _detect_kwave_cuda_binary()


# k-Wave's C++ wrapper may decode subprocess output using the platform locale.
# Install the encoding fix once, rather than toggling Popen around each call;
# this also avoids races when independent GPU simulations run in Python threads.
_original_popen = subprocess.Popen


class _UTF8Popen(_original_popen):
    """Subprocess.Popen subclass that defaults text-mode pipes to UTF-8."""

    def __init__(self, *args, **kwargs):
        if kwargs.get("text", False) or kwargs.get("universal_newlines", False):
            kwargs.setdefault("encoding", "utf-8")
            kwargs.setdefault("errors", "replace")
        super().__init__(*args, **kwargs)


subprocess.Popen = _UTF8Popen


####### ABSTRACT CLASS #######

class AcousticField(ABC):
    """
    Abstract class to generate and manipulate acoustic fields for ultrasound imaging.
    Provides methods to initialize parameters, generate fields, save and load data, and calculate envelopes.

    Principal parameters:
    - field: Acoustic field data.
    - burst: Burst signal used for generating the field for each piezo elements.
    - delayedSignal: Delayed burst signal for each piezo element.
    - medium: Medium properties for k-Wave simulation. Because field2 and Hydrophone simulation are not implemented yet, this attribute is set to None for these types of simulation.
    """

    def __init__(self, params, medium):
        """Initialize an acoustic-field object.

        Parameters
        ----------
        params : Params
            AOT-biomaps parameter object.
        medium : Medium
            Medium and simulation-grid description.
        """
        if not isinstance(params, Params):
            raise TypeError("params must be an instance of Params.")
        if not isinstance(medium, Medium):
            raise TypeError("medium must be an instance of Medium.")

        self.params = params
        self.medium = medium
        self.waveType = None
        self.field = None
        self.burst = None
        self.delayedSignal = None
        self.last_decimation = None

        if self.params.acoustic["typeSim"] == TypeSim.KWAVE.value:
            self.generate_burst_signal()

        dim_value = self.params.acoustic["dim"]
        if dim_value == Dim.D3.value and self.params.general.get("Yrange") is None:
            raise ValueError("Yrange must be provided for 3D acoustic fields.")

    def __del__(self):
        """Release references owned by the acoustic-field object."""
        for attribute in ("field", "burst", "delayedSignal"):
            try:
                setattr(self, attribute, None)
            except Exception:
                # Destructors must not raise during interpreter shutdown.
                pass

    def generate_field(
        self,
        burst=None,
        isGPU=None,
        GPUdevice=None,
        generation_type="envelope_squared",
        show_log=False,
        backend=None,
        keep_on_gpu=False,
        free_vram=True,
        envelope_lpf_hz=None,
        vram_fraction=0.95,
        accumulate_max_bytes=None,
        host_staging_fraction=1.0 / 16.0,
        host_output_path=None,
        validate_iq=False,
        simulation_mode=None,
    ):
        """Generate the acoustic field for the selected simulation type.

        k-Wave GPU envelope generation uses the streaming I/Q implementation when the required Python solver interfaces are available. 
        If the complete result cannot fit in VRAM, output frames are accumulated in a GPU ring and copied asynchronously to host memory in large chunks.

        Parameters
        ----------
        generation_type : {"envelope_squared", "envelope", "field"}
            Requested output representation.
        keep_on_gpu : bool
            Keep the final resampled result on the GPU when it fits in currently available VRAM. If the raw streamed output is too large, the result is assembled and resampled on the host before an optional final upload.
        vram_fraction : float
            Fraction of currently allocatable VRAM offered to the output ring.
        accumulate_max_bytes : int or None
            Optional caller-specified upper bound for the output buffer.
        host_staging_fraction : float
            Fraction of currently available host RAM offered to the two pinned transfer buffers. Their actual size is computed dynamically.
        host_output_path : str or None
            Optional .npy path for streamed output. When omitted, host RAM is used for the assembled result.
        validate_iq : bool
            Store one central-voxel pressure trace and compare the I/Q envelope against a Hilbert reference after the simulation. Disabled by default to avoid diagnostic allocations.
        """
        if isGPU is None:
            isGPU = config.get_process() == "gpu"

        if self.medium.medium_properties is None:
            raise ValueError("Medium properties are not defined. Generate or load a valid Medium first.")

        logging.getLogger("root").setLevel(logging.ERROR)
        simulation_type = self.params.acoustic["typeSim"]
        dimension = self.params.acoustic["dim"]

        if simulation_type == TypeSim.FIELD2.value:
            raise NotImplementedError("FIELD2 simulation is not implemented.")
        elif simulation_type == TypeSim.SIMPLE_SIM.value:
            self.field = self._generate_acoustic_field_SIMPLE_SIM(burst=burst, show_log=show_log)
        elif simulation_type == TypeSim.KWAVE.value:
            if dimension == Dim.D3.value:
                raise NotImplementedError("3D k-Wave generation is not implemented.")
            if dimension != Dim.D2.value:
                raise ValueError(f"Unsupported k-Wave dimension: {dimension!r}.")
            if simulation_mode not in ("stream", "batch", None):
                raise ValueError(f"Invalid simulation_mode: {simulation_mode!r}. Supported modes are 'stream', 'batch', or None (auto-select).")
            
            self.field = self._generate_acoustic_field_KWAVE_2D(
                burst=burst,
                isGPU=isGPU,
                GPUdevice=GPUdevice,
                generation_type=generation_type,
                show_log=show_log,
                keep_on_gpu=keep_on_gpu,
                free_vram=free_vram,
                backend=backend,
                envelope_lpf_hz=envelope_lpf_hz,
                accumulate_max_bytes=accumulate_max_bytes,
                vram_fraction=vram_fraction,
                host_staging_fraction=host_staging_fraction,
                host_output_path=host_output_path,
                validate_iq=validate_iq,
                simulation_mode=simulation_mode,
            )
        elif simulation_type == TypeSim.HYDRO.value:
            raise ValueError("Hydrophone fields are loaded from acquisitions; they cannot be simulated.")
        else:
            raise ValueError(f"Unsupported simulation type: {simulation_type!r}.")

    def save_field(self, filePath, formatSave=FormatSave.HDR_IMG):
        """
        Save the acoustic field to a file in the specified format.

        Parameters:
        - filePath (str): The path where the file will be saved.
        """
        try:
            if not isinstance(formatSave, FormatSave):
                raise TypeError("formatSave must be a FormatSave enum value.")
            if formatSave == FormatSave.HDR_IMG:
                self._save2D_HDR_IMG(filePath)
            elif formatSave == FormatSave.H5:
                self._save2D_H5(filePath)
            elif formatSave == FormatSave.NPY:
                self._save2D_NPY(filePath)
            else:
                raise ValueError(f"Unsupported format: {formatSave!r}.")
        except Exception as e:
            print(f"[AOT-biomaps] Error in save_field method: {e}")
            raise

    def load_field(self, folderPath, formatSave=FormatSave.HDR_IMG, nameBlock=None):
        """Load an acoustic field from Interfile, HDF5, or NumPy storage."""
        if not isinstance(formatSave, FormatSave):
            raise TypeError("formatSave must be a FormatSave enum value.")

        simulation_type = self.params.acoustic["typeSim"]
        dimension = self.params.acoustic["dim"]
        field_name = self.get_name_field()

        if simulation_type in (TypeSim.KWAVE.value, TypeSim.SIMPLE_SIM.value):
            if dimension == Dim.D3.value:
                raise NotImplementedError("3D field loading is not implemented for this format.")
            if formatSave == FormatSave.HDR_IMG:
                self._load_fieldKWAVE_XZ(os.path.join(folderPath, field_name + formatSave.value))
            elif formatSave == FormatSave.H5:
                self._load_field_h5(folderPath, nameBlock)
            elif formatSave == FormatSave.NPY:
                self.field = np.load(os.path.join(folderPath, field_name + formatSave.value), mmap_mode="r")
            else:
                raise ValueError(f"Unsupported field format: {formatSave!r}.")

        elif simulation_type == TypeSim.HYDRO.value:
            if formatSave == FormatSave.HDR_IMG:
                raise ValueError("HDR_IMG is not supported for hydrophone acquisitions.")
            h5_path = os.path.join(folderPath, field_name + ".h5")
            mat_path = os.path.join(folderPath, "PARAMS_" + field_name + ".mat")
            if formatSave == FormatSave.H5:
                if dimension == Dim.D2.value:
                    self.field, self.params.general["Xrange"], self.params.general["Zrange"] = (self._load_fieldHYDRO_XZ(h5_path, mat_path))
                elif dimension == Dim.D3.value:
                    self._load_fieldHYDRO_XYZ(h5_path, mat_path)
                else:
                    raise ValueError(f"Unsupported hydrophone dimension: {dimension!r}.")
            elif formatSave == FormatSave.NPY:
                npy_path = folderPath if os.path.isfile(folderPath) else os.path.join(folderPath, field_name + formatSave.value)
                self.field = np.load(npy_path, mmap_mode="r")
        else:
            raise ValueError(f"Unsupported simulation type for loading: {simulation_type!r}.")

    @abstractmethod
    def get_name_field(self):
        """Return the stable field name used by save/load operations."""
        raise NotImplementedError

    ## DISPLAY METHODS ##

    def plot_burst_signal(self, figsize=(4,3)):
        """
        Plot the burst signal used for generating the acoustic field.
        """
        try:
            time2plot = np.arange(len(self.burst)) * float(self.medium.kgrid.dt) * 1e6
            plt.figure(figsize=figsize)
            plt.plot(time2plot, self.burst)
            plt.title('Excitation burst signal')
            plt.xlabel('Time (µs)')
            plt.ylabel('Amplitude')
            plt.grid()
            plt.show()
        except Exception as e:
            print(f"[AOT-biomaps] Error in plot_burst_signal method: {e}")
            raise

    def animated_plot_AcousticField(self, desired_duration_ms = 5000, save_dir=None,figsize=(4,3)):
        """
        Plot synchronized animations of A_matrix slices for selected angles.

        Args:
            step (int): Time step between frames (default is every 10 frames).
            save_dir (str): Directory to save the animation gif; if None, animation will not be saved.

        Returns:
            ani: Matplotlib FuncAnimation object.
        """
        try:

            if self.field is None:
                raise ValueError("No acoustic field is available to animate.")
            is_gpu_field = CUPY_AVAILABLE and isinstance(self.field, cp.ndarray)
            field_for_limits = self.field[:, 20:, :] if self.field.shape[1] > 20 else self.field
            if is_gpu_field:
                maxF = float(cp.max(field_for_limits).get())
                minF = float(cp.min(field_for_limits).get())
            else:
                maxF = float(np.max(field_for_limits))
                minF = float(np.min(field_for_limits))
            # Set the maximum embedded animation size to 100 MB
            plt.rcParams['animation.embed_limit'] = 100

            if save_dir is not None:
                os.makedirs(save_dir, exist_ok=True)

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=figsize)

            # Set main title
            wave_type = getattr(self.waveType, "value", self.waveType)
            if wave_type == WaveType.FocusedWave.value:
                fig.suptitle("[System Matrix Animation] Focused Wave", y=0.98)
            elif wave_type == WaveType.PlaneWave.value:
                fig.suptitle(f"[System Matrix Animation] Plane Wave | Angles {self.angle}°", y=0.98)
            elif wave_type == WaveType.StructuredWave.value:
                fig.suptitle(f"[System Matrix Animation] Structured Wave | Pattern structure: {self.pattern.activeList} | Angles {self.angle}°", y=0.98)
            else:

                raise ValueError("Invalid wave type. Supported types are: FocusedWave, PlaneWave, StructuredWave.")

            # Initial plot
            im = ax.imshow(cp.asnumpy(self.field[0, :, :]) if is_gpu_field else self.field[0, :, :], extent=(self.params.general['Xrange'][0] * 1000, self.params.general['Xrange'][-1] * 1000, self.params.general['Zrange'][-1] * 1000, self.params.general['Zrange'][0] * 1000), vmin = 1.2*minF, vmax=0.8*maxF, aspect='equal', cmap='jet', animated=True)
            ax.set_title(f"t = 0 ms")
            ax.set_xlabel("x (mm)")
            ax.set_ylabel("z (mm)")

            # Effective time step of self.field (decimated fields are NOT
            # sampled at 1/f_AQ)
            dec = getattr(self, 'last_decimation', None)
            dt_frame = dec['dt'] if dec else 1.0 / float(self.params.acoustic['f_AQ'])

            # Unified update function for all subplots
            def update(frame):
                frame_data = self.field[frame, :, :]
                if is_gpu_field:
                    frame_data = cp.asnumpy(frame_data)
                im.set_data(frame_data)
                ax.set_title(f"t = {frame * dt_frame * 1000:.2f} ms")
                return [im]

            interval = desired_duration_ms / self.field.shape[0]

            # Create animation
            ani = animation.FuncAnimation(fig, update, frames=range(0, self.field.shape[0]), interval=interval, blit=True)

            # Save animation if needed
            if save_dir is not None:
                if self.waveType == WaveType.FocusedWave:
                    save_filename = f"Focused_Wave_.gif"
                elif self.waveType == WaveType.PlaneWave:
                    save_filename = f"Plane_Wave_{self._format_angle()}.gif"
                else:
                    save_filename = f"Structured_Wave_PatternStructure_{self.pattern.activeList}_{self._format_angle()}.gif"
                save_path = os.path.join(save_dir, save_filename)
                ani.save(save_path, writer='pillow', fps=20)
                print(f"[AOT-biomaps] Saved: {save_path}")

            plt.close(fig)

            try:
                from IPython.display import HTML
                return HTML(ani.to_jshtml())
            except ImportError:
                print("[AOT-biomaps] IPython not available. Returning animation object without HTML wrapper. (install aot-biomaps[notebook] to enable HTML display in Jupyter notebooks)")
                return ani
        except Exception as e:
            print(f"[AOT-biomaps] Error creating animation: {e}")
            return None

    def show(self, use_dB=False, reference=1e6, Vmax=None, figsize=(4, 3)):
        """Display the maximum-intensity projection of the squared envelope.

        The temporal maximum is computed on the device when ``self.field`` is a
        CuPy array. Only the final 2-D projection is transferred to the host.
        """
        if self.field is None:
            raise ValueError("Field data is not available. Generate or load a field first.")
        if reference <= 0:
            raise ValueError("reference must be positive.")

        is_gpu_field = CUPY_AVAILABLE and isinstance(self.field, cp.ndarray)
        xp = cp if is_gpu_field else np
        minimum = float(xp.min(self.field).get()) if is_gpu_field else float(np.min(self.field))
        if minimum < 0:
            raise ValueError("The field contains negative values; an envelope is expected.")

        # Taking the maximum before sqrt/log is valid because both transforms
        # are monotonic for non-negative envelope-squared values.
        projection_squared = xp.max(self.field, axis=0)
        if use_dB:
            data_to_show = 10.0 * xp.log10(xp.maximum(projection_squared, 1e-30) / (reference ** 2))
            unit_label = f"dB re {reference / 1e6:g} MPa"
            vmax = 0.0 if Vmax is None else Vmax
        else:
            data_to_show = xp.sqrt(projection_squared) / 1e6
            unit_label = "MPa"
            vmax = 0.85 * float(xp.max(data_to_show).get()) if Vmax is None and is_gpu_field else (0.85 * float(np.max(data_to_show)) if Vmax is None else Vmax)

        if is_gpu_field:
            data_to_show = cp.asnumpy(data_to_show)
        else:
            data_to_show = np.asarray(data_to_show)

        plt.figure(figsize=figsize)
        plt.imshow( data_to_show, extent=(self.params.general['Xrange'][0] * 1000, self.params.general['Xrange'][1] * 1000, self.params.general['Zrange'][1] * 1000, self.params.general['Zrange'][0] * 1000), aspect="equal", cmap="jet", vmin=0, vmax=vmax)
        plt.colorbar(label=f"Envelope amplitude ({unit_label})")
        plt.title("Maximum-intensity projection of the acoustic field envelope")
        plt.xlabel("X (mm)")
        plt.ylabel("Z (mm)")
        plt.show()

    ## PRIVATE METHODS ##

    @abstractmethod
    def _generate_acoustic_field_SIMPLE_SIM(self, burst=None, show_log=False):
        pass

    def generate_burst_signal(self):
        if self.params.acoustic['typeSim'] == TypeSim.FIELD2.value:
            raise NotImplementedError("[AOT-biomaps] FIELD2 simulation is not implemented yet.")
        elif self.params.acoustic['typeSim'] == TypeSim.KWAVE.value:
            if not KWAVE_AVAILABLE or tone_burst is None:
                raise ImportError("The k-Wave Python package is required to generate an excitation burst.")
            self._generate_burst_signalKWAVE()
        elif self.params.acoustic['typeSim'] == TypeSim.HYDRO.value:
            raise ValueError("[AOT-biomaps] Cannot generate burst signal for Hydrophone simulation.")

    def _generate_burst_signalKWAVE(self):
        """
        Private method to generate a burst signal based on the specified parameters.
        """
        try:
            self.burst = tone_burst(1/self.medium.kgrid.dt, self.params.acoustic['f_US'], self.params.acoustic['emission']['num_cycles']).squeeze()
        except Exception as e:
            print(f"[AOT-biomaps] Error in _generate_burst_signal method: {e}")
            raise

    def _generate_acoustic_field_KWAVE_2D(
        self,
        burst=None,
        dead_piezo=None,
        isGPU=None,
        GPUdevice=None,
        generation_type="envelope_squared",
        show_log=True,
        keep_on_gpu=False,
        free_vram=True,
        backend=None,
        envelope_lpf_hz=None,
        accumulate_max_bytes=None,
        vram_fraction=0.95,
        host_staging_fraction=1.0 / 16.0,
        host_output_path=None,
        simulation_mode=None,
    ):
        """Dispatch 2D k-Wave generation to streaming or batch processing.

        The streaming GPU path is used for envelope outputs with the Python
        k-Wave solver. The batch path remains available for CPU execution,
        raw pressure-field output, and the optional compiled C++ backend.
        """
        if not KWAVE_AVAILABLE:
            raise ImportError("The k-Wave Python package is not available.")
        if generation_type not in ("envelope", "envelope_squared", "field"):
            raise ValueError("generation_type must be 'envelope', 'envelope_squared', or 'field'.")

        if isGPU is None:
            isGPU = config.get_process() == "gpu"
        if GPUdevice is None:
            GPUdevice = config.select_best_gpu()

        target_dt = getattr(self.medium, "dt_save", None)
        target_dx = getattr(self.medium, "dx_save", None)
        target_dz = getattr(self.medium, "dz_save", None)

        if backend is None:
            backend = "python"
        if backend not in ("python", "cpp"):
            raise ValueError("backend must be None, 'python', or 'cpp'.")
        if backend == "cpp" and not KWAVE_BINARIES_AVAILABLE:
            if show_log:
                print("[AOT-biomaps] k-Wave CUDA binary unavailable; using the Python backend.")
            backend = "python"

        if simulation_mode is None:
            use_streaming = (bool(isGPU) and CUPY_AVAILABLE and KWAVE_STREAMING_AVAILABLE and backend == "python" and generation_type in ("envelope", "envelope_squared"))
        elif simulation_mode == "stream":
            use_streaming = True
        elif simulation_mode == "batch":
            use_streaming = False

        if use_streaming:
            return self._stream_acoustic_field_KWAVE_2D(
                burst=burst,
                dead_piezo=dead_piezo,
                isGPU=isGPU,
                GPUdevice=GPUdevice,
                generation_type=generation_type,
                show_log=show_log,
                keep_on_gpu=keep_on_gpu,
                free_vram=free_vram,
                host_output_path=host_output_path,
                envelope_lpf_hz=envelope_lpf_hz,
                accumulate_max_bytes=accumulate_max_bytes,
                vram_fraction=vram_fraction,
                host_staging_fraction=host_staging_fraction,
                
            )

        return self._batch_acoustic_field_KWAVE_2D(
            burst=burst,
            dead_piezo=dead_piezo,
            isGPU=isGPU,
            GPUdevice=GPUdevice,
            generation_type=generation_type,
            show_log=show_log,
            keep_on_gpu=keep_on_gpu,
            free_vram=free_vram,
            host_output_path=host_output_path,
            backend=backend,     
        )

    def _stream_acoustic_field_KWAVE_2D(
        self,
        burst,
        dead_piezo,
        isGPU,
        GPUdevice,
        generation_type,
        show_log,
        keep_on_gpu,
        free_vram,
        envelope_lpf_hz,
        accumulate_max_bytes=None,
        vram_fraction=0.95,
        host_staging_fraction=1.0 / 16.0,
        host_output_path=None,
        validate_iq=False,
    ):
        """Run k-Wave and fused I/Q demodulation with GPU-side spatial resampling.

        The I/Q kernel always writes native-resolution frames into one GPU allocation.
        If the complete native output does not fit in VRAM, the allocation is used as a circular ring. Completed segments are spatially resampled on a dedicated CUDA stream before being copied to pinned host memory.
        The ring can be reused as soon as its spatial resampling has finished. The D2H transfer then reads the independent resampled GPU allocation.
        If the complete native output fits in VRAM, spatial resampling is done in chunks directly on the GPU. For spatial reduction, the result is compacted into the beginning of the original GPU allocation, avoiding a second full-size GPU allocation.
        Temporal resampling is performed after the spatial processing.

        Arguments:
            burst: The excitation burst signal.
            dead_piezo: Optional list of indices for inactive piezo elements.
            GPUdevice: The GPU device index to use.
            generation_type: The type of output to generate ("envelope", "envelope_squared", or "field").
            show_log: Whether to print log messages.
            keep_on_gpu: Whether to keep the final result on the GPU if it fits in VRAM.
            free_vram: Whether to free VRAM after the simulation.
            target_dt: Target temporal sampling interval (seconds).
            target_dx: Target spatial sampling interval in x (meters).
            target_dz: Target spatial sampling interval in z (meters).
            envelope_lpf_hz: Low-pass filter cutoff frequency for envelope extraction (Hz).
            accumulate_max_bytes: Optional maximum bytes for output accumulation.
            vram_fraction: Fraction of available VRAM to use for output buffers.
            host_staging_fraction: Fraction of available host RAM for pinned staging buffers.
            host_output_path: Optional path to save streamed output on host.
            validate_iq: Whether to validate I/Q envelope against a reference.
        """

        # ------------------------------------------------------------------
        # 1. Validation and acquisition parameters
        # ------------------------------------------------------------------

        if not CUPY_AVAILABLE or not KWAVE_STREAMING_AVAILABLE:
            raise RuntimeError("The streaming k-Wave path requires CuPy and k-Wave Simulation.")

        if self.medium.medium_properties is None:
            raise ValueError("Medium properties are not defined.")

        if not (0.0 < float(vram_fraction) <= 1.0):
            raise ValueError("vram_fraction must be in (0, 1].")

        if not (0.0 < float(host_staging_fraction) <= 1.0):
            raise ValueError("host_staging_fraction must be in (0, 1].")

        Nx = int(self.medium.Nx_reshaped)
        Nz = int(self.medium.Nz_reshaped)
        n_voxels = Nx * Nz
        frame_bytes = n_voxels * np.dtype(np.float32).itemsize
        medium_copy = copy.deepcopy(self.medium)
        dt = float(medium_copy.kgrid.dt)
        dx = float(self.medium.dx_reshaped)
        dz = float(getattr(self.medium, "dz_reshaped", dx))
        f_us = float(self.params.acoustic["f_US"])

        target_dt = dt if target_dt is None else float(target_dt)
        target_dx = dx if target_dx is None else float(target_dx)
        target_dz = dz if target_dz is None else float(target_dz)

        if min(target_dt, target_dx, target_dz) <= 0.0:
            raise ValueError("Target sample spacings must be positive.")

        decimation = max(1, int(target_dt / dt))

        output_dt = decimation * dt
        output_fs = 1.0 / output_dt

        if envelope_lpf_hz is None:
            envelope_lpf_hz = 0.25 * f_us

        envelope_lpf_hz = float(envelope_lpf_hz)

        if not (0.0 < envelope_lpf_hz < output_fs / 2.0):
            raise ValueError("envelope_lpf_hz must lie between zero and the output Nyquist frequency.")

        # Two cascaded first-order low-pass stages approximate a second-order baseband filter.
        pole_corner = envelope_lpf_hz / math.sqrt(math.sqrt(2.0) - 1.0)
        alpha = 1.0 - math.exp(-2.0 * math.pi * pole_corner * dt)
        group_delay = 2.0 * (1.0 - alpha) / alpha * dt
        pml_value = self.params.acoustic["medium"].get("pml_size", 0)

        if isinstance(pml_value, (int, np.integer)):
            pml_size = (int(pml_value), int(pml_value))
        else:
            if len(pml_value) != 2:
                raise ValueError("pml_size must be an integer or a two-element sequence.")
            pml_size = (int(pml_value[0]), int(pml_value[1]))

        pml_alpha = float(self.params.acoustic["medium"].get("pml_alpha", 2.0))

        # ------------------------------------------------------------------
        # 2. k-Wave source, sensor and simulation setup
        # ------------------------------------------------------------------
        source = kSource()
        source.p_mask = np.zeros((Nx, Nz), dtype=bool)
        source = self._set_up_source(source, dead_piezo=dead_piezo, burst=burst)
        sensor = kSensor()
        sensor.mask = np.ones((Nx, Nz), dtype=bool)
        sensor.record = ["p_final"] # Do not request the pressure time series from Simulation. p_final is a valid non-empty record request, preventing the default ("p", "p_final") behavior when record is empty.
        validate_simulation(medium_copy.kgrid, medium_copy.kmedium, source, sensor, pml_size=list(pml_size))
        kgrid_sim, medium_sim, source_sim, sensor_sim = _expand_for_pml_outside(medium_copy.kgrid, medium_copy.kmedium, source, sensor, list(pml_size))
        kernel = get_iq_envelope_kernel()

        debug_enabled = bool(validate_iq)
        gpu_output = None
        cpu_output = None
        pinned_owners = []
        host_staging = []
        copy_stream = None
        resample_stream = None
        sim = None
        iq_states = None
        output_on_gpu = False
        spatial_resampling_done = False

        # ------------------------------------------------------------------
        # 3. GPU execution
        # ------------------------------------------------------------------
        with cp.cuda.Device(int(GPUdevice)):
            compute_stream = cp.cuda.get_current_stream()
            sim = Simulation(kgrid_sim, medium_sim, source_sim, sensor_sim, device="gpu", use_sg=False, use_kspace=True, smooth_p0=False, pml_size=pml_size, pml_alpha=(pml_alpha, pml_alpha), quiet=not show_log, dtype=np.float32)
            sim.setup()
            Nt = int(sim.Nt)
            _, Nz_padded = sim.grid_shape
            start_n = decimation * int(math.ceil(group_delay / output_dt))
            n_output_max = max(0,(Nt - start_n + decimation - 1) // decimation)
            if n_output_max <= 0:
                raise RuntimeError( "The simulation is too short to produce an envelope frame.")

            # ------------------------------------------------------------------
            # 4. Target dimensions
            # ------------------------------------------------------------------
            predicted_sizes, _ = compute_target_sizes(Nx, Nz, n_output_max, dx, dz, output_dt, target_dt, target_dx, target_dz)
            target_Nt_pred, target_Nz, target_Nx = map(int, predicted_sizes)
            target_n_voxels = target_Nz * target_Nx
            target_frame_bytes = (target_n_voxels * np.dtype(np.float32).itemsize)
            spatial_resampling = (target_Nz != Nz or target_Nx != Nx)

            # ------------------------------------------------------------------
            # 5. I/Q state allocation
            # ------------------------------------------------------------------
            iq_states = cp.zeros((4, n_voxels),  dtype=cp.float64)
            i_state1, i_state2, q_state1, q_state2 = iq_states

            if debug_enabled:
                debug_pressure_gpu = cp.empty(Nt, dtype=cp.float32)
                debug_env2_gpu = cp.empty(n_output_max, dtype=cp.float32)
            else:
                debug_pressure_gpu = cp.empty(1, dtype=cp.float32)
                debug_env2_gpu = cp.empty(1, dtype=cp.float32)

            # ------------------------------------------------------------------
            # 6. Dynamic VRAM budget
            # ------------------------------------------------------------------
            memory_info = get_gpu_memory_info(cp)
            budget_bytes = get_gpu_output_budget_bytes(cp, fraction=vram_fraction, cap_bytes=accumulate_max_bytes)
            output_bytes = n_output_max * frame_bytes
            streamed = output_bytes > budget_bytes

            # Try a complete native-resolution output allocation first.
            if not streamed:
                try:
                    gpu_output = cp.empty(n_output_max * n_voxels, dtype=cp.float32)
                except (cp.cuda.memory.OutOfMemoryError, MemoryError):
                    streamed = True

            # ------------------------------------------------------------------
            # 7. Streaming ring allocation
            # ------------------------------------------------------------------
            ring_frames = 0
            chunk_frames = 0
            n_segments = 0
            if streamed:
                ring_frames = min(n_output_max, int(budget_bytes // frame_bytes)) # Use as much memory as possible for the native-resolution ring. Reduce its size only after an actual allocation failure.
                allocation_error = None
                while ring_frames >= 1:
                    try:
                        gpu_output = cp.empty(ring_frames * n_voxels, dtype=cp.float32)
                        break
                    except (cp.cuda.memory.OutOfMemoryError, MemoryError) as exc:
                        allocation_error = exc
                        cp.get_default_memory_pool().free_all_blocks()
                        ring_frames //= 2

                else:
                    raise MemoryError("Insufficient VRAM for a one-frame I/Q output buffer. Reduce the spatial grid or free GPU memory before simulation.") from allocation_error

                # The transfer chunk is defined using the RESAMPLED frame size. The ring itself remains in native resolution.
                requested_chunk_frames = get_transfer_chunk_frames(ring_frames, target_frame_bytes, host_staging_fraction=host_staging_fraction)
                requested_chunk_frames = max(1, min(ring_frames, int(requested_chunk_frames)))

                # Allocate two pinned buffers at the final spatial resolution.
                pinned_owners, host_staging, chunk_frames = (allocate_pinned_staging_buffers(frame_shape=(target_Nz, target_Nx), requested_frames=requested_chunk_frames, n_buffers=2, dtype=np.float32))
                chunk_frames = max(1, min(ring_frames, int(chunk_frames)))
                n_segments = max(1, ring_frames // chunk_frames) # Round the ring down to a whole number of segments.
                ring_frames = n_segments * chunk_frames
                if ring_frames * n_voxels != gpu_output.size:
                    gpu_output = gpu_output[:ring_frames * n_voxels]
     
                if host_output_path is None:
                    cpu_output = np.empty((n_output_max, target_Nz, target_Nx), dtype=np.float32) # Host output contains already spatially resampled frames.
                else:
                    host_directory = os.path.dirname(os.path.abspath(host_output_path))
                    os.makedirs(host_directory, exist_ok=True)
                    cpu_output = np.lib.format.open_memmap(host_output_path, mode="w+", dtype=np.float32, shape=(n_output_max, target_Nz, target_Nx))

                # Dedicated streams:
                # - compute_stream: k-Wave and I/Q kernel
                # - resample_stream: spatial interpolation
                # - copy_stream: asynchronous D2H
                copy_stream = cp.cuda.Stream(non_blocking=True)
                if spatial_resampling:
                    resample_stream = cp.cuda.Stream(non_blocking=True)

                ready_events = [cp.cuda.Event(disable_timing=True) for _ in range(n_segments)]
                segment_done_events = [cp.cuda.Event(disable_timing=True) for _ in range(n_segments)]
                host_done_events = [cp.cuda.Event(disable_timing=True) for _ in range(2)]
                pending_host_copies = [None, None]
                resampled_gpu_chunks = [None, None] # Keep resampled GPU chunks alive until their D2H transfers finish.
                next_host_slot = 0
                last_scheduled_end = 0

                if keep_on_gpu and show_log:
                    print("[AOT-biomaps] The native output exceeds the VRAM ring; the spatially resampled output will initially be assembled in host memory.")
                if ring_frames < 2 and show_log:
                    print("[AOT-biomaps] Only one frame fits in the output ring; asynchronous transfer overlap will be limited.")

                if show_log:
                    print(f"[AOT-biomaps] Asynchronous output: {ring_frames} native VRAM frames ({ring_frames * frame_bytes / 2**30:.2f} GiB), {n_segments} segment(s) x {chunk_frames} frames; spatial output frame={target_Nz} x {target_Nx}; CUDA free={memory_info['free_bytes'] / 2**30:.2f} GiB, CuPy reusable={memory_info['pool_free_bytes'] / 2**30:.2f} GiB.")

                # --------------------------------------------------------------
                # 7a. Host staging management
                # --------------------------------------------------------------
                def drain_host_slot(host_slot):
                    """Wait for a pinned transfer and commit it to the host output."""
                    pending = pending_host_copies[host_slot]
                    if pending is None:
                        return
                    global_start, frame_count = pending
                    host_done_events[host_slot].synchronize()
                    np.copyto(cpu_output[global_start:global_start + frame_count], host_staging[host_slot][:frame_count])
                    pending_host_copies[host_slot] = None
                    resampled_gpu_chunks[host_slot] = None

                # --------------------------------------------------------------
                # 7b. Schedule one completed ring segment
                # --------------------------------------------------------------
                def schedule_segment(segment_id, global_start, frame_count):
                    """Resample spatially on GPU, then schedule the D2H transfer."""

                    nonlocal next_host_slot
                    nonlocal last_scheduled_end
                    host_slot = next_host_slot
                    drain_host_slot(host_slot) # The pinned buffer cannot be reused until its previous D2H transfer and host-side commit have both completed.                    
                    ready_events[segment_id].record(compute_stream) # Mark the native ring segment as ready after all previous compute-stream operations have been submitted.
                    device_start = (segment_id * chunk_frames * n_voxels)
                    device_stop = (device_start + frame_count * n_voxels)
                    device_chunk = gpu_output[device_start:device_stop].reshape(frame_count, Nz, Nx)
                    
                    if spatial_resampling:
                        resample_stream.wait_event(ready_events[segment_id]) # Wait for the native segment before processing it.
                        with resample_stream:
                            processed_chunk = _resample_axis(device_chunk, target_Nz, axis=1, xp=cp)
                            processed_chunk = _resample_axis(processed_chunk, target_Nx, axis=2, xp=cp)
                            processed_chunk = cp.ascontiguousarray(processed_chunk) # Ensure an independent contiguous buffer. This is important because integer decimation can otherwise return a view into the native ring.

                        resampled_gpu_chunks[host_slot] = processed_chunk # Keep the processed data alive until D2H completes.
                        segment_done_events[segment_id].record(resample_stream) # The native ring can be reused as soon as spatial resampling has finished reading the segment.
                        copy_stream.wait_event(segment_done_events[segment_id]) # D2H waits for the spatially processed data.
                        processed_chunk.get(out=host_staging[host_slot][:frame_count], stream=copy_stream, blocking=False)
                    else:
                        copy_stream.wait_event(ready_events[segment_id]) # No spatial processing is required. Copy the native segment directly to pinned memory.
                        device_chunk.get(out=host_staging[host_slot][:frame_count], stream=copy_stream, blocking=False)
                        segment_done_events[segment_id].record(copy_stream) # In this case, the native ring must not be overwritten until the D2H transfer has finished.

                    host_done_events[host_slot].record(copy_stream)
                    pending_host_copies[host_slot] = (global_start, frame_count)
                    last_scheduled_end = global_start + frame_count
                    next_host_slot = (next_host_slot + 1) % 2
            else:
                gpu_output = gpu_output.reshape(n_output_max, Nz, Nx) # Complete native output remains resident in VRAM.

            # ------------------------------------------------------------------
            # 8. I/Q simulation loop
            # ------------------------------------------------------------------
            debug_index = ((Nz // 2) * Nx + (Nx // 2))
            threads = 256
            blocks = (n_voxels + threads - 1) // threads
            output_sqrt = int(generation_type == "envelope")
            n_rows = 0
            iterator = range(Nt)
            try:
                from tqdm.auto import tqdm
                if show_log:
                    iterator = tqdm(iterator, desc=f"Streaming k-Wave [{self.get_name_field()}]", unit="step")
            except ImportError:
                pass

            # sim.step() and the I/Q kernel remain on the compute stream. Resampling and D2H transfers are scheduled independently.
            with compute_stream:
                for _ in iterator:
                    time_index = int(sim.t)
                    sim.step()
                    phase = math.remainder(2.0 * math.pi * f_us * (time_index * dt), 2.0 * math.pi)
                    emit = (time_index >= start_n and time_index % decimation == 0 and n_rows < n_output_max)
                    if streamed:
                        chunk_id = (n_rows // chunk_frames if emit else 0)
                        frame_in_chunk = (n_rows % chunk_frames if emit else 0)
                        segment_id = (chunk_id % n_segments if emit else 0)
                        if emit and chunk_id >= n_segments and frame_in_chunk == 0:
                            compute_stream.wait_event(segment_done_events[segment_id]) # Reuse the native ring segment only after the resampling stage (or D2H if no spatial resampling) has finished reading it.
                        output_slot = (segment_id * chunk_frames + frame_in_chunk if emit else 0)
                    else:
                        output_slot = n_rows if emit else 0

                    if sim.p.dtype == cp.float32:
                        p_is_double = 0
                    elif sim.p.dtype == cp.float64:
                        p_is_double = 1
                    else:
                        raise TypeError(f"Unsupported k-Wave pressure dtype: {sim.p.dtype}")
                    kernel((blocks,), (threads,), (sim.p, np.int32(p_is_double), np.int32(Nx), np.int32(Nz_padded), np.int32(pml_size[0]), np.int32(pml_size[1]), i_state1, i_state2, q_state1, q_state2, gpu_output, debug_pressure_gpu, debug_env2_gpu, np.int32(debug_index), np.int32(time_index), np.int64(output_slot), np.int32(n_rows), np.int32(n_voxels), np.float64(math.cos(phase)), np.float64(math.sin(phase)), np.float64(alpha), np.int32(1 if emit else 0), np.int32(1 if debug_enabled else 0), np.int32(output_sqrt)), stream=compute_stream)

                    if not emit:
                        continue

                    n_rows += 1
                    if streamed:
                        chunk_finished = (n_rows % chunk_frames == 0)or (n_rows == n_output_max)

                        if chunk_finished:
                            completed_chunk_id = (n_rows - 1) // chunk_frames
                            completed_segment_id = completed_chunk_id % n_segments
                            global_start = completed_chunk_id * chunk_frames
                            completed_frames = min(chunk_frames, n_rows - global_start)
                            schedule_segment(completed_segment_id, global_start, completed_frames)

            if n_rows <= 0:
                raise RuntimeError("The streaming simulation produced no output frames.")

            # ------------------------------------------------------------------
            # 9. Flush the last partial ring segment
            # ------------------------------------------------------------------
            if streamed and last_scheduled_end < n_rows:
                completed_chunk_id = (n_rows - 1) // chunk_frames
                completed_segment_id = completed_chunk_id % n_segments
                global_start = completed_chunk_id * chunk_frames
                completed_frames = n_rows - global_start
                schedule_segment(completed_segment_id, global_start, completed_frames)

            compute_stream.synchronize()

            # ------------------------------------------------------------------
            # 10. Collect streamed or complete GPU output
            # ------------------------------------------------------------------
            if streamed:
                if resample_stream is not None:
                    resample_stream.synchronize()
                drain_host_slot(0)
                drain_host_slot(1)
                copy_stream.synchronize()
                if hasattr(cpu_output, "flush"):
                    cpu_output.flush()
                raw_output = cpu_output[:n_rows]
                output_on_gpu = False
                spatial_resampling_done = spatial_resampling
            else:
                # --------------------------------------------------------------
                # 10a. Spatial resampling on GPU for a complete output
                # --------------------------------------------------------------
                if spatial_resampling:
                    spatial_chunk_frames = get_transfer_chunk_frames(n_rows, frame_bytes, host_staging_fraction=host_staging_fraction)
                    spatial_chunk_frames = max(1,min(n_rows, int(spatial_chunk_frames)))

                    # If the number of spatial output voxels does not increase, compact the processed output into the beginning of the existing native GPU allocation.
                    # This avoids allocating a second full output array.
                    if target_n_voxels <= n_voxels:
                        gpu_output_flat = gpu_output.reshape(-1) 

                        with compute_stream:
                            for global_start in range(0, n_rows, spatial_chunk_frames):
                                global_stop = min(global_start + spatial_chunk_frames, n_rows)
                                frame_count = global_stop - global_start
                                device_chunk = gpu_output[global_start:global_stop]
                                processed_chunk = _resample_axis(device_chunk, target_Nz, axis=1, xp=cp)
                                processed_chunk = _resample_axis(processed_chunk, target_Nx, axis=2, xp=cp)
                                processed_chunk = cp.ascontiguousarray(processed_chunk) # Detach the result from the native source before writing into the compacted destination.
                                destination_start = global_start * target_n_voxels
                                destination_stop = destination_start + frame_count * target_n_voxels
                                cp.copyto(gpu_output_flat[destination_start:destination_stop],processed_chunk.reshape(-1))
                                
                        compute_stream.synchronize()
                        raw_output_gpu = gpu_output_flat[:n_rows * target_n_voxels].reshape(n_rows, target_Nz, target_Nx)
                        if keep_on_gpu:
                            raw_output = raw_output_gpu
                            output_on_gpu = True
                        else:
                            raw_output = cp.asnumpy(raw_output_gpu)
                            output_on_gpu = False

                        spatial_resampling_done = True
                    else:
                        spatial_gpu_output = None # Spatial upsampling increases the output size. Avoid holding a second large GPU allocation unless it can actually be allocated.
                        if keep_on_gpu:
                            try:
                                spatial_gpu_output = cp.empty((n_rows, target_Nz, target_Nx), dtype=cp.float32)
                            except (cp.cuda.memory.OutOfMemoryError, MemoryError):
                                spatial_gpu_output = None

                        if spatial_gpu_output is not None:
                            with compute_stream:
                                for global_start in range(0, n_rows, spatial_chunk_frames):
                                    global_stop = min(global_start + spatial_chunk_frames, n_rows)
                                    device_chunk = gpu_output[global_start:global_stop]
                                    processed_chunk = _resample_axis(device_chunk, target_Nz, axis=1, xp=cp)
                                    processed_chunk = _resample_axis(processed_chunk, target_Nx, axis=2, xp=cp)
                                    processed_chunk = cp.ascontiguousarray(processed_chunk)
                                    cp.copyto(spatial_gpu_output[global_start:global_stop], processed_chunk)

                            compute_stream.synchronize()
                            raw_output = spatial_gpu_output
                            output_on_gpu = True

                        else:                          
                            cpu_spatial_output = np.empty((n_rows, target_Nz, target_Nx, ), dtype=np.float32) # CPU output is used only for spatial upsampling when a complete GPU output cannot be allocated.
                            with compute_stream:
                                for global_start in range(0, n_rows, spatial_chunk_frames):
                                    global_stop = min(global_start + spatial_chunk_frames, n_rows)
                                    device_chunk = gpu_output[global_start:global_stop]
                                    processed_chunk = _resample_axis(device_chunk, target_Nz, axis=1, xp=cp)
                                    processed_chunk = _resample_axis(processed_chunk, target_Nx, axis=2, xp=cp)
                                    processed_chunk = cp.ascontiguousarray(processed_chunk)
                                    cpu_spatial_output[global_start:global_stop] = cp.asnumpy(processed_chunk)
                            compute_stream.synchronize()
                            raw_output = cpu_spatial_output
                            output_on_gpu = False
                        spatial_resampling_done = True

                else:
                    raw_output_gpu = gpu_output[:n_rows]
                    if keep_on_gpu:
                        raw_output = raw_output_gpu
                        output_on_gpu = True
                    else:
                        raw_output = cp.asnumpy(raw_output_gpu)
                        output_on_gpu = False

            # ------------------------------------------------------------------
            # 11. Actual output dimensions and metadata
            # ------------------------------------------------------------------
            sizes, steps = compute_target_sizes(Nx, Nz, n_rows, dx, dz, output_dt, target_dt, target_dx, target_dz)
            if int(sizes[1]) != target_Nz or int(sizes[2]) != target_Nx: # The spatial target dimensions must remain independent of the actual number of emitted temporal frames.
                raise RuntimeError("Spatial target dimensions changed between the predicted and actual output sizes.")

            self.last_decimation = (dict(zip(("Nt", "Nz", "Nx"), sizes)) | dict(zip(("dt", "dz", "dx"), steps)))
            self.last_decimation["t0"] = (start_n * dt - group_delay)
            if show_log:
                print(f"[AOT-biomaps] Streaming output: {(n_rows, Nz, Nx)} -> {sizes}; dt={output_dt * 1e9:.2f} ns, saved dt={steps[0] * 1e9:.2f} ns, dz={steps[1] * 1e6:.1f} um, dx={steps[2] * 1e6:.1f} um.")

            # ------------------------------------------------------------------
            # 12. Release simulation and temporary references
            # ------------------------------------------------------------------
            del sim
            del iq_states
            del i_state1, i_state2, q_state1, q_state2
            del debug_pressure_gpu, debug_env2_gpu
            if streamed:
                # All transfers and resampling operations must have completed before releasing the ring and pinned staging allocations.
                if copy_stream is not None:
                    copy_stream.synchronize()
                if resample_stream is not None:
                    resample_stream.synchronize()
                del gpu_output
                del host_staging
                del pinned_owners
            elif not output_on_gpu:
                del gpu_output

        # ----------------------------------------------------------------------
        # 13. Final temporal resampling
        # ----------------------------------------------------------------------
        with cp.cuda.Device(int(GPUdevice)):
            output = raw_output
            xp = cp if output_on_gpu else np
            # Spatial resampling has already been performed on GPU for the streaming path and the complete-output path.
            if not spatial_resampling_done:
                output = _resample_axis(output, sizes[1], axis=1, xp=xp)
                output = _resample_axis(output, sizes[2], axis=2, xp=xp)

            output = _resample_axis(output, sizes[0], axis=0, xp=xp) # Temporal resampling remains a single operation after assembly.
            target_shape = tuple(int(size) for size in sizes)
            if tuple(output.shape) != target_shape:
                raise RuntimeError(f"Final output shape mismatch: got {tuple(output.shape)}, expected {target_shape}.")

            # ------------------------------------------------------------------
            # 14. Honor keep_on_gpu after final resampling
            # ------------------------------------------------------------------
            if keep_on_gpu and not output_on_gpu:
                final_bytes = int(output.nbytes)
                final_budget = get_gpu_output_budget_bytes(cp, fraction=vram_fraction, cap_bytes=None)
                if final_bytes <= final_budget:
                    try:
                        output = cp.asarray(output)
                        output_on_gpu = True
                        if show_log:
                            print("[AOT-biomaps] Final resampled output transferred to GPU.")
                    except (cp.cuda.memory.OutOfMemoryError, MemoryError):
                        if show_log:
                            print("[AOT-biomaps] The final resampled output could not be reallocated on the GPU; returning the host array.")

                elif show_log:
                    print("[AOT-biomaps] The final resampled output exceeds currently available VRAM; returning the host array.")

            elif output_on_gpu and not keep_on_gpu:
                output = cp.asnumpy(output)
                output_on_gpu = False

            # ------------------------------------------------------------------
            # 15. Optional GPU memory release
            # ------------------------------------------------------------------
            if free_vram:
                with cp.cuda.Device(GPUdevice):
                    from AOT_biomaps.AOT_Acoustic.AcousticTools import clear_gpu_memory
                    clear_gpu_memory(cp, clear_fft_plans=True)   # plans + pool
                    cp.get_default_pinned_memory_pool().free_all_blocks()

            return output
    
    def _batch_acoustic_field_KWAVE_2D(
        self,
        burst=None,
        dead_piezo=None,
        isGPU=None,
        GPUdevice=None,
        generation_type="envelope_squared",
        show_log=True,
        keep_on_gpu=False,
        free_vram=True,
        target_dt=None,
        target_dx=None,
        target_dz=None,
        backend="python",
        profile=False,
        precimate_time=False, 
        host_output_path=None,    
    ):
        """Run k-Wave batch simulation using Simulation.setup() and Simulation.step().

        The complete pressure history is stored on the selected device directly
        in the pipeline layout (Nt, Nz, Nx): each frame is transposed at write
        time, so no full-size layout conversion is needed afterwards. Sensor
        time-series recording is disabled to avoid allocating a second copy of
        the pressure history.
        """

        import time
        from contextlib import nullcontext

        # ------------------------------------------------------------------
        # 1. Configuration
        # ------------------------------------------------------------------
        if Simulation is None or validate_simulation is None:
            raise RuntimeError("The installed k-Wave package does not expose the Simulation API.")
        if _expand_for_pml_outside is None:
            raise RuntimeError("The installed k-Wave package does not expose _expand_for_pml_outside.")
        if generation_type not in ("envelope_squared", "envelope", "field"):
            raise ValueError(f"Unsupported generation_type: {generation_type!r}.")
        if backend not in (None, "python"):
            raise ValueError("The Simulation.setup()/step() batch implementation uses the Python Simulation backend. backend must be 'python'.")

        if GPUdevice is None:
            GPUdevice = config.select_best_gpu()
        if isGPU and not CUPY_AVAILABLE:
            isGPU = False
        if isGPU:
            GPUdevice = int(GPUdevice)

        xp = cp if isGPU else np
        device_context = (cp.cuda.Device(GPUdevice) if isGPU else nullcontext())
        profile_times = {}
        total_start = time.perf_counter() if profile else None

        def synchronize():
            if isGPU:
                cp.cuda.get_current_stream().synchronize()

        # ------------------------------------------------------------------
        # 2. Original grid and sampling parameters
        # ------------------------------------------------------------------
        Nx = int(self.medium.Nx_reshaped)
        Nz = int(self.medium.Nz_reshaped)
        dx = float(self.medium.dx_reshaped)
        dz = float(getattr(self.medium, "dz_reshaped", dx))
        medium_copy = copy.deepcopy(self.medium)
        dt = float(medium_copy.kgrid.dt)

        target_dt = dt if target_dt is None else float(target_dt)
        target_dx = dx if target_dx is None else float(target_dx)
        target_dz = dz if target_dz is None else float(target_dz)

        if min(dt, dx, dz, target_dt, target_dx, target_dz) <= 0:
            raise ValueError("All spatial and temporal sampling intervals must be positive.")

        # ------------------------------------------------------------------
        # 3. PML configuration
        # ------------------------------------------------------------------
        pml_value = self.params.acoustic["medium"].get("pml_size", 0)

        if isinstance(pml_value, (int, np.integer)):
            pml_size = (int(pml_value), int(pml_value))
        else:
            if len(pml_value) != 2:
                raise ValueError("pml_size must be an integer or a two-element sequence.")
            pml_size = (int(pml_value[0]), int(pml_value[1]))

        pml_alpha = float(self.params.acoustic["medium"].get("pml_alpha", 2.0))

        # ------------------------------------------------------------------
        # 4. Source and sensor
        # ------------------------------------------------------------------
        source = kSource()
        source.p_mask = np.zeros((Nx, Nz), dtype=bool)
        source = self._set_up_source(source, dead_piezo=dead_piezo, burst=burst)
        sensor = kSensor()
        sensor.mask = np.ones((Nx, Nz), dtype=bool)
        sensor.record = ["p_final"] # Do not request the pressure time series from Simulation. p_final is a valid non-empty record request, preventing the default ("p", "p_final") behavior when record is empty.

        # ------------------------------------------------------------------
        # 5. Validate and expand the simulation grid with external PML
        # ------------------------------------------------------------------
        validate_simulation(medium_copy.kgrid, medium_copy.kmedium, source, sensor, pml_size=list(pml_size))
        kgrid_sim, medium_sim, source_sim, sensor_sim = _expand_for_pml_outside(medium_copy.kgrid, medium_copy.kmedium, source, sensor, list(pml_size))
        sensor_sim.mask = None # The sensor is not used for recording. Setting its mask to None avoids constructing a large GPU sensor-index array during Simulation.setup().

        # ------------------------------------------------------------------
        # 6. Simulation setup and batch pressure acquisition
        # ------------------------------------------------------------------
        grid_field = None
        sim = None

        with device_context:
            compute_stream = (cp.cuda.get_current_stream() if isGPU else None)
            stream_context = (compute_stream if isGPU else nullcontext())
            with stream_context:

                # ----------------------------------------------------------
                # 6.1 Initialize the low-level k-Wave solver
                # ----------------------------------------------------------
                sim = Simulation(kgrid_sim, medium_sim, source_sim, sensor_sim, device="gpu" if isGPU else "cpu", use_sg=False, use_kspace=True, smooth_p0=True, pml_size=pml_size, pml_alpha=(pml_alpha, pml_alpha), quiet=not show_log, dtype=np.float32)
                sim.setup()
                if "p" in sim.sensor_data:
                    raise RuntimeError("The pressure sensor history was unexpectedly allocated. Check sensor.record before Simulation.setup().")

                Nt = int(sim.Nt)

                # ----------------------------------------------------------
                # 6.2 Extract the physical domain from the padded grid
                # ----------------------------------------------------------
                expected_shape = (Nx + 2 * pml_size[0], Nz + 2 * pml_size[1])
                if tuple(sim.grid_shape) != expected_shape:
                    raise RuntimeError(f"Unexpected padded grid shape {sim.grid_shape}; expected {expected_shape}.")

                x_slice = slice(pml_size[0], pml_size[0] + Nx)
                z_slice = slice(pml_size[1], pml_size[1] + Nz)

                # ----------------------------------------------------------
                # 6.3 Pressure history: keep in VRAM if it fits, else host. Decision made AFTER sim.setup(): free VRAM already excludes the solver grids.
                # ----------------------------------------------------------
                time_stride = int(round(target_dt / dt)) if precimate_time else 1
                if time_stride < 1 or abs(time_stride * dt - target_dt) > 0.25 * dt:
                    time_stride = 1

                stored = {int(i): int(j) for j, i in enumerate(range(0, Nt, time_stride))}
                Ns = len(stored)
                dt_eff = time_stride * dt
                hist_bytes = Ns * Nx * Nz * np.dtype(np.float32).itemsize

                store_on_gpu = False
                if isGPU:
                    free_b, _ = cp.cuda.runtime.memGetInfo()
                    store_on_gpu = hist_bytes <= int(free_b * 0.90)

                if store_on_gpu:
                    grid_field = cp.empty((Ns, Nz, Nx), dtype=cp.float32)
                else:
                    if host_output_path is not None:
                        os.makedirs(os.path.dirname(os.path.abspath(host_output_path)), exist_ok=True)
                        grid_field = np.lib.format.open_memmap(host_output_path, mode="w+", dtype=np.float32, shape=(Ns, Nz, Nx))
                    else:
                        grid_field = np.empty((Ns, Nz, Nx), dtype=np.float32)
                    if show_log:
                        where = "memmap " + host_output_path if host_output_path else "host RAM"
                        print(f"[AOT-biomaps] Batch history {hist_bytes/2**30:.1f} GiB > free VRAM -> {where}")

                # ----------------------------------------------------------
                # 6.4 run: store one frame at a time, D2H per frame on the host path
                # ----------------------------------------------------------
                iterator = range(Nt)
                if show_log:
                    try:
                        from tqdm.auto import tqdm
                        iterator = tqdm(iterator, desc=f"k-Wave batch [{self.get_name_field()}]", unit="step")
                    except ImportError:
                        pass

                for _ in iterator:
                    time_index = int(sim.t)
                    sim.step()
                    j = stored.get(time_index)
                    if j is not None:
                        frame = sim.p[x_slice, z_slice]      # (Nx, Nz) float32 on GPU
                        if store_on_gpu:
                            grid_field[j] = frame.T           # (Nz, Nx) written in place
                        else:
                            grid_field[j] = cp.asnumpy(frame).T

                synchronize()
                del sim
                sim = None
                
        # ------------------------------------------------------------------
        # 6.5 Post-processing namespace follows the data location
        # ------------------------------------------------------------------
        xp = cp if (isGPU and store_on_gpu) else np        
        post_context = device_context if (isGPU and store_on_gpu) else nullcontext() # Steps 7-11 run inside the device context when the data lives on the GPU
        with post_context:
            # ------------------------------------------------------------------
            # 7. Target dimensions and decimation (dt_eff + Ns)
            # ------------------------------------------------------------------
            Ns = int(grid_field.shape[0])
            sizes, steps = compute_target_sizes(Nx, Nz, Ns, dx, dz, dt_eff, target_dt, target_dx, target_dz)
            self.last_decimation = (dict(zip(("Nt", "Nz", "Nx"), sizes)) | dict(zip(("dt", "dz", "dx"), steps)))

            # ------------------------------------------------------------------
            # 8. Envelope computation
            # ------------------------------------------------------------------
            if generation_type == "envelope_squared":
                output = calculate_envelope_squared(grid_field, time_axis=0, xp=xp, show_log=show_log)
                del grid_field
            elif generation_type == "envelope":
                output = calculate_envelope(grid_field, time_axis=0, xp=xp, show_log=show_log)
                del grid_field
            else:
                output = grid_field  # Raw pressure field.

            # ------------------------------------------------------------------
            # 9. Resampling directly on the pipeline layout: axes (0, 1, 2) match the (Nt, Nz, Nx) order of `sizes`.
            # ------------------------------------------------------------------
            output = resample_bandlimited(output, 0, int(sizes[0]), xp=xp)  # time
            output = resample_bandlimited(output, 1, int(sizes[1]), xp=xp)  # z
            output = resample_bandlimited(output, 2, int(sizes[2]), xp=xp)  # x

            # ------------------------------------------------------------------
            # 10. Return output
            # ------------------------------------------------------------------
            if isGPU and not keep_on_gpu:
                output_host = _to_numpy_array(output)
                del output
                output = output_host

        if isGPU and not keep_on_gpu and free_vram:
            with cp.cuda.Device(GPUdevice):
                from AOT_biomaps.AOT_Acoustic.AcousticTools import clear_gpu_memory
                clear_gpu_memory(cp, clear_fft_plans=True)   # plans + pool
                cp.get_default_pinned_memory_pool().free_all_blocks()

        return output

    def _generate_acoustic_field_KWAVE_2D_old(
        self,
        burst=None,
        isGPU=None,
        GPUdevice=None,
        generation_type="envelope_squared",
        show_log=True,
        keep_on_gpu=False,
        free_vram=True,
        target_dt=None,
        target_dx=None,
        target_dz=None,
        backend=None,
    ):
        """Backward-compatible entry point for the former batch generator.

        New code should call :meth:`_generate_acoustic_field_KWAVE_2D`. This
        method remains available for older subclasses and notebooks.
        """
        return self._batch_acoustic_field_KWAVE_2D(
            burst=burst,
            isGPU=isGPU,
            GPUdevice=GPUdevice,
            generation_type=generation_type,
            show_log=show_log,
            keep_on_gpu=keep_on_gpu,
            free_vram=free_vram,
            target_dt=target_dt,
            target_dx=target_dx,
            target_dz=target_dz,
            backend=backend or "python",
        )

    @abstractmethod
    def _set_up_source(self, source, burst=None):
        """
        Abstract method: each subclass must implement its own source setup.
        All grid/physical parameters come from self.medium (SIMULATION grid);
        the source is always built at the simulation sampling rate.
        """
        pass

    @abstractmethod
    def _save2D_HDR_IMG(self, filePath):
        """
        Save the 2D acoustic field as an HDR_IMG file.
        Must be implemented in subclasses.
        """
        pass

    def _field_output_path(self, path, extension):
        """Resolve a file or directory argument for a field output."""
        path = os.fspath(path)
        extension = extension if extension.startswith(".") else f".{extension}"
        if path.lower().endswith(extension.lower()):
            return path
        if os.path.isdir(path) or path.endswith(os.sep):
            os.makedirs(path, exist_ok=True)
            return os.path.join(path, self.get_name_field() + extension)
        return path + self.get_name_field() + extension

    def _load_field_h5(self, filePath, nameBlock=None):
        """Load one field dataset from an HDF5 file."""
        if nameBlock is None:
            nameBlock = "data"
        h5_path = (
            os.fspath(filePath)
            if os.fspath(filePath).lower().endswith((".h5", ".hdf5"))
            else os.path.join(filePath, self.get_name_field() + ".h5")
        )
        with h5py.File(h5_path, "r") as handle:
            if nameBlock not in handle:
                raise KeyError(f"Dataset {nameBlock!r} is not present in {h5_path!r}.")
            self.field = handle[nameBlock][...]

    def _save2D_H5(self, filePath):
        """Save field data and lightweight metadata to HDF5."""
        if self.field is None:
            raise ValueError("No acoustic field is available to save.")
        h5_path = self._field_output_path(filePath, ".h5")
        field_data = _to_numpy_array(self.field)
        with h5py.File(h5_path, "w") as handle:
            handle.create_dataset("data", data=field_data, compression="gzip")
            if self.last_decimation is not None:
                metadata = handle.create_group("last_decimation")
                for key, value in self.last_decimation.items():
                    metadata.attrs[key] = value
        return h5_path

    def _save2D_NPY(self, filePath):
        """Save the field array as a NumPy ``.npy`` file."""
        if self.field is None:
            raise ValueError("No acoustic field is available to save.")
        npy_path = self._field_output_path(filePath, ".npy")
        np.save(npy_path, _to_numpy_array(self.field))
        return npy_path

    def _load_fieldKWAVE_XZ(self, hdr_path):
        """
        Read an Interfile (.hdr) and its binary file (.img).
        Loads the field lazily via np.memmap (read-only) and restores the
        EFFECTIVE sampling metadata (last_decimation) from the header, so
        that display/save/reconstruction use the correct grid even after
        loading a decimated field.
        """
        try:
            header = {}
            with open(hdr_path, 'r') as f:
                for line in f:
                    if ':=' in line:
                        key, value = line.split(':=', 1)
                        key = key.strip().lower().replace('!', '')
                        header[key] = value.strip()

            data_file = header.get('name of data file') or header.get('name of date file')
            if data_file is None:
                raise ValueError(f"Cannot find the data file associated with the header file {hdr_path}")
            img_path = os.path.join(os.path.dirname(hdr_path), os.path.basename(data_file))

            shape = [int(header[f'matrix size [{i}]']) for i in range(1, 3) if f'matrix size [{i}]' in header]
            if not shape:
                raise ValueError("Cannot determine the shape of the acoustic field from metadata.")

            data_type = header.get('number format', 'short float').lower()
            dtype_map = {
                'short float': np.float32,
                'float': np.float32,
                'int16': np.int16,
                'int32': np.int32,
                'uint16': np.uint16,
                'uint8': np.uint8
            }
            dtype = dtype_map.get(data_type)
            if dtype is None:
                raise ValueError(f"Unsupported data type: {data_type}")

            byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
            endianess = '<' if 'little' in byte_order else '>'

            fileSize = os.path.getsize(img_path)
            timeDim = int(fileSize / (np.dtype(dtype).itemsize * np.prod(shape)))
            if f'matrix size [3]' in header and int(header['matrix size [3]']) != timeDim:
                raise ValueError(f"[AOT-biomaps] Truncated .img: header declares "
                                 f"{header['matrix size [3]']} time samples, file has {timeDim}.")
            shape = shape + [timeDim]

            self.field = np.memmap(img_path, dtype=endianess + np.dtype(dtype).char,
                                   mode='r', shape=tuple(shape[::-1]))

            # Apply scaling factors if available (materializes a copy only if needed)
            rescale_slope = float(header.get('data rescale slope', 1))
            rescale_offset = float(header.get('data rescale offset', 0))
            if rescale_slope != 1.0 or rescale_offset != 0.0:
                self.field = self.field * rescale_slope + rescale_offset

            # ------------------------------------------------------------------
            # Effective sampling metadata, FROM THE HEADER (survives
            # generation, save, load, re-save cycles)
            # ------------------------------------------------------------------
            self.last_decimation = None
            try:
                dt_h = float(header.get('scaling factor (s/pixel) [3]'))
                dx_h = float(header.get('scaling factor (mm/pixel) [1]')) / 1000.0
                dz_h = float(header.get('scaling factor (mm/pixel) [2]')) / 1000.0
                self.last_decimation = {'Nt': timeDim, 'dt': dt_h,
                                        'Nx': shape[0], 'dx': dx_h,
                                        'Nz': shape[1], 'dz': dz_h}
            except (TypeError, ValueError):
                print("[AOT-biomaps] Warning: incomplete sampling metadata in the "
                      "header; last_decimation not restored.")

        except Exception as e:
            print(f"[AOT-biomaps] Error in _load_fieldKWAVE_XZ method: {e}")
            raise

    def _load_fieldHYDRO_XZ(self, file_path_h5, param_path_mat):
        """
        Load the 2D acoustic field for Hydrophone simulation from H5 and MAT files.

        Parameters:
        - file_path_h5 (str): The path to the H5 file.
        - param_path_mat (str): The path to the MAT file.

        Returns:
        - envelope_transposed (numpy.ndarray): The transposed envelope of the acoustic field.
        """
        try:
            # Load parameters from the .mat file
            param = loadmat(param_path_mat)

            # Load the ranges for x and z
            x_range = np.arange(-23, 21.2, 0.2)
            z_range = np.arange(0, 37.2, 0.2)

            # Load the data from the .h5 file
            with h5py.File(file_path_h5, 'r') as file:
                data = file['data'][:]

            # Initialize a matrix to store the acoustic data
            acoustic_field = np.zeros((len(z_range), len(x_range), data.shape[1]))

            # Fill the grid with acoustic data
            index = 0
            for i in range(len(z_range)):
                if i % 2 == 0:
                    # Traverse left to right
                    for j in range(len(x_range)):
                        acoustic_field[i, j, :] = data[index]
                        index += 1
                else:
                    # Traverse right to left
                    for j in range(len(x_range) - 1, -1, -1):
                        acoustic_field[i, j, :] = data[index]
                        index += 1

            # Calculate the analytic envelope
            envelope = np.abs(scipy_hilbert(acoustic_field, axis=2))
            # Reorganize the array to have the shape (Times, Z, X)
            envelope_transposed = np.transpose(envelope, (2, 0, 1))

            self.field = envelope_transposed
            self.params.general["Xrange"] = x_range
            self.params.general["Zrange"] = z_range
            return envelope_transposed, x_range, z_range

        except Exception as e:
            print(f"[AOT-biomaps] Error in _load_fieldHYDRO_XZ method: {e}")
            raise

    def _load_fieldHYDRO_YZ(self, file_path_h5, param_path_mat):
        """
        Load the 2D acoustic field for Hydrophone simulation from H5 and MAT files.

        Parameters:
        - file_path_h5 (str): The path to the H5 file.
        - param_path_mat (str): The path to the MAT file.

        Returns:
        - envelope_transposed (numpy.ndarray): The transposed envelope of the acoustic field.
        - y_range (numpy.ndarray): The range of y values.
        - z_range (numpy.ndarray): The range of z values.
        """
        try:
            # Load parameters from the .mat file
            param = loadmat(param_path_mat)

            # Extract the ranges for y and z
            y_range = param['y'].flatten()
            z_range = param['z'].flatten()

            # Load the data from the .h5 file
            with h5py.File(file_path_h5, 'r') as file:
                data = file['data'][:]

            # Calculate the number of scans
            Ny = len(y_range)
            Nz = len(z_range)

            # Create the scan positions
            positions_y = []
            positions_z = []

            for i in range(Nz):
                if i % 2 == 0:
                    # Traverse top to bottom for even rows
                    positions_y.extend(y_range)
                else:
                    # Traverse bottom to top for odd rows
                    positions_y.extend(y_range[::-1])
                positions_z.extend([z_range[i]] * Ny)

            Positions = np.column_stack((positions_y, positions_z))

            # Initialize a matrix to store the reorganized data
            reorganized_data = np.zeros((Ny, Nz, data.shape[1]))

            # Reorganize the data according to the scan positions
            for index, (j, k) in enumerate(Positions):
                y_idx = np.where(y_range == j)[0][0]
                z_idx = np.where(z_range == k)[0][0]
                reorganized_data[y_idx, z_idx, :] = data[index, :]

            # Calculate the analytic envelope
            envelope = np.abs(scipy_hilbert(reorganized_data, axis=2))
            # Reorganize the array to have the shape (Times, Z, Y)
            envelope_transposed = np.transpose(envelope, (2, 0, 1))
            return envelope_transposed, y_range, z_range
        except Exception as e:
            print(f"[AOT-biomaps] Error in _load_fieldHYDRO_YZ method: {e}")
            raise

    def _load_fieldHYDRO_XYZ(self, file_path_h5, param_path_mat):
        """
        Load the 3D acoustic field for Hydrophone simulation from H5 and MAT files.

        Parameters:
        - file_path_h5 (str): The path to the H5 file.
        - param_path_mat (str): The path to the MAT file.

        Returns:
        - envelope_field (numpy.ndarray): The envelope of the acoustic field.
        - x_range (numpy.ndarray): The range of x values.
        - y_range (numpy.ndarray): The range of y values.
        - z_range (numpy.ndarray): The range of z values.
        """
        try:
            # Load parameters from the .mat file
            param = loadmat(param_path_mat)

            # Extract the ranges for x, y, and z
            x_range = param['x'].flatten()
            y_range = param['y'].flatten()
            z_range = param['z'].flatten()

            # Load the data from the .h5 file
            with h5py.File(file_path_h5, 'r') as file:
                data = file['data'][:]

            # Calculate the number of scans
            Nx = len(x_range)
            Ny = len(y_range)
            Nz = len(z_range)
            # Create the scan positions
            if Ny % 2 == 0:
                X = np.tile(np.concatenate([x_range[:, np.newaxis], x_range[::-1, np.newaxis]]), (Ny // 2, 1))
                Y = np.repeat(y_range, Nx)
            else:
                X = np.concatenate([x_range[:, np.newaxis], np.tile(np.concatenate([x_range[::-1, np.newaxis], x_range[:, np.newaxis]]), ((Ny - 1) // 2, 1))])
                Y = np.repeat(y_range, Nx)

            XY = np.column_stack((X.flatten(), Y))

            if Nz % 2 == 0:
                XYZ = np.tile(np.concatenate([XY, np.flipud(XY)]), (Nz // 2, 1))
                Z = np.repeat(z_range, Nx * Ny)
            else:
                XYZ = np.concatenate([XY, np.tile(np.concatenate([np.flipud(XY), XY]), ((Nz - 1) // 2, 1))])
                Z = np.repeat(z_range, Nx * Ny)

            Positions = np.column_stack((XYZ, Z))

            # Initialize a matrix to store the reorganized data
            reorganized_data = np.zeros((Nx, Ny, Nz, data.shape[1]))

            # Reorganize the data according to the scan positions
            for index, (i, j, k) in enumerate(Positions):
                x_idx = np.where(x_range == i)[0][0]
                y_idx = np.where(y_range == j)[0][0]
                z_idx = np.where(z_range == k)[0][0]
                reorganized_data[x_idx, y_idx, z_idx, :] = data[index, :]

            envelope_field = np.zeros_like(reorganized_data)

            for y in range(reorganized_data.shape[1]):
                for z in range(reorganized_data.shape[2]):
                    envelope_field[:, y, z, :] = np.abs(scipy_hilbert(reorganized_data[:, y, z, :], axis=1))
            self.field = np.transpose(envelope_field,  (3, 2, 1, 0))
            self.params.general['Xrange'] = [x_range[0], x_range[-1]]
            self.params.general['Yrange'] = [y_range[0], y_range[-1]]
            self.params.general['Zrange'] = [z_range[0], z_range[-1]]
            self.params.general['Nx'] = Nx
            self.params.general['Ny'] = Ny
            self.params.general['Nz'] = Nz
        except Exception as e:
            print(f"[AOT-biomaps] Error in _load_fieldHYDRO_XYZ method: {e}")
            raise

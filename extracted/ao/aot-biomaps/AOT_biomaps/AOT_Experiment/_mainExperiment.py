"""Base experiment abstractions and memory-aware AO forward modelling.

Acoustic fields are intentionally processed on the memory layer where they
reside: GPU-resident arrays stay on their owning device, materialized arrays
use one bandwidth-saturating CPU worker, and file-backed arrays are read by a
bounded pool of chunk workers. Full acoustic matrices are never copied to VRAM
just to compute the AO forward model.
"""

from __future__ import annotations

import copy
from abc import ABC, abstractmethod
import gc
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.ndimage import zoom
from threadpoolctl import threadpool_limits
from tqdm.auto import tqdm, trange

from AOT_biomaps.Settings import Params
from AOT_biomaps.AOT_Optic._mainOptic import Phantom
from AOT_biomaps.AOT_Acoustic.AcousticEnums import FormatSave, TypeSim, WaveType
from AOT_biomaps.AOT_Medium.BubbleMedium import BubbleMedium
from AOT_biomaps.AOT_Medium.HomogeneousMedium import HomogeneousMedium
from AOT_biomaps.AOT_Medium.MediumEnums import PhantomType
from AOT_biomaps.AOT_Medium.PVAMedium import PVAMedium
from AOT_biomaps.AOT_Acoustic.AcousticTools import get_available_host_memory_bytes
from AOT_biomaps.AOT_Experiment.ExperimentTools import (
    create_dark_transparent_hot_cmap,
    load_AOsignal,
)

try:
    import cupy as cp
except ImportError:  # pragma: no cover - depends on the runtime
    cp = None

CUPY_AVAILABLE = cp is not None


def _is_memmap_backed(array):
    """Return True when an ndarray or one of its base objects is a memmap."""
    current = array
    while current is not None:
        if isinstance(current, np.memmap):
            return True
        current = getattr(current, "base", None)
    return False


def _field_is_cupy(array):
    """Identify CuPy arrays without importing CuPy in CPU-only installations."""
    return CUPY_AVAILABLE and isinstance(array, cp.ndarray)

class Experiment(ABC):
    def __init__(self, params, acousticType=WaveType.StructuredWave, formatSave=FormatSave.HDR_IMG):
        """Initialize an experiment and its optional data containers."""
        if not isinstance(params, Params):
            raise TypeError("params must be an instance of Params.")
        if not isinstance(acousticType, WaveType):
            raise TypeError("acousticType must be an instance of WaveType.")
        if not isinstance(formatSave, FormatSave):
            raise TypeError("formatSave must be an instance of FormatSave.")
    
        self.params = params
        self.OpticImage = None
        self.medium = None
        self.AcousticFields = None
        self.AOsignal_withTumor = None
        self.AOsignal_withoutTumor = None
        self.expParams = None
        self.FormatSave = formatSave
        self.TypeAcoustic = acousticType

    def copy(self):
        """Return a deep copy of the experiment and its owned data.

        This operation intentionally duplicates resident field arrays. For
        large experiments, use :meth:`release_fields` or reload file-backed
        fields instead of copying the complete object.
        """
        return copy.deepcopy(self)
    
    def generate_phantom(self):
        """
        Generate the phantom for the experiment.
        This method initializes the OpticImage attribute with a Phantom instance.
        """
        self.OpticImage = Phantom(params=self.params)
    
    def generate_medium(self):
        """
        Generate the medium for the experiment.
        This method initializes the medium attribute based on the parameters.
        """
        if self.params.acoustic['medium']['type'] == PhantomType.Homogeneous.value:
            try:
                self.medium = HomogeneousMedium(params=self.params)
                self.medium.generate_medium()
                print("[AOT-biomaps] Medium generated: Homogeneous. -- done.")
            except Exception as e:
                print(f"[AOT-biomaps] Error generating Homogeneous medium: {e}")
                raise
        elif self.params.acoustic['medium']['type'] == PhantomType.Bubble.value:
            try:
                self.medium = BubbleMedium(params=self.params)
                self.medium.generate_medium()
                print("[AOT-biomaps] Medium generated: Bubbles. -- done.")
            except Exception as e:
                print(f"[AOT-biomaps] Error generating Bubble medium: {e}")
                raise
        elif self.params.acoustic['medium']['type'] == PhantomType.PVA.value:
            try:
                self.medium = PVAMedium(params=self.params)
                self.medium.generate_medium()
                print("[AOT-biomaps] Medium generated: PVA heterogeneous. -- done.")
            except Exception as e:
                print(f"[AOT-biomaps] Error generating PVA medium: {e}")
                raise
        else:   
            raise ValueError(f"[AOT-biomaps] Unsupported medium type: {self.params.acoustic['medium']['type']}. Supported options are in PhantomType Enum: {list(PhantomType)}")
    
    def load_medium(self, folderPath, fileName="medium"):
        """
        Load the medium from a .npy file.
        
        Parameters:
        - folderPath (str): The directory where the file is located.
        - fileName (str): The name of the file (without extension).
        
        Raises:
            ValueError: If medium type is not supported.
            FileNotFoundError: If the file does not exist.
        """
        if self.params.acoustic['medium']['type'] == PhantomType.Homogeneous.value:
            self.medium = HomogeneousMedium(params=self.params)
            self.medium.load_medium(folderPath, fileName)
        elif self.params.acoustic['medium']['type'] == PhantomType.PVA.value:
            self.medium = PVAMedium(params=self.params)
            self.medium.load_medium(folderPath, fileName)
        elif self.params.acoustic['medium']['type'] == PhantomType.Bubble.value:
            self.medium = BubbleMedium(params=self.params)
            self.medium.load_medium(folderPath, fileName)
        else:
            raise ValueError(f"[AOT-biomaps] Unsupported medium type: {self.params.acoustic['medium']['type']}. Supported options are in PhantomType Enum: {list(PhantomType)}")

    def save_medium(self, folderPath, fileName="medium"):
        """
        Save the medium to a .npy file.
        
        Parameters:
        - folderPath (str): The directory where the file will be saved.
        - fileName (str): The name of the file (without extension).
        
        Raises:
            ValueError: If medium is not initialized.
        """
        if self.medium is None:
            raise ValueError("[AOT-biomaps] Medium is not initialized. Please generate or set the medium before saving.")
        self.medium.save_medium(folderPath, fileName)

    def load_experiment_data(
        self, file_path, withTumor=True, N_average=None, start_index=0, keep_raw=True
    ):
        """Load acquisition metadata and average repeated raw acquisitions.
    
        Parameters
        ----------
        file_path : str or path-like
            MATLAB acquisition file.
        withTumor : bool
            Select the destination AO signal attribute.
        N_average : int or None
            Number of repetitions to average. ``None`` uses all repetitions.
        start_index : int
            First repetition used when ``N_average`` is specified.
        keep_raw : bool
            Retain the original raw array in ``expParams``. Disable this to
            release the large raw acquisition as soon as averaging completes.
        """
        mat = loadmat(file_path)
        raw = mat.get("raw")
        self.expParams = {
            "TypeOfSequence": str(np.squeeze(mat["TypeOfSequence"])) if "TypeOfSequence" in mat else None,
            "data_raw": raw if keep_raw else None,
            "ScanParam": mat.get("ScanParam"),
            "FreqSonde": float(np.squeeze(mat["FreqSonde"])) * 1e6 if "FreqSonde" in mat else None,
            "Naverage": int(np.squeeze(mat["NTrig"])) if "NTrig" in mat else None,
            "Nelement": int(np.squeeze(mat["NbElemts"])) if "NbElemts" in mat else None,
            "SampleRate": float(np.squeeze(mat["SampleRate"])) if "SampleRate" in mat else None,
            "Volt": float(np.squeeze(mat["Volt"])) if "Volt" in mat else None,
            "nbHemicycle": float(np.squeeze(mat["NbHemicycle"])) if "NbHemicycle" in mat else None,
            "prof": float(np.squeeze(mat["Prof"])) if "Prof" in mat else None,
            "c": float(np.squeeze(mat["c"])) if "c" in mat else None,
            "pitch": float(np.squeeze(mat["pitch"])) if "pitch" in mat else None,
            "z": np.squeeze(mat["z"]) if "z" in mat else None,
            "ActiveListMatrix": mat.get("ActiveLIST"),
            "DelayLAWS": mat.get("DelayLAWS"),
            "AngleMatrix": np.squeeze(mat["Alphas"]) if "Alphas" in mat else None,
            "decimation": np.squeeze(mat["decimation"]) if "decimation" in mat else None,
            "dFx": float(np.squeeze(mat["dFx"])) if "dFx" in mat else None,
            "Foc": float(np.squeeze(mat["Foc"])) if "Foc" in mat else None,
            "x": np.squeeze(mat["x"]) if "x" in mat else None,
        }
    
        if raw is None:
            print("[AOT-biomaps] Warning: 'raw' dataset not found in the file.")
            print("[AOT-biomaps] Available datasets:", list(mat.keys()))
            return
    
        n_average = self.expParams["Naverage"]
        if n_average is None:
            raise KeyError("The acquisition file contains 'raw' but no 'NTrig' repetition count.")
        if raw.shape[0] % n_average:
            raise ValueError(
                f"Raw data length {raw.shape[0]} is not divisible by NTrig={n_average}."
            )
        data = raw.reshape(raw.shape[0], n_average, -1)
        if N_average is None:
            selected = data
        else:
            N_average = int(N_average)
            start_index = int(start_index)
            end_index = start_index + N_average
            if N_average <= 0 or start_index < 0 or end_index > n_average:
                raise ValueError(
                    f"Invalid repetition range [{start_index}, {end_index}); available repetitions: {n_average}."
                )
            selected = data[:, start_index:end_index, :]
        mean_signal = np.mean(selected, axis=1)
    
        if withTumor:
            self.AOsignal_withTumor = mean_signal
        else:
            self.AOsignal_withoutTumor = mean_signal
    
        # Drop the raw MAT payload when the caller explicitly requested the
        # memory-saving mode. ``mat`` owns another reference to the same array.
        if not keep_raw:
            del raw
            mat.clear()
        del data, selected, mat
    
    @abstractmethod
    def generate_acoustic_fields(self, *args, **kwargs):
        """Generate or load the acoustic-field collection in a subclass."""
        raise NotImplementedError

    def release_fields(self, fieldDataPath=None, lazy_reload=False):
        """Release field arrays, optionally reopening disk-backed views.
    
        Parameters
        ----------
        fieldDataPath : str or None
            Directory containing previously saved acoustic fields.
        lazy_reload : bool
            If True, reopen each field from disk after releasing its resident
            array. HDR/IMG fields are mapped lazily by the acoustic loader.
        """
        if self.AcousticFields is None:
            return 0
        if lazy_reload and fieldDataPath is None:
            raise ValueError("fieldDataPath is required when lazy_reload=True.")
    
        released = 0
        for field in self.AcousticFields:
            if getattr(field, "field", None) is not None:
                field.field = None
                released += 1
                if lazy_reload:
                    field.load_field(fieldDataPath, self.FormatSave, None)
        gc.collect()
        print(f"[AOT-biomaps] Released or remapped {released} acoustic fields.")
        return released

    def reshape_acoustic_fields(self,dx=None, dy=None, dz=None, dt=None, Nx=None, Ny=None, Nz=None, Nt=None, factorX=None, factorY=None, factorZ=None, factorT=None, reshape_type='NxNyNz', isGPU=None, GPUdevice=None, overwrite=False, fieldDataPath=None):
        """
        Reshape the acoustic fields by downsampling them by a given factor.
        Args:
            factor: Downsampling factor (tuple of 4 integers for T, Z, Y, X).
            GPUdevice: GPU device to use for reshaping (if isGPU is True).
            isGPU: Whether to use GPU for reshaping. If None, it will be determined based on configuration.
        """
        for field in tqdm(self.AcousticFields,  desc="Reshaping Acoustic Fields", unit="field"):
            field.reshape_field(dx=dx, dy=dy, dz=dz, dt=dt, Nx=Nx, Ny=Ny, Nz=Nz, Nt=Nt, factorX=factorX, factorY=factorY, factorZ=factorZ, factorT=factorT, reshape_type=reshape_type, isGPU=isGPU, GPUdevice=GPUdevice)
            if overwrite:
                if fieldDataPath is None:
                    raise ValueError("[AOT-biomaps] fieldDataPath must be provided when overwrite is True.")
                if self.params.acoustic['typeSim'] != TypeSim.SIMPLE_SIM.value:
                    field.save_field(fieldDataPath, formatSave=self.FormatSave)
    
    def uniform_size(self, withTumor=True):
        """
        Zoom only the AO signals (Times, N) to match the minimal temporal size of AcousticFields.
        """
        if not self.AcousticFields:
            raise ValueError("[AOT-biomaps] AcousticFields is empty. Cannot uniform size.")

        # Determine the minimal temporal shape across all acoustic fields
        min_temp_shape = np.min([field.field.shape[0] for field in self.AcousticFields])

        # Select the AO signal to zoom
        AO_signal = self.AOsignal_withTumor if withTumor else self.AOsignal_withoutTumor
        if AO_signal is None:
            raise ValueError("[AOT-biomaps] AO signal is None. Cannot uniform size.")

        # Calculate zoom factor for the temporal axis (axis=0)
        original_temp_shape = AO_signal.shape[0]
        zoom_factor = min_temp_shape / original_temp_shape

        # Apply zoom only on the temporal axis (axis=0)
        zoomed_AO_signal = zoom(AO_signal, zoom=(zoom_factor, 1), order=3)

        if withTumor:
            self.AOsignal_withTumor = zoomed_AO_signal
        else:
            self.AOsignal_withoutTumor = zoomed_AO_signal

    def generate_random_absorbers(self, N_min=0, N_max=5, min_radius_mm=0.5,
                                  max_radius_mm=5, min_amplitude=0,
                                  max_amplitude=1, seed=None):
        """Generate a random set of Gaussian optical absorbers.

        Radius and amplitude are sampled from the historical distributions and
        clipped to the supplied bounds. Centers are sampled inside the optical
        field of view, with one absorber radius of clearance from each edge.
        """
        if seed is not None:
            np.random.seed(seed)

        N = int(np.random.normal(loc=2.5, scale=1.5))
        N = max(N_min, min(N, N_max))

        absorbers = []
        for i in range(N):
            radius_mm = np.random.normal(loc=10, scale=5)
            radius_mm = max(min_radius_mm, min(radius_mm, max_radius_mm))
            radius = radius_mm / 1000.0  # Convert millimetres to metres.

            amplitude = np.random.normal(loc=0.5, scale=0.25)
            amplitude = max(min_amplitude, min(amplitude, max_amplitude))

            z_center = np.random.uniform(
                low=self.params.general["Zrange"][0] + radius,
                high=self.params.general["Zrange"][1] - radius
            )
            x_center = np.random.uniform(
                low=self.params.general["Xrange"][0] + radius,
                high=self.params.general["Xrange"][1] - radius
            )

            absorbers.append({
                "name": f"Absorber_{i+1}",
                "type": "Gaussian",
                "center": [x_center, z_center],
                "radius": radius,
                "amplitude": amplitude
            })

        return absorbers
    
    def cut_acoustic_fields(self, max_t, min_t=0, show_log=True):
        """Crop every acoustic field along time using sample indices.
    
        ``min_t`` and ``max_t`` are integer sample indices, not times in
        seconds. Slicing is view-based for NumPy arrays and memmaps, so it does
        not duplicate the complete field.
        """
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is empty. Cannot crop fields.")
        if int(min_t) != min_t or int(max_t) != max_t:
            raise TypeError("min_t and max_t must be integer sample indices.")
        min_t, max_t = int(min_t), int(max_t)
        if min_t < 0 or max_t <= min_t:
            raise ValueError("Require 0 <= min_t < max_t.")
    
        iterator = range(len(self.AcousticFields))
        if show_log:
            iterator = trange(len(self.AcousticFields), desc=f"[AOT-biomaps] Cropping fields [{min_t}:{max_t}]")
        for index in iterator:
            acoustic_field = self.AcousticFields[index]
            if acoustic_field.field is None:
                raise ValueError(f"Field {acoustic_field.get_name_field()} is not loaded.")
            if acoustic_field.field.shape[0] < max_t:
                raise ValueError(
                    f"Field {acoustic_field.get_name_field()} has {acoustic_field.field.shape[0]} frames; "
                    f"cannot crop up to sample {max_t}."
                )
            acoustic_field.field = acoustic_field.field[min_t:max_t]
        return self.AcousticFields

    def add_noise(self, y=None, noiseType='gaussian', snr_dB=20.0, noiseLvl=0.1, dataToUse=None, m=1, withTumor=True, keep_nonnegative=False, noiseScope='global', show_log=True):
        """
        Add noise to AO signals with various noise models.

        Supported noise types:
        - 'gaussian': additive Gaussian noise with target SNR (dB):
            sigma_n = RMS(signal) * 10^(-snr_dB / 20)
        - 'poisson': Poisson noise proportional to signal amplitude (uses noiseLvl)
        - 'experimental': noise with same SNR as experimental dataToUse for m averages

        Parameters:
            y (np.ndarray, optional): Input signal. If None, uses self.AOsignal_withTumor
                or self.AOsignal_withoutTumor.
            noiseType (str): Type of noise ('gaussian', 'poisson', or 'experimental').
            snr_dB (float): Target SNR in dB for gaussian noise (SNR_dB = 10*log10(Ps/Pn)).
            noiseLvl (float): Noise level for poisson noise.
            dataToUse (np.ndarray): Experimental data for 'experimental' noise type
                (shape: (n_repeats, n_signals)).
            m (int): Number of averages for 'experimental' noise type.
            withTumor (bool): If True and y is None, use signal with tumor.
            keep_nonnegative (bool): If True, shift each signal by its minimum BEFORE
                adding noise, so that the requested SNR is preserved (the SNR is then
                defined w.r.t. the shifted signal).
            noiseScope (str): Noise level definition for gaussian noise.
                'global' (default): sigma_n is computed once from the RMS of ALL
                signals, so the same absolute noise level is applied to every signal
                (mimics detector noise). The effective per-signal SNR then varies
                with signal amplitude; snr_dB is defined w.r.t. the global RMS.
                'per_signal': sigma_n is proportional to each signal's own RMS,
                so every signal has the same nominal SNR (original behavior).
            show_log (bool): If True, displays progress bar.

        Returns:
            np.ndarray: Noisy signal(s) with same shape as input.
        """
        # Select signal source
        if y is None:
            if withTumor:
                if self.AOsignal_withTumor is None:
                    raise ValueError("[AOT-biomaps] AO signal with tumor not generated. Generate it first.")
                signals = self.AOsignal_withTumor
            else:
                if self.AOsignal_withoutTumor is None:
                    raise ValueError("[AOT-biomaps] AO signal without tumor not generated. Generate it first.")
                signals = self.AOsignal_withoutTumor
        else:
            signals = y

        # For experimental noise, estimate noise parameters from dataToUse
        if noiseType.lower() == 'experimental':
            if dataToUse is None:
                raise ValueError("[AOT-biomaps] dataToUse must be provided for experimental noise type.")
            n_pairs = min(500, dataToUse.shape[0] // 2)
            random_pairs = np.random.choice(dataToUse.shape[0], size=(n_pairs, 2), replace=False)
            noise_var = 0.0
            for i, k in random_pairs:
                diff = dataToUse[i, :] - dataToUse[k, :]
                noise_var += np.sum(diff**2)
            # E[(n_i - n_k)^2] = 2*sigma_n^2  ->  unbiased sigma_n^2
            noise_var /= (2 * dataToUse.shape[1] * n_pairs)
            noise_var_for_m = noise_var / m
            mean_signal = np.mean(dataToUse, axis=0)
            amplitude_real = np.std(mean_signal)

        # Pre-compute sigma_n for gaussian noise according to noiseScope
        if noiseType.lower() == 'gaussian':
            if noiseScope == 'global':
                # One common noise level from the global RMS of all signals
                global_power = np.mean(signals**2)
                sigma_n_global = np.sqrt(global_power / 10**(snr_dB / 10.0))
            elif noiseScope == 'per_signal':
                sigma_n_global = None  # computed per signal inside the loop
            else:
                raise ValueError("[AOT-biomaps] noiseScope must be 'global' or 'per_signal'.")

        noiseSignals = np.zeros_like(signals)
        n_signals = signals.shape[1]

        iteration = trange(n_signals, desc=f"[AOT-biomaps] Adding {noiseType} noise") if show_log else range(n_signals)
        for i in iteration:
            signal = signals[:, i]

            # Shift BEFORE noise so the requested SNR is preserved
            if keep_nonnegative and np.min(signal) < 0:
                signal = signal - np.min(signal)

            if noiseType.lower() == 'gaussian':
                if sigma_n_global is None:
                    # per-signal SNR: sigma_n proportional to this signal's RMS
                    signal_power = np.mean(signal**2)
                    sigma_n = np.sqrt(signal_power / 10**(snr_dB / 10.0))
                else:
                    # global noise level, identical for all signals
                    sigma_n = sigma_n_global
                noise = np.random.normal(0, sigma_n, signal.shape)
                noisy_signal = signal + noise
            elif noiseType.lower() == 'poisson':
                max_signal = np.max(np.abs(signal))
                if max_signal != 0:
                    noise = np.random.poisson(noiseLvl * np.abs(signal)) / (noiseLvl * max_signal)
                    noisy_signal = signal * noise
                else:
                    noisy_signal = signal.copy()
            elif noiseType.lower() == 'experimental':
                amplitude_y = np.max(np.abs(signal))
                amplitude_ratio = amplitude_y / amplitude_real
                noise = np.random.randn(signal.shape[0]) * np.sqrt(noise_var_for_m) * amplitude_ratio
                noisy_signal = signal + noise
            else:
                raise ValueError("[AOT-biomaps] noiseType must be 'gaussian', 'poisson', or 'experimental'.")

            noiseSignals[:, i] = noisy_signal

        return noiseSignals
    
    def reduce_dims(self, mode="avg"):
        """Downsample each ``(time, z, x)`` field by two on all axes.

        Existing CuPy fields are pooled on their current GPU and remain there.
        NumPy arrays and file-backed memmaps are processed on the CPU, so the
        method never copies a complete host field to VRAM merely because CuPy
        is installed. Odd trailing samples are discarded, matching valid
        2-by-2-by-2 pooling.

        Parameters
        ----------
        mode : {"avg", "max"}
            Pooling operation applied to each 2-by-2-by-2 block.
        """
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is not initialized or is empty.")
        if mode not in ("avg", "max"):
            raise ValueError("mode must be either 'avg' or 'max'.")

        for index in trange(
            len(self.AcousticFields),
            desc="[AOT-biomaps] Downsampling acoustic fields (T, Z, X)",
        ):
            acoustic_field = self.AcousticFields[index]
            field = acoustic_field.field
            if field is None or field.ndim != 3:
                shape = None if field is None else field.shape
                raise ValueError(
                    f"Unsupported acoustic-field shape {shape}; expected (T, Z, X)."
                )

            nt, nz, nx = map(int, field.shape)
            nt2, nz2, nx2 = nt // 2, nz // 2, nx // 2
            if min(nt2, nz2, nx2) == 0:
                raise ValueError(
                    f"Field dimensions {field.shape} are too small to downsample by two."
                )

            if _field_is_cupy(field):
                # Run on the array's owning device. The crop and added batch/
                # channel dimensions are views and do not duplicate the input.
                with cp.cuda.Device(int(field.device.id)):
                    cropped = field[:2 * nt2, :2 * nz2, :2 * nx2]
                    pooling_input = cropped[None, None, ...]
                    if mode == "avg":
                        reduced = cp.nn.pooling.avg_pool3d(
                            pooling_input, kernel_size=(2, 2, 2), stride=(2, 2, 2)
                        )
                    else:
                        reduced = cp.nn.pooling.max_pool3d(
                            pooling_input, kernel_size=(2, 2, 2), stride=(2, 2, 2)
                        )
                    # Preserve the historical host-resident result convention;
                    # the reduced output is much smaller than the original field.
                    reduced_host = cp.asnumpy(reduced[0, 0])
                    acoustic_field.field = reduced_host
                    del pooling_input, cropped, reduced
            else:
                # All intermediate views are zero-copy. Only the reduced
                # output is allocated, keeping memmap-backed processing lazy.
                cropped = field[:2 * nt2, :2 * nz2, :2 * nx2]
                blocks = cropped.reshape(nt2, 2, nz2, 2, nx2, 2)
                if mode == "avg":
                    reduced = blocks.mean(axis=(1, 3, 5), dtype=np.float32)
                else:
                    reduced = blocks.max(axis=(1, 3, 5))
                acoustic_field.field = reduced

        general = self.params.general
        if general.get("ft") is not None:
            general["ft"] = float(general["ft"]) / 2.0
        for key in ("dx", "dy", "dz"):
            if general.get(key) is not None:
                general[key] = float(general[key]) * 2.0
        return self.AcousticFields

    def normalize_AOsignals(self, withTumor=True):
        """Min-max normalize one stored AO signal in place when possible."""
        attribute = "AOsignal_withTumor" if withTumor else "AOsignal_withoutTumor"
        signal = getattr(self, attribute)
        if signal is None:
            label = "with tumor" if withTumor else "without tumor"
            raise ValueError(f"AO signal {label} has not been generated.")
        if not np.issubdtype(signal.dtype, np.floating) or not signal.flags.writeable:
            signal = np.array(signal, dtype=np.float32, copy=True)
        minimum = float(np.min(signal))
        dynamic_range = float(np.max(signal)) - minimum
        if dynamic_range <= 0.0:
            signal.fill(0)
        else:
            np.subtract(signal, minimum, out=signal, casting="unsafe")
            np.divide(signal, dynamic_range, out=signal, casting="unsafe")
        setattr(self, attribute, signal)
        return signal

    def save_acoustic_fields(self, save_directory):
        """Save all loaded acoustic fields using the experiment's file format."""
        if self.AcousticFields is None:
            raise ValueError("AcousticFields is not initialized.")
        progress_bar = trange(len(self.AcousticFields), desc="[AOT-biomaps] Saving Acoustic Fields")
        for i in progress_bar:
            progress_bar.set_postfix_str(f"-- {self.AcousticFields[i].get_name_field()}")
            self.AcousticFields[i].save_field(save_directory, formatSave=self.FormatSave)

    def show_animated_acoustic(self, wave_name=None, desired_duration_ms=5000, save_dir=None, figsize=(12, 5)):
        """Display synchronized animations of the loaded acoustic fields."""
        if not self.AcousticFields:
            raise ValueError("AcousticFields is empty.")
        n_fields = len(self.AcousticFields)
        n_frames = min(int(field.field.shape[0]) for field in self.AcousticFields)
        if n_frames <= 0:
            raise ValueError("Acoustic fields contain no time frames.")
    
        mpl.rcParams["animation.embed_limit"] = 100
        if save_dir is not None:
            os.makedirs(save_dir, exist_ok=True)
    
        ncols = min(5, n_fields)
        nrows = (n_fields + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
        axes = axes.ravel()
        ims = []
        fig.suptitle(f"System Matrix Animation {wave_name or ''}", y=0.98)
    
        for index, acoustic_field in enumerate(self.AcousticFields):
            image = axes[index].imshow(
                acoustic_field.field[0],
                extent=(
                    self.params.general["Xrange"][0], self.params.general["Xrange"][1],
                    self.params.general["Zrange"][1], self.params.general["Zrange"][0],
                ),
                vmax=1,
                aspect="equal",
                cmap="jet",
                animated=True,
            )
            axes[index].set_xlabel("x (m)")
            axes[index].set_ylabel("z (m)")
            ims.append(image)
        for index in range(n_fields, len(axes)):
            fig.delaxes(axes[index])
    
        plt.tight_layout(rect=[0, 0, 1, 0.95])
    
        def update(frame):
            for image, acoustic_field in zip(ims, self.AcousticFields):
                image.set_data(acoustic_field.field[frame])
            fig.suptitle(f"System Matrix Animation {wave_name or ''} — frame {frame}")
            return ims
    
        interval = float(desired_duration_ms) / n_frames
        movie = animation.FuncAnimation(
            fig, update, frames=range(n_frames), interval=interval, blit=True
        )
        if save_dir is not None:
            date_string = datetime.now().strftime("%Y_%d_%m_%y")
            safe_name = wave_name or "all_fields"
            save_path = os.path.join(save_dir, f"AcousticField_{safe_name}_{date_string}.gif")
            movie.save(save_path, writer="pillow", fps=20)
            print(f"[AOT-biomaps] Saved: {save_path}")
    
        plt.close(fig)
        return movie

    def generate_AOsignal(self, withTumor=True, AOsignalDataPath=None, n_workers=16):
        """Compute ``y(t, i) = sum_{z,x} A(t,z,x,i) * lambda(z,x)``.

        Fields are processed where they already reside:

        * CuPy arrays are projected on their owning GPU; only one temporal
          trace per field is copied back to the host.
        * Resident NumPy arrays are processed serially with multithreaded BLAS.
        * Memmaps and other file-backed arrays use a bounded set of disk-reader
          workers. Contiguous float32 fields are passed directly to BLAS; any
          required conversion is limited to time chunks rather than a complete
          3-D field copy.

        The output is a host-side float32 array with shape ``(Nt, N_fields)``.

        Parameters
        ----------
        withTumor : bool
            Use the phantom absorption map when True, or laser intensity when
            False.
        AOsignalDataPath : str or None
            Load a precomputed AO signal instead of evaluating the forward
            model. Acoustic fields are cropped by sample index if necessary.
        n_workers : int
            Maximum number of concurrent file-backed field readers. Ignored
            for resident RAM and GPU fields.

        Returns
        -------
        numpy.ndarray
            AO signal matrix with shape ``(Nt, N_fields)`` and dtype float32.
        """
        if AOsignalDataPath is not None:
            if not os.path.isfile(AOsignalDataPath):
                raise FileNotFoundError(f"AO signal file not found: {AOsignalDataPath}")
            signal = np.asarray(load_AOsignal(AOsignalDataPath))
            if signal.ndim != 2:
                raise ValueError("Loaded AO signal must be a 2-D array (time, fields).")
            if self.AcousticFields:
                first = self.AcousticFields[0].field
                if first is None:
                    raise ValueError("Acoustic fields must be loaded before importing AO signals.")
                expected_nt = int(first.shape[0])
                if signal.shape[0] > expected_nt:
                    signal = signal[:expected_nt]
                elif signal.shape[0] < expected_nt:
                    self.cut_acoustic_fields(max_t=signal.shape[0], min_t=0, show_log=False)
            setattr(self, "AOsignal_withTumor" if withTumor else "AOsignal_withoutTumor", signal)
            return signal

        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is empty. Generate or load the system matrix first.")
        if self.OpticImage is None:
            raise ValueError("OpticImage is not initialized.")

        if any(item.field is None for item in self.AcousticFields):
            raise ValueError("Every acoustic field must be loaded before AO-signal generation.")
        first_field = self.AcousticFields[0].field
        reference_shape = tuple(first_field.shape)
        if len(reference_shape) != 3:
            raise ValueError(
                f"Expected acoustic fields with shape (Nt, Nz, Nx), got {reference_shape}."
            )

        nt, nz, nx = reference_shape
        min_nt = min(int(item.field.shape[0]) for item in self.AcousticFields)
        if any(tuple(item.field.shape[1:]) != (nz, nx) for item in self.AcousticFields):
            raise ValueError("All acoustic fields must share the same spatial dimensions.")
        if any(int(item.field.shape[0]) != min_nt for item in self.AcousticFields):
            self.cut_acoustic_fields(max_t=min_nt, min_t=0, show_log=False)
        nt = min_nt
        n_fields = len(self.AcousticFields)

        optical_image = (
            self.OpticImage.phantom if withTumor else self.OpticImage.laser.intensity
        )
        if optical_image is None or tuple(optical_image.shape) != (nz, nx):
            shape = None if optical_image is None else optical_image.shape
            raise ValueError(
                f"Optical image shape {shape} does not match acoustic spatial shape {(nz, nx)}."
            )
        weights_host = np.asarray(optical_image, dtype=np.float32).reshape(-1)
        if not weights_host.flags.c_contiguous:
            weights_host = np.ascontiguousarray(weights_host)

        n_gpu_fields = (
            sum(_field_is_cupy(item.field) for item in self.AcousticFields)
            if CUPY_AVAILABLE else 0
        )
        if 0 < n_gpu_fields < n_fields:
            raise ValueError(
                "Mixed CPU/GPU field residency is not supported. Keep all fields on the host "
                "or keep all fields on their owning GPUs."
            )
        resident_vram = n_gpu_fields == n_fields
        output = np.empty((nt, n_fields), dtype=np.float32)
        description = (
            "[AOT-biomaps] AO forward model "
            + ("with" if withTumor else "without")
            + " tumor"
        )

        # Select a per-worker scratch budget only for non-contiguous/dtype
        # conversion paths. Standard C-contiguous float32 memmaps require no
        # field-sized scratch allocation at all.
        available_ram = get_available_host_memory_bytes() or 0
        worker_hint = max(1, int(n_workers))
        per_worker_scratch = (
            max(1, int(available_ram // max(8, 4 * worker_hint)))
            if available_ram else 0
        )

        def _project_numpy_field(field):
            """Project one host field without materializing a full 3-D copy."""
            if field.dtype == np.float32 and field.flags.c_contiguous:
                return field.reshape(nt, -1) @ weights_host

            frame_bytes = max(1, nz * nx * np.dtype(np.float32).itemsize)
            if per_worker_scratch:
                frames_per_chunk = max(1, min(nt, per_worker_scratch // frame_bytes))
            else:
                frames_per_chunk = 1
            projected = np.empty(nt, dtype=np.float32)
            for start in range(0, nt, frames_per_chunk):
                stop = min(start + frames_per_chunk, nt)
                chunk = np.asarray(field[start:stop], dtype=np.float32, order="C")
                projected[start:stop] = chunk.reshape(stop - start, -1) @ weights_host
                del chunk
            return projected

        if resident_vram:
            # One worker owns each existing device. Its input fields never
            # migrate between GPUs; the temporal result buffer is reused.
            fields_by_device = {}
            for index, acoustic_field in enumerate(self.AcousticFields):
                device_id = int(acoustic_field.field.device.id)
                fields_by_device.setdefault(device_id, []).append(index)

            progress = tqdm(total=n_fields, desc=description)

            def _gpu_worker(device_id, indices):
                with cp.cuda.Device(device_id):
                    device_weights = None
                    result_gpu = None
                    result_host = None
                    current_dtype = None
                    for index in indices:
                        field = self.AcousticFields[index].field
                        dtype = field.dtype
                        if current_dtype != dtype:
                            device_weights = cp.asarray(weights_host, dtype=dtype)
                            result_gpu = cp.empty(nt, dtype=dtype)
                            result_host = np.empty(nt, dtype=np.dtype(dtype))
                            current_dtype = dtype

                        if field.flags.c_contiguous:
                            cp.matmul(field.reshape(nt, -1), device_weights, out=result_gpu)
                        else:
                            # Reshape only small temporal chunks; never let a
                            # non-contiguous field trigger a full GPU copy.
                            frame_bytes = max(1, nz * nx * int(dtype.itemsize))
                            free_bytes = int(cp.cuda.runtime.memGetInfo()[0])
                            chunk_budget = max(frame_bytes, free_bytes // 16)
                            frames_per_chunk = max(1, min(nt, chunk_budget // frame_bytes))
                            for start in range(0, nt, frames_per_chunk):
                                stop = min(start + frames_per_chunk, nt)
                                chunk = cp.ascontiguousarray(field[start:stop]).reshape(stop - start, -1)
                                cp.matmul(
                                    chunk,
                                    device_weights,
                                    out=result_gpu[start:stop],
                                )
                                del chunk

                        result_gpu.get(out=result_host, blocking=True)
                        output[:, index] = result_host
                        progress.update(1)
                    del device_weights, result_gpu, result_host

            try:
                with ThreadPoolExecutor(max_workers=len(fields_by_device)) as executor:
                    futures = [
                        executor.submit(_gpu_worker, device_id, indices)
                        for device_id, indices in fields_by_device.items()
                    ]
                    for future in as_completed(futures):
                        future.result()
            finally:
                progress.close()

        elif not any(_is_memmap_backed(item.field) for item in self.AcousticFields):
            # One CPU worker plus threaded BLAS is typically the most efficient
            # path for resident RAM arrays and avoids concurrent large reads.
            with threadpool_limits(limits=os.cpu_count() or 1):
                for index, acoustic_field in enumerate(tqdm(self.AcousticFields, desc=description)):
                    output[:, index] = _project_numpy_field(acoustic_field.field)

        else:
            # File-backed fields are assigned in contiguous index ranges. Each
            # worker writes directly to its output columns and submits only one
            # future, avoiding a queue of full-field task arguments/results.
            worker_count = min(worker_hint, n_fields)
            edges = np.linspace(0, n_fields, worker_count + 1, dtype=np.int64)
            progress = tqdm(total=n_fields, desc=description)

            def _disk_worker(start, stop):
                for index in range(start, stop):
                    output[:, index] = _project_numpy_field(
                        self.AcousticFields[index].field
                    )
                    progress.update(1)

            try:
                with threadpool_limits(limits=1):
                    with ThreadPoolExecutor(max_workers=worker_count) as executor:
                        futures = [
                            executor.submit(_disk_worker, int(edges[i]), int(edges[i + 1]))
                            for i in range(worker_count)
                        ]
                        for future in as_completed(futures):
                            future.result()
            finally:
                progress.close()

        attribute = "AOsignal_withTumor" if withTumor else "AOsignal_withoutTumor"
        setattr(self, attribute, output)
        return output

    def save_AOsignals_Castor(self, save_directory, withTumor=True):
        """Write AO signals and acquisition metadata in Castor CDF/CDH format."""
        signal = self.AOsignal_withTumor if withTumor else self.AOsignal_withoutTumor
        if signal is None:
            label = "with tumor" if withTumor else "without tumor"
            raise ValueError(f"AO signal {label} is not available.")
        if self.AcousticFields is None or len(self.AcousticFields) != signal.shape[1]:
            raise ValueError("The number of acoustic fields must match the AO signal columns.")
    
        os.makedirs(save_directory, exist_ok=True)
        stem = "AOSignals_withTumor" if withTumor else "AOSignals_withoutTumor"
        cdf_path = os.path.join(save_directory, f"{stem}.cdf")
        cdh_path = os.path.join(save_directory, f"{stem}.cdh")
        info_path = os.path.join(save_directory, "info.txt")
        signal = np.asarray(signal)
    
        with open(cdf_path, "wb") as output_file:
            for index, acoustic_field in enumerate(self.AcousticFields):
                pattern_hex = acoustic_field.pattern.activeList
                output_file.write(bytes.fromhex(pattern_hex))
                output_file.write(np.asarray(acoustic_field.angle, dtype=np.int8).tobytes())
                np.asarray(signal[:, index], dtype=np.float32).tofile(output_file)
    
        header = (
            f"Data filename: {stem}.cdf\n"
            f"Number of events: {signal.shape[1]}\n"
            f"Number of acquisitions per event: {signal.shape[0]}\n"
            "Start time (s): 0\n"
            "Duration (s): 1\n"
            f"Acquisition frequency (Hz): {self.params.general['ft']}\n"
            "Data mode: histogram\n"
            "Data type: AOT\n"
            f"Number of US transducers: {self.params.acoustic['probe']['num_elements']}"
        )
        with open(cdh_path, "w", encoding="utf-8") as header_file:
            header_file.write(header)
        with open(info_path, "w", encoding="utf-8") as info_file:
            for acoustic_field in self.AcousticFields:
                info_file.write(acoustic_field.get_name_field() + "\n")
        print(f"[AOT-biomaps] Castor files saved in {save_directory}.")
        return cdf_path, cdh_path, info_path

    def show_AOsignal(self, withTumor=True, save_dir=None, wave_name=None, figsize=(12, 5)):
        """Plot all AO signal traces for one optical phantom condition."""
        signal = self.AOsignal_withTumor if withTumor else self.AOsignal_withoutTumor
        if signal is None:
            label = "with tumor" if withTumor else "without tumor"
            raise ValueError(f"AO signal {label} is not available.")
        signal = np.asarray(signal)
        time_us = np.arange(signal.shape[0], dtype=np.float64) / float(self.params.general["ft"]) * 1e6
        if signal.ndim != 2 or signal.shape[1] == 0:
            raise ValueError("AO signal must be a non-empty 2-D array (time, traces).")
        n_traces = signal.shape[1]
        ncols = min(5, n_traces)
        nrows = (n_traces + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
        axes = axes.ravel()
        title = f"AO Signal — {wave_name}" if wave_name else "AO Signal — all traces"
        fig.suptitle(title, y=0.98)

        for index in range(n_traces):
            axes[index].plot(time_us, signal[:, index])
            axes[index].set_xlabel("Time (µs)")
            axes[index].set_ylabel("Amplitude")
        for index in range(n_traces, len(axes)):
            fig.delaxes(axes[index])
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        if save_dir is not None:
            os.makedirs(save_dir, exist_ok=True)
            date_string = datetime.now().strftime("%Y_%d_%m_%y")
            safe_name = wave_name or "all_traces"
            save_path = os.path.join(save_dir, f"AO_signal_{safe_name}_{date_string}.png")
            fig.savefig(save_path, dpi=200, bbox_inches="tight")
            print(f"[AOT-biomaps] Saved: {save_path}")
        plt.show()
        plt.close(fig)
        return fig

    def show_experiment_static(
        self, fileOfAcousticField=None, N_file=None, save_dir=None,
        withTumor=True, t=None, figsize=(8, 4), wave_name=None
    ):
        """Display one acoustic-field frame alongside its AO temporal trace."""
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is empty.")
        if fileOfAcousticField is not None and N_file is not None:
            raise ValueError("Provide either fileOfAcousticField or N_file, not both.")
        if fileOfAcousticField is None and N_file is None:
            index = 0
            print("[AOT-biomaps] No field selected; displaying the first field.")
        elif N_file is not None:
            index = int(N_file)
            if index < 0 or index >= len(self.AcousticFields):
                raise IndexError(f"N_file must be in [0, {len(self.AcousticFields) - 1}].")
        else:
            index = next(
                (i for i, field in enumerate(self.AcousticFields)
                 if field.get_name_field() == fileOfAcousticField),
                None,
            )
            if index is None:
                raise ValueError(f"Field {fileOfAcousticField!r} was not found.")
    
        field_object = self.AcousticFields[index]
        field_data = field_object.field
        if field_data is None:
            raise ValueError("The selected acoustic field is not loaded.")
        field_data = np.asarray(field_data)
        nt = field_data.shape[0]
        dt = float(self.params.general["ft"])
        t_max_us = (nt - 1) / dt * 1e6
        t = t_max_us / 2 if t is None else float(t)
        frame = int(np.clip(round(t * dt / 1e6), 0, nt - 1))
    
        signal = self.AOsignal_withTumor if withTumor else self.AOsignal_withoutTumor
        if signal is None:
            label = "with tumor" if withTumor else "without tumor"
            raise ValueError(f"AO signal {label} is not available.")
        optical_image = (
            self.OpticImage.phantom if withTumor else self.OpticImage.laser.intensity
        )
        if optical_image is None:
            raise ValueError("The requested optical image is not available.")
        if wave_name is None:
            wave_name = getattr(getattr(field_object, "pattern", None), "activeList", field_object.get_name_field())
    
        extent = [
            self.params.general["Xrange"][0] * 1e3,
            self.params.general["Xrange"][1] * 1e3,
            self.params.general["Zrange"][1] * 1e3,
            self.params.general["Zrange"][0] * 1e3,
        ]
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle(
            f"AO Signal | {wave_name} | Angle {field_object.angle}° | t = {t:.2f} µs",
            y=0.98,
        )
    
        if self.medium is not None and getattr(self.medium, "kmedium", None) is not None:
            axes[0].imshow(
                self.medium.kmedium.sound_speed.T,
                cmap="gray", origin="upper", extent=extent, aspect="equal",
            )
        optical_max = float(np.max(optical_image))
        cmap = create_dark_transparent_hot_cmap(vmin=0.2 * optical_max)
        axes[0].imshow(
            optical_image, cmap=cmap, origin="upper", extent=extent,
            aspect="equal", alpha=0.5,
        )
        frame_data = field_data[frame]
        frame_max = float(np.max(frame_data))
        if frame_max > 0:
            frame_data = frame_data / frame_max
            frame_data = np.where(frame_data > 0.02, frame_data, np.nan)
            axes[0].imshow(
                frame_data, cmap="jet", origin="upper", extent=extent,
                vmax=1, vmin=0.01, alpha=0.8, aspect="equal",
            )
        axes[0].set_xlabel("X (mm)")
        axes[0].set_ylabel("Z (mm)")
    
        time_us = np.arange(signal.shape[0]) / dt * 1e6
        if index >= signal.shape[1]:
            raise ValueError("The selected field index has no corresponding AO signal column.")
        axes[1].plot(time_us, signal[:, index], label="AO signal")
        axes[1].axvline(t, color="r", linestyle="--", label=f"t = {t:.2f} µs")
        axes[1].set_xlabel("Time (µs)")
        axes[1].set_ylabel("Amplitude")
        axes[1].legend()
        plt.tight_layout(rect=[0, 0, 1, 0.95])
    
        if save_dir is not None:
            os.makedirs(save_dir, exist_ok=True)
            date_string = datetime.now().strftime("%Y_%d_%m_%y")
            save_path = os.path.join(
                save_dir,
                f"experiment_static_{index}_{field_object.angle}_{date_string}_t{t:.2f}us.png",
            )
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"[AOT-biomaps] Saved: {save_path}")
        plt.show()
        plt.close(fig)
        return fig
    
    def show_phantom(self, withROI=False, figsize=(4,4)):
        """
        Displays the optical phantom with absorbers.
        """
        try:
            self.OpticImage.show_phantom(withROI=withROI, figsize=figsize)
        except Exception as e:
            raise RuntimeError(f"[AOT-biomaps] Error plotting phantom: {e}")
    
    def show_laser(self, figsize=(4,4)):
        """
        Displays the laser intensity distribution.
        """
        try:
            self.OpticImage.laser.show_laser(figsize=figsize)
        except Exception as e:
            raise RuntimeError(f"[AOT-biomaps] Error plotting laser: {e}")
    
    def show_medium(self, figsize=(8,4)):
        """
        Displays the medium properties.
        """
        try:
            self.medium.plot_medium_properties(figsize=figsize)
        except Exception as e:
            raise RuntimeError(f"[AOT-biomaps] Error plotting medium: {e}")

    @abstractmethod
    def check(self):
        """Validate that the concrete experiment contains all required data."""
        raise NotImplementedError

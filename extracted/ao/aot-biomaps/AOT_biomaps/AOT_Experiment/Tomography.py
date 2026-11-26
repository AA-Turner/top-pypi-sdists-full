"""Structured-wave tomography orchestration for AOT-biomaps.

This module owns pattern generation, structured-wave field orchestration,
apodization, and quadrature demodulation. Individual k-Wave simulations are
streamed by :class:`AcousticField`; this module deliberately keeps only one
simulation worker per GPU so full output fields do not accumulate in VRAM.
"""

from __future__ import annotations

import ast
import concurrent.futures
import gc
import os
import threading

import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat, savemat
from tqdm.auto import tqdm, trange

from AOT_biomaps.AOT_Acoustic.AcousticTools import (
    format_angle,
    get_angle,
    get_available_host_memory_bytes,
    get_frequency,
    hex_to_binary_profile,
)
from AOT_biomaps.AOT_Acoustic.AcousticEnums import TypeSim, WaveType
from AOT_biomaps.AOT_Acoustic.StructuredWave import StructuredWave
from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Experiment.ExperimentTools import (
    binary_to_hex_profile,
    calc_mat_os,
    convert_to_hex_list,
    get_phase_deterministic,
    load_AOsignal,
)
from AOT_biomaps.AOT_Experiment._mainExperiment import Experiment

try:
    import cupy as cp
except ImportError:  # pragma: no cover - depends on the runtime
    cp = None

CUPY_AVAILABLE = cp is not None


def _is_memmap_backed(array):
    """Return True if an array or one of its base objects is a NumPy memmap."""
    current = array
    while current is not None:
        if isinstance(current, np.memmap):
            return True
        current = getattr(current, "base", None)
    return False


class Tomography(Experiment):
    """
    Tomography experiment class for acousto-optic imaging.
    Handles structured wave patterns, acoustic field generation, and signal processing.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.patterns = None
        self.AcousticFields_demodulated = None
        self.theta = []
        self.decimations = []
        self.ActiveList = []
        self.DelayLaw = []

    # PUBLIC METHODS
    def check(self):
        """Validate that all data required by a tomography experiment exists."""
        if self.TypeAcoustic != WaveType.StructuredWave:
            raise ValueError("Tomography requires acousticType=WaveType.StructuredWave.")
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is empty. Generate or load the system matrix first.")
        if self.AOsignal_withTumor is None or self.AOsignal_withoutTumor is None:
            raise ValueError("Both AO signals (with and without tumor) must be initialized.")
        if self.OpticImage is None:
            raise ValueError("OpticImage is not initialized.")
        if self.OpticImage.phantom is None or self.OpticImage.laser is None:
            raise ValueError("The optical phantom and laser must both be initialized.")
        if self.AOsignal_withTumor.shape != self.AOsignal_withoutTumor.shape:
            raise ValueError("AO signals with and without tumor must have identical shapes.")
        if self.AOsignal_withTumor.ndim != 2:
            raise ValueError("AO signals must have shape (time, measurements).")

        reference_shape = None
        for acoustic_field in self.AcousticFields:
            field = acoustic_field.field
            if field is None or field.ndim != 3:
                raise ValueError(
                    f"Field {acoustic_field.get_name_field()} is not loaded as a (Nt, Nz, Nx) array."
                )
            if field.shape[0] != self.AOsignal_withTumor.shape[0]:
                raise ValueError(
                    f"Field {acoustic_field.get_name_field()} has {field.shape[0]} time samples; "
                    f"expected {self.AOsignal_withTumor.shape[0]}."
                )
            if reference_shape is None:
                reference_shape = tuple(field.shape)
            elif tuple(field.shape) != reference_shape:
                raise ValueError("All acoustic fields must have identical shapes.")

        if tuple(self.OpticImage.phantom.shape) != reference_shape[1:]:
            raise ValueError(
                f"Optical phantom shape {self.OpticImage.phantom.shape} does not match "
                f"acoustic spatial shape {reference_shape[1:]}."
            )
        if tuple(self.OpticImage.laser.shape) != tuple(self.OpticImage.phantom.shape):
            raise ValueError("Optical laser and phantom images must have identical shapes.")
        if self.AOsignal_withTumor.shape[1] != len(self.AcousticFields):
            raise ValueError("AO signal columns must match the number of acoustic fields.")
        print("[AOT-biomaps] Tomography experiment is correctly initialized.")

    def generate_acoustic_fields(
        self, isGPU=None, GPUdevice=None, fieldDataPath=None, tempFieldName="Kwave",
        nameBlock=None, generation_type="envelope_squared", show_log=True,
        max_workers=None, backend=None, materialize=False, vram_fraction=0.95,
        accumulate_max_bytes=None, host_staging_fraction=1.0 / 16.0,
    ):
        """Generate the structured-wave system matrix.
    
        GPU execution is bounded to one active k-Wave simulation per GPU.
        The streaming acoustic-field implementation sizes its output ring from
        current free VRAM and overlaps device-to-host transfers when the full
        field does not fit. Completed fields are returned on the host by
        default, so generating many patterns never accumulates full matrices
        in VRAM.
    
        Parameters
        ----------
        isGPU : bool or None
            Use GPU execution; ``None`` follows the package configuration.
        GPUdevice : int, sequence of int, or None
            One device or an explicit set of devices.
        fieldDataPath : str or None
            Optional directory used to load and save individual fields.
        generation_type : str
            One of ``"envelope_squared"``, ``"envelope"`` or ``"field"``.
        max_workers : int or None
            Maximum concurrent simulations. GPU execution is capped at one
            worker per selected device.
        backend : {"python", "cpp"} or None
            k-Wave backend. The Python backend supports streaming I/Q output.
        materialize : bool
            Promote loaded file-backed fields to resident host RAM when the
            estimated full collection fits the available-memory budget.
        vram_fraction : float
            Fraction of currently allocatable VRAM offered to each output ring.
        accumulate_max_bytes : int or None
            Optional caller-specified output-ring ceiling.
        host_staging_fraction : float
            Fraction of available host RAM offered to pinned transfer buffers.
        """
        if self.medium is None:
            raise ValueError("Medium is not initialized. Generate or load it first.")
        if self.TypeAcoustic != WaveType.StructuredWave:
            raise ValueError("Tomography currently supports StructuredWave acquisitions only.")
        if generation_type not in ("envelope_squared", "envelope", "field"):
            raise ValueError("generation_type must be 'envelope_squared', 'envelope', or 'field'.")
        if not (0.0 < float(vram_fraction) <= 1.0):
            raise ValueError("vram_fraction must be in (0, 1].")
        if not (0.0 < float(host_staging_fraction) <= 1.0):
            raise ValueError("host_staging_fraction must be in (0, 1].")
    
        self.AcousticFields = self._generate_acousticFields_STRUCT(
            isGPU=isGPU,
            GPUdevice=GPUdevice,
            fieldDataPath=fieldDataPath,
            tempFieldName=tempFieldName,
            nameBlock=nameBlock,
            generation_type=generation_type,
            show_log=show_log,
            max_workers=max_workers,
            backend=backend,
            materialize=materialize,
            vram_fraction=vram_fraction,
            accumulate_max_bytes=accumulate_max_bytes,
            host_staging_fraction=host_staging_fraction,
        )
        return self.AcousticFields

    def show_pattern(self,figsize=(5, 4)):
        """
        Display the transducer activation patterns.
        """
        if self.AcousticFields is None:
            raise ValueError("[AOT-biomaps] AcousticFields is not initialized. Please generate the system matrix first.")

        # Collect and sort entries
        entries = []
        for field in self.AcousticFields:
            if field.waveType != WaveType.StructuredWave:
                raise TypeError("[AOT-biomaps] AcousticFields must be of type StructuredWave to plot pattern.")
            pattern = field.pattern
            entries.append((
                (pattern.space_0, pattern.space_1, pattern.move_head_0_2tail, pattern.move_tail_1_2head),
                pattern.activeList,
                field.angle
            ))

        entries.sort(key=lambda x: (
            -(x[0][0] + x[0][1]),
            -max(x[0][0], x[0][1]),
            -x[0][0],
            -x[0][2],
            x[0][3]
        ))

        # Extract data
        hex_list = [hex_str for _, hex_str, _ in entries]
        angle_list = [angle for _, _, angle in entries]

        # Use hex_to_binary_profile instead of hex_string_to_binary_column
        bit_columns = [hex_to_binary_profile(h, n_piezos=len(h)*4).reshape(-1, 1) for h in hex_list]
        image = np.hstack(bit_columns)

        height, width = image.shape

        # Create figure with compact size
        fig, ax = plt.subplots(figsize=figsize)
        plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.2)

        # Plot binary pattern
        im = ax.imshow(image, cmap='binary', aspect='auto', interpolation='none', vmin=0, vmax=1)

        ax.set_title("Scan Configuration", fontsize=12, pad=10, weight='bold')
        ax.set_xlabel("Wave Index", fontsize=10, labelpad=8)
        ax.set_ylabel("Transducer Activation", fontsize=10, labelpad=8)
        yticks_positions = np.arange(0, height)
        yticks_labels = np.arange(1, height + 1)

        ax.set_yticks(yticks_positions)
        ax.set_yticklabels(yticks_labels, fontsize=8)

        # Plot angle markers
        angle_min, angle_max = -20.2, 20.2
        center = height / 2
        scale = height / (angle_max - angle_min)
        for i, angle in enumerate(angle_list):
            y = round(center - angle * scale)
            if 0 <= y < height:
                ax.plot(i, y - 0.5, 'ro', markersize=4, alpha=0.7)

        ax.set_ylim(height - 0.5, -0.5)

        # Twin axis for angles
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        yticks_angle = np.linspace(20, -20, 5)
        yticks_pos = np.interp(yticks_angle, [angle_min, angle_max], [height - 0.5, -0.5])
        ax2.set_yticks(yticks_pos)
        ax2.set_yticklabels([f"{a:.1f}°" for a in yticks_angle], fontsize=9, color='r')
        ax2.set_ylabel("Angle [°]", fontsize=11, color='r', labelpad=10)
        ax2.tick_params(axis='y', colors='r', labelsize=9, width=1.5, length=5)

        # Make axes thicker
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        ax2.spines['right'].set_linewidth(1.5)

        # Add grid
        ax.grid(True, linestyle='--', alpha=0.4, color='gray', linewidth=0.5)
        ax.set_xticks(np.linspace(0, width-1, 6))
        ax.set_yticks(np.linspace(0, height-1, 6))
        ax.tick_params(axis='both', which='both', labelsize=8, width=1.5, length=4)

        plt.tight_layout()
        plt.show()

    def plot_angle_frequency_distribution(self, figsize=(12, 5)):
        """
        Plot the distribution of angles and spatial frequencies in the patterns.
        """
        if self.patterns is None:
            raise ValueError("[AOT-biomaps] patterns is not initialized. Please load or generate the active list first.")

        num_elements = self.params.acoustic['probe']['num_elements']
        # Find all even divisors of num_elements (including num_elements itself)
        divs = sorted([d for d in range(2, num_elements + 1) if num_elements % d == 0 and d % 2 == 0])
        if num_elements not in divs:
            divs.append(num_elements)
        divs.sort()

        angles = []
        freqs = []

        for p in self.patterns:
            # Extract "hexa_XXX" from the dictionary
            file_name = p["fileName"]
            hex_part, angle_str = file_name.split('_')

            # Get the angle
            sign = -1 if angle_str[0] == '1' else 1
            angle = sign * int(angle_str[1:])
            angles.append(angle)

            # Get the spatial frequency
            bits = np.array([int(b) for b in bin(int(hex_part, 16))[2:].zfill(num_elements)])
            if np.all(bits == 1):  # All elements active case
                freqs.append(num_elements)
                continue

            for block_size in divs:
                half_block = block_size // 2
                block = np.array([0] * half_block + [1] * half_block)
                reps = num_elements // block_size
                pattern_check = np.tile(block, reps)
                if any(np.array_equal(np.roll(pattern_check, shift), bits) for shift in range(block_size)):
                    freqs.append(block_size)
                    break
            else:
                freqs.append(None)

        freqs = [f for f in freqs if f is not None]

        # Plot
        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Angle histogram
        axes[0].hist(angles, bins=np.arange(-20.5, 21.5, 1), color='skyblue', edgecolor='black', rwidth=0.8)
        axes[0].set_xlabel("Angle (°)")
        axes[0].set_ylabel("Number of patterns")
        axes[0].set_title("Angle Distribution")
        axes[0].set_xticks(np.arange(-20, 21, 2))

        # Spatial frequency histogram
        unique_freqs, freq_counts = np.unique(freqs, return_counts=True)
        x_pos = np.arange(len(divs))
        for freq, count in zip(unique_freqs, freq_counts):
            idx = divs.index(freq)
            axes[1].bar(x_pos[idx], count, color='salmon', edgecolor='black', width=0.8)

        axes[1].set_xticks(x_pos)
        axes[1].set_xticklabels(divs)
        axes[1].set_xlabel("Block size (spatial frequency)")
        axes[1].set_ylabel("Number of patterns")
        axes[1].set_title("Spatial Frequency Distribution")

        plt.tight_layout()
        plt.show()

    def load_activeList(self, fieldParamPath):
        """Load filename-based or parameterized structured-wave patterns."""
        if not os.path.isfile(fieldParamPath):
            raise FileNotFoundError(f"Field parameter file not found: {fieldParamPath}")
    
        self.theta = []
        self.decimations = []
        self.ActiveList = []
        self.DelayLaw = []
        patterns = []
        n_elements = int(self.params.acoustic["probe"]["num_elements"])
        element_width = float(self.params.acoustic["probe"]["element_width"])
        sound_speed = float(self.params.acoustic["medium"]["c0"])
        element_index = np.arange(1, n_elements + 1, dtype=np.float64)
    
        with open(fieldParamPath, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                if "_" in line and all(c in "0123456789abcdefABCDEF" for c in line.split("_")[0]):
                    angle = get_angle(line)
                    profile = hex_to_binary_profile(line.split("_")[0], n_elements)
                    patterns.append({"fileName": line})
                    self.theta.append(angle)
                    self.ActiveList.append(profile)
                    delays = (
                        1000.0 / sound_speed * np.sin(np.deg2rad(angle))
                        * element_index * element_width
                    )
                    self.DelayLaw.append(delays - delays.min())
                    self.decimations.append(get_frequency(line, n_elements, element_width))
                    continue
    
                try:
                    parsed = ast.literal_eval(line)
                    if not (isinstance(parsed, tuple) and len(parsed) == 2):
                        raise ValueError("Expected a tuple: (four pattern coordinates, angle list).")
                    coordinates, angles = parsed
                    if len(coordinates) != 4:
                        raise ValueError("A parameterized pattern must contain four coordinates.")
                    for angle in angles:
                        angle = float(angle)
                        patterns.append({
                            "space_0": coordinates[0],
                            "space_1": coordinates[1],
                            "move_head_0_2tail": coordinates[2],
                            "move_tail_1_2head": coordinates[3],
                            "angle": angle,
                        })
                        self.theta.append(angle)
                        self.ActiveList.append(None)
                        self.DelayLaw.append(None)
                        self.decimations.append(None)
                except (ValueError, SyntaxError, TypeError) as exc:
                    raise ValueError(
                        f"Invalid pattern specification on line {line_number}: {line!r}. {exc}"
                    ) from exc
    
        self.patterns = patterns
        return patterns

    def save_activeList(self, filePath):
        """
        Save the list of patterns to a text file.

        Parameters:
            filePath (str): Path to the output file.
        """
        with open(filePath, 'w') as file:
            for pattern in self.patterns:
                if "fileName" in pattern:
                    # Case 1: Simple pattern (format "hexa_XXX")
                    file.write(f"{pattern['fileName']}\n")
                else:
                    # Case 2: Pattern with parameters (tuple format)
                    coords = (
                        pattern["space_0"],
                        pattern["space_1"],
                        pattern["move_head_0_2tail"],
                        pattern["move_tail_1_2head"]
                    )
                    angles = [pattern["angle"]]
                    line = f"({coords}, {angles})\n"
                    file.write(line)

    def generate_activeList(self, N=None, decimations=None, angles=None):
        """
        Generate a list of balanced and regular activation patterns.

        Parameters:
            N (int): Number of patterns to generate.
            decimations (list): List of decimation factors.
            angles (list): List of angles to use.

        Raises:
            ValueError: If N < 2 and decimations/angles are not provided.
        """
        if decimations is not None and angles is not None:
            self.patterns = self._generate_patterns_from_decimations(decimations, angles)
        elif N is not None and N > 1:
            self.patterns = self._generate_patterns(N)
            if not self._check_patterns(self.patterns):
                raise ValueError("[AOT-biomaps] Generated patterns failed validation.")
        else:
            raise ValueError("[AOT-biomaps] Either N (>=2) or both decimations and angles must be provided for pattern generation.")

    def generate_activeList_from_exp(self):
        """Build structured-wave metadata from the loaded experimental parameters."""
        if self.expParams is None:
            raise ValueError("expParams is not initialized. Load experiment data first.")
        active_hex = convert_to_hex_list(self.expParams["ActiveListMatrix"])
        angles = np.asarray(self.expParams["AngleMatrix"]).reshape(-1)
        if len(active_hex) != len(angles):
            raise ValueError(
                f"Active-list count ({len(active_hex)}) does not match angle count ({len(angles)})."
            )
    
        n_elements = int(self.params.acoustic["probe"]["num_elements"])
        element_width = float(self.params.acoustic["probe"]["element_width"])
        sound_speed = float(self.params.acoustic["medium"]["c0"])
        element_index = np.arange(1, n_elements + 1, dtype=np.float64)
    
        self.patterns = []
        self.theta = []
        self.ActiveList = []
        self.DelayLaw = []
        self.decimations = []
        for pattern_hex, angle in zip(active_hex, angles):
            angle = float(angle)
            file_name = f"{pattern_hex}_{format_angle(angle)}"
            self.patterns.append({"fileName": file_name})
            self.theta.append(angle)
            self.ActiveList.append(hex_to_binary_profile(pattern_hex, n_elements))
            delays = (
                1000.0 / sound_speed * np.sin(np.deg2rad(angle))
                * element_index * element_width
            )
            self.DelayLaw.append(delays - delays.min())
            self.decimations.append(get_frequency(pattern_hex, n_elements, element_width))
        return self.patterns

    def check_ActiveList(self, activeList_path):
        """Compare a filename-based active list with the current patterns."""
        if self.patterns is None:
            raise ValueError("patterns is not initialized.")
        expected = [pattern.get("fileName") for pattern in self.patterns]
        if any(name is None for name in expected):
            raise ValueError("The current pattern list contains parameterized entries without filenames.")
        with open(activeList_path, "r", encoding="utf-8") as file:
            actual = [line.strip() for line in file if line.strip()]
        if len(actual) != len(expected):
            print(
                f"[AOT-biomaps] Active-list length mismatch: file has {len(actual)} entries, "
                f"current pattern list has {len(expected)}."
            )
            return False
        for index, (found, wanted) in enumerate(zip(actual, expected)):
            if found != wanted:
                print(
                    f"[AOT-biomaps] Active-list mismatch at entry {index + 1}: "
                    f"file has {found!r}, expected {wanted!r}."
                )
                return False
        return True

    def save_AOsignals_matlab(self, filePath):
        """
        Save AO signals to a MATLAB .mat file.

        Parameters:
            filePath (str): Path to save the .mat file.
        """
        savemat(filePath, {
            'data': self.AOsignal_withTumor,
            'thetas': self.theta,
            'decimations': self.decimations,
            'ActiveList': self.ActiveList,
            'DelayLaw': self.DelayLaw
        })

    def select_angles(self, angles):
        """
        Select acoustic fields and patterns based on specified angles.
        Works even if AcousticFields or AO signals are None.
        """
        if self.patterns is None:
            raise ValueError("[AOT-biomaps] patterns is not initialized.")

        index = []
        for i, p in enumerate(self.patterns):
            angle = get_angle(p["fileName"]) if "fileName" in p else p.get("angle")
            if angle in angles:
                index.append(i)

        self._apply_selection_indices(index)

    def select_shifts(self, shifts):
        """Select filename-based patterns by their quadrature phase."""
        if self.patterns is None:
            raise ValueError("patterns is not initialized.")
    
        phase_map = {
            "0": 0.0,
            "0.0": 0.0,
            "90": np.pi / 2,
            "180": np.pi,
            "270": 3 * np.pi / 2,
            "pi/2": np.pi / 2,
            "pi": np.pi,
            "3pi/2": 3 * np.pi / 2,
            "0rad": 0.0,
        }
        target_phases = []
        for shift in shifts:
            if isinstance(shift, str):
                token = shift.strip().lower().replace(" ", "")
                if token in phase_map:
                    target_phases.append(phase_map[token])
                else:
                    target_phases.append(float(token))
            else:
                target_phases.append(float(shift))
        target_phases = np.asarray(target_phases, dtype=np.float64)
    
        n_elements = int(self.params.acoustic["probe"]["num_elements"])
        indices = []
        for index, pattern in enumerate(self.patterns):
            if "fileName" not in pattern:
                continue
            profile = hex_to_binary_profile(pattern["fileName"].split("_")[0], n_elements)
            phase = get_phase_deterministic(profile)
            if np.any(np.isclose(phase, target_phases, rtol=0.0, atol=1e-8)):
                indices.append(index)
        self._apply_selection_indices(indices)
        return indices

    def select_decimations(self, decimations):
        """
        Select patterns based on decimation factors (spatial frequencies).
        """
        if self.patterns is None:
            raise ValueError("[AOT-biomaps] patterns is not initialized.")

        n_piezos = self.params.acoustic['probe']['num_elements']
        width = self.params.acoustic['probe']['element_width']
        
        index = []
        for i, p in enumerate(self.patterns):
            if "fileName" in p:
                f_s = get_frequency(p["fileName"], n_piezos, width)
                if f_s in decimations:
                    index.append(i)

        self._apply_selection_indices(index)

    def select_patterns(self, pattern_names):
        """
        Select patterns based on a specified list of file names or identifiers.
        """
        if self.patterns is None:
            raise ValueError("[AOT-biomaps] patterns is not initialized.")

        index = []
        for i, p in enumerate(self.patterns):
            fname = p.get("fileName")
            if fname in pattern_names:
                index.append(i)

        self._apply_selection_indices(index)

    def select_random(self, N):
        """
        Randomly select N patterns and associated data.
        """
        if self.patterns is None:
            raise ValueError("[AOT-biomaps] patterns is not initialized.")
        if N > len(self.patterns):
            raise ValueError("[AOT-biomaps] N is larger than the number of available patterns.")

        indices = np.random.choice(len(self.patterns), size=N, replace=False)
        indices = sorted(indices.tolist())
        self._apply_selection_indices(indices)

    def _apply_selection_indices(self, index):
        """
        Internal method to filter all class attributes according to a list of indices.
        Gracefully handles potentially None attributes.
        """
        # 1. Filter base pattern attributes
        self.patterns = [self.patterns[i] for i in index]
        self.theta = [self.theta[i] for i in index] if self.theta else []
        self.decimations = [self.decimations[i] for i in index] if self.decimations else []
        self.ActiveList = [self.ActiveList[i] for i in index] if self.ActiveList else []
        self.DelayLaw = [self.DelayLaw[i] for i in index] if self.DelayLaw else []

        # 2. Filter AcousticFields if initialized
        if self.AcousticFields is not None:
            if len(self.AcousticFields) >= max(index, default=-1) + 1:
                self.AcousticFields = [self.AcousticFields[i] for i in index]
            else:
                self.AcousticFields = None
                print("[AOT-biomaps] Warning: AcousticFields has been reset because indices no longer match.")

        # 3. Filter AO signals if initialized
        if self.AOsignal_withTumor is not None:
            self.AOsignal_withTumor = self.AOsignal_withTumor[:, index]
        if self.AOsignal_withoutTumor is not None:
            self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:, index]
            
    def _generate_patterns_from_decimations(self, decimations, angles):
        """
        Generate patterns from specified decimations and angles.

        Parameters:
            decimations (array): Array of decimation factors.
            angles (array): Array of angles in degrees.

        Returns:
            list: List of pattern dictionaries.
        """
        if isinstance(decimations, list):
            decimations = np.array(decimations)
        if isinstance(angles, list):
            angles = np.array(angles)

        angles = np.sort(angles)
        decimations = np.sort(decimations)
        self.DelayLaw = []
        self.theta = []
        self.decimations = []
        self.ActiveList = []
        self.patterns = []

        num_elements = self.params.acoustic['probe']['num_elements']
        Width = self.params.acoustic['probe']['element_width']
        kerf = self.params.acoustic['probe'].get('kerf', 0.00000)
        Nactuators = num_elements

        # ---
        has_zero = 0 in decimations
        if has_zero:
            Nscans = 4 * len(angles) * (len(decimations) - 1) + len(angles)
        else:
            Nscans = 4 * len(angles) * len(decimations)

        ActiveLIST = np.ones((num_elements, Nscans))

        # ---
        Xc = (Width + (Nactuators - 1) * (kerf + Width)) / 2
        Xm = np.array([Width * (i - 1) + Width / 2 - Xc for i in range(1, Nactuators + 1)])

        # ---
        # If there's a 0, modulated patterns start after the plane wave
        # Otherwise, they start at index 0
        current_offset = len(angles) if has_zero else 0

        if has_zero:
            I_plane = np.arange(len(angles))
            ActiveLIST[:, I_plane] = 1

        # ---
        active_decimations = decimations[decimations != 0]
        dFx = 1 / (Nactuators * Width)

        for i_dec in range(len(active_decimations)):
            # Calculate indices relative to start offset
            I = np.arange(len(angles)) + current_offset + (i_dec * 4 * len(angles))

            Icos = I
            Incos = I + 1 * len(angles)
            Insin = I + 2 * len(angles)  # Insin before Isin to match storage order
            Isin = I + 3 * len(angles)

            fx = dFx * active_decimations[i_dec]

            # Apply modulated patterns
            ActiveLIST[:, Icos] = calc_mat_os(Xm, fx, ActiveLIST[:, Icos[:1]], 'cos')
            ActiveLIST[:, Incos] = 1 - ActiveLIST[:, Icos]
            ActiveLIST[:, Isin] = calc_mat_os(Xm, fx, ActiveLIST[:, Isin[:1]], 'sin')
            ActiveLIST[:, Insin] = 1 - ActiveLIST[:, Isin]

        # ---
        hexa_list = convert_to_hex_list(ActiveLIST)

        patterns = []
        print(f"[AOT-biomaps] Generating {Nscans} patterns...")
        for i in range(Nscans):
            angle_val = angles[i % len(angles)]
            hex_pattern = hexa_list[i]
            fileName = f"{hex_pattern}_{format_angle(angle_val)}"
            patterns.append({"fileName": fileName})
            self.theta.append(get_angle(fileName))
            profile = hex_to_binary_profile(fileName.split('_')[0], self.params.acoustic['probe']['num_elements'])
            self.ActiveList.append(profile)
            new_Delay = 1000 * (1/self.params.acoustic['medium']['c0']) * np.sin(np.deg2rad(self.theta[-1])) * np.arange(1, self.params.acoustic['probe']['num_elements'] + 1) * self.params.acoustic['probe']['element_width']
            self.DelayLaw.append(new_Delay - np.min(new_Delay))
            self.decimations.append(get_frequency(fileName, self.params.acoustic['probe']['num_elements'], self.params.acoustic['probe']['element_width']))

        return patterns

    def _generate_patterns(self, N, angles=None):
        """
        Generate N random balanced patterns with random angles.

        Parameters:
            N (int): Number of patterns to generate.
            angles (list): Optional list of angles to use. If None, uses range(-20, 21).

        Returns:
            list: List of pattern dictionaries.
        """
        self.DelayLaw = []
        self.theta = []
        self.decimations = []
        self.ActiveList = []
        self.patterns = []

        num_elements = self.params.acoustic['probe']['num_elements']
        if angles is None:
            angle_choices = list(range(-20, 21))
        else:
            if isinstance(angles, np.ndarray):
                angles = angles.tolist()
            angle_choices = angles

        # 1. Find ALL even divisors of num_elements (including num_elements itself)
        divs = [d for d in range(2, num_elements + 1) if num_elements % d == 0 and d % 2 == 0]
        if not divs:
            print(f"[AOT-biomaps] No even divisors found for num_elements = {num_elements}")
            return []

        # Preserve draw order while using a set for constant-time duplicate checks.
        unique_patterns = set()
        ordered_patterns = []

        # Generate until N unique patterns are found.
        while len(ordered_patterns) < N:
            # Randomly select a divisor (including num_elements)
            block_size = np.random.choice(divs)

            if block_size == num_elements:
                # Special case: "all active" pattern
                pattern_bits = np.ones(num_elements, dtype=int)
            else:
                # General case: balanced pattern
                half_block = block_size // 2
                block = np.array([0] * half_block + [1] * half_block)
                reps = num_elements // block_size
                base_pattern = np.tile(block, reps)
                # Randomly select a shift
                shift = np.random.randint(0, block_size)
                pattern_bits = np.roll(base_pattern, shift)

            # Convert to hex and choose a random angle
            hex_pattern = binary_to_hex_profile(pattern_bits)
            angle = np.random.choice(angle_choices)
            pair = f"{hex_pattern}_{format_angle(angle)}"

            if pair not in unique_patterns:
                unique_patterns.add(pair)
                ordered_patterns.append(pair)

        # Convert to a stable list of filename-based pattern dictionaries.
        patterns = [{"fileName": pair} for pair in ordered_patterns]
        for i in range(N):
            self.theta.append(get_angle(patterns[i]["fileName"]))
            profile = hex_to_binary_profile(patterns[i]["fileName"].split('_')[0], self.params.acoustic['probe']['num_elements'])
            self.ActiveList.append(profile)
            new_Delay = 1000 * (1/self.params.acoustic['medium']['c0']) * np.sin(np.deg2rad(self.theta[-1])) * np.arange(1, self.params.acoustic['probe']['num_elements'] + 1) * self.params.acoustic['probe']['element_width']
            self.DelayLaw.append(new_Delay - np.min(new_Delay))
            self.decimations.append(get_frequency(patterns[i]["fileName"], self.params.acoustic['probe']['num_elements'], self.params.acoustic['probe']['element_width']))

        # 5. Return exactly N patterns
        return patterns[:N]

    def _check_patterns(self, patterns):
        """
        Check if the patterns are valid (no duplicates, correct length, balanced, regular).

        Parameters:
            patterns (list): List of pattern dictionaries to check.

        Returns:
            bool: True if all patterns are valid, False otherwise.
        """
        # 1. Check for duplicates (based on "fileName")
        file_names = [p["fileName"] for p in patterns]
        if len(file_names) != len(set(file_names)):
            from collections import Counter
            file_counts = Counter(file_names)
            duplicates = [fn for fn, count in file_counts.items() if count > 1]
            for dup in duplicates:
                print(f"[AOT-biomaps] Error: Duplicate detected for {dup}")
            return False

        # 2. Check each pattern individually
        num_elements = self.params.acoustic['probe']['num_elements']
        for pattern in patterns:
            hex_part, angle_str = pattern["fileName"].split('_')
            bits = np.array([int(b) for b in bin(int(hex_part, 16))[2:].zfill(num_elements)])

            # Check length
            if len(bits) != num_elements:
                print(f"[AOT-biomaps] Error length: {pattern['fileName']}")
                return False

            # Special case: "all active" pattern
            if np.all(bits == 1):
                continue

            # Check 0/1 balance
            if np.sum(bits) != num_elements // 2:
                print(f"[AOT-biomaps] Error 0/1 balance: {pattern['fileName']}")
                return False

            # Check regularity
            valid = False
            divs = [d for d in range(2, num_elements + 1) if num_elements % d == 0 and d % 2 == 0]
            for block_size in divs:
                half_block = block_size // 2
                block = np.array([0] * half_block + [1] * half_block)
                reps = num_elements // block_size
                expected_pattern = np.tile(block, reps)
                if any(np.array_equal(np.roll(expected_pattern, shift), bits) for shift in range(block_size)):
                    valid = True
                    break
            if not valid:
                print(f"[AOT-biomaps] Error regularity: {pattern['fileName']}")
                return False

        return True

    def apply_apodisation(self, alpha=0.3, divergence_deg=0.5):
        """Apply an angle-aligned Tukey aperture mask to each acoustic field.
    
        The mask is built from broadcast 1-D coordinates (no full meshgrid) and
        stored as float32. Writable fields are multiplied in place, avoiding a
        second full 3-D field allocation. Read-only memmaps are replaced by one
        output allocation because their backing file is not writable.
        """
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is empty.")
        if not (0.0 <= float(alpha) <= 1.0):
            raise ValueError("alpha must be in [0, 1].")
        if float(divergence_deg) < 0.0:
            raise ValueError("divergence_deg must be non-negative.")
    
        probe = self.params.acoustic["probe"]
        probe_width = float(probe["num_elements"]) * float(probe["element_width"])
    
        for acoustic_field in trange(len(self.AcousticFields), desc="[AOT-biomaps] Apodizing acoustic fields"):
            field_object = self.AcousticFields[acoustic_field]
            field = field_object.field
            if field is None or field.ndim not in (2, 3):
                raise ValueError("Apodization expects a loaded 2-D image or a (time, z, x) field.")
            nz, nx = map(int, field.shape[-2:])
            if getattr(self, "x_axis", None) is not None:
                x_axis = np.asarray(self.x_axis, dtype=np.float32)
            else:
                # Preserve the original default: the probe aperture is centered at x=0.
                x_axis = np.linspace(-probe_width / 2.0, probe_width / 2.0, nx, dtype=np.float32)
            if getattr(self, "z_axis", None) is not None:
                z_axis = np.asarray(self.z_axis, dtype=np.float32)
            else:
                # Preserve the historical default depth interval when no explicit axis is supplied.
                z_axis = np.linspace(0.0, 40e-3, nz, dtype=np.float32)
            if x_axis.ndim != 1 or z_axis.ndim != 1 or x_axis.size != nx or z_axis.size != nz:
                raise ValueError("The configured x_axis/z_axis must be 1-D and match the field grid.")
    
            angle_tan = np.float32(np.tan(np.deg2rad(float(field_object.angle))))
            divergence_tan = np.float32(np.tan(np.deg2rad(float(divergence_deg))))
            half_width = np.float32(probe_width / 2.0) + z_axis[:, None] * divergence_tan
    
            normalized = np.zeros((nz, nx), dtype=np.float32)
            np.subtract(x_axis[None, :], z_axis[:, None] * angle_tan, out=normalized)
            np.divide(normalized, half_width, out=normalized, where=half_width != 0)
            zero_width_rows = half_width[:, 0] == 0
            if np.any(zero_width_rows):
                normalized[zero_width_rows, :] = 0.0
            np.abs(normalized, out=normalized)
    
            mask = np.zeros((nz, nx), dtype=np.float32)
            plateau = normalized <= (1.0 - float(alpha))
            mask[plateau] = 1.0
            transition = (normalized > (1.0 - float(alpha))) & (normalized <= 1.0)
            if alpha > 0.0 and np.any(transition):
                position = (normalized[transition] - (1.0 - float(alpha))) / float(alpha)
                mask[transition] = 0.5 * (1.0 + np.cos(np.pi * position))
    
            if CUPY_AVAILABLE and isinstance(field, cp.ndarray):
                with cp.cuda.Device(int(field.device.id)):
                    mask_device = cp.asarray(mask)
                    broadcast_mask = mask_device[None, :, :] if field.ndim == 3 else mask_device
                    if bool(getattr(field.flags, "writeable", True)):
                        cp.multiply(field, broadcast_mask, out=field)
                    else:
                        field_object.field = cp.multiply(field, broadcast_mask)
                    del mask_device, broadcast_mask
            else:
                broadcast_mask = mask[None, :, :] if field.ndim == 3 else mask
                if field.flags.writeable:
                    np.multiply(field, broadcast_mask, out=field, casting="unsafe")
                else:
                    field_object.field = np.multiply(field, broadcast_mask, dtype=np.float32)
            del normalized, mask, half_width
    
        print("[AOT-biomaps] Apodization complete.")
        return self.AcousticFields

    # PRIVATE METHODS
    def _generate_acousticFields_STRUCT(
        self, fieldDataPath=None, isGPU=None, GPUdevice=None, tempFieldName="Kwave",
        nameBlock=None, generation_type="envelope_squared", show_log=False,
        max_workers=None, backend=None, materialize=False, vram_fraction=0.95,
        accumulate_max_bytes=None, host_staging_fraction=1.0 / 16.0,
    ):
        """Load existing structured fields and generate only missing fields.
    
        Loading and generation are deliberately separate. Existing HDR/IMG
        files are opened lazily as memmaps unless ``materialize=True`` and the
        estimated complete collection fits the host-memory budget. Simulation
        is bounded to one active worker per GPU. Each generated field is
        returned to host memory, saved, and then reopened lazily when
        materialization is disabled; this prevents the system matrix from
        accumulating in VRAM during a multi-pattern run.
        """
        if self.patterns is None:
            raise ValueError("patterns is not initialized. Load or generate the active list first.")
        if not self.patterns:
            return []
        if backend is None:
            backend = "python"
        if backend not in ("python", "cpp"):
            raise ValueError("backend must be 'python' or 'cpp'.")
        if isGPU is None:
            isGPU = config.get_process() == "gpu"
    
        # Resolve the worker-device list. The worker count is never allowed to
        # exceed the number of distinct selected GPUs.
        if isGPU and not CUPY_AVAILABLE:
            print("[AOT-biomaps] CuPy is unavailable; acoustic generation will run on CPU.")
            isGPU = False
    
        if isGPU:
            if isinstance(GPUdevice, (list, tuple, np.ndarray)):
                gpu_devices = list(dict.fromkeys(int(device) for device in GPUdevice))
                if not gpu_devices:
                    raise ValueError("GPUdevice must contain at least one device index.")
            elif GPUdevice is not None:
                gpu_devices = [int(GPUdevice)]
            else:
                gpu_devices = [int(config.select_best_gpu())]
        else:
            gpu_devices = [None]
    
        if max_workers is None:
            max_workers = len(gpu_devices) if isGPU else min(4, os.cpu_count() or 1)
        max_workers = int(max_workers)
        if max_workers < 1:
            raise ValueError("max_workers must be a positive integer.")
        if isGPU and max_workers > len(gpu_devices):
            print(
                f"[AOT-biomaps] Capping max_workers={max_workers} to {len(gpu_devices)} "
                "to keep at most one simulation per GPU."
            )
            max_workers = len(gpu_devices)
        active_devices = gpu_devices[:max_workers] if isGPU else [None]
    
        # Instantiate all field descriptors once and preserve the requested order.
        fields = [None] * len(self.patterns)
        to_load = []
        to_generate = []
        for index, pattern in enumerate(self.patterns):
            if "fileName" in pattern:
                field_object = StructuredWave(
                    fileName=pattern["fileName"], params=self.params, medium=self.medium
                )
            else:
                field_object = StructuredWave(
                    angle_deg=pattern["angle"],
                    space_0=pattern["space_0"],
                    space_1=pattern["space_1"],
                    move_head_0_2tail=pattern["move_head_0_2tail"],
                    move_tail_1_2head=pattern["move_tail_1_2head"],
                    params=self.params,
                    medium=self.medium,
                )
    
            path_field = None
            if fieldDataPath is not None:
                path_field = os.path.join(
                    fieldDataPath, field_object.get_name_field() + self.FormatSave.value
                )
            can_load = (
                path_field is not None
                and self.params.acoustic["typeSim"] != TypeSim.SIMPLE_SIM.value
                and os.path.isfile(path_field)
                and os.path.getsize(path_field) > 0
            )
            task = (index, field_object, path_field)
            (to_load if can_load else to_generate).append(task)
    
        print(
            f"[AOT-biomaps] Field plan: {len(to_load)} to load, "
            f"{len(to_generate)} to generate; {max_workers} simulation worker(s)."
        )
    
        available_ram = get_available_host_memory_bytes()
        if available_ram is None:
            available_ram = 0
        materialize_enabled = [bool(materialize and fieldDataPath is not None)]
        materialization_checked = [False]
        materialization_lock = threading.Lock()
        estimated_bytes_per_field = [None]
    
        def check_materialization_budget(field_array):
            """Make one conservative estimate for the complete field set."""
            if not materialize_enabled[0]:
                return False
            if materialization_checked[0]:
                return materialize_enabled[0]
            with materialization_lock:
                if not materialization_checked[0]:
                    estimated_bytes_per_field[0] = int(field_array.nbytes)
                    estimated_total = estimated_bytes_per_field[0] * len(fields)
                    budget = int(0.8 * available_ram) if available_ram else 0
                    materialization_checked[0] = True
                    if budget <= 0 or estimated_total > budget:
                        print(
                            "[AOT-biomaps] Materialization disabled: estimated resident field set "
                            f"is {estimated_total / 2**30:.2f} GiB, while the safe available-RAM "
                            f"budget is {budget / 2**30:.2f} GiB. Fields will remain file-backed."
                        )
                        materialize_enabled[0] = False
                        return False
                    print(
                        "[AOT-biomaps] Materializing acoustic fields: estimated "
                        f"{estimated_total / 2**30:.2f} GiB across {len(fields)} fields."
                    )
            return materialize_enabled[0]
    
        def load_one(task):
            index, field_object, path_field = task
            try:
                field_object.load_field(fieldDataPath, self.FormatSave, nameBlock)
                field_array = field_object.field
                if field_array is None:
                    raise RuntimeError("The field loader returned no array.")
                if materialize_enabled[0] and _is_memmap_backed(field_array):
                    if check_materialization_budget(field_array):
                        field_object.field = np.array(
                            field_array, dtype=field_array.dtype, order="C", copy=True
                        )
                return index, field_object, None
            except Exception as exc:
                return index, field_object, exc
    
        if to_load:
            # Serial materialization avoids several full-field RAM copies being
            # live simultaneously. Lazy memmap opens are cheap and can be parallel.
            load_workers = 1 if materialize_enabled[0] else min(8, len(to_load), os.cpu_count() or 1)
            with concurrent.futures.ThreadPoolExecutor(max_workers=load_workers) as executor:
                futures = [executor.submit(load_one, task) for task in to_load]
                for future in tqdm(
                    concurrent.futures.as_completed(futures),
                    total=len(futures),
                    desc="[AOT-biomaps] Loading fields",
                ):
                    index, field_object, error = future.result()
                    if error is None:
                        fields[index] = field_object
                    else:
                        print(
                            f"[AOT-biomaps] Could not load {field_object.get_name_field()}; "
                            f"regenerating it ({error})."
                        )
                        path_field = os.path.join(
                            fieldDataPath, field_object.get_name_field() + self.FormatSave.value
                        )
                        to_generate.append((index, field_object, path_field))
    
        def generate_one(task, device):
            index, field_object, path_field = task
            safe_temp_name = f"{tempFieldName}_{field_object.get_name_field()}"
            field_object.generate_field(
                isGPU=isGPU,
                GPUdevice=device,
                tempFieldName=safe_temp_name,
                generation_type=generation_type,
                show_log=show_log,
                backend=backend,
                keep_on_gpu=False,
                vram_fraction=vram_fraction,
                accumulate_max_bytes=accumulate_max_bytes,
                host_staging_fraction=host_staging_fraction,
            )
    
            if field_object.field is None:
                raise RuntimeError(f"Generation returned no field for {field_object.get_name_field()}.")
    
            if path_field is not None and self.params.acoustic["typeSim"] != TypeSim.SIMPLE_SIM.value:
                os.makedirs(fieldDataPath, exist_ok=True)
                # This task was classified as missing, invalid, or unreadable;
                # always overwrite the associated file set after regeneration.
                field_object.save_field(fieldDataPath, formatSave=self.FormatSave)
    
                if materialize_enabled[0]:
                    check_materialization_budget(field_object.field)
    
                if not materialize_enabled[0]:
                    field_object.field = None
                    field_object.load_field(fieldDataPath, self.FormatSave, nameBlock)
    
            fields[index] = field_object
            return index
    
        if to_generate:
            progress = tqdm(
                total=len(to_generate),
                desc=f"[AOT-biomaps] Generating fields ({backend})",
            )
            try:
                if isGPU:
                    # One long-lived worker per GPU processes its assigned queue
                    # sequentially. This is stronger than a thread-pool cap: a
                    # fast worker can never start a second simulation on a GPU
                    # while another worker is still using that same device.
                    tasks_by_device = {device: [] for device in active_devices}
                    for task_index, task in enumerate(to_generate):
                        device = active_devices[task_index % len(active_devices)]
                        tasks_by_device[device].append(task)
    
                    def device_worker(device, tasks):
                        for task in tasks:
                            generate_one(task, device)
                            progress.update(1)
    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=len(active_devices)) as executor:
                        futures = [
                            executor.submit(device_worker, device, tasks)
                            for device, tasks in tasks_by_device.items() if tasks
                        ]
                        for future in concurrent.futures.as_completed(futures):
                            future.result()
                else:
                    worker_count = min(max_workers, len(to_generate))
                    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
                        futures = [executor.submit(generate_one, task, None) for task in to_generate]
                        for future in concurrent.futures.as_completed(futures):
                            future.result()
                            progress.update(1)
            finally:
                progress.close()
    
        if any(field is None for field in fields):
            missing = [index for index, field in enumerate(fields) if field is None]
            raise RuntimeError(f"Acoustic-field generation did not complete for indices: {missing[:10]}.")
        return fields

    def stream_acoustic_fields(
        self, isGPU=True, GPUdevice=0, tempFieldName="Kwave",
        generation_type="envelope_squared", show_log=False, backend="python",
        start_index=0, vram_fraction=0.95, accumulate_max_bytes=None,
        host_staging_fraction=1.0 / 16.0, validate_iq=False,
    ):
        """Yield generated fields one at a time without retaining a field list.
    
        This is the lowest-host-memory route for operators that consume each
        field immediately. The yielded array remains owned by the caller; the
        temporary ``StructuredWave`` object releases its other references when
        iteration advances.
        """
        if self.patterns is None:
            raise ValueError("patterns is not initialized. Load the active list first.")
        start_index = int(start_index)
        if start_index < 0 or start_index > len(self.patterns):
            raise ValueError("start_index is outside the pattern list.")
        if isinstance(GPUdevice, (list, tuple, np.ndarray)):
            devices = [int(value) for value in GPUdevice]
            if not devices:
                raise ValueError("GPUdevice cannot be an empty sequence.")
            device = devices[0]
        elif GPUdevice is not None:
            device = int(GPUdevice)
        else:
            device = int(config.select_best_gpu()) if isGPU else None
    
        iterator = tqdm(
            range(start_index, len(self.patterns)),
            initial=start_index,
            total=len(self.patterns),
            desc=f"[AOT-biomaps] Streaming fields ({backend}, device={device})",
        )
        for index in iterator:
            pattern = self.patterns[index]
            if "fileName" in pattern:
                field_object = StructuredWave(
                    fileName=pattern["fileName"], params=self.params, medium=self.medium
                )
            else:
                field_object = StructuredWave(
                    angle_deg=pattern["angle"],
                    space_0=pattern["space_0"],
                    space_1=pattern["space_1"],
                    move_head_0_2tail=pattern["move_head_0_2tail"],
                    move_tail_1_2head=pattern["move_tail_1_2head"],
                    params=self.params,
                    medium=self.medium,
                )
    
            try:
                field_object.generate_field(
                    isGPU=isGPU,
                    GPUdevice=device,
                    tempFieldName=f"{tempFieldName}_{field_object.get_name_field()}",
                    generation_type=generation_type,
                    show_log=show_log,
                    backend=backend,
                    keep_on_gpu=False,
                    vram_fraction=vram_fraction,
                    accumulate_max_bytes=accumulate_max_bytes,
                    host_staging_fraction=host_staging_fraction,
                    validate_iq=validate_iq,
                )
                yield index, field_object.field
            finally:
                field_object.field = None
                field_object.delayedSignal = None
                field_object.burst = None
                del field_object
                if index and index % 50 == 0:
                    gc.collect()

    def load_experimentalAO(self, pathAO, withTumor=True, h5name='AOsignal'):
        """
        Load experimental AO signals from specified file paths.

        Parameters:
            pathAO (str): Path to the AO signal file.
            withTumor (bool): If True, load as signal with tumor. If False, load as signal without tumor.
            h5name (str): Name of the dataset in HDF5/MAT files. Default is 'AOsignal'.

        Raises:
            FileNotFoundError: If the file does not exist.
            KeyError: If the dataset is not found in the file.
            ValueError: If the file format is not supported.
        """
        if not os.path.exists(pathAO):
            raise FileNotFoundError(f"[AOT-biomaps] File {pathAO} not found.")

        if pathAO.endswith('.npy'):
            AOsignal = np.load(pathAO)
        elif pathAO.endswith('.h5'):
            with h5py.File(pathAO, 'r') as f:
                if h5name not in f:
                    raise KeyError(f"[AOT-biomaps] Dataset '{h5name}' not found in the HDF5 file.")
                AOsignal = f[h5name][:]
        elif pathAO.endswith('.mat'):
            mat_data = loadmat(pathAO)
            if h5name not in mat_data:
                raise KeyError(f"[AOT-biomaps] Dataset '{h5name}' not found in the .mat file.")
            AOsignal = mat_data[h5name]
        elif pathAO.endswith('.hdr'):
            AOsignal = load_AOsignal(pathAO)
        else:
            raise ValueError("[AOT-biomaps] Unsupported file format. Supported formats are: .npy, .h5, .mat, .hdr")

        if withTumor:
            self.AOsignal_withTumor = AOsignal
        else:
            self.AOsignal_withoutTumor = AOsignal

    def check_experimentalAO(self, activeListPath, withTumor=True):
        """Validate experimental AO columns against their active-list ordering."""
        signal = self.AOsignal_withTumor if withTumor else self.AOsignal_withoutTumor
        if signal is None:
            label = "with tumor" if withTumor else "without tumor"
            raise ValueError(f"Experimental AO signal {label} is not initialized.")
    
        if self.AcousticFields is not None and len(self.AcousticFields):
            n_fields = len(self.AcousticFields)
            if signal.shape[1] != n_fields:
                raise ValueError(
                    f"AO signal has {signal.shape[1]} columns but {n_fields} acoustic fields are loaded."
                )
            min_time = min(int(field.field.shape[0]) for field in self.AcousticFields)
            if signal.shape[0] > min_time:
                signal = signal[:min_time]
                if withTumor:
                    self.AOsignal_withTumor = signal
                else:
                    self.AOsignal_withoutTumor = signal
            elif signal.shape[0] < min_time:
                self.cut_acoustic_fields(max_t=signal.shape[0], min_t=0, show_log=False)
    
            if activeListPath is not None:
                with open(activeListPath, "r", encoding="utf-8") as file:
                    expected_names = [line.strip() for line in file if line.strip()]
                if len(expected_names) != n_fields:
                    raise ValueError(
                        f"Active-list file contains {len(expected_names)} entries; expected {n_fields}."
                    )
                for index, field in enumerate(self.AcousticFields):
                    actual = field.get_name_field()
                    if actual.startswith("field_"):
                        actual = actual[len("field_"):]
                    if actual != expected_names[index]:
                        raise ValueError(
                            f"Field {index} is {actual!r}; expected {expected_names[index]!r}."
                        )
        print("[AOT-biomaps] Experimental AO signals are correctly initialized.")
        return True

    def demodulate_AOsignal(self, withTumor=True):
        """Demodulate quadrature AO measurements by spatial frequency and angle.

        Repeated measurements assigned to the same phase retain the historical
        pairwise averaging rule. Missing quadrature phases are treated as zero,
        matching the previous implementation without allocating four separate
        zero-filled signal arrays for every configuration.

        Parameters
        ----------
        withTumor : bool
            Select the AO signal measured with or without the absorber phantom.

        Returns
        -------
        dict
            Mapping ``(spatial_frequency_mm_inverse, angle_rad)`` to complex64
            temporal signals.
        """
        signal = self.AOsignal_withTumor if withTumor else self.AOsignal_withoutTumor
        if signal is None:
            label = "with tumor" if withTumor else "without tumor"
            raise ValueError(f"AO signal {label} is not initialized.")
        if signal.ndim != 2:
            raise ValueError("AO signal must have shape (time, measurements).")
        if len(self.theta) != signal.shape[1] or len(self.ActiveList) != signal.shape[1]:
            raise ValueError("Pattern metadata must contain one angle and activation profile per AO trace.")

        n_elements = int(self.params.acoustic["probe"]["num_elements"])
        delta_x = float(self.params.general["dx"])
        if delta_x <= 0.0:
            raise ValueError("params.general['dx'] must be positive.")
        frequency_axis = np.fft.fftfreq(n_elements, d=delta_x)
        data_by_configuration = {}

        for index in trange(
            signal.shape[1],
            desc="[AOT-biomaps] Demodulating AO signals (four-phase quadrature)",
        ):
            profile = np.asarray(self.ActiveList[index])
            if profile.size != n_elements:
                raise ValueError(f"Activation profile {index} has {profile.size} elements; expected {n_elements}.")
            angle_rad = float(np.round(np.deg2rad(float(self.theta[index])), 6))

            if np.all(profile == 1):
                data_by_configuration[(0.0, angle_rad)] = np.asarray(
                    signal[:, index], dtype=np.complex64
                )
                continue

            cached_bin = (
                self.decimations[index]
                if index < len(self.decimations) else None
            )
            if cached_bin is not None:
                peak_index = int(cached_bin)
                if not (0 <= peak_index <= n_elements // 2):
                    raise ValueError(
                        f"Invalid cached spatial-frequency bin {peak_index} for pattern {index}."
                    )
            else:
                spectrum = np.fft.rfft(profile)
                positive = np.abs(spectrum[1:])
                peak_index = int(np.argmax(positive) + 1) if positive.size and np.any(positive) else 0
            frequency_key = (
                float(np.round(abs(frequency_axis[peak_index]) / 1000.0, 6))
                if peak_index else 0.0
            )
            phase = float(get_phase_deterministic(profile))
            if frequency_key == 0.0:
                data_by_configuration[(0.0, angle_rad)] = np.asarray(
                    signal[:, index], dtype=np.complex64
                )
                continue

            key = (frequency_key, angle_rad)
            phase_map = data_by_configuration.setdefault(key, {})
            current_trace = signal[:, index]
            if phase in phase_map:
                # Preserve the legacy pairwise mean for repeated phase records.
                phase_map[phase] = (phase_map[phase] + current_trace) * 0.5
            else:
                # A view is sufficient until a duplicate phase requires a new mean.
                phase_map[phase] = current_trace

        demodulated = {}
        phase_order = (0.0, np.pi / 2, np.pi, 3 * np.pi / 2)
        n_time = signal.shape[0]
        for key, phase_map in data_by_configuration.items():
            if key[0] == 0.0:
                continue
            real_part = np.zeros(n_time, dtype=np.float32)
            imag_part = np.zeros(n_time, dtype=np.float32)
            s0 = phase_map.get(phase_order[0])
            s90 = phase_map.get(phase_order[1])
            s180 = phase_map.get(phase_order[2])
            s270 = phase_map.get(phase_order[3])
            if s0 is not None:
                np.add(real_part, s0, out=real_part, casting="unsafe")
            if s180 is not None:
                np.subtract(real_part, s180, out=real_part, casting="unsafe")
            if s90 is not None:
                np.add(imag_part, s90, out=imag_part, casting="unsafe")
            if s270 is not None:
                np.subtract(imag_part, s270, out=imag_part, casting="unsafe")

            output = np.empty(n_time, dtype=np.complex64)
            output.real = real_part * np.float32(np.pi / 2.0)
            output.imag = -imag_part * np.float32(np.pi / 2.0)
            demodulated[key] = output

        # Preserve direct plane-wave traces in the output dictionary.
        for key, phase_map in data_by_configuration.items():
            if key[0] == 0.0 and isinstance(phase_map, np.ndarray):
                demodulated[key] = phase_map
        return demodulated

    def demodulate_acoustic_fields(self, max_workers=None):
        """Demodulate stored real fields into complex quadrature fields.
    
        Input fields are expected to be host-resident NumPy arrays or memmaps.
        The routine stores references while grouping phases (no initial field
        copies), then allocates one complex64 output and one float32 scratch
        field per active worker. This avoids the several full-volume temporary
        arrays created by separate real/imaginary expressions.
        """
        if not self.AcousticFields:
            raise ValueError("AcousticFields is empty.")
        n_elements = int(self.params.acoustic["probe"]["num_elements"])
        delta_x = float(self.params.general["dx"])
        frequency_axis = np.fft.fftfreq(n_elements, d=delta_x)
        buffer = {}
    
        for field_object in self.AcousticFields:
            field = field_object.field
            if field is None:
                raise ValueError(f"Field {field_object.get_name_field()} is not loaded.")
            if field.ndim != 3:
                raise ValueError(
                    f"Field {field_object.get_name_field()} has shape {field.shape}; expected (Nt, Nz, Nx)."
                )
            if reference_shape is None:
                reference_shape = tuple(field.shape)
            elif tuple(field.shape) != reference_shape:
                raise ValueError("All acoustic fields must have identical shapes for quadrature demodulation.")
            if CUPY_AVAILABLE and isinstance(field, cp.ndarray):
                raise ValueError(
                    "demodulate_acoustic_fields expects host-resident fields. "
                    "Generate with keep_on_gpu=False to avoid large VRAM intermediates."
                )
            parts = field_object.get_name_field().split("_")
            if len(parts) < 3:
                raise ValueError(f"Unexpected acoustic-field name: {field_object.get_name_field()!r}.")
            hex_pattern = parts[-2]
            angle_code = parts[-1]
            angle_deg = -int(angle_code[1:]) if angle_code.startswith("1") else int(angle_code[1:] if angle_code.startswith("0") else angle_code)
            angle_rad = float(np.round(np.deg2rad(angle_deg), 5))
    
            if set(hex_pattern.lower().replace(" ", "")) == {"f"}:
                frequency_key = 0.0
                phase = 0.0
            else:
                profile = hex_to_binary_profile(hex_pattern, n_elements)
                cached_bin = (
                    self.decimations[index]
                    if index < len(self.decimations) else None
                )
                if cached_bin is None:
                    spectrum = np.fft.rfft(profile)
                    positive = np.abs(spectrum[1:])
                    frequency_bin = (
                        int(np.argmax(positive) + 1)
                        if positive.size and np.any(positive) else 0
                    )
                else:
                    frequency_bin = int(cached_bin)
                if not (0 <= frequency_bin <= n_elements // 2):
                    raise ValueError(
                        f"Invalid spatial-frequency bin {frequency_bin} in field {field_object.get_name_field()!r}."
                    )
                frequency_key = (
                    float(np.round(abs(frequency_axis[frequency_bin]) / 1000.0, 5))
                    if frequency_bin else 0.0
                )
                phase = float(get_phase_deterministic(profile))
    
            key = (frequency_key, angle_rad)
            phase_group = buffer.setdefault(key, {})
            phase_group.setdefault(phase, []).append(field)
    
        def _write_phase_average(destination, arrays):
            """Write the historical pairwise phase average into destination."""
            if not arrays:
                destination.fill(0)
                return
            np.copyto(destination, arrays[0], casting="unsafe")
            for array in arrays[1:]:
                np.add(destination, array, out=destination, casting="unsafe")
                destination *= np.float32(0.5)
    
        def process_key(key):
            phases = buffer[key]
            example = next(iter(phases.values()))[0]
            complex_output = np.empty(example.shape, dtype=np.complex64)
            if key[0] == 0.0:
                _write_phase_average(complex_output.real, next(iter(phases.values())))
                complex_output.imag.fill(0)
                return key, complex_output
    
            scratch = np.empty(example.shape, dtype=np.float32)
            _write_phase_average(complex_output.real, phases.get(0.0, []))
            _write_phase_average(scratch, phases.get(np.pi, []))
            np.subtract(complex_output.real, scratch, out=complex_output.real)
    
            _write_phase_average(complex_output.imag, phases.get(np.pi / 2, []))
            _write_phase_average(scratch, phases.get(3 * np.pi / 2, []))
            np.subtract(complex_output.imag, scratch, out=complex_output.imag)
            complex_output *= np.float32(np.pi / 2.0)
            del scratch
            return key, complex_output
    
        keys = list(buffer)
        if not keys:
            return {}

        requested_workers = (
            min(4, os.cpu_count() or 1) if max_workers is None else int(max_workers)
        )
        if requested_workers < 1:
            raise ValueError("max_workers must be a positive integer or None.")

        # Each active task needs one complex64 output and one float32 scratch
        # field (12 bytes per voxel). Bound this transient working set using
        # current host RAM while retaining the historical parallel execution.
        example_field = next(iter(next(iter(buffer.values())).values()))[0]
        bytes_per_task = int(example_field.size) * (np.dtype(np.complex64).itemsize + np.dtype(np.float32).itemsize)
        available_ram = get_available_host_memory_bytes()
        if available_ram is not None and bytes_per_task > 0:
            transient_budget = max(bytes_per_task, int(0.25 * available_ram))
            memory_workers = max(1, transient_budget // bytes_per_task)
        else:
            memory_workers = requested_workers
        worker_count = max(1, min(requested_workers, len(keys), int(memory_workers)))
        result = {}
        if worker_count == 1:
            for key in tqdm(keys, desc="[AOT-biomaps] Demodulating acoustic fields"):
                result[key] = process_key(key)[1]
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
                futures = [executor.submit(process_key, key) for key in keys]
                for future in tqdm(
                    concurrent.futures.as_completed(futures),
                    total=len(futures),
                    desc="[AOT-biomaps] Demodulating acoustic fields",
                ):
                    key, complex_field = future.result()
                    result[key] = complex_field
    
        print(f"[AOT-biomaps] Acoustic operator complete: {len(result)} configurations processed.")
        return result
    
    def flip_probe(self, flipPattern=True, flipAngle=True):
        """Flip probe activations and/or steering angles consistently.
    
        Acoustic-field spatial reversal is a view operation. The AO measurement
        columns are reindexed in one NumPy operation. A new ``StructuredWave``
        descriptor is created for each field while its data remains shared.
        """
        if not flipPattern and not flipAngle:
            return self
        if self.patterns is None:
            raise ValueError("patterns is not initialized.")
    
        n_patterns = len(self.patterns)
        if self.AcousticFields is not None and len(self.AcousticFields) != n_patterns:
            raise ValueError("AcousticFields and patterns have inconsistent lengths.")
        for attribute in ("AOsignal_withTumor", "AOsignal_withoutTumor"):
            signal = getattr(self, attribute)
            if signal is not None and signal.shape[1] != n_patterns:
                raise ValueError(f"{attribute} has {signal.shape[1]} columns; expected {n_patterns}.")
    
        n_elements = int(self.params.acoustic["probe"]["num_elements"])
        hex_chars = (n_elements + 3) // 4
        new_fields = []
        new_patterns = []
        new_profiles = []
        new_delays = []
        new_angles = []
        new_decimations = []
        element_index = np.arange(1, n_elements + 1, dtype=np.float64)
        sound_speed = float(self.params.acoustic["medium"]["c0"])
        element_width = float(self.params.acoustic["probe"]["element_width"])
    
        for index, pattern in enumerate(self.patterns):
            if "fileName" not in pattern:
                raise ValueError("flip_probe currently requires filename-based active-list patterns.")
            current_hex = pattern["fileName"].split("_")[0]
            current_angle = (
                float(self.theta[index]) if index < len(self.theta)
                else float(get_angle(pattern["fileName"]))
            )
            if flipPattern:
                bits = format(int(current_hex, 16), f"0{n_elements}b")[-n_elements:]
                flipped_hex = format(int(bits[::-1], 2), f"0{hex_chars}x")
            else:
                flipped_hex = current_hex
            new_angle = -current_angle if flipAngle else current_angle
            new_name = f"{flipped_hex}_{format_angle(new_angle)}"
    
            if self.AcousticFields is not None:
                new_field = StructuredWave(
                    fileName=new_name, params=self.params, medium=self.medium
                )
                source_field = self.AcousticFields[index].field
                if source_field is None:
                    raise ValueError(f"Field {self.AcousticFields[index].get_name_field()} is not loaded.")
                # The pipeline layout is (Nt, Nz, Nx): reverse x, not z.
                new_field.field = source_field[:, :, ::-1] if flipPattern else source_field
                new_fields.append(new_field)
    
            new_patterns.append({"fileName": new_name})
            profile = hex_to_binary_profile(flipped_hex, n_elements)
            new_profiles.append(profile)
            delays = (
                1000.0 / sound_speed * np.sin(np.deg2rad(new_angle))
                * element_index * element_width
            )
            new_delays.append(delays - delays.min())
            new_angles.append(new_angle)
            previous_frequency = (
                self.decimations[index] if index < len(self.decimations) else None
            )
            new_decimations.append(
                get_frequency(new_name, n_elements, element_width)
                if flipPattern or previous_frequency is None else previous_frequency
            )
    
        if flipPattern:
            for attribute in ("AOsignal_withTumor", "AOsignal_withoutTumor"):
                signal = getattr(self, attribute)
                if signal is not None:
                    setattr(self, attribute, signal[:, ::-1])
        if self.AcousticFields is not None:
            self.AcousticFields = new_fields
        self.ActiveList = new_profiles
        self.DelayLaw = new_delays
        self.theta = new_angles
        self.decimations = new_decimations
        self.patterns = new_patterns
        print("[AOT-biomaps] Probe configuration flip complete.")
        return self

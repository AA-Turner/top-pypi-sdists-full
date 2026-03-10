from AOT_biomaps.AOT_Acoustic.AcousticTools import format_angle, getAngle, getFrequency

from ._mainExperiment import Experiment
from AOT_biomaps.AOT_Acoustic.AcousticEnums import TypeSim, WaveType
from AOT_biomaps.AOT_Acoustic.StructuredWave import StructuredWave
from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Experiment.ExperimentTools import calc_mat_os, convert_to_hex_list, get_phase_deterministic, hex_to_binary_profile
import os
import psutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import h5py
from scipy.io import loadmat, savemat


class Tomography(Experiment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.patterns = None
        self.theta = []
        self.decimations = []
        self.ActiveList = []
        self.DelayLaw = []

    # PUBLIC METHODS
    def check(self):
        """
        Check if the experiment is correctly initialized.
        """
        if self.TypeAcoustic is None or self.TypeAcoustic.value == WaveType.FocusedWave.value:
            return False, "acousticType must be provided and cannot be FocusedWave for Tomography experiment"
        if self.AcousticFields is None:
            return False, "AcousticFields is not initialized. Please generate the system matrix first."
        if self.AOsignal_withTumor is None:
            return False, "AOsignal with tumor is not initialized. Please generate the AO signal with tumor first."
        if self.AOsignal_withoutTumor is None:
            return False, "AOsignal without tumor is not initialized. Please generate the AO signal without tumor first."
        if self.OpticImage is None:
            return False, "OpticImage is not initialized. Please generate the optic image first."
        if self.AOsignal_withoutTumor.shape != self.AOsignal_withTumor.shape:
            return False, "AOsignal with and without tumor must have the same shape."
        for field in self.AcousticFields:
            if field.field.shape[0] != self.AOsignal_withTumor.shape[0]:
                return False, f"Field {field.getName_field()} has an invalid Time shape: {field.field.shape[0]}. Expected time shape to be {self.AOsignal_withTumor.shape[0]}."
        if not all(field.field.shape == self.AcousticFields[0].field.shape for field in self.AcousticFields):
            return False, "All AcousticFields must have the same shape."
        if self.OpticImage is None:
            return False, "OpticImage is not initialized. Please generate the optic image first."
        if self.OpticImage.phantom is None:
            return False, "OpticImage phantom is not initialized. Please generate the phantom first."
        if self.OpticImage.laser is None:
            return False, "OpticImage laser is not initialized. Please generate the laser first."
        if self.OpticImage.laser.shape != self.OpticImage.phantom.shape:
            return False, "OpticImage laser and phantom must have the same shape."
        if self.OpticImage.phantom.shape[0] != self.AcousticFields[0].field.shape[1] or self.OpticImage.phantom.shape[1] != self.AcousticFields[0].field.shape[2]:
            return False, f"OpticImage phantom shape {self.OpticImage.phantom.shape} does not match AcousticFields shape {self.AcousticFields[0].field.shape[1:]}."
        return True, "Experiment is correctly initialized."

    def generateAcousticFields(self, fieldDataPath=None, show_log=True, nameBlock=None):
        """
        Generate the acoustic fields for simulation.
        Args:
            fieldDataPath: Path to save the generated fields.
            show_log: Whether to show progress logs.
        Returns:
            systemMatrix: A numpy array of the generated fields.
        """
        if self.medium is None:
            raise ValueError("Medium is not initialized. Please generate the medium first.")
        if self.TypeAcoustic.value == WaveType.StructuredWave.value:
            self.AcousticFields = self._generateAcousticFields_STRUCT_CPU(fieldDataPath, show_log, nameBlock)
            # for i in range(len(self.AcousticFields)):
            #     profile = hex_to_binary_profile(self.AcousticFields[i].getName_field()[6:-4], self.params.acoustic['probe']['num_elements'])
            #     self.ActiveList.append(profile)
            #     angle = self.AcousticFields[i].angle
            #     self.theta.append(angle)
            #     Delay = 1000 * (1/self.params.acoustic['medium']['c0']) * np.sin(np.deg2rad(angle)) * np.arange(1, self.params.acoustic['probe']['num_elements']  + 1) * self.params.acoustic['probe']['element_width']
            #     self.DelayLaw.append(Delay - np.min(Delay))

            #     if set(self.AcousticFields[i].getName_field()[6:-4].lower().replace(" ", "")) == {'f'}:
            #         fs_key = 0.0 # fs_key est en mm^-1 (0.0 mm^-1)
            #     else:   
            #         ft_prof = np.fft.fft(profile)
            #         idx_max = np.argmax(np.abs(ft_prof[1:len(profile)//2])) + 1
            #         freqs = np.fft.fftfreq(len(profile), d=self.params.general['dx'])

            #         # freqs est en m^-1 car delta_x est en mètres.
            #         fs_m_inv = abs(freqs[idx_max]) 

            #         fs_key = fs_m_inv # Fréquence spatiale en mm^-1

            #     # fs = n * dfx  => n = fs / dfx with dfx = 1/(N*delta_x)
            #     self.decimations.append(int(fs_key / (1/(len(profile)*self.params.general['dx']))))

        else:
            raise ValueError("Unsupported wave type.")

    def show_pattern(self):
        if self.AcousticFields is None:
            raise ValueError("AcousticFields is not initialized. Please generate the system matrix first.")

        # Collect and sort entries
        entries = []
        for field in self.AcousticFields:
            if field.waveType != WaveType.StructuredWave:
                raise TypeError("AcousticFields must be of type StructuredWave to plot pattern.")
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

        def hex_string_to_binary_column(hex_str):
            bits = ''.join(f'{int(c, 16):04b}' for c in hex_str)
            return np.array([int(b) for b in bits], dtype=np.uint8).reshape(-1, 1)

        bit_columns = [hex_string_to_binary_column(h) for h in hex_list]
        image = np.hstack(bit_columns)
        print(image)  # Doit être un tableau de 1 partout

        height, width = image.shape

        # Create figure with compact size
        fig, ax = plt.subplots(figsize=(5, 4))
        plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.2)

        # Plot binary pattern
        im = ax.imshow(image, cmap='binary', aspect='auto', interpolation='none', vmin=0, vmax=1)

        ax.set_title("Scan Configuration", fontsize=12, pad=10, weight='bold')
        ax.set_xlabel("Wave Index", fontsize=10, labelpad=8)
        ax.set_ylabel("Transducer Activation", fontsize=10, labelpad=8)
        yticks_positions = np.arange(0, height)  # Positions des ticks (0 à 191)
        yticks_labels = np.arange(1, height + 1)  # Labels de 1 à 192

        ax.set_yticks(yticks_positions)
        ax.set_yticklabels(yticks_labels, fontsize=8)
        # Plot angle markers (bigger and bolder)
        angle_min, angle_max = -20.2, 20.2
        center = height / 2
        scale = height / (angle_max - angle_min)
        for i, angle in enumerate(angle_list):
            y = round(center - angle * scale)
            if 0 <= y < height:
                ax.plot(i, y - 0.5, 'ro', markersize=4, alpha=0.7)  # Points rouges plus gros

        ax.set_ylim(height - 0.5, -0.5)

        # Twin axis for angles (with larger font)
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        yticks_angle = np.linspace(20, -20, 5)  # 5 ticks pour plus de détails
        yticks_pos = np.interp(yticks_angle, [angle_min, angle_max], [height - 0.5, -0.5])
        ax2.set_yticks(yticks_pos)
        ax2.set_yticklabels([f"{a:.1f}°" for a in yticks_angle], fontsize=9, color='r')
        ax2.set_ylabel("Angle [°]", fontsize=11, color='r', labelpad=10)
        ax2.tick_params(axis='y', colors='r', labelsize=9, width=1.5, length=5)

        # Make axes thicker
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        ax2.spines['right'].set_linewidth(1.5)

        # Add grid (thicker lines)
        ax.grid(True, linestyle='--', alpha=0.4, color='gray', linewidth=0.5)
        ax.set_xticks(np.linspace(0, width-1, 6))  # Plus de ticks sur l'axe x
        ax.set_yticks(np.linspace(0, height-1, 6))  # Plus de ticks sur l'axe y
        ax.tick_params(axis='both', which='both', labelsize=8, width=1.5, length=4)

        plt.tight_layout()
        plt.show()

    def plot_angle_frequency_distribution(self):
        if self.patterns is None:
            raise ValueError("patterns is not initialized. Please load or generate the active list first.")

        num_elements = self.params.acoustic['probe']['num_elements']
        divs = sorted([d for d in range(2, num_elements + 1) if num_elements % d == 0 and d % 2 == 0])
        if num_elements not in divs:
            divs.append(num_elements)
        divs.sort()

        angles = []
        freqs = []

        for p in self.patterns:
            # Extraire la chaîne "hexa_XXX" depuis le dictionnaire
            file_name = p["fileName"]
            hex_part, angle_str = file_name.split('_')  # Split sur le dictionnaire corrigé

            # Récupérer l'angle
            sign = -1 if angle_str[0] == '1' else 1
            angle = sign * int(angle_str[1:])
            angles.append(angle)

            # Récupérer la fréquence spatiale
            bits = np.array([int(b) for b in bin(int(hex_part, 16))[2:].zfill(num_elements)])
            if np.all(bits == 1):  # Cas "tous activés"
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
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Histogramme des angles
        axes[0].hist(angles, bins=np.arange(-20.5, 21.5, 1), color='skyblue', edgecolor='black', rwidth=0.8)
        axes[0].set_xlabel("Angle (°)")
        axes[0].set_ylabel("Nombre de patterns")
        axes[0].set_title("Distribution des angles")
        axes[0].set_xticks(np.arange(-20, 21, 2))

        # Histogramme des fréquences spatiales
        unique_freqs, freq_counts = np.unique(freqs, return_counts=True)
        x_pos = np.arange(len(divs))
        for freq, count in zip(unique_freqs, freq_counts):
            idx = divs.index(freq)
            axes[1].bar(x_pos[idx], count, color='salmon', edgecolor='black', width=0.8)

        axes[1].set_xticks(x_pos)
        axes[1].set_xticklabels(divs)
        axes[1].set_xlabel("Taille du bloc (fréquence spatiale)")
        axes[1].set_ylabel("Nombre de patterns")
        axes[1].set_title("Distribution des fréquences spatiales")

        plt.tight_layout()
        plt.show()

    def loadActiveList(self, fieldParamPath):
        if not os.path.exists(fieldParamPath):
            raise FileNotFoundError(f"Field parameter file {fieldParamPath} not found.")
        patterns = []
        with open(fieldParamPath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if "_" in line and all(c in "0123456789abcdefABCDEF" for c in line.split("_")[0]):
                    patterns.append({"fileName": line})
                    self.theta.append(getAngle(line))
                    profile = hex_to_binary_profile(line.split('_')[0], self.params.acoustic['probe']['num_elements'])
                    self.ActiveList.append(profile)
                    new_Delay = 1000 * (1/self.params.acoustic['medium']['c0']) * np.sin(np.deg2rad(self.theta[-1])) * np.arange(1, self.params.acoustic['probe']['num_elements'] + 1) * self.params.acoustic['probe']['element_width']
                    self.DelayLaw.append(new_Delay - np.min(new_Delay))
                    self.decimations.append(getFrequency(line, self.params.acoustic['probe']['num_elements'], self.params.acoustic['probe']['element_width']))    
                    continue
                try:
                    parsed = eval(line, {"__builtins__": None})
                    if isinstance(parsed, tuple) and len(parsed) == 2:
                        coords, angles = parsed
                        for angle in angles:
                            patterns.append({
                                "space_0": coords[0],
                                "space_1": coords[1],
                                "move_head_0_2tail": coords[2],
                                "move_tail_1_2head": coords[3],
                                "angle": angle
                            })
                    else:
                        raise ValueError("Ligne inattendue (pas un tuple de deux éléments)")
                except Exception as e:
                    print(f"Erreur de parsing sur la ligne : {line}\n{e}")
        self.patterns = patterns

    def saveActiveList(self, filePath):
        """
        Sauvegarde la liste des patterns dans un fichier texte.
        Args:
            filePath (str): Chemin du fichier de sortie.
        """
        with open(filePath, 'w') as file:
            for pattern in self.patterns:
                if "fileName" in pattern:
                    # Cas 1 : Pattern simple (format "hexa_XXX")
                    file.write(f"{pattern['fileName']}\n")
                else:
                    # Cas 2 : Pattern avec paramètres (format tuple)
                    coords = (
                        pattern["space_0"],
                        pattern["space_1"],
                        pattern["move_head_0_2tail"],
                        pattern["move_tail_1_2head"]
                    )
                    angles = [pattern["angle"]]  # Supposons que chaque pattern a un seul angle
                    line = f"({coords}, {angles})\n"
                    file.write(line)

    def generateActiveList(self, N = None, decimations = None, angles = None):
        """
        Génère une liste de patterns d'activation équilibrés et réguliers.
        Args:
            N (int): Nombre de patterns à générer.
        Returns:
            list: Liste de strings au format "hex_angle".
        """
        if decimations is not None and angles is not None:
            self.patterns = self._genereate_patterns_from_decimations(decimations, angles)
        elif N is not None and N > 1:
            self.patterns = self._generate_patterns(N)
            if not self._check_patterns(self.patterns):
                raise ValueError("Generated patterns failed validation.")
        else:
            raise ValueError("Either N (>=2) or both decimations and angles must be provided for pattern generation.")
      
    def saveAOsignals_matlab(self, filePath):

        savemat(filePath, {'data': self.AOsignal_withTumor, 'thetas': self.theta, 'decimations': self.decimations, 'ActiveList' : self.ActiveList, 'DelayLaw': self.DelayLaw})

    def selectAngles(self, angles):

        if self.AOsignal_withTumor is None and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signals are not initialized. Please load or generate the AO signals first.")
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is not initialized. Please generate the system matrix first.")
        newAcousticFields = []
        index = []
        for i,field in enumerate(self.AcousticFields):
            if field.angle in angles:
                newAcousticFields.append(field)
                index.append(i)
        if self.AOsignal_withTumor is not None:
            self.AOsignal_withTumor = self.AOsignal_withTumor[:, index]    
        if self.AOsignal_withoutTumor is not None:
            self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:, index]
        self.AcousticFields = newAcousticFields
        self.theta = [field.angle for field in newAcousticFields]
        self.decimations = [field.f_s for field in newAcousticFields] 
        self.DelayLaw = [self.DelayLaw[i] for i in index]
        self.ActiveList = [self.ActiveList[i] for i in index]

    def selectDecimations(self, decimations):
        if self.AOsignal_withTumor is None and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signals are not initialized. Please load or generate the AO signals first.")
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is not initialized. Please generate the system matrix first.")
        newAcousticFields = []
        index = []
        for i, field in enumerate(self.AcousticFields):
            if field.f_s in decimations:
                newAcousticFields.append(field)
                index.append(i)
        if self.AOsignal_withTumor is not None:
            self.AOsignal_withTumor = self.AOsignal_withTumor[:, index]
        if self.AOsignal_withoutTumor is not None:
            self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:, index]
        self.AcousticFields = newAcousticFields
        self.decimations = [field.f_s for field in newAcousticFields]   
        self.theta = [field.angle for field in newAcousticFields]   
        self.DelayLaw = [self.DelayLaw[i] for i in index]
        self.ActiveList = [self.ActiveList[i] for i in index]

    def selectPatterns(self, pattern_names):
        if self.AOsignal_withTumor is None and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signals are not initialized. Please load or generate the AO signals first.")
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is not initialized. Please generate the system matrix first.")
        newAcousticFields = []
        index = []
        for i,field in enumerate(self.AcousticFields):
            if field.pattern.activeList in pattern_names:
                newAcousticFields.append(field)
                index.append(i)
        if self.AOsignal_withTumor is not None:
            self.AOsignal_withTumor = self.AOsignal_withTumor[:, index]    
        if self.AOsignal_withoutTumor is not None:
            self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:, index]
        self.AcousticFields = newAcousticFields
        self.decimations = [field.f_s for field in newAcousticFields]   
        self.theta = [field.angle for field in newAcousticFields]   
        self.DelayLaw = [self.DelayLaw[i] for i in index]
        self.ActiveList = [self.ActiveList[i] for i in index]

    def selectRandom(self,N):
        if self.AOsignal_withTumor is None and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signals are not initialized. Please load or generate the AO signals first.")
        if self.AcousticFields is None or len(self.AcousticFields) == 0:
            raise ValueError("AcousticFields is not initialized. Please generate the system matrix first.")
        if N > len(self.AcousticFields):
            raise ValueError("N is larger than the number of available AcousticFields.")
        indices = np.random.choice(len(self.AcousticFields), size=N, replace=False)
        newAcousticFields = [self.AcousticFields[i] for i in indices]
        if self.AOsignal_withTumor is not None:
            self.AOsignal_withTumor = self.AOsignal_withTumor[:, indices]    
        if self.AOsignal_withoutTumor is not None:
            self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:, indices]
        self.AcousticFields = newAcousticFields
        self.decimations = [field.f_s for field in newAcousticFields]   
        self.theta = [field.angle for field in newAcousticFields]   
        self.DelayLaw = [self.DelayLaw[i] for i in indices]
        self.ActiveList = [self.ActiveList[i] for i in indices]

    def _genereate_patterns_from_decimations(self, decimations, angles):
        if isinstance(decimations, list):
            decimations = np.array(decimations)
        if isinstance(angles, list):
            angles = np.array(angles)

        angles = np.sort(angles)
        decimations = np.sort(decimations)
        self.DelayLaw = []

        num_elements = self.params.acoustic['probe']['num_elements']
        Width = self.params.acoustic['probe']['element_width']
        kerf = self.params.acoustic['probe'].get('kerf', 0.00000)
        Nactuators = num_elements

        # --- Calcul du nombre de Scans ---
        has_zero = 0 in decimations
        if has_zero:
            Nscans = 4 * len(angles) * (len(decimations) - 1) + len(angles)
        else:
            Nscans = 4 * len(angles) * len(decimations)

        ActiveLIST = np.ones((num_elements, Nscans))

        # --- Calcul des positions ---
        Xc = (Width + (Nactuators - 1) * (kerf + Width)) / 2
        Xm = np.array([Width * (i - 1) + Width / 2 - Xc for i in range(1, Nactuators + 1)])

        # --- Offset initial ---
        # Si on a un 0, les motifs modulés commencent après l'onde plane
        # Sinon, ils commencent à l'indice 0
        current_offset = len(angles) if has_zero else 0

        if has_zero:
            I_plane = np.arange(len(angles))
            ActiveLIST[:, I_plane] = 1 

        # --- Traitement des décimations non nulles ---
        active_decimations = decimations[decimations != 0]
        dFx = 1 / (Nactuators * Width)

        for i_dec in range(len(active_decimations)):
            # Calcul des indices relatif à l'offset de départ
            I = np.arange(len(angles)) + current_offset + (i_dec * 4 * len(angles))

            Icos   = I
            Incos  = I + 1 * len(angles)
            Insin  = I + 2 * len(angles) # Insin avant Isin pour respecter ton ordre de stockage
            Isin   = I + 3 * len(angles)

            fx = dFx * active_decimations[i_dec]

            # Appliquer les motifs modulés
            ActiveLIST[:, Icos] = calc_mat_os(Xm, fx, ActiveLIST[:, Icos[:1]], 'cos')
            ActiveLIST[:, Incos] = 1 - ActiveLIST[:, Icos]
            ActiveLIST[:, Isin] = calc_mat_os(Xm, fx, ActiveLIST[:, Isin[:1]], 'sin')
            ActiveLIST[:, Insin] = 1 - ActiveLIST[:, Isin]

        # --- Conversion et formatage ---
        hexa_list = convert_to_hex_list(ActiveLIST)
        
        def format_angle(a):
            return f"{'1' if a < 0 else '0'}{abs(a):02d}"

        patterns = []
        print(f"Generating {Nscans} patterns...")
        for i in range(Nscans):
            angle_val = angles[i % len(angles)]
            hex_pattern = hexa_list[i]
            pair = f"{hex_pattern}_{format_angle(angle_val)}"
            patterns.append({"fileName": pair})
        
        self.decimations = decimations
        self.theta = angles
        for angle in angles:
            new_Delay = 1000 * (1/self.params.acoustic['medium']['c0']) * np.sin(np.deg2rad(angle)) * np.arange(1, num_elements + 1) * self.params.acoustic['probe']['element_width']
            self.DelayLaw.append(new_Delay - np.min(new_Delay))

        self.ActiveList = ActiveLIST
        return patterns
 
    def _generate_patterns(self, N,angles = None):
        def format_angle(a):
            return f"{'1' if a < 0 else '0'}{abs(a):02d}"

        def bits_to_hex(bits):
            bit_string = ''.join(str(b) for b in bits)
            bit_string = bit_string.zfill(len(bits))
            hex_string = ''.join([f"{int(bit_string[i:i+4], 2):x}" for i in range(0, len(bit_string), 4)])
            return hex_string

        num_elements = self.params.acoustic['probe']['num_elements']
        if angles is None:
            angle_choices = list(range(-20, 21))
        else:
            # convert np.array to list if necessary
            if isinstance(angles, np.ndarray):
                angles = angles.tolist()
            angle_choices = angles

        # 1. Trouver TOUS les diviseurs PAIRS de num_elements (y compris num_elements)
        divs = [d for d in range(2, num_elements + 1) if num_elements % d == 0 and d % 2 == 0]
        if not divs:
            print(f"Aucun diviseur pair trouvé pour num_elements = {num_elements}")
            return []

        # 2. Utiliser un ensemble pour suivre les patterns uniques
        unique_patterns = set()

        # 3. Générer jusqu'à N patterns uniques
        while len(unique_patterns) < N:
            # Tirer un diviseur aléatoire (y compris num_elements)
            block_size = np.random.choice(divs)

            if block_size == num_elements:
                # Cas spécial : pattern "tous activés"
                pattern_bits = np.ones(num_elements, dtype=int)
            else:
                # Cas général : pattern équilibré
                half_block = block_size // 2
                block = np.array([0] * half_block + [1] * half_block)
                reps = num_elements // block_size
                base_pattern = np.tile(block, reps)
                # Tirer un décalage aléatoire
                shift = np.random.randint(0, block_size)
                pattern_bits = np.roll(base_pattern, shift)

            # Convertir en hex et choisir un angle aléatoire
            hex_pattern = bits_to_hex(pattern_bits)
            angle = np.random.choice(angle_choices)
            pair = f"{hex_pattern}_{format_angle(angle)}"

            # Ajouter à l'ensemble (les doublons sont automatiquement ignorés)
            unique_patterns.add(pair)

        # 4. Convertir en liste de dictionnaires avec la clé "fileName"
        patterns = [{"fileName": pair} for pair in unique_patterns]

        # 5. Retourner exactement N patterns (on a déjà vérifié la taille avec while)
        return patterns[:N]  # Par sécurité, même si len(unique_patterns) == N

    def _check_patterns(self, patterns):
        # 1. Vérifier les doublons (basé sur "fileName")
        file_names = [p["fileName"] for p in patterns]
        if len(file_names) != len(set(file_names)):
            # Trouver les doublons
            from collections import Counter
            file_counts = Counter(file_names)
            duplicates = [fn for fn, count in file_counts.items() if count > 1]
            for dup in duplicates:
                print(f"Erreur : Doublon détecté pour {dup}")
            return False

        # 2. Vérifier chaque pattern individuellement
        num_elements = self.params.acoustic['probe']['num_elements']
        for pattern in patterns:
            hex_part, angle_str = pattern["fileName"].split('_')
            bits = np.array([int(b) for b in bin(int(hex_part, 16))[2:].zfill(num_elements)])

            # Vérifier la longueur
            if len(bits) != num_elements:
                print(f"Erreur longueur: {pattern['fileName']}")
                return False

            # Cas spécial : pattern "tous activés"
            if np.all(bits == 1):
                continue

            # Vérifier l'équilibre 0/1
            if np.sum(bits) != num_elements // 2:
                print(f"Erreur équilibre 0/1: {pattern['fileName']}")
                return False

            # Vérifier la régularité
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
                print(f"Erreur régularité: {pattern['fileName']}")
                return False

        return True

    def applyApodisation(self, alpha=0.3, divergence_deg=0.5):
        """
        Applique une apodisation dynamique sur les champs acoustiques stockés dans l'objet.
        L'apodisation suit l'angle d'émission et la divergence naturelle du faisceau pour
        supprimer les lobes de diffraction (artefacts de bord) sans toucher au signal utile.
        Args:
            probe_width (float): Largeur physique active de la sonde (ex: 40e-3 pour 40mm).
            alpha (float): Paramètre de Tukey (0.0=rectangle, 1.0=hann). 0.3 est un bon compromis.
            divergence_deg (float): Angle d'ouverture du masque pour suivre l'élargissement du faisceau.
                                    0.0 = Droit, 0.5 = Légère ouverture (conseillé).
        """
        print(f"Applying apodization (Alpha={alpha}, Div={divergence_deg}°) on {len(self.AcousticFields)} fields...")
        
        probe_width = self.params.acoustic['probe']['num_elements'] * self.params.acoustic['probe']['element_width']

        for i in trange(len(self.AcousticFields), desc="Apodisation"):
            # 1. Récupération des données et de l'angle
            field = self.AcousticFields[i].field  # Peut être (Z, X) ou (Time, Z, X)
            angle = self.AcousticFields[i].angle  # L'angle de l'onde plane

            # 2. Récupération ou construction des axes physiques
            nz, nx = field.shape[-2:]

            if hasattr(self, 'x_axis') and self.x_axis is not None:
                x_axis = self.x_axis
            else:
                # Génération par défaut centrée sur 0 (ex: -20mm à +20mm)
                x_axis = np.linspace(-probe_width/2, probe_width/2, nx)

            if hasattr(self, 'z_axis') and self.z_axis is not None:
                z_axis = self.z_axis
            else:
                # Génération par défaut (ex: 0 à 40mm, basé sur un pitch standard ou arbitraire)
                estimated_depth = 40e-3  # Valeur arbitraire si inconnue
                z_axis = np.linspace(0, estimated_depth, nz)

            # 3. Préparation des grilles pour le masque
            Z, X = np.meshgrid(z_axis, x_axis, indexing='ij')

            # 4. Calcul de la géométrie orientée (Steering)
            angle_rad = np.deg2rad(angle)
            X_aligned = X - Z * np.tan(angle_rad)

            # 5. Calcul de la largeur dynamique du masque (Divergence)
            div_rad = np.deg2rad(divergence_deg)
            current_half_width = (probe_width / 2.0) + Z * np.tan(div_rad)

            # 6. Normalisation et création du masque Tukey
            X_norm = np.divide(X_aligned, current_half_width, out=np.zeros_like(X_aligned), where=current_half_width!=0)

            mask = np.zeros_like(X_norm)
            plateau_threshold = 1.0 * (1 - alpha)

            # Zone centrale (plateau = 1)
            mask[np.abs(X_norm) <= plateau_threshold] = 1.0

            # Zone de transition (cosinus)
            transition_indices = (np.abs(X_norm) > plateau_threshold) & (np.abs(X_norm) <= 1.0)
            if np.any(transition_indices):
                x_trans = np.abs(X_norm[transition_indices]) - plateau_threshold
                width_trans = 1.0 * alpha
                mask[transition_indices] = 0.5 * (1 + np.cos(np.pi * x_trans / width_trans))

            # 7. Application du masque (Gestion 2D vs 3D)
            if field.ndim == 3:
                field_apodized = field * mask[np.newaxis, :, :]
            else:
                field_apodized = field * mask

            # 8. Mise à jour de l'objet
            self.AcousticFields[i].field = field_apodized

        print("Apodisation done.")

    # PRIVATE METHODS
    def _generateAcousticFields_STRUCT_CPU(self, fieldDataPath=None, show_log=False, nameBlock=None):
        if self.patterns is None:
            raise ValueError("patterns is not initialized. Please load or generate the active list first.")
        listAcousticFields = []
        progress_bar = trange(0, len(self.patterns), desc="Generating acoustic fields")
        for i in progress_bar:
            memory = psutil.virtual_memory()
            pattern = self.patterns[i]
            if "fileName" in pattern:
                AcousticField = StructuredWave(fileName=pattern["fileName"], params=self.params, medium=self.medium)
            else:
                AcousticField = StructuredWave(
                    angle_deg=pattern["angle"],
                    space_0=pattern["space_0"],
                    space_1=pattern["space_1"],
                    move_head_0_2tail=pattern["move_head_0_2tail"],
                    move_tail_1_2head=pattern["move_tail_1_2head"],
                    params=self.params,
                    medium=self.medium
                )
            if fieldDataPath is None:
                pathField = None
            else:
                pathField = os.path.join(fieldDataPath, AcousticField.getName_field() + self.FormatSave.value)
            if pathField is not None and os.path.exists(pathField) and self.params.acoustic['typeSim'] != TypeSim.SIMPLE_SIM.value:
                progress_bar.set_postfix_str(f"Loading field - {AcousticField.getName_field()} -- Memory used: {memory.percent}%")
                try:
                    AcousticField.load_field(fieldDataPath, self.FormatSave,nameBlock)
                except:
                    progress_bar.set_postfix_str(f"Error loading field -> Generating field - {AcousticField.getName_field()} -- Memory used: {memory.percent}% ---- processing on {config.get_process().upper()} ----")
                    AcousticField.generate_field(show_log=show_log)
                    if not os.path.exists(pathField):
                        progress_bar.set_postfix_str(f"Saving field - {AcousticField.getName_field()} -- Memory used: {memory.percent}%")
                        os.makedirs(os.path.dirname(pathField), exist_ok=True)
                        AcousticField.save_field(fieldDataPath)
            else:
                progress_bar.set_postfix_str(f"Generating field - {AcousticField.getName_field()} -- Memory used: {memory.percent}% ---- processing on {config.get_process().upper()} ----")
                AcousticField.generate_field(show_log=show_log)
                if pathField is not None and not os.path.exists(pathField) and self.params.acoustic['typeSim'] != TypeSim.SIMPLE_SIM.value:
                    progress_bar.set_postfix_str(f"Saving field - {AcousticField.getName_field()} -- Memory used: {memory.percent}%")
                    os.makedirs(os.path.dirname(pathField), exist_ok=True)
                    AcousticField.save_field(fieldDataPath)
            listAcousticFields.append(AcousticField)
            progress_bar.set_postfix_str("")

        return listAcousticFields

    def load_experimentalAO(self, pathAO, withTumor = True, h5name='AOsignal'):
        """
        Load experimental AO signals from specified file paths.
        Args:
            path_withTumor: Path to the AO signal with tumor.
            path_withoutTumor: Path to the AO signal without tumor.
        """
        if not os.path.exists(pathAO):
            raise FileNotFoundError(f"File {pathAO} not found.")

        if pathAO.endswith('.npy'):
            ao_signal = np.load(pathAO)
        elif pathAO.endswith('.h5'):
            with h5py.File(pathAO, 'r') as f:
                if h5name not in f:
                    raise KeyError(f"Dataset '{h5name}' not found in the HDF5 file.")
                ao_signal = f[h5name][:]
        elif pathAO.endswith('.mat'):
            mat_data = loadmat(pathAO)
            if h5name not in mat_data:
                raise KeyError(f"Dataset '{h5name}' not found in the .mat file.")
            ao_signal = mat_data[h5name]
        elif pathAO.endswith('.hdr'):
            ao_signal = self._loadAOSignal(pathAO)
        else:
            raise ValueError("Unsupported file format. Supported formats are: .npy, .h5, .mat, .hdr")
        
        if withTumor:
            self.AOsignal_withTumor = ao_signal
        else:
            self.AOsignal_withoutTumor = ao_signal

    def check_experimentalAO(self, activeListPath, withTumor=True):
        """
        Check if the experimental AO signals are correctly initialized.
        """
        if withTumor:
            if self.AOsignal_withTumor is None:
                raise ValueError("Experimental AOsignal with tumor is not initialized. Please load the experimental AO signal with tumor first.")
        else:
            if self.AOsignal_withoutTumor is None:
                raise ValueError("Experimental AOsignal without tumor is not initialized. Please load the experimental AO signal without tumor first.")
        if self.AcousticFields is not None:
            # get min time shape between all AO signals
            print()
            
            if self.AcousticFields[0].field.shape[0] > self.AOsignal_withTumor.shape[0]:
                self.cutAcousticFields(max_t=self.AOsignal_withTumor.shape[0]/float(self.params.acoustic['f_saving']))
            else:
                for i in range(len(self.AcousticFields)):
                    min_time_shape = min(self.AcousticFields[i].field.shape[0])
                if withTumor:
                    self.AOsignal_withTumor = self.AOsignal_withTumor[:min_time_shape, :]
                else:
                    self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:min_time_shape, :]

            for field in self.AcousticFields:                        
                if activeListPath is not None:
                    with open(activeListPath, 'r') as file:
                        lines = file.readlines()
                        expected_name = lines[self.AcousticFields.index(field)].strip()
                        nameField = field.getName_field()
                        if nameField.startswith("field_"):
                            nameField = nameField[len("field_"):]
                        if nameField != expected_name:
                            raise ValueError(f"Field name {nameField} does not match the expected name {expected_name} from the active list.")
        print("Experimental AO signals are correctly initialized.")

    def parse_and_demodulate(self, withTumor=True):

        if withTumor:
            AOsignal = self.AOsignal_withTumor
        else:
            AOsignal = self.AOsignal_withoutTumor
        delta_x = self.params.general['dx']  # en m 
        n_piezos = self.params.acoustic['probe']['num_elements']
        demodulated_data = {}
        structured_buffer = {} 

        for i in trange(AOsignal.shape[1], desc="Demodulating AO signals"):   
            hex_pattern =  self.patterns[i]["fileName"]
            fs_key = self.decimations[i]
            angle_rad = np.deg2rad(self.theta[i])
            
            # Onde Plane (f_s = 0)
            if fs_key == 0:
                demodulated_data[(fs_key, angle_rad)] = np.array(AOsignal[:,i])
                continue
                
            # Onde Structurée
            profile = hex_to_binary_profile(hex_pattern, n_piezos)
            
            # Calcul FS (Fréquence de Structuration)
            ft_prof = np.fft.fft(profile)
            # On regarde uniquement la partie positive non DC
            idx_max = np.argmax(np.abs(ft_prof[1:len(profile)//2])) + 1
            freqs = np.fft.fftfreq(len(profile), d=delta_x)
            
            # freqs est en m^-1 car delta_x est en mètres.
            fs_m_inv = abs(freqs[idx_max]) 
            
            # *** CORRECTION 1: Conversion de f_s en mm^-1 (mm^-1 est utilisé dans iRadon) ***
            fs_key = fs_m_inv / 1000.0 # Fréquence spatiale en mm^-1

            
            if fs_key == 0: continue

            # Calcul de la Phase (Shift)
            phase = get_phase_deterministic(profile)
            
            # Stockage par (fs, theta) et phase
            key = (fs_key, angle_rad)
            if key not in structured_buffer:
                structured_buffer[key] = {}
            
            # La moyenne est nécessaire si plusieurs acquisitions ont la même phase (pour le SNR) 
            if phase in structured_buffer[key]:
                structured_buffer[key][phase] = (structured_buffer[key][phase] + np.array(AOsignal[:,i])) / 2
            else:
                structured_buffer[key][phase] = np.array(AOsignal[:,i])
 
        for (fs, theta), phases in structured_buffer.items():
            s0 = phases.get(0.0, 0)
            s_pi_2 = phases.get(np.pi/2, 0)
            s_pi = phases.get(np.pi, 0)
            s_3pi_2 = phases.get(3*np.pi/2, 0)

            # Assurer que les zéros sont des vecteurs de la bonne taille
            example = next(val for val in phases.values() if not isinstance(val, int))
            if isinstance(s0, int): s0 = np.zeros_like(example)
            if isinstance(s_pi, int): s_pi = np.zeros_like(example)
            if isinstance(s_pi_2, int): s_pi_2 = np.zeros_like(example)
            if isinstance(s_3pi_2, int): s_3pi_2 = np.zeros_like(example)

            real = s0 - s_pi
            imag = s_pi_2 - s_3pi_2 
              
            demodulated_data[(fs, theta)] = (real - 1j * imag) / (2/np.pi)
            
        return demodulated_data
    
    def demodulate_acoustic_fields(self):
        """
        Retourne un dictionnaire plat : {(fs, theta): champ_complexe}
        Identique à la structure de parse_and_demodulate.
        """
        n_piezos = self.params.acoustic['probe']['num_elements']
        delta_x = self.params.general['dx']
        
        # buffer[(fs, theta)][phase] = champ_réel
        buffer = {} 

        # 1. Groupement et Moyennage
        for i in trange(len(self.AcousticFields), desc="Organizing Acoustic Fields"):   
            field_obj = self.AcousticFields[i]
            label = field_obj.getName_field()
            parts = label.split("_")
            hex_pattern = parts[1]
            angle_code = parts[-1]
            
            # Extraction Angle et Fréquence
            angle_deg = -int(angle_code[1:]) if angle_code.startswith("1") else int(angle_code)
            angle_rad = np.round(np.deg2rad(angle_deg), 6)
            
            if set(hex_pattern.lower().replace(" ", "")) == {'f'}:
                fs_key = 0.0
                phase = 0.0
            else:
                profile = hex_to_binary_profile(hex_pattern, n_piezos)
                ft_prof = np.fft.fft(profile)
                idx_max = np.argmax(np.abs(ft_prof[1:n_piezos//2])) + 1
                freqs = np.fft.fftfreq(n_piezos, d=delta_x)
                fs_key = np.round(abs(freqs[idx_max]) / 1000.0, 6)
                phase = get_phase_deterministic(profile)
            
            # CLÉ PLATE (fs, theta)
            key = (fs_key, angle_rad)
            if key not in buffer: buffer[key] = {}
            
            current_f = field_obj.field
            if phase in buffer[key]:
                buffer[key][phase] = (buffer[key][key] + current_f) / 2
            else:
                buffer[key][phase] = current_f

        # 2. Quadrature
        demodulated_fields = {}
        keys = list(buffer.keys())
        
        for i in trange(len(keys), desc="Computing Complex Operator"):
            key = keys[i] # key est (fs, theta)
            phases = buffer[key]
            fs = key[0]
            
            if fs == 0.0:
                demodulated_fields[key] = next(iter(phases.values())).astype(np.complex64)
            else:
                s0 = phases.get(0.0)
                s_pi_2 = phases.get(np.pi/2)
                s_pi = phases.get(np.pi)
                s_3pi_2 = phases.get(3*np.pi/2)

                example = next(iter(phases.values()))
                s0 = s0 if s0 is not None else np.zeros_like(example)
                s_pi = s_pi if s_pi is not None else np.zeros_like(example)
                s_pi_2 = s_pi_2 if s_pi_2 is not None else np.zeros_like(example)
                s_3pi_2 = s_3pi_2 if s_3pi_2 is not None else np.zeros_like(example)

                real = s0 - s_pi
                imag = s_pi_2 - s_3pi_2 
                
                # Stockage avec la clé (fs, theta)
                demodulated_fields[key] = ((real - 1j * imag) / (2/np.pi)).astype(np.complex64)
                    
        print(f"Acoustic Operator complete: {len(demodulated_fields)} configurations processed.")
        return demodulated_fields

    def flipProbe(self, flipPattern=True, flipAngle=True):
        """
        Flip the probe (binary pattern and/or angle) for all acoustic fields and AO signals.

        Args:
            flipPattern (bool): If True, reverse the order of active elements in the binary pattern.
            flipAngle (bool): If True, invert the sign of the angle.
        """
        if self.AcousticFields is None:
            print("Warning: AcousticFields is not initialized. No fields to flip, only AO signals.")
            available_fields = False
        else:            
            available_fields = True

        num_elements = self.params.acoustic['probe']['num_elements']
        hex_chars_expected = (num_elements + 3) // 4  # Number of hex chars expected for num_elements bits

        new_AcousticFields = []
        new_ActiveList = []
        new_DelayLaw = []
        new_theta = []
        new_decimations = []

        # Flip AO signals if they exist
        if self.AOsignal_withTumor is not None:
            if flipPattern:
                self.AOsignal_withTumor = self.AOsignal_withTumor[:, ::-1]  # Inverse l'ordre des colonnes (N)
            numScans = self.AOsignal_withTumor.shape[1]
        if self.AOsignal_withoutTumor is not None:
            if flipPattern:
                self.AOsignal_withoutTumor = self.AOsignal_withoutTumor[:, ::-1]  # Inverse l'ordre des colonnes (N)
            numScans = self.AOsignal_withoutTumor.shape[1]

        for i in trange(numScans, desc="Flipping AO signals"):
            fileName = self.patterns[i]["fileName"].split('_')[0]  # Extract the hex pattern part
            # Extract the current pattern and angle from the field name
            angle = self.theta[i]

            # Flip the binary pattern if requested
            if flipPattern:
                bits = bin(int(fileName, 16))[2:].zfill(num_elements)
                flipped_bits = bits[::-1]  # Reverse the bits
                flipped_hex = f"{int(flipped_bits, 2):0{hex_chars_expected}x}"
            else:
                flipped_hex = fileName  # Keep the original pattern


            if flipAngle:
                new_angle = -angle  # Invert the angle
            else:
                new_angle = angle  # Keep the original angle

 

            # Create a new StructuredWave with the flipped pattern and/or angle
            if available_fields:
                new_angle_str = format_angle(new_angle)
                new_field_name = f"field_{flipped_hex}_{new_angle_str}"
                new_field = StructuredWave(
                    fileName=new_field_name,
                    params=self.params,
                    medium=self.medium
                )

            # Copy the field data (flipping columns if flipPattern is True)
            if flipPattern:
                if available_fields:
                    new_field.field = self.AcousticFields[i].field[:, ::-1, :]  # Reverse the order of elements (columns)
            else:
                if available_fields:
                    new_field.field = self.AcousticFields[i].field.copy()  # Keep the original field data
            if available_fields:
                new_AcousticFields.append(new_field)
            new_theta.append(new_angle)

            # Update ActiveList (binary profile)
            new_profile = hex_to_binary_profile(flipped_hex, num_elements)
            new_ActiveList.append(new_profile)

            # Update DelayLaw
            new_Delay = 1000 * (1/self.params.acoustic['medium']['c0']) * np.sin(np.deg2rad(new_angle)) * np.arange(1, num_elements + 1) * self.params.acoustic['probe']['element_width']
            new_DelayLaw.append(new_Delay - np.min(new_Delay))

            # Update decimations (recalculate if pattern is flipped)
            if flipPattern:
                if set(flipped_hex.lower().replace(" ", "")) == {'f'}:
                    fs_key = 0.0  # fs_key in mm^-1 (0.0 mm^-1 for all elements active)
                else:
                    ft_prof = np.fft.fft(new_profile)
                    idx_max = np.argmax(np.abs(ft_prof[1:len(new_profile)//2])) + 1
                    freqs = np.fft.fftfreq(len(new_profile), d=self.params.general['dx'])
                    fs_m_inv = abs(freqs[idx_max])
                    fs_key = fs_m_inv  # Spatial frequency in mm^-1
                new_decimations.append(int(fs_key / (1/(len(new_profile)*self.params.general['dx']))))
            else:
                new_decimations.append(self.AcousticFields[i].f_s)  # Keep the original decimation

        # Update the attributes
        if available_fields:
            self.AcousticFields = new_AcousticFields
        self.ActiveList = new_ActiveList
        self.DelayLaw = new_DelayLaw
        self.theta = new_theta
        self.decimations = new_decimations
        if flipPattern and flipAngle:
            print(f"Flipped both probe and AO signals (pattern and angle).")
        elif flipPattern and not flipAngle:
            print(f"Flipped probe and AO signals (pattern).")
        elif not flipPattern and flipAngle:
            print(f"Flipped probe and AO signals (angle).")
        else:   
            print(f"No flipping applied.")


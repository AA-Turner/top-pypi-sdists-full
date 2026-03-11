from AOT_biomaps.Settings import Params
from AOT_biomaps.AOT_Optic._mainOptic import Phantom
from AOT_biomaps.AOT_Acoustic.AcousticEnums import WaveType, FormatSave
from AOT_biomaps.AOT_Acoustic.StructuredWave import StructuredWave
from AOT_biomaps.AOT_Medium.HomogeneousMedium import HomogeneousMedium
from AOT_biomaps.AOT_Medium.PVAMedium import PVAMedium
from AOT_biomaps.AOT_Medium.MediumEnums import PhantomType

from abc import ABC, abstractmethod
import os

import numpy as np
import torch
import torch.nn.functional as F
from tqdm import trange
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import copy

class Experiment(ABC):
    def __init__(self, params, acousticType=WaveType.StructuredWave, formatSave=FormatSave.HDR_IMG):
        self.params = params
        self.OpticImage = None
        self.medium = None
        self.AcousticFields = None
        self.AOsignal_withTumor = None
        self.AOsignal_withoutTumor = None

        if type(acousticType).__name__ != "WaveType":
            raise TypeError("acousticType must be an instance of the WaveType class")

        self.FormatSave = formatSave
        self.TypeAcoustic = acousticType

        if type(self.params) != Params:
            raise TypeError("params must be an instance of the Params class")

    def copy(self):
        """Retourne une copie profonde de l'objet."""
        return copy.deepcopy(self)
    
    def generatePhantom(self):
        """
        Generate the phantom for the experiment.
        This method initializes the OpticImage attribute with a Phantom instance.
        """
        self.OpticImage = Phantom(params=self.params)
    
    def generateMedium(self):
        """
        Generate the medium for the experiment.
        This method initializes the medium attribute based on the parameters.
        """
        if self.params.acoustic['medium']['type'] == PhantomType.Homogeneous.value:
            self.medium = HomogeneousMedium(params=self.params)
            self.medium.generate_medium()
            print("Medium generated: Homogeneous. -- done.")
        elif self.params.acoustic['medium']['type'] == PhantomType.PVA.value:
            try:
                self.medium = PVAMedium(params=self.params)
                self.medium.generate_medium()
                print("Medium generated: PVA heterogeneous. -- done.")
            except Exception as e:
                
                print(f"Error generating PVA medium: {e}")
                raise
    
    def loadMedium(self, folderPath, fileName="medium"):
        """
        Load the medium from a .joblib file.
        This method initializes the medium attribute by loading it from the specified file.
        """
        if self.params.acoustic['medium']['type'] == PhantomType.Homogeneous.value:
            self.medium = HomogeneousMedium(params=self.params)
            self.medium.load_medium(folderPath, fileName)
        elif self.params.acoustic['medium']['type'] == PhantomType.PVA.value:
            self.medium = PVAMedium(params=self.params)
            self.medium.load_medium(folderPath, fileName)

        print(f"Medium loaded from {os.path.join(folderPath, fileName)} -- done.")

    def saveMedium(self, folderPath, fileName="medium"):
        """
        Save the medium to a .joblib file.
        This method saves the medium attribute to the specified file.
        """
        if self.medium is None:
            raise ValueError("Medium is not initialized. Please generate or set the medium before saving.")
        self.medium.save_medium(folderPath, fileName)
        print(f"Medium saved to {os.path.join(folderPath, fileName)} -- done.")

    @abstractmethod
    def generateAcousticFields(self, fieldDataPath, fieldParamPath, show_log=True):
        """
        Generate the acoustic fields for simulation.
        Args:
            fieldDataPath: Path to save the generated fields.
            fieldParamPath: Path to the field parameters file.
        Returns:
            systemMatrix: A numpy array of the generated fields.
        """
        pass

    def cutAcousticFields(self, max_t, min_t=0, show_log=True):
        """
        Cut the acoustic fields to a specified time range.
        Args:
            max_t: Maximum time in SAMPLE to keep in the fields.
            min_t: Minimum time in SAMPLE to keep in the fields (default is 0).
            show_log: Whether to display a progress bar.
        """

        if min_t < 0 or max_t < 0:
            raise ValueError("min_t and max_t must be non-negative integers.")
        if min_t >= max_t:
            raise ValueError("min_t must be less than max_t.")

        if not self.AcousticFields:
            raise ValueError("AcousticFields is empty. Cannot cut fields.")

        iteration = range(len(self.AcousticFields)) if not show_log else trange(len(self.AcousticFields), desc=f"Cutting Acoustic Fields ({min_t} to {max_t} samples)")
        for i in iteration:
            field = self.AcousticFields[i]
            if field.field.shape[0] < max_t:
                raise ValueError(f"Field {field.getName_field()} has an invalid shape: {field.field.shape}. Expected shape to be at least ({max_t},).")
            self.AcousticFields[i].field = field.field[min_t:max_t, :, :]

    def addNoise(self, noiseType='gaussian', noiseLvl=0.1, withTumor=True, show_log=True):
        """
        Ajoute du bruit (gaussien ou poisson) au signal AO sélectionné.

        Args:
            noiseType (str): Type de bruit à ajouter ('gaussian' ou 'poisson').
            noiseLvl (float): Niveau de bruit (écart-type pour le bruit gaussien, facteur multiplicatif pour le bruit de Poisson).
            withTumor (bool): Si True, ajoute le bruit au signal avec tumeur, sinon au signal sans tumeur.
        """
        if withTumor and self.AOsignal_withTumor is None:
            raise ValueError("AO signal with tumor is not generated. Please generate it first.")
        if not withTumor and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signal without tumor is not generated. Please generate it first.")

        if withTumor:
            AOsignals = self.AOsignal_withTumor
        else:
            AOsignals = self.AOsignal_withoutTumor
        
        noiseSignals = np.zeros_like(AOsignals)
        iteration = range(AOsignals.shape[1]) if not show_log else trange(AOsignals.shape[1], desc=f"Adding {noiseType} noise to AO signal {'with' if withTumor else 'without'} tumor")
        for i in iteration:
            AOsignal = AOsignals[:, i]
            if noiseType.lower() == 'gaussian':
                noise = np.random.normal(0, noiseLvl*np.max(AOsignal), AOsignal.shape)
                noisy_signal = AOsignal + noise
            elif noiseType.lower() == 'poisson':
                # Pour le bruit de Poisson, on utilise souvent un facteur multiplicatif
                # car le bruit de Poisson est proportionnel à la racine carrée du signal.
                # Ici, on multiplie le signal par un facteur aléatoire centré autour de 1.
                noise = np.random.poisson(noiseLvl * np.abs(AOsignal)) / (noiseLvl * np.abs(AOsignal).max())
                noisy_signal = AOsignal * noise
            else:
                raise ValueError("noiseType must be either 'gaussian' or 'poisson'.")
            noisy_signal = np.clip(noisy_signal, a_min=0, a_max=None)  # Assurer que le signal reste non négatif
            noiseSignals[:, i] = noisy_signal
        return noiseSignals

    def reduceDims(self, mode='avg'):
        """
        Réduit les dimensions T, X, Z d'un numpy array (T, X, Z) par 2 en utilisant une convolution.
        Retourne un numpy array et met à jour les paramètres numériques.
        """
        for i in trange(len(self.AcousticFields),
                        desc="Downsampling Acoustic Fields (T, X, Z → T//2, X//2, Z//2)"):
            # Conversion en tenseur PyTorch
            field = self.AcousticFields[i].field
            if not isinstance(field, torch.Tensor):
                field = torch.from_numpy(field)

            # Vérification de la forme (doit être 3D : T, X, Z)
            if field.dim() != 3:
                raise ValueError(f"Forme non supportée : {field.shape}. Attendu (T, X, Z).")

            # Ajout des dimensions pour conv3d : (1, 1, T, X, Z)
            x = field.unsqueeze(0).unsqueeze(0)

            # Réduction par convolution 3D
            if mode == 'avg':
                x_down = F.avg_pool3d(x, kernel_size=(2, 2, 2), stride=(2, 2, 2))
            else:  # mode == 'max'
                x_down = F.max_pool3d(x, kernel_size=(2, 2, 2), stride=(2, 2, 2))

            # Conversion en numpy array et suppression des dimensions ajoutées
            self.AcousticFields[i].field = x_down.squeeze(0).squeeze(0).cpu().numpy()

        # Fonction utilitaire pour convertir et mettre à jour un paramètre
        def convert_and_update(param_dict, key, operation):
            if key in param_dict:
                if isinstance(param_dict[key], str):
                    param_dict[key] = float(param_dict[key])
                param_dict[key] = operation(param_dict[key])

        # Mise à jour des paramètres
        convert_and_update(self.params.acoustic, 'f_saving', lambda x: x / 2)
        for param in ['dx', 'dy', 'dz']:
            convert_and_update(self.params.general, param, lambda x: x * 2)

    def normalizeAOsignals(self, withTumor=True):
        if withTumor and self.AOsignal_withTumor is None:
            raise ValueError("AO signal with tumor is not generated. Please generate it first.")
        if not withTumor and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signal without tumor is not generated. Please generate it first.")
        if withTumor:
            self.AOsignal_withTumor = self.AOsignal_withTumor - np.min(self.AOsignal_withTumor)/(np.max(self.AOsignal_withTumor)-np.min(self.AOsignal_withTumor))
        else:
            self.AOsignal_withoutTumor = self.AOsignal_withoutTumor - np.min(self.AOsignal_withoutTumor)/(np.max(self.AOsignal_withoutTumor)-np.min(self.AOsignal_withoutTumor))

    def saveAcousticFields(self, save_directory):
        progress_bar = trange(len(self.AcousticFields), desc="Saving Acoustic Fields")
        for i in progress_bar:
            progress_bar.set_postfix_str(f"-- {self.AcousticFields[i].getName_field()}")
            self.AcousticFields[i].save_field(save_directory, formatSave=self.FormatSave)

    def show_animated_Acoustic(self, wave_name=None, desired_duration_ms=5000, save_dir=None):
        """
        Plot synchronized animations of A_matrix slices for selected angles.
        Args:
            wave_name: optional name for labeling the subplots (e.g., "wave1")
            desired_duration_ms: Total duration of the animation in milliseconds.
            save_dir: directory to save the animation gif; if None, animation will not be saved
        Returns:
            ani: Matplotlib FuncAnimation object
        """
        mpl.rcParams['animation.embed_limit'] = 100
        if save_dir is not None:
            os.makedirs(save_dir, exist_ok=True)

        num_plots = len(self.AcousticFields)
        if num_plots <= 5:
            nrows, ncols = 1, num_plots
        else:
            ncols = 5
            nrows = (num_plots + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 5.3 * nrows))
        if isinstance(axes, plt.Axes):
            axes = np.array([axes])
        axes = axes.flatten()
        ims = []

        fig.suptitle(f"System Matrix Animation {wave_name}", fontsize=12, y=0.98)

        for idx in range(num_plots):
            ax = axes[idx]
            im = ax.imshow(self.AcousticFields[0, :, :, idx],
                        extent=(self.params.general['Xrange'][0], self.params.general['Xrange'][1], self.params.general['Zrange'][1], self.params.general['Zrange'][0]),
                        vmax=1, aspect='equal', cmap='jet', animated=True)
            ax.set_xlabel("x (mm)", fontsize=8)
            ax.set_ylabel("z (mm)", fontsize=8)
            ims.append((im, ax, idx))

        for j in range(num_plots, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        def update(frame):
            artists = []
            for im, ax, idx in ims:
                im.set_array(self.AcousticFields[frame, :, :, idx])
                fig.suptitle(f"System Matrix Animation {wave_name} t = {frame * 25e-6 * 1000:.2f} ms", fontsize=10)
                artists.append(im)
            return artists

        interval = desired_duration_ms / self.AcousticFields.shape[0]
        ani = animation.FuncAnimation(
            fig, update,
            frames=range(0, self.AcousticFields.shape[0]),
            interval=interval, blit=True
        )

        if save_dir is not None:
            now = datetime.now()
            date_str = now.strftime("%Y_%d_%m_%y")
            save_filename = f"AcousticField_{wave_name}_{date_str}.gif"
            save_path = os.path.join(save_dir, save_filename)
            ani.save(save_path, writer='pillow', fps=20)
            print(f"Saved: {save_path}")

        plt.close(fig)
        return ani

    def generateAOsignal(self, withTumor=True, AOsignalDataPath=None):

        if AOsignalDataPath is not None:
            if not os.path.exists(AOsignalDataPath):
                raise FileNotFoundError(f"AO file {AOsignalDataPath} not found.")
            if withTumor:
                self.AOsignal_withTumor = self._loadAOSignal(AOsignalDataPath)
                if self.AOsignal_withTumor.shape[0] != self.AcousticFields[0].field.shape[0]:
                    print(f"AO signal shape {self.AOsignal_withTumor.shape} does not match the expected shape {self.AcousticFields[0].field.shape}. Resizing Acoustic fields...")
                    self.cutAcousticFields(max_t=self.AOsignal_withTumor.shape[0] / float(self.params.acoustic['f_saving']), min_t=0)
            else:
                self.AOsignal_withoutTumor = self._loadAOSignal(AOsignalDataPath)
                if self.AOsignal_withoutTumor.shape[0] != self.AcousticFields[0].field.shape[0]:
                    print(f"AO signal shape {self.AOsignal_withoutTumor.shape} does not match the expected shape {self.AcousticFields[0].field.shape}. Resizing Acoustic fields...")
                    self.cutAcousticFields(max_t=self.AOsignal_withoutTumor.shape[0] / float(self.params.acoustic['f_saving']), min_t=0)
        else:    
            if self.AcousticFields is None:
                raise ValueError("AcousticFields is not initialized. Please generate the system matrix first.")

            if self.OpticImage is None:
                raise ValueError("OpticImage is not initialized. Please generate the phantom first.")
            
            if not all(field.field.shape == self.AcousticFields[0].field.shape for field in self.AcousticFields):
                minShape = min([field.field.shape[0] for field in self.AcousticFields])
                self.cutAcousticFields(max_t=minShape * self.params.acoustic['f_saving'])
            else:
                shape_field = self.AcousticFields[0].field.shape

            AOsignal = np.zeros((shape_field[0], len(self.AcousticFields)), dtype=np.float32)

            if withTumor:
                description = "Generating AO Signal with Tumor"
            else:
                description = "Generating AO Signal without Tumor"

            for i in trange(len(self.AcousticFields), desc=description):
                for t in range(self.AcousticFields[i].field.shape[0]):
                    if withTumor:
                        interaction = self.OpticImage.phantom * self.AcousticFields[i].field[t, :, :]
                    else:
                        interaction = self.OpticImage.laser.intensity * self.AcousticFields[i].field[t, :, :]
                    AOsignal[t, i] = np.sum(interaction)

            if withTumor:
                self.AOsignal_withTumor = AOsignal
            else:
                self.AOsignal_withoutTumor = AOsignal

    @staticmethod
    def _loadAOSignal(AOsignalPath):
        if AOsignalPath.endswith(".cdh"):
            with open(AOsignalPath, "r") as file:
                cdh_content = file.readlines()
            
            cdf_path = AOsignalPath.replace(".cdh", ".cdf")

            # Extraire les paramètres depuis le fichier .cdh
            n_scans = int([line.split(":")[1].strip() for line in cdh_content if "Number of events" in line][0])
            n_acquisitions_per_event = int([line.split(":")[1].strip() for line in cdh_content if "Number of acquisitions per event" in line][0])
            num_elements = int([line.split(":")[1].strip() for line in cdh_content if "Number of US transducers" in line][0])

            # Initialisation des structures
            AO_signal = np.zeros((n_acquisitions_per_event, n_scans), dtype=np.float32)
            active_lists = []
            angles = []

            # Lecture du fichier binaire
            with open(cdf_path, "rb") as file:
                for j in trange(n_scans, desc="Lecture des événements"):
                    # Lire l'activeList : 48 caractères hex = 24 bytes
                    active_list_bytes = file.read(24)
                    active_list_hex = active_list_bytes.hex()
                    active_lists.append(active_list_hex)

                    # Lire l'angle (1 byte signé)
                    angle_byte = file.read(1)
                    angle = np.frombuffer(angle_byte, dtype=np.int8)[0]
                    angles.append(angle)

                    # Lire le signal AO (float32)
                    data = np.frombuffer(file.read(n_acquisitions_per_event * 4), dtype=np.float32)
                    if len(data) != n_acquisitions_per_event:
                        raise ValueError(f"Erreur à l'événement {j} : attendu {n_acquisitions_per_event}, obtenu {len(data)}")
                    AO_signal[:, j] = data

            return AO_signal


        elif AOsignalPath.endswith(".npy"):
            return np.load(AOsignalPath)  # Supposé déjà au bon format
        else:
            raise ValueError("Format de fichier non supporté. Utilisez .cdh/.cdf ou .npy.")

    def saveAOsignals_Castor(self, save_directory, withTumor=True):
        if withTumor:
            AO_signal = self.AOsignal_withTumor
            cdf_location = os.path.join(save_directory, "AOSignals_withTumor.cdf")
            cdh_location = os.path.join(save_directory, "AOSignals_withTumor.cdh")
        else:
            AO_signal = self.AOsignal_withoutTumor
            cdf_location = os.path.join(save_directory, "AOSignals_withoutTumor.cdf")
            cdh_location = os.path.join(save_directory, "AOSignals_withoutTumor.cdh")

        info_location = os.path.join(save_directory, "info.txt")
        nScan = AO_signal.shape[1]

        with open(cdf_location, "wb") as fileID:
            for j in range(AO_signal.shape[1]):
                active_list_hex = self.AcousticFields[j].pattern.activeList
                for i in range(0, len(active_list_hex), 2):
                    byte_value = int(active_list_hex[i:i+2], 16)
                    fileID.write(byte_value.to_bytes(1, byteorder='big'))
                angle = self.AcousticFields[j].angle
                fileID.write(np.int8(angle).tobytes())
                fileID.write(AO_signal[:, j].astype(np.float32).tobytes())

        header_content = (
            f"Data filename: {'AOSignals_withTumor.cdf' if withTumor else 'AOSignals_withoutTumor.cdf'}\n"
            f"Number of events: {nScan}\n"
            f"Number of acquisitions per event: {AO_signal.shape[0]}\n"
            f"Start time (s): 0\n"
            f"Duration (s): 1\n"
            f"Acquisition frequency (Hz): {self.params.acoustic['f_saving']}\n"
            f"Data mode: histogram\n"
            f"Data type: AOT\n"
            f"Number of US transducers: {self.params.acoustic['probe']['num_elements']}"
        )

        with open(cdh_location, "w") as fileID:
            fileID.write(header_content)

        with open(info_location, "w") as fileID:
            for field in self.AcousticFields:
                fileID.write(field.getName_field() + "\n")

        print(f"Fichiers .cdf, .cdh et info.txt sauvegardés dans {save_directory}")

    def showAOsignal(self, withTumor=True, save_dir=None, wave_name=None):
        if withTumor and self.AOsignal_withTumor is None:
            raise ValueError("AO signal with tumor is not generated. Please generate it first.")
        if not withTumor and self.AOsignal_withoutTumor is None:
            raise ValueError("AO signal without tumor is not generated. Please generate it first.")

        if withTumor:
            AOsignal = self.AOsignal_withTumor
        else:
            AOsignal = self.AOsignal_withoutTumor

        time_axis = np.arange(AOsignal.shape[0]) / float(self.params.acoustic['f_saving']) * 1e6

        num_plots = AOsignal.shape[1]
        if num_plots <= 5:
            nrows, ncols = 1, num_plots
        else:
            ncols = 5
            nrows = (num_plots + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 5.3 * nrows))
        if isinstance(axes, plt.Axes):
            axes = np.array([axes])
        axes = axes.flatten()

        if wave_name is None:
            title = "AO Signal -- all plots"
        else:
            title = f"AO Signal -- {wave_name}"

        fig.suptitle(title, fontsize=12, y=0.98)

        for idx in range(num_plots):
            ax = axes[idx]
            ax.plot(time_axis, AOsignal[:, idx])
            ax.set_xlabel("Time (µs)", fontsize=8)
            ax.set_ylabel("Value", fontsize=8)

        for j in range(num_plots, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        if save_dir is not None:
            now = datetime.now()
            date_str = now.strftime("%Y_%d_%m_%y")
            os.makedirs(save_dir, exist_ok=True)
            save_filename = f"Static_y_Plot{wave_name}_{date_str}.png"
            save_path = os.path.join(save_dir, save_filename)
            plt.savefig(save_path, dpi=200)
            print(f"Saved: {save_path}")

        plt.show()
        plt.close(fig)

    def show_animated_all(self, fileOfAcousticField=None, save_dir=None, desired_duration_ms=5000):
        mpl.rcParams['animation.embed_limit'] = 100
        pattern_str = StructuredWave.getPattern(fileOfAcousticField)
        angle = StructuredWave.getAngle(fileOfAcousticField)
        fieldToPlot = None

        for field in self.AcousticFields:
            if field.get_path() == fileOfAcousticField:
                fieldToPlot = field
                idx = self.AcousticFields.index(field)
                break
        else:
            raise ValueError(f"Field {fileOfAcousticField} not found in AcousticFields.")

        if wave_name is None:
            wave_name = f"Pattern structure {pattern_str}"

        fig, axs = plt.subplots(1, 2, figsize=(6 * 2, 5.3 * 1))
        if isinstance(axs, plt.Axes):
            axs = np.array([axs])

        fig.suptitle(f"AO Signal Animation {wave_name} | Angle {angle}°", fontsize=12, y=0.98)

        axs[0].imshow(self.OpticImage.T, cmap='hot', alpha=1, origin='upper',
                    extent=(self.params.general['Xrange'][0], self.params.general['Xrange'][1], self.params.general['Zrange'][1], self.params.general['Zrange'][0]),
                    aspect='equal')

        im_field = axs[0].imshow(fieldToPlot[0, :, :, idx], cmap='jet', origin='upper',
                                extent=(self.params.general['Xrange'][0], self.params.general['Xrange'][1], self.params.general['Zrange'][1], self.params.general['Zrange'][0]),
                                vmax=1, vmin=0.01, alpha=0.8, aspect='equal')

        axs[0].set_title(f"{wave_name} | Angle {angle}° | t = 0.00 ms", fontsize=10)
        axs[0].set_xlabel("x (mm)", fontsize=8)
        axs[0].set_ylabel("z (mm)", fontsize=8)

        time_axis = np.arange(self.AOsignal.shape[0]) * 25e-6 * 1000
        line_y, = axs[1].plot(time_axis, self.AOsignal[:, idx])
        vertical_line, = axs[1].plot([time_axis[0], time_axis[0]], [0, self.AOsignal[0, idx]], 'r--')

        axs[1].set_xlabel("Time (ms)", fontsize=8)
        axs[1].set_ylabel("Value", fontsize=8)
        axs[1].set_title(f"{wave_name} | Angle {angle}° | t = 0.00 ms", fontsize=10)

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        def update(frame):
            current_time_ms = frame * 25e-6 * 1000
            frame_data = fieldToPlot[frame, :, :, idx]
            masked_data = np.where(frame_data > 0.02, frame_data, np.nan)
            im_field.set_data(masked_data)
            axs[0].set_title(f"{wave_name} | Angle {angle}° | t = {current_time_ms:.2f} ms", fontsize=10)

            y_vals = self.AOsignal[:, idx]
            y_copy = np.full_like(y_vals, np.nan)
            y_copy[:frame + 1] = y_vals[:frame + 1]
            line_y.set_data(time_axis, y_copy)

            vertical_line.set_data([time_axis[frame], time_axis[frame]], [0, y_vals[frame]])
            axs[1].set_title(f"{wave_name} | Angle {angle}° | t = {current_time_ms:.2f} ms", fontsize=10)

            return [im_field, vertical_line, line_y]

        interval = desired_duration_ms / fieldToPlot.shape[0]
        ani = animation.FuncAnimation(
            fig, update,
            frames=range(0, self.AcousticFields.shape[0]),
            interval=interval, blit=True
        )

        if save_dir is not None:
            now = datetime.now()
            date_str = now.strftime("%Y_%d_%m_%y")
            os.makedirs(save_dir, exist_ok=True)
            save_filename = f"A_y_LAMBDA_overlay_{pattern_str}_{angle}_{date_str}.gif"
            save_path = os.path.join(save_dir, save_filename)
            ani.save(save_path, writer='pillow', fps=20)
            print(f"Saved: {save_path}")

        plt.close(fig)
        return ani

    def showPhantom(self, withROI=False):
        """
        Displays the optical phantom with absorbers.
        """
        try:
            if withROI:
                self.OpticImage.show_ROI()
            else:
                self.OpticImage.show_phantom()
        except Exception as e:
            raise RuntimeError(f"Error plotting phantom: {e}")
        
    @abstractmethod
    def check(self):
        """
        Check if the experiment is correctly initialized.
        """
        pass

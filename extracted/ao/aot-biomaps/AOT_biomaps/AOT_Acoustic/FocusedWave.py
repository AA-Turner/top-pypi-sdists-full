from ._mainAcoustic import AcousticField
from .AcousticEnums import WaveType

import os
import numpy as np
import matplotlib.pyplot as plt



class FocusedWave(AcousticField):

    def __init__(self, focal_line, **kwargs):
        """
        Initialize the FocusedWave object.

        Parameters:
        - focal_line (tuple): The focal line coordinates (x) in meters.
        - **kwargs: Additional keyword arguments for AcousticField initialization.
        """
        super().__init__(**kwargs)
        self.waveType = WaveType.FocusedWave
        # self.medium.kgrid.setTime(int(self.medium.kgrid.Nt*2),self.medium.kgrid.dt) # Extend the time grid to allow for delays
        self.focal_line = focal_line
        self.delayedSignal = self._apply_delay()

    def getName_field(self):
        """
        Generate the name for the field file based on the focal line.

        Returns:
            str: File name for the system matrix file.
        """
        try:
            return f"field_focused_X{self.focal_line*1000:.2f}_Z{self.params.acoustic['emission']['Foc']*1000:.2f}"
        except Exception as e:
            print(f"Error generating file name: {e}")
            return None

    def _apply_delay(self, dt=None, dx=None, c0=None):
        """
        Applique un retard temporel parabolique CORRECT pour une focalisation.
        Les éléments sur les bords sont activés EN PREMIER (retard plus petit).

        Args:
            dt: Pas temporel (en secondes). Si None, utilise self.medium.kgrid.dt.
            dx: Pas spatial (en mètres). Si None, utilise self.params.general['dx'].
            c0: Vitesse du son (en m/s). Si None, utilise self.params.acoustic['medium']['c0'].

        Returns:
            ndarray: Tableau des signaux retardés (shape: [total_grid_points, len(burst) + max_delay]).
        """
        try:
            # 1. Initialisation des paramètres
            if dx is None:
                dx = self.params.general['dx']
            if c0 is None:
                c0 = self.params.acoustic['medium']['c0']
            actual_dt = dt if dt is not None else self.medium.kgrid.dt

            # 2. Configuration de la grille et des éléments
            element_width_grid_points = int(round(self.params.acoustic['probe']['element_width'] / dx))
            total_grid_points = self.params.acoustic['probe']['num_elements'] * element_width_grid_points

            # Positions physiques des éléments (en mètres)
            element_positions = np.linspace(
                self.params.general['Xrange'][0] + self.params.acoustic['probe']['element_width'] / 2,
                self.params.general['Xrange'][1] - self.params.acoustic['probe']['element_width'] / 2,
                self.params.acoustic['probe']['num_elements']
            )

            # 3. Sélection des éléments actifs (focalisation)
            N_piezoFocal = self.params.acoustic['emission']['N_piezoFocal']  # Utilisation directe du paramètre


            center_idx = np.argmin(np.abs(element_positions - self.focal_line))
            start_idx = max(0, center_idx - N_piezoFocal)
            end_idx = min(self.params.acoustic['probe']['num_elements'] - 1, center_idx + N_piezoFocal)
            active_elements = np.arange(start_idx, end_idx + 1)
            active_element_positions = element_positions[active_elements]

            # 4. Calcul des retards paraboliques CORRECTS
            # On veut que les éléments sur les bords aient un retard plus petit
            # La loi correcte : retard = (Foc - sqrt(Foc² + x_rel²)) / c0
            x_rel = active_element_positions - self.focal_line
            delays = (self.params.acoustic['emission']['Foc'] - np.sqrt(self.params.acoustic['emission']['Foc']**2 + x_rel**2)) / c0

            # 5. Trouver le retard maximum (en valeur absolue)
            max_delay = np.max(np.abs(delays))

            # 6. Conversion en échantillons
            delay_samples = np.round(delays / actual_dt).astype(int)
            max_delay_samples = np.max(np.abs(delay_samples))

            # 7. Initialisation du tableau des signaux retardés
            delayed_signals = np.zeros((total_grid_points, len(self.burst) + max_delay_samples))

            # 8. Application des retards aux éléments actifs
            for elem_idx in active_elements:
                start_grid = elem_idx * element_width_grid_points
                end_grid = start_grid + element_width_grid_points
                elem_delay = delay_samples[elem_idx - start_idx]  # Retard pour cet élément

                # Décalage dans le tableau : max_delay + elem_delay
                # Cela permet de gérer les retards négatifs
                shift = max_delay_samples + elem_delay

                for grid_idx in range(start_grid, end_grid):
                    if shift >= 0 and shift + len(self.burst) <= delayed_signals.shape[1]:
                        delayed_signals[grid_idx, shift:shift + len(self.burst)] = self.burst


            return delayed_signals

        except Exception as e:
            print(f"Erreur lors de l'application des retards: {e}")
            return None

    def plot_delay(self):
        """
        Plot the time of the maximum of each delayed signal to visualize the wavefront.
        """
        try:
            # Find the index of the maximum for each delayed signal
            max_indices = np.argmax(self.delayedSignal, axis=1)
            element_indices = np.linspace(0, self.params.acoustic['probe']['num_elements'] - 1, self.delayedSignal.shape[0])
            # Convert indices to time
            max_times = max_indices / self.params.acoustic['f_AQ'] * 1e6

            # Détermine la valeur minimale des temps de maximum (pour les éléments actifs)
            min_active_time = np.min(max_times[max_times > 0])

            # Plot the times of the maxima
            plt.figure(figsize=(10, 6))
            plt.plot(element_indices, max_times, 'o-')
            plt.title('Time of Maximum for Each Delayed Signal')
            plt.xlabel('Transducer Element Index')
            plt.ylabel('Time of Maximum (µs)')
            plt.grid(True)

            # Ajuste l'échelle de l'axe Y pour commencer à la valeur minimale des éléments actifs
            plt.ylim(bottom=min_active_time * 0.95)  # Ajoute une marge de 5% pour plus de lisibilité
            plt.show()
        except Exception as e:
            print(f"Error plotting max times: {e}")

    def _SetUpSource(self, source, Nx, dt, dx, c0, factorT):
        """
        Configure la source k-Wave pour une onde focalisée en 2D.
        Applique les retards paraboliques et sélectionne les éléments actifs autour du point focal.

        Args:
            source: Objet k-Wave source (p_mask et p seront modifiés).
            Nx: Nombre de points de la grille en x.
            dt: Pas temporel (en secondes).
            dx: Pas spatial (en mètres).
            c0: Vitesse du son (en m/s).
            factorT: Facteur de sous-échantillonnage temporel.
        """
        # Largeur d'un élément en pixels
        el_width_px = int(round(self.params.acoustic['probe']['element_width'] / dx))
        total_sonde_px = self.params.acoustic['probe']['num_elements'] * el_width_px

        # Largeur du milieu (PVA) en pixels
        pva_nx = int(np.round(self.params.acoustic['medium']['width'] / dx))
        air_margin = (Nx - pva_nx) // 2

        # Position de départ pour centrer la sonde sur le milieu
        current_position = air_margin + (pva_nx - total_sonde_px) // 2

        # --- Sélection des éléments actifs (focalisation) ---
        element_positions = np.linspace(
            self.params.general['Xrange'][0] + self.params.acoustic['probe']['element_width'] / 2,
            self.params.general['Xrange'][1] - self.params.acoustic['probe']['element_width'] / 2,
            self.params.acoustic['probe']['num_elements']
        )

        # Largeur active et éléments actifs (TxWidth = Foc/2)
        TxWidth = self.params.acoustic['emission']['Foc'] / 2  # en mètres
        pitch = self.params.acoustic['probe']['element_width']  # en mètres
        N_piezoFocal = int(round(TxWidth / pitch))

        center_idx = np.argmin(np.abs(element_positions - self.focal_line))
        start_idx = max(0, center_idx - N_piezoFocal)
        end_idx = min(self.params.acoustic['probe']['num_elements'] - 1, center_idx + N_piezoFocal)
        active_indices = np.arange(start_idx, end_idx + 1)

        # Masque des éléments actifs (grille 1D)
        activeListGrid = np.zeros(total_sonde_px, dtype=int)

        # Configuration du masque k-Wave et marquage des indices actifs
        for i in range(self.params.acoustic['probe']['num_elements']):
            if i in active_indices:
                x_start = current_position
                x_end = x_start + el_width_px
                source.p_mask[x_start:x_end, 0] = 1  # Activation dans p_mask

                # Marquage des indices pour injection du signal
                idx_start = i * el_width_px
                idx_end = idx_start + el_width_px
                activeListGrid[idx_start:idx_end] = 1

            current_position += el_width_px

        # Injection du signal (retards paraboliques)
        if factorT != 1:
            delayedSignal = self._apply_delay(dt=dt, dx=dx, c0=c0)
        else:
            delayedSignal = self.delayedSignal

        # Application du signal uniquement aux éléments actifs
        amplitude = float(self.params.acoustic['emission']['voltage']) * float(self.params.acoustic['emission']['sensitivity'])
        source.p = amplitude * delayedSignal[activeListGrid == 1, :]

        return source

    def _save2D_HDR_IMG(self, filePath):
        """
        Save the acoustic field to .img and .hdr files.

        Parameters:
        - filePath (str): Path to the folder where files will be saved.
        """
        try:
            t_ex = 1 / self.params.acoustic['f_US']
            x_focal = self.focal_line
            z_focal = self.params.acoustic['emission']['Foc']
            file_name = self.getName_field()

            img_path = os.path.join(filePath, file_name + ".img")
            hdr_path = os.path.join(filePath, file_name + ".hdr")

            # Save the acoustic field to the .img file
            with open(img_path, "wb") as f_img:
                self.field.astype('float32').tofile(f_img)

            # Generate headerFieldGlob
            headerFieldGlob = (
                f"!INTERFILE :=\n"
                f"modality : AOT\n"
                f"voxels number transaxial: {self.field.shape[2]}\n"
                f"voxels number transaxial 2: {self.field.shape[1]}\n"
                f"voxels number axial: {1}\n"
                f"field of view transaxial: {(self.params.general['Xrange'][1] - self.params.general['Xrange'][0]) * 1000}\n"
                f"field of view transaxial 2: {(self.params.general['Zrange'][1] - self.params.general['Zrange'][0]) * 1000}\n"
                f"field of view axial: {1}\n"
            )

            # Generate header
            header = (
                f"!INTERFILE :=\n"
                f"!imaging modality := AOT\n\n"
                f"!GENERAL DATA :=\n"
                f"!data offset in bytes := 0\n"
                f"!name of data file := system_matrix/{file_name}.img\n\n"
                f"!GENERAL IMAGE DATA\n"
                f"!total number of images := {self.field.shape[0]}\n"
                f"imagedata byte order := LITTLEENDIAN\n"
                f"!number of frame groups := 1\n\n"
                f"!STATIC STUDY (General) :=\n"
                f"number of dimensions := 3\n"
                f"!matrix size [1] := {self.field.shape[2]}\n"
                f"!matrix size [2] := {self.field.shape[1]}\n"
                f"!matrix size [3] := {self.field.shape[0]}\n"
                f"!number format := short float\n"
                f"!number of bytes per pixel := 4\n"
                f"scaling factor (mm/pixel) [1] := {self.params.general['dx'] * 1000}\n"
                f"scaling factor (mm/pixel) [2] := {self.params.general['dx'] * 1000}\n"
                f"scaling factor (s/pixel) [3] := {1 / self.params.acoustic['f_AQ']}\n"
                f"first pixel offset (mm) [1] := {self.params.general['Xrange'][0] * 1e3}\n"
                f"first pixel offset (mm) [2] := {self.params.general['Zrange'][0] * 1e3}\n"
                f"first pixel offset (s) [3] := 0\n"
                f"data rescale offset := 0\n"
                f"data rescale slope := 1\n"
                f"quantification units := 1\n\n"
                f"!SPECIFIC PARAMETERS :=\n"
                f"focal point (x, z) := {x_focal}, {z_focal}\n"
                f"number of US transducers := {self.params.acoustic['probe']['num_elements']}\n"
                f"delay (s) := 0\n"
                f"us frequency (Hz) := {self.params.acoustic['f_US']}\n"
                f"excitation duration (s) := {t_ex}\n"
                f"!END OF INTERFILE :=\n"
            )

            # Save the .hdr file
            with open(hdr_path, "w") as f_hdr:
                f_hdr.write(header)

            with open(os.path.join(filePath, "field.hdr"), "w") as f_hdr2:
                f_hdr2.write(headerFieldGlob)
        except Exception as e:
            print(f"Error saving HDR/IMG files: {e}")
 
    def _generate_acoustic_field_SIMPLE_SIM(self, show_log=False):
        pass
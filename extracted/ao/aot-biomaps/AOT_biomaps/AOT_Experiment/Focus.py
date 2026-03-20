from AOT_biomaps.AOT_Acoustic.AcousticEnums import WaveType
from AOT_biomaps.AOT_Acoustic.FocusedWave import FocusedWave
from ._mainExperiment import Experiment

from tqdm import trange
import os
import psutil
import numpy as np
from scipy.ndimage import zoom
class Focus(Experiment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # PUBLIC METHODS

    def check(self):
        """
        Check if the experiment is correctly initialized.
        """
        if self.TypeAcoustic is None or self.TypeAcoustic.value != WaveType.FocusedWave.value:
           return False, "acousticType must be provided and must be FocusedWave for Focus experiment"
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

    def generateAcousticFields(self, fieldDataPath=None, show_log=False, nameBlock=None):
        """
        Génère une liste de champs acoustiques focalisés pour chaque élément de la sonde.
        Utilise trange pour afficher une barre de progression et gère la mémoire.

        Args:
            fieldDataPath (str): Chemin pour sauvegarder les champs générés.
            show_log (bool): Si True, affiche les logs de progression.
            nameBlock (str): Nom du bloc pour la sauvegarde (optionnel).

        Returns:
            list: Liste des objets FocusedWave générés.
        """
        listAcousticFields = []
        num_elements = self.params.acoustic['probe']['num_elements']
        element_width = self.params.acoustic['probe']['element_width']

        # Barre de progression avec trange
        progress_bar = trange(num_elements, desc="Generating focused acoustic fields")

        for k in progress_bar:
            # Vérifie l'utilisation mémoire
            memory = psutil.virtual_memory()

            # Calcule la position de la ligne focale pour l'élément k (en mètres)
            x_k = (k - (num_elements - 1) / 2) * element_width

            # Crée un nom de fichier pour ce champ
            field_name = f"field_focused_X{x_k*1000:.2f}_Z{self.params.acoustic['emission']['Foc']*1000:.2f}"

            # Chemin complet pour sauvegarder le champ
            if fieldDataPath is not None:
                pathField = os.path.join(fieldDataPath, field_name + ".hdr")  # ou ".img" selon ton format
            else:
                pathField = None

            # Si le fichier existe déjà, charge-le
            if pathField is not None and os.path.exists(pathField):
                progress_bar.set_postfix_str(f"Loading field - {field_name} -- Memory used: {memory.percent}%")
                try:
                    focused_wave = FocusedWave(params=self.params, focal_line=x_k, medium=self.medium)
                    focused_wave.load_field(fieldDataPath)  # À adapter selon ta méthode de chargement
                except Exception as e:
                    progress_bar.set_postfix_str(f"Error loading field -> Generating field - {field_name} -- Memory used: {memory.percent}%")
                    focused_wave = FocusedWave(params=self.params, focal_line=x_k, medium=self.medium)
                    focused_wave.generate_field(show_log=show_log)
                    if not os.path.exists(pathField):
                        os.makedirs(os.path.dirname(pathField), exist_ok=True)
                        focused_wave.save_field(fieldDataPath)  # À adapter selon ta méthode de sauvegarde
            # Sinon, génère le champ
            else:
                progress_bar.set_postfix_str(f"Generating field - {field_name} -- Memory used: {memory.percent}%")
                focused_wave = FocusedWave(params=self.params, focal_line=x_k, medium=self.medium)
                focused_wave.generate_field(show_log=show_log)
                if pathField is not None:
                    os.makedirs(os.path.dirname(pathField), exist_ok=True)
                    focused_wave.save_field(fieldDataPath)  # À adapter selon ta méthode de sauvegarde

            # Ajoute le champ à la liste
            listAcousticFields.append(focused_wave)
            progress_bar.set_postfix_str("")

        self.AcousticFields = listAcousticFields

    def reconFocus(self):
        """
        Reconstruction de l'image de la zone focalisée à partir des champs acoustiques et des signaux AO.
        Place les signaux AO côte à côte, puis redimensionne pour obtenir une image (X, Z).

        Returns:
            np.ndarray: Image reconstruite de dimensions (X, Z).
        """
        # --- 1. Récupération des signaux AO (ex: self.signals_AO) ---
        # Supposons que self.signals_AO est une liste de signaux 1D (un par position focale)
        # Chaque signal AO est de longueur Nt (nombre d'échantillons temporels)
        if not hasattr(self, 'signals_AO') or self.signals_AO is None:
            raise ValueError("Les signaux AO ne sont pas initialisés.")

        # --- 2. Concaténation des signaux AO côte à côte ---
        # Stack les signaux verticalement pour former une image (X, Time)
        ao_signals_stacked = np.stack(self.signals_AO, axis=0)  # Shape: (num_focal_positions, Nt)

        # --- 3. Redimensionnement pour obtenir une image (X, Z) ---
        # Détermine les dimensions cibles (X, Z)
        X = self.params.general['Nx']  # Nombre de pixels en X (ex: 400)
        Z = self.params.general['Nz']  # Nombre de pixels en Z (ex: 500)

        # Redimensionne avec scipy.ndimage.zoom (conserve l'intégrité des données)
        # Le facteur de zoom est calculé pour passer de Nt à Z
        zoom_factor_y = Z / ao_signals_stacked.shape[1]  # Facteur pour passer de Time à Z
        recon_image = zoom(ao_signals_stacked, (1, zoom_factor_y), order=1)  # order=1 pour interpolation linéaire

        # --- 4. Normalisation (optionnel) ---
        recon_image = (recon_image - np.min(recon_image)) / (np.max(recon_image) - np.min(recon_image) + 1e-9)

        return recon_image


        

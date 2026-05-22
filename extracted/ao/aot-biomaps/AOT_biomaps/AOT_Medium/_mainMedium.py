from abc import abstractmethod
import os
import numpy as np
import warnings

# Optional matplotlib import for visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Optional kwave imports
try:
    from kwave.kgrid import kWaveGrid
    from kwave.kmedium import kWaveMedium
    KWAVE_AVAILABLE = True
except ImportError:
    KWAVE_AVAILABLE = False


class Medium:
    
    def __init__(self, params):
        self.params = params
        self.medium = None
        self.factorX = None
        self.factorZ = None
        self.factorT = None
        self.c_mean = None
        self.Nx_reshaped = None
        self.Nz_reshaped = None
        self.dx_reshaped = None
        self.medium_properties = None

        if KWAVE_AVAILABLE:
            self.kgrid = kWaveGrid([self.params.general["Nx"], self.params.general["Nz"]], 
                                   [self.params.general["dx"], self.params.general["dz"]])

            if self.params.acoustic['f_AQ'] is None:
                self.kgrid.makeTime(self.params.acoustic['medium']['c0'])
                self.params.acoustic['f_AQ'] = int(1/self.kgrid.dt)
            else:
                if self.params.general['Nt'] is None or self.params.general['Nt'] == "None":
                    Nt = int(1.25*np.ceil((self.params.general['Zrange'][1] - self.params.general['Zrange'][0])*float(self.params.acoustic['f_AQ']) / self.params.acoustic['medium']['c0']))
                    self.params.general['Nt'] = Nt
                else:
                    Nt = self.params.general['Nt']
                self.kgrid.setTime(Nt, 1/float(self.params.acoustic['f_AQ']))
            self.Nt_reshaped = self.kgrid.Nt
        else:
            self.kgrid = None
            self.Nt_reshaped = self.params.general.get('Nt', 100)
            warnings.warn("kWave is not available. Using default values for grid parameters.", UserWarning)

    @abstractmethod
    def generate_medium(self):
        """
        Abstract method to generate the medium properties.
        This method should be implemented by subclasses.
        """
        pass

    def save_medium(self, folderPath, fileName="medium"):
        """
        Save the entire medium properties to a .npy file.
        Universally handles any subclass (PVAMedium, BubbleMedium, etc.)
        """
        if os.path.splitext(fileName)[1]:
            raise ValueError("The fileName should not contain an extension; .npy will be added automatically.")
        
        os.makedirs(folderPath, exist_ok=True)
        filePath = os.path.join(folderPath, fileName + '.npy')
        
        if os.path.isdir(filePath):
            raise IsADirectoryError(f"Cannot save medium: {filePath} is a directory.")
        
        state_to_save = {}
        kmedium_data = {}
        
        # 1. On sauvegarde l'empreinte de la classe enfant (ex: "PVAMedium")
        state_to_save['__class_name__'] = self.__class__.__name__
        
        for key, value in self.__dict__.items():
            if key == 'kgrid':
                continue
            elif key == 'kmedium':
                if value is not None:
                    kmedium_data['sound_speed'] = getattr(value, 'sound_speed', None)
                    kmedium_data['density'] = getattr(value, 'density', None)
                    kmedium_data['alpha_coeff'] = getattr(value, 'alpha_coeff', None)
                    kmedium_data['alpha_mode'] = getattr(value, 'alpha_mode', None)
                    kmedium_data['BonA'] = getattr(value, 'BonA', None) # Spécifique à vos sous-classes
                continue
            else:
                state_to_save[key] = value
                
        state_to_save['__kmedium_data__'] = kmedium_data
        np.save(filePath, state_to_save, allow_pickle=True)

    def load_medium(self, folderPath, fileName="medium", isAbsorbingMedium=None):
        """
        Load the medium properties from a .npy file for ANY subclass.
        Rebuilds kWave objects by injecting saved physical tensors directly 
        into their constructors.
        """
        if os.path.splitext(fileName)[1]:
            raise ValueError("The fileName should not contain an extension; .npy will be added automatically.")
        
        filePath = os.path.join(folderPath, fileName + '.npy')
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"The file {filePath} does not exist.")
        
        loaded_state = np.load(filePath, allow_pickle=True).item()
        
        # 1. Vérification de cohérence du type
        saved_class = loaded_state.pop('__class_name__', 'Medium')
        if saved_class != self.__class__.__name__ and saved_class != 'Medium':
            warnings.warn(f"Attention : Vous chargez un fichier généré par '{saved_class}' dans une instance de '{self.__class__.__name__}'.", UserWarning)

        kmedium_data = loaded_state.pop('__kmedium_data__', {})
        
        # 2. Restauration dynamique (Restaure medium_properties, params, factorX, c_mean, etc.)
        self.__dict__.update(loaded_state)
        
        # 3. Reconstruction des objets k-Wave
        if KWAVE_AVAILABLE and hasattr(self, 'params'):
            # Reconstruction de kgrid
            self.kgrid = kWaveGrid([self.params.general["Nx"], self.params.general["Nz"]], 
                                   [self.params.general["dx"], self.params.general["dz"]])
            
            if getattr(self, 'Nt_reshaped', None) is not None and 'f_AQ' in self.params.acoustic:
                self.kgrid.setTime(self.Nt_reshaped, 1/float(self.params.acoustic['f_AQ']))
            
            # Reconstruction rigoureuse de kmedium par dépaquetage
            # On ne garde que les paramètres valides pour éviter de passer des None au constructeur
            kmedium_kwargs = {k: v for k, v in kmedium_data.items() if v is not None}
            
            # kWaveMedium exige au moins sound_speed. S'il n'est pas dans les données, 
            # c'est que l'objet sauvegardé n'avait pas de kmedium initialisé.
            if 'sound_speed' in kmedium_kwargs:
                self.kmedium = kWaveMedium(**kmedium_kwargs)
            else:
                self.kmedium = None
        else:
            self.kgrid = None
            self.kmedium = None

        # 4. Gestion de l'absorption
        if isAbsorbingMedium is not None:
            self.params.acoustic['medium']['isAbsorbingMedium'] = isAbsorbingMedium
            
        if self.params.acoustic['medium']['isAbsorbingMedium']:
            print("[AOT-biomaps] Info: The loaded medium is set to be absorbing.")
        else:
            if KWAVE_AVAILABLE and getattr(self, 'kmedium', None) is not None:
                self.kmedium.alpha_coeff = np.zeros((self.Nx_reshaped, self.Nz_reshaped), dtype=np.float32)
                self.kmedium.alpha_mode = 'no_absorption'
            print("[AOT-biomaps] Info: The loaded medium is set to be non-absorbing.")
            
    def plot_medium_properties(self, figsize=(12, 5),vmin_speed=None, vmax_speed=None, vmin_density=None, vmax_density=None):
        if not KWAVE_AVAILABLE:
            warnings.warn("kWave is not available. Cannot plot medium properties.", UserWarning)
            return
        
        if not MATPLOTLIB_AVAILABLE:
            warnings.warn("matplotlib is not available. Cannot plot medium properties.", UserWarning)
            return
        
        if getattr(self, 'kmedium', None) is None:
            raise ValueError("Medium properties are not available. Please generate or load the medium first.")
            
        if vmin_speed is None:
            vmin_speed = np.min(self.kmedium.sound_speed)
        if vmax_speed is None:
            vmax_speed = np.max(self.kmedium.sound_speed)
        if vmin_density is None:
            vmin_density = np.min(self.kmedium.density)
        if vmax_density is None:
            vmax_density = np.max(self.kmedium.density)
            
        extent = [self.params.general['Xrange'][0]*1e3, self.params.general['Xrange'][1]*1e3, 
                  self.params.general['Zrange'][1]*1e3, self.params.general['Zrange'][0]*1e3]
        
        plt.figure(figsize=figsize)
        plt.subplot(121)
        plt.imshow(self.kmedium.sound_speed.T, vmin=vmin_speed, vmax=vmax_speed, cmap='autumn', extent=extent)
        plt.title('Sound speed map (m/s)')
        plt.xlabel('X (mm)')
        plt.ylabel('Z (mm)')
        plt.colorbar()
        
        plt.subplot(122)
        plt.imshow(self.kmedium.density.T, vmin=vmin_density, vmax=vmax_density, cmap='summer', extent=extent)
        plt.title('Density map (kg/m^3)')
        plt.xlabel('X (mm)')
        plt.ylabel('Z (mm)')
        plt.colorbar()
        plt.tight_layout()
        plt.show()
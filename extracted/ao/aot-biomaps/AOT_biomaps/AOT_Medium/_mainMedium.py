from abc import abstractmethod
import os
from joblib import dump, load
from kwave.kgrid import kWaveGrid
from math import ceil
import numpy as np
import matplotlib.pyplot as plt

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

        self.kgrid = kWaveGrid([self.params.general["Nx"], self.params.general["Nz"]], [self.params.general["dx"], self.params.general["dz"]])

        if self.params.acoustic['f_AQ'] == None:
            self.kgrid.makeTime(self.params.acoustic['medium']['c0'])
            self.params.acoustic['f_AQ'] = int(1/self.kgrid.dt)
        else:
            if self.params.general['Nt'] is None or self.params.general['Nt'] == "None":
                Nt = ceil((self.params.general['Zrange'][1] - self.params.general['Zrange'][0])*float(self.params.acoustic['f_AQ']) / self.params.acoustic['medium']['c0'])
                self.params.general['Nt'] = Nt
            else:
                Nt = self.params.general['Nt']
            self.kgrid.setTime(Nt,1/float(self.params.acoustic['f_AQ']))
        self.Nt_reshaped = self.kgrid.Nt


    @abstractmethod
    def generate_medium(self):
        """
        Abstract method to generate the medium properties.
        This method should be implemented by subclasses.
        """
        pass

    def save_medium(self, folderPath, fileName = "medium"):
        """
        Save the medium properties to a .joblib file.

        Parameters:
        - folderPath (str): The directory where the .joblib file will be saved.
        - fileName (str): The name of the .joblib file (without extension).
        """
        try:
            os.makedirs(folderPath, exist_ok=True)
            filePath = os.path.join(folderPath, fileName)
            # check if filename ends with an extension
            if not os.path.splitext(fileName)[1]:
                filePath += '.joblib'
            else:
                raise ValueError("The fileName should not contain an extension; .joblib will be added automatically.")
            dump(self, filePath)
        except Exception as e:
            print(f"Error in save_medium method: {e}")
            raise
    
    def load_medium(self, folderPath, fileName = "medium"):
        """
        Load the medium properties from a .joblib file.

        Parameters:
        - folderPath (str): The directory where the .joblib file will be loaded from.
        - fileName (str): The name of the .joblib file (without extension).
        """
        try:          
            if not os.path.splitext(fileName)[1]:
                fileName += '.joblib'
            else:
                raise ValueError("The fileName should not contain an extension; .joblib will be added automatically.")
            filePath = os.path.join(folderPath, fileName)
            if os.path.exists(filePath) == False:
                raise FileNotFoundError(f"The file {filePath} does not exist.")
            loaded_obj = load(filePath)
            self.kmedium = loaded_obj.kmedium
            self.factorX = loaded_obj.factorX
            self.factorZ = loaded_obj.factorZ
            self.factorT = loaded_obj.factorT
            self.c_mean = loaded_obj.c_mean
            self.Nx_reshaped = loaded_obj.Nx_reshaped
            self.Nz_reshaped = loaded_obj.Nz_reshaped
            self.dx_reshaped = loaded_obj.dx_reshaped
            self.kgrid = loaded_obj.kgrid
        except Exception as e:
            print(f"Error in load_medium method: {e}")
            raise   

    def plot_medium_properties(self):
        if self.kmedium is None:
            raise ValueError("Medium properties are not available. Please generate or load the medium first.")
        vmin_speed = np.min(self.kmedium.sound_speed)
        vmax_speed = np.max(self.kmedium.sound_speed)
        vmin_density = np.min(self.kmedium.density)
        vmax_density = np.max(self.kmedium.density)
        extent = [self.params.general['Xrange'][0]*1e3, self.params.general['Xrange'][1]*1e3, self.params.general['Zrange'][1]*1e3, self.params.general['Zrange'][0]*1e3]
        plt.figure(figsize=(13,6))
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

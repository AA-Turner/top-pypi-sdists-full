from AOT_biomaps.Config import config

from scipy.signal import hilbert
import os
import h5py
import numpy as np
import torch
from concurrent.futures import ThreadPoolExecutor
from scipy.stats import linregress

def loadmat(param_path_mat):
    """
    Charge un fichier .mat (format HDF5) sans SciPy.
    Args:
        param_path_mat: Chemin vers le fichier .mat.
    Returns:
        Dictionnaire contenant les variables du fichier.
    """
    with h5py.File(param_path_mat, 'r') as f:
        data = {}
        for key in f.keys():
            # Récupère les données et convertit en numpy array si nécessaire
            item = f[key]
            if isinstance(item, h5py.Dataset):
                data[key] = item[()]  # Convertit en numpy array
            elif isinstance(item, h5py.Group):
                # Pour les structures MATLAB (nested)
                data[key] = {}
                for subkey in item:
                    data[key][subkey] = item[subkey][()]
    return data

def reshape_field(field, factor, device=None):
    """
    Downsample a 3D or 4D field using PyTorch interpolation (auto-detects GPU/CPU).
    Args:
        field: Input field (numpy array or torch.Tensor).
        factor: Downsampling factor (tuple of ints).
        device: Force device ('cpu' or 'cuda'). If None, auto-detects GPU.
    Returns:
        Downsampled field (same type as input: numpy array or torch.Tensor).
    """
    # Check input
    if field is None:
        raise ValueError("Acoustic field is not generated. Please generate the field first.")

    # Auto-detect device if not specified
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = device.lower()
        if device not in ['cpu', 'cuda']:
            raise ValueError("Device must be 'cpu' or 'cuda'.")

    # Convert to torch.Tensor if needed
    if isinstance(field, np.ndarray):
        field = torch.from_numpy(field)
    elif not isinstance(field, torch.Tensor):
        raise TypeError("Input must be a numpy array or torch.Tensor.")

    # Move to the target device
    field = field.to(device)

    # Add batch and channel dimensions (required by torch.interpolate)
    if len(factor) == 3:
        if field.dim() != 3:
            raise ValueError("Expected 3D field.")
        field = field.unsqueeze(0).unsqueeze(0)  # (1, 1, D, H, W)

        # Calculate new shape
        new_shape = [
            field.shape[2] // factor[0],
            field.shape[3] // factor[1],
            field.shape[4] // factor[2]
        ]

        # Trilinear interpolation
        downsampled = torch.nn.functional.interpolate(
            field,
            size=new_shape,
            mode='trilinear',
            align_corners=True
        )
        downsampled = downsampled.squeeze(0).squeeze(0)  # Remove batch/channel dims

    elif len(factor) == 4:
        if field.dim() != 4:
            raise ValueError("Expected 4D field.")
        field = field.unsqueeze(0).unsqueeze(0)  # (1, 1, T, D, H, W)

        new_shape = [
            field.shape[2] // factor[0],
            field.shape[3] // factor[1],
            field.shape[4] // factor[2],
            field.shape[5] // factor[3]
        ]

        # Tetra-linear interpolation
        downsampled = torch.nn.functional.interpolate(
            field,
            size=new_shape,
            mode='trilinear',  # PyTorch uses 'trilinear' for both 3D and 4D
            align_corners=True
        )
        downsampled = downsampled.squeeze(0).squeeze(0)

    else:
        raise ValueError("Unsupported dimension. Only 3D and 4D fields are supported.")

    # Convert back to numpy if input was numpy
    if isinstance(field, np.ndarray):
        return downsampled.cpu().numpy()
    else:
        return downsampled.cpu().numpy()

def calculate_envelope_squared(field):
    """
    Calcule l'enveloppe au carré du champ acoustique en utilisant scipy.signal.hilbert (CPU uniquement).

    Args:
        field: Champ acoustique (numpy.ndarray) de forme (T, X, Z) ou (T, X, Y, Z).

    Returns:
        envelope (numpy.ndarray): Enveloppe au carré du champ acoustique.
    """
    try:
        if field is None:
            raise ValueError("Le champ acoustique n'est pas généré. Veuillez d'abord générer le champ.")

        if not isinstance(field, np.ndarray):
            if hasattr(field, 'cpu'):
                field = field.cpu().numpy()  # Si c'est un tenseur PyTorch sur GPU/CPU
            else:
                field = np.array(field)  # Conversion générique

        if len(field.shape) not in [3, 4]:
            raise ValueError("Le champ acoustique doit être un tableau 3D (T, X, Z) ou 4D (T, X, Y, Z).")

        # Calcul de l'enveloppe avec scipy.signal.hilbert
        if len(field.shape) == 3:
            T, X, Z = field.shape
            envelope = np.zeros_like(field)
            for x in range(X):
                for z in range(Z):
                    envelope[:, x, z] = np.abs(hilbert(field[:, x, z], axis=0)) ** 2
        elif len(field.shape) == 4:
            T, X, Y, Z = field.shape
            envelope = np.zeros_like(field)
            for x in range(X):
                for y in range(Y):
                    for z in range(Z):
                        envelope[:, x, y, z] = np.abs(hilbert(field[:, x, y, z], axis=0)) ** 2
                        

        return envelope

    except Exception as e:
        print(f"Erreur dans calculate_envelope_squared: {e}")
        raise

def getPattern(pathFile):
    """
    Get the pattern from a file path.

    Args:
        pathFile (str): Path to the file containing the pattern.

    Returns:
        str: The pattern string.
    """
    try:
        # Pattern between first _ and last _
        pattern = os.path.basename(pathFile).split('_')[1:-1]
        pattern_str = ''.join(pattern)
        return pattern_str
    except Exception as e:
        print(f"Error reading pattern from file: {e}")
        return None
    
def detect_space_0_and_space_1(hex_string):
    binary_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
    
    # Trouver la plus longue séquence de 0 consécutifs
    zeros_groups = [len(s) for s in binary_string.split('1')]
    space_0 = max(zeros_groups) if zeros_groups else 0

    # Trouver la plus longue séquence de 1 consécutifs
    ones_groups = [len(s) for s in binary_string.split('0')]
    space_1 = max(ones_groups) if ones_groups else 0

    return space_0, space_1

def getAngle(pathFile):
    """
    Get the angle from a file path.

    Args:
        pathFile (str): Path to the file containing the angle.

    Returns:
        int: The angle in degrees.
    """
    try:
        # Angle between last _ and .
        angle_str = os.path.basename(pathFile).split('_')[-1].replace('.', '')
        if angle_str.startswith('0'):
            angle_str = angle_str[1:]
        elif angle_str.startswith('1'):
            angle_str = '-' + angle_str[1:]
        else:
            raise ValueError("Invalid angle format in file name.")
        return int(angle_str)
    except Exception as e:
        print(f"Error reading angle from file: {e}")
        return None

def getFrequency(fileName, num_elements, dx):
     
    profile = hex_to_binary_profile(fileName[6:-4], num_elements)

    if set(fileName[6:-4].lower().replace(" ", "")) == {'f'}:
        fs_key = 0.0 # fs_key est en mm^-1 (0.0 mm^-1)
    else:   
        ft_prof = np.fft.fft(profile)
        idx_max = np.argmax(np.abs(ft_prof[1:len(profile)//2])) + 1
        freqs = np.fft.fftfreq(len(profile), d=dx)

        # freqs est en m^-1 car delta_x est en mètres.
        fs_m_inv = abs(freqs[idx_max]) 

        fs_key = fs_m_inv # Fréquence spatiale en mm^-1
    return  int(fs_key / (1/(len(profile)*dx)))

def format_angle(a):
    return f"{'1' if a < 0 else '0'}{abs(int(a)):02d}"
        
def next_power_of_2(n):
    """Calculate the next power of 2 greater than or equal to n."""
    return int(2 ** np.ceil(np.log2(n)))
        
def hex_to_binary_profile(hex_string, n_piezos=192):
    hex_string = hex_string.strip().replace(" ", "").replace("\n", "")
    if set(hex_string.lower()) == {'f'}:
        return np.ones(n_piezos, dtype=int)
    
    try:
        n_char = len(hex_string)
        n_bits = n_char * 4
        binary_str = bin(int(hex_string, 16))[2:].zfill(n_bits)
        if len(binary_str) < n_piezos:
             # Tronquer/padder en fonction de la taille réelle de la sonde
             binary_str = binary_str.ljust(n_piezos, '0') 
        elif len(binary_str) > n_piezos:
             binary_str = binary_str[:n_piezos]
        return np.array([int(b) for b in binary_str])
    except ValueError:
        return np.zeros(n_piezos, dtype=int)
    
def calculate_angle_from_delays(delays, c=1540):
    """
    Calcule l'angle d'incidence θ (en degrés) à partir d'un tableau de 192 retards.
    Utilise une régression linéaire pour estimer la pente des retards.
    Args:
        delays: Tableau de 192 retards (en secondes).
        c: Vitesse du son (m/s).
    Returns:
        theta: Angle en degrés (positif à droite, négatif à gauche).
    """
    pitch = 0.2e-3  # Espacement entre éléments (m)
    x = np.linspace(-(192-1)/2 * pitch, (192-1)/2 * pitch, 192)  # Positions des éléments (m)

    # Régression linéaire pour estimer la pente (sinθ / c)
    slope, _, _, _, _ = linregress(x, delays)

    # Calcul de l'angle (en degrés)
    theta = np.rad2deg(np.arcsin(slope * c))

    # Déterminer le signe en fonction de la position du retard maximal
    max_index = np.argmax(delays)
    if max_index < 95:  # Gauche
        theta = -abs(theta)
    elif max_index > 95:  # Droite
        theta = abs(theta)
    else:  # Centre (θ ≈ 0)
        theta = 0.0

    return int(np.round(theta,0))


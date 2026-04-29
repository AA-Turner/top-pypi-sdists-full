import numpy as np
from itertools import groupby

def calc_mat_os(xm, fx, bool_active_list, signal_type):
    """
    xm : vecteur des positions réelles des éléments (en m)
    fx : fréquence spatiale (en m^-1)
    signal_type : 'cos' ou 'sin'
    """
    num_els = len(xm)
    num_cols = bool_active_list.shape[1]

    if signal_type == 'cos':
        mask = (np.cos(2 * np.pi * fx * xm) > 0).astype(float)
    elif signal_type == 'sin':
        mask = (np.sin(2 * np.pi * fx * xm) > 0).astype(float)
    else:
        mask = np.ones(num_els)  # Sécurité

    return np.tile(mask[:, np.newaxis], (1, num_cols))

def convert_to_hex_list(matrix):
    """
    Convertit une matrice binaire en liste de strings hexa (paquets de 4 bits).
    Chaque colonne devient une chaîne de caractères.
    """
    n_els, n_scans = matrix.shape
    
    # 1. Padding pour s'assurer que n_els est multiple de 4
    remainder = n_els % 4
    if remainder != 0:
        padding = np.zeros((4 - remainder, n_scans))
        matrix = np.vstack([matrix, padding])
    
    # 2. Reshape pour isoler des blocs de 4 bits (nibbles)
    # Shape résultante : (Nombre de blocs, 4 bits, Nombre de scans)
    blocks = matrix.reshape(-1, 4, n_scans)
    
    # 3. Calcul de la valeur décimale de chaque bloc (0 à 15)
    # On considère le premier élément comme le bit de poids faible (LSB)
    weights = np.array([1, 2, 4, 8]).reshape(1, 4, 1)
    dec_values = np.sum(blocks * weights, axis=1).astype(int)
    
    # 4. Conversion en caractères Hexadécimaux
    # On définit la table de conversion pour la rapidité
    hex_table = np.array(list("0123456789abcdef"))
    hex_matrix = hex_table[dec_values]
    
    # 5. Assemblage des chaînes (de l'élément N vers 0 pour l'ordre Shift Register standard)
    return ["".join(hex_matrix[::-1, col]) for col in range(n_scans)]

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
    
def binary_to_hex_profile(bits):
    bit_string = ''.join(str(b) for b in bits)
    bit_string = bit_string.zfill(len(bits))
    hex_string = ''.join([f"{int(bit_string[i:i+4], 2):x}" for i in range(0, len(bit_string), 4)])
    return hex_string

def get_phase_deterministic(profile):
    """
    Détermine la phase en se basant sur la valeur initiale (0 ou 1) et l'état
    de décalage (is_shifted) de la séquence binaire.
    
    ATTENTION: Cette fonction est conservée mais la logique est souvent simplifiée
    en pratique si les labels garantissent les phases 0, pi/2, pi, 3pi/2.
    """
    runs = [(k, sum(1 for _ in g)) for k, g in groupby(profile)]
    if not runs: return 0.0
    
    nominal_half_period = max([r[1] for r in runs]) 
    if nominal_half_period == 0: return 0.0

    first_val = runs[0][0] # 0 ou 1
    first_len = runs[0][1] 
    # Détection de cycle 50%
    is_shifted = (0.3 < first_len / nominal_half_period < 0.7) 
    
    # --- LOGIQUE DE MAPPAGE DE PHASE SIMPLIFIÉE (idx 1 à 4) ---
    
    if first_val == 0: 
        if is_shifted:
            idx = 3 # C1/C3 décalé (phi_1 ou phi_3)
        else:
            idx = 4 # C2/C4 non décalé
    else: # first_val == 1
        if is_shifted:
            idx = 1 # C1/C3 décalé (phi_1 ou phi_3)
        else:
            idx = 2 # C2/C4 non décalé

    # On utilise les phases de quadrature 0, pi/2, pi, 3pi/2 
    if idx == 1:
        phase = 0
    elif idx == 2 :
        phase = np.pi/2
    elif idx == 3 :
        phase = np.pi
    elif idx == 4 :
        phase = 3*np.pi/2
            
    return phase

def add_sincos_cpu(R, decimation, theta):
    decimation = np.asarray(decimation)
    theta = np.asarray(theta)

    ScanParam = np.stack([decimation, theta], axis=1)
    uniq, ia, ib = np.unique(ScanParam, axis=0, return_index=True, return_inverse=True)

    theta_u = uniq[:,1]
    decim_u = uniq[:,0]

    theta0 = np.unique(theta_u)
    N0 = len(theta0)

    Rg = np.asarray(R)
    Nz = Rg.shape[0]
    Nk = N0 + (Rg.shape[1] - N0)//4

    Iout = np.zeros((Nz, Nk), dtype=np.complex64)
    # fx = 0 (onde plane)
    Iout[:, :N0] = Rg[:, :N0]

    k = N0
    for i in range(N0, len(ia)):
        idx = np.where(ib == i)[0]
        h1, h2, h3, h4 = Rg[:, idx].T
        Iout[:, k] = ((h1 - h2) - 1j*(h3 - h4)) / 2
        k += 1

    return Iout, theta_u, decim_u


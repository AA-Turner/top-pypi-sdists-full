import numpy as np

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



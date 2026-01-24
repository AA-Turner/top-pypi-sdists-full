import os
from AOT_biomaps.AOT_Recon.AOT_SparseSMatrix import SparseSMatrix_CSR, SparseSMatrix_SELL
import torch
import numpy as np
import pycuda.driver as drv
from numba import njit, prange
from torch_sparse import coalesce
from scipy.signal.windows import hann
from itertools import groupby
import cupy as cp
from cupyx.scipy.ndimage import map_coordinates

def load_recon(hdr_path):
    """
    Lit un fichier Interfile (.hdr) et son fichier binaire (.img) pour reconstruire une image comme le fait Vinci.
    
    Paramètres :
    ------------
    - hdr_path : chemin complet du fichier .hdr
    
    Retour :
    --------
    - image : tableau NumPy contenant l'image
    - header : dictionnaire contenant les métadonnées du fichier .hdr
    """
    header = {}
    with open(hdr_path, 'r') as f:
        for line in f:
            if ':=' in line:
                key, value = line.split(':=', 1)  # s'assurer qu'on ne coupe que la première occurrence de ':='
                key = key.strip().lower().replace('!', '')  # Nettoyage des caractères
                value = value.strip()
                header[key] = value
    
    # 📘 Obtenez le nom du fichier de données associé (le .img)
    data_file = header.get('name of data file')
    if data_file is None:
        raise ValueError(f"Impossible de trouver le fichier de données associé au fichier header {hdr_path}")
    
    img_path = os.path.join(os.path.dirname(hdr_path), data_file)
    
    # 📘 Récupérer la taille de l'image à partir des métadonnées
    shape = [int(header[f'matrix size [{i}]']) for i in range(1, 4) if f'matrix size [{i}]' in header]
    if shape and shape[-1] == 1:  # Si la 3e dimension est 1, on la supprime
        shape = shape[:-1]  # On garde (192, 240) par exemple
    
    if not shape:
        raise ValueError("Impossible de déterminer la forme de l'image à partir des métadonnées.")
    
    # 📘 Déterminez le type de données à utiliser
    data_type = header.get('number format', 'short float').lower()
    dtype_map = {
        'short float': np.float32,
        'float': np.float32,
        'int16': np.int16,
        'int32': np.int32,
        'uint16': np.uint16,
        'uint8': np.uint8
    }
    dtype = dtype_map.get(data_type)
    if dtype is None:
        raise ValueError(f"Type de données non pris en charge : {data_type}")
    
    # 📘 Ordre des octets (endianness)
    byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
    endianess = '<' if 'little' in byte_order else '>'
    
    # 📘 Vérifie la taille réelle du fichier .img
    img_size = os.path.getsize(img_path)
    expected_size = np.prod(shape) * np.dtype(dtype).itemsize
    
    if img_size != expected_size:
        raise ValueError(f"La taille du fichier img ({img_size} octets) ne correspond pas à la taille attendue ({expected_size} octets).")
    
    # 📘 Lire les données binaires et les reformater
    with open(img_path, 'rb') as f:
        data = np.fromfile(f, dtype=endianess + np.dtype(dtype).char)
    
    image =  data.reshape(shape[::-1]) 
    
    # 📘 Rescale l'image si nécessaire
    rescale_slope = float(header.get('data rescale slope', 1))
    rescale_offset = float(header.get('data rescale offset', 0))
    image = image * rescale_slope + rescale_offset
    
    return image

def mse(y_true, y_pred):
    """
    Calcule la Mean Squared Error (MSE) entre deux tableaux.
    Équivalent à sklearn.metrics.mean_squared_error.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return np.mean((y_true - y_pred) ** 2)

def ssim(img1, img2, win_size=7, k1=0.01, k2=0.03, L=1.0):
    """
    Calcule l'SSIM entre deux images 2D (niveaux de gris).
    Équivalent à skimage.metrics.structural_similarity avec :
    - data_range=1.0 (images normalisées entre 0 et 1)
    - gaussian_weights=True (fenêtre gaussienne)
    - multichannel=False (1 canal)

    Args:
        img1, img2: Images 2D (numpy arrays) de même taille.
        win_size: Taille de la fenêtre de comparaison (doit être impair).
        k1, k2: Constantes pour stabiliser la division (valeurs typiques : 0.01, 0.03).
        L: Dynamique des pixels (1.0 si images dans [0,1], 255 si dans [0,255]).
    Returns:
        SSIM moyen sur l'image (float entre -1 et 1).
    """
    if img1.shape != img2.shape:
        raise ValueError("Les images doivent avoir la même taille.")
    if win_size % 2 == 0:
        raise ValueError("win_size doit être impair.")

    # Constantes
    C1 = (k1 * L) ** 2
    C2 = (k2 * L) ** 2

    # Fenêtre gaussienne
    window = np.ones((win_size, win_size)) / (win_size ** 2)  # Approximation (skimage utilise une gaussienne)
    window = window / np.sum(window)  # Normalisation

    # Pad les images pour éviter les bords
    pad = win_size // 2
    img1_pad = np.pad(img1, pad, mode='reflect')
    img2_pad = np.pad(img2, pad, mode='reflect')

    # Calcul des statistiques locales
    mu1 = np.zeros_like(img1, dtype=np.float64)
    mu2 = np.zeros_like(img1, dtype=np.float64)
    sigma1_sq = np.zeros_like(img1, dtype=np.float64)
    sigma2_sq = np.zeros_like(img1, dtype=np.float64)
    sigma12 = np.zeros_like(img1, dtype=np.float64)

    # Itère sur chaque pixel (optimisé avec des convolutions)
    for i in range(pad, img1_pad.shape[0] - pad):
        for j in range(pad, img1_pad.shape[1] - pad):
            patch1 = img1_pad[i-pad:i+pad+1, j-pad:j+pad+1]
            patch2 = img2_pad[i-pad:i+pad+1, j-pad:j+pad+1]

            mu1[i-pad, j-pad] = np.sum(patch1 * window)
            mu2[i-pad, j-pad] = np.sum(patch2 * window)
            sigma1_sq[i-pad, j-pad] = np.sum(window * (patch1 - mu1[i-pad, j-pad]) ** 2)
            sigma2_sq[i-pad, j-pad] = np.sum(window * (patch2 - mu2[i-pad, j-pad]) ** 2)
            sigma12[i-pad, j-pad] = np.sum(window * (patch1 - mu1[i-pad, j-pad]) * (patch2 - mu2[i-pad, j-pad]))

    # SSIM locale
    ssim_map = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / (
        (mu1**2 + mu2**2 + C1) * (sigma1_sq + sigma2_sq + C2)
    )

    return np.mean(ssim_map)

def calculate_memory_requirement(SMatrix, y):
    """
    Calcule la mémoire requise (en Go) pour :
    - SMatrix : Matrice (np.ndarray, CuPy CSR, SparseSMatrix_CSR ou SparseSMatrix_SELL)
    - y : vecteur (NumPy ou CuPy, float32)

    Args:
        SMatrix: Matrix object (np.ndarray, cpsparse.csr_matrix, SparseSMatrix_CSR, or SparseSMatrix_SELL)
        y: Vector (float32)
    """
    total_bytes = 0

    # --- 1. Memory for SMatrix ---
    
    # 1.1. Custom Sparse Matrix (SELL/CSR)
    if isinstance(SMatrix, (SparseSMatrix_SELL, SparseSMatrix_CSR)):
        # We rely on the getMatrixSize method, which we fixed to track all host/GPU bytes.
        # This is the most reliable way to estimate memory for custom GPU-backed structures.
        try:
            matrix_size_gb = SMatrix.getMatrixSize()
            if isinstance(matrix_size_gb, dict) and 'error' in matrix_size_gb:
                raise ValueError(f"SMatrix allocation error: {matrix_size_gb['error']}")
            
            # Convert GB back to bytes (1 GB = 1024^3 bytes)
            size_SMatrix = matrix_size_gb * (1024 ** 3)
            total_bytes += size_SMatrix
            print(f"SMatrix (Custom Sparse) size: {matrix_size_gb:.3f} GB")

        except AttributeError:
            raise AttributeError("Custom Sparse Matrix must implement the getMatrixSize() method.")
    
    # 1.2. NumPy Dense Array (Standard)
    elif isinstance(SMatrix, np.ndarray):
        # Dense NumPy array (float32)
        size_SMatrix = SMatrix.nbytes
        total_bytes += size_SMatrix
        print(f"SMatrix (NumPy Dense) size: {size_SMatrix / (1024 ** 3):.3f} GB")

    # 1.3. CuPy CSR Matrix (Standard Sparse CuPy)
    # Note: Requires CuPy to be imported, which is usually done outside this function.
    # Assuming 'cpsparse.csr_matrix' is available in the environment if this path is taken.
    elif 'cupy.sparse' in str(type(SMatrix)): # Using string check for type safety outside CuPy context
        # CuPy CSR matrix structure: data (float32), indices (int32), indptr (int32)
        nnz = SMatrix.nnz
        num_rows = SMatrix.shape[0]
        size_data = nnz * 4        # float32 = 4 bytes
        size_indices = nnz * 4     # int32 = 4 bytes
        size_indptr = (num_rows + 1) * 4 # int32 = 4 bytes
        size_SMatrix = size_data + size_indices + size_indptr
        total_bytes += size_SMatrix
        print(f"SMatrix (CuPy CSR) size: {size_SMatrix / (1024 ** 3):.3f} GB")

    else:
        raise ValueError("SMatrix must be a np.ndarray, cpsparse.csr_matrix, or a custom SparseSMatrix object (CSR/SELL).")

    # --- 2. Memory for Vector y ---
    
    # Check if y is a CuPy array or NumPy array (assuming float32 based on docstring)
    if hasattr(y, 'nbytes'):
        size_y = y.nbytes
        total_bytes += size_y
        print(f"Vector y size: {size_y / (1024 ** 3):.3f} GB")
    else:
        # Fallback if object doesn't expose nbytes (e.g., custom buffer), but usually array objects do.
        raise ValueError("Vector y must be an array type exposing the .nbytes attribute.")


    # --- 3. Final Result ---
    return total_bytes / (1024 ** 3)

def check_gpu_memory(device_index, required_memory, show_logs=True):
    """Check if enough memory is available on the specified GPU."""
    free_memory, _ = torch.cuda.mem_get_info(f"cuda:{device_index}")
    free_memory_gb = free_memory / 1024**3
    if show_logs:
        print(f"Free memory on GPU {device_index}: {free_memory_gb:.2f} GB, Required memory: {required_memory:.2f} GB")
    return free_memory_gb >= required_memory

@njit(parallel=True)
def _forward_projection(SMatrix, theta_p, q_p):
    t_dim, z_dim, x_dim, i_dim = SMatrix.shape
    for _t in prange(t_dim):
        for _n in range(i_dim):
            total = 0.0
            for _z in range(z_dim):
                for _x in range(x_dim):
                    total += SMatrix[_t, _z, _x, _n] * theta_p[_z, _x]
            q_p[_t, _n] = total

@njit(parallel=True)
def _backward_projection(SMatrix, e_p, c_p):
    t_dim, z_dim, x_dim, n_dim = SMatrix.shape
    for _z in prange(z_dim):
        for _x in range(x_dim):
            total = 0.0
            for _t in range(t_dim):
                for _n in range(n_dim):
                    total += SMatrix[_t, _z, _x, _n] * e_p[_t, _n]
            c_p[_z, _x] = total

def _build_adjacency_sparse(Z, X, device, corner=(0.5 - np.sqrt(2) / 4) / np.sqrt(2), face=0.5 - np.sqrt(2) / 4,dtype=torch.float32):
    rows, cols, weights = [], [], []
    for z in range(Z):
        for x in range(X):
            j = z * X + x
            for dz, dx in [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),           (0, 1),
                           (1, -1),   (1, 0), (1, 1)]:
                nz, nx = z + dz, x + dx
                if 0 <= nz < Z and 0 <= nx < X:
                    k = nz * X + nx
                    weight = corner if abs(dz) + abs(dx) == 2 else face
                    rows.append(j)
                    cols.append(k)
                    weights.append(weight)
    index = torch.tensor([rows, cols], dtype=torch.long, device=device)
    values = torch.tensor(weights, dtype=dtype, device=device)
    index, values = coalesce(index, values, m=Z*X, n=Z*X)
    return index, values

def power_method(P, PT, data, Z, X, n_it=10):
    x = torch.randn(Z * X, device=data.device)
    x = x / torch.norm(x)
    for _ in range(n_it):
        Ax = P(x)
        ATax = PT(Ax)
        x = ATax / torch.norm(ATax)
    ATax = PT(P(x))
    return torch.sqrt(torch.dot(x, ATax))

def proj_l2(p, alpha):
    if alpha <= 0:
        return torch.zeros_like(p)
    norm = torch.sqrt(torch.sum(p**2, dim=0, keepdim=True) + 1e-12)
    return p * torch.min(norm, torch.tensor(alpha, device=p.device)) / (norm + 1e-12)

def gradient(x):
    grad_x = torch.zeros_like(x)
    grad_y = torch.zeros_like(x)
    grad_x[:, :-1] = x[:, 1:] - x[:, :-1]  # Gradient horizontal
    grad_y[:-1, :] = x[1:, :] - x[:-1, :]   # Gradient vertical
    return torch.stack((grad_x, grad_y), dim=0)

def div(x):
    if x.dim() == 3:
        x = x.unsqueeze(0)  # Ajoute une dimension batch si nécessaire

    gx = x[:, 0, :, :]  # Gradient horizontal (shape: [1, H, W] ou [H, W])
    gy = x[:, 1, :, :]  # Gradient vertical   (shape: [1, H, W] ou [H, W])

    # Divergence du gradient horizontal (gx)
    div_x = torch.zeros_like(gx)
    div_x[:, :, 1:] += gx[:, :, :-1]  # Contribution positive (gauche)
    div_x[:, :, :-1] -= gx[:, :, :-1] # Contribution négative (droite)

    # Divergence du gradient vertical (gy)
    div_y = torch.zeros_like(gy)
    div_y[:, 1:, :] += gy[:, :-1, :]  # Contribution positive (haut)
    div_y[:, :-1, :] -= gy[:, :-1, :] # Contribution négative (bas)

    return -(div_x + div_y)

def norm2sq(x):
    return torch.sum(x**2)

def norm1(x):
    return torch.sum(torch.abs(x))

def KL_divergence(Ax, y):
    return torch.sum(Ax - y * torch.log(Ax + 1e-10))

def gradient_KL(Ax, y):
    return 1 - y / (Ax + 1e-10)

def prox_F_star(y, sigma, a):
    return 0.5 * (y - torch.sqrt(y**2 + 4 * sigma * a))

def prox_G(x, tau, K):
    return torch.clamp(x - tau * K, min=0)

def filter_radon(f, N, filter_type, Fc):
    """
    Implémente les filtres pour la rétroprojection filtrée (iRadon).
    Inspirée de la fonction MATLAB FilterRadon de Mamouna Bocoum.

    Paramètres :
    ------------
    f : np.ndarray
        Vecteur des fréquences (ex: f_t ou f_z).
    N : int
        Taille du filtre (longueur de f).
    filter_type : str
        Type de filtre : 'ram-lak', 'shepp-logan', 'cosine', 'hamming', 'hann'.
    Fc : float
        Fréquence de coupure.

    Retourne :
    -----------
    FILTER : np.ndarray
        Filtre appliqué aux fréquences.
    """
    FILTER = np.abs(f)

    if filter_type == 'ram-lak':
        pass  # FILTER = |f| (déjà calculé)
    elif filter_type == 'shepp-logan':
        # Évite la division par zéro
        with np.errstate(divide='ignore', invalid='ignore'):
            FILTER = FILTER * (np.sinc(2 * f / (2 * Fc)))  # sin(2πf/(2Fc))/(2πf/(4Fc)) = sinc(2f/(2Fc))
        FILTER[np.isnan(FILTER)] = 1.0  # Pour f=0
    elif filter_type == 'cosine':
        FILTER = FILTER * np.cos(2 * np.pi * f / (4 * Fc))
    elif filter_type == 'hamming':
        FILTER = FILTER * (0.54 + 0.46 * np.cos(2 * np.pi * f / Fc))
    elif filter_type == 'hann':
        FILTER = FILTER * (1 + np.cos(2 * np.pi * f / (4 * Fc))) / 2
    else:
        raise ValueError(f"Type de filtre inconnu : {filter_type}")

    # Coupure des fréquences au-delà de Fc
    FILTER[np.abs(f) > Fc] = 0
    # Atténuation exponentielle (optionnelle, comme dans le code MATLAB)
    FILTER = FILTER * np.exp(-2 * (np.abs(f) / Fc)**10)

    return FILTER

def compute_TV_cpu(x, Z, X, isotropic=False):
    """
    Compute total variation of x (1D flattened of shape Z*X).
    isotropic=False -> anisotropic (sum |dx| + |dy|)
    isotropic=True -> isotropic sqrt(dx^2 + dy^2)
    """
    x2d = x.reshape(Z, X)
    dx = np.diff(x2d, axis=1)
    dy = np.diff(x2d, axis=0)
    if isotropic:
        # pad to original size for consistent measure (we only need sum of norms)
        mags = np.sqrt(dx**2 + dy**2)
        return float(np.sum(mags))
    else:
        return float(np.sum(np.abs(dx)) + np.sum(np.abs(dy)))

def get_apodization_vector_gpu(matrix_sparse_obj):
    """
    Génère un vecteur de fenêtrage 2D (Hanning) pour l'apodisation 
    de la matrice système A et le transfère sur le GPU.
    Ce vecteur doit être multiplié par les colonnes de A (pixels Z*X).
    """
    Z = matrix_sparse_obj.Z
    X = matrix_sparse_obj.X
    
    # 1. Génération des fenêtres 1D sur l'axe X et Z
    # Forte apodisation latérale (X) pour cibler l'artefact de bordure.
    fenetre_x = hann(X).astype(np.float32)
    
    # Fenêtre uniforme en profondeur (Z), car l'artefact est surtout latéral.
    fenetre_z = np.ones(Z, dtype=np.float32)
    
    # 2. Création de la matrice de fenêtre 2D (Z, X)
    fenetre_2d = np.outer(fenetre_z, fenetre_x)
    
    # 3. Vectorisation (Z*X)
    fenetre_vectorisee = fenetre_2d.flatten()
    
    # 4. Transfert sur GPU (mémoire contiguë)
    fenetre_gpu = drv.mem_alloc(fenetre_vectorisee.nbytes)
    drv.memcpy_htod(fenetre_gpu, fenetre_vectorisee)
    
    print(f"✅ Vecteur de fenêtrage (Z*X={Z*X}) généré et transféré sur GPU.")
    
    return fenetre_gpu

def _call_axpby(axpby_kernel, out_ptr, x_ptr, y_ptr, a, b, N, stream, block):
    grid = ((int(N) + block - 1) // block, 1, 1)
    axpby_kernel(out_ptr, x_ptr, y_ptr,
                    np.float32(a), np.float32(b),
                    np.int32(N),
                    block=(block, 1, 1), grid=grid, stream=stream)

def _call_minus_axpy(minus_kernel, out_ptr, z_ptr, a, N, stream, block):
    grid = ((int(N) + block - 1) // block, 1, 1)
    minus_kernel(out_ptr, z_ptr, np.float32(a), np.int32(N),
                    block=(block, 1, 1), grid=grid, stream=stream)

def power_method_estimate_L__SELL(SMatrix, stream, n_it=20, block_size=256):
    """Estimate ||A||^2 using power method (uses your projection/backprojection kernels)."""
    TN = int(SMatrix.N * SMatrix.T)
    ZX = int(SMatrix.Z * SMatrix.X)
    proj = SMatrix.sparse_mod.get_function("projection_kernel__SELL")
    back = SMatrix.sparse_mod.get_function("backprojection_kernel__SELL")
    TN_i = np.int32(TN)
    ZX_i = np.int32(ZX)
    slice_h = np.int32(SMatrix.slice_height)
    grid_rows = ((TN + block_size - 1) // block_size, 1, 1)
    block_1D = (block_size, 1, 1)

    dtype = np.float32
    x_host = np.random.randn(ZX).astype(dtype)
    x_host /= np.linalg.norm(x_host) + 1e-12
    x_gpu = drv.mem_alloc(x_host.nbytes)
    drv.memcpy_htod_async(x_gpu, x_host, stream)
    q_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
    ATq_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
    ATq_host = np.empty(ZX, dtype=dtype)

    for _ in range(n_it):
        proj(q_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                x_gpu, TN_i, slice_h, block=block_1D, grid=grid_rows, stream=stream)
        drv.memset_d32_async(ATq_gpu, 0, ZX, stream)
        back(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                q_gpu, ATq_gpu, TN_i, slice_h, block=block_1D, grid=grid_rows, stream=stream)
        stream.synchronize()
        drv.memcpy_dtoh(ATq_host, ATq_gpu)
        norm = np.linalg.norm(ATq_host)
        if norm < 1e-12:
            break
        x_host = ATq_host / norm
        drv.memcpy_htod_async(x_gpu, x_host, stream)
    # final Rayleigh quotient
    proj(q_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
            x_gpu, TN_i, slice_h, block=block_1D, grid=grid_rows, stream=stream)
    drv.memset_d32_async(ATq_gpu, 0, ZX, stream)
    back(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
            q_gpu, ATq_gpu, TN_i, slice_h, block=block_1D, grid=grid_rows, stream=stream)
    stream.synchronize()
    drv.memcpy_dtoh(ATq_host, ATq_gpu)
    L_sq = float(np.dot(x_host, ATq_host))
    for g in (x_gpu, q_gpu, ATq_gpu):
        try:
            g.free()
        except:
            pass
    return max(L_sq, 1e-6)

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

def fourierz_gpu(z, X):
    dz = float(z[1] - z[0])
    Nz = X.shape[0]

    return cp.fft.fftshift(
        cp.fft.fft(
            cp.fft.ifftshift(X, axes=0),
            axis=0
        ),
        axes=0
    ) * (Nz * dz)

def ifourierz_gpu(z, X):
    dz = float(z[1] - z[0])
    Nz = X.shape[0]

    return cp.fft.ifftshift(
        cp.fft.ifft(
            cp.fft.fftshift(X, axes=0),
            axis=0
        ),
        axes=0
    ) * (1 / dz)

def ifourierx_gpu(F_fx_z, dx):
    """
    Inverse Fourier along X (axis=1), Matlab-compatible
    F_fx_z : (Nz, Nx) complex cupy array
    dx : scalar (spacing in x)
    """

    return (
        cp.fft.ifftshift(
            cp.fft.ifft(
                cp.fft.fftshift(F_fx_z, axes=1),
                axis=1
            ),
            axes=1
        ) * (1.0 / dx)
    )

def EvalDelayLawOS_center(X_m, theta, DelayLAWS, ActiveLIST, c):
    """
    Retourne le centre de rotation C pour chaque angle
    X_m : positions des éléments de la sonde
    DelayLAWS : delays en secondes (chaque colonne = angle, chaque ligne = élément)
    ActiveLIST : masque des éléments actifs (1 = actif)
    c : vitesse du son
    """
    Nangle = DelayLAWS.shape[1]
    C = np.zeros((Nangle, 2))
    
    ct = DelayLAWS * c  # convert seconds to distance

    for i in range(Nangle):
        active_idx = np.where(ActiveLIST[:, i] == 1)[0]
        if len(active_idx) == 0:
            continue


        angle_i = np.round(theta[i], 5)
        # unit vector orthogonal to wavefront
        u = np.array([np.sin(angle_i), np.cos(angle_i)])

        # initial positions X0, Z0
        X0 = X_m - u[0] * ct[:, i]
        Z0 = 0 - u[1] * ct[:, i]

        if Z0[-1] - Z0[0] != 0:
            C[i, 0] = (Z0[-1]*X0[0] - Z0[0]*X0[-1]) / (Z0[-1] - Z0[0])
            C[i, 1] = 0

    return C

def rotate_theta_gpu(X, Z, Iin, theta, C):
    """
    GPU equivalent of RotateTheta.m
    X, Z, Iin : cupy arrays (Nz, Nx)
    theta : scalar (float)
    C : (2,) array-like
    """

    # --- Translation ---
    X_rel = X - C[0]
    Z_rel = Z - C[1]

    c = cp.cos(theta)
    s = cp.sin(theta)

    # --- Rotation (Matlab convention) ---
    Xout = c * X_rel + s * Z_rel
    Zout = -s * X_rel + c * Z_rel

    # Back to original frame
    Xout += C[0]
    Zout += C[1]

    # --- Conversion coordonnées -> indices ---
    # Grille régulière supposée
    dx = X[0, 1] - X[0, 0]
    dz = Z[1, 0] - Z[0, 0]

    x0 = X[0, 0]
    z0 = Z[0, 0]

    ix = (Xout - x0) / dx
    iz = (Zout - z0) / dz

    # --- Interpolation bilinéaire GPU ---
    # map_coordinates attend (ndim, Npoints)
    coords = cp.stack([iz.ravel(), ix.ravel()])

    Iout = map_coordinates(
        Iin,
        coords,
        order=1,          # bilinear
        mode='constant',
        cval=0.0
    )

    return Iout.reshape(Iin.shape)

def filter_radon_gpu(fz, Fc):
    FILTER = cp.abs(fz)
    FILTER = cp.where(cp.abs(fz) > Fc, 0, FILTER)
    FILTER *= cp.exp(-2 * cp.abs(fz / Fc)**10)
    return FILTER


import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule
from tqdm import trange
import gc
import os

class SparseSMatrix_CSR:
    """Construction d'une matrice CSR à partir d'un objet `manip`.
    Usage:
        S = SparseMatrixGPU(manip)
        S.allocate()
    Après allocate(), on a: row_ptr (host np.int64 array), row_ptr_gpu (device ptr),
    h_col_ind, h_values, col_ind_gpu, values_gpu, norm_factor_inv.
    """

    def __init__(self, manip, block_rows=64, relative_threshold=0.3, device=0):
        drv.init()
        self.device = drv.Device(device)
        self.ctx = self.device.make_context()
        self.manip = manip
        self.N = len(manip.AcousticFields)
        self.T = manip.AcousticFields[0].field.shape[0]
        self.Z = manip.AcousticFields[0].field.shape[1]
        self.X = manip.AcousticFields[0].field.shape[2]
        self.block_rows = block_rows
        self.relative_threshold = relative_threshold
        
        # --- FIX: Résolution du chemin du .cubin (dans AOT_Recon/) ---
        # Le fichier SparseSMatrix_CSR.py est dans AOT_Recon/AOT_SparseSMatrix/
        # On remonte d'un répertoire pour atteindre AOT_Recon/
        cubin_parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.module_path = os.path.join(cubin_parent_dir, "AOT_biomaps_kernels.cubin")
        # --- FIN FIX ---

        self.h_dense = None
        self.row_ptr = None
        self.row_ptr_gpu = None
        self.h_col_ind = None
        self.h_values = None
        self.total_nnz = 0
        self.norm_factor_inv = None
        self.sparse_mod = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.free()

    def load_precompiled_module(self):
        """
        Charge le module CUDA pré-compilé (.cubin) en utilisant le chemin résolu.
        Supprime la logique de compilation JIT.
        """
        so_path = self.module_path # Utilise le chemin résolu dans __init__

        if not os.path.exists(so_path):
            raise FileNotFoundError(
                f"Le module CUDA {os.path.basename(so_path)} est introuvable au chemin: {so_path}. "
                "Assurez-vous qu'il est compilé et bien placé."
            )
            
        try:
            self.sparse_mod = drv.module_from_file(so_path)
            print(f"✅ Module CUDA chargé depuis {so_path}")
        except Exception as e:
             raise RuntimeError(f"Le fichier {os.path.basename(so_path)} a été trouvé, mais PyCUDA n'a pas pu le charger. Vérifiez la compatibilité.") from e

    def estimate_nnz_cpu(self):
        """Estimation rapide (non-exacte) — utile si tu veux une estimation faible.
        Recommandé : utiliser la passe GPU exacte (count_nnz_per_row_kernel) à la place.
        """
        total = 0
        for n in range(self.N):
            field = self.manip.AcousticFields[n].field
            for t in range(self.T):
                row = field[t].flatten()
                row_max = np.max(np.abs(row))
                thr = row_max * self.relative_threshold
                total += np.count_nonzero(np.abs(row) > thr)
        return int(total)

    def allocate(self, kernel_module_path=None):
        try:
            # --- 1. Construction bloc par bloc (sans garder tout le dense si possible) ---
            num_rows = self.N * self.T
            num_cols = self.Z * self.X
            bytes_float = np.dtype(np.float32).itemsize

            # Charge module
            # FIX: Toujours charger depuis self.module_path (résolu)
            self.load_precompiled_module() 

            count_nnz_kernel = self.sparse_mod.get_function('count_nnz_rows_kernel')
            fill_csr_kernel = self.sparse_mod.get_function('fill_kernel__CSR')

            # allocate host row_ptr
            self.row_ptr = np.zeros(num_rows + 1, dtype=np.int64)

            # GPU temp buffers
            dense_block_host = np.empty((self.block_rows, num_cols), dtype=np.float32)
            dense_block_gpu = drv.mem_alloc(self.block_rows * num_cols * bytes_float)
            row_nnz_gpu = drv.mem_alloc(self.block_rows * np.dtype(np.int32).itemsize)

            block_size = 128

            # --- Count NNZ per row using GPU kernel to be consistent with filling logic ---
            for b in trange(0, num_rows, self.block_rows, desc='Comptage NNZ'):
                current_rows = min(self.block_rows, num_rows - b)
                # Fill dense_block_host from manip
                for r in range(current_rows):
                    global_row = b + r
                    n_idx = global_row // self.T
                    t_idx = global_row % self.T
                    dense_block_host[r, :] = self.manip.AcousticFields[n_idx].field[t_idx].flatten()
                drv.memcpy_htod(dense_block_gpu, dense_block_host)

                grid = ((current_rows + block_size - 1) // block_size, 1, 1)
                # Note: Assuming 'count_nnz_per_row_kernel' is the correct name (verified by user in prior steps)
                count_nnz_kernel(dense_block_gpu, row_nnz_gpu,
                                 np.int32(current_rows), np.int32(num_cols),
                                 np.float32(self.relative_threshold),
                                 block=(block_size, 1, 1), grid=grid)

                row_nnz_host = np.empty(current_rows, dtype=np.int32)
                drv.memcpy_dtoh(row_nnz_host, row_nnz_gpu)
                self.row_ptr[b + 1:b + current_rows + 1] = self.row_ptr[b] + np.cumsum(row_nnz_host, dtype=np.int64)

            # total nnz
            self.total_nnz = int(self.row_ptr[-1])
            print(f"NNZ total : {self.total_nnz}")

            # allocate final arrays
            self.h_col_ind = np.zeros(self.total_nnz, dtype=np.uint32)
            self.h_values = np.zeros(self.total_nnz, dtype=np.float32)

            # copy row_ptr to device once
            self.row_ptr_gpu = drv.mem_alloc(self.row_ptr.nbytes)
            drv.memcpy_htod(self.row_ptr_gpu, self.row_ptr)

            # allocate device arrays for final csr
            self.col_ind_gpu = drv.mem_alloc(self.h_col_ind.nbytes)
            self.values_gpu = drv.mem_alloc(self.h_values.nbytes)

            # --- Fill CSR per-block ---
            for b in trange(0, num_rows, self.block_rows, desc='Remplissage CSR'):
                current_rows = min(self.block_rows, num_rows - b)
                for r in range(current_rows):
                    global_row = b + r
                    n_idx = global_row // self.T
                    t_idx = global_row % self.T
                    dense_block_host[r, :] = self.manip.AcousticFields[n_idx].field[t_idx].flatten()
                drv.memcpy_htod(dense_block_gpu, dense_block_host)

                grid = ((current_rows + block_size - 1) // block_size, 1, 1)
                fill_csr_kernel(dense_block_gpu,
                                self.row_ptr_gpu,
                                self.col_ind_gpu,
                                self.values_gpu,
                                np.int32(b),
                                np.int32(current_rows),
                                np.int32(num_cols),
                                np.float32(self.relative_threshold),
                                np.int64(self.total_nnz),
                                block=(block_size, 1, 1), grid=grid)
                drv.Context.synchronize()

            # copy back
            drv.memcpy_dtoh(self.h_col_ind, self.col_ind_gpu)
            drv.memcpy_dtoh(self.h_values, self.values_gpu)
            print('CSR généré ✔')

            # compute normalization factor from CSR (sum per column)
            self.compute_norm_factor_from_csr()

            # free temporaries
            dense_block_gpu.free(); row_nnz_gpu.free()

        except Exception as e:
            print(f"❌ Erreur détaillée : {e}")
            self.free()
            raise

    def compute_norm_factor_from_csr(self):
        ZX = self.Z * self.X

        # 1) Allouer un vecteur de somme colonne sur le GPU
        col_sum_gpu = drv.mem_alloc(ZX * np.dtype(np.float32).itemsize)
        drv.memset_d32(col_sum_gpu, 0, ZX)

        # 2) Récupérer le kernel
        # FIX: Utiliser le nom générique 'accumulate_columns_atomic' comme dans SELL (si le binaire est partagé)
        # Si le développeur utilise la convention __CSR, on la garde.
        # Basé sur notre historique SELL, le nom est probablement générique 'accumulate_columns_atomic'.
        # Je vais supposer que le nom est générique pour éviter une LogicError ici aussi.
        acc_kernel = self.sparse_mod.get_function("accumulate_columns_atomic") 

        # 3) Lancer le kernel
        threads = 256
        blocks = (self.total_nnz + threads - 1) // threads

        acc_kernel(
            self.values_gpu,
            self.col_ind_gpu,
            np.int64(self.total_nnz),
            col_sum_gpu,
            block=(threads,1,1),
            grid=(blocks,1,1)
        )
        drv.Context.synchronize()

        # 4) Récupérer le résultat
        norm = np.empty(ZX, dtype=np.float32)
        drv.memcpy_dtoh(norm, col_sum_gpu)
        col_sum_gpu.free()

        norm = np.maximum(norm.astype(np.float64), 1e-6)
        self.norm_factor_inv = (1.0 / norm).astype(np.float32)

        self.norm_factor_inv_gpu = drv.mem_alloc(self.norm_factor_inv.nbytes)
        drv.memcpy_htod(self.norm_factor_inv_gpu, self.norm_factor_inv)

    def getMatrixSize(self):
        """
        Retourne la taille totale de la matrice CSR en Go (en sommant la mémoire GPU).
        Utilise les attributs de taille stockés pour contourner l'AttributeError de DeviceAllocation.
        """
        # Note: L'utilisateur doit s'assurer que self.row_ptr existe avant cet appel.
        if self.row_ptr is None:
            return {"error": "La matrice sparse n'est pas encore allouée."}
            
        total_bytes = 0

        # Somme des tailles stockées (Taille calculée et attribuée dans allocate et compute_norm_factor_from_csr)
        total_bytes += getattr(self, 'row_ptr_gpu_size', 0)
        total_bytes += getattr(self, 'col_ind_gpu_size', 0)
        total_bytes += getattr(self, 'values_gpu_size', 0)
        total_bytes += getattr(self, 'norm_factor_inv_gpu_size', 0)
        
        return total_bytes / (1024**3)

    def free(self):
        try:
            if hasattr(self, 'col_ind_gpu') and self.col_ind_gpu:
                self.col_ind_gpu.free()
            if hasattr(self, 'values_gpu') and self.values_gpu:
                self.values_gpu.free()
            if hasattr(self, 'row_ptr_gpu') and self.row_ptr_gpu:
                self.row_ptr_gpu.free()
            if hasattr(self, 'norm_factor_inv_gpu') and self.norm_factor_inv_gpu:
                self.norm_factor_inv_gpu.free()
            if hasattr(self, 'ctx') and self.ctx:
                try:
                    self.ctx.pop()
                except Exception:
                    pass
                self.ctx = None
            print('✅ Mémoire GPU libérée.')
        except Exception as e:
            print(f"❌ Erreur lors de la libération de la mémoire GPU : {e}")
        
    def compute_density(self):
        """
        Retourne la densité réelle de la CSR = NNZ / (num_rows * num_cols)
        Nécessite que self.h_values et self.row_ptr existent (host).
        """
        if self.row_ptr is None or self.h_values is None:
            raise RuntimeError("row_ptr et h_values requis pour calculer la densité")
        num_rows = int(self.N * self.T)
        num_cols = int(self.Z * self.X)
        total_nnz = int(self.row_ptr[-1])
        density = total_nnz / (num_rows * num_cols)
        return density
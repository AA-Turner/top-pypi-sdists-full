import pycuda.driver as drv
import numpy as np
from tqdm import trange
import os
import gc

class SparseSMatrix_SELL:
    def __init__(self, manip, block_rows=64, relative_threshold=0.3, device=0,
                 module_path="AOT_biomaps_kernels.cubin", slice_height=32):
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
        
        # --- PATH RESOLUTION FIX ---
        # The cubin file is located in the parent directory (AOT_Recon/)
        # We use os.path.dirname(os.path.dirname(__file__)) to go up one directory level.
        cubin_parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.module_path = os.path.join(cubin_parent_dir, module_path)
        # --- END FIX ---
        
        self.slice_height = slice_height

        # SELL arrays (device) & Size Tracking (CRITICAL FIX: Initialized attributes)
        self.sell_values_gpu = None
        self.sell_colinds_gpu = None
        self.slice_ptr = None
        self.slice_len = None
        self.slice_ptr_gpu = None
        self.slice_len_gpu = None
        
        # Attributes to store allocated size in bytes (bypassing the problematic .size attribute)
        self.sell_values_gpu_size = 0  
        self.sell_colinds_gpu_size = 0 
        self.slice_ptr_gpu_size = 0    
        self.slice_len_gpu_size = 0    

        self.total_storage = 0

        self.norm_factor_inv = None
        self.norm_factor_inv_gpu = None
        self.norm_factor_inv_gpu_size = 0

        self.sparse_mod = None
        self.load_module()

    def load_module(self):
        """Loads the pre-compiled CUDA module (.cubin file)."""
        
        # Check if the file exists at the calculated absolute path
        if not os.path.exists(self.module_path):
            # The path is now correctly calculated to the parent directory.
            raise FileNotFoundError(f"CUDA module {os.path.basename(self.module_path)} not found at path: {self.module_path}")
            
        # Try to load the module
        try:
            self.sparse_mod = drv.module_from_file(self.module_path)
            print(f"Loaded CUDA module {os.path.basename(self.module_path)}")
        except Exception as e:
            print(f"❌ Error loading CUDA module {os.path.basename(self.module_path)}: {e}")
            raise RuntimeError(f"File {os.path.basename(self.module_path)} was found, but PyCUDA could not load it. Check compatibility.") from e

    def free(self):
        try:
            # Free device allocations
            attrs = ["sell_values_gpu","sell_colinds_gpu","slice_ptr_gpu","slice_len_gpu","norm_factor_inv_gpu"]
            for a in attrs:
                if hasattr(self, a) and getattr(self, a) is not None:
                    getattr(self, a).free()
                    setattr(self, a, None)
            
            # Reset stored sizes
            self.sell_values_gpu_size = 0
            self.sell_colinds_gpu_size = 0
            self.slice_ptr_gpu_size = 0
            self.slice_len_gpu_size = 0
            self.norm_factor_inv_gpu_size = 0
            
            if hasattr(self, 'ctx') and self.ctx:
                try: self.ctx.pop()
                except Exception: pass
                self.ctx = None
        except Exception as e:
            print("Error freeing GPU memory:", e)

    def allocate(self):
        """
        Build SELL-C-σ directly from manip AcousticFields in streaming blocks.
        Corrected: per-block row_nnz copy, zeroing of host block, proper sync.
        """
        if self.sparse_mod is None:
            raise RuntimeError("CUDA module not loaded. Check compilation.")

        count_kernel = self.sparse_mod.get_function("count_nnz_rows_kernel")
        fill_kernel  = self.sparse_mod.get_function("fill_kernel__SELL")

        num_rows = int(self.N * self.T)
        num_cols = int(self.Z * self.X)
        C = int(self.slice_height)

        br = int(self.block_rows)
        dense_host = np.empty((br, num_cols), dtype=np.float32)

        # Allocation dense buffer on device (size = br * num_cols)
        dense_gpu_size = dense_host.nbytes
        dense_gpu  = drv.mem_alloc(dense_gpu_size)

        # 1) count nnz per row (per block)
        row_nnz = np.zeros(num_rows, dtype=np.int32)
        row_nnz_gpu_block_size = br * np.dtype(np.int32).itemsize
        row_nnz_gpu_block = drv.mem_alloc(row_nnz_gpu_block_size)

        block = 128
        for b in trange(0, num_rows, br, desc="Count NNZ per row"):
            R = min(br, num_rows - b)
            # zero the host block to avoid garbage in tail when R < br
            dense_host.fill(0.0)
            for i in range(R):
                rg = b + i
                n_idx = rg // self.T
                t_idx = rg % self.T
                dense_host[i, :] = self.manip.AcousticFields[n_idx].field[t_idx].flatten()
            # copy whole buffer (safe because we zeroed tail)
            drv.memcpy_htod(dense_gpu, dense_host)
            grid = ((R + block - 1) // block, 1, 1)
            count_kernel(dense_gpu, row_nnz_gpu_block, np.int32(R), np.int32(num_cols), np.float32(self.relative_threshold),
                        block=(block,1,1), grid=grid)
            drv.Context.synchronize()
            tmp = np.empty(R, dtype=np.int32)
            drv.memcpy_dtoh(tmp, row_nnz_gpu_block)
            row_nnz[b:b+R] = tmp

        row_nnz_gpu_block.free()
        dense_gpu.free()

        # 2) compute per-slice maxlen and slice_ptr
        num_slices = (num_rows + C - 1) // C
        slice_len = np.zeros(num_slices, dtype=np.int32)
        for s in range(num_slices):
            r0 = s * C
            r1 = min(num_rows, r0 + C)
            slice_len[s] = int(np.max(row_nnz[r0:r1])) if (r1>r0) else 0

        # Vérification de slice_len
        if np.all(slice_len == 0):
            raise ValueError("slice_len contient uniquement des zéros. Vérifie row_nnz.")

        # Calcul de slice_ptr
        slice_ptr = np.zeros(num_slices + 1, dtype=np.int64)
        for s in range(num_slices):
            slice_ptr[s+1] = slice_ptr[s] + (slice_len[s] * C)

        total_storage = int(slice_ptr[-1])
        self.total_storage = total_storage

        # Taille des valeurs (float32) + indices (uint32) + métadonnées
        taille_valeurs = total_storage * np.dtype(np.float32).itemsize
        taille_indices = total_storage * np.dtype(np.uint32).itemsize
        taille_slice_ptr = slice_ptr.nbytes
        taille_slice_len = slice_len.nbytes

        taille_totale = taille_valeurs + taille_indices + taille_slice_ptr + taille_slice_len
        taille_go = taille_totale / (1024 ** 3)

        print(f"SELL: num_rows={num_rows}, num_slices={num_slices}, total_storage(padded)={total_storage}")
        print(f"Estimated SELL-C-σ matrix size: {taille_go:.3f} GB (valeurs: {taille_valeurs/(1024**3):.3f} GB, indices: {taille_indices/(1024**3):.3f} GB, métadonnées: {(taille_slice_ptr + taille_slice_len)/(1024**3):.3f} GB)")

        # allocate device SELL arrays (values float32, colinds uint32)
        self.sell_values_gpu_size = total_storage * np.dtype(np.float32).itemsize
        self.sell_colinds_gpu_size = total_storage * np.dtype(np.uint32).itemsize

        # allocate and optionally zero them
        self.sell_values_gpu = drv.mem_alloc(self.sell_values_gpu_size)
        # It's good practice to zero the values buffer to avoid leftover memory
        drv.memset_d32(self.sell_values_gpu, 0, total_storage)

        self.sell_colinds_gpu = drv.mem_alloc(self.sell_colinds_gpu_size)
        drv.memset_d32(self.sell_colinds_gpu, 0, total_storage)

        # allocate slice metadata on device
        self.slice_ptr = slice_ptr
        self.slice_len = slice_len

        self.slice_ptr_gpu_size = self.slice_ptr.nbytes
        self.slice_len_gpu_size = self.slice_len.nbytes

        self.slice_ptr_gpu = drv.mem_alloc(self.slice_ptr_gpu_size)
        self.slice_len_gpu = drv.mem_alloc(self.slice_len_gpu_size)

        drv.memcpy_htod(self.slice_ptr_gpu, self.slice_ptr)
        drv.memcpy_htod(self.slice_len_gpu, self.slice_len)

        # 3) fill SELL arrays by streaming blocks again (use GPU fill kernel)
        dense_host = np.empty((br, num_cols), dtype=np.float32)
        dense_gpu  = drv.mem_alloc(dense_host.nbytes)

        # For per-block row_nnz pointer we allocate a buffer of max block size once, then reuse
        row_nnz_host_gpu = drv.mem_alloc(br * np.dtype(np.int32).itemsize)

        for b in trange(0, num_rows, br, desc="Fill SELL"):
            R = min(br, num_rows - b)
            dense_host.fill(0.0)
            for i in range(R):
                rg = b + i
                n_idx = rg // self.T
                t_idx = rg % self.T
                dense_host[i, :] = self.manip.AcousticFields[n_idx].field[t_idx].flatten()
            # copy host block
            drv.memcpy_htod(dense_gpu, dense_host)
            # copy corresponding row_nnz slice (only R entries)
            drv.memcpy_htod(row_nnz_host_gpu, row_nnz[b:b+R])

            grid = ((R + block - 1) // block, 1, 1)
            fill_kernel(dense_gpu,
                        row_nnz_host_gpu,
                        self.slice_ptr_gpu,
                        self.slice_len_gpu,
                        self.sell_colinds_gpu,
                        self.sell_values_gpu,
                        np.int32(R),
                        np.int32(num_cols),
                        np.int32(b),          # rows_global_offset
                        np.int32(C),
                        np.float32(self.relative_threshold),
                        block=(block,1,1), grid=grid)
            drv.Context.synchronize()

        dense_gpu.free()
        row_nnz_host_gpu.free()

        # 4) compute norm_factor_inv via GPU accumulate (col sums)
        self.compute_norm_factor()

    def apply_apodization_gpu(self, window_vector_gpu):
        """
        Applique le fenêtrage directement sur self.sell_values_gpu 
        en utilisant les indices de colonnes (pixels) pour référencer 
        la fenêtre. Opération : A_values[i] *= W_vec[A_colinds[i]].
        """
        if self.sparse_mod is None:
            raise RuntimeError("Le module CUDA n'a pas été chargé.")
            
        try:
            apodize_kernel = self.sparse_mod.get_function("apply_apodisation_kernel__SELL")
        except drv.LogicError as e:
            raise RuntimeError(
                f"Le kernel CUDA 'multiply_sell_by_window_kernel' est manquant dans le .cubin. "
                f"Veuillez le compiler et l'ajouter. Erreur : {e}"
            )

        # Le total_storage inclut les éléments non-nuls et le padding SELL.
        threads = 128
        blocks = (self.total_storage + threads - 1) // threads
        
        # Lancement du kernel. Il travaille sur total_storage éléments.
        apodize_kernel(
            self.sell_values_gpu, 
            self.sell_colinds_gpu, 
            window_vector_gpu, 
            np.int64(self.total_storage), 
            block=(threads, 1, 1), 
            grid=(blocks, 1, 1)
        )
        drv.Context.synchronize()
        print("✅ Multiplication par le fenêtrage effectuée in-place sur GPU (SELL-C-σ).")
    
    def compute_norm_factor(self):
        """
        Compute the TRUE MLEM normalization norm_factor_inv = 1 / (A^T * 1)
        by performing a SELL backprojection of a vector of ones.
        This is the ONLY correct normalization for MLEM.
        """
        ZX = int(self.Z * self.X)
        TN = int(self.T * self.N)

        # Allocate device vector of ones (projections)
        ones_gpu = drv.mem_alloc(TN * np.dtype(np.float32).itemsize)
        drv.memset_d32(ones_gpu, 0x3f800000, TN)   # 1.0f bit pattern

        # Allocate output for backprojection (ZX pixels)
        c_gpu = drv.mem_alloc(ZX * np.dtype(np.float32).itemsize)
        drv.memset_d32(c_gpu, 0, ZX)

        # Get SELL backprojection kernel
        try:
            bp_kernel = self.sparse_mod.get_function("backprojection_kernel__SELL")
        except Exception as e:
            raise RuntimeError("Missing kernel backprojection_kernel__SELL in the cubin") from e

        threads = 256  
        blocks = (TN + threads - 1) // threads 

        # Launch GPU backprojection
        bp_kernel(
            self.sell_values_gpu,
            self.sell_colinds_gpu,
            self.slice_ptr_gpu,
            self.slice_len_gpu,
            ones_gpu,
            c_gpu,
            np.int32(TN),
            # np.int32(ZX),
            np.int32(self.slice_height),
            # np.int64(self.total_storage),
            block=(threads, 1, 1), # Utilise le nouveau nombre de threads
            grid=(blocks, 1, 1)
        )
        drv.Context.synchronize()

        # Copy back to host
        c_host = np.empty(ZX, dtype=np.float32)
        drv.memcpy_dtoh(c_host, c_gpu)
        ones_gpu.free()
        c_gpu.free()

        # Avoid divide-by-zero
        c_host = np.maximum(c_host, 1e-6)

        # Compute inverse (stored for use in MLEM)
        self.norm_factor_inv = (1.0 / c_host).astype(np.float32)

        # Upload to GPU
        if self.norm_factor_inv_gpu is not None:
            self.norm_factor_inv_gpu.free()

        self.norm_factor_inv_gpu_size = self.norm_factor_inv.nbytes
        self.norm_factor_inv_gpu = drv.mem_alloc(self.norm_factor_inv_gpu_size)
        drv.memcpy_htod(self.norm_factor_inv_gpu, self.norm_factor_inv)

        print("✓ Normalization (A^T*1) computed for MLEM.")

    def compute_density(self):
        """
        Returns only the density of the SELL-C-σ matrix.
        """
        if not hasattr(self, 'slice_ptr') or self.slice_ptr is None:
            raise RuntimeError("The SELL-C-σ matrix is not allocated.")

        num_rows = self.N * self.T
        num_cols = self.Z * self.X
        total_elements = num_rows * num_cols

        # Conservative estimate of non-zeros (excluding padding)
        nnz_ell_estimated = int(0.9 * self.total_storage)

        return nnz_ell_estimated / total_elements  # Returns only the density

    def getMatrixSize(self):
        """
        Returns the total size of the SELL-C-σ matrix in Gigabytes (GB).
        """
        if self.sell_values_gpu is None:
            return {"error": "The SELL-C-σ matrix is not yet allocated."}

        total_bytes = 0

        # Host-side arrays (using .nbytes which works for NumPy arrays)
        if hasattr(self, 'slice_ptr') and self.slice_ptr is not None:
            total_bytes += self.slice_ptr.nbytes
        if hasattr(self, 'slice_len') and self.slice_len is not None:
            total_bytes += self.slice_len.nbytes
        if hasattr(self, 'norm_factor_inv') and self.norm_factor_inv is not None:
            total_bytes += self.norm_factor_inv.nbytes

        # GPU-side arrays (using the stored size attributes instead of the problematic .size)
        total_bytes += self.sell_values_gpu_size
        total_bytes += self.sell_colinds_gpu_size
        total_bytes += self.slice_ptr_gpu_size
        total_bytes += self.slice_len_gpu_size
        total_bytes += self.norm_factor_inv_gpu_size
        
        return total_bytes / (1024 ** 3)  # Returns only the size in GB
    
    def flipAngle(self):
        """
        Permute les colonnes de la matrice SELL-C-σ correspondant à des angles opposés.
        Suppose que N est pair et que les angles sont organisés de manière symétrique.
        """
        if self.N % 2 != 0:
            raise ValueError("Le nombre d'angles doit être pair pour permuter les angles opposés.")

        # 1. Calculer la taille d'un bloc d'angle (en colonnes)
        ZX = self.Z * self.X
        angle_block_size = ZX // self.N

        # 2. Récupérer sell_colinds sur le host pour modification
        sell_colinds_host = np.empty(self.total_storage, dtype=np.uint32)
        drv.memcpy_dtoh(sell_colinds_host, self.sell_colinds_gpu)

        # 3. Pour chaque paire d'angles opposés
        for n in range(self.N // 2):
            n_opposite = n + self.N // 2
            # Indices des blocs de colonnes à permuter
            block_n_start = n * angle_block_size
            block_n_end = (n + 1) * angle_block_size
            block_opposite_start = n_opposite * angle_block_size
            block_opposite_end = (n_opposite + 1) * angle_block_size

            # 4. Trouver tous les éléments dans sell_colinds_host qui pointent vers ces blocs
            mask_n = (sell_colinds_host >= block_n_start) & (sell_colinds_host < block_n_end)
            mask_opposite = (sell_colinds_host >= block_opposite_start) & (sell_colinds_host < block_opposite_end)

            # 5. Permuter les indices
            sell_colinds_host[mask_n] = sell_colinds_host[mask_n] - block_n_start + block_opposite_start
            sell_colinds_host[mask_opposite] = sell_colinds_host[mask_opposite] - block_opposite_start + block_n_start

        # 6. Mettre à jour sell_colinds_gpu
        drv.memcpy_htod(self.sell_colinds_gpu, sell_colinds_host)

        # 7. Recalculer norm_factor_inv (car les colonnes ont changé)
        self.compute_norm_factor()

        print("Permutation des angles opposés effectuée pour SELL-C-σ.")

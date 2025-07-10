from AOT_biomaps.AOT_Recon.ReconTools import _forward_projection, _backward_projection

import numba
import torch
import numpy as np
import os
from tqdm import trange

def _MLEM_GPU_basic(SMatrix, y, numIterations, isSavingEachIteration, withTumor):
    """
    This method implements the MLEM algorithm using PyTorch for GPU acceleration.
    Parameters:
        SMatrix: 4D numpy array (time, z, x, nScans)
        y: 2D numpy array (time, nScans)
        numIterations: number of iterations for the MLEM algorithm
    """
    A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).cuda()  # shape: (T, Z, X, N)
    y_torch = torch.tensor(y, dtype=torch.float32).cuda()                # shape: (T, N)

    # Initialize variables
    T, Z, X, N = SMatrix.shape

    # flat
    A_flat = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)     # shape: (T * N, Z * X)
    y_flat = y_torch.reshape(-1)                                          # shape: (T * N, )

    # Step 1: start from a strickly positive image theta^(0)
    theta_0 = torch.ones((Z, X), dtype=torch.float32, device='cuda')      # shape: (Z, X)
    matrix_theta_torch = [theta_0]
    # matrix_theta_from_gpu = []

    # Compute normalization factor: A^T * 1
    normalization_factor = A_matrix_torch.sum(dim=(0, 3))                # shape: (Z, X)
    normalization_factor_flat = normalization_factor.reshape(-1)         # shape: (Z * X, )

    if withTumor:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
    else:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
    # EM Algebraic update
    for _ in trange(numIterations, desc=description):

        theta_p = matrix_theta_torch[-1]                                 # shape: (Z, X)

        # Step 2: Forward projection of current estimate : q = A * theta + b (acc with GPU)
        theta_p_flat = theta_p.reshape(-1)                               # shape: (Z * X, )
        q_flat = A_flat @ theta_p_flat                                   # shape: (T * N, )

        # Step 3: Current error estimate : compute ratio e = m / q
        e_flat = y_flat / (q_flat + torch.finfo(torch.float32).tiny)                                # shape: (T * N, )

        # Step 4: Backward projection of the error estimate : c = A.T * e (acc with GPU)
        c_flat = A_flat.T @ e_flat                                       # shape: (Z * X, )

        # Step 5: Multiplicative update of current estimate
        theta_p_plus_1_flat = (theta_p_flat / (normalization_factor_flat + torch.finfo(torch.float32).tiny)) * c_flat

        matrix_theta_torch.append(theta_p_plus_1_flat.reshape(Z, X))      # shape: (Z, X)
    
    if not isSavingEachIteration:
        return matrix_theta_torch[-1]
    else:
        return [theta.cpu().numpy() for theta in matrix_theta_torch]
        
def _MLEM_CPU_basic(SMatrix, y, numIterations, isSavingEachIteration, withTumor):
    """
    This method implements the MLEM algorithm using basic numpy operations.
    Parameters:
        SMatrix: 4D numpy array (time, z, x, nScans)
        y: 2D numpy array (time, nScans)
        numIterations: number of iterations for the MLEM algorithm
    """
    # Initialize variables
    q_p = np.zeros((SMatrix.shape[0], SMatrix.shape[3]))  # shape : (t, i)
    c_p = np.zeros((SMatrix.shape[1], SMatrix.shape[2]))  # shape : (z, x)

    # Step 1: start from a strickly positive image theta^(0)
    theta_p_0 = np.ones((SMatrix.shape[1], SMatrix.shape[2]))  # initial theta^(0)
    matrix_theta = [theta_p_0]  # store theta 

    # Compute normalization factor: A^T * 1
    normalization_factor = np.sum(SMatrix, axis=(0, 3))  # shape: (z, x)

    if withTumor:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITH TUMOR ---- processing on single CPU (basic) ----"
    else:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITHOUT TUMOR ---- processing on single CPU (basic) ----"
    
    # EM Algebraic update
    for _ in trange(numIterations, desc=description):

        theta_p = matrix_theta[-1]

        # Step 1: Forward projection of current estimate : q = A * theta + b
        for _t in range(SMatrix.shape[0]):
            for _n in range(SMatrix.shape[3]):
                q_p[_t, _n] = np.sum(SMatrix[_t, :, :, _n] * theta_p)
        
        # Step 2: Current error estimate : compute ratio e = m / q
        e_p = y / (q_p + 1e-8)  # 避免除零
        
        # Step 3: Backward projection of the error estimate : c = A.T * e
        for _z in range(SMatrix.shape[1]):
            for _x in range(SMatrix.shape[2]):
                c_p[_z, _x] = np.sum(SMatrix[:, _z, _x, :] * e_p)
        
        # Step 4: Multiplicative update of current estimate
        theta_p_plus_1 = theta_p / (normalization_factor + 1e-8) * c_p
        
        # Step 5: Store current theta
        matrix_theta.append(theta_p_plus_1)
    
    if not isSavingEachIteration:
        return matrix_theta[-1]
    else:
        return matrix_theta  # Return the list of numpy arrays

def _MLEM_CPU_multi(SMatrix, y, numIterations, isSavingEachIteration, withTumor):
    """
    This method implements the MLEM algorithm using multi-threading with Numba.
    Parameters:
        SMatrix: 4D numpy array (time, z, x, nScans)
        y: 2D numpy array (time, nScans)
        numIterations: number of iterations for the MLEM algorithm
    """
    numba.set_num_threads(os.cpu_count())
    q_p = np.zeros((SMatrix.shape[0], SMatrix.shape[3]))  # shape : (t, i)
    c_p = np.zeros((SMatrix.shape[1], SMatrix.shape[2]))  # shape : (z, x)

    # Step 1: start from a strickly positive image theta^(0)
    theta_p_0 = np.ones((SMatrix.shape[1], SMatrix.shape[2]))
    matrix_theta = [theta_p_0]

    # Compute normalization factor: A^T * 1
    normalization_factor = np.sum(SMatrix, axis=(0, 3))  # shape: (z, x)

    if withTumor:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITH TUMOR ---- processing on multithread CPU ({numba.config.NUMBA_DEFAULT_NUM_THREADS} threads)----"
    else:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITHOUT TUMOR ---- processing on multithread CPU ({numba.config.NUMBA_DEFAULT_NUM_THREADS} threads)----"

    # EM Algebraic update
    for _ in trange(numIterations, desc=description):
        
        theta_p = matrix_theta[-1]

        # Step 1: Forward projection of current estimate : q = A * theta + b (acc with njit)
        _forward_projection(SMatrix, theta_p, q_p)

        # Step 2: Current error estimate : compute ratio e = m / q
        e_p = y / (q_p + 1e-8)

        # Step 3: Backward projection of the error estimate : c = A.T * e (acc with njit)
        _backward_projection(SMatrix, e_p, c_p)

        # Step 4: Multiplicative update of current estimate
        theta_p_plus_1 = theta_p / (normalization_factor + 1e-8) * c_p

        # Step 5: Store current theta
        matrix_theta.append(theta_p_plus_1)
    
    if not isSavingEachIteration:
        return matrix_theta[-1]
    else:
        return matrix_theta

def _MLEM_CPU_opti(SMatrix, y, numIterations, isSavingEachIteration, withTumor):
    """
    This method implements the MLEM algorithm using optimized numpy operations.
    Parameters:
        SMatrix: 4D numpy array (time, z, x, nScans)
        y: 2D numpy array (time, nScans)
        numIterations: number of iterations for the MLEM algorithm
    """
    # Initialize variables
    T, Z, X, N = SMatrix.shape

    A_flat = SMatrix.astype(np.float32).transpose(0, 3, 1, 2).reshape(T * N, Z * X)         # shape: (T * N, Z * X)
    y_flat = y.astype(np.float32).reshape(-1)                                                # shape: (T * N, )

    # Step 1: start from a strickly positive image theta^(0)
    theta_0 = np.ones((Z, X), dtype=np.float32)              # shape: (Z, X)
    matrix_theta = [theta_0]

    # Compute normalization factor: A^T * 1
    normalization_factor = np.sum(SMatrix, axis=(0, 3)).astype(np.float32)                  # shape: (Z, X)
    normalization_factor_flat = normalization_factor.reshape(-1) 

    if withTumor:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITH TUMOR ---- processing on single CPU (optimized) ----"
    else:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITHOUT TUMOR ---- processing on single CPU (optimized) ----"

    # EM Algebraic update
    for _ in trange(numIterations, desc=description):
        theta_p = matrix_theta[-1]

        # Step 2: Forward projection of current estimate : q = A * theta + b (acc with njit)
        theta_p_flat = theta_p.reshape(-1)                                                    # shape: (Z * X, )
        q_flat = A_flat @ theta_p_flat                                                        # shape: (T * N)

        # Step 3: Current error estimate : compute ratio e = m / q
        e_flat = y_flat / (q_flat + np.finfo(np.float32).tiny)                                         # shape: (T * N, )
        # np.float32(1e-8)
        
        # Step 4: Backward projection of the error estimate : c = A.T * e (acc with njit)
        c_flat = A_flat.T @ e_flat                                                            # shape: (Z * X, )

        # Step 5: Multiplicative update of current estimate
        theta_p_plus_1_flat = theta_p_flat / (normalization_factor_flat + np.finfo(np.float32).tiny) * c_flat
        
        
        # Step 5: Store current theta
        matrix_theta.append(theta_p_plus_1_flat.reshape(Z, X))

    if not isSavingEachIteration:
        return matrix_theta[-1]
    else:
        return matrix_theta


def _MLEM_GPU_multi(SMatrix, y, numIterations, isSavingEachIteration, withTumor):
    """
    This method implements the MLEM algorithm using PyTorch for multi-GPU acceleration.
    Parameters:
        SMatrix: 4D numpy array (time, z, x, nScans)
        y: 2D numpy array (time, nScans)
        numIterations: number of iterations for the MLEM algorithm
    """
    # Check the number of available GPUs
    num_gpus = torch.cuda.device_count()

    # Convert data to tensors and distribute across GPUs
    A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).cuda()
    y_torch = torch.tensor(y, dtype=torch.float32).cuda()

    # Initialize variables
    T, Z, X, N = SMatrix.shape

    # Distribute the data across GPUs
    A_matrix_torch = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)
    y_flat = y_torch.reshape(-1)

    # Split data across GPUs
    A_split = torch.chunk(A_matrix_torch, num_gpus, dim=0)
    y_split = torch.chunk(y_flat, num_gpus)

    # Initialize theta on each GPU
    theta_0 = torch.ones((Z, X), dtype=torch.float32, device='cuda')
    theta_list = [theta_0.clone() for _ in range(num_gpus)]

    # Compute normalization factor: A^T * 1
    normalization_factor = A_matrix_torch.sum(dim=0)
    normalization_factor = normalization_factor.reshape(Z, X)

    if withTumor:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITH TUMOR ---- processing on multi-GPU ({num_gpus} GPUs)----"
    else:
        description = f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- WITHOUT TUMOR ---- processing on multi-GPU ({num_gpus} GPUs)----"

    # EM Algebraic update
    for _ in trange(numIterations, desc=description):
        theta_p_list = theta_list.copy()

        for i in range(num_gpus):
            A_i = A_split[i].to(f'cuda:{i}')
            y_i = y_split[i].to(f'cuda:{i}')
            theta_p = theta_p_list[i].to(f'cuda:{i}')

            # Forward projection
            q_flat = A_i @ theta_p.reshape(-1)

            # Current error estimate
            e_flat = y_i / (q_flat + torch.finfo(torch.float32).tiny)

            # Backward projection
            c_flat = A_i.T @ e_flat

            # Multiplicative update
            theta_p_plus_1_flat = (theta_p.reshape(-1) / (normalization_factor.reshape(-1) + torch.finfo(torch.float32).tiny)) * c_flat
            theta_list[i] = theta_p_plus_1_flat.reshape(Z, X).to('cuda:0')

    if not isSavingEachIteration:
        return torch.stack(theta_list).mean(dim=0).cpu().numpy()
    else:
        return [theta.cpu().numpy() for theta in theta_list]
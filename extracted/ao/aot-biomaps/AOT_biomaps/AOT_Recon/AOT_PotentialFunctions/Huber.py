from AOT_biomaps.Config import config

import numpy as np
import torch
from numba import njit
if config.get_process()  == 'gpu':
    import torch
    try:
        from torch_scatter import scatter
    except ImportError:
        raise ImportError("torch_scatter and torch_sparse are required for GPU processing. Please install them using 'pip install torch-scatter torch-sparse' with correct link (follow instructions https://github.com/LucasDuclos/AcoustoOpticTomography/edit/main/README.md).")


@njit
def _Omega_HUBER_PIECEWISE_CPU(theta_flat, index, values, delta):
    """
    Compute the gradient and Hessian of the Huber penalty function for sparse data.
    Parameters:
        theta_flat (torch.Tensor): Flattened parameter vector.
        index (torch.Tensor): Indices of the sparse matrix in COO format.
        values (torch.Tensor): Values of the sparse matrix in COO format.
        delta (float): Threshold for the Huber penalty.
    Returns:
        grad_U (torch.Tensor): Gradient of the penalty function.
        hess_U (torch.Tensor): Hessian of the penalty function.
        U_value (float): Value of the penalty function.
    """
    j_idx, k_idx = index
    diff = theta_flat[j_idx] - theta_flat[k_idx]
    abs_diff = np.abs(diff)

    # Huber penalty (potential function)
    psi_pair = np.where(abs_diff > delta,
                        delta * abs_diff - 0.5 * delta ** 2,
                        0.5 * diff ** 2)
    psi_pair = values * psi_pair

    # Huber gradient
    grad_pair = np.where(abs_diff > delta,
                            delta * np.sign(diff),
                            diff)
    grad_pair = values * grad_pair

    # Huber Hessian
    hess_pair = np.where(abs_diff > delta,
                            np.zeros_like(diff),
                            np.ones_like(diff))
    hess_pair = values * hess_pair

    grad_U = np.zeros_like(theta_flat)
    hess_U = np.zeros_like(theta_flat)

    np.add.at(grad_U, j_idx, grad_pair)
    np.add.at(hess_U, j_idx, hess_pair)

    # Total penalty energy
    U_value = 0.5 * np.sum(psi_pair)

    return grad_U, hess_U, U_value

def _Omega_HUBER_PIECEWISE_GPU(theta_flat, index, values, delta):
    """
    Compute the gradient and Hessian of the Huber penalty function for sparse data.
    Parameters:
        theta_flat (torch.Tensor): Flattened parameter vector.
        index (torch.Tensor): Indices of the sparse matrix in COO format.
        values (torch.Tensor): Values of the sparse matrix in COO format.
        delta (float): Threshold for the Huber penalty.
    Returns:
        grad_U (torch.Tensor): Gradient of the penalty function.
        hess_U (torch.Tensor): Hessian of the penalty function.
        U_value (float): Value of the penalty function.
    """
    
    j_idx, k_idx = index
    diff = theta_flat[j_idx] - theta_flat[k_idx]
    abs_diff = torch.abs(diff)

    # Huber penalty (potential function) 
    psi_pair = torch.where(abs_diff > delta,
                        delta * abs_diff - 0.5 * delta ** 2,
                        0.5 * diff ** 2)
    psi_pair = values * psi_pair  

    # Huber gradient
    grad_pair = torch.where(abs_diff > delta,
                            delta * torch.sign(diff),
                            diff)
    grad_pair = values * grad_pair

    # Huber Hessian
    hess_pair = torch.where(abs_diff > delta,
                            torch.zeros_like(diff),
                            torch.ones_like(diff))
    hess_pair = values * hess_pair

    grad_U = scatter(grad_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')
    hess_U = scatter(hess_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')

    # Total penalty energy
    U_value = 0.5 * psi_pair.sum()  

    return grad_U, hess_U, U_value

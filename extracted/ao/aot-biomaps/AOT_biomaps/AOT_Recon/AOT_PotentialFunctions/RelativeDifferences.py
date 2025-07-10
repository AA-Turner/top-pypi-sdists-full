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
def _Omega_RELATIVE_DIFFERENCE_CPU(theta_flat, index, values, gamma):
    j_idx, k_idx = index
    theta_j = theta_flat[j_idx]
    theta_k = theta_flat[k_idx]
    diff = theta_k - theta_j
    abs_diff = np.abs(diff)

    denom = theta_k + theta_j + gamma * abs_diff + 1e-8
    num = diff ** 2

    # First derivative ∂U/∂θ_j
    dpsi = (2 * diff * denom - num * (1 + gamma * np.sign(diff))) / (denom ** 2)
    grad_pair = values * (-dpsi)  # Note the negative sign: U contains ψ(θ_k, θ_j), seeking ∂/∂θ_j

    # Second derivative ∂²U/∂θ_j² (numerically stable, approximate treatment)
    d2psi = (2 * denom ** 2 - 4 * diff * denom * (1 + gamma * np.sign(diff))
                + 2 * num * (1 + gamma * np.sign(diff)) ** 2) / (denom ** 3 + 1e-8)
    hess_pair = values * d2psi

    grad_U = np.zeros_like(theta_flat)
    hess_U = np.zeros_like(theta_flat)

    np.add.at(grad_U, j_idx, grad_pair)
    np.add.at(hess_U, j_idx, hess_pair)

    return grad_U, hess_U

@staticmethod
def _Omega_RELATIVE_DIFFERENCE_GPU(theta_flat, index, values, gamma):
    j_idx, k_idx = index
    theta_j = theta_flat[j_idx]
    theta_k = theta_flat[k_idx]
    diff = theta_k - theta_j
    abs_diff = torch.abs(diff)

    denom = theta_k + theta_j + gamma * abs_diff + 1e-8
    num = diff ** 2

    dpsi = (2 * diff * denom - num * (1 + gamma * torch.sign(diff))) / (denom ** 2)
    grad_pair = values * (-dpsi) 

    d2psi = (2 * denom ** 2 - 4 * diff * denom * (1 + gamma * torch.sign(diff))
            + 2 * num * (1 + gamma * torch.sign(diff)) ** 2) / (denom ** 3 + 1e-8)
    hess_pair = values * d2psi

    grad_U = scatter(grad_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')
    hess_U = scatter(hess_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')

    return grad_U, hess_U

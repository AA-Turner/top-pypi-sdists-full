
from AOT_biomaps.AOT_Recon.ReconEnums import PotentialType
from AOT_biomaps.AOT_Recon.AOT_PotentialFunctions.Quadratic import _Omega_QUADRATIC_CPU, _Omega_QUADRATIC_GPU
from AOT_biomaps.AOT_Recon.AOT_PotentialFunctions.RelativeDifferences import _Omega_RELATIVE_DIFFERENCE_CPU, _Omega_RELATIVE_DIFFERENCE_GPU
from AOT_biomaps.AOT_Recon.AOT_PotentialFunctions.Huber import _Omega_HUBER_PIECEWISE_CPU, _Omega_HUBER_PIECEWISE_GPU
from AOT_biomaps.AOT_Recon.ReconTools import _build_adjacency_sparse_CPU, _build_adjacency_sparse_GPU
from AOT_biomaps.Config import config

import numpy as np
import torch
from tqdm import trange


def _MAPEM_CPU_STOP(SMatrix, y, Omega, numIterations, beta, delta, gamma, sigma, isSavingEachIteration, withTumor):
    """
    MAPEM version CPU simple - sans GPU - torch uniquement
    """
    if Omega is not isinstance(Omega, PotentialType):
        raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if gamma == None:
            raise ValueError("gamma must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
        if beta == None:
            raise ValueError("beta must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if delta == None:
            raise ValueError("delta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.")
        if beta == None:
            raise ValueError("beta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.") 
    elif Omega == PotentialType.QUADRATIC:
        if sigma == None:
            raise ValueError("sigma must be specified for QUADRATIC potential type. Please find the value in the paper.")
    else:
        raise ValueError(f"Unknown potential type: {Omega}")
    
    SMatrix = torch.tensor(SMatrix, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)

    T, Z, X, N = SMatrix.shape
    A_flat = SMatrix.permute(0, 3, 1, 2).reshape(T * N, Z * X)
    y_flat = y_tensor.reshape(-1)

    I_0 = torch.ones((Z, X), dtype=torch.float32)
    theta_list = [I_0]
    results = [I_0.numpy()]
    previous=-np.inf

    normalization_factor = SMatrix.sum(dim=(0, 3)).reshape(-1)
    adj_index, adj_values = _build_adjacency_sparse_CPU(Z, X)

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
            if withTumor:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f})+ STOP condtion (penalized log-likelihood) ---- WITH TUMOR ---- processing on single CPU ----"
            else:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f})+ STOP condtion (penalized log-likelihood) ---- WITHOUT TUMOR ---- processing on single CPU ----"
    elif Omega == PotentialType.HUBER_PIECEWISE:
            if withTumor:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f})+ STOP condtion (penalized log-likelihood) ---- WITH TUMOR ---- processing on single CPU ----"
            else:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f})+ STOP condtion (penalized log-likelihood) ---- WITHOUT TUMOR ---- processing on single CPU ----"
    elif Omega == PotentialType.QUADRATIC:
            if withTumor:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f})+ STOP condtion (penalized log-likelihood) ---- WITH TUMOR ---- processing on single CPU ----"
            else:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f})+ STOP condtion (penalized log-likelihood) ---- WITHOUT TUMOR ---- processing on single CPU ----"

    for p in trange(numIterations, desc=description):
        theta_p = theta_list[-1]
        theta_p_flat = theta_p.reshape(-1)

        q_flat = A_flat @ theta_p_flat
        e_flat = (y_flat - q_flat) / (q_flat + torch.finfo(torch.float32).tiny)
        c_flat = A_flat.T @ e_flat

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            grad_U, hess_U, U_value = _Omega_RELATIVE_DIFFERENCE_CPU(theta_p_flat, adj_index, adj_values, delta)
        elif Omega == PotentialType.HUBER_PIECEWISE:
            grad_U, hess_U, U_value = _Omega_HUBER_PIECEWISE_CPU(theta_p_flat, adj_index, adj_values, gamma)
        elif Omega == PotentialType.QUADRATIC:
            grad_U, hess_U, U_value = _Omega_QUADRATIC_CPU(theta_p_flat, adj_index, adj_values, sigma)

        denom = normalization_factor + theta_p_flat * beta * hess_U
        num = theta_p_flat * (c_flat - beta * grad_U)

        theta_next_flat = theta_p_flat + num / (denom + torch.finfo(torch.float32).tiny)
        theta_next_flat = torch.clamp(theta_next_flat, min=0)
        theta_next = theta_next_flat.reshape(Z, X)

        theta_list[-1] = theta_next
        results.append(theta_next.numpy())

        log_likelihood = (y_flat * torch.log(q_flat + 1e-8) - (q_flat + 1e-8)).sum()
        penalized_log_likelihood = log_likelihood - beta * U_value
        current = penalized_log_likelihood.item()

        if (p + 1) % 100 == 0:
            print(f"Iter {p+1}: logL={log_likelihood:.3e}, U={U_value:.3e}, penalized logL={penalized_log_likelihood:.3e}")
            if current <= previous:
                nb_false_successive += 1
            else:
                nb_false_successive = 0
            previous = current

            # Optionally add early stop:
            # if nb_false_successive >= 25:
            #     break

    if isSavingEachIteration:
        return results[-1]
    else:
        return results  

def _MAPEM_GPU_STOP(SMatrix, y, Omega, numIterations, beta, delta, gamma, sigma, isSavingEachIteration, withTumor):
    """
    Maximum A Posteriori (MAP) estimation for Bayesian reconstruction.
    This method computes the MAP estimate of the parameters given the data.
    """

    if Omega is not isinstance(Omega, PotentialType):
        raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if gamma == None:
            raise ValueError("gamma must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
        if beta == None:
            raise ValueError("beta must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if delta == None:
            raise ValueError("delta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.")
        if beta == None:
            raise ValueError("beta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.") 
    elif Omega == PotentialType.QUADRATIC:
        if sigma == None:
            raise ValueError("sigma must be specified for QUADRATIC potential type. Please find the value in the paper.")
    else:
        raise ValueError(f"Unknown potential type: {Omega}")

    device = torch.device(f"cuda:{config.select_best_gpu()}")

    A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).to(device)
    y_torch = torch.tensor(y, dtype=torch.float32).to(device)

    T, Z, X, N = SMatrix.shape
    J = Z * X

    A_flat = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)
    y_flat = y_torch.reshape(-1)

    I_0 = torch.ones((Z, X), dtype=torch.float32, device=device)
    matrix_theta_torch = []
    matrix_theta_torch = [I_0]
    matrix_theta_from_gpu_MAPEM = []
    matrix_theta_from_gpu_MAPEM = [I_0.cpu().numpy()]

    normalization_factor = A_matrix_torch.sum(dim=(0, 3))                # (Z, X)
    normalization_factor_flat = normalization_factor.reshape(-1)         # (Z*X,)
    previous = -np.inf
    adj_index, adj_values = _build_adjacency_sparse_GPU(Z, X)

    
    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f})+ STOP condtion (penalized log-likelihood) ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f})+ STOP condtion (penalized log-likelihood) ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f})+ STOP condtion (penalized log-likelihood) ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f})+ STOP condtion (penalized log-likelihood) ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
    elif Omega == PotentialType.QUADRATIC:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f})+ STOP condtion (penalized log-likelihood) ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"   
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f})+ STOP condtion (penalized log-likelihood) ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"

    for p in trange(numIterations, desc=description):
        theta_p = matrix_theta_torch[-1]
        theta_p_flat = theta_p.reshape(-1)

        q_flat = A_flat @ theta_p_flat
        e_flat = (y_flat - q_flat) / (q_flat + torch.finfo(torch.float32).tiny)
        c_flat = A_flat.T @ e_flat

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
                grad_U, hess_U, U_value = _Omega_RELATIVE_DIFFERENCE_CPU(theta_p_flat, adj_index, adj_values, delta)
        elif Omega == PotentialType.HUBER_PIECEWISE:
                grad_U, hess_U, U_value = _Omega_HUBER_PIECEWISE_CPU(theta_p_flat, adj_index, adj_values, gamma)
        elif Omega == PotentialType.QUADRATIC:
                grad_U, hess_U, U_value = _Omega_QUADRATIC_CPU(theta_p_flat, adj_index, adj_values, sigma)
        else:
            raise ValueError(f"Unknown potential type: {Omega}")
        
        denom = normalization_factor_flat + theta_p_flat * beta * hess_U
        num = theta_p_flat * (c_flat - beta * grad_U)

        theta_p_plus_1_flat = theta_p_flat + num / (denom + torch.finfo(torch.float32).tiny)
        theta_p_plus_1_flat = torch.clamp(theta_p_plus_1_flat, min=0)

        theta_next = theta_p_plus_1_flat.reshape(Z, X)
        #matrix_theta_torch.append(theta_next) # save theta in GPU
        matrix_theta_torch[-1] = theta_next    # do not save theta in GPU

        if p % 1 == 0:
            matrix_theta_from_gpu_MAPEM.append(theta_next.cpu().numpy())

        # === compute penalized log-likelihood (without term ln(m_i !) inside) ===
        # log-likelihood (without term ln(m_i !) inside)
        # log_likelihood = (torch.where(q_flat > 0, y_flat * torch.log(q_flat), torch.zeros_like(q_flat)) - q_flat).sum()
        # log_likelihood = (y_flat * torch.log(q_flat) - q_flat).sum()
        log_likelihood = (y_flat * ( torch.log( q_flat + torch.finfo(torch.float32).tiny ) ) - (q_flat + torch.finfo(torch.float32).tiny)).sum()

        # penalized log-likelihood
        penalized_log_likelihood = log_likelihood - beta * U_value

        if p == 0 or (p+1) % 100 == 0:
            current = penalized_log_likelihood.item()

            if current<=previous:
                nb_false_successive = nb_false_successive + 1

            else:
                nb_false_successive = 0
            
            print(f"Iter {p+1}: lnL without term ln(m_i !) inside={log_likelihood.item():.8e}, Gibbs energy function U={U_value.item():.4e}, penalized lnL without term ln(m_i !) inside={penalized_log_likelihood.item():.8e}, p lnL (current {current:.8e} - previous {previous:.8e} > 0)={(current-previous>0)}, nb_false_successive={nb_false_successive}")
            
            #if nb_false_successive >= 25:
                #break
        
            previous = penalized_log_likelihood.item()
    if isSavingEachIteration:
        return matrix_theta_from_gpu_MAPEM[-1]
    else:
        return matrix_theta_from_gpu_MAPEM

def _MAPEM_CPU(SMatrix, y, Omega, numIterations, beta, delta, gamma, sigma, isSavingEachIteration, withTumor):
    if not isinstance(Omega, PotentialType):
        raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if gamma is None or beta is None:
            raise ValueError("gamma and beta must be specified for RELATIVE_DIFFERENCE.")
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if delta is None or beta is None:
            raise ValueError("delta and beta must be specified for HUBER_PIECEWISE.")
    elif Omega == PotentialType.QUADRATIC:
        if sigma is None:
            raise ValueError("sigma must be specified for QUADRATIC.")
    else:
        raise ValueError(f"Unknown potential type: {Omega}")

    T, Z, X, N = SMatrix.shape
    J = Z * X

    A_flat = np.transpose(SMatrix, (0, 3, 1, 2)).reshape(T * N, Z * X)
    y_flat = y.reshape(-1)

    theta_0 = np.ones((Z, X), dtype=np.float32)
    matrix_theta_np = [theta_0]
    I_reconMatrix = [theta_0.copy()]

    normalization_factor = SMatrix.sum(axis=(0, 3))
    normalization_factor_flat = normalization_factor.reshape(-1)

    adj_index, adj_values = _build_adjacency_sparse_CPU(Z, X)

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f}) ---- WITH TUMOR ---- processing on single CPU ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f}) ---- WITHOUT TUMOR ---- processing on single CPU ----"
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f}) ---- WITH TUMOR ---- processing on single CPU ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f}) ---- WITHOUT TUMOR ---- processing on single CPU ----"
    elif Omega == PotentialType.QUADRATIC:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f}) ---- WITH TUMOR ---- processing on single CPU ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f}) ---- WITHOUT TUMOR ---- processing on single CPU ----"

    for p in trange(numIterations, desc=description):
        theta_p = matrix_theta_np[-1]
        theta_p_flat = theta_p.reshape(-1)

        q_flat = A_flat @ theta_p_flat
        e_flat = (y_flat - q_flat) / (q_flat + np.finfo(np.float32).tiny)
        c_flat = A_flat.T @ e_flat

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            grad_U, hess_U, _ = _Omega_RELATIVE_DIFFERENCE_CPU(theta_p_flat, adj_index, adj_values, delta)
        elif Omega == PotentialType.HUBER_PIECEWISE:
            grad_U, hess_U, _ = _Omega_HUBER_PIECEWISE_CPU(theta_p_flat, adj_index, adj_values, gamma)
        elif Omega == PotentialType.QUADRATIC:
            grad_U, hess_U, _ = _Omega_QUADRATIC_CPU(theta_p_flat, adj_index, adj_values, sigma)


        denom = normalization_factor_flat + theta_p_flat * beta * hess_U
        num = theta_p_flat * (c_flat - beta * grad_U)

        theta_p_plus_1_flat = theta_p_flat + num / (denom + np.finfo(np.float32).tiny)
        theta_p_plus_1_flat = np.clip(theta_p_plus_1_flat, 0, None)

        theta_next = theta_p_plus_1_flat.reshape(Z, X)
        matrix_theta_np.append(theta_next)


        if p % 1 == 0:
            I_reconMatrix.append(theta_next.copy())

    if isSavingEachIteration:
        return I_reconMatrix
    else:
        return I_reconMatrix[-1]

def _MAPEM_GPU(SMatrix, y, Omega, numIterations, beta, delta, gamma, sigma, isSavingEachIteration, withTumor):
    '''
    Maximum A Posteriori (MAP) estimation for Bayesian reconstruction using GPU.
    This method computes the MAP estimate of the parameters given the data.
    Parameters:
        SMatrix (numpy.ndarray): The system matrix of shape (T, Z, X, N).
        y (numpy.ndarray): The observed data of shape (T, N).
        Omega (PotentialType): The potential function to use for regularization.
        iteration (int): The number of iterations for the MAP-EM algorithm.
    Returns:
        matrix_theta_from_gpu_MAPEM (list): A list of numpy arrays containing the estimated parameters at each iteration.
        '''
    
    if Omega is not isinstance(Omega, PotentialType):
        raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if gamma == None:
            raise ValueError("gamma must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
        if beta == None:
            raise ValueError("beta must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if delta == None:
            raise ValueError("delta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.")
        if beta == None:
            raise ValueError("beta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.") 
    elif Omega == PotentialType.QUADRATIC:
        if sigma == None:
            raise ValueError("sigma must be specified for QUADRATIC potential type. Please find the value in the paper.")
    else:
        raise ValueError(f"Unknown potential type: {Omega}")

    device = torch.device(f"cuda:{config.select_best_gpu()}")

    A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).to(device)
    y_torch = torch.tensor(y, dtype=torch.float32).to(device)

    T, Z, X, N = SMatrix.shape
    J = Z * X

    A_flat = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)
    y_flat = y_torch.reshape(-1)

    theta_0 = torch.ones((Z, X), dtype=torch.float32, device=device)
    matrix_theta_torch = []
    matrix_theta_torch = [theta_0]
    I_reconMatrix = [theta_0.cpu().numpy()]

    normalization_factor = A_matrix_torch.sum(dim=(0, 3))                # (Z, X)
    normalization_factor_flat = normalization_factor.reshape(-1)         # (Z*X,)

    adj_index, adj_values = _build_adjacency_sparse_GPU(Z, X)

    if Omega == PotentialType.RELATIVE_DIFFERENCE:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f}) ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f}) ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"   
    elif Omega == PotentialType.HUBER_PIECEWISE:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f}) ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f}) ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
    elif Omega == PotentialType.QUADRATIC:
        if withTumor:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f}) ---- WITH TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        else:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f}) ---- WITHOUT TUMOR ---- processing on single GPU no.{torch.cuda.current_device()} ----"

    for p in trange(numIterations, desc=description):
        theta_p = matrix_theta_torch[-1]
        theta_p_flat = theta_p.reshape(-1)

        q_flat = A_flat @ theta_p_flat
        e_flat = (y_flat - q_flat) / (q_flat + torch.finfo(torch.float32).tiny)
        c_flat = A_flat.T @ e_flat
        
        if Omega == PotentialType.RELATIVE_DIFFERENCE:
                grad_U, hess_U, _ = _Omega_RELATIVE_DIFFERENCE_GPU(theta_p_flat, adj_index, adj_values, delta=delta)
        elif Omega == PotentialType.HUBER_PIECEWISE:
                grad_U, hess_U, _ = _Omega_HUBER_PIECEWISE_GPU(theta_p_flat, adj_index, adj_values, gamma=gamma)
        elif Omega == PotentialType.QUADRATIC:
                grad_U, hess_U, _ = _Omega_QUADRATIC_GPU(theta_p_flat, adj_index, adj_values, sigma=sigma)
        else:
            raise ValueError(f"Unknown potential type: {Omega}")

        denom = normalization_factor_flat + theta_p_flat * beta * hess_U
        num = theta_p_flat * (c_flat - beta * grad_U)

        theta_p_plus_1_flat = theta_p_flat + num / (denom + torch.finfo(torch.float32).tiny)
        theta_p_plus_1_flat = torch.clamp(theta_p_plus_1_flat, min=0)

        theta_next = theta_p_plus_1_flat.reshape(Z, X)
        matrix_theta_torch.append(theta_next) # save theta in GPU

        if p % 1 == 0:
            I_reconMatrix.append(theta_next.cpu().numpy())   

    if isSavingEachIteration:
        return I_reconMatrix
    else:
        return I_reconMatrix[-1]

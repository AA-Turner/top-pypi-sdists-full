import pyro
import pyro.distributions as dist
from pyro.optim import ExponentialLR
from pyro.infer import SVI, JitTraceEnum_ELBO, TraceEnum_ELBO, config_enumerate

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.distributions.utils import logits_to_probs, probs_to_logits, clamp_probs
from torch.distributions import constraints
from torch.distributions.transforms import SoftmaxTransform

from .utils.custom_mlp import MLP, Exp, ZeroBiasMLP2
from .utils.utils import CustomDataset, CustomDataset2, CustomDataset4, tensor_to_numpy, convert_to_tensor

from .dist.negbinomial import NegativeBinomial as MyNB
from .dist.negbinomial import ZeroInflatedNegativeBinomial as MyZINB
from .graph.graph_utils import ClusterNetworkBuilder, KnnClusterNetworkBuilder,visualize_network,keep_top_k_edges_per_node,visualize_network_interactive,EdgeAllocation

from .SURE_nsf import SURENF
from .SURE_vae import SUREVAE
from .SURE_vanilla import SUREVanilla

import zuko 
from pyro.contrib.zuko import ZukoToPyro

import os
import argparse
import random
import numpy as np
import datatable as dt
from tqdm import tqdm
from scipy import sparse
from scipy.stats import epps_singleton_2samp, ks_2samp
import networkx as nx
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA

import scanpy as sc
from .atac import binarize

from typing import Literal

import warnings
warnings.filterwarnings("ignore")

import dill as pickle
import gzip
from packaging.version import Version
torch_version = torch.__version__


def set_random_seed(seed):
    # Set seed for PyTorch
    torch.manual_seed(seed)
    
    # If using CUDA, set the seed for CUDA
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # For multi-GPU setups.
    
    # Set seed for NumPy
    np.random.seed(seed)
    
    # Set seed for Python's random module
    random.seed(seed)

    # Set seed for Pyro
    pyro.set_rng_seed(seed)

class SURE(nn.Module):
    """SUccinct REpresentation of single-omics cells

    Parameters
    ----------
    inpute_size
        Number of features (e.g., genes, peaks, proteins, etc.) per cell.
    codebook_size
        Number of metacells.
    covariate_sizes
        Number of cell-level factors. 
    transforms
        Number of neural spline flows
    z_dim
        Dimensionality of latent states and metacells. 
    hidden_layers
        A list gives the numbers of neurons for each hidden layer.
    flow_hidden_layers
        A list gives the numbers of neurons for each hidden layer in neural spline flows.
    loss_func
        The likelihood model for single-cell data generation. 
        
        One of the following: 
        * ``'negbinomial'`` -  negative binomial distribution (default)
        * ``'poisson'`` - poisson distribution
        * ``'multinomial'`` - multinomial distribution
    use_cuda
        A boolean option for switching on cuda device. 

    Examples
    --------
    >>>
    >>>
    >>>

    """
    def __init__(self,
                 input_dim: int,
                 codebook_size: int,
                 context_sizes: list = [0],
                 perturb_size: int = 0,
                 covariate_sizes: int = 0,
                 method: Literal['flow','vae'] = 'vae',
                 transforms: int = 1,
                 z_dim: int = 30,
                 z_dist: Literal['normal','studentt','laplacian','cauchy','gumbel'] = 'studentt',
                 loss_func: Literal['negbinomial','poisson','multinomial','bernoulli'] = 'multinomial',
                 dispersion: float = 10.0,
                 use_zeroinflate: bool = True,
                 hidden_layers: list = [500],
                 hidden_layer_activation: Literal['relu','softplus','leakyrelu','linear'] = 'relu',
                 flow_hidden_layers = [256],
                 nn_dropout: float = 0.1,
                 post_layer_fct: list = ['layernorm'],
                 post_act_fct: list = None,
                 config_enum: str = 'parallel',
                 use_cuda: bool = True,
                 seed: int = 42,
                 dtype = torch.float32, # type: ignore
                 ):
        super().__init__()
        
        if method == 'flow':
            self.engine = SURENF(input_dim=input_dim,
                                 codebook_size=codebook_size,
                                 context_sizes=context_sizes,
                                 perturb_size=perturb_size,
                                 covariate_sizes=covariate_sizes,
                                 transforms=transforms,
                                 z_dim=z_dim,
                                 z_dist=z_dist,
                                 loss_func=loss_func,
                                 dispersion=dispersion,
                                 use_zeroinflate=use_zeroinflate,
                                 hidden_layers=hidden_layers,
                                 hidden_layer_activation=hidden_layer_activation,
                                 flow_hidden_layers=flow_hidden_layers,
                                 nn_dropout=nn_dropout,
                                 post_act_fct=post_act_fct,
                                 post_layer_fct=post_layer_fct,
                                 config_enum=config_enum,
                                 use_cuda=use_cuda,
                                 seed=seed,
                                 dtype=dtype)
        elif method == 'vae':
            self.engine = SUREVAE(input_dim=input_dim,
                                  codebook_size=codebook_size,
                                  context_sizes=context_sizes,
                                  perturb_size=perturb_size,
                                  covariate_sizes=covariate_sizes,
                                  z_dim=z_dim,
                                  z_dist=z_dist,
                                  loss_func=loss_func,
                                  dispersion=dispersion,
                                  use_zeroinflate=use_zeroinflate,
                                  hidden_layers=hidden_layers,
                                  hidden_layer_activation=hidden_layer_activation,
                                  nn_dropout=nn_dropout,
                                  post_layer_fct=post_layer_fct,
                                  post_act_fct=post_act_fct,
                                  config_enum=config_enum,
                                  use_cuda=use_cuda,
                                  seed=seed,
                                  dtype=dtype)

    def get_device(self):
        return self.engine.get_device()

    def get_codebook(self):
        """
        Return the mean part of metacell codebook
        """
        return self.engine.get_codebook()

    def get_cell_embedding(self, 
                             xs, 
                             batch_size: int = 1024,
                             show_progress: bool = True):
        """
        Return cells' latent representations

        Parameters
        ----------
        xs
            Single-cell expression matrix. It should be a Numpy array or a Pytorch Tensor.
        batch_size
            Size of batch processing.
        show_progress
            Verbose on or off
        """
        return self.engine.get_cell_embedding(xs=xs, batch_size=batch_size, show_progress=show_progress)
    
    def code(self, xs, batch_size=1024, show_progress=True):
        return self.engine.code(xs=xs, batch_size=batch_size, show_progress=show_progress)
    
    def soft_assignments(self, xs, batch_size=1024, show_progress=True):
        """
        Map cells to metacells and return the probabilistic values of metacell assignments
        """
        return self.engine.soft_assignments(xs=xs, batch_size=batch_size, show_progress=show_progress)
    
    def hard_assignments(self, xs, batch_size=1024, show_progress=True):
        """
        Map cells to metacells and return the assigned metacell identities.
        """
        return self.engine.hard_assignments(xs=xs, batch_size=batch_size, show_progress=show_progress)
    
    def get_context_effect(self, z_basal, cs, i, batch_size=1024, show_progress=True):
        return self.engine.get_context_effect(z_basal, cs, i, batch_size=batch_size, show_progress=show_progress)
    
    def get_perturb_effect(self, z_basal, zcs, ps, batch_size=1024, show_progress=True):
        return self.engine.get_perturb_effect(z_basal, zcs, ps, batch_size, show_progress)
    
    def predict_cluster(self, xs, batch_size=1024, show_progress=True):
        return self.engine.predict_cluster(xs, batch_size=batch_size, show_progress=show_progress)
    
    def predict(self, xs, cs_list, ps, fs_list=None, batch_size=1024, show_progress=True):
        """
        Generate gene expression prediction from given cell data and covariates.
        This function can be used for simulating cells' transcription profiles at new conditions.
        
        :param self: SURE model
        :param xs: Cell data at the source condition
        :param cs: Covariates specifying the target condition for generation
        :param batch_size: Data size per batch
        :param show_progress: Toggle on or off message output
        """
        return self.engine.predict(xs, cs_list, ps, fs_list, batch_size, show_progress)
    
    def preprocess(self, xs, threshold=0):
        return self.engine.preprocess(xs=xs, threshold=threshold) 
    
    def fit(self, xs:np.array, 
            css:list = None, 
            ps:np.array = None,
            fss:list = None,
            num_epochs: int = 100, 
            learning_rate: float = 0.0001, 
            use_mask: bool = False,
            mask_ratio: float = 0.15,
            batch_size: int = 1000, 
            algo: Literal['adam','rmsprop','adamw'] = 'adam', 
            beta_1: float = 0.9, 
            weight_decay: float = 0.005, 
            decay_rate: float = 0.9,
            config_enum: str = 'parallel',
            threshold: int = 0,
            use_jax: bool = False,
            show_progress: bool = True,
            # Early stopping 相关参数
            patience: int = 10,
            min_delta: float = 1e-4,
            restore_best_weights: bool = True,
            monitor: str = 'loss'):
        """
        Train the SURE model.

        Parameters
        ----------
        xs
            Single-cell experssion matrix. It should be a Numpy array or a Pytorch Tensor. Rows are cells and columns are features.
        us
            cell-level factor matrix. 
        num_epochs
            Number of training epochs.
        learning_rate
            Parameter for training.
        batch_size
            Size of batch processing.
        algo
            Optimization algorithm.
        beta_1
            Parameter for optimization.
        weight_decay
            Parameter for optimization.
        decay_rate 
            Parameter for optimization.
        use_jax
            If toggled on, Jax will be used for speeding up. CAUTION: This will raise errors because of unknown reasons when it is called in
            the Python script or Jupyter notebook. It is OK if it is used when runing SURE in the shell command.
        """
        self.engine.fit(xs=xs, css=css, ps=ps, fss=fss, num_epochs=num_epochs, learning_rate=learning_rate, use_mask=use_mask, mask_ratio=mask_ratio, batch_size=batch_size, algo=algo,
                        beta_1=beta_1, weight_decay=weight_decay, decay_rate=decay_rate, config_enum=config_enum, threshold=threshold,
                        use_jax=use_jax, show_progress=show_progress, patience=patience, min_delta=min_delta, restore_best_weights=restore_best_weights,
                        monitor=monitor)
        
    def build_network(self, xs, 
                      k_data_to_data:int=5,
                      k_data_to_centers:int=3,
                      k_centers_to_data:int=30, 
                      k_centers_to_centers:int=7, 
                      sample_size:int=3000,
                      temperature:float=1.0,
                      builder:Literal['bipartite','knn']='bipartite',
                      weight_method:Literal['count','proportion', 'weighted']='weighted',
                      metric:Literal['euclidean','correlation','cosine','mahalanobis']='cosine',
                      min_edge_weight:float=0.01,
                      normalize_weights:bool=True,
                      show_progress:bool=False):
        
        n_sample = xs.shape[0]
        # metacell attributes
        zs = self.engine.get_cell_embedding(xs, show_progress=show_progress)
        
        pca_model = PCA().fit(self.engine.codebook_loc)
        zs = pca_model.transform(zs)
        cb = pca_model.transform(self.engine.codebook_loc)
        
        idx = np.arange(n_sample)
        if n_sample>sample_size:
            idx = np.random.choice(idx, size=sample_size)
            
        # create network
        if builder=='bipartite':
            network_builder = ClusterNetworkBuilder(weight_method=weight_method, 
                                                    k_data_to_centers=k_data_to_centers, k_centers_to_data=k_centers_to_data,
                                                    min_edge_weight=min_edge_weight, normalize_weights=normalize_weights)
            G = network_builder.build_network(zs[idx], cb, metric=metric)
        else:
            network_builder = KnnClusterNetworkBuilder(k_data=k_data_to_data, k_centers=k_centers_to_data,
                                                       temperature=temperature, metric=metric)
            G = network_builder.build_network(zs[idx], cb)
        
        y = self.predict_cluster(xs, show_progress=show_progress)
        Y = np.zeros([n_sample, self.engine.code_dim])
        Y[np.arange(n_sample),y] = 1 
        nY = np.sum(Y, axis=0)
        
        for i in np.arange(self.engine.code_dim):
            G.nodes[i]['cluster_size'] = nY[i]
            G.nodes[i]['cluster_weight'] = nY[i]/n_sample
            G.nodes[i]['weight'] = nY[i]/n_sample
        
        G = keep_top_k_edges_per_node(G, k_centers_to_centers, inplace=True)
        
        # assign data points to edges
        edge_allocator = EdgeAllocation()
        edge_weights = edge_allocator.fit_transform(zs[idx], cb, G, metric=metric)
        for edge in edge_weights.keys():
            i,j = edge 
            G[i][j]['weight'] = edge_weights[edge]
            
        nodes_data = [
            {'node_id': node, **attrs} 
            for node, attrs in G.nodes(data=True)
        ]
        
        edges_data = [
            {'source': u, 'target': v, **attrs}
            for u, v, attrs in G.edges(data=True)
        ]
        
        return G,pd.DataFrame(nodes_data),pd.DataFrame(edges_data)
    
    def display_network(self, G,
                        node_size_attr='weight',
                        node_size_scale=5000, edge_size_scale=10, 
                        use_plotly=False,
                        figsize=(12,10)):       
        # 元细胞坐标点
        pos_array = PCA().fit_transform(self.engine.codebook_loc)
        
        if not use_plotly:
            visualize_network(G, pos_array, node_size_attr=node_size_attr, node_size_scale=node_size_scale, edge_size_scale=edge_size_scale, figsize=figsize)
        else:
            visualize_network_interactive(G, pos_array, node_size_scale=node_size_scale, edge_size_scale=edge_size_scale, figsize=figsize*100)

    @classmethod
    def save_model(cls, model, file_path, compression=False):
        """Save the model to the specified file path."""
        file_path = os.path.abspath(file_path)

        model.eval()
        if compression:
            with gzip.open(file_path, 'wb') as pickle_file:
                pickle.dump(model, pickle_file)
        else:
            with open(file_path, 'wb') as pickle_file:
                pickle.dump(model, pickle_file)

        print(f'Model saved to {file_path}')

    @classmethod
    def load_model(cls, file_path):
        """Load the model from the specified file path and return an instance."""
        print(f'Model loaded from {file_path}')

        file_path = os.path.abspath(file_path)
        if file_path.endswith('gz'):
            with gzip.open(file_path, 'rb') as pickle_file:
                model = pickle.load(pickle_file)
        else:
            with open(file_path, 'rb') as pickle_file:
                model = pickle.load(pickle_file)
        
        return model

        

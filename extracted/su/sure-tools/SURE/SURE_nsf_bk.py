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

from .utils.custom_mlp import MLP, Exp, ZeroBiasMLP2, ZeroBiasMLP3
from .utils.utils import CustomDataset, CustomDataset2, CustomDataset4, tensor_to_numpy, convert_to_tensor

from .dist.negbinomial import NegativeBinomial as MyNB
from .dist.negbinomial import ZeroInflatedNegativeBinomial as MyZINB

import zuko 
from pyro.contrib.zuko import ZukoToPyro

import os
import argparse
import random
import numpy as np
import datatable as dt
from tqdm import tqdm
from scipy import sparse
from sklearn.cluster import KMeans

import scanpy as sc
from .atac import binarize

from typing import Literal

import warnings
warnings.filterwarnings("ignore")

import dill as pickle
import gzip
from packaging.version import Version
torch_version = torch.__version__

SCALAR_MODE='scalar'

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

def mask_matrix(matrix, mask_ratio=0.3, mask_value=0):
    """
    随机遮掩2D矩阵的元素
    matrix: [H, W] 或 [N, D]
    mask_ratio: 遮掩比例
    mask_value: 遮掩后的填充值
    """
    H, W = matrix.shape
    
    # 生成随机掩码
    mask = torch.rand(H, W) > mask_ratio
    mask = mask.to(matrix.device)
    
    # 应用遮掩
    masked_matrix = matrix.clone()
    masked_matrix[~mask] = mask_value
    
    return masked_matrix


class SURENF(nn.Module):
    """SUccinct REpresentation of single-omics cells

    Parameters
    ----------
    inpute_size
        Number of features (e.g., genes, peaks, proteins, etc.) per cell.
    codebook_size
        Number of metacells.
    context_sizes
        Number of context factors. 
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
                 covariate_sizes: list = [0],
                 covariate_dim: int = 5,
                 profile_decoder: Literal['linear','nonlinear'] = 'linear',
                 z_dim: int = 50,
                 z_dist: Literal['normal','studentt','laplacian','cauchy','gumbel','nsf'] = 'studentt',
                 loss_func: Literal['negbinomial','poisson','multinomial','bernoulli'] = 'negbinomial',
                 dispersion: float = 10.0,
                 use_zeroinflate: bool = True,
                 hidden_layers: list = [500],
                 hidden_layer_activation: Literal['relu','softplus','leakyrelu','linear'] = 'relu',
                 flow_transforms: int = 1,
                 flow_hidden_layers: list = [256],
                 nn_dropout: float = 0.1,
                 post_layer_fct: list = ['layernorm'],
                 post_act_fct: list = None,
                 config_enum: str = 'parallel',
                 use_cuda: bool = True,
                 seed: int = 42,
                 dtype = torch.float32, # type: ignore
                 ):
        super().__init__()

        self.input_dim = input_dim
        self.context_sizes = context_sizes
        self.perturb_size = perturb_size
        self.covariate_sizes = covariate_sizes
        self.dispersion = dispersion
        self.latent_dim = z_dim
        self.latent_dist = z_dist
        self.hidden_layers = hidden_layers
        self.decoder_hidden_layers = hidden_layers[::-1]
        self.allow_broadcast = config_enum == 'parallel'
        self.use_cuda = use_cuda
        self.loss_func = loss_func
        self.options = None
        self.code_dim=codebook_size
        self.dtype = dtype
        self.use_zeroinflate=use_zeroinflate
        self.nn_dropout = nn_dropout
        self.post_layer_fct = post_layer_fct
        self.post_act_fct = post_act_fct
        self.hidden_layer_activation = hidden_layer_activation
        self.covariate_dim = covariate_dim
        self.profile_decoder = profile_decoder
        
        self.codebook_weights = None
        self.centroids = None
        
        self.use_mask = False
        self.mask_ratio = 0
        
        self.transforms = flow_transforms
        self.flow_hidden_layers = flow_hidden_layers
        
        self.kmeans = KMeans(n_clusters=codebook_size)
        self.seed = seed

        set_random_seed(seed)
        self.setup_networks()

    def setup_networks(self):
        latent_dim = self.latent_dim
        hidden_sizes = self.hidden_layers

        nn_layer_norm, nn_batch_norm, nn_layer_dropout = False, False, False
        na_layer_norm, na_batch_norm, na_layer_dropout = False, False, False

        if self.post_layer_fct is not None:
            nn_layer_norm=True if ('layernorm' in self.post_layer_fct) or ('layer_norm' in self.post_layer_fct) else False
            nn_batch_norm=True if ('batchnorm' in self.post_layer_fct) or ('batch_norm' in self.post_layer_fct) else False
            nn_layer_dropout=True if 'dropout' in self.post_layer_fct else False

        if self.post_act_fct is not None:
            na_layer_norm=True if ('layernorm' in self.post_act_fct) or ('layer_norm' in self.post_act_fct) else False
            na_batch_norm=True if ('batchnorm' in self.post_act_fct) or ('batch_norm' in self.post_act_fct) else False
            na_layer_dropout=True if 'dropout' in self.post_act_fct else False

        if nn_layer_norm and nn_batch_norm and nn_layer_dropout:
            post_layer_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.Dropout(self.nn_dropout),nn.BatchNorm1d(layer.module.out_features), nn.LayerNorm(layer.module.out_features))
        elif nn_layer_norm and nn_layer_dropout:
            post_layer_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.Dropout(self.nn_dropout), nn.LayerNorm(layer.module.out_features))
        elif nn_batch_norm and nn_layer_dropout:
            post_layer_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.Dropout(self.nn_dropout), nn.BatchNorm1d(layer.module.out_features))
        elif nn_layer_norm and nn_batch_norm:
            post_layer_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.BatchNorm1d(layer.module.out_features), nn.LayerNorm(layer.module.out_features))
        elif nn_layer_norm:
            post_layer_fct = lambda layer_ix, total_layers, layer: nn.LayerNorm(layer.module.out_features)
        elif nn_batch_norm:
            post_layer_fct = lambda layer_ix, total_layers, layer:nn.BatchNorm1d(layer.module.out_features)
        elif nn_layer_dropout:
            post_layer_fct = lambda layer_ix, total_layers, layer: nn.Dropout(self.nn_dropout)
        else:
            post_layer_fct = lambda layer_ix, total_layers, layer: None

        if na_layer_norm and na_batch_norm and na_layer_dropout:
            post_act_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.Dropout(self.nn_dropout),nn.BatchNorm1d(layer.module.out_features), nn.LayerNorm(layer.module.out_features))
        elif na_layer_norm and na_layer_dropout:
            post_act_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.Dropout(self.nn_dropout), nn.LayerNorm(layer.module.out_features))
        elif na_batch_norm and na_layer_dropout:
            post_act_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.Dropout(self.nn_dropout), nn.BatchNorm1d(layer.module.out_features))
        elif na_layer_norm and na_batch_norm:
            post_act_fct = lambda layer_ix, total_layers, layer: nn.Sequential(nn.BatchNorm1d(layer.module.out_features), nn.LayerNorm(layer.module.out_features))
        elif na_layer_norm:
            post_act_fct = lambda layer_ix, total_layers, layer: nn.LayerNorm(layer.module.out_features)
        elif na_batch_norm:
            post_act_fct = lambda layer_ix, total_layers, layer:nn.BatchNorm1d(layer.module.out_features)
        elif na_layer_dropout:
            post_act_fct = lambda layer_ix, total_layers, layer: nn.Dropout(self.nn_dropout)
        else:
            post_act_fct = lambda layer_ix, total_layers, layer: None

        if self.hidden_layer_activation == 'relu':
            activate_fct = nn.ReLU
        elif self.hidden_layer_activation == 'softplus':
            activate_fct = nn.Softplus
        elif self.hidden_layer_activation == 'leakyrelu':
            activate_fct = nn.LeakyReLU
        elif self.hidden_layer_activation == 'linear':
            activate_fct = nn.Identity

        self.encoder_alpha = MLP(
                [self.latent_dim] + hidden_sizes + [self.code_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )

        self.encoder_zn = MLP(
            [self.input_dim] + hidden_sizes + [[latent_dim, latent_dim]],
            activation=activate_fct,
            output_activation=[None, Exp],
            post_layer_fct=post_layer_fct,
            post_act_fct=post_act_fct,
            allow_broadcast=self.allow_broadcast,
            use_cuda=self.use_cuda,
        )

        if np.sum(self.context_sizes)>0:
            self.context_effects = nn.ModuleList()
            for context_size in self.context_sizes:
                self.context_effects.append(ZeroBiasMLP3(
                        [context_size + self.latent_dim] + self.decoder_hidden_layers + [self.latent_dim],
                        activation=activate_fct,
                        output_activation=None,
                        post_layer_fct=post_layer_fct,
                        post_act_fct=post_act_fct,
                        allow_broadcast=self.allow_broadcast,
                        use_cuda=self.use_cuda,
                    )
                )
        
        if self.perturb_size>0:
            self.perturb_effect = ZeroBiasMLP3(
                [self.perturb_size + self.latent_dim] + self.decoder_hidden_layers + [self.latent_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )
            '''self.latent_decoder = MLP(
                [self.perturb_size+self.latent_dim] + self.decoder_hidden_layers + [self.latent_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )
        else:
            self.latent_decoder = MLP(
                [self.latent_dim] + self.decoder_hidden_layers + [self.latent_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )'''
        
        self.latent_decoder = zuko.flows.NSF(features=self.latent_dim, context=self.latent_dim, 
                                             transforms=self.transforms, 
                                             hidden_features=self.flow_hidden_layers)
        
        if np.sum(self.covariate_sizes)>0:
            self.covariate_effects = nn.ModuleList()
            for covariate_size in self.covariate_sizes:
                self.covariate_effects.append(ZeroBiasMLP2(
                        [covariate_size] + self.decoder_hidden_layers + [self.covariate_dim],
                        activation=activate_fct,
                        output_activation=None,
                        post_layer_fct=post_layer_fct,
                        post_act_fct=post_act_fct,
                        allow_broadcast=self.allow_broadcast,
                        use_cuda=self.use_cuda,
                    )
                )
            
        if self.latent_dist == 'nsf':
            self.decoder_zn = zuko.flows.NSF(features=self.latent_dim, context=self.latent_dim, 
                                             transforms=self.transforms, 
                                             hidden_features=self.flow_hidden_layers)
            
        if self.profile_decoder == 'linear':
            self.decoder_log_mu = MLP(
                    [self.latent_dim + self.covariate_dim] + self.decoder_hidden_layers + [self.input_dim],
                    #activation=activate_fct,
                    activation=nn.Identity,
                    output_activation=None,
                    #post_layer_fct=post_layer_fct,
                    #post_act_fct=post_act_fct,
                    allow_broadcast=self.allow_broadcast,
                    use_cuda=self.use_cuda,
                )
        else:
            self.decoder_log_mu = MLP(
                    [self.latent_dim + self.covariate_dim] + self.decoder_hidden_layers + [self.input_dim],
                    activation=activate_fct,
                    output_activation=None,
                    post_layer_fct=post_layer_fct,
                    post_act_fct=post_act_fct,
                    allow_broadcast=self.allow_broadcast,
                    use_cuda=self.use_cuda,
                )
        
        if self.latent_dist == 'studentt':
            self.codebook = MLP(
                [self.code_dim] + hidden_sizes + [[latent_dim,latent_dim]],
                activation=activate_fct,
                output_activation=[Exp,None],
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )
        else:
            self.codebook = MLP(
                [self.code_dim] + hidden_sizes + [latent_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )
        
        if self.use_cuda:
            self.cuda()

    def get_device(self):
        return next(self.parameters()).device

    def cutoff(self, xs, thresh=None):
        eps = torch.finfo(xs.dtype).eps
        
        if not thresh is None:
            if eps < thresh:
                eps = thresh

        xs = xs.clamp(min=eps)

        if torch.any(torch.isnan(xs)):
            xs[torch.isnan(xs)] = eps

        return xs

    def softmax(self, xs):
        #xs = SoftmaxTransform()(xs)
        xs = dist.Multinomial(total_count=1, logits=xs).mean
        return xs
    
    def sigmoid(self, xs):
        #sigm_enc = nn.Sigmoid()
        #xs = sigm_enc(xs)
        #xs = clamp_probs(xs)
        xs = dist.Bernoulli(logits=xs).mean
        return xs

    def softmax_logit(self, xs):
        eps = torch.finfo(xs.dtype).eps
        xs = self.softmax(xs)
        xs = torch.logit(xs, eps=eps)
        return xs

    def logit(self, xs):
        eps = torch.finfo(xs.dtype).eps
        xs = torch.logit(xs, eps=eps)
        return xs

    def dirimulti_param(self, xs):
        xs = self.dirimulti_mass * self.sigmoid(xs)
        return xs

    def multi_param(self, xs):
        xs = self.softmax(xs)
        return xs

    def model(self, xs, cs=None, ps=None, fs=None):
        pyro.module('sure', self)

        eps = torch.finfo(xs.dtype).eps
        batch_size = xs.size(0)
        self.options = dict(dtype=xs.dtype, device=xs.device)
        
        if self.loss_func=='negbinomial':
            dispersion = pyro.param("dispersion", self.dispersion *
                                     xs.new_ones(self.input_dim), constraint=constraints.positive)
            
        if self.use_zeroinflate:
            gate_logits = pyro.param("dropout_rate", xs.new_zeros(self.input_dim))

        if self.latent_dist != 'nsf':
            acs_scale = pyro.param("codebook_scale", xs.new_ones(self.latent_dim), constraint=constraints.positive)

        I = torch.eye(self.code_dim)
        if self.latent_dist=='studentt':
            acs_dof,acs_loc = self.codebook(I)
        else:
            acs_loc = self.codebook(I)
            
        with pyro.plate('data'):
            prior = torch.zeros(batch_size, self.code_dim, **self.options)
            ns = pyro.sample('n', dist.OneHotCategorical(logits=prior))
            _, ind = torch.topk(ns, 1)
            
            zn_loc = acs_loc[ind.squeeze()]
            if self.latent_dist != 'nsf':
                zn_scale = acs_scale

            if self.latent_dist == 'studentt':
                zn_dof = acs_dof[ind.squeeze()]
                zns = pyro.sample('zn', dist.StudentT(df=zn_dof, loc=zn_loc, scale=zn_scale).to_event(1))
            elif self.latent_dist == 'laplacian':
                zns = pyro.sample('zn', dist.Laplace(zn_loc, zn_scale).to_event(1))
            elif self.latent_dist == 'cauchy':
                zns = pyro.sample('zn', dist.Cauchy(zn_loc, zn_scale).to_event(1))
            elif self.latent_dist == 'normal':
                zns = pyro.sample('zn', dist.Normal(zn_loc, zn_scale).to_event(1))
            elif self.latent_dist == 'gumbel':
                zns = pyro.sample('zn', dist.Gumbel(zn_loc, zn_scale).to_event(1))
            elif self.latent_dist == 'nsf':
                zns = pyro.sample('zn', ZukoToPyro(self.decoder_zn(zn_loc)))
            
            zs = torch.zeros_like(zns)
            zs += zns
            if (np.sum(self.context_sizes)>0) and (cs is not None):
                zcs = torch.zeros_like(zs)
                shift = 0
                for i, context_size in enumerate(self.context_sizes):
                    cs_i = cs[:,shift:(shift+context_size)]
                    zcs += self.context_effects[i]([cs_i,zs])
                    shift += context_size
                zs += zcs

            if (self.perturb_size>0) and (ps is not None):
                zs += self.perturb_effect([ps, zs])
                
            if (np.sum(self.covariate_sizes)>0) and (fs is not None):
                zfs = torch.zeros(batch_size, self.covariate_dim).to(self.get_device())
                shift = 0
                for i, covariate_size in enumerate(self.covariate_sizes):
                    fs_i = fs[:,shift:(shift+covariate_size)]
                    zfs += self.covariate_effects[i](fs_i)#.repeat(1,self.latent_dim)
                    shift += covariate_size
            else:
                zfs = torch.zeros(batch_size, self.covariate_dim).to(self.get_device())

            zps = pyro.sample('latent', ZukoToPyro(self.latent_decoder(zs)))
            log_mu = self.decoder_log_mu([zps,zfs])
            if self.loss_func in ['bernoulli']:
                log_theta = log_mu
            elif self.loss_func in ['negbinomial']:
                mu = log_mu.exp()
            else:
                rate = log_mu.exp()
                theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                if self.loss_func == 'poisson':
                    rate = theta * torch.sum(xs, dim=1, keepdim=True)

            if self.loss_func == 'negbinomial':
                if self.use_zeroinflate:
                    pyro.sample("x", MyZINB(mu=mu, theta=dispersion, zi_logits=gate_logits).to_event(1), obs=xs)
                else:
                    pyro.sample("x", MyNB(mu=mu, theta=dispersion).to_event(1), obs=xs)
            elif self.loss_func == 'poisson':
                if self.use_zeroinflate:
                    pyro.sample('x', dist.ZeroInflatedDistribution(dist.Poisson(rate=rate),gate_logits=gate_logits).to_event(1), obs=xs.round())
                else:
                    pyro.sample('x', dist.Poisson(rate=rate).to_event(1), obs=xs.round())
            elif self.loss_func == 'multinomial':
                pyro.sample('x', dist.Multinomial(total_count=int(1e8), probs=theta), obs=xs)
            elif self.loss_func == 'bernoulli':
                if self.use_zeroinflate:
                    pyro.sample('x', dist.ZeroInflatedDistribution(dist.Bernoulli(logits=log_theta),gate_logits=gate_logits).to_event(1), obs=xs)
                else:
                    pyro.sample('x', dist.Bernoulli(logits=log_theta).to_event(1), obs=xs)

    def guide(self, xs, cs=None, ps=None, fs=None):
        if self.options is None:
            self.options = dict(dtype=xs.dtype, device=xs.device)
            
        with pyro.plate('data'):
            if self.use_mask:
                xs = mask_matrix(xs, self.mask_ratio)
                
            zn_loc, zn_scale = self.encoder_zn(xs)
            zns = pyro.sample('zn', dist.Normal(zn_loc, zn_scale).to_event(1))
                    
            #alpha = self.encoder_n(zns)
            alpha = self.encoder_alpha(zns)
            ns = pyro.sample('n', dist.OneHotCategorical(logits=alpha))
    
    def _codebook(self):
        I = torch.eye(self.code_dim)
        if self.latent_dist=='studentt':
            _,acs_loc = self.codebook(I)
        else:
            acs_loc = self.codebook(I)
        return acs_loc
    
    def get_codebook(self):
        """
        Return the mean part of metacell codebook
        """
        return tensor_to_numpy(self._codebook())

    def get_kmeans_centroids(self):
        return self.centroids
    
    def _get_cell_embedding(self, xs):           
        zns, _ = self.encoder_zn(xs)
        return zns 
    
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
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, device='cpu')
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        Z = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, _ in dataloader:
                X_batch = X_batch.to(self.get_device())
                zns = self._get_cell_embedding(X_batch)
                Z.append(tensor_to_numpy(zns))
                pbar.update(1)

        Z = np.concatenate(Z)
        return Z
    
    def _code(self, xs):
        #zns,_ = self.encoder_zn(xs)
        zns = self._get_cell_embedding(xs)
        alpha = self.encoder_alpha(zns)
        return alpha
    
    def code(self, xs, batch_size=1024, show_progress=True):
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, device='cpu')
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, _ in dataloader:
                X_batch = X_batch.to(self.get_device())
                a = self._code(X_batch)
                A.append(tensor_to_numpy(a))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def _soft_assignments(self, xs):
        alpha = self._code(xs)
        alpha = self.softmax(alpha)
        return alpha
    
    def soft_assignments(self, xs, batch_size=1024, show_progress=True):
        """
        Map cells to metacells and return the probabilistic values of metacell assignments
        """
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, device='cpu')
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, _ in dataloader:
                X_batch = X_batch.to(self.get_device())
                a = self._soft_assignments(X_batch)
                A.append(tensor_to_numpy(a))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def _hard_assignments(self, xs):
        alpha = self._code(xs)
        res, ind = torch.topk(alpha, 1)
        ns = torch.zeros_like(alpha).scatter_(1, ind, 1.0)
        return ns,ind
    
    def hard_assignments(self, xs, batch_size=1024, show_progress=True):
        """
        Map cells to metacells and return the assigned metacell identities.
        """
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, device='cpu')
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, _ in dataloader:
                X_batch = X_batch.to(self.get_device())
                a,_ = self._hard_assignments(X_batch)
                A.append(tensor_to_numpy(a))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def get_context_effect(self, z_basal, cs, i, batch_size=1024, show_progress=True):
        z_basal = convert_to_tensor(z_basal, dtype=self.dtype, device='cpu')
        cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(z_basal)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for Z_batch, idx in dataloader:
                Z_batch = Z_batch.to(self.get_device())
                C_batch = cs[idx].to(self.get_device())
                
                dzs = self.context_effects[i]([C_batch,Z_batch])
                
                A.append(tensor_to_numpy(dzs))
                pbar.update(1)

        A = np.concatenate(A)
        return A
        
    def get_perturb_effect(self, z_basal, zcs, ps, batch_size=1024, show_progress=True):
        z_basal = convert_to_tensor(z_basal, dtype=self.dtype, device='cpu')
        zcs = convert_to_tensor(zcs, dtype=self.dtype, device='cpu')
        ps = convert_to_tensor(ps, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(z_basal)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for Z_batch, idx in dataloader:
                Z_batch = Z_batch.to(self.get_device())
                C_batch = zcs[idx].to(self.get_device())
                P_batch = ps[idx].to(self.get_device())
                
                dzs = self.perturb_effect([P_batch,Z_batch+C_batch])
                
                A.append(tensor_to_numpy(dzs))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def decode_latent(self, z_basal, batch_size=1024, show_progress=True):
        z_basal = convert_to_tensor(z_basal, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(z_basal)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for Z_batch, idx in dataloader:
                Z_batch = Z_batch.to(self.get_device())
                
                dzs = self.latent_decoder([Z_batch]).sample((10,)).mean(axis=0)
                
                A.append(tensor_to_numpy(dzs))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def predict_cluster(self, xs, batch_size=1024, show_progress=True):
        #zs = self.get_cell_embedding(xs, batch_size=batch_size, show_progress=show_progress)
        zs = self.code(xs, batch_size=batch_size, show_progress=show_progress)
        return self.kmeans.predict(zs)
    
    def predict(self, xs:np.array, cs_list:list, ps:np.array, fs_list:list=None, batch_size=1024, show_progress=True):
        """
        Generate gene expression prediction from given cell data and covariates.
        This function can be used for simulating cells' transcription profiles at new conditions.
        
        :param self: SURE model
        :param xs: Cell data at the source condition
        :param cs: Covariates specifying the target condition for generation
        :param batch_size: Data size per batch
        :param show_progress: Toggle on or off message output
        """
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, dtype=self.dtype, device='cpu')
        if cs_list is not None:
            cs = np.hstack(cs_list)
            cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')
        if ps is not None:
            ps = convert_to_tensor(ps, dtype=self.dtype, device='cpu')
        if fs_list is not None:
            fs = np.hstack(fs_list)
            fs = convert_to_tensor(fs, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, idx in dataloader:
                X_batch = X_batch.to(self.get_device())
                library_size = torch.sum(X_batch, 1, keepdim=True)
                
                z_basal = self._get_cell_embedding(X_batch)
                
                zcs = torch.zeros_like(z_basal)
                if cs_list is not None:
                    C_batch = cs[idx].to(self.get_device())
                    shift = 0
                    for i, context_size in enumerate(self.context_sizes):
                        C_batch_i = C_batch[:, shift:(shift+context_size)]
                        zcs += self.context_effects[i]([C_batch_i,z_basal])
                        shift += context_size
                    z_basal += zcs
                    
                if ps is not None:
                    P_batch = ps[idx].to(self.get_device())
                    z_basal += self.perturb_effect([P_batch,z_basal])
                    
                zfs = torch.zeros(X_batch.shape[0], self.covariate_dim).to(self.get_device())
                if fs_list is not None:
                    F_batch = fs[idx].to(self.get_device())
                    shift = 0
                    for i, covariate_size in enumerate(self.covariate_sizes):
                        F_batch_i = F_batch[:, shift:(shift+covariate_size)]
                        zfs += self.covariate_effects[i](F_batch_i)#.repeat(1,self.latent_dim)
                        shift += covariate_size
                             
                zps = self.latent_decoder([z_basal]).sample((10,)).mean(axis=0)
                log_mu = self.decoder_log_mu([zps,zfs])
                if self.loss_func == 'bernoulli':
                    counts = dist.Bernoulli(logits=log_mu).to_event(1).mean
                else:
                    rate = log_mu.exp()
                    theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                    counts = theta * library_size
            
                A.append(tensor_to_numpy(counts))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def predict_log_mu(self, xs:np.array, cs_list:list, ps:np.array, fs_list:list=None, batch_size=1024, show_progress=True):
        """
        Generate gene expression prediction from given cell data and covariates.
        This function can be used for simulating cells' transcription profiles at new conditions.
        
        :param self: SURE model
        :param xs: Cell data at the source condition
        :param cs: Covariates specifying the target condition for generation
        :param batch_size: Data size per batch
        :param show_progress: Toggle on or off message output
        """
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, dtype=self.dtype, device='cpu')
        if cs_list is not None:
            cs = np.hstack(cs_list)
            cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')
        if ps is not None:
            ps = convert_to_tensor(ps, dtype=self.dtype, device='cpu')
        if fs_list is not None:
            fs = np.hstack(fs_list)
            fs = convert_to_tensor(fs, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, idx in dataloader:
                X_batch = X_batch.to(self.get_device())
                library_size = torch.sum(X_batch, 1, keepdim=True)
                
                z_basal = self._get_cell_embedding(X_batch)
                
                zcs = torch.zeros_like(z_basal)
                if cs_list is not None:
                    C_batch = cs[idx].to(self.get_device())
                    shift = 0
                    for i, context_size in enumerate(self.context_sizes):
                        C_batch_i = C_batch[:, shift:(shift+context_size)]
                        zcs += self.context_effects[i]([C_batch_i,z_basal])
                        shift += context_size
                    z_basal += zcs
                    
                if ps is not None:
                    P_batch = ps[idx].to(self.get_device())
                    z_basal += self.perturb_effect([P_batch,z_basal])
                    
                zfs = torch.zeros(X_batch.shape[0], self.covariate_dim).to(self.get_device())
                if fs_list is not None:
                    F_batch = fs[idx].to(self.get_device())
                    shift = 0
                    for i, covariate_size in enumerate(self.covariate_sizes):
                        F_batch_i = F_batch[:, shift:(shift+covariate_size)]
                        zfs += self.covariate_effects[i](F_batch_i)#.repeat(1,self.latent_dim)
                        shift += covariate_size
                                
                zps = self.latent_decoder([z_basal]).sample((10,)).mean(axis=0)
                log_mu = self.decoder_log_mu([zps,zfs])
            
                A.append(tensor_to_numpy(log_mu))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def decode(self, xs:np.array, zs:np.array, zfs:np.array, batch_size=1024, show_progress=True):
        """
        Generate gene expression prediction from given cell data and covariates.
        This function can be used for simulating cells' transcription profiles at new conditions.
        
        :param self: SURE model
        :param xs: Cell data at the source condition
        :param cs: Covariates specifying the target condition for generation
        :param batch_size: Data size per batch
        :param show_progress: Toggle on or off message output
        """
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, dtype=self.dtype, device='cpu')
        zs = convert_to_tensor(zs, dtype=self.dtype, device='cpu')
        zfs = convert_to_tensor(zfs, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, idx in dataloader:
                X_batch = X_batch.to(self.get_device())
                library_size = torch.sum(X_batch, 1, keepdim=True)
                
                z_latent = zs[idx].to(self.get_device())
                z_covariate = zfs[idx].to(self.get_device())
                                
                log_mu = self.decoder_log_mu([z_latent,z_covariate])
                if self.loss_func == 'bernoulli':
                    counts = dist.Bernoulli(logits=log_mu).to_event(1).mean
                else:
                    rate = log_mu.exp()
                    theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                    counts = theta * library_size
            
                A.append(tensor_to_numpy(counts))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def decode_log_mu(self, xs:np.array, zs:np.array, zfs:np.array, batch_size=1024, show_progress=True):
        """
        Generate gene expression prediction from given cell data and covariates.
        This function can be used for simulating cells' transcription profiles at new conditions.
        
        :param self: SURE model
        :param xs: Cell data at the source condition
        :param cs: Covariates specifying the target condition for generation
        :param batch_size: Data size per batch
        :param show_progress: Toggle on or off message output
        """
        xs = self.preprocess(xs)
        xs = convert_to_tensor(xs, dtype=self.dtype, device='cpu')
        zs = convert_to_tensor(zs, dtype=self.dtype, device='cpu')
        zfs = convert_to_tensor(zfs, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for X_batch, idx in dataloader:
                X_batch = X_batch.to(self.get_device())
                library_size = torch.sum(X_batch, 1, keepdim=True)
                
                z_latent = zs[idx].to(self.get_device())
                z_covariate = zfs[idx].to(self.get_device())
                                
                log_mu = self.decoder_log_mu([z_latent,z_covariate])
            
                A.append(tensor_to_numpy(log_mu))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def preprocess(self, xs, threshold=0):
        if self.loss_func == 'bernoulli':
            ad = sc.AnnData(xs)
            binarize(ad, threshold=threshold)
            xs = ad.X.copy()
        else:
            xs = np.round(xs)
            
        if sparse.issparse(xs):
            xs = xs.toarray()
        return xs 
    
    '''def fit(self, xs, 
            cs = None, 
            num_epochs: int = 100, 
            learning_rate: float = 0.0001, 
            batch_size: int = 256, 
            algo: Literal['adam','rmsprop','adamw'] = 'adam', 
            beta_1: float = 0.9, 
            weight_decay: float = 0.005, 
            decay_rate: float = 0.9,
            config_enum: str = 'parallel',
            threshold: int = 0,
            use_jax: bool = True,
            show_progress: bool = True):
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
        xs = self.preprocess(xs, threshold=threshold)
        xs = convert_to_tensor(xs, dtype=self.dtype, device='cpu')
        if cs is not None:
            cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')

        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # setup the optimizer
        optim_params = {'lr': learning_rate, 'betas': (beta_1, 0.999), 'weight_decay': weight_decay}

        if algo.lower()=='rmsprop':
            optimizer = torch.optim.RMSprop
        elif algo.lower()=='adam':
            optimizer = torch.optim.Adam
        elif algo.lower() == 'adamw':
            optimizer = torch.optim.AdamW
        else:
            raise ValueError("An optimization algorithm must be specified.")
        scheduler = ExponentialLR({'optimizer': optimizer, 'optim_args': optim_params, 'gamma': decay_rate})

        pyro.clear_param_store()

        # set up the loss(es) for inference, wrapping the guide in config_enumerate builds the loss as a sum
        # by enumerating each class label form the sampled discrete categorical distribution in the model
        Elbo = JitTraceEnum_ELBO if use_jax else TraceEnum_ELBO
        elbo = Elbo(max_plate_nesting=1, strict_enumeration_warning=False)
        guide = config_enumerate(self.guide, config_enum, expand=True)
        loss_basic = SVI(self.model, guide, scheduler, loss=elbo)

        # build a list of all losses considered
        losses = [loss_basic]
        num_losses = len(losses)

        with tqdm(total=num_epochs, disable=not show_progress, desc='Training', unit='epoch') as pbar:
            for epoch in range(num_epochs):
                epoch_losses = [0.0] * num_losses
                for batch_x, idx in dataloader:
                    batch_x = batch_x.to(self.get_device())
                    for loss_id in range(num_losses):
                        if cs is None:
                            new_loss = losses[loss_id].step(batch_x)
                        else:
                            batch_c = cs[idx].to(self.get_device())
                            new_loss = losses[loss_id].step(batch_x, batch_c)
                        epoch_losses[loss_id] += new_loss

                avg_epoch_losses_ = map(lambda v: v / len(dataloader), epoch_losses)
                avg_epoch_losses = map(lambda v: "{:.4f}".format(v), avg_epoch_losses_)

                # store the loss
                str_loss = " ".join(map(str, avg_epoch_losses))

                # Update progress bar
                pbar.set_postfix({'loss': str_loss})
                pbar.update(1)'''

    def fit(self, xs: np.array, 
            css: list = None, 
            ps: np.array = None,
            fss: list = None,
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
        Train the SURENF model.

        Parameters
        ----------
        xs
            Single-cell expression matrix. It should be a Numpy array or a Pytorch Tensor. 
            Rows are cells and columns are features.
        cs
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
        patience
            Number of epochs with no improvement after which training will be stopped.
        min_delta
            Minimum change in the monitored quantity to qualify as an improvement.
        restore_best_weights
            Whether to restore model weights from the epoch with the best value of the monitored quantity.
        monitor
            Quantity to be monitored. Currently supports 'loss'.
        use_jax
            If toggled on, Jax will be used for speeding up.
        show_progress
            Whether to show training progress bar.
        """
        self.use_mask = use_mask
        self.mask_ratio = mask_ratio
        
        xs = self.preprocess(xs, threshold=threshold)
        xs = convert_to_tensor(xs, dtype=self.dtype, device='cpu')
        if css is not None:
            cs = np.hstack(css)
            cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')
        if ps is not None:
            ps = convert_to_tensor(ps, dtype=self.dtype, device='cpu')
        if fss is not None:
            fs = np.hstack(fss)
            fs = convert_to_tensor(fs, dtype=self.dtype, device='cpu')

        dataset = CustomDataset(xs)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # setup the optimizer
        optim_params = {'lr': learning_rate, 'betas': (beta_1, 0.999), 'weight_decay': weight_decay}

        if algo.lower()=='rmsprop':
            optimizer_class = torch.optim.RMSprop
        elif algo.lower()=='adam':
            optimizer_class = torch.optim.Adam
        elif algo.lower() == 'adamw':
            optimizer_class = torch.optim.AdamW
        else:
            raise ValueError("An optimization algorithm must be specified.")
        
        # 初始化优化器
        scheduler_config = {
            'optimizer': optimizer_class, 
            'optim_args': optim_params, 
            'gamma': decay_rate
        }
        
        pyro.clear_param_store()

        # set up the loss(es) for inference
        Elbo = JitTraceEnum_ELBO if use_jax else TraceEnum_ELBO
        elbo = Elbo(max_plate_nesting=1, strict_enumeration_warning=False)
        guide = config_enumerate(self.guide, config_enum, expand=True)
        
        # 创建 scheduler
        scheduler = ExponentialLR(scheduler_config)
        loss_basic = SVI(self.model, guide, scheduler, loss=elbo)

        # build a list of all losses considered
        losses = [loss_basic]
        num_losses = len(losses)
        
        # Early stopping 初始化
        best_loss = float('inf')
        best_epoch = 0
        patience_counter = 0
        
        # 保存最佳状态
        best_state = None
        
        with tqdm(total=num_epochs, disable=not show_progress, desc='Training', unit='epoch') as pbar:
            for epoch in range(num_epochs):
                epoch_losses = [0.0] * num_losses
                for batch_x, idx in dataloader:
                    batch_x = batch_x.to(self.get_device())
                    for loss_id in range(num_losses):
                        if css is None:
                            batch_c = None
                        else:
                            batch_c = cs[idx].to(self.get_device())
                        if ps is None:
                            batch_p = None
                        else:
                            batch_p = ps[idx].to(self.get_device())
                        if fss is None:
                            batch_f = None
                        else:
                            batch_f = fs[idx].to(self.get_device())
                            
                        new_loss = losses[loss_id].step(xs=batch_x, cs=batch_c, ps=batch_p, fs=batch_f)
                        epoch_losses[loss_id] += new_loss

                avg_epoch_losses_ = list(map(lambda v: v / len(dataloader), epoch_losses))
                avg_epoch_losses_str = list(map(lambda v: "{:.4f}".format(v), avg_epoch_losses_))
                
                # 计算当前 epoch 的总损失
                current_loss = sum(avg_epoch_losses_)
                
                # Early stopping 逻辑
                if current_loss < best_loss - min_delta:
                    # 有显著改进
                    best_loss = current_loss
                    best_epoch = epoch
                    patience_counter = 0
                    
                    # 保存最佳状态（模型参数 + 优化器状态）
                    if restore_best_weights:
                        best_state = self.get_model_and_optimizer_state(scheduler)
                        
                    pbar.set_postfix({
                        'loss': ' '.join(avg_epoch_losses_str),
                        'best': f"{best_loss:.4f}",
                        'patience': f"{patience_counter}/{patience}"
                    })
                else:
                    # 没有改进
                    patience_counter += 1
                    pbar.set_postfix({
                        'loss': ' '.join(avg_epoch_losses_str),
                        'best': f"{best_loss:.4f}",
                        'patience': f"{patience_counter}/{patience}"
                    })
                    
                    # 检查是否应该提前停止
                    if patience_counter >= patience:
                        print(f"\nEarly stopping triggered at epoch {epoch + 1}")
                        print(f"Best loss {best_loss:.4f} achieved at epoch {best_epoch + 1}")
                        
                        # 恢复最佳状态
                        if restore_best_weights and best_state is not None:
                            self.load_model_and_optimizer_state(best_state, scheduler)
                            print("Restored model and optimizer states from best epoch.")
                        
                        break
                
                pbar.update(1)
            
            # 训练完成（达到最大 epoch 数）
            if epoch == num_epochs - 1:
                print(f"\nTraining completed. Best loss {best_loss:.4f} at epoch {best_epoch + 1}")
                if restore_best_weights and best_state is not None:
                    self.load_model_and_optimizer_state(best_state, scheduler)
                    print("Restored model and optimizer states from best epoch.")
        
        xs = tensor_to_numpy(xs)
        #zs = self.get_cell_embedding(xs, show_progress=False)     
        zs = self.code(xs, batch_size=batch_size, show_progress=False)   
        self.kmeans.fit(zs)
        self.centroids = self.kmeans.cluster_centers_

    def get_model_and_optimizer_state(self, scheduler=None):
        """获取模型和优化器的完整状态"""
        state_dict = {
            'model_params': dict(pyro.get_param_store()),  # 保存所有参数
        }
        
        # 保存优化器状态
        if scheduler is not None and hasattr(scheduler, 'optimizer'):
            # Pyro scheduler 通常包含 optimizer
            optimizer = scheduler.optimizer
            if optimizer is not None:
                state_dict['optimizer_state'] = optimizer.state_dict()
        
        # 保存 scheduler 状态
        if scheduler is not None and hasattr(scheduler, 'scheduler'):
            scheduler_obj = scheduler.scheduler
            if scheduler_obj is not None and hasattr(scheduler_obj, 'state_dict'):
                state_dict['scheduler_state'] = scheduler_obj.state_dict()
        
        return state_dict

    def load_model_and_optimizer_state(self, state_dict, scheduler=None):
        """加载模型和优化器的完整状态"""
        
        # 1. 加载模型参数
        if 'model_params' in state_dict:
            param_store = pyro.get_param_store()
            for name, value in state_dict['model_params'].items():
                # 确保参数存在
                if name in param_store:
                    # 创建可训练的参数
                    param_store[name] = value.clone().detach().requires_grad_(True)
                else:
                    # 如果参数不存在，则创建它
                    param_store[name] = torch.nn.Parameter(
                        value.clone().detach().requires_grad_(True)
                    )
        
        # 2. 加载优化器状态
        if scheduler is not None and 'optimizer_state' in state_dict:
            optimizer = scheduler.optimizer
            if optimizer is not None:
                # 确保优化器的参数与当前模型参数匹配
                current_params = dict(pyro.get_param_store())
                
                # 创建一个新的状态字典，只包含当前存在的参数
                filtered_optimizer_state = {
                    'state': {},
                    'param_groups': state_dict['optimizer_state']['param_groups']
                }
                
                # 过滤状态，只保留当前存在的参数
                for param_idx, param_state in state_dict['optimizer_state']['state'].items():
                    # 检查参数是否仍然存在
                    param_key = f'Param_{param_idx}'
                    if param_idx < len(optimizer.param_groups[0]['params']):
                        filtered_optimizer_state['state'][param_idx] = param_state
                
                optimizer.load_state_dict(filtered_optimizer_state)
        
        # 3. 加载 scheduler 状态
        if (scheduler is not None and 
            'scheduler_state' in state_dict and 
            hasattr(scheduler, 'scheduler')):
            scheduler_obj = scheduler.scheduler
            if (scheduler_obj is not None and 
                hasattr(scheduler_obj, 'load_state_dict')):
                scheduler_obj.load_state_dict(state_dict['scheduler_state'])

    def get_optimizer_param_mapping(self, optimizer):
        """获取优化器参数到模型参数的映射关系"""
        if optimizer is None:
            return {}
        
        mapping = {}
        param_store = dict(pyro.get_param_store())
        
        for group_idx, param_group in enumerate(optimizer.param_groups):
            for param_idx, param in enumerate(param_group['params']):
                # 找到对应的模型参数名
                for name, model_param in param_store.items():
                    if param is model_param or torch.equal(param, model_param):
                        mapping[f'group{group_idx}_param{param_idx}'] = name
                        break
        
        return mapping

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

        

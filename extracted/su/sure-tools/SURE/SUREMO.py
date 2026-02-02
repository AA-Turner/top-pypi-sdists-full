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

import zuko 
from pyro.contrib.zuko import ZukoToPyro

import os
import argparse
import random
import numpy as np
import datatable as dt
from tqdm import tqdm
from scipy import sparse

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


class SUREMO(nn.Module):
    """SUccinct REpresentation of multi-omics cells

    :param rna_dim: Number of genes per cell
    :param atac_dim: Number of chromatin accessibility regions per cell
    :param codebook_size: Number of metacells
    :param covariate_size: Number of cell-level factors
    :param z_dim: Dimensionality of latent states and metacells
    :param z_dist: Distribution model of latent variable
    :param rna_loss_func: The likelihood model for rna data generation
        One of the following: 
        * ``'negbinomial'`` -  negative binomial distribution (default)
        * ``'poisson'`` - poisson distribution
        * ``'multinomial'`` - multinomial distribution
        * ``'bernoulli'`` - bernoulli distribution
    :param atac_loss_func: The likelihood model for atac data generation
        One of the following: 
        * ``'negbinomial'`` -  negative binomial distribution (default)
        * ``'poisson'`` - poisson distribution
        * ``'multinomial'`` - multinomial distribution
        * ``'bernoulli'`` - bernoulli distribution
    :param use_zeroinflate: Toggle on zero-inflation model or off
    :param hidden_layers: A list gives the numbers of neurons for each hidden layer
    :param use_cuda: A boolean option for switching on cuda device

    """
    def __init__(self,
                 rna_dim: int,
                 atac_dim: int,
                 codebook_size: int,
                 covariate_size: int = 0,
                 z_dim: int = 50,
                 z_dist: Literal['normal','studentt','laplacian','cauchy','gumbel'] = 'studentt',
                 rna_loss_func: Literal['negbinomial','poisson','multinomial','bernoulli'] = 'multinomial',
                 atac_loss_func: Literal['negbinomial','poisson','multinomial','bernoulli'] = 'multinomial',
                 dispersion: float = 10.0,
                 use_zeroinflate: bool = True,
                 hidden_layers: list = [500],
                 hidden_layer_activation: Literal['relu','softplus','leakyrelu','linear'] = 'relu',
                 nn_dropout: float = 0.1,
                 post_layer_fct: list = ['layernorm'],
                 post_act_fct: list = None,
                 config_enum: str = 'parallel',
                 use_cuda: bool = True,
                 seed: int = 42,
                 dtype = torch.float32, # type: ignore
                 ):
        super().__init__()

        self.rna_dim = rna_dim
        self.atac_dim = atac_dim
        self.covariate_size = covariate_size
        self.dispersion = dispersion
        self.latent_dim = z_dim
        self.latent_dist = z_dist
        self.hidden_layers = hidden_layers
        self.decoder_hidden_layers = hidden_layers[::-1]
        self.allow_broadcast = config_enum == 'parallel'
        self.use_cuda = use_cuda
        self.rna_loss_func = rna_loss_func
        self.atac_loss_func = atac_loss_func
        self.options = None
        self.code_dim=codebook_size
        self.dtype = dtype
        self.use_zeroinflate=use_zeroinflate
        self.nn_dropout = nn_dropout
        self.post_layer_fct = post_layer_fct
        self.post_act_fct = post_act_fct
        self.hidden_layer_activation = hidden_layer_activation
        
        self.codebook_weights = None
        self.codebook_loc = None
        
        self.use_mask = False
        self.mask_ratio = 0
        
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
            [self.rna_dim + self.atac_dim] + hidden_sizes + [[latent_dim, latent_dim]],
            activation=activate_fct,
            output_activation=[None, Exp],
            post_layer_fct=post_layer_fct,
            post_act_fct=post_act_fct,
            allow_broadcast=self.allow_broadcast,
            use_cuda=self.use_cuda,
        )

        if self.covariate_size>0:
            self.covariate_effect = ZeroBiasMLP2(
                [self.covariate_size] + self.decoder_hidden_layers + [self.latent_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )
            
        self.decoder_rna_log_mu = MLP(
                [self.latent_dim] + self.decoder_hidden_layers + [self.rna_dim],
                activation=activate_fct,
                output_activation=None,
                post_layer_fct=post_layer_fct,
                post_act_fct=post_act_fct,
                allow_broadcast=self.allow_broadcast,
                use_cuda=self.use_cuda,
            )
        
        self.decoder_atac_log_mu = MLP(
                [self.latent_dim] + self.decoder_hidden_layers + [self.atac_dim],
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

    def model(self, xs_rna, xs_atac, cs=None):
        pyro.module('sure', self)

        eps = torch.finfo(xs_rna.dtype).eps
        batch_size = xs_rna.size(0)
        self.options = dict(dtype=xs_rna.dtype, device=xs_rna.device)
        
        if self.rna_loss_func=='negbinomial':
            rna_dispersion = pyro.param("rna_dispersion", self.dispersion *
                                     xs_rna.new_ones(self.rna_dim), constraint=constraints.positive)
            
        if self.atac_loss_func=='negbinomial':
            atac_dispersion = pyro.param("atac_dispersion", self.dispersion *
                                     xs_rna.new_ones(self.atac_dim), constraint=constraints.positive)
            
        if self.use_zeroinflate:
            rna_gate_logits = pyro.param("rna_dropout_rate", xs_rna.new_zeros(self.rna_dim))
            atac_gate_logits = pyro.param("atac_dropout_rate", xs_rna.new_zeros(self.atac_dim))

        acs_scale = pyro.param("codebook_scale", xs_rna.new_ones(self.latent_dim), constraint=constraints.positive)

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
                
            if (self.covariate_size>0) and (cs is not None):
                zus = self.covariate_effect(cs)
                zs = zns+zus
            else:
                zs = zns

            # rna generation
            rna_log_mu = self.decoder_rna_log_mu(zs)
            if self.rna_loss_func in ['bernoulli']:
                log_theta = rna_log_mu
            elif self.rna_loss_func in ['negbinomial']:
                mu = rna_log_mu.exp()
            else:
                rate = rna_log_mu.exp()
                theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                if self.rna_loss_func == 'poisson':
                    rate = theta * torch.sum(rna_log_mu, dim=1, keepdim=True)

            if self.rna_loss_func == 'negbinomial':
                if self.use_zeroinflate:
                    pyro.sample("rna", MyZINB(mu=mu, theta=rna_dispersion, zi_logits=rna_gate_logits).to_event(1), obs=xs_rna)
                else:
                    pyro.sample("rna", MyNB(mu=mu, theta=rna_dispersion).to_event(1), obs=xs_rna)
            elif self.rna_loss_func == 'poisson':
                if self.use_zeroinflate:
                    pyro.sample('rna', dist.ZeroInflatedDistribution(dist.Poisson(rate=rate),gate_logits=rna_gate_logits).to_event(1), obs=xs_rna.round())
                else:
                    pyro.sample('rna', dist.Poisson(rate=rate).to_event(1), obs=xs_rna.round())
            elif self.rna_loss_func == 'multinomial':
                pyro.sample('rna', dist.Multinomial(total_count=int(1e8), probs=theta), obs=xs_rna)
            elif self.rna_loss_func == 'bernoulli':
                if self.use_zeroinflate:
                    pyro.sample('rna', dist.ZeroInflatedDistribution(dist.Bernoulli(logits=log_theta),gate_logits=rna_gate_logits).to_event(1), obs=xs_rna)
                else:
                    pyro.sample('rna', dist.Bernoulli(logits=log_theta).to_event(1), obs=xs_rna)
                    
            # atac generation
            atac_log_mu = self.decoder_atac_log_mu(zs)
            if self.atac_loss_func in ['bernoulli']:
                log_theta = atac_log_mu
            elif self.atac_loss_func in ['negbinomial']:
                mu = atac_log_mu.exp()
            else:
                rate = atac_log_mu.exp()
                theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                if self.atac_loss_func == 'poisson':
                    rate = theta * torch.sum(atac_log_mu, dim=1, keepdim=True)

            if self.atac_loss_func == 'negbinomial':
                if self.use_zeroinflate:
                    pyro.sample("atac", MyZINB(mu=mu, theta=atac_dispersion, zi_logits=atac_gate_logits).to_event(1), obs=xs_atac)
                else:
                    pyro.sample("atac", MyNB(mu=mu, theta=atac_dispersion).to_event(1), obs=xs_atac)
            elif self.atac_loss_func == 'poisson':
                if self.use_zeroinflate:
                    pyro.sample('atac', dist.ZeroInflatedDistribution(dist.Poisson(rate=rate),gate_logits=atac_gate_logits).to_event(1), obs=xs_atac.round())
                else:
                    pyro.sample('atac', dist.Poisson(rate=rate).to_event(1), obs=xs_atac.round())
            elif self.atac_loss_func == 'multinomial':
                pyro.sample('atac', dist.Multinomial(total_count=int(1e8), probs=theta), obs=xs_atac)
            elif self.atac_loss_func == 'bernoulli':
                if self.use_zeroinflate:
                    pyro.sample('atac', dist.ZeroInflatedDistribution(dist.Bernoulli(logits=log_theta),gate_logits=atac_gate_logits).to_event(1), obs=xs_atac)
                else:
                    pyro.sample('atac', dist.Bernoulli(logits=log_theta).to_event(1), obs=xs_atac)

    def guide(self, xs_rna, xs_atac, cs=None):
        if self.options is None:
            self.options = dict(dtype=xs_rna.dtype, device=xs_rna.device)
            
        with pyro.plate('data'):
            if self.use_mask:
                xs_rna = mask_matrix(xs_rna, self.mask_ratio)
                xs_atac = mask_matrix(xs_atac, self.mask_ratio)
                
            zn_loc, zn_scale = self.encoder_zn([xs_rna, xs_atac])
            zns = pyro.sample('zn', dist.Normal(zn_loc, zn_scale).to_event(1))

            #alpha = self.encoder_n(zns)
            alpha = self.encoder_alpha(zns)
            ns = pyro.sample('n', dist.OneHotCategorical(logits=alpha))
    
    def get_codebook(self):
        """
        Return the mean part of metacell codebook
        """
        return self.codebook_loc

    def _get_cell_embedding(self, xs_rna, xs_atac):           
        zns, _ = self.encoder_zn([xs_rna, xs_atac])
        return zns 
    
    def get_cell_embedding(self, 
                             xs_rna, xs_atac, 
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
        xs_rna = self.preprocess(xs_rna, 'rna')
        xs_rna = convert_to_tensor(xs_rna, device='cpu')
        xs_atac = self.preprocess(xs_atac, 'atac')
        xs_atac = convert_to_tensor(xs_atac, device='cpu')
        dataset = CustomDataset(xs_rna)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        Z = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for RNA_batch, idx in dataloader:
                RNA_batch = RNA_batch.to(self.get_device())
                ATAC_batch = xs_atac[idx].to(self.get_device())
                zns = self._get_cell_embedding(RNA_batch, ATAC_batch)
                Z.append(tensor_to_numpy(zns))
                pbar.update(1)

        Z = np.concatenate(Z)
        return Z
    
    def _code(self, xs_rna, xs_atac):
        #zns,_ = self.encoder_zn(xs)
        zns = self._get_cell_embedding(xs_rna,xs_atac)
        alpha = self.encoder_alpha(zns)
        return alpha
    
    def code(self, xs_rna, xs_atac, batch_size=1024, show_progress=True):
        xs_rna = self.preprocess(xs_rna, 'rna')
        xs_rna = convert_to_tensor(xs_rna, device='cpu')
        xs_atac = self.preprocess(xs_atac, 'atac')
        xs_atac = convert_to_tensor(xs_atac, device='cpu')
        dataset = CustomDataset(xs_rna)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for RNA_batch, idx in dataloader:
                RNA_batch = RNA_batch.to(self.get_device())
                ATAC_batch = xs_atac[idx].to(self.get_device())
                a = self._code(RNA_batch, ATAC_batch)
                A.append(tensor_to_numpy(a))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def _soft_assignments(self, xs_rna, xs_atac):
        alpha = self._code(xs_rna, xs_atac)
        alpha = self.softmax(alpha)
        return alpha
    
    def soft_assignments(self, xs_rna, xs_atac, batch_size=1024, show_progress=True):
        """
        Map cells to metacells and return the probabilistic values of metacell assignments
        """
        xs_rna = self.preprocess(xs_rna, 'rna')
        xs_rna = convert_to_tensor(xs_rna, device='cpu')
        xs_atac = self.preprocess(xs_atac, 'atac')
        xs_atac = convert_to_tensor(xs_atac, device='cpu')
        dataset = CustomDataset(xs_rna)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for RNA_batch, idx in dataloader:
                RNA_batch = RNA_batch.to(self.get_device())
                ATAC_batch = xs_atac[idx].to(self.get_device())
                a = self._soft_assignments(RNA_batch, ATAC_batch)
                A.append(tensor_to_numpy(a))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def _hard_assignments(self, xs_rna, xs_atac):
        alpha = self._code(xs_rna, xs_atac)
        res, ind = torch.topk(alpha, 1)
        ns = torch.zeros_like(alpha).scatter_(1, ind, 1.0)
        return ns,ind
    
    def hard_assignments(self, xs_rna, xs_atac, batch_size=1024, show_progress=True):
        """
        Map cells to metacells and return the assigned metacell identities.
        """
        xs_rna = self.preprocess(xs_rna, 'rna')
        xs_rna = convert_to_tensor(xs_rna, device='cpu')
        xs_atac = self.preprocess(xs_atac, 'atac')
        xs_atac = convert_to_tensor(xs_atac, device='cpu')
        dataset = CustomDataset(xs_rna)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        A = []
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for RNA_batch, idx in dataloader:
                RNA_batch = RNA_batch.to(self.get_device())
                ATAC_batch = xs_atac[idx].to(self.get_device())
                a,_ = self._hard_assignments(RNA_batch, ATAC_batch)
                A.append(tensor_to_numpy(a))
                pbar.update(1)

        A = np.concatenate(A)
        return A
    
    def predict(self, xs_rna, xs_atac, cs, batch_size=1024, show_progress=True):
        """
        Generate gene expression prediction from given cell data and covariates.
        This function can be used for simulating cells' transcription profiles at new conditions.
        
        :param self: SURE model
        :param xs_rna: RNA data at the source condition
        :param xs_atac: ATAC data at the source condition
        :param cs: Covariates specifying the target condition for generation
        :param batch_size: Data size per batch
        :param show_progress: Toggle on or off message output
        """
        xs_rna = self.preprocess(xs_rna, 'rna')
        xs_rna = convert_to_tensor(xs_rna, device='cpu')
        xs_atac = self.preprocess(xs_atac, 'atac')
        xs_atac = convert_to_tensor(xs_atac, device='cpu')
        cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')
        
        dataset = CustomDataset(xs_rna)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        RNA,ATAC = [],[]
        with tqdm(total=len(dataloader), disable=not show_progress, desc='', unit='batch') as pbar:
            for RNA_batch, idx in dataloader:
                RNA_batch = RNA_batch.to(self.get_device())
                ATAC_batch = xs_atac[idx].to(self.get_device())
                C_batch = cs[idx].to(self.get_device())
                rna_library_size = torch.sum(RNA_batch, 1)
                atac_library_size = torch.sum(ATAC_batch, 1)
                
                z_basal = self._get_cell_embedding(RNA_batch,ATAC_batch)
                dzs = self.covariate_effect(C_batch)
                zs = z_basal + dzs 
                
                # rna
                log_mu = self.decoder_rna_log_mu(zs)
                if self.rna_loss_func == 'bernoulli':
                    counts = dist.Bernoulli(logits=log_mu).to_event(1).mean
                else:
                    rate = log_mu.exp()
                    theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                    counts = theta * rna_library_size
            
                RNA.append(tensor_to_numpy(counts))
                
                # atac
                log_mu = self.decoder_atac_log_mu(zs)
                if self.atac_loss_func == 'bernoulli':
                    counts = dist.Bernoulli(logits=log_mu).to_event(1).mean
                else:
                    rate = log_mu.exp()
                    theta = dist.DirichletMultinomial(total_count=1, concentration=rate).mean
                    counts = theta * atac_library_size
            
                ATAC.append(tensor_to_numpy(counts))
                
                pbar.update(1)

        RNA = np.concatenate(RNA)
        ATAC = np.concatenate(ATAC)
        return RNA,ATAC
    
    def preprocess(self, xs, modality, threshold=0):
        if modality=='rna':
            loss_func = self.rna_loss_func
        else:
            loss_func = self.atac_loss_func
            
        if loss_func == 'bernoulli':
            ad = sc.AnnData(xs)
            binarize(ad, threshold=threshold)
            xs = ad.X.copy()
        else:
            xs = np.round(xs)
            
        if sparse.issparse(xs):
            xs = xs.toarray()
        return xs 
    
    def fit(self, xs_rna, xs_atac, 
            cs = None, 
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
        
        xs_rna = self.preprocess(xs_rna, 'rna', threshold=threshold)
        xs_rna = convert_to_tensor(xs_rna, device='cpu')
        xs_atac = self.preprocess(xs_atac, 'atac', threshold=threshold)
        xs_atac = convert_to_tensor(xs_atac, device='cpu')
        if cs is not None:
            cs = convert_to_tensor(cs, dtype=self.dtype, device='cpu')

        dataset = CustomDataset(xs_rna)
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
                for batch_rna, idx in dataloader:
                    batch_rna = batch_rna.to(self.get_device())
                    batch_atac = xs_atac[idx].to(self.get_device())
                    for loss_id in range(num_losses):
                        if cs is None:
                            new_loss = losses[loss_id].step(batch_rna, batch_atac)
                        else:
                            batch_c = cs[idx].to(self.get_device())
                            new_loss = losses[loss_id].step(batch_rna, batch_atac, batch_c)
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
        
        ns = self.soft_assignments(xs, show_progress=False)
        zs = self.get_cell_embedding(xs, show_progress=False)
        ns2 = ns.T / np.sum(ns.T, axis=1, keepdims=True)
        self.codebook_loc = ns2 @ zs

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

        
EXAMPLE_RUN = (
    "example run: SURE --help"
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="SURE\n{}".format(EXAMPLE_RUN))

    parser.add_argument(
        "--cuda", action="store_true", help="use GPU(s) to speed up training"
    )
    parser.add_argument(
        "--jit", action="store_true", help="use PyTorch jit to speed up training"
    )
    parser.add_argument(
        "-n", "--num-epochs", default=200, type=int, help="number of epochs to run"
    )
    parser.add_argument(
        "-enum",
        "--enum-discrete",
        default="parallel",
        help="parallel, sequential or none. uses parallel enumeration by default",
    )
    parser.add_argument(
        "-data",
        "--data-file",
        default=None,
        type=str,
        help="the data file",
    )
    parser.add_argument(
        "-cf",
        "--covariate-file",
        default=None,
        type=str,
        help="the file for the record of covariates",
    )
    parser.add_argument(
        "-bs",
        "--batch-size",
        default=1000,
        type=int,
        help="number of cells to be considered in a batch",
    )
    parser.add_argument(
        "-lr",
        "--learning-rate",
        default=0.0001,
        type=float,
        help="learning rate for Adam optimizer",
    )
    parser.add_argument(
        "-cs",
        "--codebook-size",
        default=100,
        type=int,
        help="size of vector quantization codebook",
    )
    parser.add_argument(
        "-zd",
        "--z-dim",
        default=10,
        type=int,
        help="size of the tensor representing the latent variable z variable",
    )
    parser.add_argument(
        "-likeli",
        "--likelihood",
        default='negbinomial',
        type=str,
        choices=['negbinomial', 'multinomial', 'poisson', 'bernoulli'],
        help="specify the distribution likelihood function",
    )
    parser.add_argument(
        "-zi",
        "--zeroinflate",
        action="store_true",
        help="use zeroinflation",
    )
    parser.add_argument(
        "-id",
        "--inverse-dispersion",
        default=10.0,
        type=float,
        help="inverse dispersion prior for negative binomial",
    )
    parser.add_argument(
        "-hl",
        "--hidden-layers",
        nargs="+",
        default=[500],
        type=int,
        help="a tuple (or list) of MLP layers to be used in the neural networks "
        "representing the parameters of the distributions in our model",
    )
    parser.add_argument(
        "-hla",
        "--hidden-layer-activation",
        default='relu',
        type=str,
        choices=['relu','softplus','leakyrelu','linear'],
        help="activation function for hidden layers",
    )
    parser.add_argument(
        "-plf",
        "--post-layer-function",
        nargs="+",
        default=['layernorm'],
        type=str,
        help="post functions for hidden layers, could be none, dropout, layernorm, batchnorm, or combination, default is 'dropout layernorm'",
    )
    parser.add_argument(
        "-paf",
        "--post-activation-function",
        nargs="+",
        default=['none'],
        type=str,
        help="post functions for activation layers, could be none or dropout, default is 'none'",
    )
    parser.add_argument(
        "-dr",
        "--decay-rate",
        default=0.9,
        type=float,
        help="decay rate for Adam optimizer",
    )
    parser.add_argument(
        "--layer-dropout-rate",
        default=0.1,
        type=float,
        help="droput rate for neural networks",
    )
    parser.add_argument(
        "-b1",
        "--beta-1",
        default=0.95,
        type=float,
        help="beta-1 parameter for Adam optimizer",
    )
    parser.add_argument(
        "-64",
        "--float64",
        action="store_true",
        help="use double float precision",
    )
    parser.add_argument(
        "--seed",
        default=None,
        type=int,
        help="seed for controlling randomness in this example",
    )
    parser.add_argument(
        "--save-model",
        default=None,
        type=str,
        help="path to save model for prediction",
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    assert (
        (args.data_file is not None) and (
            os.path.exists(args.data_file))
    ), "data file must be provided"

    if args.seed is not None:
        set_random_seed(args.seed)

    if args.float64:
        dtype = torch.float64
        torch.set_default_dtype(torch.float64)
    else:
        dtype = torch.float32
        torch.set_default_dtype(torch.float32)

    xs = dt.fread(file=args.data_file, header=True).to_numpy()
    us = None 
    if args.covariate_file is not None:
        us = dt.fread(file=args.covariate_file, header=True).to_numpy()

    rna_dim = xs.shape[1]
    covariate_size = 0 if us is None else us.shape[1]

    ###########################################
    sure = SUREMO(
        rna_dim=rna_dim,
        covariate_size=covariate_size,
        dispersion=args.dispersion,
        z_dim=args.z_dim,
        hidden_layers=args.hidden_layers,
        hidden_layer_activation=args.hidden_layer_activation,
        use_cuda=args.cuda,
        config_enum=args.enum_discrete,
        use_zeroinflate=args.zeroinflate,
        loss_func=args.likelihood,
        nn_dropout=args.layer_dropout_rate,
        post_layer_fct=args.post_layer_function,
        post_act_fct=args.post_activation_function,
        codebook_size=args.codebook_size,
        dtype=dtype,
    )

    sure.fit(xs, us=us, 
             num_epochs=args.num_epochs,
             learning_rate=args.learning_rate,
             batch_size=args.batch_size,
             beta_1=args.beta_1,
             decay_rate=args.decay_rate,
             use_jax=args.jit,
             config_enum=args.enum_discrete,
             )

    if args.save_model is not None:
        if args.save_model.endswith('gz'):
            SUREMO.save_model(sure, args.save_model, compression=True)
        else:
            SUREMO.save_model(sure, args.save_model)
    


if __name__ == "__main__":

    main()
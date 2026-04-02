import time

import numpy as np
import torch
from matplotlib import pyplot as plt

from pykeops.torch import LazyTensor

nump = lambda t: t.cpu().numpy()
use_cuda = torch.cuda.is_available()
dtype = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor
M, N = (5000, 5000) if use_cuda else (2000, 2000)

x = (torch.rand(N, 3) - 0.5) * 100

from pykeops.torch.cluster import grid_cluster

eps = 40  # Size of our square bins

x_labels = grid_cluster(x, eps)  # class labels
print(grid_cluster(x, eps).unique())

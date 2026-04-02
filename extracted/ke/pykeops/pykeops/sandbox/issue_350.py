from pykeops.torch import LazyTensor
from pykeops.torch.cluster import (
    grid_cluster,
    from_matrix,
    sort_clusters,
    cluster_ranges_centroids,
)
import torch

#
#
# N, M = 5, 251  # Batch, Sample size, Sample Size, Channel in, Channel out
#
# x = torch.randn(N, 2).cuda()
# y = torch.randn(M, 2).cuda()
#
#
# ## MAKE RANGES
#
# eps = 0.1  # Size of our square bins
#
# alpha = 1 / 100
#
# x_labels = grid_cluster(x, eps)  # class labels
# y_labels = grid_cluster(y, eps)  # class labels
#
# x_ranges, x_centroids, _ = cluster_ranges_centroids(x, x_labels)
# y_ranges, y_centroids, _ = cluster_ranges_centroids(y, y_labels)
#
# x, x_labels = sort_clusters(x, x_labels)
# y, y_labels = sort_clusters(y, y_labels)
#
# keep = (((y_centroids[None, :, :] - x_centroids[:, None, :]) ** 2).sum(-1) - 1 / alpha) < 0
#
# ranges_ij = from_matrix(x_ranges, y_ranges, keep)
#
# ## RUN KEOPS CODE
# x_i = LazyTensor(x.view(N, 1, 2))
# y_j = LazyTensor(y.view(1, M, 2))
#
#
# G_ij =  x_i.keops_kron(y_j, [2], [2])
#
# # G_ij.ranges = ranges_ij
#
# out = G_ij.sum_reduction(axis=1).reshape(N, 2, 2)
# print(out)
#
# ## RUN NAIVE CODE
# out2 = torch.zeros(N, 2, 2).cuda()
# for i in range(N):
#     for j in range(M):
#         out2[i, :, :] += torch.kron(x[i, :], y[j, :]).reshape(2, 2)
#
# print(out2)


## DEFINE VARS AND FUNCTIONS
def apply_lazy_mlp(x, lazy_list):
    """
    Applies a list of lazy tensors to x
    """
    out = x
    for lazy in lazy_list:
        out = lazy.matvecmult(out)
    return out


B, N, M, I, J = (
    8,
    2500,
    2500,
    4,
    16,
)  # Batch, Sample size, Sample Size, Channel in, Channel out

x = torch.randn(N, 2).cuda()
y = torch.randn(M, 2).cuda()
f = torch.randn(B, N, I).cuda()
rho = torch.randn(1, N, 1).cuda()

L1 = LazyTensor(torch.randn(16).cuda())
L2 = LazyTensor(torch.randn(64).cuda())
L3 = LazyTensor(torch.randn(8 * I * J).cuda())

lazy_list = [L1, L2, L3]

## MAKE RANGES

eps = 0.1  # Size of our square bins

alpha = 1 / 100

x_labels = grid_cluster(x, eps)  # class labels
y_labels = grid_cluster(y, eps)  # class labels

x_ranges, x_centroids, _ = cluster_ranges_centroids(x, x_labels)
y_ranges, y_centroids, _ = cluster_ranges_centroids(y, y_labels)

x, x_labels = sort_clusters(x, x_labels)
y, y_labels = sort_clusters(y, y_labels)

keep = (
    ((y_centroids[None, :, :] - x_centroids[:, None, :]) ** 2).sum(-1) - 1 / alpha
) < 0

ranges_ij = from_matrix(x_ranges, y_ranges, keep)

## RUN KEOPS CODE
x_i = LazyTensor(x.view(N, 1, 2))
y_j = LazyTensor(y.view(1, M, 2))

f_i = LazyTensor(f.view(B, N, 1, I))

ex_tensor = LazyTensor(torch.ones(1, 1, 1, J).cuda())

ex_f_i = f_i.keops_kron(ex_tensor, [I], [J])

rho_i = LazyTensor(rho.view(N, 1, 1))

G_ij = ex_f_i

# G_ij.ranges = ranges_ij

out = G_ij.sum_reduction(axis=1).reshape(M, I, J).sum(dim=-2)

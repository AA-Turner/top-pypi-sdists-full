from pykeops.torch import Vi, Vj
import pykeops
import torch
import nvidia_smi

device = "cuda:0"
# pykeops.clean_pykeops()


def kernel(x1: torch.Tensor, x2: torch.Tensor):
    X_i = Vi(0, x1.shape[-1])
    X_j = Vj(1, x2.shape[-1])
    D_ij = ((X_i - X_j) ** 2).sum(-1)
    cont = D_ij.sum(1)
    return cont(x1, x2)


def kernel_torch(x1: torch.Tensor, x2: torch.Tensor):
    D_ij = ((x1[:, None, :] - x2[None, :, :]) ** 2).sum(-1)
    return D_ij.sum(1)


def get_free_mem():
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    print(
        "Memory : ({:.2f}% free): {}(total), {} (free), {} (used), {} (occupied)".format(
            100 * info.free / info.total,
            info.total,
            info.free,
            info.used,
            torch.cuda.mem_get_info(device=device)[1],
        )
    )
    return info.free


if __name__ == "__main__":
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    n_points = 1638 * 1
    n_iter = 10000

    current_free = -1

    for iter in range(n_iter):
        points1 = torch.rand((n_points, 1), device=device)
        points2 = torch.rand((n_points, 1), device=device)
        with torch.no_grad():
            output = kernel(points1, points2)
            # equivalent torch code that do not produce leaks

            # output_torch = kernel_torch(points1, points2)
            # print(torch.allclose(output.squeeze(), output_torch.squeeze()))

        info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        if info.free != current_free:
            print(f"Iter {iter} : ", end=" ")
            current_free = get_free_mem()

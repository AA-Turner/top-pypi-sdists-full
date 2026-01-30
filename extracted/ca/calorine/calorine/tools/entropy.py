from warnings import warn
import numpy as np

try:
    import torch
    torch_available = True
except ImportError:  # pragma: no cover
    torch_available = False
    # If pytorch is not available, we still need a torch object
    # to satisfy type hints etc. Otherwise the file will not run.

    class _DummyTensor:
        """Fallback Tensor placeholder."""
        pass

    class _DummyDevice:
        """Fallback device placeholder."""
        def __init__(self, *args, **kwargs):
            pass

    class _DummyDType:
        """Fallback dtype placeholder."""
        pass

    class _DummyTorchModule:
        Tensor = _DummyTensor
        device = _DummyDevice
        dtype = _DummyDType

        # Provide common dtype names you might reference
        float32 = _DummyDType()
        float64 = _DummyDType()

    torch = _DummyTorchModule()

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    def tqdm(x):
        return x


def get_entropy(
    descriptors: np.ndarray | torch.Tensor,
    width: float,
    use_tqdm: bool = True,
    device: str | torch.device = 'cuda',
    block: int = 1024,
    dtype: torch.dtype = torch.float32,
    eps: float = 1e-12,
) -> tuple[float, np.ndarray]:
    r"""
    Computes an estimate for the information entropy :math:`H(\mathbf{X})` of a
    set of descriptors :math:`\mathbf{X}`. The estimate is described in
    [Nat. Comm. **16**, 4014 (2025)](https://doi.org/10.1038/s41467-025-59232-0)
    and given by

    .. math::

        \mathcal{H}(\{\mathbf{X}\}) = -\frac{1}{n} \sum_{i=1}^{n} p_i

    where

    .. math::

        p_i
        = \log \left[
                \frac{1}{n} \sum_{j=1}^{n}
                K_h(\mathbf{X}_i, \mathbf{X}_j)
            \right]

    with a Gaussian kernel

    .. math::

        K_h(\mathbf{X}_i, \mathbf{X}_j)
        = \exp\!\left(
            -\frac{\lVert \mathbf{X}_i - \mathbf{X}_j \rVert^2}{2h^2}.
        \right)

    The calculation is done via torch if the library has been installed,
    and numpy otherwise. When using torch the calculation is run via CUDA.
    The latter behavior can be controlled using the :attr:`device` argument.

    Parameters
    ----------
    descriptors
        The set of descriptors :math:`\mathbf{X}` for which to evaluate to
        the entropy. Typically each row corresponds to one atom and the
        columns correspond to the different descriptor components.
    width
        Width :math:`h` of the Gaussian kernel.
    use_tqdm
        Use `tqdm <https://tqdm.github.io/>`_ to show a progress bar.
        Note that this requires tqdm to be installed.
    block
        In order to limit the memory needs, the kernel density estimate
        matrix is handled in blocks. This parameter controls the size of
        each block. Smaller numbers imply a smaller memory footprint.
    eps
        Smallest (absolute) permissible value.
    device
        Device to use for calculation. The documentation of
        [`torch.device`](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device)
        provides more information.
        Only used when pytorch is available.
    dtype
        Floating point precision used for the computation. The documentation of
        [`torch.dtype`](https://docs.pytorch.org/docs/stable/tensor_attributes.html)
        provides an overview.
        Only used when pytorch is available.

    Returns
    -------
    A tuple comprising the total entropy :math:`H(\mathbf{X})` and the entropy contributions
    :math:`p_i` from each row in the input descriptor matrix.
    """
    if torch_available:
        res = _get_entropy_torch(descriptors, width, use_tqdm, block, eps, device, dtype)
        return res
    else:  # pragma: no cover
        warn('Using the numpy implementation.'
             ' Install torch in order to use GPUs and achieve a considerable speed-up.')
        res = _get_entropy_numpy(descriptors, width, use_tqdm, block, eps)
        return res


def _get_entropy_numpy(
    descriptors: np.ndarray,
    width: float,
    use_tqdm: bool,
    block: int,
    eps: float,
) -> float:
    """Compute the informational entropy using numpy.
    See get_entropy for documentation.
    """
    X = np.asarray(descriptors, dtype=np.float64)
    N, d = X.shape
    s = np.sum(X * X, axis=1)                         # (N,)
    inv_two_sigma2 = 1.0 / (2.0 * width * width)

    row_sums = np.zeros(N, dtype=np.float64)
    for i0 in tqdm(range(0, N, block), leave=False):
        i1 = min(i0 + block, N)
        # D2[i0:i1, :] = s[i0:i1,None] + s[None,:] - 2*X[i0:i1]@X.T
        G = X[i0:i1] @ X.T                            # (B,N)
        D2_blk = (s[i0:i1, None] + s[None, :] - 2.0 * G)
        row_sums[i0:i1] = np.sum(np.exp(-D2_blk * inv_two_sigma2), axis=1)

    subvals = -np.log(np.clip(row_sums / N, min=eps))
    subvals /= N
    entropy = np.sum(subvals)
    return -float(entropy), subvals


def _get_entropy_torch(
    descriptors: np.ndarray | torch.Tensor,
    width: float,
    use_tqdm: bool,
    block: int,
    eps: float,
    device: str | torch.device = 'cuda',
    dtype: torch.dtype = torch.float32,
) -> tuple[float, np.ndarray]:
    """Compute the informational entropy using torch.
    See get_entropy for documentation.
    """
    with torch.no_grad():
        # Move data to device
        if not torch.cuda.is_available() and str(device) == 'cuda':  # pragma: no cover
            device = 'cpu'
        X = torch.as_tensor(descriptors, dtype=dtype, device=device)
        N, d = X.shape
        inv_two_sigma2 = 1.0 / (2.0 * width * width)

        # Precompute norms once
        s = (X * X).sum(dim=1)  # (N,)
        row_sums = torch.zeros(N, dtype=dtype, device=device)

        # Block over rows i; each block computes K[i0:i1, :].sum(-1)
        # D2 = s[i] + s[j] - 2 * X[i] @ X[j]^T  (formed in blocks to save memory)
        XT = X.T  # reuse in matmuls
        for i0 in tqdm(range(0, N, block), leave=False):
            i1 = min(i0 + block, N)
            try:
                G = X[i0:i1] @ XT                       # (B, N)
                D2_blk = s[i0:i1, None] + s[None, :] - 2.0 * G
            except torch.cuda.OutOfMemoryError:  # pragma: no cover
                torch.cuda.empty_cache()
                raise ValueError(
                    'Tried to allocate too much GPU memory.'
                    f' Try to reduce the value of block, e.g., to {block//2}.')
            row_sums[i0:i1] = torch.exp(-D2_blk * inv_two_sigma2).sum(dim=1)

        subvals = -torch.log(torch.clamp(row_sums / N, min=eps))
        subvals /= N
        entropy = torch.sum(subvals)
    return -float(entropy.detach().cpu().item()), subvals.detach().cpu().numpy()

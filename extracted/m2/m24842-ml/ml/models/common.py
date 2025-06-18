import torch
import torch.nn as nn
import torch.nn.functional as F

class GatedRMSNorm(nn.Module):
    def __init__(self, d, eps=1e-5, device=None):
        """Gated Root Mean Square Layer Normalization

        Paper: https://arxiv.org/abs/1910.07467
        """
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d, device=device))

    def forward(self, x, z=None):
        if z is not None:
            x = x * F.silu(z)
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.weight

class DilatedSlidingWindow(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, size, stride, dilation, dim, pad):
        ctx.size = size
        ctx.stride = stride
        ctx.dilation = dilation
        ctx.dim = dim
        ctx.pad = pad
        ctx.x_shape = x.shape
        
        # Save the original input BEFORE padding
        ctx.save_for_backward(x)
        
        ndim = x.dim()
        if dim < -ndim or dim >= ndim:
            raise IndexError(f"Dimension out of range (expected to be in range of [-{ndim}, {ndim-1}], but got {dim})")
        
        if dim < 0:
            dim = ndim + dim

        if pad[0] > 0 or pad[1] > 0:
            pad_tuple = [0] * (2 * ndim)
            pad_idx = 2 * (ndim - 1 - dim)
            pad_tuple[pad_idx] = pad[0]
            pad_tuple[pad_idx + 1] = pad[1]
            x = F.pad(x, tuple(pad_tuple))

        n_padded = x.shape[dim]
        
        effective_window_size = (size - 1) * dilation + 1
        
        num_windows = (n_padded - effective_window_size) // stride + 1

        if num_windows <= 0:
            final_shape = list(x.shape)
            final_shape[dim:dim+1] = [0, size]
            return torch.empty(final_shape, dtype=x.dtype, device=x.device)

        out_shape = list(x.shape)
        out_shape[dim:dim+1] = [num_windows, size]

        original_strides = x.stride()
        element_stride = original_strides[dim]

        out_stride = (
            original_strides[:dim] 
            + (stride * element_stride, dilation * element_stride) 
            + original_strides[dim+1:]
        )
        y = x.as_strided(out_shape, tuple(out_stride))

        return y

    @staticmethod
    def backward(ctx, grad_output):
        x, = ctx.saved_tensors  # This is now the original input
        
        # Create grad_input for the original input shape
        grad_input = torch.zeros_like(x)
        
        # Apply padding to grad_input if needed (to match forward pass)
        ndim = x.dim()
        dim = ctx.dim
        if dim < 0:
            dim = ndim + dim
            
        if ctx.pad[0] > 0 or ctx.pad[1] > 0:
            pad_tuple = [0] * (2 * ndim)
            pad_idx = 2 * (ndim - 1 - dim)
            pad_tuple[pad_idx] = ctx.pad[0]
            pad_tuple[pad_idx + 1] = ctx.pad[1]
            grad_input_padded = F.pad(grad_input, tuple(pad_tuple))
        else:
            grad_input_padded = grad_input

        n_padded = grad_input_padded.shape[dim]
        effective_window_size = (ctx.size - 1) * ctx.dilation + 1
        num_windows = (n_padded - effective_window_size) // ctx.stride + 1

        if num_windows > 0:
            out_shape = list(grad_input_padded.shape)
            out_shape[dim:dim+1] = [num_windows, ctx.size]
            original_strides = grad_input_padded.stride()
            element_stride = original_strides[dim]
            out_stride = (
                original_strides[:dim] 
                + (ctx.stride * element_stride, ctx.dilation * element_stride) 
                + original_strides[dim+1:]
            )
            grad_input_padded.as_strided(out_shape, out_stride).add_(grad_output)

        # If we padded, we need to "unpad" to get back to original input size
        if ctx.pad[0] > 0 or ctx.pad[1] > 0:
            # Extract the original region from the padded gradient
            slices = [slice(None)] * ndim
            slices[dim] = slice(ctx.pad[0], grad_input_padded.shape[dim] - ctx.pad[1] if ctx.pad[1] > 0 else None)
            grad_input = grad_input_padded[tuple(slices)]
        else:
            grad_input = grad_input_padded
            
        return grad_input, None, None, None, None, None

def dilated_sliding_window(x, size, stride=1, dilation=1, dim=-1, pad=(0, 0)):
    return DilatedSlidingWindow.apply(x, size, stride, dilation, dim, pad)

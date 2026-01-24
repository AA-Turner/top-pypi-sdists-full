
def apply_spline_at_mask(func, *, inputs, outputs, logabsdet, mask, **kwargs):
    """Helper function to apply a spline function to a masked subset of inputs.

    Only updates the outputs and logabsdet tensors at the locations specified
    by the mask.

    Parameters
    ----------
    func : Callable
        The spline function to apply.
    inputs : torch.Tensor
        The input tensor.
    outputs : torch.Tensor
        The output tensor.
    logabsdet : torch.Tensor
        The log absolute determinant tensor.
    mask : torch.Tensor
        The mask tensor.
    **kwargs:
        Additional keyword arguments to pass to the spline function.
    """
    outputs_masked, logabsdet_masked = func(
        inputs=inputs[mask],
        **kwargs,
    )
    if outputs.dtype == outputs_masked.dtype and logabsdet.dtype == logabsdet_masked.dtype:
        outputs[mask] = outputs_masked
        logabsdet[mask] = logabsdet_masked
    else:
        outputs[mask] = outputs_masked.to(outputs.dtype)
        logabsdet[mask] = logabsdet_masked.to(logabsdet.dtype)
    return outputs, logabsdet

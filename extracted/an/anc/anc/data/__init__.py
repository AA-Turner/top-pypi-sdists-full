# for now just return a torch dataloader
# TODO: implement the actual anc dataloader
def create_dataloader(*args, **kwargs):
    try:
        import torch
    except ImportError as e:
        raise ImportError(
            "Optional dependency 'torch' is required to use `create_dataloader()`. "
            "Please install it with `pip install torch`."
        ) from e
    return torch.utils.data.DataLoader(*args, **kwargs)

from __future__ import annotations

from rich.markdown import Markdown

from ..utils import render_example


def pytorch() -> bool | None:
    msg_start = Markdown(
        """
## Example: Train a PyTorch model on a GPU

Below we define a PyTorch model and training loop.
We use the Coiled serverless functions decorator to run our
model training function on an NVIDIA A10 GPU on AWS.\n
"""
    )

    return render_example(
        name="pytorch", dependencies=["coiled", "dask", "torch", "torchvision", "ipython"], msg_start=msg_start
    )

r"""batcharray: NumPy array manipulation for batches and sequences.

`batcharray` is a lightweight library built on top of NumPy to manipulate
nested data structures with NumPy arrays. It provides functions for arrays
where the first axis is the batch axis, and optionally the second axis is
the sequence axis.

Main modules:
    - array: Functions to manipulate single arrays with batch/sequence dimensions
    - nested: Functions to manipulate nested structures (dicts, lists) of arrays
    - computation: Computation models for abstracting array operations
    - recursive: Tools for recursively applying functions to nested structures
    - utils: Utility functions for exploring nested structures

Example:
```pycon
>>> import numpy as np
>>> from batcharray import array, nested
>>> # Working with single arrays
>>> batch = np.array([[1, 2], [3, 4], [5, 6]])
>>> sliced = array.slice_along_batch(batch, stop=2)
>>> # Working with nested structures
>>> data = {"a": np.array([1, 2, 3]), "b": np.array([4, 5, 6])}
>>> sliced = nested.slice_along_batch(data, stop=2)

```

For more information, see https://durandtibo.github.io/batcharray/
"""

from __future__ import annotations

__all__ = ["__version__"]

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    # Package is not installed, fallback if needed
    __version__ = "0.0.0"

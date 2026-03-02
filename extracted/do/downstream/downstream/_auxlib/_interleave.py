import typing

import numpy as np


# adapted from https://schlameel.com/interleaving-and-de-interleaving-data-with-python/
def interleave(arrs: typing.Sequence[np.ndarray]) -> np.ndarray:
    """Interleave a sequence of 1-D arrays element-wise.

    Parameters
    ----------
    arrs : sequence of ndarray
        Sequence of 1-D NumPy arrays to be interleaved. All arrays must have
        the same length.

    Returns
    -------
    interleaved : ndarray
        1-D NumPy array containing the interleaved elements from the input
        arrays.

    Examples
    --------
    >>> import numpy as np
    >>> arr1 = np.array([1, 2, 3])
    >>> arr2 = np.array([4, 5, 6])
    >>> interleave([arr1, arr2])
    array([1, 4, 2, 5, 3, 6])
    """
    return np.vstack(arrs).reshape((-1,), order="F")

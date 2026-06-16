r"""
Kramers-Kronig relation:

.. math::

    \chi_\mathrm{real}(\omega) = \frac{2}{\pi} \mathcal{P}
    \int_0^\infty \frac{\omega' \chi_\mathrm{imag}(\omega')}
    {\omega'^2 - \omega^2} \, d\omega'

Two private implementations are provided for validation purposes.
The public entry point is :func:`apply_kramers_kronig`, which defaults to the O(n²) vectorized
variant for accuracy; pass ``method='fft'`` for the O(n log n) approximation.
"""

import numpy as np
from pandas import DataFrame


def _hilbert(x):
    """ Discrete Hilbert transform via FFT (one-sided spectrum approach). """
    N = len(x)
    Xf = np.fft.fft(x)
    h = np.zeros(N)
    if N % 2 == 0:
        h[0] = h[N // 2] = 1
        h[1:N // 2] = 2
    else:
        h[0] = 1
        h[1:(N + 1) // 2] = 2
    return np.fft.ifft(Xf * h)


def _kramers_kronig_vectorized(omega: np.ndarray, chi_imag: np.ndarray) -> np.ndarray:
    """ Compute Re[chi] via a fully vectorized (n x n) matrix approach.

    Parameters
    ----------
    omega
        Non-negative angular frequency grid in rad/s, uniform or non-uniform.
    chi_imag
        Imaginary part of the susceptibility at each point in :attr:`omega`.

    Returns
    -------
    np.ndarray
        Real part of the susceptibility at each point in :attr:`omega`.

    Notes
    -----
    Complexity: O(n²) time, O(n²) memory.
    Accuracy: exact trapezoid rule over the supplied angular frequency grid.
    """
    omega = np.asarray(omega, dtype=float)
    chi_imag = np.asarray(chi_imag, dtype=float)

    w = omega[:, np.newaxis]
    om = omega[np.newaxis, :]

    denom = om ** 2 - w ** 2
    np.fill_diagonal(denom, 1.0)

    integrand = om * chi_imag[np.newaxis, :] / denom
    np.fill_diagonal(integrand, 0.0)

    return (2.0 / np.pi) * np.trapezoid(integrand, omega, axis=1)


def _kramers_kronig_fft(omega: np.ndarray, chi_imag: np.ndarray) -> np.ndarray:
    """ Compute Re[chi] via an FFT-based Hilbert transform.

    Parameters
    ----------
    omega
        Non-negative, uniformly spaced angular frequency grid in rad/s.
    chi_imag
        Imaginary part of the susceptibility at each point in :attr:`omega`.

    Returns
    -------
    np.ndarray
        Real part of the susceptibility at each point in :attr:`omega`.

    Notes
    -----
    Complexity: O(n log n) time, O(n) memory.
    Accuracy: approximation; differs from direct quadrature by roughly 5-10% of
    peak amplitude on typical grids.
    Requirement: :attr:`omega` must be uniformly spaced and :attr:`chi_imag` must be
    negligibly small at both endpoints.
    """
    chi_full = np.concatenate([-chi_imag[::-1], chi_imag])  # odd extension
    return -_hilbert(chi_full).imag[len(omega):]


def apply_kramers_kronig(df: DataFrame, method: str = 'vectorized') -> DataFrame:
    r""" Apply the Kramers-Kronig relation to add the real part of the dielectric function.

    Takes the output of :func:`~calorine.tools.get_dielectric_function`, computes
    :math:`\epsilon_1(\omega)` from :math:`\epsilon_2(\omega)` via the Kramers-Kronig
    relation, and returns the DataFrame with new ``epsilon_real*`` columns appended.

    Each ``epsilon_imag{suffix}`` column in :attr:`df` produces a corresponding
    ``epsilon_real{suffix}`` column (e.g. ``epsilon_imag_xx`` → ``epsilon_real_xx``).

    Parameters
    ----------
    df
        DataFrame as returned by :func:`~calorine.tools.get_dielectric_function` or
        :func:`~calorine.tools.get_ir_spectrum`;
        must contain ``angular_frequency`` and at least one column whose name starts
        with ``epsilon_imag``.
    method
        Integration method.  ``'vectorized'`` (default) uses an exact trapezoid rule
        over an :math:`n \times n` matrix (:math:`\mathcal{O}(n^2)` time and memory);
        ``'fft'`` uses an :math:`\mathcal{O}(n \log n)` Hilbert transform and is faster
        for large arrays but approximates the principal-value integral.
        The two methods agree to within a few percent on typical grids.

    Returns
    -------
    DataFrame
        Input DataFrame with additional ``epsilon_real*`` columns.
    """
    if method not in ('fft', 'vectorized'):
        raise ValueError(f"method must be 'fft' or 'vectorized', got {method!r}")

    kk = _kramers_kronig_fft if method == 'fft' else _kramers_kronig_vectorized
    omega = df['angular_frequency'].to_numpy()
    imag_cols = [c for c in df.columns if c.startswith('epsilon_imag')]

    df = df.copy()
    for col in imag_cols:
        suffix = col[len('epsilon_imag'):]
        df['epsilon_real' + suffix] = kk(omega, df[col].to_numpy())
    return df

r"""
Tools for computing optical and vibrational spectra from MD trajectories.

Covers three routes depending on the model and GPUMD output:

* **Dielectric tensor** (:func:`get_dielectric_function`): full 3×3 tensor
  from ``dpdt.out`` (qNEP, ``column='dP'`` or ``column='P'``) or ``dipole.out``
  (TNEP, ``column='mu'``).
* **IR spectrum** (:func:`get_ir_spectrum`): from ``dpdt.out``
  (qNEP, ``column='dP'`` or ``column='P'``) or ``dipole.out``
  (TNEP, ``column='mu'``).
* **Raman spectrum** (:func:`get_raman_spectrum`): from ``polarizability.out``
  (TNEP polarizability/susceptibility model).

Nomenclature
------------
- **Molecules / nanoparticles (localized systems)**: dipole moment :math:`\mu`
  (e·Å) and polarizability :math:`\alpha` (bohr³ or training-data units).
- **Solids / liquids (extended systems)**: polarization :math:`P` (e·Å, total
  cell dipole) and susceptibility :math:`\chi` (same unit as training data per
  cell).

Both cases use the same GPUMD output files and formulas; the distinction is
whether :attr:`volume` is supplied for normalization.

Quantum corrections
-------------------
The spectra from classical MD can be corrected for quantum statistics via
:func:`apply_quantum_correction`.  The correction factors differ by scattering
order (M. Cardona, *Topics in Applied Physics*, Vol. 50 (Springer, 1982);
Rosander *et al.*, PRB **111**, 064107 (2025)).
"""

import numpy as np
from pandas import DataFrame
from ase.units import _k as kB_SI, _e as e_SI, _eps0 as eps0_SI, _c as c_SI, _hbar as hbar_SI

_rad_s_to_thz = 1e-12
_rad_s_to_invcm = 1 / (2 * np.pi * c_SI * 100)


def _compute_correlation_function(Z1, Z2):
    """Normalized cross-correlation; normalization divides by the number of contributing pairs."""
    N = len(Z1)
    return np.correlate(Z1, Z2, mode='full')[N - 1:] / np.arange(N, 0, -1)


def _gaussian_decay(t, t_sigma):
    r"""Gaussian envelope :math:`\exp(-t^2 / 2\sigma^2)` used as a window applied to the ACF."""
    return np.exp(-0.5 * (t / t_sigma) ** 2)


def _psd_from_acf(acf, dt):
    """Power spectral density via even extension of the ACF followed by rfft."""
    signal = np.hstack((acf, acf[:0:-1]))
    fft = dt * np.fft.rfft(signal)
    freqs = 2 * np.pi * np.fft.rfftfreq(len(signal), dt)
    return freqs, fft.real


def _parse_polarization_pair(polarization_in, polarization_out):
    """Validate and parse a pair of polarization unit vectors, or return (None, None)."""
    if (polarization_in is None) != (polarization_out is None):
        raise ValueError('polarization_in and polarization_out must be given together')
    if polarization_in is None:
        return None, None
    n_in = np.asarray(polarization_in, dtype=float)
    n_out = np.asarray(polarization_out, dtype=float)
    if n_in.shape != (3,) or n_out.shape != (3,):
        raise ValueError('polarization_in and polarization_out must have shape (3,)')
    return n_in, n_out


# ── Signal column mapping ──────────────────────────────────────────────────────

_SIGNAL_COLS = {
    'dP': (['dPx', 'dPy', 'dPz'], True),
    'P':  (['Px', 'Py', 'Pz'], False),
    'mu': (['mu_x', 'mu_y', 'mu_z'], False),
}


def _resolve_signal(signal, column, dt):
    """Select signal columns from a DataFrame, infer derivative flag, auto-extract dt."""
    if column not in _SIGNAL_COLS:
        raise ValueError(
            f'column must be one of {list(_SIGNAL_COLS)!r}, got {column!r}'
        )
    col_names, derivative = _SIGNAL_COLS[column]
    missing = [c for c in col_names if c not in signal.columns]
    if missing:
        raise ValueError(
            f'signal is missing columns {missing!r} for column={column!r}'
        )
    if dt is None:
        if 'time' not in signal.columns:
            raise ValueError(
                'dt must be provided when signal has no time column '
                f'(got columns: {list(signal.columns)!r})'
            )
        dt = float(signal['time'].diff().dropna().iloc[0])
    return signal[col_names].to_numpy(dtype=float), dt, derivative


# ── IR spectrum ────────────────────────────────────────────────────────────────

def _acf_to_psd(acf, dt, t_sigma, max_lag):
    """Truncate ACF, apply optional Gaussian window, and compute PSD.  dt and t_sigma in ps."""
    acf = np.real(acf[:int(len(acf) * max_lag)])
    t_acf = dt * np.arange(len(acf))  # ps
    if t_sigma is not None:
        acf = acf * _gaussian_decay(t_acf, t_sigma=t_sigma)  # both ps
    return _psd_from_acf(acf, dt * 1e-12)  # _psd_from_acf uses seconds


def _ir_spectrum_1d(dt, signal, volume_SI, temperature, t_sigma, max_lag, derivative=False):
    """Compute IR spectrum for a single dipole/polarization component in SI units."""
    D = e_SI * 1e-10 / (1e-15 if derivative else 1.0)
    signal_SI = (signal - np.mean(signal)) * D
    acf = _compute_correlation_function(signal_SI, signal_SI)
    w, S = _acf_to_psd(acf, dt, t_sigma, max_lag)
    # When input is the signal itself, multiply by omega**2 to get PSD of its derivative
    # (PSD[dx/dt] = omega**2 * PSD[x]).  When input is already the derivative, use PSD directly.
    S_dpdt = S if derivative else w ** 2 * S

    if volume_SI is not None:
        beta = 1.0 / (kB_SI * temperature)
        conductivity = (beta / (3.0 * volume_SI)) * S_dpdt
        with np.errstate(divide='ignore', invalid='ignore'):
            eps_imag = conductivity / (eps0_SI * w)
        return w, eps_imag, conductivity
    else:
        return w, S_dpdt


def get_ir_spectrum(
    signal: DataFrame,
    volume: float = None,
    temperature: float = None,
    column: str = 'dP',
    dt: float = None,
    polarization: np.ndarray = None,
    t_sigma: float = None,
    max_lag: float = 0.25,
) -> DataFrame:
    r"""Compute the IR spectrum from a time series of dipole moments or polarizations.

    Parameters
    ----------
    signal
        ``DataFrame`` as returned by :func:`~calorine.gpumd.read_dpdt` or
        :func:`~calorine.gpumd.read_dipole`.  The columns to use are selected
        via :attr:`column`.
    volume
        Simulation cell volume in Å³.  Required for extended systems; when
        provided the function returns the imaginary dielectric function and
        conductivity.  Pass ``None`` for molecules to obtain an unnormalized
        line shape in arbitrary units.
    temperature
        Temperature in K.  Required when :attr:`volume` is not ``None``.
    column
        Selects which columns of :attr:`signal` to use and implies whether
        the input is a time derivative:

        ``'dP'`` (default)
            Uses ``dPx``, ``dPy``, ``dPz`` from :func:`~calorine.gpumd.read_dpdt`
            (qNEP); signal is :math:`\mathrm{d}P/\mathrm{d}t` in e·Å/fs.
        ``'P'``
            Uses ``Px``, ``Py``, ``Pz`` from :func:`~calorine.gpumd.read_dpdt`
            (qNEP); signal is the polarization :math:`P(t)` in e·Å.
        ``'mu'``
            Uses ``mu_x``, ``mu_y``, ``mu_z`` from
            :func:`~calorine.gpumd.read_dipole` (TNEP); signal is the dipole
            moment :math:`\mu(t)` in e·Å.

    dt
        Time between consecutive frames in ps.  Auto-extracted from the
        ``time`` column when present (i.e. for :func:`~calorine.gpumd.read_dpdt`
        output).  Must be supplied explicitly for step-indexed inputs such as
        :func:`~calorine.gpumd.read_dipole` output.
    polarization
        Unit vector ``(3,)`` defining the electric-field polarization direction.
        When given, the spectrum is computed from the projected signal
        :math:`s(t) = \hat{n} \cdot \mathrm{signal}(t)` instead of the
        isotropic average.
    t_sigma
        Width of the Gaussian window applied to the ACF in ps.
        ``None`` uses no windowing.
    max_lag
        Maximum ACF length as a fraction of the trajectory length; must be
        in (0, 1].  Defaults to 0.25 (25 %).

    Returns
    -------
    DataFrame
        Always contains ``angular_frequency`` (THz) and
        ``wavenumber_invcm`` (:math:`\mathrm{cm}^{-1}`).
        When :attr:`volume` and :attr:`temperature` are given:
        ``epsilon_imag`` (dimensionless) and ``conductivity`` (S/m).
        When :attr:`volume` is ``None``: ``ir_intensity`` (arbitrary units,
        proportional to :math:`\mathrm{PSD}[\dot{\mu}]`).
    """
    if volume is not None and temperature is None:
        raise ValueError('temperature must be provided when volume is given')

    arr, dt, derivative = _resolve_signal(signal, column, dt)
    volume_SI = volume * 1e-30 if volume is not None else None

    if polarization is not None:
        n = np.asarray(polarization, dtype=float)
        if n.shape != (3,):
            raise ValueError('polarization must have shape (3,)')
        components = [arr @ n]
    else:
        components = [arr[:, i] for i in range(3)]

    results = [_ir_spectrum_1d(dt, c, volume_SI, temperature, t_sigma, max_lag, derivative)
               for c in components]

    if volume_SI is not None:
        w = results[0][0]
        eps_imag = np.mean([r[1] for r in results], axis=0)
        conductivity = np.mean([r[2] for r in results], axis=0)
        mask = np.isfinite(eps_imag)
        cols = ['angular_frequency', 'wavenumber_invcm', 'epsilon_imag', 'conductivity']
        data = np.column_stack((w[mask] * _rad_s_to_thz, w[mask] * _rad_s_to_invcm,
                                eps_imag[mask], conductivity[mask]))
        return DataFrame(data, columns=cols)
    else:
        w = results[0][0]
        ir_intensity = np.mean([r[1] for r in results], axis=0)
        cols = ['angular_frequency', 'wavenumber_invcm', 'ir_intensity']
        data = np.column_stack((w * _rad_s_to_thz, w * _rad_s_to_invcm, ir_intensity))
        return DataFrame(data, columns=cols)


# ── Raman spectrum ─────────────────────────────────────────────────────────────

_POL_COLS = ['xx', 'yy', 'zz', 'yz', 'xz', 'xy']


def get_raman_spectrum(
    dt: float,
    polarizability: DataFrame,
    polarization_in: np.ndarray = None,
    polarization_out: np.ndarray = None,
    t_sigma: float = None,
    max_lag: float = 0.25,
) -> DataFrame:
    r"""Compute the Raman spectrum from a time series of polarizability tensors.

    Parameters
    ----------
    dt
        Time between consecutive frames in ps.
    polarizability
        DataFrame with columns ``xx``, ``yy``, ``zz``, ``xy``, ``yz``, ``xz``
        containing the polarizability :math:`\alpha` (molecules) or susceptibility
        :math:`\chi` (extended systems), as returned by
        :func:`~calorine.gpumd.read_polarizability`.  Units are those of the
        TNEP training data (typically bohr³).
    polarization_in
        Unit vector ``(3,)`` for the polarization of the incoming light.  If
        both :attr:`polarization_in` and :attr:`polarization_out` are given,
        the polarization-resolved intensity
        :math:`I(\omega) \propto \mathrm{FT}[\langle s(0)s(t)\rangle]` with
        :math:`s(t) = \hat{n}^\mathrm{out} \cdot \alpha(t) \cdot \hat{n}^\mathrm{in}`
        is added as the column ``raman_polarized``.
    polarization_out
        Unit vector ``(3,)`` for the polarization of the outgoing (scattered)
        light.
    t_sigma
        Width of the Gaussian window applied to the ACF in ps.  ``None`` uses no
        windowing.
    max_lag
        Maximum ACF length as a fraction of the trajectory length; must be
        in (0, 1].  Defaults to 0.25 (25 %).

    Returns
    -------
    DataFrame
        Always contains ``angular_frequency`` (THz),
        ``wavenumber_invcm`` (:math:`\mathrm{cm}^{-1}`),
        ``raman_isotropic`` (proportional to
        :math:`\mathrm{FT}[\langle\gamma(0)\gamma(t)\rangle]`), and
        ``raman_anisotropic`` (proportional to
        :math:`\mathrm{FT}[\langle\mathrm{Tr}[\beta(0)\beta(t)]\rangle]`).
        If both polarization vectors are given, also contains
        ``raman_polarized``.
    """
    missing = [c for c in _POL_COLS if c not in polarizability.columns]
    if missing:
        raise ValueError(f'polarizability is missing columns: {missing}')

    # Remove mean (Rayleigh component) before computing fluctuation spectrum.
    pol = polarizability[_POL_COLS] - polarizability[_POL_COLS].mean()

    n_in, n_out = _parse_polarization_pair(polarization_in, polarization_out)

    # Isotropic component gamma(t) = Tr[alpha(t)] / 3.
    gamma = (pol['xx'] + pol['yy'] + pol['zz']).to_numpy() / 3.0

    # Traceless part beta = alpha - gamma*I.
    beta_xx = pol['xx'].to_numpy() - gamma
    beta_yy = pol['yy'].to_numpy() - gamma
    beta_zz = pol['zz'].to_numpy() - gamma
    # Off-diagonal elements are unchanged: beta_xy = alpha_xy, etc.

    with np.errstate(invalid='ignore', divide='ignore'):
        # Isotropic Raman: FT[<gamma(0)*gamma(t)>].
        acf_iso = _compute_correlation_function(gamma, gamma)
        w, L_iso = _acf_to_psd(acf_iso, dt, t_sigma, max_lag)

        # Anisotropic Raman: FT[<Tr[beta(0)*beta(t)]>].
        # Tr[beta(0)*beta(t)] = sum_ij beta_ij(0)*beta_ij(t) — sum of per-element
        # ACFs with factor 2 for off-diagonal (since beta_ij = beta_ji).
        acf_aniso = (
            _compute_correlation_function(beta_xx, beta_xx)
            + _compute_correlation_function(beta_yy, beta_yy)
            + _compute_correlation_function(beta_zz, beta_zz)
            + 2.0 * _compute_correlation_function(pol['yz'].to_numpy(), pol['yz'].to_numpy())
            + 2.0 * _compute_correlation_function(pol['xz'].to_numpy(), pol['xz'].to_numpy())
            + 2.0 * _compute_correlation_function(pol['xy'].to_numpy(), pol['xy'].to_numpy())
        )
        _, L_aniso = _acf_to_psd(acf_aniso, dt, t_sigma, max_lag)

    cols = ['angular_frequency', 'wavenumber_invcm', 'raman_isotropic', 'raman_anisotropic']
    data = np.column_stack((w * _rad_s_to_thz, w * _rad_s_to_invcm, L_iso, L_aniso))
    df = DataFrame(data, columns=cols)

    # Polarization-resolved spectrum: s(t) = n_out . alpha(t) . n_in.
    # s = sum_ij n_out_i * alpha_ij * n_in_j; use symmetry alpha_ij = alpha_ji.
    if n_in is not None:
        s = (n_in[0]*n_out[0] * pol['xx'].to_numpy()
             + n_in[1]*n_out[1] * pol['yy'].to_numpy()
             + n_in[2]*n_out[2] * pol['zz'].to_numpy()
             + (n_in[1]*n_out[2] + n_in[2]*n_out[1]) * pol['yz'].to_numpy()
             + (n_in[0]*n_out[2] + n_in[2]*n_out[0]) * pol['xz'].to_numpy()
             + (n_in[0]*n_out[1] + n_in[1]*n_out[0]) * pol['xy'].to_numpy())
        with np.errstate(invalid='ignore', divide='ignore'):
            acf_pol = _compute_correlation_function(s, s)
            _, L_pol = _acf_to_psd(acf_pol, dt, t_sigma, max_lag)
        df['raman_polarized'] = L_pol

    return df


# ── Quantum correction ─────────────────────────────────────────────────────────

def apply_quantum_correction(
    df: DataFrame,
    temperature: float,
    column: str,
    order: str = 'first',
    force: bool = False,
) -> DataFrame:
    r"""Apply a quantum correction to a classically computed spectrum.

    Classical MD underestimates spectral intensities because it samples the
    classical Boltzmann distribution rather than the Bose-Einstein distribution.
    The correction factor depends on the scattering order and mode type
    [Cardona1982]_ [Rosander2025]_.

    Parameters
    ----------
    df
        DataFrame with an ``angular_frequency`` column (THz) and the column
        to correct.
    temperature
        Temperature in K.
    column
        Name of the spectral column to correct (e.g. ``'raman_isotropic'``,
        ``'ir_intensity'``, ``'epsilon_imag'``).
    order
        Correction type:

        ``'first'``
            First-order scattering (IR absorption and first-order Raman):
            :math:`f = \beta\hbar\omega / (1 - e^{-\beta\hbar\omega})`.
        ``'overtone'``
            Second-order overtone (same mode, :math:`\omega_1 = \omega/2`):
            :math:`f = [y/(1 - e^{-y})]^2 (2 - e^{-y})` with
            :math:`y = \beta\hbar\omega/2`.
        ``'combination'``
            Second-order combination band upper bound
            (:math:`\omega_1 = \omega_2 = \omega/2`):
            :math:`f = [y/(1 - e^{-y})]^2` with :math:`y = \beta\hbar\omega/2`.
    force
        If ``True``, overwrite an existing ``column + '_qm'`` column.
        Default ``False`` raises :class:`ValueError` to prevent accidental
        double-correction.

    Returns
    -------
    DataFrame
        Copy of :attr:`df` with a new column ``column + '_qm'`` containing
        the quantum-corrected intensities.  The input is not mutated.

    References
    ----------
    .. [Cardona1982] M. Cardona, *Resonance phenomena*, in *Topics in Applied
       Physics*, Vol. 50, edited by M. Cardona and G. Güntherodt
       (Springer, Berlin, 1982).
    .. [Rosander2025] Rosander *et al.*, Phys. Rev. B **111**, 064107 (2025),
       Supp. Eqs. S5, S7, S10.
    """
    if order not in ('first', 'overtone', 'combination'):
        raise ValueError("order must be 'first', 'overtone', or 'combination'")

    if not force and column + '_qm' in df.columns:
        raise ValueError(
            f"column '{column}_qm' already exists; pass force=True to overwrite"
        )

    w = df['angular_frequency'].to_numpy() * 1e12  # THz → rad/s
    beta = 1.0 / (kB_SI * temperature)
    x = beta * hbar_SI * w  # beta*hbar*omega (dimensionless)

    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        if order == 'first':
            # f = beta*hbar*omega / (1 - exp(-beta*hbar*omega))
            factor = np.where(x > 0, x / (1.0 - np.exp(-x)), 1.0)
        elif order == 'overtone':
            # f = [y/(1-exp(-y))]**2 * (2-exp(-y)),  y = beta*hbar*omega/2
            y = x / 2.0
            base = np.where(y > 0, y / (1.0 - np.exp(-y)), 1.0)
            factor = base ** 2 * np.where(y > 0, 2.0 - np.exp(-y), 1.0)
        else:  # combination
            # f = [y/(1-exp(-y))]**2,  y = beta*hbar*omega/2
            y = x / 2.0
            base = np.where(y > 0, y / (1.0 - np.exp(-y)), 1.0)
            factor = base ** 2

    result = df.copy()
    result[column + '_qm'] = df[column].to_numpy() * factor
    return result


# ── Dielectric tensor ─────────────────────────────────────────────────────────

_TENSOR_COMPONENTS = [(0, 0, 'xx'), (1, 1, 'yy'), (2, 2, 'zz'),
                      (1, 2, 'yz'), (0, 2, 'xz'), (0, 1, 'xy')]


def get_dielectric_function(
    signal: DataFrame,
    volume: float,
    temperature: float,
    column: str = 'dP',
    dt: float = None,
    t_sigma: float = None,
    max_lag: float = 0.25,
    return_real_part: bool = True,
    kk_method: str = 'vectorized',
) -> DataFrame:
    r"""Compute the dielectric function from a three-component polarization time series.

    Computes all six unique Voigt components of :math:`\epsilon_2^{\alpha\beta}(\omega)`
    (xx, yy, zz, yz, xz, xy) from the three-component time series written by GPUMD.
    The real part :math:`\epsilon_1^{\alpha\beta}(\omega)` is obtained via the
    Kramers-Kronig relation when :attr:`return_real_part` is ``True`` (the default).

    The imaginary part is related to the symmetrized cross-correlation via

    .. math::

        \epsilon_2^{\alpha\beta}(\omega) = \frac{\beta}{\epsilon_0 \omega V}
        \,\mathrm{Re}\!\left[\int_0^\infty
        \langle \dot{P}_\alpha(0)\,\dot{P}_\beta(t) \rangle
        e^{-i\omega t}\,dt\right],

    where :math:`\beta = 1/(k_\mathrm{B}T)` and :math:`V` is the cell volume.

    Parameters
    ----------
    signal
        ``DataFrame`` as returned by :func:`~calorine.gpumd.read_dpdt` or
        :func:`~calorine.gpumd.read_dipole`.  The columns to use are selected
        via :attr:`column`.
    volume
        Simulation cell volume in Å³.
    temperature
        Temperature in K.
    column
        Selects which columns of :attr:`signal` to use and implies whether
        the input is a time derivative:

        ``'dP'`` (default)
            Uses ``dPx``, ``dPy``, ``dPz`` from :func:`~calorine.gpumd.read_dpdt`
            (qNEP); input is :math:`\dot{\mathbf{P}}(t)` in e·Å/fs.
        ``'P'``
            Uses ``Px``, ``Py``, ``Pz`` from :func:`~calorine.gpumd.read_dpdt`
            (qNEP); input is the polarization :math:`\mathbf{P}(t)` in e·Å.
        ``'mu'``
            Uses ``mu_x``, ``mu_y``, ``mu_z`` from
            :func:`~calorine.gpumd.read_dipole` (TNEP); input is the dipole
            moment :math:`\boldsymbol{\mu}(t)` in e·Å.

    dt
        Time between consecutive frames in ps.  Auto-extracted from the
        ``time`` column when present (i.e. for :func:`~calorine.gpumd.read_dpdt`
        output).  Must be supplied explicitly for step-indexed inputs such as
        :func:`~calorine.gpumd.read_dipole` output.
    t_sigma
        Width of the Gaussian window applied to the ACF in ps.
        ``None`` uses no windowing.
    max_lag
        Maximum ACF length as a fraction of the trajectory length; must be
        in (0, 1].  Defaults to 0.25 (25 %).
    return_real_part
        When ``True`` (default), the real part :math:`\epsilon_1^{\alpha\beta}(\omega)`
        is computed via the Kramers-Kronig relation and appended as
        ``epsilon_real_{xx,yy,zz,yz,xz,xy}`` columns.
    kk_method
        Integration method passed to :func:`~calorine.tools.apply_kramers_kronig`
        when :attr:`return_real_part` is ``True``.  ``'vectorized'`` (default) uses
        an exact trapezoid rule; ``'fft'`` uses a faster Hilbert transform
        approximation.  Ignored when :attr:`return_real_part` is ``False``.

    Returns
    -------
    DataFrame
        Contains ``angular_frequency`` (THz), ``wavenumber_invcm``
        (:math:`\mathrm{cm}^{-1}`),
        ``epsilon_imag_{xx,yy,zz,yz,xz,xy}`` (dimensionless, imaginary dielectric
        tensor components), and ``conductivity_{xx,yy,zz,yz,xz,xy}`` (S/m).
        When :attr:`return_real_part` is ``True``, ``epsilon_real_{xx,yy,zz,yz,xz,xy}``
        columns are appended.
    """
    arr, dt, derivative = _resolve_signal(signal, column, dt)

    D = e_SI * 1e-10 / (1e-15 if derivative else 1.0)
    volume_SI = volume * 1e-30
    beta = 1.0 / (kB_SI * temperature)

    signal_SI = (arr - arr.mean(axis=0)) * D

    def _psd(z1, z2=None):
        if z2 is None:
            acf = _compute_correlation_function(z1, z1)
        else:
            acf = (_compute_correlation_function(z1, z2)
                   + _compute_correlation_function(z2, z1)) / 2
        w, S = _acf_to_psd(acf, dt, t_sigma, max_lag)
        # PSD[dx/dt] = omega**2 * PSD[x] when input is the signal itself.
        return w, S if derivative else w ** 2 * S

    w = None
    conductivities = {}
    eps_imags = {}
    for i, j, lbl in _TENSOR_COMPONENTS:
        zi = signal_SI[:, i]
        zj = signal_SI[:, j]
        w, S_dpdt = _psd(zi) if i == j else _psd(zi, zj)
        conductivity = (beta / volume_SI) * S_dpdt
        with np.errstate(divide='ignore', invalid='ignore'):
            eps_imag = conductivity / (eps0_SI * w)
        conductivities[lbl] = conductivity
        eps_imags[lbl] = eps_imag

    mask = w > 0
    cols = (['angular_frequency', 'wavenumber_invcm']
            + [f'epsilon_imag_{lbl}' for _, _, lbl in _TENSOR_COMPONENTS]
            + [f'conductivity_{lbl}' for _, _, lbl in _TENSOR_COMPONENTS])
    arrays = ([w[mask] * _rad_s_to_thz, w[mask] * _rad_s_to_invcm]
              + [eps_imags[lbl][mask] for _, _, lbl in _TENSOR_COMPONENTS]
              + [conductivities[lbl][mask] for _, _, lbl in _TENSOR_COMPONENTS])
    result = DataFrame(np.column_stack(arrays), columns=cols)
    if return_real_part:
        from .kramers_kronig import apply_kramers_kronig
        result = apply_kramers_kronig(result, method=kk_method)
    return result

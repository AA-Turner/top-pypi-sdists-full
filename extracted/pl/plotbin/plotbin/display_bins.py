"""

Modification History
--------------------
V1.0.0: Michele Cappellari, Oxford, 15 January 2015
V1.0.1: Further input checks. MC, Oxford, 15 July 2015
V1.0.2: Raise an error if bin_num is not integer. Pass kwargs to display_pixels.
    Thanks to Rebekka Schupp (MPIA) for the feedback. MC, Oxford, 31 July 2017
V1.0.3: Changed imports for plotbin as a package. MC, Oxford, 17 April 2018
V1.0.4: Fixed display_pixels import. Thanks to Adriano Poci (Macquarie).
    MC, Oxford, 3 May 2019
V2.0.0: Added interpolation and symmetrization options. MC, Oxford, 5 July 2026

"""

from typing import Any

import numpy as np
from numpy.typing import ArrayLike
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy import interpolate, spatial

from plotbin.display_pixels import display_pixels
from plotbin.symmetrize_velfield import _rotate_points
    
#----------------------------------------------------------------------

class display_bins:

    """
    Display a Voronoi-binned map, with optional interpolation and symmetrization.

    If ``interp=False`` (the default), each input pixel is simply displayed 
    with the value of its parent bin, ``zbin[bin_num]``. 

    If ``interp=True``, the routine computes the bin barycenters from the pixel
    coordinates and evaluates the map at all pixel locations using a linear
    ``RBFInterpolator``. The barycenters are flux-weighted when ``flux`` is
    provided and geometric otherwise.

    If ``zbin_err`` is provided, an approximate statistical heuristic calculates 
    the RBF smoothing weights based on the noise-to-signal variance ratio. The 
    overall amount of smoothing can be scaled via the ``smoothing`` tuning 
    parameter. The nearest ``num_exact_center`` bins are forced to have zero 
    smoothing (exact interpolation) to preserve sharp central gradients.

    When ``sym`` is specified, the bin values are mirrored into all four 
    quadrants before interpolation. This symmetrization ALWAYS happens with 
    respect to the Cartesian (x, y) axes of the image. This means that to 
    symmetrize a map along its principal axes, you must use the ``angle`` 
    parameter to rotate the galaxy's major axis to align with the x-axis.

    The ``sym`` parameter accepts:
        - ``'odd'``: Anti-symmetric across the Y-axis. Suitable for odd-parity 
          kinematic fields like velocity.
        - ``'even'``: Symmetric across all quadrants. Suitable for even-parity 
          fields like velocity dispersion or Vrms.

    Parameters
    ----------
    x, y : array_like
        Pixel coordinates.
    bin_num : array_like of int
        Bin number for each pixel.
    zbin : array_like
        Quantity measured for each bin.
    zbin_err : array_like, optional
        Uncertainties on ``zbin``; activates automated smoothing during 
        interpolation.
    angle : float, optional
        Rotation angle in degrees. Used to align the major axis with the x-axis 
        for symmetrization. Also passed to the image display and flux contours.
        When ``sym=None``, this only rotates the displayed image, not the 
        interpolation coordinates.
    interp : bool, optional
        If True, interpolate from bin centers to individual pixels.
    debug : bool, optional
        If True, overplots the mirrored bin centers as red circles to help 
        visually verify the symmetrization geometry.
    num_exact_center : int, optional
        Number of central bins forced to have zero smoothing when using errors.
    markersize : float, optional
        Size of the overplotted bin-center markers when ``interp=True``.
    smoothing : float, optional
        Global tuning factor for the automated RBF smoothing heuristic 
        (default is 1.0). Values > 1 increase the global smoothness of the 
        interpolation, while values < 1 decrease it, preserving more local 
        structure.
    sym : {'even', 'odd', None}, optional
        Type of bi-symmetry applied to the interpolated field.
    flux : array_like, optional
        Pixel fluxes used to compute flux-weighted bin barycenters when
        ``interp=True`` and to overplot logarithmic grey contours.
    ax : matplotlib.axes.Axes, optional
        Axes on which to draw. Defaults to the current axes.
    **kwargs
        Additional keywords passed to ``display_pixels``.

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        Axes used for the plot.
    img : matplotlib artist
        Artist returned by ``display_pixels``.
    z : ndarray
        Final values displayed at the input pixel coordinates.
    xbin, ybin : ndarray or None
        Bin centres overplotted on the map, after rotation by ``angle``.
        These are only set when ``interp=True``.
    xybin : ndarray or None
        Coordinates passed to ``RBFInterpolator``. These include mirrored
        copies when ``sym`` is specified.
    xy : ndarray or None
        Coordinates where the RBF is evaluated.
    zbin : ndarray or None
        Values passed to ``RBFInterpolator``. These include mirrored copies
        when ``sym`` is specified.
    smoothing_rbf : float or ndarray
        Smoothing parameter passed to ``RBFInterpolator``.
    """

    def __init__(
        self,
        x: ArrayLike,
        y: ArrayLike,
        bin_num: np.ndarray,
        zbin: ArrayLike,
        zbin_err: ArrayLike | None = None,
        angle: float = 0.0,
        interp: bool = False,
        debug: bool = False,
        num_exact_center: int = 1,
        markersize: float = 3,
        smoothing: float = 1.0,
        sym: str | None = None,
        flux: ArrayLike | None = None,
        ax: Axes | None = None,
        **kwargs: Any
    ) -> None:

        assert bin_num.dtype.kind == 'i', "bin_num must be integer"
        assert x.size == y.size == bin_num.size, "The vectors (x, y, bin_num) must have the same size"
        assert np.unique(bin_num).size == zbin.size, "zbin size does not match number of bins"
        
        self.ax = ax = ax or plt.gca()
        self.xbin = self.ybin = None
        self.zbin = zbin
        self.xybin = None
        self.xy = None
        self.smoothing_rbf = sm = 0
        self.x, self.y = x, y
        self.z = zbin[bin_num]
        
        if interp:

            npix = np.bincount(bin_num)
            if flux is None:
                weights = npix
                xbin = np.bincount(bin_num, weights=x)/weights
                ybin = np.bincount(bin_num, weights=y)/weights
            else:
                weights = np.bincount(bin_num, weights=flux)
                xbin = np.bincount(bin_num, weights=flux*x)/weights
                ybin = np.bincount(bin_num, weights=flux*y)/weights
            xbin_plot, ybin_plot = _rotate_points(xbin, ybin, angle)

            self.xbin, self.ybin = xbin_plot, ybin_plot

            # Compute Smoothing Array (Independent of symmetry)
            if zbin_err is not None:

                # Efficient median nearest neighbor distance of the unmirrored bins
                xybin_orig = np.column_stack([xbin, ybin])
                tree = spatial.KDTree(xybin_orig)
                dist, ind = tree.query(xybin_orig, k=[2])  # dist to nearest neighbor
                scale = np.median(dist)

                # Local noise: Difference between each bin and its nearest neighbor
                dz = zbin - zbin[ind[:, 0]]
                mad = np.median(np.abs(dz - np.median(dz)))
                
                # The variance of the difference of two variables is 2x the variance
                total_var = (1.4826 * mad)**2 / 2.0
                noise_var = np.median(zbin_err)**2

                # The statistical uncertainty of the variance estimator
                var_err = total_var * np.sqrt(2 / len(zbin_err))

                # Smoothing vector
                signal_var = max(total_var - noise_var, var_err)                
                sm = smoothing * scale * zbin_err**2 / signal_var

                # Avoid smoothing the central few points to allow for a singularity
                if num_exact_center > 0:
                    _, center_ind = tree.query([0.0, 0.0], k=num_exact_center)
                    sm[center_ind] = 0

            # Apply Symmetrization (If requested)
            if sym is None:
                xybin = np.column_stack([xbin, ybin])
                xy = np.column_stack([x, y])
            else:
                assert sym in ['even', 'odd'], "sym must be 'even' or 'odd'"
                assert zbin_err is None or zbin_err.size == zbin.size, "zbin_err size does not match zbin size"

                # Replicate and mirror the dataset across the appropriate axes
                xbin_sym, ybin_sym = _rotate_points(xbin, ybin, angle)
                xybin = np.column_stack([np.hstack([xbin_sym, -xbin_sym, xbin_sym, -xbin_sym]),
                                         np.hstack([ybin_sym, ybin_sym, -ybin_sym, -ybin_sym])])
                xy = np.column_stack(_rotate_points(x, y, angle))
                
                zbin = np.hstack([zbin, -zbin] * 2) if sym == 'odd' else np.tile(zbin, 4)
                if zbin_err is not None:
                    sm = np.tile(sm, 4)
                    zbin_err = np.tile(zbin_err, 4)

                if debug:
                    ax.plot(*xybin.T, 'o', color='red', mfc='none', ms=markersize, zorder=8)

                xybin, inv_ind, counts = np.unique(np.round(xybin, 3), axis=0, return_inverse=True, return_counts=True)            

                # Merge duplicated coordinates by averaging their values
                if zbin_err is not None:                
                    w = 1.0 / zbin_err**2
                    w_z = w * zbin            
                    sum_w = np.bincount(inv_ind, weights=w)
                    zbin = np.bincount(inv_ind, weights=w_z) / sum_w
                    sm = np.bincount(inv_ind, weights=(sm * w**2)) / sum_w**2
                else:
                    zbin = np.bincount(inv_ind, weights=zbin) / counts

            self.xybin = xybin
            self.xy = xy
            self.zbin = zbin
            self.smoothing_rbf = sm

            self.z = interpolate.RBFInterpolator(xybin, zbin, kernel='linear', smoothing=sm)(xy)
            ax.plot(xbin_plot, ybin_plot, '.', color='dimgray', ms=markersize, zorder=10)
            
        self.img = display_pixels(x, y, self.z, angle=angle, ax=ax, **kwargs)

        if flux is not None:
            w = flux > 0
            if not np.all(w):
                flux = flux.clip(flux[w].min())  # Avoid zero or negative values
            flux = np.log10(flux)   # more accurate interpolation in log space
            levels = np.max(flux) - 0.4*np.arange(20)[::-1]  # 1 mag contours
            x, y = _rotate_points(x, y, angle)
            ax.tricontour(x, y, flux, levels=levels, colors='darkgray')

#----------------------------------------------------------------------

#!/usr/bin/env python
"""
  Copyright (C) 2013-2026, Michele Cappellari
  E-mail: michele.cappellari_at_physics.ox.ac.uk
  http://purl.org/cappellari

  See example at the bottom for usage instructions.

MODIFICATION HISTORY:
    V1.0.0: Michele Cappellari, Paranal, 11 November 2013
    V1.0.1: Clip values before contouring. MC, Oxford, 26 February 2014
    V1.0.2: Include SAURON colormap. MC, Oxford, 29 January 2014
    V1.0.3: Call set_aspect(1). MC, Oxford, 22 February 2014
    V1.0.4: Call autoscale_view(tight=True). Overplot small dots by default.
        MC, Oxford, 25 February 2014
    V1.0.5: Use axis('image'). MC, Oxford, 29 March 2014
    V1.0.6: Allow changing colormap. MC, Oxford, 29 July 2014
    V1.0.7: Added optional fixpdf keyword to remove PDF visual artifacts.
        Make nice tick levels for colorbar. Added nticks keyword for colorbar.
        MC, Oxford, 16 October 2014
    V1.0.8: Return axis of main plot. MC, Oxford, 26 March 2015
    V1.0.9: Clip values within +/-eps of vmin/vmax, to assign clipped values
        the top colour in the colormap, rather than having an empty contour.
        MC, Oxford, 18 May 2015
    V1.0.10: Removed optional fixpdf keyword and replaced with better solution.
        MC, Oxford, 5 October 2015
    V1.0.11: Activate main plot after colorbar. Return plot rather than axis.
        MC, Oxford, 6 November 2015
    V1.0.12: Simplified passing of default keywords. Included np.ravel(flux).
        MC, Oxford, 16 February 2017
    V1.1.0: Use tricontourf(extend=...) insted of clipping, for better contours.
        The colorbar edges show when contours do not extend to full range.
        MC, Oxford, 23 March 2017
    V1.1.1: Use register_sauron_colormap(). MC, Oxford, 29 March 2017
    V1.1.2: Removed fix for gaps in colorbar. MC, Oxford, 15 December 2017
    V1.1.3: Changed imports for plotbin as a package. MC, Oxford, 17 April 2018
    V1.1.4: Included `linescolor` keyword. MC, Oxford, 30 April 2018
    V1.1.5: Commented set_edgecolor to avoid bug in Matplotlib 3.3.
        MC, Oxford, 24 September 2020
    V1.1.6: Re-activated set_edgecolor. MC, Oxford, 8 April 2022
    V1.1.7: Removed .collections loop, which was deprecated in Matplotlib 3.8.
        Ensure ticks are within the given limits (to fix a new Matplotlib bug).
        Use default_rng instead of deprecated numpy.random. 
        MC, Oxford, 4 June 2024
    V1.1.8: Removed dependency on mpl_toolkits.axes_grid1.make_axes_locatable.
        This fixes a new Matplotlib bug when saving the colorbar to a PDF file.
        MC, Oxford, 12 December 2024
    V1.1.9: Allow for negative flux values in log contour plot. 
        MC, Oxford, 30 August 2025
    V1.1.10: Reverted to plotting log(flux), with clipping of negative values, 
        for more accurate interpolation.
        MC, Oxford, 14 January 2026
    V1.1.11: Added `rasterized` keyword to optionally rasterize the contour plot,
        which can significantly reduce the file size of vector graphics output.
        MC, Oxford, 17 February 2026

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from plotbin.sauron_colormap import register_sauron_colormap

##############################################################################


def plot_velfield(x, y, vel, vmin=None, vmax=None, ncolors=64,
                  nodots=False, colorbar=False, linescolor='k', label=None,
                  flux=None, nticks=7, markersize=3, cmap='sauron', ax=None, 
                  rasterized=False, **kwargs):
    """
    Plot a velocity field using filled contours.

    This function creates a filled contour plot of a velocity field on a 2D grid,
    optionally overlaying flux contours and a colorbar. It is designed for visualizing
    astronomical velocity fields, such as those from integral field spectroscopy.

    Parameters
    ----------
    x : array_like
        x-coordinates of the data points.
    y : array_like
        y-coordinates of the data points.
    vel : array_like
        Velocity values at each (x, y) point.
    vmin : float, optional
        Minimum value for the color scale. If None, uses the minimum of `vel`.
    vmax : float, optional
        Maximum value for the color scale. If None, uses the maximum of `vel`.
    ncolors : int, optional
        Number of color levels in the contour plot (default is 64).
    nodots : bool, optional
        If True, do not overplot small black dots at each data point (default is False).
    colorbar : bool, optional
        If True, add a colorbar to the plot (default is False).
    linescolor : str, optional
        Color of the flux contour lines (default is 'k' for black).
    label : str, optional
        Label for the colorbar (default is None).
    flux : array_like, optional
        Flux values for overlaying logarithmic contours. If provided, contours are
        drawn at levels corresponding to 1 magnitude intervals (default is None).
    nticks : int, optional
        Number of ticks on the colorbar (default is 7).
    markersize : float, optional
        Size of the black dots overplotted on the data points (default is 3).
    cmap : str, optional
        Colormap name (default is 'sauron'). Supports 'sauron' and 'sauron_r'.
    ax : matplotlib.axes.Axes, optional
        Pre-existing axes for the plot. Otherwise, call `plt.gca()` internally.
    rasterized : bool, optional
        Rasterize the tricontourf plot (default is False). This is useful to 
        reduce the file size of vector graphics output (e.g. PDF, EPS).
    **kwargs : dict
        Additional keyword arguments passed to `tricontourf` and `plot`.

    Returns
    -------
    matplotlib.tri.TriContourSet
        The contour plot object.

    Notes
    -----
    - The function uses triangular interpolation for contouring, suitable for irregular grids.
    - Flux contours are logarithmic, spaced by 1 magnitude, if `flux` is provided.
    - The SAURON colormap is registered automatically if selected.

    Examples
    --------
    >>> import numpy as np
    >>> from matplotlib import pyplot as plt
    >>> from plotbin.plot_velfield import plot_velfield
    >>> 
    >>> # Generate sample data
    >>> x = np.random.uniform(-30, 30, 300)
    >>> y = np.random.uniform(-20, 20, 300)
    >>> vel = np.sin(x / 10) * np.cos(y / 10) * 100
    >>> flux = np.exp(-(x**2 + y**2) / 100)
    >>> 
    >>> plt.figure()
    >>> plot_velfield(x, y, vel, flux=flux, colorbar=True, label='Velocity (km/s)')
    >>> plt.show()

    See Also
    --------
    matplotlib.pyplot.tricontourf : Triangular contour plot.
    matplotlib.pyplot.colorbar : Add a colorbar to a plot.
    """

    x, y, vel, flux = map(np.ravel, [x, y, vel, flux])

    assert x.size == y.size == vel.size, 'The vectors (x, y, vel) must have the same size'

    if cmap in ['sauron', 'sauron_r']:
        register_sauron_colormap()

    dmin, dmax = np.min(vel), np.max(vel)

    if 'extend' in kwargs:
        extend = kwargs.pop('extend')
    else:
        under = vmin is not None and dmin < vmin
        over  = vmax is not None and dmax > vmax
        extend = 'both' if under and over else 'min' if under else 'max' if over else 'neither'

    vmin = dmin if vmin is None else vmin
    vmax = dmax if vmax is None else vmax

    levels = np.linspace(vmin, vmax, ncolors)

    if ax is None:
        ax = plt.gca()

    # https://matplotlib.org/stable/gallery/misc/rasterization_demo.html
    zorder = kwargs.pop('zorder', None) if not rasterized else -10
    cnt = ax.tricontourf(x, y, vel, levels=levels, cmap=cmap, extend=extend, zorder=zorder, **kwargs)
    if rasterized:      
        ax.set_rasterization_zorder(0)  

    # Remove white gaps in contour levels of PDF  http://stackoverflow.com/a/32911283/
    cnt.set_edgecolor("face")  

    ax.axis('image')  # Equal axes and no rescaling

    if flux[0] is not None:
        w = flux > 0
        if np.any(~w):
            flux = flux.clip(flux[w].min())  # Avoid zero or negative values
        flux = np.log10(flux)   # more accurate interpolation in log space
        levels = np.max(flux) - 0.4*np.arange(20)[::-1]  # 1 mag contours
        ax.tricontour(x, y, flux, levels=levels, colors=linescolor, linestyles='solid')

    if not nodots:
        ax.plot(x, y, '.k', markersize=markersize, **kwargs)

    if colorbar:
        cax = ax.inset_axes([1.02, 0, .05, 1], transform=ax.transAxes)
        ticks = MaxNLocator(nticks).tick_values(vmin, vmax)
        ticks = ticks[(ticks >= vmin) & (ticks <= vmax)]  # Fix Matplotlib bug
        cbar = plt.colorbar(cnt, cax=cax, ticks=ticks)
        if label is not None:
            cbar.set_label(label)
        plt.sca(ax)  # Activate main plot before returning

    return cnt

##############################################################################

# Usage example for plot_velfield()

if __name__ == '__main__':

    prng = np.random.default_rng(123) 
    xbin, ybin = prng.uniform(low=[-30, -20], high=[30, 20], size=(300, 2)).T
    inc = 60.                       # assumed galaxy inclination
    r = np.sqrt(xbin**2 + (ybin/np.cos(np.radians(inc)))**2) # Radius in the plane of the disk
    a = 40                          # Scale length in arcsec
    vr = 2000*np.sqrt(r)/(r+a)      # Assumed velocity profile
    vel = vr * np.sin(np.radians(inc))*xbin/r # Projected velocity field
    flux = np.exp(-r/10)

    plt.clf()
    plt.title('Velocity')
    plot_velfield(xbin, ybin, vel, flux=flux, colorbar=True, label='km/s', vmin=-120, vmax=120)
    plt.pause(10)

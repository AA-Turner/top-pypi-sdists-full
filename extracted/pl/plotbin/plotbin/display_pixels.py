#!/usr/bin/env python
"""
Copyright (C) 2014-2023, Michele Cappellari
E-mail: michele.cappellari_at_physics.ox.ac.uk

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

See example at the bottom for usage instructions.

MODIFICATION HISTORY:
    V1.0.0: Created to emulate my IDL procedure with the same name.
        Michele Cappellari, Oxford, 28 March 2014
    V1.0.1: Fixed treatment of optional parameters. MC, Oxford, 6 June 2014
    V1.0.2: Avoid potential runtime warning. MC, Oxford, 2 October 2014
    V1.0.3: Return axis. MC, Oxford, 26 March 2015
    V1.0.4: Return image instead of axis. MC, Oxford, 15 July 2015
    V1.0.5: Removes white gaps from rotated images using edgecolors.
        MC, Oxford, 5 October 2015
    V1.0.6: Pass kwargs to graphics functions.
        MC, Campos do Jordao, Brazil, 23 November 2015
    V1.0.7: Check that input (x,y) come from an axis-aligned image.
        MC, Oxford, 28 January 2016
    V1.0.8: Fixed deprecation warning in Numpy 1.11. MC, Oxford, 22 April 2016
    V1.1.0: Fixed program stop with kwargs. Included `colorbar` keyword.
        MC, Oxford, 18 May 2016
    V1.1.1: Use interpolation='nearest' to avoid crash on MacOS.
        MC, Oxford, 14 June 2016
    V1.1.2: Specify origin=`upper` in imshow() for consistent results with older
        Matplotlib version. Thanks to Guillermo Bosch for reporting the issue.
        MC, Oxford, 6 January 2017
    V1.1.3: Simplified passing of default keywords. MC, Oxford, 20 February 2017
    V1.1.4: Use register_sauron_colormap(). MC, Oxford, 29 March 2017
    V1.1.5: Request `pixelsize` when dataset is large. Thanks to Davor
        Krajnovic (Potsdam) for the feedback. MC, Oxford, 10 July 2017
    V1.1.6: Fixed new incompatibility with Matplotlib 2.1.
        MC, Oxford, 9 November 2017
    V1.1.7: Changed imports for plotbin as a package. MC, Oxford, 17 April 2018
    V1.1.8: Use default size for tick marks. MC, Oxford, 12 December 2023
    V1.1.9: Removed edgecolors="face" in pcolormesh to avoid possible spurious
        artifacts, introduced by Matplotlib changes. MC, Oxford, 16 August 2024
    V1.1.10: Removed dependency on mpl_toolkits.axes_grid1.make_axes_locatable.
        This fixes a new Matplotlib bug when saving the colorbar to a PDF file.
        MC, Oxford, 12 December 2024
    V1.2.0: Use KDTree for pixel size estimation. Removed masked_array logic.
        Updated usage example. MC, Oxford, 7 September 2025

"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.spatial import KDTree
import numpy as np

from plotbin.sauron_colormap import register_sauron_colormap

##############################################################################

def display_pixels(x, y, val, pixelsize=None, vmin=None, vmax=None,
                   angle=None, colorbar=False, label=None, nticks=7,
                   cmap='sauron', check_grid=True, **kwargs):
    """
    Display vectors of square pixels at coordinates (x,y) coloured with "val".
    An optional rotation around the origin can be applied to the whole image.
    
    The pixels are assumed to be taken from a regular cartesian grid with 
    constant spacing (like an axis-aligned image), but not all elements of
    the grid are required (missing data are OK).

    By default, the program checks that the data form a regular grid within 10%
    of the pixel size. One can ignore this check with ``check_grid=False``

    This routine is designed to be fast even with large images and to produce
    minimal file sizes when the output is saved in a vector format like PDF.

    NOTE: To avoid possible small white gaps between the pixels in the PDF, one
    may try to pass to `display_pixels` the parameters `edgecolors="face"` and
    something like `linewidth=.01`. However, I found the above `linewidth` to
    be suitable for the PDF but to produce too thick edges on the screen.
    Alternatively, one can set `rasterized="True"`.

    """
    x, y, val = map(np.ravel, [x, y, val])

    assert x.size == y.size == val.size, 'The vectors (x, y, val) must have the same size'

    if cmap in ['sauron', 'sauron_r']:
        register_sauron_colormap()

    if vmin is None:
        vmin = np.min(val)

    if vmax is None:
        vmax = np.max(val)

    if pixelsize is None:
        xy = np.c_[x, y]
        dist, _ = KDTree(xy).query(xy, [2])
        pixelsize = np.median(dist)

    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    x1 = (x - xmin)/pixelsize
    y1 = (y - ymin)/pixelsize
    nx = int(round((xmax - xmin)/pixelsize) + 1)
    ny = int(round((ymax - ymin)/pixelsize) + 1)
    img = np.full((nx, ny), np.nan)  # use nan for missing data
    j = np.round(x1).astype(int)
    k = np.round(y1).astype(int)
    img[j, k] = val

    if check_grid:
        assert np.all(np.abs(np.append(j - x1, k - y1)) < 0.1), \
            'The coordinates (x, y) must come from an axis-aligned image with square pixels'

    ax = plt.gca()

    if (angle is None) or (angle == 0):
        imx = ax.imshow(img.T, interpolation='nearest',
                        origin='lower', cmap=cmap, vmin=vmin, vmax=vmax,
                        extent=[xmin-pixelsize/2, xmax+pixelsize/2,
                                ymin-pixelsize/2, ymax+pixelsize/2], **kwargs)
    else:
        x, y = np.ogrid[xmin-pixelsize/2 : xmax+pixelsize/2 : (nx+1)*1j,
                        ymin-pixelsize/2 : ymax+pixelsize/2 : (ny+1)*1j]
        ang = np.radians(angle)
        x, y = x*np.cos(ang) - y*np.sin(ang), x*np.sin(ang) + y*np.cos(ang)
        imx = ax.pcolormesh(x, y, img, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)
        ax.axis('image')

    if colorbar:
        cax = ax.inset_axes([1.02, 0, .05, 1], transform=ax.transAxes)
        ticks = MaxNLocator(nticks).tick_values(vmin, vmax)
        cbar = plt.colorbar(imx, cax=cax, ticks=ticks)
        cbar.solids.set_edgecolor("face")  # Remove gaps in PDF http://stackoverflow.com/a/15021541
        if label:
            cbar.set_label(label)
        plt.sca(ax)  # Activate main plot before returning

    ax.minorticks_on()

    return imx

##############################################################################

# Usage example for display_pixels()

if __name__ == '__main__':

    n = 20
    x = np.linspace(-20, 20, n)
    y = np.linspace(-20, 20, n)
    xx, yy = np.meshgrid(x, y)

    # Two Gaussians with different centers
    g1 = np.exp((-((xx - 10)**2 + yy**2))/100)
    g2 = np.exp((-((xx + 8)**2 + (yy - 20)**2))/100)
    counts = g1 + g2
    w = ((xx > -8) | (yy > -5)) & ((xx < 15) | (yy < 5))   # mask

    plt.clf()
    ax = display_pixels(xx[w], yy[w], counts[w], angle=10, colorbar=True)
    plt.pause(1)

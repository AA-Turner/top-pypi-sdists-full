"""
  Copyright (C) 2014-2024, Michele Cappellari
  E-mail: michele.cappellari_at_physics.ox.ac.uk
  http://purl.org/cappellari

    V1.0.0: Created to emulate my IDL procedure with the same name.
        Michele Cappellari, Oxford, 28 March 2014
    V1.1.0: Included reversed colormap. MC, Oxford, 9 August 2015
    V1.1.1: Register colormaps in Matplotlib. MC, Oxford, 29 March 2017
    V1.2.0: Do not re-register colormap. Start x coordinate from zero.
        Reduced numbers duplication to make it easier to modify.
        MC, Oxford, 14 September 2021
    V1.2.1: Replaced deprecated plt.register_cmap with colormaps.register.
        Thanks to Thomas I. Maindl (sdb.ltd) for reporting.
        MC, Oxford, 24 June 2024        
"""

from matplotlib import pyplot as plt
from matplotlib import colors, colormaps
import numpy as np

##############################################################################

# V1.0: SAURON colormap by Michele Cappellari & Eric Emsellem, Leiden, 10 July 2001
#
# Start with these 7 equally spaced coordinates, then add 4 additional control points
# x = np.arange(7)*255/6.
#   [0., 42.5, 85., 127.5, 170., 212.5, 255.]
#
# x = [0, 42.5, 85, 85 + 20, 127.5 - 10, 127.5, 127.5 + 10, 170 - 20, 170, 212.5, 255]
# red =   [0.0, 0.0, 0.4,  0.5, 0.3, 0.0, 0.7, 1.0, 1.0,  1.0, 0.9]
# green = [0.0, 0.0, 0.85, 1.0, 1.0, 0.9, 1.0, 1.0, 0.85, 0.0, 0.9]
# blue =  [0.0, 1.0, 1.0,  1.0, 0.7, 0.0, 0.0, 0.0, 0.0,  0.0, 0.9]

def register_sauron_colormap():
    """Register the 'sauron' and 'sauron_r' colormaps in Matplotlib"""

    if 'sauron' in plt.colormaps():
        return

    # By construction x is symmetric around 1/2: (1 - x)[::-1] - x = 0
    x = np.array([0, 42.5, 85, 105, 117.5, 127.5, 137.5, 150, 170, 212.5, 255])/255
    r = [0.0, 0.0, 0.4,  0.5, 0.3, 0.0, 0.7, 1.0, 1.0,  1.0, 0.9]
    g = [0.0, 0.0, 0.85, 1.0, 1.0, 0.9, 1.0, 1.0, 0.85, 0.0, 0.9]
    b = [0.0, 1.0, 1.0,  1.0, 0.7, 0.0, 0.0, 0.0, 0.0,  0.0, 0.9]

    rr = np.column_stack([x, r, r])
    gg = np.column_stack([x, g, g])
    bb = np.column_stack([x, b, b])
    cdict = {'red': rr, 'green': gg, 'blue': bb}
    sauron = colors.LinearSegmentedColormap('sauron', cdict)
    colormaps.register(cmap=sauron)

    rr = np.column_stack([x, r[::-1], r[::-1]])
    gg = np.column_stack([x, g[::-1], g[::-1]])
    bb = np.column_stack([x, b[::-1], b[::-1]])
    rdict = {'red': rr, 'green': gg, 'blue': bb}
    sauron_r = colors.LinearSegmentedColormap('sauron_r', rdict)
    colormaps.register(cmap=sauron_r)

##############################################################################

# Usage example for the SAURON colormap.

if __name__ == '__main__':

    n = 41 
    x, y = np.ogrid[-n:n, -n:n]
    img = x**2 - 2*y**2

    register_sauron_colormap()
    
    plt.clf()

    plt.subplot(121)
    plt.imshow(img, cmap='sauron')
    plt.title("SAURON colormap")

    plt.subplot(122)
    plt.imshow(img, cmap='sauron_r')
    plt.title("reversed colormap")

#!/usr/bin/env python3
"""
Generates 2D-skymap from RapidPE/RIFT results
"""

__author__ = "Caitlin Rose, Vinaya Valsan"

import os
import sys

import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from matplotlib import rcParams
from astropy.coordinates import SkyCoord
from glob import glob
from ligo.skymap import plot
from ligo.skymap import postprocess
from ligo.skymap.io import fits

import rapidpe_rift_pipe.postscript_utils as postutils

optp = ArgumentParser()
optp.add_argument("input_dir", help="path to event run dir")
optp.add_argument(
    "--ratio-to-include",
    type=str,
    default=None,
    help="if specified, considers outputfile tagged by this from convert_result_to_txt.py ",
)
optp.add_argument("--output-dir", default=None, help="directory to save plots")
opts = optp.parse_args()


print("---------------------Creating skymap---------------------")
input_dir = opts.input_dir

ratio_to_include = opts.ratio_to_include

if opts.output_dir:
    output_dir = opts.output_dir
else:
    output_dir = input_dir


namestr = ratio_to_include.replace(".", "p")
filename = glob(
    input_dir + "/ll_samples_loudest_highweight_" + namestr + ".txt"
)[0]
os.makedirs(os.path.join(input_dir, "summary"), exist_ok=True)

(
    mass1,
    mass2,
    mchirp,
    eta,
    spin1z,
    spin2z,
    distance,
    dec,
    ra,
    inclination,
    phase,
    polarization,
    likelihood,
    prior,
    sampling_function,
    weight,
) = np.loadtxt(filename, skiprows=1, unpack=True)
p = np.asarray(weight)
p /= p.sum()
theta = (np.pi / 2.0) - dec
phi = ra
nside = 256  # 128
npix = hp.pixelfunc.nside2npix(nside)
pixels = hp.pixelfunc.ang2pix(nside, theta, phi, nest=True)
skymap = [0] * npix
index = -1
for i in pixels:
    index = index + 1
    if skymap[i] == 0:
        skymap[i] = p[index]
    else:
        skymap[i] = skymap[i] + p[index]
skymap = skymap / np.sum(skymap)
skymapring = hp.pixelfunc.reorder(skymap, inp="NESTED", out="RING")
sigma = 0.05  # smooting parameter
skymapring = hp.sphtfunc.smoothing(skymapring, sigma=sigma)
skymap = hp.pixelfunc.reorder(skymapring, inp="RING", out="NESTED")
skymap[skymap < 0] = 0
skymap = skymap / np.sum(skymap)
fits.write_sky_map(f"{output_dir}/summary/skymap.fits.gz", skymap)


deg2perpix = hp.nside2pixarea(nside, degrees=True)
probperdeg2 = skymap / deg2perpix
ax = plt.axes(projection="astro hours mollweide")
ax.grid()
vmax = probperdeg2.max()
img = ax.imshow_hpx(
    (probperdeg2, "ICRS"), nested=True, vmin=0.0, vmax=vmax, cmap="cylon"
)
plot.outline_text(ax)

# contour option in ligo-skymap-plot
cls = 100 * postprocess.find_greedy_credible_levels(skymap)
cs = ax.contour_hpx(
    (cls, "ICRS"), nested=True, colors="k", linewidths=0.5, levels=(50, 90)
)
fmt = r"%g\%%" if rcParams["text.usetex"] else "%g%%"
plt.clabel(cs, fmt=fmt, fontsize=6, inline=True)

# annotate option in ligo-skymap-plot
text = []
pp = np.round((50, 90)).astype(int)
ii = np.round(np.searchsorted(np.sort(cls), (50, 90)) * deg2perpix).astype(int)
for i, p in zip(ii, pp):
    text.append("{:d}% area: {:d} deg²".format(p, i, grouping=True))
ax.text(1, 1, "\n".join(text), transform=ax.transAxes, ha="right")


event_info = postutils.event_info(input_dir)
injection_info = event_info.load_injection_info()
if injection_info is not None:
    ax.plot_coord(
        SkyCoord(
            injection_info["longitude"], injection_info["latitude"], unit="rad"
        ),
        "*",
        markerfacecolor="white",
        markeredgecolor="black",
        markersize=10,
    )


plt.savefig(f"{output_dir}/summary/skymap_{namestr}.png")
np.savetxt(
    f"{output_dir}/summary/RapidPE_skymap_{namestr}.dat",
    skymap,
)

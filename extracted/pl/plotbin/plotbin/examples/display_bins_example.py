"""
Michele Cappellari, Oxford, 2026-07-08

Usage example for display_bins with PowerBin.

This builds a toy Vrms field keeps the pixels inside one elliptical isophote,
bins them to nearly constant linear mass with PowerBin, averages Vrms in the
bins, adds noise, and displays the binned map with display_bins and several
interpolation options.

"""
import numpy as np
import matplotlib.pyplot as plt

from jampy.axi.jam_axi_sersic import sersic_profile
from powerbin import PowerBin
from plotbin.display_bins import display_bins

#-----------------------------------------------------------------------------

def display_bins_example():
    """
    Simple display_bins test using equal-mass PowerBin bins.

    """
    inc = 60.0
    qobs = 0.57
    pixelsize = 0.5

    xgrid = np.arange(-55-pixelsize/2, 55+pixelsize/2, pixelsize)
    ygrid = np.arange(-40-pixelsize/2, 40+pixelsize/2, pixelsize)
    x_all, y_all = map(np.ravel, np.meshgrid(xgrid, ygrid))

    # Same toy Vrms field as in jampy.examples.jam_axi_proj_example, evaluated
    # on a regular image grid for display_pixels/display_bins.
    inc_rad = np.radians(inc)
    r = np.sqrt(x_all**2 + (y_all/np.cos(inc_rad))**2)
    a = 40
    vr = 2000*np.sqrt(r)/(r + a)
    vel_all = vr*np.sin(inc_rad)*x_all/r
    sig_all = 8700/(r + a)
    vrms_all = np.sqrt(vel_all**2 + sig_all**2)
    
    re = 20.0
    n_sersic = 4.0
    rell = np.hypot(x_all, y_all/qobs)
    mass_all = sersic_profile(n_sersic, rell/re)

    # Select pixels inside an elliptical isophote.
    good = rell <= np.max(xgrid)

    x = x_all[good]
    y = y_all[good]
    mass = mass_all[good]
    vrms = vrms_all[good]
    
    # Use linear mass as the additive capacity, giving nearly equal-mass bins.
    xy = np.column_stack([x, y])
    nbins = 500  # estimate of the bin number
    target_mass = np.sum(mass)/nbins
    pow = PowerBin(xy, mass, target_mass, pixelsize=pixelsize, verbose=1)
    bin_num = pow.bin_num

    # Average Vrms in each bin. The mass weighting matches the binning capacity.
    nbin = pow.xybin.shape[0]
    mass_bin = np.bincount(bin_num, weights=mass, minlength=nbin)
    vrms_bin = np.sqrt(np.bincount(bin_num, weights=mass*vrms**2, minlength=nbin)/mass_bin)

    vrms_bin_err = 0.05*vrms_bin
    rng = np.random.default_rng(3)
    vrms_bin = rng.normal(vrms_bin, vrms_bin_err)

    plt.figure()
    vmin, vmax = np.percentile(vrms_bin, [1, 99])
    kwargs = dict(colorbar=True, label=r"$V_{\rm rms}$ (km/s)", vmin=vmin, vmax=vmax)
    display_bins(x, y, bin_num, vrms_bin, flux=mass, **kwargs)
    plt.xlabel("x (arcsec)")
    plt.ylabel("y (arcsec)")
    plt.title("Noisy PowerBin Vrms map")

    plt.figure()
    display_bins(x, y, bin_num, vrms_bin, interp=True, flux=mass, **kwargs)
    plt.xlabel("x (arcsec)")
    plt.ylabel("y (arcsec)")
    plt.title("Default interpolation of the binned Vrms")

    plt.figure()
    display_bins(x, y, bin_num, vrms_bin, interp=True,
                 flux=mass, sym='even', num_exact_center=0, **kwargs)
    plt.xlabel("x (arcsec)")
    plt.ylabel("y (arcsec)")
    plt.title("even-symmetric interpolation")

    plt.figure()
    display_bins(x, y, bin_num, vrms_bin, zbin_err=vrms_bin_err, interp=True,
                 flux=mass, sym='even', num_exact_center=0, **kwargs)
    plt.xlabel("x (arcsec)")
    plt.ylabel("y (arcsec)")
    plt.title("Error-smoothed even-symmetric interpolation")

    plt.figure()
    display_bins(x_all, y_all, np.arange(x_all.size), vrms_all, flux=mass_all, **kwargs)
    plt.xlabel("x (arcsec)")
    plt.ylabel("y (arcsec)")
    plt.title("Original noiseless toy Vrms field")

#-----------------------------------------------------------------------------

if __name__ == "__main__":

    display_bins_example()

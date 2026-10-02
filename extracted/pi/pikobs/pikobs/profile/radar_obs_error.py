"""Theoretical radial-velocity observation error, for validation.

A Python copy of the Fortran calc_radvel_obs_error of the radar
assimilation: a look-up table of (base, onset, slope, accel) per radar
network (first letter of the station, C or U) and per antenna elevation,
and a quadratic growth with height above an onset:

    dh      = max(0, h - onset)                       [km]
    sigma_o = clip(base + slope dh + accel dh^2, 2, 16)   [m/s]

Revised calibration 2022053100 -> 2022073100: sigma_o >= the real
standard deviation at every calibration point with Nobs >= 30.

pikobs.profile draws it beside the real sigma when OBS_ERROR_MODEL is
on, and writes it in the calibration table, so a new model can be judged
before the Fortran side is deployed. Once the operational files carry the
new errors, OBS_ERROR in the files is the one to trust.
"""

from typing import Optional

import numpy as np

# (elevation lower, upper) in tenths of a degree -> (base, onset, slope,
# accel); N is the number of calibration points of each class.
_TABLE = {
    'C': [
        ((-999, -1), (3.570404, 99.0, 0.000000, 0.000000)),    # N=3
        ((0, 3), (8.092700, 0.5, 0.737051, 0.000000)),         # N=6
        ((4, 6), (3.795588, 1.5, 0.129861, 0.023308)),         # N=6
        ((7, 9), (3.491600, 0.5, 0.086264, 0.033268)),         # N=8
        ((10, 11), (3.885128, 4.5, 0.113474, 0.117283)),       # N=9
        ((12, 14), (4.174704, 1.5, 0.058653, 0.042064)),       # N=10
        ((15, 18), (3.753986, 3.5, 0.044166, 0.074304)),       # N=11
        ((19, 20), (3.907102, 4.5, 0.106036, 0.087192)),       # N=13
        ((21, 24), (3.791696, 4.5, 0.050372, 0.091061)),       # N=13
        ((25, 31), (3.801294, 4.5, 0.083894, 0.079856)),       # N=15
        ((32, 40), (4.197492, 5.5, 0.075658, 0.153273)),       # N=14
        ((41, 48), (4.407397, 7.5, 0.859283, 0.122748)),       # N=14
        ((49, 60), (4.521300, 6.5, 0.000000, 0.198585)),       # N=14
        ((61, 76), (3.924617, 4.5, 0.007715, 0.075932)),       # N=14
        ((77, 92), (4.259625, 4.5, 0.156861, 0.044562)),       # N=13
        ((93, 108), (3.816149, 5.5, 0.146793, 0.081248)),      # N=13
        ((109, 132), (3.811158, 4.5, 0.120052, 0.058104)),     # N=12
        ((133, 164), (3.954562, 4.5, 0.002498, 0.069374)),     # N=9
        ((165, 196), (3.815400, 4.5, 0.193684, 0.048023)),     # N=7
        ((197, 228), (4.158800, 5.5, 0.372549, 0.023513)),     # N=6
        ((229, 9999), (4.442500, 6.5, 0.832865, 0.000000)),    # N=5
    ],
    'U': [
        ((-999, -1), (3.852986, 99.0, 0.000000, 0.000000)),    # N=3
        ((0, 2), (4.165516, 1.5, 0.237484, 0.000000)),         # N=9
        ((3, 3), (4.208900, 0.5, 0.020554, 0.029796)),         # N=6
        ((4, 4), (4.216400, 0.5, 0.077158, 0.000000)),         # N=6
        ((5, 7), (4.139639, 1.5, 0.280885, 0.000571)),         # N=8
        ((8, 11), (5.338063, 1.5, 0.346756, 0.001020)),        # N=10
        ((12, 13), (5.385510, 0.5, 0.237824, 0.010341)),       # N=13
        ((14, 16), (2.465817, 0.5, 0.539898, 0.000000)),       # N=11
        ((17, 21), (4.408275, 0.5, 0.225724, 0.018018)),       # N=15
        ((22, 24), (4.079790, 1.5, 0.053722, 0.039978)),       # N=15
        ((25, 28), (3.960086, 3.5, 0.260212, 0.027246)),       # N=13
        ((29, 33), (4.374351, 2.5, 0.094801, 0.042317)),       # N=14
        ((34, 37), (4.008751, 8.5, 0.810741, 0.059391)),       # N=14
        ((38, 42), (5.051197, 3.5, 0.150155, 0.046717)),       # N=14
        ((43, 48), (4.242615, 4.5, 0.196911, 0.000087)),       # N=13
        ((49, 57), (4.854939, 4.5, 0.179369, 0.050047)),       # N=14
        ((58, 72), (4.883054, 2.5, 0.151684, 0.030123)),       # N=14
        ((73, 90), (4.393236, 2.5, 0.190922, 0.025627)),       # N=13
        ((91, 110), (4.351659, 3.5, 0.162661, 0.033905)),      # N=13
        ((111, 122), (4.416174, 3.5, 0.304101, 0.012084)),     # N=12
        ((123, 132), (4.703718, 3.5, 0.211000, 0.018392)),     # N=12
        ((133, 148), (4.146918, 4.5, 0.160778, 0.037805)),     # N=12
        ((149, 161), (5.156168, 4.5, 0.114622, 0.042467)),     # N=11
        ((162, 181), (5.155605, 4.5, 0.412761, 0.012559)),     # N=10
        ((182, 9999), (4.841900, 5.5, 0.287717, 0.030053)),    # N=9
    ],
}
_DEFAULT = (3.7, 4.0, 0.5, 0.0)


def coefficients(station: str, elevation_deg: float):
    """(base, onset, slope, accel) of a station's network and elevation."""
    net = str(station)[:1].upper()
    tenths = int(round(float(elevation_deg) * 10.0))
    for (lo, hi), coef in _TABLE.get(net, []):
        if lo <= tenths <= hi:
            return coef
    return _DEFAULT


def model_obs_error(height_km, elevation_deg: Optional[float],
                    station: str) -> np.ndarray:
    """sigma_o [m/s] of the model at the given heights [km]."""
    h = np.asarray(height_km, float)
    if elevation_deg is None:
        return np.full_like(h, np.nan)
    base, onset, slope, accel = coefficients(station, elevation_deg)
    dh = np.maximum(0.0, h - onset)
    return np.clip(base + slope * dh + accel * dh * dh, 2.0, 16.0)

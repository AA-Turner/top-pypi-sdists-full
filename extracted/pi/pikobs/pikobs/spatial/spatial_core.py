"""
Spatial correlogram of an observation-space quantity (e.g. OmP) as a
function of great-circle distance -- the Hollingsworth-Lönnberg (1986)
method, standard in NWP data assimilation for estimating observation
error correlation length scales.

Method
------
1. Anomalies: subtract the GLOBAL mean from the quantity (e.g. OmP)
   before doing anything else. This matters: a spatially-varying
   systematic bias (e.g. latitude-dependent) would otherwise show up
   as spurious long-range "correlation" that has nothing to do with
   the actual random error structure.
2. Every PAIR of observations within a maximum separation distance
   contributes one covariance sample: anomaly[i] * anomaly[j].
   Finding these pairs is the expensive part for a large dataset (a
   naive "every observation against every other" is O(N^2), which is
   infeasible past a few thousand observations) -- solved here with a
   KD-tree built on each observation's 3D Cartesian position on the
   unit sphere (so straight-line/chord distance in 3D is a monotonic
   function of great-circle distance), and scipy's own query_pairs,
   which finds every pair within a cutoff WITHOUT ever computing the
   full N^2 distance matrix.
3. Pairs are binned by distance; the MEAN covariance product in each
   bin, divided by the zero-lag variance (the anomalies' own
   variance), gives the correlation at that distance -- the
   correlogram.

Scalability
-----------
For anything past ``max_obs`` observations (default 50,000), a random
subsample is used instead of the full dataset -- even with the KD-tree
cutoff, a large enough and sufficiently DENSE set of observations
(e.g. a single high-resolution satellite swath) could still produce
an unmanageable number of pairs within the cutoff radius. 50,000
points already gives many millions of candidate pairs for a several-
thousand-km cutoff, which is enough to resolve a correlogram with low
noise while keeping both memory and runtime bounded regardless of how
large the actual input file is.
"""

import numpy as np
from scipy.spatial import cKDTree

EARTH_RADIUS_KM = 6371.0


def compute_correlogram(lat, lon, values, max_dist_km=3000.0, n_bins=30,
                        max_obs=50000, seed=42, min_pairs_per_bin=30):
    """
    Compute the spatial correlation of `values` as a function of
    great-circle distance.

    Args:
        lat, lon: 1D arrays, degrees.
        values: 1D array, the quantity to correlate (e.g. OmP).
        max_dist_km: maximum pair separation to consider. Correlation
            beyond this is assumed negligible and not computed --
            this is also what keeps runtime bounded (see module
            docstring).
        n_bins: number of distance bins between 0 and max_dist_km.
        max_obs: random-subsample cap (see module docstring).
        seed: RNG seed for the subsample, for reproducibility.
        min_pairs_per_bin: bins with fewer pairs than this are set to
            NaN in the output rather than reporting a noisy estimate
            from too few samples.

    Returns:
        dict with bin_centers_km, correlation, n_pairs (per bin),
        zero_lag_variance, n_obs_used, n_total_pairs.
    """
    lat = np.asarray(lat, dtype=np.float64)
    lon = np.asarray(lon, dtype=np.float64)
    values = np.asarray(values, dtype=np.float64)

    finite = np.isfinite(lat) & np.isfinite(lon) & np.isfinite(values)
    lat, lon, values = lat[finite], lon[finite], values[finite]
    n = len(values)
    if n < 2:
        raise ValueError(f"Need at least 2 finite observations, got {n}")

    if n > max_obs:
        rng = np.random.default_rng(seed)
        idx = rng.choice(n, size=max_obs, replace=False)
        lat, lon, values = lat[idx], lon[idx], values[idx]
        n = max_obs

    anomaly = values - np.mean(values)
    variance = float(np.mean(anomaly ** 2))
    if variance <= 0:
        raise ValueError("Zero variance in the input values -- cannot normalise to a correlation.")

    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    points = np.column_stack([x, y, z])

    tree = cKDTree(points)
    # Chord length on the unit sphere corresponding to max_dist_km of
    # great-circle separation: chord = 2*sin(d / (2R)).
    max_chord = 2.0 * np.sin(max_dist_km / (2.0 * EARTH_RADIUS_KM))
    pairs = tree.query_pairs(max_chord, output_type="ndarray")

    if len(pairs) == 0:
        raise ValueError(
            "No observation pairs found within max_dist_km -- check "
            "that lat/lon are in degrees and max_dist_km is reasonable."
        )

    i, j = pairs[:, 0], pairs[:, 1]
    chord = np.sqrt(np.sum((points[i] - points[j]) ** 2, axis=1))
    chord = np.clip(chord, 0.0, 2.0)
    dist_km = 2.0 * EARTH_RADIUS_KM * np.arcsin(chord / 2.0)

    cov_product = anomaly[i] * anomaly[j]

    bin_edges = np.linspace(0.0, max_dist_km, n_bins + 1)
    bin_idx = np.clip(np.digitize(dist_km, bin_edges) - 1, 0, n_bins - 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    mean_cov = np.full(n_bins, np.nan)
    n_pairs_per_bin = np.zeros(n_bins, dtype=np.int64)
    for b in range(n_bins):
        mask = bin_idx == b
        cnt = int(mask.sum())
        n_pairs_per_bin[b] = cnt
        if cnt >= min_pairs_per_bin:
            mean_cov[b] = cov_product[mask].mean()

    correlation = mean_cov / variance

    return {
        "bin_centers_km": bin_centers,
        "correlation": correlation,
        "n_pairs": n_pairs_per_bin,
        "zero_lag_variance": variance,
        "n_obs_used": n,
        "n_total_pairs": len(pairs),
    }

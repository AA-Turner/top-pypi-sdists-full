from statistics import NormalDist


def z_score(ci: float = 0.95) -> float:
    """Two-sided critical z-score for confidence level `ci` in (0, 1)."""
    if not 0.0 < ci < 1.0:
        raise ValueError("ci must be between 0 and 1 (exclusive)")
    return NormalDist().inv_cdf((1.0 + ci) / 2.0)

"""Calculate Bayesian credibility intervals for online polling using the Ipsos method."""
from __future__ import annotations

import math

from scipy import stats


def get(sample_size: int, weight: float = 1.3, confidence_level: float = 0.95) -> float:
    """Calculate the Ipsos credibility interval for a given sample size.

    The Ipsos credibility interval is a Bayesian metric that can be used to
    calculate the margin of error for online polling. It estimates accuracy
    plus or minus a number of percentage points.

    You can learn more by reading the Ipsos white papers at:
    https://www.ipsos.com/sites/default/files/2017-03/IpsosPA_CredibilityIntervals.pdf
    https://www.ipsos.com/sites/default/files/ct/publication/documents/2021-03/credibility_intervals_for_online_polling_-_2021.pdf

    Args:
        sample_size (int): the size of the sample
        weight (float): the weight to apply to formula. Default is 1.3.
        confidence_level (float): the confidence level to use for the interval. Default is 0.95.

    Returns:
        float: the Ipsos credibility interval, which is a margin of error measured as percentage points.

    Examples:
        >>> import ipsos_credibility_interval
        >>> ipsos_credibility_interval.get(2000)
        2.498473650777201
        >>> ipsos_credibility_interval.get(1000)
        3.5333753221609374
        >>> ipsos_credibility_interval.get(500)
        4.996947301554402
    """
    # Use the confidence level to calculate the expected distribution
    p = (1 - confidence_level) / 2
    z = abs(stats.norm.ppf(p, 0, 1))

    # Calculate the Ipsos credibility interval
    ici = z * math.sqrt(weight) * (1 / (2 * math.sqrt(sample_size)))

    # Multiply by 100 to convert to percentage points
    return ici * 100

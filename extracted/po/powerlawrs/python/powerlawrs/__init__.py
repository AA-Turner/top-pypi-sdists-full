# Copyright (c) 2025 Adam Ulichny
#
# This source code is licensed under the MIT OR Apache-2.0 license
# that can be found in the LICENSE-MIT or LICENSE-APACHE files
# at the root of this source tree.

"""
powerlawrs: A Python package for analyzing power-law distributions.
"""

# Import the native Rust module
from . import _powerlawrs
import matplotlib.pyplot as plt
import numpy as np


# Expose the submodules from the native module at the package level
stats = _powerlawrs.stats
util = _powerlawrs.util
dist = _powerlawrs.dist

# For convenience, nested modules are exposed directly
exponential = dist.exponential
powerlaw = dist.powerlaw
pareto = dist.pareto
lognormal = dist.lognormal

# The `Powerlaw` class needs these
estimation = pareto.estimation
gof = pareto.gof
hypothesis = pareto.hypothesis

class Powerlaw:
    """
    A class to fit and analyze power-law distributions in a given dataset.
    """
    def __init__(self, data):
        """
        Initializes the Powerlaw object with data.

        Args:
            data (list[float]): The dataset to analyze.
        """
        self.data = data
        self.alphas = None
        self.x_mins = None
        self.ParetoFit = None

    def fit(self):
        """
        Fits the data to a power-law distribution.

        This method finds the optimal x_min and alpha parameters for the power-law
        fit and assesses the goodness of fit. The results are stored in the
        object's attributes.
        """
        # Ensure data is sorted for some of the underlying functions
        self.sorted_data = sorted(self.data)

        # find_alphas_fast returns a list of tuples, but we want two separate lists
        (self.x_mins, self.alphas) = estimation.find_alphas_fast(self.sorted_data)

        # gof expects the full dataset, not just the tail
        self.ParetoFit = gof.gof(self.sorted_data, self.x_mins, self.alphas)
        return

    def plot(self):
        """
        Plots the CCDF of the data and plots the model. Plots for the entire distribution 
        as well as just the tail are shown.
        """
        if self.ParetoFit is None: 
            raise RuntimeError("You must call 'fit()' before plotting.")

        # full-sample empirical CCDF 
        n = len(self.sorted_data)
        # fit sorts ascending, we need descending.
        y_all = np.arange(n, 0, -1) / n   # P(X >= x) with denominator n

        # extract tail data
        tail = [x for x in self.sorted_data if x >= self.ParetoFit.x_min]
        sorted_tail = sorted(tail, reverse=True)
        m = len(sorted_tail)
        y_tail = np.arange(1, m+1) / m   # P(X >= x | x >= xmin) with denom m

        # model lines
        x_line = np.linspace(self.ParetoFit.x_min, max(self.sorted_data), 200)
        s_tail_model = np.array([pareto.Pareto(self.ParetoFit.alpha, self.ParetoFit.x_min).ccdf(x) for x in x_line])
        s_full_model = (m / n) * s_tail_model        # S_full(x) to compare with full-sample CCDF

        # Plot 1: full empirical CCDF + full-sample scaled model
        plt.figure(figsize=(10,6))
        plt.loglog(self.sorted_data, y_all, '.', label='Empirical CCDF')
        plt.loglog(x_line, s_full_model, '-', lw=2, label='Pareto Type I')
        plt.axvline(x=self.ParetoFit.x_min, color='k', ls='--', label=f'x_min={self.ParetoFit.x_min:.3g}')
        plt.xlabel('x'); plt.ylabel('P(X >= x)')
        plt.legend(); plt.grid(True, which='both', ls='--', alpha=0.6)
        plt.title('Full-sample CCDF and Pareto Type I Model')
        plt.show()

        # Plot 2: tail-only empirical CCDF + tail-conditional model (CSN style)
        plt.figure(figsize=(10,5))
        plt.loglog(sorted_tail, y_tail, '.', label='Empirical tail CCDF')
        plt.loglog(x_line, s_tail_model, '-', lw=2, label='Pareto Type I')
        plt.axvline(x=self.ParetoFit.x_min, color='k', ls='--', label=f'x_min={self.ParetoFit.x_min:.3g}')
        plt.xlabel('x'); plt.ylabel('P(X >= x | x >= x_min)')
        plt.legend(); plt.grid(True, which='both', ls='--', alpha=0.6)
        plt.title('Tail-only CCDF and Pareto Type I Model')
        plt.show()


def fit(data):
    """
    Fits the data to a power-law distribution.

    This function is a convenience wrapper that instantiates the Powerlaw class,
    fits the data, and returns the ParetoFit results.

    Args:
        data (list[float]): The dataset to analyze.

    Returns:
        The ParetoFit result object.
    """
    p = Powerlaw(data)
    p.fit()
    return p

# Define what gets imported with 'from powerlawrs import *'
__all__ = [
    "fit",
    "Powerlaw",
    "stats",
    "util",
    "dist",
    "exponential",
    "lognormal",
    "powerlaw",
    "pareto",
    "estimation",
    "gof",
    "hypothesis",
]

# Package-level metadata
__version__ = "0.1.0"
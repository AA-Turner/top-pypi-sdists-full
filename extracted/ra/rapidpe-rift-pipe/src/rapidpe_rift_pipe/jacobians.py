#!/usr/bin/env python3

__author__ = "Soichiro Morisaki, Vinaya Valsan"

import numpy as np
from rapid_pe import amrlib


# Jacobian used in posterior calculations.


def uniform_m1_m2_prior_in_mchirp_eta(mchirp, eta):
    """
    Returns  jacobian  p(mchirp, eta) = d(mass1,mass2)/d(mchirp,eta)
    """
    p = np.abs(mchirp * eta ** (-1.2) * (1.0 - 4.0 * eta) ** (-0.5))
    return p


def uniform_m1_m2_prior_in_mchirp_q(mchirp, q):
    """
    Returns  jacobian  p(mchirp, q) = d(mass1,mass2)/d(mchirp,q)
    """
    p = np.abs(mchirp * (1.0 + q) ** 0.4 * q ** (-1.2))
    return p


def uniform_m1_m2_prior_in_mtotal_q(mtotal, q):
    """
    Returns  jacobian  p(mtotal, q) = d(mass1,mass2)/d(mtotal,q)
    """
    p = np.abs(mtotal * (1 + q) ** (-2))
    return p


def uniform_m1_m2_prior_in_tau0_tau3(tau0, tau3, f_lower):
    """
    Returns  jacobian  p(tau0, tau3) = d(mass1,mass2)/d(tau0,tau3)
    """
    a3 = np.pi / (8.0 * (np.pi * f_lower) ** (5.0 / 3.0))
    a0 = 5.0 / (256.0 * (np.pi * f_lower) ** (8.0 / 3.0))
    tmp1 = (a0 * tau3) / (a3 * tau0)
    num = a0 * (tmp1) ** (1.0 / 3.0)
    tmp2 = 1 - ((4 * a3) / (tau3 * tmp1 ** (2.0 / 3.0)))
    den = tau0**2.0 * tau3 * np.sqrt(tmp2)
    return np.abs(num / den)


def uniform_m1m2chi1chi2_prior_to_mu1mu2qchi2(mu1, mu2, q, s2z):
    """Return d(mu1, mu2, q, s2z) / d(m1, m2, s1z, s2z)"""
    MsunToTime = 4.92659 * 10.0 ** (
        -6.0
    )  # conversion from solar mass to seconds
    fref_mu = 200.0
    # coefficients of mu1 and mu2
    mu_coeffs = np.array(
        [
            [0.97437198, 0.20868103, 0.08397302],
            [-0.22132704, 0.82273827, 0.52356096],
        ]
    )
    m1, m2, s1z, s2z = amrlib.transform_mu1mu2qs2z_m1m2s1zs2z(mu1, mu2, q, s2z)
    mc = (m1 * m2) ** (3.0 / 5.0) / (m1 + m2) ** (1.0 / 5.0)
    q = m2 / m1
    eta = amrlib.qToeta(q)
    x = np.pi * mc * MsunToTime * fref_mu
    tmp1 = (
        mu_coeffs[0, 2] * mu_coeffs[1, 0] - mu_coeffs[0, 0] * mu_coeffs[1, 2]
    )
    tmp2 = (
        mu_coeffs[0, 2] * mu_coeffs[1, 1] - mu_coeffs[0, 1] * mu_coeffs[1, 2]
    )
    denominator = (
        x
        * 5.0
        * (113.0 + 75.0 * q)
        * (
            252.0 * tmp1 * q * eta ** (-3.0 / 5.0)
            + tmp2 * (743.0 + 2410.0 * q + 743.0 * q**2.0) * x ** (2.0 / 3.0)
        )
    )
    numerator = (
        m1**2.0 * 4128768.0 * q * (1.0 + q) ** 2.0 * x ** (10.0 / 3.0)
    )
    return np.abs(numerator / denominator)


PRIOR_MAP = {
    "mchirp_eta": uniform_m1_m2_prior_in_mchirp_eta,
    "tau0_tau3": uniform_m1_m2_prior_in_tau0_tau3,
    "mchirp_q": uniform_m1_m2_prior_in_mchirp_q,
    "mtotal_q": uniform_m1_m2_prior_in_mtotal_q,
    "mu1_mu2_q_s2q": uniform_m1m2chi1chi2_prior_to_mu1mu2qchi2,
}

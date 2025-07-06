# ----------------------------------------------------------------------------
# Description    : Simulation functions for the filters in Qblox hardware.
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2024)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import warnings

import numpy as np
from scipy.signal import lfilter

# -- functions ---------------------------------------------------------------


def get_filter_delay(number_of_exp: int = 0, fir: bool = False) -> float:
    """Return the delay for an output given active filters.

    Enabling the real-time predistortion filters in Qblox hardware
    introduces a delay in the output path. This function can be used to
    calculate the delay when different combinations of filters are activated.

    Parameters
    ----------
    number_of_exp : int
        The number of exponential filters active.
    fir : bool
        Whether the FIR filter is active.

    Returns
    -------
    delay
        The extra delay due to the active filters in seconds.
    """
    exp_dly_clk = 25
    fir_dly_clk = 40
    any_filt = 10 + 11
    is_filtered = number_of_exp > 0 or fir
    delay = 1e-9 * (
        2 * is_filtered * (any_filt + exp_dly_clk * number_of_exp + fir_dly_clk * fir + 7)
        + 1 * 4 * is_filtered
    )
    return delay


def exponential_overshoot_correction(
    sig: np.ndarray,
    amp: float,
    tau: float,
) -> np.ndarray:
    """Simulate the exponential overshoot correction filter.

    Parameters
    ----------
    sig : array_like
        Input signal to the filter in units of relative DAC amplitude.
    amp : float
        Relative amplitude of exponential overshoot.
        Note that a positive (negative) amplitude predistorts
        such that an overshoot (undershoot) is corrected.
    tau : float
        Time constant of the exponential overshoot.

    Returns
    -------
    predistorted
        The output signal from the filter.
    """
    alpha = 1 - np.exp(-1 / (tau))
    k = amp
    den = np.array([1, -(1 - alpha)])
    num = [alpha]
    predistorted = k * (lfilter(num, den, sig) - sig) + sig
    if np.any(predistorted > 1.0) or np.any(predistorted < -1.0):
        warnings.warn(
            "Qblox simulator plugin WARNING: Output will be clipped."
            "The result of the simulation cannot be trusted."
        )
    return predistorted


def fir_correction(sig: np.ndarray, coeffs: np.ndarray) -> np.ndarray:
    """Simulate the ideal fir filter.

    Parameters
    ----------
    sig : array_like
        Input signal to the filter in units of relative DAC amplitude.
    coeffs : array_like
        Coefficients of the FIR filter.

    Returns
    -------
    predistorted
        The output signal from the filter.
    """
    predistorted = lfilter(coeffs, [1], sig)
    if np.any(predistorted > 1.0) or np.any(predistorted < -1.0):
        warnings.warn(
            "Qblox simulator plugin WARNING: Output will be clipped."
            "The result of the simulation cannot be trusted."
        )
    return predistorted


def get_impulse_response(
    response_length,
    exp0_time_constant: float = 0.0,
    exp0_amplitude: float = 0.0,
    exp1_time_constant: float = 0.0,
    exp1_amplitude: float = 0.0,
    exp2_time_constant: float = 0.0,
    exp2_amplitude: float = 0.0,
    exp3_time_constant: float = 0.0,
    exp3_amplitude: float = 0.0,
    fir_coeffs=None,
) -> np.ndarray:
    """Return an impulse response given a set of coefficients for an output.

    This function can be used to convert the coefficients
    of the filters in the Qblox hardware into a long FIR filter.

    Parameters
    ----------
    response_length : int
        Length of the impulse response returned.
    exp0_time_constant : float
        Time constant of the exponential overshoot.
    exp0_amplitude : float
        Relative amplitude of exponential overshoot.
        Note that a positive (negative) amplitude predistorts
        such that an overshoot (undershoot) is corrected.
    exp1_time_constant : float
        Time constant of the exponential overshoot.
    exp1_amplitude : float
        Relative amplitude of exponential overshoot.
        Note that a positive (negative) amplitude predistorts
        such that an overshoot (undershoot) is corrected.
    exp2_time_constant : float
        Time constant of the exponential overshoot.
    exp2_amplitude : float
        Relative amplitude of exponential overshoot.
        Note that a positive (negative) amplitude predistorts
        such that an overshoot (undershoot) is corrected.
    exp3_time_constant : float
        Time constant of the exponential overshoot.
    exp3_amplitude : float
        Relative amplitude of exponential overshoot.
        Note that a positive (negative) amplitude predistorts
        such that an overshoot (undershoot) is corrected.
    fir_coeffs : array_like
        Coefficients of the FIR filter.

    Returns:
        impulse_response
            The impulse response of the system.

    """
    # pylint: disable=too-many-arguments
    if fir_coeffs is None:
        fir_coeffs = [1.0] + [0.0] * 31
    impulse_response = np.zeros(response_length)
    impulse_response[0] = 1.0
    impulse_response = exponential_overshoot_correction(
        impulse_response, exp0_amplitude, exp0_time_constant
    )
    impulse_response = exponential_overshoot_correction(
        impulse_response, exp1_amplitude, exp1_time_constant
    )
    impulse_response = exponential_overshoot_correction(
        impulse_response, exp2_amplitude, exp2_time_constant
    )
    impulse_response = exponential_overshoot_correction(
        impulse_response, exp3_amplitude, exp3_time_constant
    )
    impulse_response = fir_correction(impulse_response, fir_coeffs)

    return impulse_response

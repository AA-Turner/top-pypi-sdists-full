#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=False
"""
Hamilton filter

Author: Chad Fulton
License: Simplified-BSD
"""

# Typical imports
import numpy as np
import warnings
cimport numpy as np
cimport cython
from statsmodels.src.math cimport dlog, zlog, dexp, zexp

cdef int FORTRAN = 1


def shamilton_filter_log(int nobs, int k_regimes, int order,
                                  np.float32_t [:,:,:] regime_transition,
                                  np.float32_t [:,:] conditional_likelihoods,
                                  np.float32_t [:] joint_likelihoods,
                                  np.float32_t [:,:] predicted_joint_probabilities,
                                  np.float32_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, regime_transition_t = 0, time_varying_regime_transition
    cdef:
        # k_regimes_order_m1 is not used when order == 0.
        int k_regimes_order_m1 = k_regimes**max(order - 1, 0)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float32_t [:] weighted_likelihoods, tmp_filtered_marginalized_probabilities, tmp_predicted_joint_probabilities
        np.float64_t tmp_max_real
        np.float32_t tmp_max

    time_varying_regime_transition = regime_transition.shape[2] > 1
    weighted_likelihoods = np.zeros(k_regimes_order_p1, dtype=np.float32)
    # tmp_filtered_marginalized_probabilities is not used if order == 0.
    tmp_filtered_marginalized_probabilities = np.zeros(k_regimes_order, dtype=np.float32)
    tmp_predicted_joint_probabilities = np.zeros(k_regimes, dtype=np.float32)

    with nogil:
        for t in range(nobs):
            if time_varying_regime_transition:
                regime_transition_t = t

            if order > 0:
                # Collapse filtered joint probabilities over the last dimension
                # Pr[S_{t-1}, ..., S_{t-r} | t-1] = \sum_{ S_{t-r-1} } Pr[S_{t-1}, ..., S_{t-r}, S_{t-r-1} | t-1]
                ix = 0
                # tmp_filtered_marginalized_probabilities[:] = 0
                for j in range(k_regimes_order):
                    # This is logsumexp, so we use the maximum trick
                    tmp_max_real = filtered_joint_probabilities[ix, t]
                    tmp_max = filtered_joint_probabilities[ix, t]
                    for i in range(k_regimes):
                        if filtered_joint_probabilities[ix + i, t] > tmp_max_real:
                            tmp_max_real = filtered_joint_probabilities[ix + i, t]
                            tmp_max = filtered_joint_probabilities[ix + i, t]

                    tmp_filtered_marginalized_probabilities[j] = 0
                    for i in range(k_regimes):
                        tmp_filtered_marginalized_probabilities[j] = (
                            tmp_filtered_marginalized_probabilities[j] +
                            dexp(filtered_joint_probabilities[ix, t] - tmp_max))
                        ix = ix + 1
                    tmp_filtered_marginalized_probabilities[j] = (tmp_max +
                      dlog(tmp_filtered_marginalized_probabilities[j]))

            shamilton_filter_log_iteration(t, k_regimes, order,
                                      regime_transition[:, :, regime_transition_t],
                                      weighted_likelihoods,
                                      tmp_filtered_marginalized_probabilities,
                                      conditional_likelihoods[:, t],
                                      joint_likelihoods,
                                      predicted_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t+1],
                                      tmp_predicted_joint_probabilities)


cdef void shamilton_filter_log_iteration(int t, int k_regimes, int order,
                              np.float32_t [:,:] regime_transition,
                              np.float32_t [:] weighted_likelihoods,
                              np.float32_t [:] prev_filtered_marginalized_probabilities,
                              np.float32_t [:] conditional_likelihoods,
                              np.float32_t [:] joint_likelihoods,
                              np.float32_t [:] curr_predicted_joint_probabilities,
                              np.float32_t [:] prev_filtered_joint_probabilities,
                              np.float32_t [:] curr_filtered_joint_probabilities,
                              np.float32_t [:] tmp_predicted_joint_probabilities) noexcept nogil:
    cdef int i, j, k, ix
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float64_t tmp_max_real
        np.float32_t tmp_max

    # Compute predicted joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] = Pr[S_t | S_{t-1}] * Pr[S_{t-1}, ..., S_{t-r} | t-1]
    if order > 0:
        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    curr_predicted_joint_probabilities[ix] = (
                        prev_filtered_marginalized_probabilities[j * k_regimes_order_m1 + k] +
                        regime_transition[i, j])
                    ix += 1
    else:
        curr_predicted_joint_probabilities[:] = 0
        for i in range(k_regimes):
            # Again, this is logsumexp, so we use the maximum trick
            tmp_max_real = 0
            tmp_max = 0
            for j in range(k_regimes):
                tmp_predicted_joint_probabilities[j] = (
                    prev_filtered_joint_probabilities[j] + regime_transition[i, j])
                if tmp_predicted_joint_probabilities[j] > tmp_max_real:
                    tmp_max_real = tmp_predicted_joint_probabilities[j]
                    tmp_max = tmp_predicted_joint_probabilities[j]

            curr_predicted_joint_probabilities[i] = 0
            for j in range(k_regimes):
                curr_predicted_joint_probabilities[i] = (
                  curr_predicted_joint_probabilities[i] +
                  dexp(tmp_predicted_joint_probabilities[j] - tmp_max))

            curr_predicted_joint_probabilities[i] = (tmp_max +
              dlog(curr_predicted_joint_probabilities[i]))


    # Compute weighted likelihoods f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) * Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1]
    tmp_max_real = 0
    tmp_max = 0
    for i in range(k_regimes_order_p1):
        weighted_likelihoods[i] = (
            curr_predicted_joint_probabilities[i] +
            conditional_likelihoods[i])

        # Compute the maximum for use below in logsumexp
        if weighted_likelihoods[i] > tmp_max_real:
            tmp_max_real = weighted_likelihoods[i]
            tmp_max = weighted_likelihoods[i]

    # Compute the joint likelihood f(y_t | t-1)
    # Again, this is logsumexp, so we use the maximum trick (where the
    # maximum was just computed above)
    joint_likelihoods[t] = 0
    for i in range(k_regimes_order_p1):
        joint_likelihoods[t] = (
          joint_likelihoods[t] +
          dexp(weighted_likelihoods[i] - tmp_max))
    joint_likelihoods[t] = tmp_max + dlog(joint_likelihoods[t])

    # Compute filtered joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t] = (
    #     f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) *
    #     Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] /
    #     f(y_t | t-1))
    for i in range(k_regimes_order_p1):
        # TODO: do I need to worry about some value for joint_likelihoods?
        curr_filtered_joint_probabilities[i] = (
            weighted_likelihoods[i] - joint_likelihoods[t])


def dhamilton_filter_log(int nobs, int k_regimes, int order,
                                  np.float64_t [:,:,:] regime_transition,
                                  np.float64_t [:,:] conditional_likelihoods,
                                  np.float64_t [:] joint_likelihoods,
                                  np.float64_t [:,:] predicted_joint_probabilities,
                                  np.float64_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, regime_transition_t = 0, time_varying_regime_transition
    cdef:
        # k_regimes_order_m1 is not used when order == 0.
        int k_regimes_order_m1 = k_regimes**max(order - 1, 0)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float64_t [:] weighted_likelihoods, tmp_filtered_marginalized_probabilities, tmp_predicted_joint_probabilities
        np.float64_t tmp_max_real
        np.float64_t tmp_max

    time_varying_regime_transition = regime_transition.shape[2] > 1
    weighted_likelihoods = np.zeros(k_regimes_order_p1, dtype=float)
    # tmp_filtered_marginalized_probabilities is not used if order == 0.
    tmp_filtered_marginalized_probabilities = np.zeros(k_regimes_order, dtype=float)
    tmp_predicted_joint_probabilities = np.zeros(k_regimes, dtype=float)

    with nogil:
        for t in range(nobs):
            if time_varying_regime_transition:
                regime_transition_t = t

            if order > 0:
                # Collapse filtered joint probabilities over the last dimension
                # Pr[S_{t-1}, ..., S_{t-r} | t-1] = \sum_{ S_{t-r-1} } Pr[S_{t-1}, ..., S_{t-r}, S_{t-r-1} | t-1]
                ix = 0
                # tmp_filtered_marginalized_probabilities[:] = 0
                for j in range(k_regimes_order):
                    # This is logsumexp, so we use the maximum trick
                    tmp_max_real = filtered_joint_probabilities[ix, t]
                    tmp_max = filtered_joint_probabilities[ix, t]
                    for i in range(k_regimes):
                        if filtered_joint_probabilities[ix + i, t] > tmp_max_real:
                            tmp_max_real = filtered_joint_probabilities[ix + i, t]
                            tmp_max = filtered_joint_probabilities[ix + i, t]

                    tmp_filtered_marginalized_probabilities[j] = 0
                    for i in range(k_regimes):
                        tmp_filtered_marginalized_probabilities[j] = (
                            tmp_filtered_marginalized_probabilities[j] +
                            dexp(filtered_joint_probabilities[ix, t] - tmp_max))
                        ix = ix + 1
                    tmp_filtered_marginalized_probabilities[j] = (tmp_max +
                      dlog(tmp_filtered_marginalized_probabilities[j]))

            dhamilton_filter_log_iteration(t, k_regimes, order,
                                      regime_transition[:, :, regime_transition_t],
                                      weighted_likelihoods,
                                      tmp_filtered_marginalized_probabilities,
                                      conditional_likelihoods[:, t],
                                      joint_likelihoods,
                                      predicted_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t+1],
                                      tmp_predicted_joint_probabilities)


cdef void dhamilton_filter_log_iteration(int t, int k_regimes, int order,
                              np.float64_t [:,:] regime_transition,
                              np.float64_t [:] weighted_likelihoods,
                              np.float64_t [:] prev_filtered_marginalized_probabilities,
                              np.float64_t [:] conditional_likelihoods,
                              np.float64_t [:] joint_likelihoods,
                              np.float64_t [:] curr_predicted_joint_probabilities,
                              np.float64_t [:] prev_filtered_joint_probabilities,
                              np.float64_t [:] curr_filtered_joint_probabilities,
                              np.float64_t [:] tmp_predicted_joint_probabilities) noexcept nogil:
    cdef int i, j, k, ix
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float64_t tmp_max_real
        np.float64_t tmp_max

    # Compute predicted joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] = Pr[S_t | S_{t-1}] * Pr[S_{t-1}, ..., S_{t-r} | t-1]
    if order > 0:
        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    curr_predicted_joint_probabilities[ix] = (
                        prev_filtered_marginalized_probabilities[j * k_regimes_order_m1 + k] +
                        regime_transition[i, j])
                    ix += 1
    else:
        curr_predicted_joint_probabilities[:] = 0
        for i in range(k_regimes):
            # Again, this is logsumexp, so we use the maximum trick
            tmp_max_real = 0
            tmp_max = 0
            for j in range(k_regimes):
                tmp_predicted_joint_probabilities[j] = (
                    prev_filtered_joint_probabilities[j] + regime_transition[i, j])
                if tmp_predicted_joint_probabilities[j] > tmp_max_real:
                    tmp_max_real = tmp_predicted_joint_probabilities[j]
                    tmp_max = tmp_predicted_joint_probabilities[j]

            curr_predicted_joint_probabilities[i] = 0
            for j in range(k_regimes):
                curr_predicted_joint_probabilities[i] = (
                  curr_predicted_joint_probabilities[i] +
                  dexp(tmp_predicted_joint_probabilities[j] - tmp_max))

            curr_predicted_joint_probabilities[i] = (tmp_max +
              dlog(curr_predicted_joint_probabilities[i]))


    # Compute weighted likelihoods f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) * Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1]
    tmp_max_real = 0
    tmp_max = 0
    for i in range(k_regimes_order_p1):
        weighted_likelihoods[i] = (
            curr_predicted_joint_probabilities[i] +
            conditional_likelihoods[i])

        # Compute the maximum for use below in logsumexp
        if weighted_likelihoods[i] > tmp_max_real:
            tmp_max_real = weighted_likelihoods[i]
            tmp_max = weighted_likelihoods[i]

    # Compute the joint likelihood f(y_t | t-1)
    # Again, this is logsumexp, so we use the maximum trick (where the
    # maximum was just computed above)
    joint_likelihoods[t] = 0
    for i in range(k_regimes_order_p1):
        joint_likelihoods[t] = (
          joint_likelihoods[t] +
          dexp(weighted_likelihoods[i] - tmp_max))
    joint_likelihoods[t] = tmp_max + dlog(joint_likelihoods[t])

    # Compute filtered joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t] = (
    #     f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) *
    #     Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] /
    #     f(y_t | t-1))
    for i in range(k_regimes_order_p1):
        # TODO: do I need to worry about some value for joint_likelihoods?
        curr_filtered_joint_probabilities[i] = (
            weighted_likelihoods[i] - joint_likelihoods[t])


def chamilton_filter_log(int nobs, int k_regimes, int order,
                                  np.complex64_t [:,:,:] regime_transition,
                                  np.complex64_t [:,:] conditional_likelihoods,
                                  np.complex64_t [:] joint_likelihoods,
                                  np.complex64_t [:,:] predicted_joint_probabilities,
                                  np.complex64_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, regime_transition_t = 0, time_varying_regime_transition
    cdef:
        # k_regimes_order_m1 is not used when order == 0.
        int k_regimes_order_m1 = k_regimes**max(order - 1, 0)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.complex64_t [:] weighted_likelihoods, tmp_filtered_marginalized_probabilities, tmp_predicted_joint_probabilities
        np.float64_t tmp_max_real
        np.complex64_t tmp_max

    time_varying_regime_transition = regime_transition.shape[2] > 1
    weighted_likelihoods = np.zeros(k_regimes_order_p1, dtype=np.complex64)
    # tmp_filtered_marginalized_probabilities is not used if order == 0.
    tmp_filtered_marginalized_probabilities = np.zeros(k_regimes_order, dtype=np.complex64)
    tmp_predicted_joint_probabilities = np.zeros(k_regimes, dtype=np.complex64)

    with nogil:
        for t in range(nobs):
            if time_varying_regime_transition:
                regime_transition_t = t

            if order > 0:
                # Collapse filtered joint probabilities over the last dimension
                # Pr[S_{t-1}, ..., S_{t-r} | t-1] = \sum_{ S_{t-r-1} } Pr[S_{t-1}, ..., S_{t-r}, S_{t-r-1} | t-1]
                ix = 0
                # tmp_filtered_marginalized_probabilities[:] = 0
                for j in range(k_regimes_order):
                    # This is logsumexp, so we use the maximum trick
                    tmp_max_real = filtered_joint_probabilities[ix, t].real
                    tmp_max = filtered_joint_probabilities[ix, t]
                    for i in range(k_regimes):
                        if filtered_joint_probabilities[ix + i, t].real > tmp_max_real:
                            tmp_max_real = filtered_joint_probabilities[ix + i, t].real
                            tmp_max = filtered_joint_probabilities[ix + i, t]

                    tmp_filtered_marginalized_probabilities[j] = 0
                    for i in range(k_regimes):
                        tmp_filtered_marginalized_probabilities[j] = (
                            tmp_filtered_marginalized_probabilities[j] +
                            zexp(filtered_joint_probabilities[ix, t] - tmp_max))
                        ix = ix + 1
                    tmp_filtered_marginalized_probabilities[j] = (tmp_max +
                      zlog(tmp_filtered_marginalized_probabilities[j]))

            chamilton_filter_log_iteration(t, k_regimes, order,
                                      regime_transition[:, :, regime_transition_t],
                                      weighted_likelihoods,
                                      tmp_filtered_marginalized_probabilities,
                                      conditional_likelihoods[:, t],
                                      joint_likelihoods,
                                      predicted_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t+1],
                                      tmp_predicted_joint_probabilities)


cdef void chamilton_filter_log_iteration(int t, int k_regimes, int order,
                              np.complex64_t [:,:] regime_transition,
                              np.complex64_t [:] weighted_likelihoods,
                              np.complex64_t [:] prev_filtered_marginalized_probabilities,
                              np.complex64_t [:] conditional_likelihoods,
                              np.complex64_t [:] joint_likelihoods,
                              np.complex64_t [:] curr_predicted_joint_probabilities,
                              np.complex64_t [:] prev_filtered_joint_probabilities,
                              np.complex64_t [:] curr_filtered_joint_probabilities,
                              np.complex64_t [:] tmp_predicted_joint_probabilities) noexcept nogil:
    cdef int i, j, k, ix
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float64_t tmp_max_real
        np.complex64_t tmp_max

    # Compute predicted joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] = Pr[S_t | S_{t-1}] * Pr[S_{t-1}, ..., S_{t-r} | t-1]
    if order > 0:
        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    curr_predicted_joint_probabilities[ix] = (
                        prev_filtered_marginalized_probabilities[j * k_regimes_order_m1 + k] +
                        regime_transition[i, j])
                    ix += 1
    else:
        curr_predicted_joint_probabilities[:] = 0
        for i in range(k_regimes):
            # Again, this is logsumexp, so we use the maximum trick
            tmp_max_real = 0
            tmp_max = 0
            for j in range(k_regimes):
                tmp_predicted_joint_probabilities[j] = (
                    prev_filtered_joint_probabilities[j] + regime_transition[i, j])
                if tmp_predicted_joint_probabilities[j].real > tmp_max_real:
                    tmp_max_real = tmp_predicted_joint_probabilities[j].real
                    tmp_max = tmp_predicted_joint_probabilities[j]

            curr_predicted_joint_probabilities[i] = 0
            for j in range(k_regimes):
                curr_predicted_joint_probabilities[i] = (
                  curr_predicted_joint_probabilities[i] +
                  zexp(tmp_predicted_joint_probabilities[j] - tmp_max))

            curr_predicted_joint_probabilities[i] = (tmp_max +
              zlog(curr_predicted_joint_probabilities[i]))


    # Compute weighted likelihoods f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) * Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1]
    tmp_max_real = 0
    tmp_max = 0
    for i in range(k_regimes_order_p1):
        weighted_likelihoods[i] = (
            curr_predicted_joint_probabilities[i] +
            conditional_likelihoods[i])

        # Compute the maximum for use below in logsumexp
        if weighted_likelihoods[i].real > tmp_max_real:
            tmp_max_real = weighted_likelihoods[i].real
            tmp_max = weighted_likelihoods[i]

    # Compute the joint likelihood f(y_t | t-1)
    # Again, this is logsumexp, so we use the maximum trick (where the
    # maximum was just computed above)
    joint_likelihoods[t] = 0
    for i in range(k_regimes_order_p1):
        joint_likelihoods[t] = (
          joint_likelihoods[t] +
          zexp(weighted_likelihoods[i] - tmp_max))
    joint_likelihoods[t] = tmp_max + zlog(joint_likelihoods[t])

    # Compute filtered joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t] = (
    #     f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) *
    #     Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] /
    #     f(y_t | t-1))
    for i in range(k_regimes_order_p1):
        # TODO: do I need to worry about some value for joint_likelihoods?
        curr_filtered_joint_probabilities[i] = (
            weighted_likelihoods[i] - joint_likelihoods[t])


def zhamilton_filter_log(int nobs, int k_regimes, int order,
                                  np.complex128_t [:,:,:] regime_transition,
                                  np.complex128_t [:,:] conditional_likelihoods,
                                  np.complex128_t [:] joint_likelihoods,
                                  np.complex128_t [:,:] predicted_joint_probabilities,
                                  np.complex128_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, regime_transition_t = 0, time_varying_regime_transition
    cdef:
        # k_regimes_order_m1 is not used when order == 0.
        int k_regimes_order_m1 = k_regimes**max(order - 1, 0)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.complex128_t [:] weighted_likelihoods, tmp_filtered_marginalized_probabilities, tmp_predicted_joint_probabilities
        np.float64_t tmp_max_real
        np.complex128_t tmp_max

    time_varying_regime_transition = regime_transition.shape[2] > 1
    weighted_likelihoods = np.zeros(k_regimes_order_p1, dtype=complex)
    # tmp_filtered_marginalized_probabilities is not used if order == 0.
    tmp_filtered_marginalized_probabilities = np.zeros(k_regimes_order, dtype=complex)
    tmp_predicted_joint_probabilities = np.zeros(k_regimes, dtype=complex)

    with nogil:
        for t in range(nobs):
            if time_varying_regime_transition:
                regime_transition_t = t

            if order > 0:
                # Collapse filtered joint probabilities over the last dimension
                # Pr[S_{t-1}, ..., S_{t-r} | t-1] = \sum_{ S_{t-r-1} } Pr[S_{t-1}, ..., S_{t-r}, S_{t-r-1} | t-1]
                ix = 0
                # tmp_filtered_marginalized_probabilities[:] = 0
                for j in range(k_regimes_order):
                    # This is logsumexp, so we use the maximum trick
                    tmp_max_real = filtered_joint_probabilities[ix, t].real
                    tmp_max = filtered_joint_probabilities[ix, t]
                    for i in range(k_regimes):
                        if filtered_joint_probabilities[ix + i, t].real > tmp_max_real:
                            tmp_max_real = filtered_joint_probabilities[ix + i, t].real
                            tmp_max = filtered_joint_probabilities[ix + i, t]

                    tmp_filtered_marginalized_probabilities[j] = 0
                    for i in range(k_regimes):
                        tmp_filtered_marginalized_probabilities[j] = (
                            tmp_filtered_marginalized_probabilities[j] +
                            zexp(filtered_joint_probabilities[ix, t] - tmp_max))
                        ix = ix + 1
                    tmp_filtered_marginalized_probabilities[j] = (tmp_max +
                      zlog(tmp_filtered_marginalized_probabilities[j]))

            zhamilton_filter_log_iteration(t, k_regimes, order,
                                      regime_transition[:, :, regime_transition_t],
                                      weighted_likelihoods,
                                      tmp_filtered_marginalized_probabilities,
                                      conditional_likelihoods[:, t],
                                      joint_likelihoods,
                                      predicted_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t],
                                      filtered_joint_probabilities[:, t+1],
                                      tmp_predicted_joint_probabilities)


cdef void zhamilton_filter_log_iteration(int t, int k_regimes, int order,
                              np.complex128_t [:,:] regime_transition,
                              np.complex128_t [:] weighted_likelihoods,
                              np.complex128_t [:] prev_filtered_marginalized_probabilities,
                              np.complex128_t [:] conditional_likelihoods,
                              np.complex128_t [:] joint_likelihoods,
                              np.complex128_t [:] curr_predicted_joint_probabilities,
                              np.complex128_t [:] prev_filtered_joint_probabilities,
                              np.complex128_t [:] curr_filtered_joint_probabilities,
                              np.complex128_t [:] tmp_predicted_joint_probabilities) noexcept nogil:
    cdef int i, j, k, ix
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float64_t tmp_max_real
        np.complex128_t tmp_max

    # Compute predicted joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] = Pr[S_t | S_{t-1}] * Pr[S_{t-1}, ..., S_{t-r} | t-1]
    if order > 0:
        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    curr_predicted_joint_probabilities[ix] = (
                        prev_filtered_marginalized_probabilities[j * k_regimes_order_m1 + k] +
                        regime_transition[i, j])
                    ix += 1
    else:
        curr_predicted_joint_probabilities[:] = 0
        for i in range(k_regimes):
            # Again, this is logsumexp, so we use the maximum trick
            tmp_max_real = 0
            tmp_max = 0
            for j in range(k_regimes):
                tmp_predicted_joint_probabilities[j] = (
                    prev_filtered_joint_probabilities[j] + regime_transition[i, j])
                if tmp_predicted_joint_probabilities[j].real > tmp_max_real:
                    tmp_max_real = tmp_predicted_joint_probabilities[j].real
                    tmp_max = tmp_predicted_joint_probabilities[j]

            curr_predicted_joint_probabilities[i] = 0
            for j in range(k_regimes):
                curr_predicted_joint_probabilities[i] = (
                  curr_predicted_joint_probabilities[i] +
                  zexp(tmp_predicted_joint_probabilities[j] - tmp_max))

            curr_predicted_joint_probabilities[i] = (tmp_max +
              zlog(curr_predicted_joint_probabilities[i]))


    # Compute weighted likelihoods f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) * Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1]
    tmp_max_real = 0
    tmp_max = 0
    for i in range(k_regimes_order_p1):
        weighted_likelihoods[i] = (
            curr_predicted_joint_probabilities[i] +
            conditional_likelihoods[i])

        # Compute the maximum for use below in logsumexp
        if weighted_likelihoods[i].real > tmp_max_real:
            tmp_max_real = weighted_likelihoods[i].real
            tmp_max = weighted_likelihoods[i]

    # Compute the joint likelihood f(y_t | t-1)
    # Again, this is logsumexp, so we use the maximum trick (where the
    # maximum was just computed above)
    joint_likelihoods[t] = 0
    for i in range(k_regimes_order_p1):
        joint_likelihoods[t] = (
          joint_likelihoods[t] +
          zexp(weighted_likelihoods[i] - tmp_max))
    joint_likelihoods[t] = tmp_max + zlog(joint_likelihoods[t])

    # Compute filtered joint probabilities
    # Pr[S_t, S_{t-1}, ..., S_{t-r} | t] = (
    #     f(y_t | S_t, S_{t-1}, ..., S_{t-r}, t-1) *
    #     Pr[S_t, S_{t-1}, ..., S_{t-r} | t-1] /
    #     f(y_t | t-1))
    for i in range(k_regimes_order_p1):
        # TODO: do I need to worry about some value for joint_likelihoods?
        curr_filtered_joint_probabilities[i] = (
            weighted_likelihoods[i] - joint_likelihoods[t])
